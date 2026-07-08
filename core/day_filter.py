

"""
day_filter.py

Agrupa, normaliza y ordena clientes por día.
"""

from collections import OrderedDict

from core.models import Cliente


class DayFilter:

    DIAS_SEMANA = [
        "LUNES",
        "MARTES",
        "MIERCOLES",
        "JUEVES",
        "VIERNES",
        "SABADO",
        "DOMINGO",
    ]

    NORMALIZACION = {
        "LUNES": "LUNES",
        "MARTES": "MARTES",
        "MIERCOLES": "MIERCOLES",
        "MIÉRCOLES": "MIERCOLES",
        "JUEVES": "JUEVES",
        "VIERNES": "VIERNES",
        "SABADO": "SABADO",
        "SÁBADO": "SABADO",
        "DOMINGO": "DOMINGO",
    }

    def agrupar_por_dia(
        self,
        clientes: list[Cliente],
    ) -> OrderedDict:

        grupos = {}

        # Crear primero todos los días
        for dia in self.DIAS_SEMANA:
            grupos[dia] = []

        # Agregar clientes
        for cliente in clientes:

            dia = cliente.dia.strip().upper()

            if dia not in self.NORMALIZACION:

                raise ValueError(
                    f"Día inválido encontrado: {cliente.dia}"
                )

            dia = self.NORMALIZACION[dia]

            cliente.dia = dia

            grupos[dia].append(cliente)

        # Eliminar días vacíos
        grupos = {
            dia: lista
            for dia, lista in grupos.items()
            if lista
        }

        return OrderedDict(grupos)