"""
! Antes de este archivo: 
? User: modulo de django para crear ususarios.
? profiles: es un modelo que creamos
* entonces: la creación de usuarios y de perfiles era independiente

! Despues de este archivo:
* la creacion de perfiles se crea de forma automática al crear un usuario
? usuarios y perfiles tienen una referencia directa?

# signals:
- la señal se creó en el receptor
- sistema de comunicacion entre apps
- forma en Django de detectar eventos en el proyecto
? app emisora "User" > app receptora "Profile"
? emisor: envía un tipo de notificacion acerca de una accion que ocurre. (User informa que la instancia usuario a sido creada)
? receptor: realiza una acción en base a la información recibida. (Profile será creado para ese usuario)

"""

from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver

from .models import *

# decorador (receiver) la señal será despues de guardar (post_save) y el emisor
@receiver(post_save, sender=User)
# función "despues de salvar crea perfil": emisor, instancia, creado?, kwargs.
# Kwargs: keyword arguments, pero se puede usar otro nombre, y pasa un diccionario a una función
def post_save_create_profile(sender, instance, created, **Kwargs):

    print(sender) # entrega un elemento del módulo: django.contrib.auth.models.User
    print(instance) # string o dato

    # es un booleano
    # true: 'instancia' de emisor es creada
    # False: ejemplo: enviar formulario que no crea una instancia/ en admin: editar o salvar user ya creado
    print(created) 

    if created:
        # se creará/establecerá(set) un objeto? con la 'instancia' en objeto?/columna: user, del modelo Perfil.
        Profile.objects.create(user=instance)