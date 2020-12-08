const getElementById = (elementName) =>{
    return document.getElementById(elementName);
}

const setClassDiv = (divName, className) =>{
    let element = getElementById(divName);
    element.classList.add(className)
}

const cleanElement = (divName) =>{
    let element = getElementById(divName)
    element.innerHTML = '';       
}

const hideLoader = () =>{
    let element = getElementById('loading')
    element.classList.value = '';       
    setClassDiv('loading','hideDiv')
}

const showLoader = () =>{
    let element = getElementById('loading')
    element.classList.value = '';       
    setClassDiv('loading','showLoader')
}

const setModelImg = (divName, pathElement) =>{
    let element = getElementById(divName)
    element.classList.add("model-color");
    let imageElement = document.createElement("img");
    imageElement.src = pathElement;                
    element.appendChild(imageElement)        
}

openFile = (event, idDivImage) => {
    const localServer = 'http://localhost:5000/'
    const prodServer = 'https://alphapaladino.herokuapp.com/'
    const currentServer = prodServer
    var input = event.target;
    var reader = new FileReader();

    // show loader
    cleanElement('model-container')
    
    showLoader()
    
    reader.onload = () => {
        var dataURL = reader.result;        
        var imageElement = document.createElement("img");
        

        const filename = event.target.files[0].name
        const jsondata = {
           'filename': filename
        }

        var imageDiv = document.getElementById(idDivImage);           
        //imageDiv.innerHTML = '';       
        
        let form = new FormData();
        form.append('file', event.target.files[0]);         
        
        // request upload file
        $.ajax({
            type: 'POST',
            cache: false,
            async: false,
            contentType: false,
            processData: false,
            url: currentServer+'uploader',
            data: form,
            success: (response) => { 
                console.log('atualizado com sucesso')
                //alert(' arquivo ok!'); 
                //alert(response);
            },
            error: (exr, sender) => {
                console.log(exr)
                //alert('Erro ao carregar pagina');
            }            
        });

        
        // request proccess xes
        $.ajax({
            type: 'POST',       
            contentType: "application/json; charset=UTF-8",            
            async: false,
            url: currentServer+'process_xes',
            data: JSON.stringify(jsondata),
            success: (response) => { 
                console.log('tudo ok')
                //alert('Processado com sucesso!');
            },
            error: (exr, sender) => {
                console.log(exr)
                //alert('Error on procces your xml file');
            }            
        });        

        // request append model
        $.ajax({
            type: 'POST',
            async: false,
            contentType: "application/json; charset=UTF-8",            
            url: currentServer+'get_model',
            data: JSON.stringify(jsondata),
            success: (response) => {   

                const path = '/static/output/'+response
                setModelImg('model-container', path)   

            },
            complete: () => {
                hideLoader()                
            },            
            error: (exr, sender) => {
                console.log(exr)
                alert('Error when image is obtained');
            }            
        });        
    };
    reader.readAsDataURL(input.files[0]);
};