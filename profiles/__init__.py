# indica a Django cuál es la configuración de la aplicación por defecto
# Establece la variable default_app_config con el valor de la ruta como la configuración por defecto de esa app

# __init__.py marca un directorio como un paquete de Python
# 'default_app_config' dentro de __init__.py : es una convención utilizada x Django q permite personalizar la configuración de la app
# 'default_app_config'  puede tener cualquier otro nombre

default_app_config = 'profiles.apps.ProfilesConfig'