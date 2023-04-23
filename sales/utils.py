
#! where we going to store all the helper functions

# frameworks, bibliotecas, librerías importadas con un seudónimo
import matplotlib.pyplot as plt
import seaborn as sns

# módulos importados de rameworks, bibliotecas, librerías
from io import BytesIO

# módulos importados de python
#* módulo es un archivo q contiene definiciones, declaraciones de variables, funciones y clases
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


def get_salesman_from_id(val):

    salesman = Profile.objects.get(id=val)
    return salesman.user.username


def get_customer_from_id(val):

    customer = Customer.objects.get(id=val)
    return customer


def get_graph():

    buffer = BytesIO()
    plt.savefig(buffer,format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    graph = base64.b64encode(image_png)
    graph = graph.decode('utf-8')
    buffer.close()
    return graph


def get_chart(chart_type,data,**kwargs):
    
    plt.switch_backend('AGG')
    fig = plt.figure(figsize=(10,4))
    if chart_type == '#1':
        #plt.bar(data['transaction'],data['price'])
        sns.barplot(x='transaction',y='price',data=data)
    elif chart_type =='#2':
        labels = kwargs.get('labels')
        plt.pie(data['transaction'],data['price'], labels=labels)
    elif chart_type =='#3':
        plt.plot(data['transaction'],data['price'],color='green',marker='o',linestyle='dashed')
    else:
        print('ups...failed to identify the chart type')
    plt.tight_layout()
    chart = get_graph()
    return chart