import xes_parser_log as iterparse
from alpha import algorithm as alpha_miner
from visualization import visualizer as pn_vis

 # old path: "G:\\Meu Drive\\SIN-5025\\01-Trabalho\\04-Projeto Final\\01-AlphaAlgo\\pm4py-core\\tests\\input_data\\running-example.xes"
log_path = "running-example.xes"

# created function to visualize log structure
def saveLog(log):
    with open("z_logProcessed.txt", 'w') as f:
        for i in log:            
            for j in i:
                f.write(str(j))
                f.write("\n")

def execute_script():
    # 1 process log
    log = iterparse.import_log(log_path)
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
    pn_vis.save(gviz, "z22_alpha_miner_petri_net.png")


if __name__ == "__main__":
    execute_script()