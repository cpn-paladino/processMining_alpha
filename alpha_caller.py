import sys
# add project folder
sys.path.append('alpha_project')
# import main dependency
from alpha_project.mainTest import execute_script
# pass file path
log_ruido = r'logs_input/ruido.xes'
def call(file):
    #execute_script(file)
    execute_script(log_ruido)

#call(log_ruido)   

