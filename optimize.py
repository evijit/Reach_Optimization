import networkx as nx
from networkx.readwrite import json_graph
import pickle
from random import choice,uniform,randint
import http_server
import json
import math
import matplotlib.pyplot as plt


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

def weighted_choice(choices):
   total = sum(w for c, w in choices)
   r = uniform(0, total)
   upto = 0
   for c, w in choices:
	  if upto + w >= r:
		 return c
	  upto += w
   assert False, "Error"


def population_generate_random(P,size,income):
	#P is population of parents
	#size is size of each chromosome
	population=[]
	i=0
	while (i<P):
		chromosome=[]
		while (True):
			gene = choice(G.nodes())#random node
			if minimuminc(gene,income)==False:
				continue
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

def population_generate_weighted(P,size,income):
	sortednodes=sorted(G.nodes(), key= lambda node: G.node[node]['reach']) 
	choices=[]
	for n in sortednodes:
		choices.append((n,G.node[n]['reach']))

	population=[]
	i=0
	while (i<P):
		chromosome=[]
		while (True):
			gene = weighted_choice(choices)#random node
			if minimuminc(gene,income)==False:
				continue
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

def replace(l, X, Y):
  for i,v in enumerate(l):
     if v == X:
        l.pop(i)
        l.insert(i, Y)

def pickparents(population):
	parents=[]
	choices=[]
	sortedpopulation=sorted(population, key= lambda ch: fitness(ch)) 
	for ch in sortedpopulation:
		choices.append((ch,fitness(ch)))

	i=0
	while(i<2):
		p=weighted_choice(choices)
		if p not in parents:
			parents.append(p)
			i=i+1
	return parents

def makechild(population, parents,income):
	choices=[]
	child=[]
	size=len(parents[0])
	sortedparents=sorted(parents, key= lambda ch: fitness(ch)) 
	for ch in sortedparents:
		choices.append((ch,fitness(ch)))
	i=0
	while i<size:
		p=weighted_choice(choices)
		g=choice(p)
		r=randint(1,100)
		if r==1 or r==2 or r==3 or r==4 or r==5:
			g=choice(G.nodes())
			if minimuminc(g,income)==False:
				continue
			print "Mutation"
		if g not in child:
			child.append(g)
			i=i+1

	child=tuple(child)

	FP0=fitness(parents[0])
	FP1=fitness(parents[1])
	FC=fitness(child)

	# print "\n\n\nCHILDREN\n\n\n"

	print parents[0] , FP0
	print parents[1] , FP1
	print child, FC

	if min(FP0,FP1,FC)==FP0:
		print "replaced: " ,parents[0], FP0
		replace(population,parents[0],child)
	elif min(FP0,FP1,FC)==FP1:
		print "replaced: " ,parents[1], FP1
		replace(population,parents[1],child)
	else:
		print "No replacement"




def minimuminc(site,inc):
	#inc can take values 0,30,60 or 100. 0 means no restriction
	# (0-30)(30-60)(60-100)(100+)
	print G.node[site]
	if inc==0:
		return True
	if inc==30:
		if sum(G.node[site]['ilist'][1:])>=300:
			return True
		else :
			return False
	if inc==60:
		if sum(G.node[site]['ilist'][2:])>=200:
			return True
		else:
			return False
	if inc==100:
		if sum(G.node[site]['ilist'][3])>=100:
			return True
		else:
			return False





def main():
	
	# d = json_graph.node_link_data(G) 
	# json.dump(d, open('force/force.json','w'))
	# http_server.load_url('force/force.html')

	# print '\n\nRandom\n\n'
	# pop=population_generate_random(100,5,60)
	# print '\n\nWeighted\n\n'
	# # pop = population_generate_weighted(100,5)

	print minimuminc('google.com',30)

	# fitnesscurve=[]

	# for i in range(1,2000):
	# 	print "\n\n", i, "\n\n"
	# 	par= pickparents(pop)
	# 	makechild(pop,par)
	# 	sortedpop=sorted(pop, key= lambda ch: fitness(ch), reverse=True) 
	# 	print "fittest: "
	# 	print sortedpop[0], fitness(sortedpop[0])
	# 	fitnesscurve.append((i,fitness(sortedpop[0])))

	# plt.scatter(*zip(*fitnesscurve))
	# plt.show()
	

	


if __name__ == "__main__": main()

		
		
	
	
	
