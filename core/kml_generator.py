"""
kml_generator.py

Generador de archivos KML compatibles con Map Marker.
"""

import re
from pathlib import Path
import xml.etree.ElementTree as ET
from xml.dom import minidom

from core.id_generator import IdGenerator
from core.models import Cliente

# Marcador temporal usado para poder insertar CDATA real, ya que
# ElementTree no soporta CDATA de forma nativa (escaparía los
# símbolos < > si se insertan directo como texto).
_CDATA_TOKEN = "@@CDATA:{}@@"


class KMLGenerator:

    KML_NS = "http://www.opengis.net/kml/2.2"
    GX_NS = "http://www.google.com/kml/ext/2.2"

    FOLDER_COLOR = "ff2257ff"
    MARKER_COLOR = "ff00b371"

    def __init__(self):

        self.ids = IdGenerator()

        ET.register_namespace("", self.KML_NS)

        ET.register_namespace("gx", self.GX_NS)

    # =====================================================
    # API pública
    # =====================================================

    def generar(
        self,
        nombre_documento: str,
        nombre_carpeta: str,
        clientes: list[Cliente],
        archivo_salida: str | Path,
    ):
        """
        Genera un único KML con una sola carpeta que contiene
        todos los clientes recibidos.
        """

        kml, document = self._crear_documento(nombre_documento)

        self._agregar_folder(document, nombre_carpeta, clientes)

        self._guardar(kml, archivo_salida)

    def generar_semanal(
        self,
        nombre_documento: str,
        grupos: dict,
        archivo_salida: str | Path,
    ):
        """
        Genera un único KML con una carpeta por cada día
        (una por cada entrada del diccionario `grupos`).
        """

        kml, document = self._crear_documento(nombre_documento)

        for dia, clientes in grupos.items():

            self._agregar_folder(document, dia, clientes)

        self._guardar(kml, archivo_salida)

    # =====================================================
    # Construcción del documento
    # =====================================================

    def _crear_documento(self, nombre: str):

        kml = ET.Element(
            "kml",
            {
                "xmlns": self.KML_NS,
                "xmlns:gx": self.GX_NS,
            },
        )

        document = ET.SubElement(kml, "Document")

        ET.SubElement(document, "name").text = nombre

        return kml, document

    def _agregar_folder(
        self,
        document,
        nombre: str,
        clientes: list[Cliente],
    ):
        """
        Crea una carpeta con su propio estilo (con id único, para
        que varias carpetas puedan convivir en el mismo documento
        sin chocar) y agrega dentro un Placemark por cada cliente.
        """

        folder_id = self.ids.siguiente()

        folder_style_id = f"mm_folder_color_{folder_id}"
        marker_style_id = f"mm_marker_color_{folder_id}"

        self._crear_folder_style(document, folder_style_id)

        folder = ET.SubElement(document, "Folder", {"id": str(folder_id)})

        ET.SubElement(folder, "styleUrl").text = f"#{folder_style_id}"
        ET.SubElement(folder, "name").text = nombre

        self._agregar_extended_data(folder)

        # Un solo estilo de marcador compartido por todos los
        # clientes de esta carpeta (KML estándar permite que
        # múltiples Placemarks referencien el mismo styleUrl).
        self._crear_marker_style(folder, marker_style_id)

        for cliente in clientes:

            self._crear_placemark(folder, cliente, marker_style_id)

    def _crear_folder_style(self, parent, style_id, color=None):

        color = color or self.FOLDER_COLOR

        style = ET.SubElement(parent, "Style", {"id": style_id})

        icon = ET.SubElement(style, "IconStyle")
        ET.SubElement(icon, "color").text = color
        ET.SubElement(icon, "colorMode").text = "normal"
        ET.SubElement(icon, "scale").text = "1"

        line = ET.SubElement(style, "LineStyle")
        ET.SubElement(line, "color").text = color
        ET.SubElement(line, "width").text = "4"

        poly = ET.SubElement(style, "PolyStyle")
        ET.SubElement(poly, "color").text = color

    def _crear_marker_style(self, parent, style_id, color=None):

        color = color or self.MARKER_COLOR

        style = ET.SubElement(parent, "Style", {"id": style_id})

        icon = ET.SubElement(style, "IconStyle")
        ET.SubElement(icon, "color").text = color
        ET.SubElement(icon, "colorMode").text = "normal"
        ET.SubElement(icon, "scale").text = "1"

        line = ET.SubElement(style, "LineStyle")
        ET.SubElement(line, "color").text = color
        ET.SubElement(line, "width").text = "4"

        poly = ET.SubElement(style, "PolyStyle")
        ET.SubElement(poly, "color").text = color

    def _agregar_extended_data(self, folder):

        extended = ET.SubElement(folder, "ExtendedData")

        data = ET.SubElement(
            extended, "Data", {"name": "com_exlyo_mapmarker_piniconcode"}
        )
        ET.SubElement(data, "value").text = "-1"

        data = ET.SubElement(
            extended, "Data", {"name": "com_exlyo_mapmarker_customfields"}
        )
        ET.SubElement(data, "value").text = "[]"

    def _crear_placemark(self, folder, cliente: Cliente, marker_style_id: str):

        placemark_id = self.ids.siguiente()

        placemark = ET.SubElement(folder, "Placemark", {"id": str(placemark_id)})

        ET.SubElement(placemark, "name").text = cliente.nombre

        # El texto real se inserta luego como CDATA (ver _guardar).
        ET.SubElement(placemark, "description").text = _CDATA_TOKEN.format(
            placemark_id
        )
        self._cdata_pendientes = getattr(self, "_cdata_pendientes", {})
        self._cdata_pendientes[str(placemark_id)] = cliente.descripcion

        ET.SubElement(placemark, "phoneNumber")

        point = ET.SubElement(placemark, "Point")
        ET.SubElement(point, "coordinates").text = cliente.coordenadas_kml()

        self._agregar_extended_data(placemark)

        ET.SubElement(placemark, "styleUrl").text = f"#{marker_style_id}"

    # =====================================================
    # Guardado
    # =====================================================

    def _guardar(self, raiz, archivo):

        xml = self._pretty_xml(raiz)

        xml = self._insertar_cdata(xml)

        ruta = Path(archivo)

        ruta.parent.mkdir(parents=True, exist_ok=True)

        ruta.write_text(xml, encoding="utf-8")

    def _pretty_xml(self, elemento):

        xml = ET.tostring(elemento, encoding="utf-8")

        return minidom.parseString(xml).toprettyxml(indent="    ")

    def _insertar_cdata(self, xml: str) -> str:
        """
        Reemplaza los tokens temporales de descripción por el
        bloque CDATA real esperado por Map Marker.
        """

        pendientes = getattr(self, "_cdata_pendientes", {})

        def _reemplazar(match):

            placemark_id = match.group(1)

            texto = pendientes.get(placemark_id, "")

            texto = (
                texto.replace("&", "&amp;")
                .replace("<", "&lt;")
                .replace(">", "&gt;")
            )

            return (
                "<![CDATA["
                f'<pre id="com.exlyo.mapmarker.description_p_tag">{texto}</pre>'
                "]]>"
            )

        xml = re.sub(r"@@CDATA:(\d+)@@", _reemplazar, xml)

        self._cdata_pendientes = {}

        return xml


    