"""
^ importar en color amarillo:
# indica módulos/funciones definidos en Django
~ importar en color verde:
indica 'clases definidas en Django' q 'heredan de otras clases' """

from django.http import HttpRequest, HttpResponse, JsonResponse
"""
! parte d submódulo "http" d Django "manejar solicitudes/respuestas HTTP en app Django":
* HttpRequest:
clase representa solicitud HTTP q llega al servidor web.
Proporciona acceso a datos de solicitud, como:
parámetros d URL, datos d formulario y cabeceras d solicitud
* HttpResponse:
clase representa respuesta HTTP enviada desde el servidor web
Puede contener cualquier contenido, como: 
HTML, texto sin formato, JSON, etc.
También establece cabeceras d respuesta y 'códigos de estado HTTP'
* JsonResponse:
clase q extiende HttpResponse 'permitir creación respuestas HTTP JSON'
para enviar datos JSON desde servidor web a 'app cliente'. """


from django.views.generic import ListView, DetailView, TemplateView
"""
* ListView:
clase 'vista genérica' Al heredar d esta clase,
puede crear vista, q muestre lista objetos en plantilla HTML, d1 DB u otra DB
* DetailView:
clase vista genérica, mostrar detalles d1 objeto en plantilla HTML, d1 DB u otra DB
* TemplateView:
clase vista genérica, renderizar plantilla HTML sin 1 DB """

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
"""
! parte d submódulo "contrib.auth" d Django "agregar autenticación autorización a app"
! buena práctica de seguridad para proteger su aplicación contra posibles vulnerabilidades
* login_required: 
'decorador de función' restringe acceso a vista a usuarios autenticados.
Si usuario no está autenticado, redirige a 'página inicio sesión predeterminada d Django'
! @login_required(login_url=reverse_lazy('miapp:login')):
reverse_lazy genera URL completa d vista de 'inicio d sesión personalizada'
reemplazar 'miapp:login' con ruta d vista personalizada
* LoginRequiredMixin: 
'clase d mezcla d vista' restringir acceso a vista a usuarios autenticados
Al heredar d esta clase, crea vista q solo sea accesible para usuarios autenticados
para redirigir ruta personalizada "login_url = '/mi-login/'" dentro de clase
y si login_url ya esta en uso, entonces "redirect_field_name = '/mi-login/'" """


from django.shortcuts import render, get_object_or_404

from django.template.loader import get_template
from django.utils.dateparse import parse_date
"""
! parte del submódulo "template.loader" y "utils" cargar plantillas y analizar
* get_template:
función q cargar plantilla desde sistema d archivos o desde ubicación en línea, según el argumento
devuelve objeto Template para renderizar plantilla con 1 contexto dado (con datos dinámicos)
* parse_date:
función analizar cadena fecha en objeto d 'fecha Python'
detecta automáticamente formato fecha 'correcto' devuelve objeto fecha 'válido' si cadena fecha es válida """

from django.conf import settings
from datetime import datetime
from xhtml2pdf import pisa
import csv
"""
* django.conf.settings:
módulo accede a configuración d Django definida en settings.py
acceder a variables d configuración como DB, apps instaladas, ajustes d seguridad, etc
* datetime:
módulo d Python, proporciona clases para trabajar con fechas y tiempos
crea objetos d fecha, hora y realizar operaciones con ellos
* xhtml2pdf.pisa:
biblioteca convertir documentos HTML a PDF
genera archivos PDF a partir de plantillas HTML.
!generar facturas o informes
* csv:
módulo d Python, proporciona clases para trabajar con archivos CSV
leer y escribir datos de CSV (valores separados por comas)
!importar, exportar datos """


from profiles.models import *
from .models import *
from .utils import *
from .forms import *

from sales.models import *
from products.models import *
from customers.models import *

"""
class ReportListView(LoginRequiredMixin, ListView):
Define nueva clase llamada 'ReportListView'
clase hereda de LoginRequiredMixin y ListView
requiere que el usuario esté autenticado
y qc está usando vista basada en lista."""
class ReportListView(LoginRequiredMixin, ListView):

    """
    model = Report
    Establece modelo d datos usado en vista en Report """
    model = Report

    """
    template_name = 'reports/main.html'
    Establece plantilla HTML qc usará para renderizar datos d vista
    plantilla c llama 'main.html' esta en carpeta 'reports' dentro de plantillas d app """
    template_name = 'reports/main.html'
    

