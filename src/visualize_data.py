import utils
import os
from os import path

def load_csv(path):
    pass

def store_graph(graph, name):
    path = os.path.join(utils.graphs_dir(), f"{name}.pdf") #idk jaky extension chceme
    #store
    pass

def visualizeA1(name, path):
    data = load_csv(path)
    #pyplot logic
    #savepyplot
    pass


#main body
utils.delete_dir_content(utils.graphs_dir())

####EXAMPLE - TODO delete
save_path = path.join(utils.graphs_dir(), "shitA1.pdf")
#################

visualizeA1("", path.join(utils.extracted_data_dir(), "shitA1.csv"))
#visualizeA2("", path.join(extracted_data_dir, "shitA2.csv"))
#visualizeB1("", path.join(extracted_data_dir, "shitB1.csv"))