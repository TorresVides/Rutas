"""
models.py

Modelos de datos utilizados en el proyecto.
"""

from dataclasses import dataclass


@dataclass(slots=True)
class Cliente:
    """
    Representa una parada de la programación semanal.

    Cada instancia corresponde a una fila del archivo Excel.
    """

    # Número de fila en el Excel (incluyendo encabezado)
    fila_excel: int

    # Día de la programación
    dia: str

    # Nombre que aparecerá en Map Marker
    nombre: str

    # Dirección que aparecerá como descripción
    direccion: str

    # Coordenadas
    latitud: float
    longitud: float

    def coordenadas_kml(self) -> str:
        """
        Devuelve las coordenadas en el formato esperado por KML.

        Formato:
            longitud,latitud
        """

        return f"{self.longitud},{self.latitud}"

    @property
    def nombre_archivo(self) -> str:
        """
        Nombre limpio del cliente.

        Puede utilizarse más adelante para exportaciones.
        """

        return self.nombre.strip()

    @property
    def descripcion(self) -> str:
        """
        Texto que aparecerá como descripción del marcador.
        """

        return self.direccion.strip()

    def __str__(self):

        return f"{self.nombre} ({self.dia})"