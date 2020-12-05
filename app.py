import os
from flask import Flask, render_template, request, flash, redirect, send_file, send_from_directory 
from alpha_caller import call
#from werkzeug import secure_filename

BASE_FOLDER = os.getcwd()
OUTPUT_FOLDER = os.path.join(BASE_FOLDER,'static','output')
OUTPUT_MODEL_FOLDER = os.path.join(BASE_FOLDER,'models_output')
UPLOAD_FOLDER = os.path.join(BASE_FOLDER,'logs_input')

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'xes','png'}
#app.config['MAX_CONTENT_PATH']

def allowed_file(filename):
  return '.' in filename and \
    filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/favicon.ico', methods = ['GET', 'POST']) 
def favicon(): 
  return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')

# Method to save model
@app.route('/get_model', methods = ['GET', 'POST'])
def get_model():  
  print('get model chamado!')
  data = request.get_json() 
  print(data)
  base_file = data.get('filename')  
  print(base_file)
  if base_file:
    print('entrei?')
    base_file =  base_file.replace('.xes','')
    base_file = base_file+'_alpha_discovery.png'
    print(base_file)
    currentFile = os.path.join(OUTPUT_MODEL_FOLDER, base_file)
    print('current file:')
    print(currentFile)
    newFile = os.path.join(OUTPUT_FOLDER, base_file)  
    print('new file is here:')
    print(newFile)
    import shutil    
    shutil.copy(currentFile, newFile)       
    justFileName = newFile.split('/')
    justFileNameLast = justFileName[-1]
    return justFileNameLast
  else:
    print('error, nao entrei!')
    return 'error, file is None!'

@app.route('/process_xes', methods = ['POST'])
def process_xes():  
  fileName = None
  data = request.get_json()  
  if data:    
    fileName = str(data.get('filename'))  
    if fileName:
      if request.method == 'POST':            
        fullPathFile = os.path.join(app.config['UPLOAD_FOLDER'], fileName)        
        call(fullPathFile)        
        return 'xes file was processed with success'    
  return 'error: None file'



@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():  
  if request.method == 'POST':
    # check if the post request has the file part
    if 'file' not in request.files:
        print('file is not here!')
        flash('No file part')
        return redirect(request.url)               
    # submit an empty part without filename
    file = request.files['file']
    if file.filename == '':
        flash('No selected file')   
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = file.filename
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return 'xes file uploaded successfully'
  else:           
      return 'error your request'

@app.route("/")
def home():
  return render_template("index.html")
  
if __name__ == "__main__":
  #port = int(os.environ.get("PORT", 5000))
  #app.run(host='0.0.0.0', port=port)  
  #app.run(debug=True)
  app.run(debug=True)