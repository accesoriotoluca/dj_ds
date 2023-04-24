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
# modulos y decorators de signal importados
from django.db.models.signals import m2m_changed
from django.dispatch import receiver

#modelos importados de esta app
from .models import *

""" 
# la señal será m2m(manytomany) emisor es 'Sale.positions.through' tabla intermedia:
# envía cada q realiza una acción EDICIÓN en relación manytomany
# como agregar o eliminar objetos relacionados.

*through: especifica d forma explícita, nombre tabla intermedia en relación manytomany

todo. El signal m2m_changed proporciona información sobre la acción realizada:
todo. pre_add, post_add, pre_remove, post_remove, pre_clear, post_clear
todo. los objetos implicados (sender, instance)
    ! los objetos agregados o eliminados (model, pk_set)

# @receiver: registrar la función 'calculate_total_price' como manejador del signal 'm2m_changed' para el modelo 'Sale'

# La def 'calculate_total_price' decorada con @receiver: se ejecuta cada vez q se envíe el signal 'm2m_changed' para una instancia del modelo 'Sale'

# y recibirá los argumentos específicos del signal en los paráms de la función. 

* en 'm2m_changed' se podría usar: 
* parámetro "model" para especificar la clase del modelo relacionado """
@receiver(m2m_changed,sender=Sale.positions.through)
def calculate_total_price(sender,instance,action,**kwargs):

    # se establece inicialmente var total_price a 0
    #? probablemente establecida en cero ya no deja el campo null,empty
    total_price = 0

    # action: string de la acción que se realiza en la tabla intermedia
    # post_add: se agrega un Positión en un Sale
    # post_remove: se quita un Positión de un Sale
    #* parece que se debe especificar ambos jeje
    #* o almenos en este es al agregar y quitar
    #* y no se si existen otras acciones
    if action == 'post_add' or action == 'post_remove':

        # por cada posición/subtotal
        # (lista de productosa con precio y cantidades)
        #! get_positions() llama al método creado en Sales
        #! que obtiene todas las posiciones
        for item in instance.get_positions():

            # var total_price sumará 
            # la iteración de posiciones 
            # en la columna price que igual es una suma
            total_price += item.price

    # me parece que como este llama el modelo 
    # y como este tiene acceso a todos los campos
    # y estamos en el modelo de la instancia a modificar que esta en blank
    # 'total_price' se establece con el resultado de la suma de posiciones
    #? clase instancia puede entrar a la instancia jeje creo... 
    #? Entra, Edita y salva la instancia
    instance.total_price = total_price
    instance.save()