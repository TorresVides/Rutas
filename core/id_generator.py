"""
id_generator.py

Generador secuencial de identificadores para elementos KML.
"""


class IdGenerator:

    def __init__(self, inicio: int = 10):

        self._valor = inicio

    def siguiente(self) -> int:

        actual = self._valor

        self._valor += 1

        return actual