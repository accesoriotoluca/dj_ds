"""
^ render:
renderiza HTML en respuesta HTTP
Toma solicitud HTTP, HTML y diccionario d contexto opcional como argumento
devuelve respuesta HTTP con HTML y contexto aplicado
^ redirect:
redirigir a usuario a nueva URL
Toma URL argumento devuelve respuesta HTTP q redirige usuario a URL
^ authenticate:
autenticar usuario en Django
Toma  nombre y contraseña como argumentos
si es exitosa devuelve objeto User, si no lo es None
^ login:
iniciar sesión en Django
Toma solicitud HTTP y objeto User como argumentos
establece 1 cookie d sesión para usuario en solicitud
^ logout:
cerrar sesión d usuario en Django.
Toma solicitud HTTP como argumento
elimina cookie d sesión d usuario en solicitud
^ django.contrib.auth.forms
proporciona formularios predefinidos para la autenticación y control de acceso en Django
^ clase AuthenticationForm:
formulario d inicio d sesión, incluye campos para nombre y contraseña
se puede usar en HTML para permitir que usuarios inicien sesión en app """

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm

def logout_view(request):
    logout(request)
    return redirect('login')

# tomo una solicitud(request) como argumento
def login_view(request):

    #inicia como None, xq no hay mensaje error
    error_message = None

    #formulario d autenticación predeterminado d Django
    form = AuthenticationForm

    #Verifica si solicitud es un POST (si usuario ha enviado formulario)
    if request.method == 'POST':

        #Si solicitud es POST,
        #crea instancia d formulario d autenticación con datos enviados por usuario de formulario
        form = AuthenticationForm(data=request.POST)

        #si formulario es válido
        if form.is_valid():

            # obtiene nombre y contraseña proporcionada x usuario
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            #intenta autenticar usuario con nombre y contraseña
            #si exitosa = objeto User, si no = None
            user = authenticate(username=username, password=password)

            #Si usuario autenticó(== objeto User)
            if user is not None:

                #Inicia sesión en Django con usuario autenticado.
                login(request, user)

                """
                si usuario intenta acceder a página protegida x autenticación
                y no ha iniciado sesión. Django redirige a página d inicio d sesión
                *Y agrega URL q intento acceder en parámetro 'next' de solicitud ejem: '/login/?next=/ventas/'
                *si solicitud incluye URL d redireccionamiento en parámetro 'next' """
                if request.GET.get('next'):

                    #Si hay URL d redireccionamiento, redirige usuario a esa URL
                    return redirect(request.GET.get('next'))
                
                #Si no hay URL de redireccionamiento
                else:

                    #Redirige usuario a página d inicio d módulo ventas
                    return redirect('sales:home')
                
        #Si formulario no es válido:       
        else:

            #Establece mensaje error
            error_message = 'Ups ... something went wrong'

    #diccionario con formulario y mensaje error
    context = {

        'form':form,
        'error_message': error_message,
    }

    #Renderiza plantilla inicio sesión
    #y pasa diccionario context a plantilla para mostrar formulario y mensaje error si corresponde
    return render(request, 'auth/login.html', context)

