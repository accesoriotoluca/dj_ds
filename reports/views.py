from django.http import JsonResponse
from django.http import HttpRequest

from django.views.generic import ListView, DetailView, TemplateView
from django.shortcuts import render, get_object_or_404

from profiles.models import *
from .models import *
from .utils import *
from .forms import *

from sales.models import *
from products.models import *
from customers.models import *

from django.conf import settings
from django.http import HttpResponse
from django.template.loader import get_template
from datetime import datetime
from xhtml2pdf import pisa

from django.utils.dateparse import parse_date
import csv

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin


class ReportListView(LoginRequiredMixin, ListView):

    model = Report
    template_name = 'reports/main.html'
    

class ReportDetailView(LoginRequiredMixin, DetailView):
    
    model = Report
    template_name = 'reports/detail.html'


class UploadTemplateView(LoginRequiredMixin, TemplateView):

    template_name = 'reports/from_file.html'


@login_required
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


#* response['Content-Disposition'] = 'attachment; filename="report.pdf"'
@login_required
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


@login_required
def csv_upload_view(request):

    print('file is being send')

    if request.method == 'POST':

        csv_file_name = request.FILES.get('file').name
        csv_file = request.FILES.get('file')
        obj, created = CSV.objects.get_or_create(file_name=csv_file_name)

        if created:

            obj.csv_file = csv_file
            obj.save()
            
            with open(obj.csv_file.path,'r') as f:

                reader = csv.reader(f)
                reader.__next__()

                for row in reader:

                    transaction_id = row[0]
                    product = row[1]
                    quantity = int(row[2])
                    customer = row[3]
                    date = datetime.strptime(row[4], '%m/%d/%Y').strftime('%Y-%m-%d')#parse_date(row[4])#

                    try:
                        product_obj = Product.objects.get(name__iexact=product)
                    except Product.DoesNotExist:
                        product_obj = None
                    
                    if product_obj is not None:
                        # '_' if 'get': false, 'create': true
                        customer_obj, _ = Customer.objects.get_or_create(name=customer)
                        # esta es una lista de venta de un vendedor de un perfil a diferentes compradores
                        salesman_obj = Profile.objects.get(user=request.user)
                        position_obj = Position.objects.create(product=product_obj, quantity=quantity, created=date)

                        sale_obj, _ = Sale.objects.get_or_create(transaction_id=transaction_id, customer=customer_obj, salesman=salesman_obj, created=date)
                        sale_obj.positions.add(position_obj)
                        sale_obj.save()

                return JsonResponse({'ex':False})

        return JsonResponse({'ex': True})

    return HttpResponse()