# Reference:
# - Factoring with Cyclotomic Polynomials (https://www.ams.org/journals/mcom/1989-52-185/S0025-5718-1989-0947467-1/S0025-5718-1989-0947467-1.pdf)

def factor_cyclotomic_polynomial_prime_power(n,p,k,N,E,trials=-1,proof=True,debug=False,threshold=2**20):
    """
    Factoring with k-th cyclotomic polynomial where k is a prime power.
    Generalization of <cry> in WACon 2023 Qualification

    [Explanation]
    For every positive integer n, it holds that:
    prod(phi_d(x)| (d|n)) = x^n-1

    Putting n=p^k for some prime p and integer k bigger than 1,
    phi_n(x) = (x^n-1)/(x^(n/p)-1)

    Since (q^(n/p)-1) divides (q^n-1) for every prime q,
    We could expect the existence of a multiplicative subgroup of order (q^(n/p)-1)
    which is imbedded in the finite field of order (q^n-1)

    So we pick a random irreducible polynomial f(x) of degree (n/p)
    Then we choose a polynomial ring R:=F_q[x]/f(x^p) as a domain for the algorithm
    What we, the attacker, hope here is that f(x^p) is irreducible over F_q
    to get an isomorphic ring to F_{q^n}

    Here, let g be a random polynomial of degree strictly less than (n/p) over F_q
    g(x^p) is an element of R whose order is (q^(n/p)-1),
    and we can explicitly find (q^(n/p)-1) such non-zero polynomials g
    Therefore, every element is in the subgroup of order (q^(n/p)-1) is of form g(x^p) for some g

    We suppose here that an integer E, which is a multiple of phi_n(q), is known.
    Let t be an arbitrary non-zero element of R.
    Then t^E is of form g(x^p) for some polynomial g.

    The actual computation works on R':=Z/<f(x^p),N>.
    In detail,
    1. Let t be a random element of R'.
    2. Compute t^E and let it be s.
    3. We hope the coefficient of x^i be a multiple of q, where i is relatively prime to p.
    """
    from sage.all import Zmod,Integer,gcd
    if proof:
        assert k>1
        assert p**k == n
    Z = Zmod(N)["x"]
    x = Z.gen()
    
    trial_count = 0
    while trial_count != trials:
        f = x**(n//p)+Z.random_element(n//p-1) # random monic polynomial
        if debug:
            print(f"[i] New try with {f = }")
        R = Z.quotient(f.subs(x=x**p))
        t = R.random_element()
        s = t**E
        g = gcd(Integer(v) for i,v in enumerate(list(s)) if gcd(i,p)==1)
        g = gcd(g,N)
        if threshold<g<N:
            if debug:
                print(f"[+] Succeeded with {g=}")
            return g
        if debug:
            if g < threshold:
                print(f"[-] Failed by g<threshold")
            if g == N:
                print(f"[-] Failed by g=N")
        trial_count += 1
    return None