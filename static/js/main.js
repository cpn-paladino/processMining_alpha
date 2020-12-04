// load file
openFile = function(event, idDivImage) {
    var input = event.target;
    var reader = new FileReader();
    reader.onload = () => {
        var dataURL = reader.result;        
        var imageElement = document.createElement("img");
        var imageDiv = document.getElementById(idDivImage);
        
        imageDiv.innerHTML = '';
        //imageElement.src = dataURL;
        
        form = new FormData();
        form.append('file', event.target.files[0]);         
        
        $.ajax({
            type: 'POST',
            cache: false,
            contentType: false,
            processData: false,
            url: 'http://localhost:5000/uploader',
            data: form,
            success: function(response) { alert(' arquivo ok!'); 
                alert(response);
            },
            error: function (exr, sender) {
                console.log(exr)
                alert('Erro ao carregar pagina');
            }            
        });

        $.ajax({
            type: 'GET',
            cache: false,
            contentType: false,
            processData: false,
            url: 'http://localhost:5000/get_model',
            data: form,
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

        //imageDiv.appendChild(imageElement)        
        // document.getElementById("xes_form").submit();        
    };
    reader.readAsDataURL(input.files[0]);
};