# easy construction for Multivariate Polynomial Ring

from .util import partition

def mprcon(base_ring,variables,partition_gens=False):
    is_ring = (hasattr(base_ring,"is_ring") and base_ring.is_ring())
    assert is_ring, "base ring must be a ring"

    var_string = ",".join(
        f"{x}{i}" for x,n in variables for i in range(n)
    )
    mpr = base_ring[var_string]
    gens = mpr.gens()

    if partition_gens:
        partition_sizes = [n for _,n in variables]
        par_gens = partition(gens,partition_sizes)
        dict_gens = {x:g for (x,_),g in zip(variables,par_gens)}
        return mpr,dict_gens
    else:
        return mpr,gens

if __name__ == "__main__":
    print(partition)