class ReportDetailView(LoginRequiredMixin, DetailView):
    
    model = Report
    template_name = 'reports/detail.html'


class UploadTemplateView(LoginRequiredMixin, TemplateView):

    template_name = 'reports/from_file.html'


# create_report_view toma 1 objeto HttpRequest como argumento
@login_required
def create_report_view(request: HttpRequest):

    """
    Crea instancia d formulario 'ReportForm'
    le pasamos datos enviados en request.POST, si los hay
    Si está vacío, establecemos formulario en None """
    form = ReportForm(request.POST or None)

    #! no se porque manda el reques 2 veces... 

    """
    ~ request.method == POST
    ~ request.POST == <QueryDict: {'csrfmiddlewaretoken': ['j2m4...'], 'name': ['a'], 'remarks': ['a'], 'image': ['data:image/png;base64,iVBOR...]}>
    ~ request.GET == <QueryDict: {}> <QueryDict: {}>
    ~ request.COOKIES == {'csrftoken': 'pZnG9yn7VP5YuzpKiCm8dl270TACZV6H', 'sessionid': 'yop3y62cftfk51qkijfpucoctd3emkff'} {x2}
    ~ request.path == /reports/save/ /reports/save/
    ~ request.FILES == <MultiValueDict: {}> <MultiValueDict: {}>
    ~ request.user == isaac
    ~ request.META == {diccionario info d solicitud, servidor, como cabeceras HTTP, dirección IP cliente, servidor web usado, etc...}
    ~ request.content_type == multipart/form-data multipart/form-data
    ~ request.content_params == {'boundary': '----WebKitFormBoundaryOTaaVtu8MTqN0vs8'} {x2}
    Comprobamos si petición es petición AJAX (Asynchronous JavaScript and XML)
    verificando si cabecera HTTP 'X-Requested-With' tiene valor 'XMLHttpRequest' """
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':

        """ request.headers ==
        {
            'Content-Length': '21715',
            * longitud d cuerpo d solicitud en bytes
            'Content-Type': 'multipart/form-data; boundary=----WebKitFormBoundarywC0ZWvIlFsVf3Qty',
            * tipo contenido d cuerpo d solicitud, en este caso: formulario multiparte y boundary es el content param
            'Host': '127.0.0.1:8000',
            * nombre, número d puerto d servidor al qc envía solicitud.
            'Connection': 'keep-alive',
            * especifica si se debe mantener abierta conexión entre cliente servidor
            'Sec-Ch-Ua': '"Chromium";v="112", "Google Chrome";v="112", "Not:A-Brand";v="99"',
            * versión d navegador usado x cliente
            *(Secured Client Hints User-Agent)
            'Accept': '*/*',
            * tipo contenido q cliente está dispuesto a aceptar en respuesta, en este caso; acepta cualquier tipo
            'X-Requested-With': 'XMLHttpRequest',
            * si solicitud fue realizada con XMLHttpRequest, es decir, si c realizó petición AJAX
            'Sec-Ch-Ua-Mobile': '*0',
            *'directiva d encabezado' Sec-CH-UA (Secured Client Hints User-Agent)
            *proporcionar info tipo dispositivo qc usa para acceder a sitio
            *Ayuda a sitios a adaptarse a diferentes dispositivos, mejorar experiencia d usuario
            * si navegador usando por cliente es dispositivo móvil
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
            * agente d usuario q realizó solicitud, es decir, navegador usando x cliente
            'Sec-Ch-Ua-Platform': '"Windows"',
            * plataforma del cliente, en este caso, Windows
            *(Secured Client Hints User-Agent)
            'Origin': 'http:*127.0.0.1:8000',
            * origen d la solicitud, es decir, página web q originó la petición
            *para proteger contra ataques CSRF (falsificación de solicitud entre sitios)
            'Sec-Fetch-Site': 'same-origin',
            * sitio de origen de la solicitud
            *si origen d solicitud == origen d recurso solicitado
            *"same-origin" si recurso c solicitó desde mismo origen que sitio actual
            *"cross-origin" si c solicitó desde origen diferente
            *"none" si no c proporcionó información de origen
            *FETCH == BUSCAR
            'Sec-Fetch-Mode': 'cors',
            * modo d navegación usado x cliente para realizar la solicitud
            'Sec-Fetch-Dest': 'empty',
            * destino de la respuesta, en este caso, vacío
            'Referer': 'http:*127.0.0.1:8000/',
            * página web q originó solicitud
            *dirección URL d página q realizó solicitud
            *rastrear navegación d usuario, ayudar a servidores a entender cómo se están usando sus recursos
            'Accept-Encoding': 'gzip, deflate, br',
            * algoritmos d compresión q cliente está dispuesto a aceptar en respuesta
            'Accept-Language': 'en-US,en;q=0.9,es;q=0.8',
            * idiomas q cliente está dispuesto a aceptar en respuesta
            'Cookie': 'csrftoken=pZnG9yn7VP5YuzpKiCm8dl270TACZV6H; sessionid=yop3y62cftfk51qkijfpucoctd3emkff'
            * cookies enviadas con solicitud
        }
        [07/May/2023 08:24:48] "POST /reports/save/ HTTP/1.1" 200 15
        * muestra que solicitud fue recibida con éxito """

        """ 
        name = request.POST.get('name')
        remarks = request.POST.get('remarks')
        Report.objects.create(name=name, remarks=remarks,image=img,author=author)  """

        # del modelo se obtiene el perfin del usuario actualmente autenticado
        author = Profile.objects.get(user=request.user)
        # de POST obtenemos la imagen
        image = request.POST.get('image')
        # a esa imagen del post la decodificamos
        img = get_report_image(image)

        if form.is_valid():

            instance = form.save(commit=False)
            instance.image = img
            instance.author = author
            instance.save()

        """
        ! se que aparece en la consola del navegador...
         JSON c envía si petición AJAX
         mensaje c usa JavaScript despues procesar AJAX
         si envío es en modal, mensaje "send" para cerrar ventana modal """
        return JsonResponse({'msg':'send'})

    # si solicitud AJAX devuelve respuesta JSON
    # Si no hay solicitud AJAX, devuelve respuesta JSON vacía
    return JsonResponse({})


