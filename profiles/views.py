from django.shortcuts import render
from .models import *
from .forms import *

from django.contrib.auth.decorators import login_required

@login_required
def my_profile_view(request):

    profile = Profile.objects.get(user=request.user)

    """
    !request.POST or None:
    *si POST, formulario usa datos para nueva instancia.
    *Si no se envió POST, formulario se creará vacío.

    !request.FILES or None:
    *indicarle al formulario que puede esperar archivos en la solicitud
    *archivo se almacena en la memoria del servidor
    *si POST con archivos, formulario usa archivos para nueva instancia.
    *Si no se enviaron archivos, formulario se creará sin campos de archivo.

    todo si POST (datos y/o archivos), formulario actualiza o crea instancia en Profile
    todo Si POST vacío (ni datos ni archivos): formulario no actualiza o crea.
    todo Si no POST, formulario mostrará datos existentes de perfil de usuario.
    
    ! instance=profile: 
    *si profile tiene datos
    *formulario carga datos
    *Si no formulario carga vacío """
    form = ProfileForm(request.POST or None, request.FILES or None, instance=profile)
    confirm = False

    if form.is_valid():
        form.save()
        confirm = True

    context = {
        'profile':profile,
        'form':form,
        'confirm':confirm,
    }
    return render(request, 'profiles/main.html', context)
