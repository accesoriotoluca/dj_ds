from django.contrib.auth.models import User
from django.db import models

class Profile(models.Model):

    """
    ? OneToOneField:
    * definir relación uno a uno entre dos modelos
    - 1 User > 1 Profile
    - tabla: Perfil, columna 'user' (internamente:'user_id'), tiene los id's predeterminado de tabla: Usuario """
    user = models.OneToOneField(User,on_delete=models.CASCADE)

    # default: aparace dentro del formulario
    bio = models.TextField(default="no bio...")
    
    avatar = models.ImageField(upload_to='avatars',default='no_picture.png')

    """
    ? auto_now_add=True:
    registrar: fecha, hora, creación objeto x primera vez, no se actualiza
    ? auto_now=True:
    registrar: fecha, hora, actualiza cada vez q guarda objeto
    abro, no edito, guardo: llama al método save() que actualiza todos los campos incluyendo 'auto_now'
    * auto_now_add=True, auto_now=True: no aparece en el formulario de admin, interno automático
    * blank=true: si aparece en el formulario de admin, establecer manualmente"""
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Profile of {self.user.username}"