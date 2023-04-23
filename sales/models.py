# modulos predeterminados
from django.utils import timezone
from django.urls import reverse
from django.db import models

# Modelos creados de otras apps
from products.models import *
from customers.models import *
from profiles.models import *

# Modelos creados en esta app
from .utils import *


# Product times Quantity
# Creo sería como subtotal
class Position(models.Model):

    """
    ? ForeignKey:
    * definir relación uno a muchos entre dos modelos
    - 1 Product > 1+ Position
    - tabla: Position, columna 'product' (internamente:'product_id'), tiene los id's predeterminado de tabla: Product """
    #! cuando se elemine un productose eliminan las posiciones...
    product = models.ForeignKey(Product,on_delete=models.CASCADE)

    quantity = models.PositiveIntegerField()

    # blank=true: permite que un campo pueda ser dejado en blanco
    # overriding: 'se actualize automáticamente' con una función establecida "the same method"
    price = models.FloatField(blank=True)

    """
    ? auto_now_add=True:
    registrar: fecha, hora, creación objeto x primera vez, no se actualiza
    ? auto_now=True:
    registrar: fecha, hora, actualiza cada vez q guarda objeto
    abro, no edito, guardo: llama al método save() que actualiza todos los campos incluyendo 'auto_now'
    * auto_now_add=True, auto_now=True: no aparece en el formulario de admin, establece interno automático
    * blank=true: si aparece en el formulario de admin, establecer manualmente
    * blank=true: permite que un campo pueda ser dejado en blanco
    ! null: permite establecer dato nulo 
    ! diferencia entre este y el de abajo:
    - este tiene null por el error y ahora no puedo quitarlo para corroborar
    - me pide poner default= '(aparentemente del tipo fecha)' y chatgpt adicionar null=False"""
    created = models.DateTimeField(blank=True, null=True)

    #to override price
    # save(): convension, guardar instancias de modelos en la base de datos.
    # super(): convension, llama un método de superclase del objeto actual
    # self: = Position, 
    # *args y **Kwargs no los ocupa por el momento, pero la hace más flexible y permite q sea llamada con cualquier número y tipo de argumentos
    # podría ser solo self
    def save(self, *args, **kwargs):
        self.price = self.product.price * self.quantity
        return super().save(*args, **kwargs)
    
    def get_sales_id(self):
        sale_obj = self.sale_set.first()
        return sale_obj.id

    def __str__(self):
        # le llama f-Strings: f" string {variante-valor} string "
        return f"id: {self.id}, product: {self.product.name}, quantity: {self.quantity}"
        

# A sale consist in many positions
# Este creo sería como Total del subtotal
class Sale(models.Model):

    # blank=True: tambien sera iverride
    transaction_id = models.CharField(max_length=12,blank=True)

    """ 
    ? ManyToManyField:
    * definir una relación muchos a muchos entre dos modelos
    - 1 Sale > 1+ Position y 1 Position > 1+ Sale
    - apesar de definir columna 'positions' no aparece ni 'positions' o 'positions_id'
    - se crea una tabla adicional interna:
         'id': por cada ocurrencia entre Sale y Position
            (si elimina 1 Sale o 1 Position, se eliminan todas las filas/ids relacionadas)
         'position_id': (nuevo nombre en minúsculas) tiene los id's predeterminado de tabla: Position
         'sale_id': (nuevo nombre en minúsculas) tiene los id's predeterminado de tabla: Sale
    * para administrar objetos relacionados, manualmente en signals o mediante la escritura de código personalizado."""
    positions = models.ManyToManyField(Position)

    # blank=true: permite que un campo pueda ser dejado en blanco
    # overriding: 'se actualize automáticamente' con una función establecida "the same method"
    #! falta saber porque null
    total_price = models.FloatField(blank=True, null=True)

    """
    ? ForeignKey:
    * definir relación uno a muchos entre dos modelos
    - 1 Customer > 1+ Sale
    - 1 Profile > 1+ Sale
    - tabla: Sale, columna 'customer' (internamente:'customer_id'), tiene los id's predeterminado de tabla: Customer
    - tabla: Sale, columna 'salesman' (internamente:'salesman_id'), tiene los id's predeterminado de tabla: Profile """
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE)
    salesman = models.ForeignKey(Profile,on_delete=models.CASCADE)

    """
    ? auto_now_add=True:
    registrar: fecha, hora, creación objeto x primera vez, no se actualiza
    ? auto_now=True:
    registrar: fecha, hora, actualiza cada vez q guarda objeto
    abro, no edito, guardo: llama al método save() que actualiza todos los campos incluyendo 'auto_now'
    * auto_now_add=True, auto_now=True: no aparece en el formulario de admin, interno automático
    * blank=true: si aparece en el formulario de admin, establecer manualmente
    * blank=true: permite que un campo pueda ser dejado en blanco
    ! hubo error en 'DateTimeField' > ví que agrego null=True en 'FloatField' > agregué null en 'DateTimeField' > se 'arreglo'
    ! ahora ya no me permite quitar null=True a 'DateTimeField' de arriba
    ! apesar de que este 'DateTimeField' no necesita 'null=True'
    ! aparentemente 'null=True' solo permite dejar el campo como 'null'
    ! incluso algunas bases de datos tratan 'vacias' como 'null' automáticamente
    - este cuenta con una funcion que establece 'now' por eso no queda blank"""

    created = models.DateTimeField(blank=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        
        # este solo entrega 1 de lista productos: return f"Sales for the amount of ${self.total_price}, producto: {self.positions.all()[0].product.name}"
        # y este itera en lista productos crea f-strings en array(autosepara x coma)
        # bonita sintaxis de for con f-strings
        positions_list = ", ".join([f"product: {p.product.name} price: {p.product.price} quantity: {p.quantity}" for p in self.positions.all()])
        return f"Sales for the amount of ${self.total_price}, ventas: {positions_list}"

        

    
    def get_absolute_url(self):
        return reverse('sales:detail', kwargs={'pk':self.pk})
    
    def save(self,*args,**kwargs):
        if self.transaction_id == '':
            self.transaction_id = generate_code()
        if self.created is None:
            self.created = timezone.now()
        return super().save(*args,**kwargs)
        
    def get_positions(self):
        return self.positions.all()


class CSV(models.Model):
    
    file_name = models.FileField(upload_to='csvs')
    activated = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.file_name)