# response['Content-Disposition'] = 'attachment; filename="report.pdf"'
@login_required
def render_pdf_view(request, pk):

    # ruta templete aparte...
    template_path = 'reports/pdf.html'

    # obtiene un reporte con id = param url
    obj = get_object_or_404(Report,pk=pk)
    # contexto que tiene dentro la instancia reporte id
    context = {'obj': obj}

    """
    obtienen plantilla especificada en template_path
    carga la plantilla HTML en memoria para enviarla a pisa """
    template = get_template(template_path) 
    """
    no usa return render() usar get_template() para pisa.PDF
    renderizan plantilla con el contexto para enviarla a pisa """
    html = template.render(context)

    """ 
    crea nueva respuesta HTTP VACIA desde cero
    puedo establecer encabezados, contenido respuesta...
    content_type='application/pdf': establece tipo d contenido
    indica a navegador q espera un PDF
    *response.__dict__ da un poco de info como request.META """
    response = HttpResponse(content_type='application/pdf')
    """ 
    [Content-Disposition] = encabezado HTTP:
    'sugerir' nombre d archivo descargado 'filename="report.pdf"' 
    *mostrarse en navegador: inline... predeterminado
    *descarga archivo: 'attachment;filename="name.pdf"' """
    response['Content-Disposition'] = 'filename="report.pdf"'
    """
    pisa: biblioteca generar PDF de var HTML renderizado
    establece respuesta HTTP como destination d PDF generado """
    pisa_status = pisa.CreatePDF(html, dest=response) #, link_callback=link_callback) 
    """
    pisa es objeto, contiene info 'proceso creación PDF'
    Si error, pisa_status.err == True """
    if pisa_status.err:
       
       """
       </pre>': cadena resultante == texto preformateado:
       facilitar la lectura y la depuración de errores
       Si error, respuesta HTTP con error:
       usuario verá HTML c/error en navegador """
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    
    # finalmente manda http response con pdf y sus carácterísticas
    return response

