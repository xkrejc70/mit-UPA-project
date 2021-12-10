import utils
import os

def load_csv(path):
    pass

def store_graph(graph, name):
    path = os.path.join(utils.graphs_dir(), f"{name}.pdf") #idk jaky extension chceme
    #store
    pass

def visualize1(name, path):
    data = load_csv(path)
    #pyplot logic
    pass


#main body
utils.delete_dir_content(utils.graphs_dir())
extracted_data_dir = utils.extracted_data_dir()

def visualize1(name, path)
#def visualize2(name, path)
#def visualize3(name, path)