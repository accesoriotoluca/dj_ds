from django.db import models
from profiles.models import *

class Report(models.Model):
    
    name = models.CharField(max_length=120)

    #upload_to='reports': inside the media reports we´ve another folder called reports where to keep charts base on date from date to
    image = models.ImageField(upload_to='reports',blank=True)

    remarks = models.TextField()

    """
    ? ForeignKey:
    * definir relación uno a muchos entre dos modelos
    - 1 Profile > 1+ Report
    - tabla: Report, columna 'author' (internamente:'author_id'), tiene los id's predeterminado de tabla: Profile """
    author = models.ForeignKey(Profile,on_delete=models.CASCADE)

    """
    ? auto_now_add=True:
    registrar: fecha, hora, creación objeto x primera vez, no se actualiza
    ? auto_now=True:
    registrar: fecha, hora, actualiza cada vez q guarda objeto
    abro, no edito, guardo: llama al método save() que actualiza todos los campos incluyendo 'auto_now'
    * auto_now_add=True, auto_now=True: no aparece en el formulario de admin, interno automático
    * blank=true: si aparece en el formulario de admin, establecer manualmente """
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.name)