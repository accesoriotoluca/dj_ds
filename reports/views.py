from django.http import JsonResponse
from django.http import HttpRequest

from django.views.generic import ListView, DetailView, TemplateView
from django.shortcuts import render, get_object_or_404

from profiles.models import *
from .models import *
from .utils import *
from .forms import *

from sales.models import *

from django.conf import settings
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
import csv

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


#* response['Content-Disposition'] = 'attachment; filename="report.pdf"'
def render_pdf_view(request, pk):

    obj = get_object_or_404(Report,pk=pk)
    template_path = 'reports/pdf.html'
    context = {'obj': obj}
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="report.pdf"'
    template = get_template(template_path)
    html = template.render(context)
    pisa_status = pisa.CreatePDF(
       html, dest=response)#, link_callback=link_callback)
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response

class UploadTemplateView(TemplateView):
    template_name = 'reports/from_file.html'

def csv_upload_view(request):
    print('file is being send')

    if request.method == 'POST':

        csv_file = request.FILES.get('file')
        obj = CSV.objects.create(file_name=csv_file)

        with open(obj.file_name.path,'r') as f:

            reader = csv.reader(f)

            for row in reader:

                print(row, type(row))

    return HttpResponse()