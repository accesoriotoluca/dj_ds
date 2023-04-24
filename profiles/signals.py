"""
! Antes de este archivo: 
? User: modulo de django para crear ususarios.
? profiles: es un modelo que creamos
* entonces: la creación de usuarios y de perfiles era independiente

! Despues de este archivo:
* la creacion de perfiles se crea de forma automática al crear un usuario
? usuarios y perfiles tienen una referencia directa?

# signals:
- en este caso la señal tiene referencias de: 
* app (receptora(profiles))/ modelo (receptor(Profile))/ columna(receptora(user))
- sistema de comunicacion entre apps
- forma en Django de detectar eventos en el proyecto
? app emisora "User" > app receptora "Profile"
? emisor: envía un tipo de notificacion acerca de una accion que ocurre. (User informa que la instancia usuario a sido creada)
? receptor: realiza una acción en base a la información recibida. (Profile será creado para ese usuario)

"""
# modulos y decorators de signal y librerias importados
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver

#modelos importados de esta app
from .models import *

""" 
# la señal será despues de guardar 'post_save' y el emisor es 'User'

# @receiver: registrar la función 'post_save_create_profile' como manejador del signal 'post_save' para el modelo 'Profile'

# La def 'post_save_create_profile' decorada con @receiver: se ejecuta cada vez q se envíe el signal 'post_save' para una instancia del modelo 'Profile'

# y recibirá los argumentos específicos del signal en los paráms de la función. 

#todo: para hacer pruebas puedo hacer un modelo:
# todo Creo que no necesita un campo en especial.
# todo simplemente con importar los signal existentes
# todo investigar los parámetros que manejan
# todo ver los datos que arrojan
# todo preguntar a chat x datos que no reconozca
# todo y ya creo
#! las señales parecen ser como código predefinido para intercepta la comunicación interna entre apps/models que entrega info y correspondiente a esa info se puede configurar un todo o accion """
@receiver(post_save, sender=User)

# función "despues de salvar crea perfil": emisor, instancia, creado?, kwargs.
# Kwargs: keyword arguments, pero se puede usar otro nombre, y pasa un diccionario a una función
def post_save_create_profile(sender, instance, created, **Kwargs):

    # entrega un elemento del módulo: django.contrib.auth.models.User
    # sender: especifica clase del modelo q está guardando
    print(sender)

    # string o dato
    # instance: especifica instancia específica del modelo q está guardando
    print(instance)

    # es un booleano
    # true: 'instancia' de emisor es creada
    # False: ejemplo: enviar formulario que no crea una instancia/ en admin: editar o salvar user ya creado
    print(created) 

    if created:
        # se creará/establecerá(set) un objeto? con la 'instancia' en objeto?/columna: user, del modelo Perfil.
        Profile.objects.create(user=instance)