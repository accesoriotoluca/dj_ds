//~ valor 'primer elemento' q encuentre en doc HTML con nombre "csrfmiddlewaretoken".
const csrf = document.getElementsByName('csrfmiddlewaretoken')[0].value

//~ asigna elemento HTML que tiene identificador "alert-box".
const alertBox = document.getElementById('alert-box')

/*
~ función "handleAlerts":
* toma dos argumentos: "type" y "msg".
* establece "alertBox" como: 
* 1 cuadro de alerta con:  tipo alerta y mensaje */
const handleAlerts = (type, msg) => {

    alertBox.innerHTML =

        `<div class="alert alert-${type}" role="alert">
            ${msg}
        </div>`

}

//~ desactiva auto-deteción de Dropzone.
Dropzone.autoDiscover = false

/*
~ variable "myDropzone":
*crea nueva instancia de Dropzone. 
* argumento 1 '#my-dropzone' = '#my-dropzone' selector CSS para el contenedor de Dropzone en la página. está en el formulario del templete referencia?
* argumento 2 {} =  objeto con opciones, eventos de Dropzone. */
const myDropzone = new Dropzone('#my-dropzone',{

    //~ ruta y vista en urls.py 'donde enviará archivos cargados':
    url: '/reports/upload/',

    /*
    ~ "init": especifica 1 función de inicialización
    * qc ejecutará cuando cree la instancia de Dropzone.
    * Dentro definen 2 eventos: "sending" y "success" */
    init: function() {

        /*
        ~ evento "sending": c activa cuando c está enviando 1 archivo al servidor.
        * file, xhr, formData: son parámetros internos d API d Dropzone
        * file: archivo que se está enviando actualmente
        * xhr: objeto XMLHttpRequest qc está usando para enviar archivo al servidor
        * formData: objeto FormData qc está usando para recopilar datos del archivo qc enviará al servidor.
        ~ c agrega el valor d "csrf" al objeto 'formData' para incluir token al formulario d carga d archivos
        ~ así Django verifica el token y permite la carga d archivos */
        this.on('sending', function(file, xhr, formData){

            formData.append('csrfmiddlewaretoken', csrf)

        })

        /*
        ~ evento "success": c activa cuando c ha completado carga de archivo en el servidor.
        * Dentro c comprueba si objeto 'response' contiene propiedad "ex".
        * Si es así, llama función "handleAlerts" con tipo alerta: "danger" y mensaje: "File already exists".
        * Si no, llama función "handleAlerts" con tipo alerta: "success" y mensaje: "Your file has been uploaded". */
        this.on('success', function(file, response){

            const ex = response.ex

            if(ex) {

                handleAlerts('danger', 'File already exists'

            )} 
            else {
                
                handleAlerts('success', 'Your file has been uploaded'
                
            )}
            
        })

    },

    //~ "maxFiles" y "maxFilesize" limitan número y tamaño de archivos qc pueden cargar.
    maxFiles: 3,
    maxFilesize: 3,
    //~ especifica tipo d archivo qc puede cargar
    acceptedFiles: '.csv'

})