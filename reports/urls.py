from django.urls import path
from .views import *

app_name = 'reports'

urlpatterns = [
    path('save/', create_report_view, name='create-report')
]