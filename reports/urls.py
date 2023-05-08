from django.urls import path
from .views import *

app_name = 'reports'

"""
~ <> definen parámetros de ruta 
~ / (barra diagonal) separar segmentos d ruta.
~ ^ (circunflejo) indica inicio d ruta.
~ $ (signo de dólar) indica final d ruta.
~ . (punto) separar nombre d archivo y extensión en ruta.
~ ~ (asterisco) indica q cualquier cadena d texto reemplaza valor correspondiente en ruta.
~ + (signo más) indica q 1 o + caracteres pueden aparecer en posición en ruta.
~ ? (signo de interrogación) para indicar q segmento d ruta es opcional. """

urlpatterns = [

    #* 'from_file/' = 'segmento o parámetro de ruta'
    #* <pk> = 'parámetro de ruta' se definen utilizando corchetes angulares < >
    path('from_file/', UploadTemplateView.as_view(), name='from-file'),
    path('upload/', csv_upload_view, name='upload'),
    path('save/', create_report_view, name='create-report'),

    path('', ReportListView.as_view(), name='main'),
    path('<pk>/', ReportDetailView.as_view(), name='detail'),
    path('<pk>/pdf/', render_pdf_view, name='pdf'),

]