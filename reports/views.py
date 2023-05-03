from django.http import JsonResponse
from django.http import HttpRequest

from django.views.generic import ListView, DetailView
from django.shortcuts import render

from profiles.models import *
from .models import *
from .utils import *
from .forms import *

def create_report_view(request: HttpRequest):

    form = ReportForm(request.POST or None)

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        """
        name = request.POST.get('name')
        remarks = request.POST.get('remarks')
        Report.objects.create(name=name, remarks=remarks,image=img,author=author) """

        author = Profile.objects.get(user=request.user)
        image = request.POST.get('image')
        img = get_report_image(image)

        if form.is_valid():
            instance = form.save(commit=False)
            instance.image = img
            instance.author = author
            instance.save()

        return JsonResponse({'msg':'send'})
    
    return JsonResponse({})


class ReportListView(ListView):

    model = Report
    template_name = 'reports/main.html'
    

class ReportDetailView(DetailView):
    
    model = Report
    template_name = 'reports/detail.html'