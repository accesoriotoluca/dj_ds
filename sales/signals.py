"""
! Objetivo de este archivo:
whenever something is added or remove.
from Model(sale)/instance(positions(ManyToManyField)) 
perfom calculation
stored calculation in Model(sale)/instance(total_price)

# signals:
- la señal tiene referencias de:
* app (emisora-receptora(sales))/ modelo (emisor-receptor(Sale))/ columna(emisora-receptora(positions,transaction_id))
- sistema de comunicacion entre apps
- forma en Django de detectar eventos en el proyecto
? app emisora "User" > app receptora "Profile"
? emisor: envía un tipo de notificacion acerca de una accion que ocurre. (User informa que la instancia usuario a sido creada)
? receptor: realiza una acción en base a la información recibida. (Profile será creado para ese usuario)

"""

from django.db.models.signals import m2m_changed
from django.dispatch import receiver

from .models import *

""" 
# la señal será despues de modificar m2m 'post_save' y el emisor es 'User'

# @receiver: registrar la función 'post_save_create_profile' como manejador del signal 'post_save' para el modelo 'Profile'

# La def 'post_save_create_profile' decorada con @receiver: se ejecuta cada vez q se envíe el signal 'pre_save' para una instancia de MyModel

# y recibirá los argumentos específicos del signal en los parámetros de la función. 

* en 'm2m_changed' se podría usar: 
* parámetro "model" para especificar la clase del modelo relacionado """

@receiver(m2m_changed,sender=Sale.positions.through)
def calculate_total_price(sender,instance,action,**kwargs):

    total_price = 0
    if action == 'post_add' or action == 'post_remove':
        for item in instance.get_positions():
            total_price += item.price

    instance.total_price = total_price
    instance.save()