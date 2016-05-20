import networkx as nx
from networkx.readwrite import json_graph
import pickle

G = pickle.load(open('saved/graph300.txt'))

for n in G.nodes():
	print n
