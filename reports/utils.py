import base64, uuid
from django.core.files.base import ContentFile

"""
In the function get_report_image(), the variable _ is used to discard the first part of the string data, which is the string ";base64". The remaining part of the string, str_image, is a base64-encoded image. The image is decoded using the base64.b64decode() function and saved to a file with the name img_name. The file is then returned.

The use of the variable _ is a common Python idiom for discarding a value. In this case, it is used to discard the ";base64" string, which is not needed."""

def get_report_image(data):
    _ , str_image = data.split(';base64')
    decode_img = base64.b64decode(str_image)
    img_name = str(uuid.uuid4())[:10]+'.png'
    data = ContentFile(decode_img,name=img_name)
    return data