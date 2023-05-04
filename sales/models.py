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
    #! Si, si elimino producto elimino position/subtotal y la venta queda sin referencia de producto/precio/cantidad.
    #TODO: grabar string en db, en columna q copie y pegue, se eliminan objetos, pero string ('producto/precio/cantidad') xq en ADMIN aun aparece.
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
    # Al parecer esta función se resuelve despues de salvar el formulario
    # save(): convension, guardar instancias de modelos en la base de datos. 
    #! podría ser solo save(self) 
    # *args y **Kwargs no los ocupa por el momento...
    # *'flexible' llamada x n# y tipo de argumentos...
    def save(self, *args, **kwargs):

        #* (then we'll refere to self) price será igual a (ref de precio en esta tabla a> precio del producto) x (cantidad definida en esta tabla)
        self.price = self.product.price * self.quantity

        #? super(): llama a la tabla fuera de esta función, tabla superior fuera d self función
        # super(): convension, llama un método de superclase del objeto actual
        #! podría ser solo save()
        # *self ya esta definido dentro de la función y ya lo toma al inicio al ser llamada
        # *args y **Kwargs no los ocupa por el momento...
        # * mas 'flexible' llamada x n# y tipo de argumentos...
        return super().save(*args, **kwargs)
    
    """
    cant perform a direct forward relation, 
    posiciones no tiene relacion con sale
    pero en la clase sale existe position con manytomany
    se puede realizar reverse relationship
    en este proyecto cada posición pertenecerá a un solo objeto sale"""
    def get_sales_id(self):

        """
        esta es una relacion inversa, 
        se tiene que especificar la case 'siguiente'
        este parámetro podría ser '.all()' y podría ser con 'related name'
        * el nombre de la referencia inversa generada por Django
        * es el nombre en minúsculas del modelo seguido de "_set",
        * lo que en este caso daría como resultado "sale_set"
        * para la relación ManyToManyField entre Sale y Position.
        ! La referencia inversa es una propiedad interna de Django 
        ! y no se refleja como una columna en la tabla de la base de datos,
        ! sino que es una 'propiedad del modelo' que se utiliza para acceder a los objetos relacionados."""
        sale_obj = self.sale_set.first()
        return sale_obj.id

    def __str__(self):
        # le llama f-Strings: f" string {variante-valor} string "
        return f"created: {self.created}, product: {self.product.name} x {self.quantity} pzas"


#! TABLA Sale >>>
# A sale consist in many positions
# Este creo sería como Total del subtotal
class Sale(models.Model):

    # override in utils
    # blank=True: no se pudo dejar solo, se puso null=True
    # Despues se definió en otra función en utils
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
    * para administrar objetos relacionados, manualmente en signals o mediante la escritura de código personalizado.
    * positions.all() puede llamar un query set de productos precios y cantidades

    ! al eliminar 1 posicion:
        elimino: posicion y referencia 'positions_id - sale_id' en tabla interna
        pero en tabla Sale permanece: id, transaction, total, dates, (pero no se sabe, producto, precio y cantidad)

    ! al eliminar 1 producto:
        elimino: producto > posicion (CASCADE) > referencia 'positions_id - sale_id' en tabla interna
        pero en tabla Sale permanece: id, transaction, total, dates, (pero no se sabe, producto, precio y cantidad)"""
    positions = models.ManyToManyField(Position)

    # blank=true: permite que un campo pueda ser dejado en blanco
    # overriding: 'se actualize automáticamente' con una función establecida "the same method"
    #! falta saber porque null 
    #! por que no puede ser blank, debe ser null y null permite dejar un campo como null
    #! como se define total_price?
    #* será calculado a traves de signals
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
        positions_list = ", ".join([f"{p.product.name} x {p.quantity} pzas" for p in self.positions.all()])
        return f"{self.transaction_id} - {self.created}: {positions_list}"

    """
    *método de instancia
     proporciona URL absoluta d1 instancia particular de un modelo
     'URL absoluta'= 'URL completa' incluye "esquema, nombre de dominio, puerto, ruta"
    ! este methodo se llama del templete 'lista'
    ! tanto la vista como el templete y este metodo:
    ! iteran por todas las instancias creando una lista de urls"""
    def get_absolute_url(self):
        
        """
        # crear 'URL inversa' a partir de vista 'detail' dentro de app 'sales'
        ! La URL se construye: 
        * pasando un diccionario de argumentos de palabras clave 
        * en el que la clave es 'pk' (clave principal)
        * y el valor es el valor de la clave principal de la instancia actual del modelo.
        # Esto asegura que la URL generada sea única para cada instancia del modelo.
        ? reverse: busca el patrón de URL ('sales:detail')
        ? en el archivo urls.py de app sales, 
        ? y utiliza el nombre de la vista definido 
        ? en este patrón de URL para construir la URL
        ! En Django al definir un modelo
        ! se crea automáticamente un campo pk/id
        ! pk/id es un número entero qc asigna automáticamente a cada instancia se guarda en db
        ! 'pk' en el diccionario corresponde a la variable en la URL del archivo urls.py
        ! y el parámetro q espera la vista con nombre pk"""
        return reverse('sales:detail', kwargs={'pk':self.pk})
    
    #? to override transaction_id, created
    # Al parecer esta función se resuelve despues de salvar el formulario
    # save(): convension, guardar instancias de modelos en la base de datos.
    #! podría ser solo save(self) 
    # *args y **Kwargs no los ocupa por el momento...
    # *'flexible' llamada x n# y tipo de argumentos...
    def save(self,*args,**kwargs):

        #* 'despues de llenar' si 'transaction_id' fue dejado en blanco:
        if self.transaction_id == '':

            #* se genera un código en utils y se establece en el campo de 'transaction_id'
            self.transaction_id = generate_code()

        #! xq 'created' se debe corroborar como None, creo None es blank :
        if self.created is None:
            
            #* (then we'll refere to self) se genera un código en utils y se establece en el campo de 'transaction_id'
            self.created = timezone.now()

        #? super(): llama a la tabla fuera de esta función, tabla superior fuera d self función
        # super(): convension, llama un método de superclase del objeto actual
        #! podría ser solo save()
        # *self ya esta definido dentro de la función y ya lo toma al inicio al ser llamada
        # *args y **Kwargs no los ocupa por el momento...
        # * mas 'flexible' llamada x n# y tipo de argumentos...
        return super().save(*args,**kwargs)
        
    #* CUSTOM METHOD   
    def get_positions(self):

        #? columna/instancia posiciones, como es un manytomany
        #? devuelve un QUERY SET con '.all()'
        #? lista de todas las referencias que tiene cada Sale
        return self.positions.all()


class CSV(models.Model):
    
    #upload_to='csvs': inside the media csvs we´ve another folder called csvs where to keep csvs
    file_name = models.FileField(upload_to='csvs')

    activated = models.BooleanField(default=False)

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

    #? STR METHOD (método es una función que se define dentro de una clase)
    def __str__(self):
        return str(self.file_name)
