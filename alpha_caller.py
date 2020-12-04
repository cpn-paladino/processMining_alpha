import sys
# add project folder
sys.path.append('alpha_project')
# import main dependency
from alpha_project.mainTest import execute_script

# main function to call alpha miner process
def call(file):    
    execute_script(file)