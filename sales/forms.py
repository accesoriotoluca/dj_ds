from django import forms

CHART_CHOICES = (
    ('#1','Bar chart'),
    ('#2','Pie chart'),
    ('#3','Line chart'),
)

RESULT_CHOICES = (
    ('#1','transaction'),
    ('#2','sales date'),
)

# form.Form save add update objects to the database
# form base in the model
# create a model that isnt related to any of other models

"""
? utilizando el formulario estándar de Django. 
Esto significa que cada campo debe ser especificado manualmente, 
y se debe implementar la lógica de validación y almacenamiento de datos por separado. 
* Este enfoque es útil cuando se desea más control sobre la apariencia 
* y el comportamiento del formulario, 
*y cuando no se requiere la integración completa con la base de datos."""

class SalesSearchForm(forms.Form):
    
    date_from = forms.DateField(widget=forms.DateInput(attrs={'type':'date'}))
    date_to = forms.DateField(widget=forms.DateInput(attrs={'type':'date'}))
    chart_type = forms.ChoiceField(choices=CHART_CHOICES)
    results_by = forms.ChoiceField(choices=RESULT_CHOICES)