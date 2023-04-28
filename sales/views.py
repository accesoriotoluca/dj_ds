# modulos importados de frameworks, librerias, etc
from django.views.generic import ListView, DetailView
from django.shortcuts import render

# frameworks, librerias,etc. importados con seudónimo
import pandas as pd
import locale

# clase que cambia el idioma
locale.setlocale(locale.LC_ALL, 'es_ES.utf8')

# modelos, formularios y utiles importados de esta app
from .models import *
from .forms import *
from .utils import *

#! utilizo una vista basada en una función
#! por que agregará mucha lógica en esta vista
#! en su opinion las vistas basadas en funciones... no son un cagadero como las vistas basadas en clase, y que chinguen su madre las vistas basadas en clase, asi lo dijo él...
def home_view(request):

    sales_df = None
    positions_df = None
    merge_df = None
    df = None
    chart = None
    
    form = SalesSearchForm(request.POST or None)

    if request.method =='POST':

        date_from = request.POST.get('date_from')
        date_to = request.POST.get('date_to')
        chart_type = request.POST.get('chart_type')

        sale_qs = Sale.objects.filter(
            created__date__lte=date_to,
            created__date__gte=date_from
        )

        if len(sale_qs) > 0:

            sales_df = pd.DataFrame(sale_qs.values())

            sales_df['customer_id'] = sales_df['customer_id'].apply(get_customer_from_id)
            sales_df['salesman_id'] = sales_df['salesman_id'].apply(get_salesman_from_id)
            sales_df['created'] = sales_df['created'].apply(lambda x:x.strftime('%d / %b / %y - %A')).str.title()
            sales_df['updated'] = sales_df['updated'].apply(lambda x:x.strftime('%d / %b / %y - %A')).str.title()

            sales_df.rename({
                        'id':'sales_id',
                        'transaction_id':'transaction',
                        'total_price':'total',
                        'customer_id':'customer',
                        'salesman_id':'salesman',
                    }
                ,axis=1,inplace=True
            )

            positions_data = []

            for sale in sale_qs:
                for pos in sale.get_positions():
                    obj = {
                        'sales_id':pos.get_sales_id(),
                        'positions_id':pos.id,
                        'product':pos.product.name,
                        'quantity':pos.quantity,
                        'price':pos.price,
                    }
                    positions_data.append(obj)

            positions_df = pd.DataFrame(positions_data)
            merge_df = pd.merge(sales_df,positions_df,on='sales_id')
            df = merge_df.groupby('transaction',as_index=False)['price'].agg('sum')
            chart = get_chart(chart_type,df,labels=df['transaction'].values)

            sales_df = sales_df.to_html()
            positions_df = positions_df.to_html()
            merge_df = merge_df.to_html()
            df = df.to_html()

        else:

            print('no data')

    context ={
        'form':form,
        'sales_df':sales_df,
        'positions_df':positions_df,
        'merge_df':merge_df,
        'df':df,
        'chart':chart
    }

    return render(request,'sales/home.html',context)


class SaleListView(ListView):

    model = Sale
    template_name = 'sales/main.html'


class SaleDetailView(DetailView):
    
    model = Sale
    template_name = 'sales/detail.html'