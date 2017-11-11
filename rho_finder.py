from gurobipy import *
import itertools
import numpy as np
import time
from lcm import lcm
from prime_factorization import prime_factorization
from prime_list import prime_list
from list_product import list_product

def rho_finder(N, rho, mono, subadd, submod, account, alphaaug, alpha):
	
	M = 1

	numb = range(N)

	numb[0] = prime_list(N)

	for i in range(1, N):
    		numb[i] = list_product(numb[0], i+1)

	points = []
	for i in range(N):
	    points += numb[i]

	pointswithone = [1] + points	

	strategies = np.asarray(list(itertools.permutations(numb[0])))

	for i in range(len(strategies)):
	    for j in range(N-1):
	        strategies[i][j+1] = int(strategies[i][j])*int(strategies[i][j+1])

###
### Gurobi Part
###
	m = Model('incremental')

	w = m.addVars(pointswithone, lb=0, ub=1)

	opt = m.addVars(range(N), lb=0, ub=1)

	b = range(N)
	l = range(N)
	for i in range(N):
	    b[i] = m.addVars(numb[i], lb=0, ub=1, vtype=GRB.BINARY)
	    l[i] = m.addVars(range(len(strategies)), lb=0, ub=1, vtype=GRB.BINARY)

	t = range(N-1)
	for i in range(N-1):
	    t[i] = m.addVars(numb[i], numb[i+1], lb=0, ub=1, vtype=GRB.BINARY)

	g = m.addVars(numb[0], points, points, lb=0, ub=1, vtype=GRB.BINARY)

###
### Monotonicity
###
	if mono == 1:	
		m.addConstrs(w[i] <= w[j] for i in points for j in points if (int(j) % int(i) == 0))
###
### Sub-Additivity
###
	if subadd == 1:		
		m.addConstrs(w[lcm(i, j)] <= w[i] + w[j] for i in points for j in points)
###
### Sub-Modularity
###
	if submod == 1:
		m.addConstrs(w[a*i] - w[a] >= w[b*i] - w[b] 
			for a in pointswithone
			for b in pointswithone
			for i in numb[0]
			if (b % a == 0) 
			if (b % i != 0)
		             )
###
### alpha-augmentable
###

	if alphaaug == 1: 
		m.addConstrs(g.sum('*', a, b) == 1 for a in points for b in points if (a%b != 0))
		m.addConstrs(g[i, a, b] == 0 for a in points for b in points for i in numb[0] if i in prime_factorization(a))
		m.addConstrs(g[i, a, b] == 0 for a in points for b in points for i in numb[0] if i not in prime_factorization(b))
		m.addConstrs(w[a*i] - w[a] + (1 - g[i, a, b])*M >= (w[lcm(a, b)] - alpha*w[a])/len(prime_factorization(b))
	                	 for a in points	                		 
				 for b in points
                		 for i in numb[0]
                		 if (a % i != 0)
                		 if (b % i == 0)
                	    )

###
### Accountability
###
	if account == 1:
		for x in range(N-1):
			m.addConstrs(t[x].sum('*', j) == 1 for j in numb[x+1])
		    	m.addConstrs(t[x][i, j] == 0 for i in numb[x] for j in numb[x+1] if (j % i) != 0)
		    	m.addConstrs(w[i] >= ((x+1)/(x+2.)) * w[j] - ((1 - t[x][i, j])*M) for j in numb[x+1] 
			for i in numb[x] if (j % i == 0))
###
### rho-strategies
###
	for i in range(N-1):
	    m.addConstr(b[i].sum('*') == 1)

	for i in range(len(strategies)):
	    m.addConstr(quicksum(l[j][i] for j in range(N)) == 1)

	for x in range(N):
	    m.addConstrs(opt[x] >= w[j] for j in numb[x])
	    m.addConstrs(opt[x] <= w[j] + ((1 - b[x][j]) * M) for j in numb[x])
	    m.addConstrs(opt[x] >= rho * w[strategies[i][x]] - (1 - l[x][i]) * M for i in range(len(strategies)))
###
### speed the code up
###
	m.addConstr(w[numb[N-1][0]] == 1)

	for i in range(N-1):
	    m.addConstr(opt[i] <= opt[i+1])
	    m.addConstr(w[numb[0][i]] <= w[numb[0][i+1]])

	m.addConstrs(opt[i] >= ((i+1)/(i+2))*opt[i + 1] for i in range(0, N-1))
	m.addConstrs(2*opt[i] >= opt[(2*i)+1] for i in range(N) if ((2*i)+1) <= (N-1))
###
###
###
	m.optimize()

	print('-------------------------')
	for i in points:
    		print(i)
    		print(w[i])

	f=open(time.strftime('%d-%m-%Y--%H-%M-%S.txt'), 'a+')
	f.write('rho_finder_output \n')
	f.write(time.strftime('%d.%m.%Y %H:%M:%S.txt \n \n'))
	f.write('N='+str(N)+'\n')
	f.write('rho='+str(rho)+'\n')
	f.write('mono='+str(mono)+'\n')
	f.write('subadd='+str(subadd)+'\n')
	f.write('submod='+str(submod)+'\n')
	f.write('account='+str(account)+'\n')
	f.write('alphaaug='+str(alphaaug)+'\n')
	f.write('alpha='+str(alpha)+'\n \n')
	for i in points:
		f.write('w-'+str(i)+'='+str(w[i])+'\n')
	f.close






