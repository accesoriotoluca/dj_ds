from django.contrib import admin
from .models import *

admin.site.register(Position)
admin.site.register(Sale)
admin.site.register(CSV)

""" 
! admin.site.register(blank_test_2())
al intentar registrar el modelo blank_test_2
En lugar de pasar la clase del modelo 'blank_test_2'
está pasando una instancia del modelo 'blank_test_2()' """