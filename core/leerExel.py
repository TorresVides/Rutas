"""
leerExel.py

Lectura del archivo Excel de programación semanal.
"""

from pathlib import Path

import pandas as pd

from config import (
    COLUMNAS_OBLIGATORIAS,
    COLUMN_CLIENTE,
    COLUMN_DIA,
    COLUMN_DIRECCION,
    COLUMN_LATITUD,
    COLUMN_LONGITUD,
)

from core.models import Cliente


class ExcelReader:
    """
    Lee el archivo Excel y devuelve una lista de objetos Cliente.
    """

    def leer(self, ruta_excel: str | Path) -> list[Cliente]:
        """
        Lee el archivo Excel.

        Parameters
        ----------
        ruta_excel : str | Path

        Returns
        -------
        list[Cliente]
        """

        ruta = Path(ruta_excel)

        if not ruta.exists():
            raise FileNotFoundError(
                f"No existe el archivo:\n{ruta}"
            )

        try:

            df = pd.read_excel(
                ruta,
                engine="openpyxl"
            )

        except Exception as e:

            raise RuntimeError(
                f"No fue posible leer el Excel.\n\n{e}"
            )

        self._validar_columnas(df)

        clientes = []

        for indice, fila in df.iterrows():

            cliente = Cliente(

                fila_excel=indice + 2,

                dia=self._texto(
                    fila[COLUMN_DIA]
                ),

                nombre=self._texto(
                    fila[COLUMN_CLIENTE]
                ),

                direccion=self._texto(
                    fila[COLUMN_DIRECCION]
                ),

                latitud=self._numero(
                    fila[COLUMN_LATITUD]
                ),

                longitud=self._numero(
                    fila[COLUMN_LONGITUD]
                )

            )

            clientes.append(cliente)

        return clientes

    # =====================================================

    def _validar_columnas(
        self,
        df: pd.DataFrame,
    ):

        columnas = list(df.columns)

        faltantes = []

        for columna in COLUMNAS_OBLIGATORIAS:

            if columna not in columnas:

                faltantes.append(columna)

        if faltantes:

            texto = "\n".join(faltantes)

            raise ValueError(

                "El Excel no contiene las siguientes columnas:\n\n"

                + texto

            )

    # =====================================================

    @staticmethod
    def _texto(valor) -> str:

        if pd.isna(valor):

            return ""

        return str(valor).strip()

    # =====================================================

    @staticmethod
    def _numero(valor) -> float:

        if pd.isna(valor):

            return float("nan")

        try:

            return float(valor)

        except Exception:

            return float("nan")