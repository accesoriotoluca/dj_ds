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
#! en su opinion las vistas basadas en funciones son mas legibles que las basadas en clases
def home_view(request):

    sales_df = None
    positions_df = None
    merge_df = None
    df = None
    chart = None
    
    form = SalesSearchForm(request.POST or None)
    #* se está 'tratando' de crear una instancia del formulario mediante una petición POST.
    """
    Cuando envía formulario a través de POST,
    los datos se incluyen en 'carga útil' de petición (POST)
    y se pueden acceder: en el objeto 'request.POST'

    ! La expresión 'request.POST or None': 
    * permitir que el formulario se maneje correctamente
    * en caso de que la petición no incluya 'datos de formulario'
    ? Si la petición POST incluye datos de formulario:
    ? request.POST contendrá esos datos y se utilizarán. 
    ! Si la petición no incluye 'datos de formulario' (como en una petición GET), 
    ! request.POST será None y se creará una instancia vacía del formulario.
    * De esta manera, al pasar request.POST or None como argumento al constructor de SalesSearchForm, 
    * se garantiza que el formulario se inicializará correctamente en ambas situaciones, 
    * es decir, tanto si la petición incluye datos de formulario como si no."""

    if request.method =='POST':

        date_from = request.POST.get('date_from')
        date_to = request.POST.get('date_to')
        chart_type = request.POST.get('chart_type')

        sale_qs = Sale.objects.filter(created__date__lte=date_to, created__date__gte=date_from)

        if len(sale_qs) > 0:

            # dataframe de Lista de datos de la fecha especificada en el formulario
            sales_df = pd.DataFrame(sale_qs.values())

            # en esta parte se establece/formatean datos de sales_df (sales_qs.valores)
            #* apply() se usa para aplicar una función a cada valor en una columna de un DataFrame
            #* sales_df['customer_id'] envía el id a .apply(get_etc)
            sales_df['customer_id'] = sales_df['customer_id'].apply(get_customer_from_id)
            sales_df['salesman_id'] = sales_df['salesman_id'].apply(get_salesman_from_id)

            #* sales_df['created'] = sales_df['created'].apply(lambda x: x.strftime('%d / %b / %y - %A')).str.title()
            sales_df['created'] = sales_df['created'].apply(lambda x: x.strftime('%Y-%m-%d'))

            # axis=1 indica qc quiere cambiar el nombre de las columnas del DataFrame.
            # Si se quisiera cambiar el nombre de las filas, se usaría axis=0
            #* inplace=True modifica directamente el DataFrame existente.
            #* Si inplace=False (x defecto) devuelve un nuevo DataFrame, sin modificar el original.
            sales_df.rename({
                        'id': 'sales_id',
                        'customer_id':'customer',
                        'salesman_id':'salesman',
                    }
                ,axis=1,inplace=True
            )

            """
            ! positions_df = pd.DataFrame(qs.get_positions())
            para iterar por cada posicion de la venta
            *no se puede con en el 'metodo' get positions, 
            *se debe crear un for loop """
            positions_data = []

            #se esta iterando de sales_qs este es un query list, los otros son dataframes.
            #cada sale puede iterar dentro del metodo get_positions del modelo sale
            for sale in sale_qs:

                #* pos = position, esta llamando de cada sale a cada position a cada producto: 
                for pos in sale.get_positions():

                    # esta estableciendo un diccionario de cada atributo x nombre y objeto
                    """
                        * no es necesario referenciar la tabla positions es que.
                        * get_sales_id es de esa tabla y estamos en la tabla sales. 
                        * pero como sales tiene un foreignkey con positions se puede sin hacer referencia, entra directo. """
                    obj = {
                        'sales_id':pos.get_sales_id(),
                        'positions_id':pos.id,
                        'product':pos.product.name,
                        'quantity':pos.quantity,
                        'price':pos.price,
                    }

                    # itera por cada objeto obtenido en el diccionario y lo agrega a la variable
                    positions_data.append(obj)

            # dataframe de lista de datos obtenidos x la iteracion de posiciones y productos en diccionario
            positions_df = pd.DataFrame(positions_data)

            # mergea 2 dataframes por 1 mismo id y se chingo, nose?????, 'aqui me la aplicaron :('
            merge_df = pd.merge(sales_df,positions_df,on='sales_id')

            """
            * agrupan merge_df x la columna "transaction_id"
            * as_index=False para que la columna "transaction_id"
            * no sea el índice del nuevo DataFrame, si no que sea id 0,1,2,3,4,etc.

            ?luego del resultante se escoge 'price'
            agg() a la columna "price" y se usa la función sum()
            para sumar todos los valores en la columna "price"
            para cada grupo de transacciones.
            se almacena en df.
            *tendrá 2 columnas: "transaction_id", "price":
            "transaction_id": identificador de la transacción
            "price": suma total d precios para las filas en merge_df con el mismo "transaction_id" """
            df = merge_df.groupby('transaction_id',as_index=False)['price'].agg('sum')

            
            chart = get_chart(chart_type,df,labels=df['transaction_id'].values)

            # para que lo procese como html
            sales_df = sales_df.to_html() #lista de sales
            positions_df = positions_df.to_html() #lista de posiciones
            merge_df = merge_df.to_html()
            df = df.to_html()

        else: print('no data')

    #! si es POST ↑
    #! si se recibe una solicitud POST para una vista determinada
    #! significa que se está enviando información al servidor para su procesamiento o actualización
    #! Por lo tanto, en este caso, la vista debe procesar los datos enviados en la solicitud POST y actualizar la base de datos según sea necesario.

    #* si es GET:

    # cuando se recibe una solicitud GET para una vista determinada
    # se espera que el servidor devuelva una respuesta que incluya una representación HTML de la información solicitada

    # si la vista es accesible a través de una URL determinada
    # y se hace una solicitud GET
    # Django responderá con la plantilla correspondiente a esa vista

    context ={
        'form':form, # formularios fechas y chart tipe
        'sales_df':sales_df, # lista de sales
        'positions_df':positions_df, # lista de positions
        'merge_df':merge_df,
        'df':df,
        'chart':chart
    }

    return render(request,'sales/home.html',context)


class SaleListView(ListView):

    model = Sale
    template_name = 'sales/main.html'


"""
la vista espera un parámetro llamado pk de forma predeterminada.
! sin necesidad de especificarlo en el parametro de la funcion
clase DetailView diseñada manejar detalles de instancia de modelo
El pk se utiliza para identificar la instancia específica,
por lo que la vista espera un valor pk """
class SaleDetailView(DetailView):
    
    model = Sale
    template_name = 'sales/detail.html'