def prime_factorization(n):
    primfactors = []
    d = 2
    while d*d <= n:
        while (n % d) == 0:
            primfactors.append(d)
            n /= d
        d += 1
    if n > 1:
       primfactors.append(n)
    return primfactors
