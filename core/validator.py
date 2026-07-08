"""
validator.py

Valida la información proveniente del Excel.
"""

from dataclasses import dataclass
import math

from config import DIAS_SEMANA, NORMALIZACION_DIAS
from core.models import Cliente


# =====================================================
# MODELO DE ERROR
# =====================================================

@dataclass(slots=True)
class ErrorValidacion:

    fila_excel: int

    dia: str

    cliente: str

    campo: str

    valor: str

    mensaje: str


# =====================================================
# VALIDADOR
# =====================================================

class Validator:

    # Campos cuyo error excluye la fila del KML (no se puede
    # ubicar el marcador sin ellos). Un cliente duplicado, en
    # cambio, solo se reporta pero SÍ se incluye en el KML.
    CAMPOS_EXCLUYENTES = {
        "NOMBRE_CLIENTE",
        "DIA_ESPECIFICO",
        "LATITUD_CLIENTE",
        "LONGITUD_CLIENTE",
    }

    def validar(
        self,
        clientes: list[Cliente]
    ) -> list[ErrorValidacion]:

        errores = []

        errores.extend(
            self._validar_individual(clientes)
        )

        errores.extend(
            self._validar_duplicados(clientes)
        )

        return errores

    def separar(
        self,
        clientes: list[Cliente],
    ) -> tuple[list[Cliente], list[ErrorValidacion]]:
        """
        Valida la lista completa y separa los clientes en dos grupos:

        - válidos: se pueden generar en el KML sin problema.
        - excluidos: tienen un error en un campo excluyente
          (nombre, día o coordenadas) y no se incluyen en el KML.

        Los duplicados se reportan como error pero no excluyen al
        cliente del KML.

        Devuelve (clientes_validos, todos_los_errores).
        """

        errores = self.validar(clientes)

        filas_excluidas = {
            error.fila_excel
            for error in errores
            if error.campo in self.CAMPOS_EXCLUYENTES
        }

        validos = [
            cliente
            for cliente in clientes
            if cliente.fila_excel not in filas_excluidas
        ]

        return validos, errores

    # =================================================

    def _validar_individual(
        self,
        clientes: list[Cliente]
    ) -> list[ErrorValidacion]:

        errores = []

        for cliente in clientes:

            errores.extend(
                self._validar_cliente(cliente)
            )

        return errores

    # =================================================

    def _validar_cliente(
        self,
        cliente: Cliente
    ) -> list[ErrorValidacion]:

        errores = []

        # -------------------------------
        # Nombre
        # -------------------------------

        if cliente.nombre == "":

            errores.append(

                ErrorValidacion(

                    fila_excel=cliente.fila_excel,

                    dia=cliente.dia,

                    cliente="",

                    campo="NOMBRE_CLIENTE",

                    valor="",

                    mensaje="El nombre del cliente está vacío."

                )

            )

        # -------------------------------
        # Dirección
        # -------------------------------

        if cliente.direccion == "":

            errores.append(

                ErrorValidacion(

                    fila_excel=cliente.fila_excel,

                    dia=cliente.dia,

                    cliente=cliente.nombre,

                    campo="DIRECCION",

                    valor="",

                    mensaje="La dirección está vacía."

                )

            )

        # -------------------------------
        # Día
        # -------------------------------

        dia = cliente.dia.upper()

        if dia not in NORMALIZACION_DIAS:

            errores.append(

                ErrorValidacion(

                    fila_excel=cliente.fila_excel,

                    dia=cliente.dia,

                    cliente=cliente.nombre,

                    campo="DIA_ESPECIFICO",

                    valor=cliente.dia,

                    mensaje="El día no es válido."

                )

            )

        else:

            cliente.dia = NORMALIZACION_DIAS[dia]

        # -------------------------------
        # Coordenadas en (0, 0)
        # -------------------------------
        # No es un error de rango (0 es técnicamente válido), pero
        # en la práctica (0,0) significa que la geocodificación
        # falló: nunca es una ubicación real en Bogotá.

        if cliente.latitud == 0 and cliente.longitud == 0:

            errores.append(

                ErrorValidacion(

                    fila_excel=cliente.fila_excel,

                    dia=cliente.dia,

                    cliente=cliente.nombre,

                    campo="LATITUD_CLIENTE",

                    valor="0, 0",

                    mensaje="Coordenadas en (0,0): la geocodificación probablemente falló."

                )

            )

            return errores

        # -------------------------------
        # Latitud
        # -------------------------------

        if math.isnan(cliente.latitud):

            errores.append(

                ErrorValidacion(

                    fila_excel=cliente.fila_excel,

                    dia=cliente.dia,

                    cliente=cliente.nombre,

                    campo="LATITUD_CLIENTE",

                    valor="",

                    mensaje="La latitud está vacía."

                )

            )

        elif cliente.latitud < -90 or cliente.latitud > 90:

            errores.append(

                ErrorValidacion(

                    fila_excel=cliente.fila_excel,

                    dia=cliente.dia,

                    cliente=cliente.nombre,

                    campo="LATITUD_CLIENTE",

                    valor=str(cliente.latitud),

                    mensaje="La latitud está fuera del rango permitido."

                )

            )

        # -------------------------------
        # Longitud
        # -------------------------------

        if math.isnan(cliente.longitud):

            errores.append(

                ErrorValidacion(

                    fila_excel=cliente.fila_excel,

                    dia=cliente.dia,

                    cliente=cliente.nombre,

                    campo="LONGITUD_CLIENTE",

                    valor="",

                    mensaje="La longitud está vacía."

                )

            )

        elif cliente.longitud < -180 or cliente.longitud > 180:

            errores.append(

                ErrorValidacion(

                    fila_excel=cliente.fila_excel,

                    dia=cliente.dia,

                    cliente=cliente.nombre,

                    campo="LONGITUD_CLIENTE",

                    valor=str(cliente.longitud),

                    mensaje="La longitud está fuera del rango permitido."

                )

            )

        return errores

    # =================================================

    def _validar_duplicados(
        self,
        clientes: list[Cliente]
    ) -> list[ErrorValidacion]:

        errores = []

        vistos = set()

        for cliente in clientes:

            clave = (

                cliente.nombre.upper(),

                cliente.direccion.upper(),

                cliente.dia.upper(),

            )

            if clave in vistos:

                errores.append(

                    ErrorValidacion(

                        fila_excel=cliente.fila_excel,

                        dia=cliente.dia,

                        cliente=cliente.nombre,

                        campo="CLIENTE",

                        valor=cliente.nombre,

                        mensaje="Cliente duplicado."

                    )

                )

            else:

                vistos.add(clave)

        return errores
