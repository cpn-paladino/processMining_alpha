// load file



openFile = function(event, idDivImage) {
    const localServer = 'http://localhost:5000/'
    const prodServer = 'https://alphapaladino.herokuapp.com/'
    const currentServer = localServer
    var input = event.target;
    var reader = new FileReader();

    reader.onload = () => {
        var dataURL = reader.result;        
        var imageElement = document.createElement("img");
        var imageDiv = document.getElementById(idDivImage);
                
        const filename = event.target.files[0].name

        const jsondata = {
           'filename': filename
        }

        console.log(filename)
        
        imageDiv.innerHTML = '';
        //imageElement.src = dataURL;
        
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
            success: function(response) { alert(' arquivo ok!'); 
                alert(response);
            },
            error: function (exr, sender) {
                console.log(exr)
                alert('Erro ao carregar pagina');
            }            
        });

        
        // request proccess xes
        $.ajax({
            type: 'POST',       
            contentType: "application/json; charset=UTF-8",            
            async: false,
            url: currentServer+'process_xes',
            data: JSON.stringify(jsondata),
            success: function(response) { 
                alert('Processado com sucesso!');
            },
            error: function (exr, sender) {
                console.log(exr)
                alert('Error on procces your xml file');
            }            
        });        

        // request append model
        $.ajax({
            type: 'POST',
            async: false,
            contentType: "application/json; charset=UTF-8",            
            url: currentServer+'get_model',
            data: JSON.stringify(jsondata),
            success: function(response) {                 
                imageDiv.classList.add("model-color");
                path = '/static/output/'+response
                imageElement.src = path;                
                imageDiv.appendChild(imageElement)              
            },
            error: function (exr, sender) {
                console.log(exr)
                alert('Error when image is obtained');
            }            
        });        
    };
    reader.readAsDataURL(input.files[0]);
};