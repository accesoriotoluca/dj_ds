from django.apps import AppConfig


class CustomersConfig(AppConfig):
    """
    "default_auto_field": especificar tipo d campo d <pk> q Django debe usar x defecto en modelo
    'django.db.models.BigAutoField': tipo d campo d pk q usa 1 entero grande (Big Integer)
    para manejar gran cantidad de datos, permite manejar pks grandes
    si esta variable no se establece django establece "BigAutoField" por defecto """
    default_auto_field = 'django.db.models.BigAutoField'

    # para que Django sepa cómo llamar al módulo en el proyecto
    name = 'customers'
