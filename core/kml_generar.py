"""
kml_generator.py

Generador de archivos KML compatibles con Map Marker.

Este módulo recibe una lista de clientes y genera un archivo KML
que posteriormente puede importarse directamente en Map Marker.

Autor:
"""


from pathlib import Path
import xml.etree.ElementTree as ET
from xml.dom import minidom

from core.models import Cliente

# ==========================================================
# MODELO DE DATOS
# ==========================================================



# ==========================================================
# GENERADOR KML
# ==========================================================

class KMLGenerator:
    """
    Clase encargada de generar archivos KML compatibles con Map Marker.
    """

    def __init__(self):

        # Namespace oficial KML
        self.kml_namespace = "http://www.opengis.net/kml/2.2"

        # Namespace de Google
        self.gx_namespace = "http://www.google.com/kml/ext/2.2"

        ET.register_namespace("", self.kml_namespace)
        ET.register_namespace("gx", self.gx_namespace)

    # ------------------------------------------------------

    def generar(
        self,
        nombre_documento: str,
        nombre_carpeta: str,
        clientes: list,
        archivo_salida: str,
    ):
        """
        Genera un archivo KML.

        Parameters
        ----------

        nombre_documento :
            Nombre del documento KML.

        nombre_carpeta :
            Nombre de la carpeta que aparecerá en Map Marker.

        clientes :
            Lista de objetos Cliente.

        archivo_salida :
            Ruta donde se guardará el archivo.
        """

        # ======================================================
        # Crear nodo raíz
        # ======================================================

        kml = ET.Element(
            "kml",
            {
                "xmlns": self.kml_namespace,
                "xmlns:gx": self.gx_namespace,
            },
        )

        # ======================================================
        # Document
        # ======================================================

        document = ET.SubElement(kml, "Document")

        ET.SubElement(document, "name").text = nombre_documento

        # ======================================================
        # Folder
        # ======================================================

        folder = ET.SubElement(document, "Folder")

        ET.SubElement(folder, "name").text = nombre_carpeta

        # ======================================================
        # Agregar todos los clientes
        # ======================================================

        for cliente in clientes:

            self._crear_placemark(folder, cliente)

        # ======================================================
        # Guardar
        # ======================================================

        xml = self._pretty_xml(kml)

        salida = Path(archivo_salida)

        salida.parent.mkdir(parents=True, exist_ok=True)

        salida.write_text(xml, encoding="utf-8")

    # ------------------------------------------------------

    def _crear_placemark(
        self,
        folder,
        cliente: Cliente,
    ):
        """
        Agrega un marcador al Folder.
        """

        placemark = ET.SubElement(folder, "Placemark")

        # Nombre

        ET.SubElement(
            placemark,
            "name"
        ).text = cliente.nombre

        # Dirección

        ET.SubElement(
            placemark,
            "description"
        ).text = cliente.direccion

        # Punto

        point = ET.SubElement(
            placemark,
            "Point"
        )

        ET.SubElement(
            point,
            "coordinates"
        ).text = f"{cliente.longitud},{cliente.latitud}"

    # ------------------------------------------------------
    def generar_semanal(
        self,
        nombre_documento: str,
        grupos: dict[str, list],
        archivo_salida: str,
    ):
    """
    Genera un único archivo KML con una carpeta por cada día.
    """

        kml = ET.Element(
            "kml",
            {
                "xmlns": self.kml_namespace,
                "xmlns:gx": self.gx_namespace,
            },
        )

        document = ET.SubElement(kml, "Document")

        ET.SubElement(document, "name").text = nombre_documento

        # Crear un Folder por cada día
        for dia, clientes in grupos.items():

         folder = ET.SubElement(document, "Folder")

            ET.SubElement(folder, "name").text = dia

            for cliente in clientes:

                self._crear_placemark(folder, cliente)

        xml = self._pretty_xml(kml)

        salida = Path(archivo_salida)

        salida.parent.mkdir(parents=True, exist_ok=True)

        salida.write_text(
            xml,
            encoding="utf-8",
        )

    # -------------------------------------------------------
    @staticmethod
    def _pretty_xml(root):
        """
        Devuelve el XML bien indentado.
        """

        xml_bytes = ET.tostring(
            root,
            encoding="utf-8",
        )

        reparsed = minidom.parseString(xml_bytes)

        return reparsed.toprettyxml(indent="    ")
