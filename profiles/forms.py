from django import forms
from .models import *

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile

        """ 
        !exclude: c usa en la def de 1 formulario mediante clase Meta:
        * para excluir campos específicos de un modelo del formulario """
        exclude = ('user',)