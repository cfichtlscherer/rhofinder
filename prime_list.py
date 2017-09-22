import math as math

def prime_list(n):
	list=[]
	p=2
	while (len(list) <=n-1):
		if (math.factorial(p-1) + 1) % p == 0:
			list.append(p) 
		p += 1	

	return(list)
