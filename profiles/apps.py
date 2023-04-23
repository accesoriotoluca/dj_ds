from django.apps import AppConfig

# override 'ready' method (anular)
# ProfilesConfig: clase q organiza partes del proyecto en módulos
# ProfilesConfig es modificable, puedo poner señalPerfiles_<accion de la señal>, etc.
class ProfilesConfig(AppConfig):

    # para que Django sepa cómo llamar al módulo en el proyecto
    name = 'profiles'

    # ready(): función se llama automáticamente al iniciar proyecto carga all signals definidas en módulo "profiles"
    def ready(self):

        # importamos signals
        import profiles.signals