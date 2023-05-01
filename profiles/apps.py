from django.apps import AppConfig

#! override 'ready' method (anular)
# clase 'ProfilesConfig': organiza partes del proyecto en módulos
# clase 'ProfilesConfig': puede terner otro nombre
class ProfilesConfig(AppConfig):

    # para que Django sepa cómo llamar al módulo en el proyecto
    name = 'profiles'

    # ready(): función se llama automáticamente al iniciar proyecto carga all signals definidas en módulo "profiles"
    def ready(self):

        # importamos signals
        import profiles.signals