from django.apps import AppConfig


class CustomersConfig(AppConfig):

    # la variante "default_auto_field": especificar el tipo de campo de clave primaria <pk> que Django debe utilizar por defecto en los modelos
    # su valor 'django.db.models.BigAutoField': tipo de campo de pk que utiliza un entero grande (Big Integer) para almacenar la pk. adecuado en dbs manejan gran cantidad de datos, permite manejar pks grandes
    # si esta variable no se establece django establece "BigAutoField" por defecto
    default_auto_field = 'django.db.models.BigAutoField'

    # para que Django sepa cómo llamar al módulo en el proyecto
    name = 'customers'