"""
vista procesa CSV a travez d POST 
y crea instancias d objetos d varios modelos """
@login_required
def csv_upload_view(request):

    if request.method == 'POST':

        #obtiene nombre d csv de post
        csv_file_name = request.FILES.get('file').name

        #obtiene csv de post
        csv_file = request.FILES.get('file')

        #obj == istancia modelo CSV pp: por que son 2 variables, que hace created y que especifican los parametros de get or create, si solo establece el titulo, los demás campos los deja en blanco, o aunque se establesca una variable 1 dato del modelo se guarda mas adelante cuando tiene el archivo guardado en la instancia?
        obj, created = CSV.objects.get_or_create(file_name=csv_file_name)

        # si se creo la instancia pp: created es un valor booleano?
        if created:

            """
            instancia CSV.csv_file = archivo CSV y guarda
            solo tiene 2 campos y 2 created automáticos"""
            obj.csv_file = csv_file
            obj.save()
            
            """
            pp: que hace with?, open sirve para abrir cualquier archivo?, .path es para referencias la ruta donde se encuentra el archivo?, 'r' significa read? as f es para establecerle una variable o seudónimo? 
            
            Abre csv modo read """
            with open(obj.csv_file.path,'r') as f:
                
                #lo lee pp: reader() es una funcion para abrir un csv?
                reader = csv.reader(f)

                #Omitir primera línea d CSV
                reader.__next__()

                # x cada línea d CSV ==
                for row in reader:
                    
                    """
                    x cada línea d CSV obtiene:
                    transaction_id, product, quantity, customer, date """
                    transaction_id = row[0]
                    product = row[1]
                    quantity = int(row[2])
                    customer = row[3]
                    date = datetime.strptime(row[4], '%m/%d/%Y').strftime('%Y-%m-%d')#parse_date(row[4])

                    #pp: en este caso Product.DoesNotExist funciona sin crear una relacion a Product.objects.get(name__iexact=product), es decir except ya sabe que en try se esta buscando un objeto y si el modelo producto se establece como "DoesNotExist", convierte la variable product_obj a None? except se activa con cualquier cosa que se especifique y que suceda en try, sin tener que poner una referencia?

                    #busca product name == product línea CSV
                    try:
                        product_obj = Product.objects.get(name__iexact=product)
                    #Si producto no existe product_obj == None.
                    except Product.DoesNotExist:
                        product_obj = None

                    # Si producto existe
                    if product_obj is not None:
                        """
                        busca Customer == customer fila csv
                        si get '_' == false, si create '_' == true
                        si get: instance Customer
                        si create: new instance Customer"""
                        customer_obj, _ = Customer.objects.get_or_create(name=customer)
                        """
                        busca salesman == salesman user log
                        1 perfil/user, varios compradores """
                        salesman_obj = Profile.objects.get(user=request.user)

                        """ no pregunta get,create:
                        crea instancia posición
                        product, quantity, created == x2 fila csv """
                        position_obj = Position.objects.create(product=product_obj, quantity=quantity, created=date)

                        """
                        busca sale: id,customer,salesma,created == x2 fila csv
                        si get '_' == false, si create '_' == true
                        si get: instance sale
                        si create: new instance sale """
                        sale_obj, _ = Sale.objects.get_or_create(transaction_id=transaction_id, customer=customer_obj, salesman=salesman_obj, created=date)

                        #agrega posiciones a instancia sale
                        #de esta manera x ser M2M
                        sale_obj.positions.add(position_obj)
                        #guarda instancia sale en modelo sale
                        sale_obj.save()
                
                #Si crea 'todas' instancias d modelo:
                #vista devuelve resp HTTP C/objeto JSON c/valor 'ex':False'
                return JsonResponse({'ex':False})

        #Si no crea 'ninguna' instancia d modelo:
        #vista devuelve resp HTTP C/objeto JSON c/valor 'ex':True'
        return JsonResponse({'ex': True})
    """
    como no se realizó ninguna acción:
    para cumplir con especificación de HTTP,
    es suficiente devolver respuesta HTTP vacía"""
    return HttpResponse()


