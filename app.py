"""
app.py

Programa principal.
"""
from pathlib import Path

import config
from core.day_filter import DayFilter
from core.error_report import ErrorReport
from core.excel_reader import ExcelReader
from core.kml_generator import KMLGenerator
from core.validator import Validator


def main():

    print("=" * 60)
    print(" MAP MARKER AUTOMATION ")
    print("=" * 60)

    print("\nLeyendo Excel...\n")

    lector = ExcelReader()

    clientes = lector.leer(config.EXCEL_FILE)

    print(f"Filas leídas en el Excel: {len(clientes)}")

    # -------------------------
    # Filtrar por asesor
    # -------------------------

    clientes = [
        c for c in clientes if c.asesor == str(config.ASESOR_ID)
    ]

    print(
        f"Filas del asesor {config.ASESOR_ID}: {len(clientes)}"
    )

    if not clientes:
        print(
            "\nNo se encontró ninguna fila para ese código de asesor. "
            "Revisa config.ASESOR_ID."
        )
        return

    # -------------------------
    # Validar (sin abortar todo el proceso)
    # -------------------------

    validator = Validator()

    clientes_validos, errores = validator.separar(clientes)

    if errores:

        print()
        print("=" * 60)
        print("ADVERTENCIAS / ERRORES ENCONTRADOS")
        print("=" * 60)

        for error in errores:
            print(
                f"Fila {error.fila_excel}"
                f" | {error.campo}"
                f" | {error.mensaje}"
            )

        reporte = ErrorReport()
        reporte.generar(errores, "salida/errores.xlsx")

        print()
        print(f"Total advertencias/errores: {len(errores)}")
        print(f"Clientes excluidos del KML: {len(clientes) - len(clientes_validos)}")
        print("Se generó el archivo: salida/errores.xlsx")
        print()

    print(f"Clientes válidos para generar KML: {len(clientes_validos)}")

    if not clientes_validos:
        print("\nNo quedó ningún cliente válido para generar KML.")
        return

    print("\nAgrupando por día...\n")

    filtro = DayFilter()

    grupos = filtro.agrupar_por_dia(clientes_validos)

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
        archivo_salida=str(carpeta_salida / "SEMANA.kml"),
    )

    print("\nProceso terminado correctamente.")


if __name__ == "__main__":
    main()