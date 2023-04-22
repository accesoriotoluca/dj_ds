from io import BytesIO
import uuid, base64

import matplotlib.pyplot as plt
import seaborn as sns

from customers.models import *
from profiles.models import *


def generate_code():

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