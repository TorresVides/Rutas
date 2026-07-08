"""
app.py

Programa principal.


"""
from core.validator import Validator
from pathlib import Path

from core.day_filter import DayFilter
from core.excel_reader import ExcelReader
from core.kml_generator import KMLGenerator
from core.error_report import ErrorReport


def main():

    print("=" * 60)
    print(" MAP MARKER AUTOMATION ")
    print("=" * 60)

    print("\nLeyendo Excel...\n")

    lector = ExcelReader()

    clientes = lector.leer("data/programacion.xlsx")
    #???????????????????????????
    validator = Validator()

    errores = validator.validar(clientes)
    #_______________--
    if errores:

        print()

        print("=" * 60)
        print("ERRORES ENCONTRADOS")
        print("=" * 60)

        for error in errores:

            print(
                f"Fila {error.fila}"
                f" | {error.campo}"
                f" | {error.mensaje}"
            )

        reporte = ErrorReport()

        reporte.generar(
            errores,
            "salida/errores.xlsx",
        )

        print()
        print(f"Total errores: {len(errores)}")
        print()
        print("Se generó el archivo:")
        print("salida/errores.xlsx")

        return

    #???????????????????????/ 

    print(f"Clientes encontrados: {len(clientes)}")

    print("\nAgrupando por día...\n")

    filtro = DayFilter()

    grupos = filtro.agrupar_por_dia(clientes)

    generador = KMLGenerator()

    carpeta_salida = Path("salida")

    carpeta_salida.mkdir(exist_ok=True)

    # -------------------------
    # Generar un archivo por día
    # -------------------------

    for dia, lista_clientes in grupos.items():

        archivo = carpeta_salida / f"{dia}.kml"

        print(f"Generando {archivo.name} ({len(lista_clientes)} clientes)")

        generador.generar(

            nombre_documento=f"Ruta {dia}",

            nombre_carpeta=dia,

            clientes=lista_clientes,

            archivo_salida=str(archivo),

        )

    # -------------------------
    # Generar archivo semanal
    # -------------------------

    print("\nGenerando archivo semanal...")

    generador.generar_semanal(

        nombre_documento="Programación semanal",

        grupos=grupos,

        archivo_salida=str(
            carpeta_salida / "SEMANA.kml"
        ),

    )

    print("\nProceso terminado correctamente.")


if __name__ == "__main__":
    main()