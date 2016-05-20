import requests
import re
from robobrowser import RoboBrowser
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from time import sleep
import networkx as nx
from networkx.readwrite import json_graph
import http_server
import json
import matplotlib.pyplot as plt
import pickle




G=nx.Graph()



browser = RoboBrowser(history=True,parser="html.parser")
driver = webdriver.Chrome()
visited=[]
maxnodes=100


def login():

	login_url="https://www.alexa.com/secure/login"
	browser.open(login_url)
	form = browser.get_form(attrs={'id':'ajax-login-form'})
	form['email'].value = 'divyas12@email.iimcal.ac.in'
	form['password'].value = 'divya@alexa'
	browser.submit_form(form)

	driver.get(login_url)
	username = driver.find_element_by_name('email')
	username.send_keys('divyas12@email.iimcal.ac.in')

	password = driver.find_element_by_name('password')
	password.send_keys('divya@alexa')

	form = driver.find_element_by_id('ajax-login-form')
	form.submit()

def siteinfo(siteurl):

	print "Scraping " + siteurl

	sitelink='http://www.alexa.com/siteinfo/'+siteurl
	browser.open(sitelink)
	hc=str(browser.parsed)
	# hc=driver.page_source
	soup = BeautifulSoup(hc,"html.parser")

	#upstream links
	upsec = soup.find("section", {"id": "upstream-content"})
	uplist=upsec.find_all('tr')
	uplinks=[]
	for tr in uplist:
		data = [td.findChildren(text=True) for td in tr.find_all('td')]
		if len(data):
			tup= (str(data[0][2]), str(data[1][0])[:-1])
			uplinks.append(tup)


	#incomes
	print "Income percentages wrt average"

	incomediv=soup.find("div", {"class": "row-fluid col-pad pybar demo-income"})
	ig=incomediv.find_all('span',{"class":'pybar-bars'})

	incperlist=[]
	for bar in ig:
		barlist=bar.find_all('span',{"class":''})
		if barlist:
			c = 0
			for b in barlist:
				c=c+ int(filter(str.isdigit, str(b['style'])))
			print c
			incperlist.append(c)

	print "Age percentages wrt average"

	agediv=soup.find("div", {"class": "row-fluid col-pad pybar demo-age"})
	ag=agediv.find_all('span',{"class":'pybar-bars'})

	ageperlist=[]
	for bar in ag:
		barlist=bar.find_all('span',{"class":''})
		if barlist:
			c = 0
			for b in barlist:
				c=c+ int(filter(str.isdigit, str(b['style'])))
			print c
			ageperlist.append(c)

	print incperlist, ageperlist

	print "Reach numbers"

	sitelink='http://www.alexa.com/comparison/'+siteurl
	driver.get(sitelink)

	try:
		print "about to look for element"
		element_xpath = '//td[@data-type="reach"]'
		element = WebDriverWait(driver, 10).until(
				lambda driver : driver.find_element_by_xpath(element_xpath)
		)
		print "still looking?"
	finally: 
		print 'yowp'

	hc=driver.page_source
	soup = BeautifulSoup(hc,"html.parser")

	reachtd=soup.find_all("td", {"class": "align-right"})
	rval=reachtd[2].text[:-1]
	pval=reachtd[4].text

	# if u[0] not in G:
	G.add_node(siteurl, ilist=incperlist, alist=ageperlist, reach=float(rval), pageviews=float(pval))
	visited.append(siteurl)
	# else:
	# 	nx.set_node_attributes(G,siteurl,{'ilist'=incperlist, 'alist'=ageperlist, 'reach':float(rval), 'pageviews':float(pval)})

	if(nx.number_of_nodes(G)>=maxnodes):
		return

	for u in uplinks:
		# print u
		if G.has_edge(siteurl, u[0]):
			G[siteurl][u[0]]['weight'] = (G[siteurl][u[0]]['weight'] + (float(u[1])/100))/2
		else:
			G.add_edge(siteurl,u[0],weight=(float(u[1])/100))

	for u in uplinks:
		if u[0] not in visited:
			siteinfo(u[0])




def main():
	login()
	# firstsite=raw_input("Enter beginning site url: ")
	firstsite="thehindu.com"
	siteinfo(firstsite)
	driver.close()

	for n in G:
		G.node[n]['name'] = n

	edgewidth = [ d['weight'] for (u,v,d) in G.edges(data=True)]
	# nsize=[]
	# for u in G.nodes(data=True):
	# 	if not 'reach' in G[u]:
	# 		nsize.append(0.1*100)
	# 	else:
	# 		nsize.append(G.node[u]['reach']*100) 


	

	# pos = nx.spring_layout(G)
	# # nx.draw_networkx_nodes(G, pos, node_size=nsize, with_labels=True)
	# nx.draw_networkx_nodes(G, pos)
	# nx.draw_networkx_edges(G, pos, edge_color=edgewidth)

	# plt.show()

	pickle.dump(G, open('saved/graph.txt', 'w'))


	d = json_graph.node_link_data(G) 
	json.dump(d, open('force/force.json','w'))

	http_server.load_url('force/force.html')




if __name__ == "__main__": main()


