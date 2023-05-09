const csrf = document.getElementsByName('csrfmiddlewaretoken')[0].value
const reportRemarks = document.getElementById('id_remarks')
const reportForm = document.getElementById('report-form')
const modalBody = document.getElementById('modal-body')
const reportName = document.getElementById('id_name')
const reportBtn = document.getElementById('report-btn')


const img = document.getElementById('img')
if(img){
    reportBtn.classList.remove('not_visible')
}


const alertBox = document.getElementById('alert-box')
const handleAlerts = (type, msg) => {
    alertBox.innerHTML = 
        `<div class="alert alert-${type}" role="alert">
            ${msg}
        </div>`
}


reportBtn.addEventListener('click',()=>{

    img.setAttribute('class','w-100')
    modalBody.prepend(img)

    reportForm.addEventListener('submit',e=>{

        e.preventDefault()
        const formData = new FormData()
        formData.append('csrfmiddlewaretoken',csrf)
        formData.append('name',reportName.value)
        formData.append('remarks',reportRemarks.value)
        formData.append('image',img.src)

        $.ajax({

            type:'POST',
            url:'/reports/save/',
            data:formData,

            success: function(response){
                console.log(response)
                handleAlerts('success','report created')
                reportForm.reset()
            },
            
            error: function(error){
                console.log(error)
                handleAlerts('danger','ups... something went wrong')
            },
            
            processData:false,
            contentType:false,
        })
    })
})