from prime_factorization import prime_factorization

def list_product(liste, z):
	p=2
	neu=[]

	prod = reduce(lambda x, y: x*y, liste)


	while(p<=prod):
		if len(prime_factorization(p))==z and len(set(prime_factorization(p)))==z:
			if len(set(liste + (prime_factorization(p))))==len(liste):
				neu.append(p) 
		p += 1	
	return(neu)	

