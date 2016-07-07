from flask import Flask, render_template,url_for,request,session,redirect
from flask.ext.session import Session
from optimize import Optimize
import pickle
import networkx as nx
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt,mpld3



# timestr = time.strftime("%Y%m%d-%H%M%S")

app = Flask(__name__)
sess=Session()

@app.route("/")
def main():
	return render_template('index.html')

@app.route("/index")
def index():
	return render_template('index.html')

@app.route('/index_post', methods=['POST'])
def index_post():
	session['csize'] = request.form['csize']
	session['psize'] = request.form['psize']
	session['inc'] = request.form['inc']
	session['age'] = request.form['age']
	session['mut'] = request.form['mut']
	session['budget'] = request.form['budget']
	session['probselect'] = request.form['probselect']
	session['iteration'] = request.form['iteration']
	return redirect(url_for('result'))

@app.route("/result", methods=['GET'])
def result():
	csize = session.get('csize', None)
	psize = session.get('psize', None)
	inc = session.get('inc', None)
	age = session.get('age', None)
	mut = session.get('mut', None)
	budget = session.get('budget', None)
	probselect = session.get('probselect', None)
	iteration = session.get('iteration', None)

	opt=Optimize(int(psize), int(csize),int(inc),int(age),int(mut),int(probselect),int(iteration),int(budget));
	data=opt.calculate();

	impressions=[d[1] for d in data[1:]]
	# overlaps=[d[2] for d in data[1:]]
	ans=data[int(iteration)-1][0]
	imp=data[int(iteration)-1][1]
	ov=data[int(iteration)-1][2]
	
	ans=list(ans)

	G = pickle.load(open('saved/graph300.txt'))
	normalnode=[]
	for n in G.nodes():
		if n not in ans:
			normalnode.append(n)

	f=plt.figure()
	plt.autoscale()
	f.tight_layout()
	plt.gcf().subplots_adjust(left=0.2)
	pos=nx.random_layout(G)

	nx.draw_networkx_nodes(G,pos,nodelist=normalnode, node_color='r', node_size=50, alpha=0.8)
	nx.draw_networkx_nodes(G,pos, nodelist=ans, node_color='b', node_size=100, alpha=1.0)
	nx.draw_networkx_edges(G,pos,width=1.0,alpha=0.5)

	graph=mpld3.fig_to_html(f)

	fitnesscurve=[]
	for i in range(0,int(iteration)):
		fitnesscurve.append((i,impressions[i]))

	f2=plt.figure(2)
	plt.autoscale()
	f2.tight_layout()
	plt.gcf().subplots_adjust(left=0.2)
	plt.clf()
	plt.scatter(*zip(*fitnesscurve))
	chart=mpld3.fig_to_html(f2)



	return render_template('result.html',chart=chart,graph=graph,ans=ans,imp=imp,ov=ov)

@app.route("/about", methods=['GET'])
def about():
	return render_template('about.html')



# if __name__ == "__main__":

app.secret_key = 'avijit_iimc'
app.config['SESSION_TYPE'] = 'filesystem'

sess.init_app(app)
app.debug = True
	# app.run()