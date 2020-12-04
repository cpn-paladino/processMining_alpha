import os
from flask import Flask, render_template, request, flash, redirect, send_file
from werkzeug import secure_filename
from alpha_caller import call

BASE_FOLDER = os.getcwd()
OUTPUT_FOLDER = os.path.join(BASE_FOLDER,'static','output')
UPLOAD_FOLDER = os.path.join(BASE_FOLDER,'logs_input')

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'xes','png'}
#app.config['MAX_CONTENT_PATH']

def allowed_file(filename):
    return '.' in filename and \
      filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/get_model', methods = ['GET', 'POST'])
def get_model():
  base_file = 'ruido_alpha_discovery.png'  
  currentFile = os.path.join(BASE_FOLDER, base_file)
  newFile = os.path.join(OUTPUT_FOLDER, base_file)  
  import shutil
  shutil.copy(currentFile, newFile) 
  #outFile = open(newFile,'w')

  #file.save(OUTPUT_FOLDER, currentFile)
  '''
  with open(newFile,'w') as file:
    file_binary = open(currentFile,'r')
    file.write(file_binary)  
    file_binary.close()
  '''    
  #send_file('ruido_alpha_discovery.png', mimetype='image/png')
  return base_file



@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
  print('fui chamado')
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
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return 'file uploaded successfully'
  else:     
      print('nada aconteceu')
      return 'error your request'

@app.route("/")
def home():
  return render_template("index.html")
  
if __name__ == "__main__":
  port = int(os.environ.get("PORT", 5000))
  app.run(host='0.0.0.0', port=port)  
  #app.run(debug=True)