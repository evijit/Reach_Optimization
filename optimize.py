import networkx as nx
from networkx.readwrite import json_graph
import pickle
from random import choice,uniform
import http_server
import json
import math


def prune(G):
	tbd=[]
	for n in G.nodes():
		if sum(G.node[n]['alist'])==0 or sum(G.node[n]['ilist'])==0:
			tbd.append(n)
	for t in tbd:
		# print t
		G.remove_node(t)

def remove_isolated(G):
	iso=[]
	for n in G.nodes():
		if G.degree(n)==0:
			iso.append(n)
	for i in iso:
		# print i
		G.remove_node(i)


G = pickle.load(open('saved/graph300.txt'))

for u,v,attr in G.edges(data=True):
	G.edge[u][v]['neglog']= -1*math.log(G.edge[u][v]['weight']) 

prune(G)
remove_isolated(G)

F=nx.floyd_warshall(G, weight='neglog')




def D(i,j):
	return math.pow(10,(-1*F.get(i).get(j)))



def U(n):
	world=3000000000
	return G.node[n]['reach']*(world/100) 


def fitness(S):
	#S is a chromosome
	L=len(S)
	outsum=0
	for i in range(1,L):
		insum=0
		for j in range(i+1,L):
			insum+= D(S[i],S[j])* min(U(S[i]),U(S[j]))
		outsum+=U(S[i])-insum
	return outsum



# def get_weight_product(path):
#     prod = 1
#     weight='weight'
#     if len(path) > 1:
#         for i in range(len(path) - 1):
#             u = path[i]
#             v = path[i + 1]
            
#             prod *= G.edge[u][v].get(weight, 1)
    
#     return prod  


# def maxpath(source,dest):
# 	max_path = max((path for path in nx.all_simple_paths(G, source, dest)), key=lambda path: get_weight_product(path))
# 	return max_path

def weighted_choice_node(choices):
   total = sum(w for c, w in choices)
   r = uniform(0, total)
   upto = 0
   for c, w in choices:
	  if upto + w >= r:
		 return c
	  upto += w
   assert False, "Error"


def population_generate_random(P,size):
	#P is population of parents
	#size is size of each chromosome
	population=[]
	i=0
	while (i<P):
		chromosome=[]
		while (True):
			gene = choice(G.nodes())#random node
			if gene not in chromosome:
				chromosome.append(gene)
			if(len(chromosome)==size):
				break
		chromosome=sorted(chromosome, key= lambda node: G.node[node]['reach']) 
		ch=tuple(chromosome)
		if ch not in population:
			population.append(ch)
			i=i+1

	for p in population:
		print p
	return population

def population_generate_weighted(P,size):
	sortednodes=sorted(G.nodes(), key= lambda node: G.node[node]['reach']) 
	choices=[]
	for n in sortednodes:
		choices.append((n,G.node[n]['reach']))

	population=[]
	i=0
	while (i<P):
		chromosome=[]
		while (True):
			gene = weighted_choice_node(choices)#random node
			# print G.node[gene]['reach']
			if gene not in chromosome:
				chromosome.append(gene)
			if(len(chromosome)==size):
				break
		chromosome=sorted(chromosome, key= lambda node: G.node[node]['reach']) 
		ch=tuple(chromosome)
		if ch not in population:
			population.append(ch)
			i=i+1

	for p in population:
		print p
	return population


def main():
	
	# d = json_graph.node_link_data(G) 
	# json.dump(d, open('force/force.json','w'))
	# http_server.load_url('force/force.html')

	print '\n\nRandom\n\n'
	population_generate_random(10,5)
	print '\n\nWeighted\n\n'
	pop = population_generate_weighted(10,5)

	print F.get(pop[0][0]).get(pop[1][0])

	for p in pop:
		print fitness(p)

	


if __name__ == "__main__": main()

		
		
	
	
	