""" request.META ==
{
    ! estos valores son variables d entorno d Windows
    ! útiles: obtener información sobre equipo, ubicar archivos y archivos comunes d sistema o usuario o app o controladores instalados, configuración del servidor
    'ALLUSERSPROFILE': 'C:\\ProgramData', 
    * ubicación d archivos q son comunes a 'todos usuarios d sistema'
    'APPDATA': 'C:\\Users\\isaac\\AppData\\Roaming', 
    * ubicación d archivos d aplicación para usuario actual
    'CHROME_CRASHPAD_PIPE_NAME': '\\\\.\\pipe\\LOCAL\\crashpad_3924_PBHTYITJYYDHFABS', 
    * nombre d pipe d comunicación que usa Chrome para manejar informes d fallos
    'COMMONPROGRAMFILES': 'C:\\Program Files\\Common Files', 
    * ubicación d archivos q son comunes a todas app instaladas en sistema
    'COMMONPROGRAMFILES(X86)': 'C:\\Program Files (x86)\\Common Files', 
    * ubicación d archivos q son comunes a todas app instaladas en sistema, ver. 32 bits
    'COMMONPROGRAMW6432': 'C:\\Program Files\\Common Files', 
    * ubicación d archivos q son comunes a todas app instaladas en sistema, ver. 64 bits
    'COMPUTERNAME': 'DESKTOP-68U2DAM', 
    * nombre de equipo
    'COMSPEC': 'C:\\Windows\\system32\\cmd.exe', 
    * ubicación d intérprete d comandos d Windows
    'DRIVERDATA': 'C:\\Windows\\System32\\Drivers\\DriverData', 
    * ubicación d controladores instalados en sistema
    'FPS_BROWSER_APP_PROFILE_STRING': 'Internet Explorer', 
    * cadena d perfil d app usada por Firefox
    'FPS_BROWSER_USER_PROFILE_STRING': 'Default', 
    * cadena d perfil d usuario usada por Firefox
    'HOMEDRIVE': 'C:', 
    * unidad donde se encuentra directorio personal d usuario
    'HOMEPATH': '\\Users\\isaac', 
    * ruta 'relativa' directorio personal d usuario
    'JD2_HOME': 'C:\\Users\\isaac\\AppData\\Local\\JDownloader 2.0', 
    * ubicación carpeta principal d JDownloader 2
    'LOCALAPPDATA': 'C:\\Users\\isaac\\AppData\\Local', 
    * ubicación archivos d app para usuario actual
    'LOGONSERVER': '\\\\DESKTOP-68U2DAM', 
    * nombre servidor d inicio d sesión q autenticó al usuario
    'NUMBER_OF_PROCESSORS': '4', 
    * número procesadores disponibles en equipo
    'ONEDRIVE': 'C:\\Users\\isaac\\OneDrive', 
    * ubicación carpeta d OneDrive d usuario
    'ORIGINAL_XDG_CURRENT_DESKTOP': 'undefined', 
    * entorno escritorio actual en qc está ejecutando servidor
    'OS': 'Windows_NT', 
    * nombre sistema operativo en qc está ejecutando servidor
    'PATH': 
        !'C:\\Users\\isaac\\Desktop\\A\\dj_ds\\venv/Scripts;
        C:\\Program Files (x86)\\Intel\\Intel(R) Management Engine Components\\iCLS\\;
        C:\\Program Files\\Intel\\Intel(R) Management Engine Components\\iCLS\\;
        C:\\Windows\\system32;
        C:\\Windows;
        C:\\Windows\\System32\\Wbem;
        C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\;
        !C:\\Windows\\System32\\OpenSSH\\;
        C:\\Program Files (x86)\\Intel\\Intel(R) Management Engine Components\\DAL;
        C:\\Program Files\\Intel\\Intel(R) Management Engine Components\\DAL;
        C:\\Program Files (x86)\\Intel\\Intel(R) Management Engine Components\\IPT;
        C:\\Program Files\\Intel\\Intel(R) Management Engine Components\\IPT;
        !C:\\Program Files\\Git\\cmd;
        C:\\Users\\isaac\\AppData\\Local\\Programs\\Python\\Python311\\Scripts\\;
        C:\\Users\\isaac\\AppData\\Local\\Programs\\Python\\Python311\\;
        C:\\Users\\isaac\\AppData\\Local\\Microsoft\\WindowsApps;
        C:\\Users\\isaac\\AppData\\Local\\Programs\\Microsoft VS Code\\bin', 
    * rutas acceso d sistema donde c buscan archivos ejecutables para apps qc llaman desde línea d comandos
    'PATHEXT': '.COM;.EXE;.BAT;.CMD;.VBS;.VBE;.JS;.JSE;.WSF;.WSH;.MSC;.CPL', 
    * extensiones d archivo qc consideran ejecutables en sistema operativo
    'PROCESSOR_ARCHITECTURE': 'AMD64', 
    * arquitectura del procesador
    'PROCESSOR_IDENTIFIER': 'Intel64 Family 6 Model 158 Stepping 9, GenuineIntel', 
    * cadena que describe el procesador en el sistema
    'PROCESSOR_LEVEL': '6', 
    * nivel del procesador
    'PROCESSOR_REVISION': '9e09', 
    * revisión del procesador
    'PROGRAMDATA': 'C:\\ProgramData', 
    * ubicación d datos d programas compartidos
    'PROGRAMFILES': 'C:\\Program Files', 
    * ubicación d programas instalados para sistema operativo
    'PROGRAMFILES(X86)': 'C:\\Program Files (x86)', 
    * ubicación d programas d 32 bits en sistema d 64 bits
    'PROGRAMW6432': 'C:\\Program Files', 
    * ubicación d programas d 64 bits en sistema d 64 bits
    'PSMODULEPATH': 
       'C:\\Users\\isaac\\Documents\\WindowsPowerShell\\Modules;
        C:\\Program Files\\WindowsPowerShell\\Modules;
        C:\\Windows\\system32\\WindowsPowerShell\\v1.0\\Modules', 
    * Ruta módulos de PowerShell
    'PUBLIC': 'C:\\Users\\Public', 
    * Ruta carpeta pública en sistema
    'SESSIONNAME': 'Console', 
    * nombre sesión d inicio d sesión actual
    'SYSTEMDRIVE': 'C:', 
    * unidad d sistema
    'SYSTEMROOT': 'C:\\Windows', 
    * Ruta sistema operativo Windows
    'TEMP': 'C:\\Users\\isaac\\AppData\\Local\\Temp', 
    * Ruta carpeta temporal para usuario actual
    'TMP': 'C:\\Users\\isaac\\AppData\\Local\\Temp', 
    * Ruta carpeta temporal para usuario actual
    'USERDOMAIN': 'DESKTOP-68U2DAM', 
    * nombre dominio d usuario actual
    'USERDOMAIN_ROAMINGPROFILE': 'DESKTOP-68U2DAM', 
    * nombre dominio d usuario actual para perfiles d roaming
    'USERNAME': 'isaac', 
    * usuario actual
    'USERPROFILE': 'C:\\Users\\isaac', 
    * Ruta carpeta d perfil d usuario actual
    'VIRTUAL_ENV': 'C:\\Users\\isaac\\Desktop\\A\\dj_ds\\venv', 
    * Ruta entorno virtual d Python activo (si está activo)
    'WINDIR': 'C:\\Windows', 
    * directorio raíz d Windows
    'TERM_PROGRAM': 'vscode', 
    * programa d terminal qc está usando
    'TERM_PROGRAM_VERSION': '1.78.0', 
    * versión d programa d terminal
    'LANG': 'en_US.UTF-8', 
    * idioma y codificación qc está usando en sesión
    'COLORTERM': 'truecolor', 
    * si programa d terminal es compatible con colores
    'GIT_ASKPASS': 'c:\\Users\\isaac\\AppData\\Local\\Programs\\Microsoft VS Code\\resources\\app\\extensions\\git\\dist\\askpass.sh', 
    * ubicación script d Git usado para solicitar credenciales d autenticación
    'VSCODE_GIT_ASKPASS_NODE': 'C:\\Users\\isaac\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe', 
    * ubicación archivo ejecutable d VS Code usando para ejecutar script d Git
    'VSCODE_GIT_ASKPASS_EXTRA_ARGS': '--ms-enable-electron-run-as-node', 
    * Argumentos adicionales para pasar al script d Git
    'VSCODE_GIT_ASKPASS_MAIN': 'c:\\Users\\isaac\\AppData\\Local\\Programs\\Microsoft VS Code\\resources\\app\\extensions\\git\\dist\\askpass-main.js', 
    * ubicación script d Node.js usando para ejecutar script d Git
    'VSCODE_GIT_IPC_HANDLE': '\\\\.\\pipe\\vscode-git-d7fda8e19a-sock', 
    * ubicación socket IPC usando para comunicarse con proceso d Git
    'VSCODE_INJECTION': '1', 
    * si extensión d VS Code está inyectando código en página
    'DJANGO_SETTINGS_MODULE': 'reports_proj.settings', 
    * módulo d configuración d Django usando para configurar app
    'RUN_MAIN': 'true', 
    * si servidor c está ejecutando en modo d reinicio automático
    'SERVER_NAME': 'DESKTOP-68U2DAM', 
    * nombre del servidor
    'GATEWAY_INTERFACE': 'CGI/1.1', 
    * interfaz d puerta d enlace usanda para comunicarse con servidor
    'SERVER_PORT': '8000', 
    * número d puerto usando x servidor
    'REMOTE_HOST': '', 
    * nombre d host remoto q está accediendo al servidor
    * 'CONTENT_LENGTH': '21715', 
    'SCRIPT_NAME': '', 
    * prefijo d URL d app. Si c usa una app montada en subdirectorio, este valor contendrá 'nombre d subdirectorio'
    'SERVER_PROTOCOL': 'HTTP/1.1', 
    * versión d protocolo usando en solicitud HTTP, >> GENERALMENTE HTTP/1.1 o HTTP/1.0
    'SERVER_SOFTWARE': 'WSGIServer/0.2', 
    * nombre, versión d servidor web usando para procesar solicitud
    'REQUEST_METHOD': 'POST', 
    * método HTTP usando en solicitud, como GET o POST
    'PATH_INFO': '/reports/save/', 
    * ruta 'relativa' d URL d solicitud, no incluye nombre d dominio o prefijo d aplicación relativa x que no incluye c:
    'QUERY_STRING': '', 
    * cadena d consulta d URL d solicitud, 'si está presente'
    'REMOTE_ADDR': '127.0.0.1', 
    * dirección IP d cliente q hizo solicitud. En este caso, solicitud c originó en mismo servidor en qc está ejecutando app Django
    *'CONTENT_TYPE': 'multipart/form-data; boundary=----WebKitFormBoundaryFQgat2daBS2fiBea', 
    *'HTTP_HOST': '127.0.0.1:8000', 
    *'HTTP_CONNECTION': 'keep-alive', 
    *'HTTP_SEC_CH_UA': '"Chromium";v="112", "Google Chrome";v="112", "Not:A-Brand";v="99"', 
    *'HTTP_ACCEPT': '*/*', 
    *'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest', 
    *'HTTP_SEC_CH_UA_MOBILE': '*0', 
    *'HTTP_USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36', 
    *'HTTP_SEC_CH_UA_PLATFORM': '"Windows"', 
    *'HTTP_ORIGIN': 'http:*127.0.0.1:8000', 
    *'HTTP_SEC_FETCH_SITE': 'same-origin', 
    *'HTTP_SEC_FETCH_MODE': 'cors', 
    *'HTTP_SEC_FETCH_DEST': 'empty', 
    *'HTTP_REFERER': 'http:*127.0.0.1:8000/', 
    *'HTTP_ACCEPT_ENCODING': 'gzip, deflate, br', 
    *'HTTP_ACCEPT_LANGUAGE': 'en-US,en;q=0.9,es;q=0.8', 
    *'HTTP_COOKIE': 'csrftoken=pZnG9yn7VP5YuzpKiCm8dl270TACZV6H; sessionid=yop3y62cftfk51qkijfpucoctd3emkff', 
    'wsgi.input': <django.core.handlers.wsgi.LimitedStream object at 0x000001A791B001C0>, 
    * representa entrada d petición HTTP, q es 1 objeto 'stream' q contiene datos enviados en petición
    ! limitar cantidad datos qc pueden leer d cuerpo de solicitud.
    ! evitar ataques d denegación d servicio q podrían surgir 
    ! si c permitiera leer 1 número arbitrariamente grande d datos desde cuerpo de solicitud.
    'wsgi.errors': <_io.TextIOWrapper name='<stderr>' mode='w' encoding='utf-8'>, 
    * flujo d salida d errores q puede ser usando para enviar mensajes d error d servidor
    'wsgi.version': (1, 0), 
    * versión d especificación WSGI qc está usando
    'wsgi.run_once': False, 
    * si servidor c ejecuta 1 sola vez para procesar 1 petición específica
    'wsgi.url_scheme': 'http', 
    * esquema d URL usando en petición, x ejemplo, "http" o "https"
    'wsgi.multithread': True, 
    * si servidor puede manejar varias solicitudes en subprocesos simultáneamente
    'wsgi.multiprocess': False, 
    * si servidor puede manejar varias solicitudes en procesos simultáneamente
    'wsgi.file_wrapper': <class 'wsgiref.util.FileWrapper'>, 
    * 1 objeto usando para envolver archivos en respuesta HTTP
    *'CSRF_COOKIE': 'pZnG9yn7VP5YuzpKiCm8dl270TACZV6H'
} 

{ x2 } """

