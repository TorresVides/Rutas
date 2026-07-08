"""
config.py

Configuración general del proyecto.

Todas las rutas, nombres de columnas y parámetros
globales se centralizan aquí para facilitar el
mantenimiento del sistema.
"""

from pathlib import Path

# ==========================================================
# RUTAS
# ==========================================================

# Carpeta raíz del proyecto
ROOT_DIR = Path(__file__).resolve().parent

# Carpeta donde se almacenan los Excel
DATA_DIR = ROOT_DIR / "data"

# Carpeta donde se generan los KML
OUTPUT_DIR = ROOT_DIR / "salida"

# Excel principal
EXCEL_FILE = DATA_DIR / "programacion.xlsx"

# ==========================================================
# COLUMNAS DEL EXCEL
# ==========================================================

COLUMN_DIA = "DIA_ESPECIFICO"

COLUMN_CLIENTE = "NOMBRE_CLIENTE"

COLUMN_DIRECCION = "DIRECCION"

COLUMN_LATITUD = "LATITUD_CLIENTE"

COLUMN_LONGITUD = "LONGITUD_CLIENTE"

COLUMNAS_OBLIGATORIAS = [
    COLUMN_DIA,
    COLUMN_CLIENTE,
    COLUMN_DIRECCION,
    COLUMN_LATITUD,
    COLUMN_LONGITUD,
]

# ==========================================================
# DÍAS VÁLIDOS
# ==========================================================

DIAS_SEMANA = [
    "LUNES",
    "MARTES",
    "MIERCOLES",
    "JUEVES",
    "VIERNES",
    "SABADO",
    "DOMINGO",
]

# Se aceptan diferentes formas de escribir los días
NORMALIZACION_DIAS = {

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