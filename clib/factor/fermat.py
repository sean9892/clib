def ceil_sqrt(N):
    from sage.all import ceil,sqrt
    return int(ceil(sqrt(N)))

def fermat_factor(N,trials=None):
    from sage.all import is_prime,is_square,sqrt
    # trivial cases
    if N%2 == 0:
        return 2
    if is_prime(N):
        return N
    
    a = ceil_sqrt(N)
    b2 = a*a-N
    if trials:
        for _ in range(trials):
            if is_square(b2):
                return a-sqrt(b2)
            b2 += 2*a+1
            a += 1
        return None
    else:
        while not is_square(b2):
            b2 += 2*a+1
            a += 1
        return a-sqrt(b2)