"""
kml_generator.py

Generador de archivos KML compatibles con Map Marker.
"""

from pathlib import Path
import xml.etree.ElementTree as ET
from xml.dom import minidom

from core.id_generator import IdGenerator


class KMLGenerator:

    KML_NS = "http://www.opengis.net/kml/2.2"
    GX_NS = "http://www.google.com/kml/ext/2.2"

    def __init__(self):

        self.ids = IdGenerator()

        ET.register_namespace("", self.KML_NS)

        ET.register_namespace("gx", self.GX_NS)

    def _crear_documento(
        self,
        nombre: str,
    ):

        kml = ET.Element(

            "kml",

            {

                "xmlns": self.KML_NS,

                "xmlns:gx": self.GX_NS,

            },

        )

        document = ET.SubElement(
            kml,
            "Document",
        )

        ET.SubElement(
            document,
            "name",
        ).text = nombre

        return kml, document

    def _crear_folder_style(
        self,
        document,
        color="ff2257ff",
    ):

        style = ET.SubElement(

            document,

            "Style",

            {

                "id": "folder_style"

            }

        )

        icon = ET.SubElement(
            style,
            "IconStyle",
        )

        ET.SubElement(
            icon,
            "color",
        ).text = color

        ET.SubElement(
            icon,
            "colorMode",
        ).text = "normal"

        ET.SubElement(
            icon,
            "scale",
        ).text = "1"

        line = ET.SubElement(
            style,
            "LineStyle",
        )

        ET.SubElement(
            line,
            "color",
        ).text = color

        ET.SubElement(
            line,
            "width",
        ).text = "4"

        poly = ET.SubElement(
            style,
            "PolyStyle",
        )

        ET.SubElement(
            poly,
            "color",
        ).text = color

        return "#folder_style"

    def _crear_marker_style(
        self,
        document,
        color="ff00b371",
    ):

        style = ET.SubElement(

            document,

            "Style",

            {

                "id": "marker_style"

            }

        )

        icon = ET.SubElement(
            style,
            "IconStyle",
        )

        ET.SubElement(
            icon,
            "color",
        ).text = color

        ET.SubElement(
            icon,
            "colorMode",
        ).text = "normal"

        ET.SubElement(
            icon,
            "scale",
        ).text = "1"

        line = ET.SubElement(
            style,
            "LineStyle",
        )

        ET.SubElement(
            line,
            "color",
        ).text = color

        ET.SubElement(
            line,
            "width",
        ).text = "4"

        poly = ET.SubElement(
            style,
            "PolyStyle",
        )

        ET.SubElement(
            poly,
            "color",
        ).text = color

        return "#marker_style"

    #----------Estlilo Folder
    def _crear_folder(
        self,
        document,
            nombre: str,
    ):

        folder = ET.SubElement(

            document,

            "Folder",

            {

                "id": str(
                    self.ids.siguiente()
                )

            }

        )

        ET.SubElement(
            folder,
            "styleUrl"
        ).text = "#folder_style"

        ET.SubElement(
            folder,
            "name"
        ).text = nombre

        extended = ET.SubElement(
            folder,
            "ExtendedData"
        )

        data = ET.SubElement(

            extended,

            "Data",

            {

                "name":
                "com_exlyo_mapmarker_piniconcode"

            }

        )

        ET.SubElement(
            data,
            "value"
        ).text = "-1"

        data = ET.SubElement(

            extended,

            "Data",

            {

                "name":
                "com_exlyo_mapmarker_customfields"

            }

        )

        ET.SubElement(
            data,
            "value"
        ).text = "[]"

        return folder
    #--------------------
    #----------------Descripcion html
    def _descripcion_html(
        self,
            texto: str,
    ) -> str:

        return (
            "<![CDATA["
            "<pre id=\"com.exlyo.mapmarker.description_p_tag\">"
            f"{texto}"
            "</pre>"
            "]]>"
        )

    #--------------------------------------
    def _guardar(
        self,
        raiz,
        archivo,
    ):

        xml = self._pretty_xml(raiz)

        ruta = Path(archivo)

        ruta.parent.mkdir(
            parents=True,
            exist_ok=True,
            )

        ruta.write_text(
            xml,
            encoding="utf-8",
        )

    def _pretty_xml(
        self,
        elemento,
    ):

        xml = ET.tostring(

            elemento,

            encoding="utf-8",

        )

        return minidom.parseString(
            xml
        ).toprettyxml(indent="    ")

    