"""
^"base64":
codificar y decodificar datos en Base64.
Base64 es método representar datos binarios en ASCII
usa conjunto limitado d caracteres seguros para la transmisión en redes.
codificación Base64 convierte datos binarios en cadena texto qc puede enviar en la red
decodificación Base64 convierte esa cadena de texto en los datos binarios originales¡¡¡ """
import base64, uuid

"""
crear un objeto de 'archivo ContentFile'.
Este objeto se usa para almacenar contenido en memoria
y luego guardarlo en un 'archivo'.
útil:
crear archivo temporal para procesamiento
guardar archivo generado dinámicamente
*trabajar contenido de archivo en memoria en lugar de en disco
*El objeto ContentFile proporciona API simple para leer, escribir contenido del archivo"""
from django.core.files.base import ContentFile

"""
^base64 + ContentFile:
guardar archivos codificados en Base64
útil cuando c necesita enviar archivo en formato Base64:
    como al usar una API web que no admite la carga de archivos:
        Al codificar un archivo en Base64,
        c puede enviar como una cadena de texto 
        luego decodificarlo en el servidor para obtener archivo original"""


#data = data:image/png ; base64,iVBORw0KGgoAA...
def get_report_image(data):
    """
    '_' to discard first part of the string data
    '_' common Python idiom for discarding value";base64" 'string', is not needed
    *ahora es 1 Array y ';base64' se elimina: ['data:image/png' , ',iVBORw0KGgoAA...']
    str_image = base64-encoded image """
    _ , str_image = data.split(';base64')

    #Image in 'str_image' is decoded using base64.b64decode() function.
    #*Ahora es "b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x0..matplotlib..etc."
    decode_img = base64.b64decode(str_image)
    
    # crea string en 'uuid func' - d 10 char, concatena con '.png'
    img_name = str(uuid.uuid4())[:10]+'.png'

    # saved to a file with the name img_name
    #*data ahora es decoded + name
    data = ContentFile(decode_img,name=img_name)

    return data