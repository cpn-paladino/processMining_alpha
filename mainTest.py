import xes_parser_log as iterparse
from alpha import algorithm as alpha_miner
from visualization import visualizer as pn_vis

# old path: "G:\\Meu Drive\\SIN-5025\\01-Trabalho\\04-Projeto Final\\01-AlphaAlgo\\pm4py-core\\tests\\input_data\\running-example.xes"
#log_path = "running-example.xes"
#log_elio = "elio_teste.xes"
log_professor = r'logs_input/logProfessor.xes'
log_ruido = r'logs_input/ruido.xes'

# created function to visualize log structure
def saveLog(log):
    with open("z_logProcessed.txt", 'w') as f:
        for i in log:            
            for j in i:
                f.write(str(j))
                f.write("\n")

def cleanXmlLogAttributes(filepath):
    import re
    logPattern = re.compile(r"<log.*>")    
    with open(filepath, 'r') as f:
        res = re.sub(logPattern, "<log>", f.read()) 
    newFilePath = re.sub('.xes','', filepath) +'_cleaned.xes'
    with open(newFilePath,'w') as f:
        f.write(res)    
    return newFilePath    

def execute_script(xes_file):
    # 1 process log    

    xmlCleaned = cleanXmlLogAttributes(xes_file)

    log = iterparse.import_log(xmlCleaned)    
    saveLog(log)
    # 2 get petrinet with init and end
    net, i_m, f_m = alpha_miner.apply(log)
    print(net.name)  
    print(i_m)
    print(f_m)
    # 3 generate diagram

    gviz = pn_vis.apply(net, i_m, f_m,
                        parameters={pn_vis.Variants.WO_DECORATION.value.Parameters.FORMAT: "png",
                                    pn_vis.Variants.WO_DECORATION.value.Parameters.DEBUG: False})
    # pn_vis.view(gviz)
    # 4 save on default path
    pngFinalMap = str(xes_file).replace('logs_input/','').replace('.xes','')+'_alpha_discovery.png'
    print(pngFinalMap)
    pn_vis.save(gviz, pngFinalMap)

if __name__ == "__main__":    
    execute_script(log_ruido)