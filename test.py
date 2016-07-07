import networkx as nx
from networkx.readwrite import json_graph
import pickle
import json
import http_server

G = pickle.load(open('saved/graph300.txt'))

# for n in G.nodes():
# 	print n
d = json_graph.node_link_data(G) 
json.dump(d, open('force/force.json','w'))

http_server.load_url('force/force.html')