import os
from flask import Flask, render_template, request, flash, redirect, send_file, send_from_directory, request_finished
from alpha_caller import call
from multiprocessing import Process
import threading
import time

BASE_FOLDER = os.getcwd()
OUTPUT_MODEL_FOLDER = os.path.join(BASE_FOLDER,'models_output')
UPLOAD_FOLDER = os.path.join(BASE_FOLDER,'logs_input')
OUTPUT_FOLDER = os.path.join(BASE_FOLDER,'static','output')

app = Flask(__name__)


app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'xes'}


def generateFilesList(mainName):
  files = []
  xesPath = UPLOAD_FOLDER
  outputPath = OUTPUT_MODEL_FOLDER
  staticPath = OUTPUT_FOLDER
  files.append(os.path.join(xesPath, mainName+'.xes'))
  files.append(os.path.join(xesPath, mainName+'_cleaned.xes'))  
  files.append(os.path.join(outputPath, mainName+'_alpha_discovery.png'))
  files.append(os.path.join(staticPath, mainName+'_alpha_discovery.png'))
  return files


def background_remove(files):
  task = Process(target=removeFiles, args=files)
  task.start()  
    
def removeFiles(*files):
  now = time.time()
  time.sleep(200)
  for path in files:
    os.remove(path)

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
    filenameOutExtension =  base_file.replace('.xes','')
    base_file = filenameOutExtension+'_alpha_discovery.png'    
    currentFile = os.path.join(OUTPUT_MODEL_FOLDER, base_file)
    newFile = os.path.join(OUTPUT_FOLDER, base_file)  
    import shutil    
    shutil.copy(currentFile, newFile)       
    justFileName = newFile.split('/')
    justFileNameLast = justFileName[-1]    
    filesToRemove = generateFilesList(filenameOutExtension)
    #p = Process(target=filesToRemove, args=(15))
    #p.start()
    background_remove(filesToRemove)
    #threading.Timer(filesToRemove, removeFiles).start()
    #processThread = threading.Thread(target=removeFiles, args=filesToRemove)  # <- 1 element list
    #processThread.start()
    #task = Process(target=removeFiles(filesToRemove))
    #task.start()  
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
  app.run(debug=True)