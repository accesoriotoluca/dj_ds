/*
?En esta línea se obtiene el valor del token CSRF de Django. Django utiliza el token CSRF para prevenir ataques CSRF (Cross Site Request Forgery). El token CSRF es generado por Django y se incluye en todas las solicitudes POST que se envían al servidor. En esta línea se está obteniendo el valor del token CSRF del campo oculto en el formulario */
const csrf = document.getElementsByName('csrfmiddlewaretoken')[0].value

/*
?Estas líneas se encargan de obtener las referencias a varios elementos HTML en la página. reportRemarks, reportName, reportBtn y reportForm son referencias a diferentes elementos del formulario de informe. modalBody y img son referencias a elementos de la página que se utilizarán más adelante para mostrar la imagen del informe. */
const reportRemarks = document.getElementById('id_remarks')
const reportForm = document.getElementById('report-form')
const modalBody = document.getElementById('modal-body')
const reportName = document.getElementById('id_name')

//usa JavaScript para buscar elemento en página c/ atributo "id" c/ valor "report-btn" y almacena en var "reportBtn"
const reportBtn = document.getElementById('report-btn')

//usa JavaScript para buscar elemento en página c/ atributo "id" c/ valor "img" y almacena en var "img"
const img = document.getElementById('img')

/*
if(img){...}: condicional verifica si variable "img" existe 
y si su valor distinto d "null", "undefined", "false", "0", "", o "NaN"
Si es cierto ejecutará código dentro de llaves
Si no, omitirá código y continuará ejecución d programa*/
if(img){
    /*
    usa JavaScript para quitar clase "not_visible" d elemento almacenado en "reportBtn"
    La clase "not_visible" probablemente tiene reglas CSS q hacen q elemento sea invisible
    o qc oculte d alguna otra manera en página.
    *Al quitar esta clase, el elemento se mostrará en la página web.
    *usos: mostrar botón d informe en página cuando carga imagen en misma página. */
    reportBtn.classList.remove('not_visible')
}

/*
const alertBox = document.getElementById('alert-box')
asigna a constante alertBox elemento HTML q tiene ID alert-box
el elemento HTML 'podría' ser div o cualquier otro elemento que tenga atributo id alert-box
^usa método document.getElementById():
*busca en DOM (Document Object Model) elemento HTML con ID especificado y devuelve referencia a él*/
const alertBox = document.getElementById('alert-box')

//define función handleAlerts toma 2 argumentos: type y msg, para mostrar alertas a usuario
const handleAlerts = (type, msg) => {

    //asigna elemento HTML alertBox el código HTML generado x plantilla 'd cadena literal'
    alertBox.innerHTML = 

        //'La plantilla d cadena literal' usa:
        //valor d argumento type para establecer clase CSS d elemento div
        //valor d argumento msg para establecer texto dentro d elemento div.
        `<div class="alert alert-${type}" role="alert">
            ${msg}
        </div>`
        //usuario verá mensaje d alerta en div con clase CSS
}

//Básicamente lo que hace es crear un formulario de informe que se puede enviar a través de AJAX
/*
?Esta línea agrega un escucha de eventos para el botón de enviar del formulario. Cuando se hace clic en el botón de enviar, se ejecutará el código dentro de la función. */
reportBtn.addEventListener('click',()=>{
    
    /*
    ?Estas líneas establecen la clase CSS de la imagen y luego la insertan en el elemento modalBody. Esto es útil para mostrar una vista previa de la imagen antes de enviar el formulario.*/
    img.setAttribute('class','w-100')
    modalBody.prepend(img)

    /*
    ?Esta línea agrega un escucha de eventos para el envío del formulario. Cuando se envía el formulario, se ejecutará el código dentro de la función. La función e=>{} recibe un objeto evento e que representa el evento de envío del formulario. */
    reportForm.addEventListener('submit',e=>{

        //?Esta línea evita que el formulario se envíe de forma predeterminada. En su lugar, se enviará mediante AJAX.
        e.preventDefault()

        /*
        ?Estas líneas crean un objeto FormData, que es un objeto que representa los datos del formulario. Los valores del formulario se agregan al objeto FormData utilizando el método append(). En este caso, se agregan el token CSRF, el nombre, las observaciones y la imagen del informe. */
        const formData = new FormData()
        formData.append('csrfmiddlewaretoken',csrf)
        formData.append('name',reportName.value)
        formData.append('remarks',reportRemarks.value)
        formData.append('image',img.src)

        /*
        ?VEstas líneas envían el formulario mediante AJAX utilizando jQuery. Se establece el método de solicitud como POST, la URL a la que se enviará el formulario, los datos del formulario y dos funciones de devolución de llamada para manejar la respuesta del servidor. processData y `contentType
        
        ?Esta parte del código utiliza el método de solicitud $.ajax() de jQuery para enviar el formulario de informe a través de AJAX a la URL /reports/save/.

        ?Los siguientes parámetros se pasan a $.ajax()*/
        $.ajax({

            /*
            ?type: este parámetro indica el método HTTP que se utilizará para enviar la solicitud. En este caso, se utiliza el método POST para enviar los datos del formulario.*/
            type:'POST',
            /*
            ?este parámetro especifica la URL a la que se enviará la solicitud.*/
            url:'/reports/save/',
            /*
            ?data: este parámetro especifica los datos que se enviarán con la solicitud. En este caso, se utiliza el objeto FormData que se creó anteriormente para enviar los datos del formulario. */
            data:formData,

            /*
            ?success: esta es una función de devolución de llamada que se ejecuta cuando la solicitud AJAX se completa correctamente. En este caso, la función success simplemente imprime la respuesta del servidor en la consola, muestra una alerta de éxito y resetea el formulario. */
            success: function(response){
                console.log(response)
                handleAlerts('success','report created')
                reportForm.reset()
            },
            
            /*
            ?error: esta es una función de devolución de llamada que se ejecuta cuando la solicitud AJAX falla. En este caso, la función error imprime el error en la consola y muestra una alerta de error. */
            error: function(error){
                console.log(error)
                handleAlerts('danger','ups... something went wrong')
            },
            
            /*
            ?processData y contentType: estos son parámetros opcionales que se establecen en false. processData indica si los datos deben serializarse antes de enviarlos. En este caso, se establece en false porque los datos ya están en el formato adecuado (objeto FormData). contentType indica el tipo de contenido de los datos que se envían. En este caso, se establece en false para que jQuery no establezca automáticamente el tipo de contenido. */
            processData:false,
            contentType:false,
        })
    })
})