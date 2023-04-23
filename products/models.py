from django.db import models

class Product(models.Model):
    
    name = models.CharField(max_length=120)

    #upload_to='products': inside the media products we´ve another folder called products where to keep images
    image = models.ImageField(upload_to='products',default='no_picture.png')

    # help_text aparece debajo del formulario
    price = models.FloatField(help_text='in US dollars $')

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
        # le llama f-Strings: f" string {variante-valor} string "
        # strftime method
        return f"{self.name}-{self.created.strftime('%d/%m/%Y')}"