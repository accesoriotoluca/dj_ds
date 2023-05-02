
#! where we going to store all the helper functions

# frameworks, bibliotecas, librerías importadas con un seudónimo
import matplotlib.pyplot as plt
import seaborn as sns

# módulos importados de rameworks, bibliotecas, librerías
"""
El módulo io proporciona clases base para trabajar con flujos de entrada/salida. La clase BytesIO del módulo io es una clase de flujo de bytes que se utiliza para crear un objeto de flujo de memoria de bytes. Este objeto se comporta como un archivo en memoria, permitiendo la lectura y escritura de datos binarios en memoria utilizando la misma interfaz que un objeto de archivo normal.

El objeto BytesIO se inicializa sin argumentos y se puede utilizar para almacenar datos binarios en memoria. La clase proporciona métodos para leer y escribir datos binarios en el objeto de flujo, y para obtener la posición actual dentro del flujo. También se pueden utilizar métodos para obtener el contenido completo del objeto de flujo o para obtener una vista de memoria en los datos contenidos en el objeto.

En resumen, el módulo io con su clase BytesIO permite la manipulación de datos binarios en memoria, lo que puede ser útil para realizar operaciones de procesamiento de datos en memoria sin la necesidad de acceder a archivos en disco."""
from io import BytesIO

# módulos importados de python
#* módulo es un archivo q contiene definiciones, declaraciones de variables, funciones y clases
#* base64 proporciona funcionalidad para la codificación y decodificación de datos binarios en formato de texto ASCII. Este módulo se utiliza comúnmente en aplicaciones web y de red para transferir datos binarios, como imágenes, entre sistemas que pueden no ser compatibles con la transferencia de datos binarios directamente. La codificación Base64 es una forma de representar datos binarios utilizando caracteres ASCII seguros para su transferencia a través de redes que solo admiten caracteres ASCII.
import uuid, base64

# modelos importados de otras carpetas
from customers.models import *
from profiles.models import *


#? CUSTOM METHOD/DEF
#? Se llamará de: Modelo Sale > def save()
def generate_code():

    """
    # set the 'code' var, call 'uuid.uuid4()'
    ! c1 = UUid.Uuid4()
    * print(c1): d7fee3f6-7df6-4f5f-982b-baea54597edc

    # grap in a str, to perform the replace
    # replace dashes w/ empy space
    # limit to 12 characters [:12]
    # ! [:12] c establecio en: param(max_length=12)/instance(transaction_id)/model(Sale)
    ! c2 = str(c1).replace('-',)[:12]
    * print(c2): d7fee3f67df6 
    # por ultimo se pasa a MAYÚSCULAS x estética"""
    code = str(uuid.uuid4()).replace('-','').upper()[:12]
    return code


#* val =sales_df['customer_id'] que es el id
def get_salesman_from_id(val):

    # variable = modelo objetos obtener donde columna id sea igual a val que ya dijimos 
    salesman = Profile.objects.get(id=val)

    # obtiene variable/ahora objeto. instancia campo usuario. de foreignkey con tabla user de django. 'username'
    return salesman.user.username


#* val =sales_df['customer_id'] que es el id
def get_customer_from_id(val):

    # variable = modelo objetos obtener donde columna id sea igual a val que ya dijimos 
    customer = Customer.objects.get(id=val)

    # obtiene variable/ahora objeto. instancia campo customer. y ya por que no tiene nada mas
    return customer

#TODO GPT
def get_graph():

    buffer = BytesIO()
    plt.savefig(buffer,format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    graph = base64.b64encode(image_png)
    graph = graph.decode('utf-8')
    buffer.close()
    return graph

def get_key(res_by):
    if res_by == '#1':
        key = 'transaction_id'
    elif res_by == '#2':
        key = 'created'
    return key

#TODO GPT
def get_chart(chart_type,data,results_by,**kwargs):
    
    plt.switch_backend('AGG')

    fig = plt.figure(figsize=(10,4))

    key = get_key(results_by)

    d = data.groupby(key,as_index=False)['total_price'].agg('sum')

    if chart_type == '#1':

        #plt.bar(d[key],d['total_price'])
        sns.barplot(x=key,y='total_price',data=d)

    elif chart_type =='#2':

        plt.pie(data=d,x='total_price', labels=d[key].values)

    elif chart_type =='#3':

        plt.plot(d[key],d['total_price'],color='green',marker='o',linestyle='dashed')

    else:

        print('ups...failed to identify the chart type')


    plt.tight_layout()
    
    chart = get_graph()

    return chart