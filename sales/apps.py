from django.apps import AppConfig

#! override 'ready' method (anular)
# SalesConfig: clase q organiza partes del proyecto en módulos
# SalesConfig es modificable, puedo poner señalPerfiles_<accion de la señal>, etc.
class SalesConfig(AppConfig):
    
    # para que Django sepa cómo llamar al módulo en el proyecto
    name = 'sales'

    # ready(): función se llama automáticamente al iniciar proyecto carga all signals definidas en módulo "sales"
    def ready(self):
        
        # importamos signals
        import sales.signals