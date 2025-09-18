from clib.binary.symbolic import BSymInteger
from clib.utils.mprcon import mprcon
from sage.all import ZZ,GF,randrange

try:
    from tqdm import trange
    rng = trange
except:
    rng = range

F2 = GF(2)
R,xs = mprcon(F2,[("x",24)])

# LFSR with feedback polynomial x^24+x^23+x^22+x^17+1
# symbolic computation
def snext(state):
    nxt = ((state>>23)^(state>>22)^(state>>21)^(state>>16))&1
    new_state = (state<<1)^nxt
    return new_state

sym_state = BSymInteger(24,list(xs))
for _ in rng(512):
    sym_state = snext(sym_state)

monomials = sym_state.monomials()
assert len(monomials) == 24
sym_coefs = sym_state.coefficients_matrix().change_ring(ZZ)
print(sym_coefs.nrows(),sym_coefs.ncols())

def cnext(state):
    nxt = ((state>>23)^(state>>22)^(state>>21)^(state>>16))&1
    new_state = ((state<<1)^nxt)&0xffffff
    return new_state

T = 16384
for _ in rng(T):
    _state = randrange(0,2**24)
    
    state = _state
    for _ in range(512):
        state = cnext(state)

    expected = 0
    bits = [(_state>>i)&1 for i in range(24)]
    for i in range(24):
        s = sum(sym_coefs[i,monomials.index(xs[j])]*bits[j] for j in range(24))
        expected += (s&1)<<i
    assert state == expected