from sage.all import *
from sage.all import matrix
proof.all(False)

def symmetric_mod(x, m):
    """
    Computes the symmetric modular reduction.
    :param x: the number to reduce
    :param m: the modulus
    :return: x reduced in the interval [-m/2, m/2]
    """
    return int((x + m + m // 2) % m) - int(m // 2)

def shortest_vectors(B):
    """
    Computes the shortest non-zero vectors in a lattice.
    :param B: the basis of the lattice
    :return: a generator generating the shortest non-zero vectors
    """
    B = B.LLL()

    for row in B.rows():
        if not row.is_zero():
            yield row


# Babai's Nearest Plane Algorithm from "Lecture 3: CVP Algorithm" by Oded Regev.
def _closest_vectors_babai(B, t):
    B = B.LLL()

    for G in B.gram_schmidt():
        b = t
        for j in reversed(range(B.nrows())):
            b -= round((b * G[j]) / (G[j] * G[j])) * B[j]

        yield t - b


def _closest_vectors_embedding(B, t):
    B_ = B.new_matrix(B.nrows() + 1, B.ncols() + 1)
    for row in range(B.nrows()):
        for col in range(B.ncols()):
            B_[row, col] = B[row, col]

    for col in range(B.ncols()):
        B_[B.nrows(), col] = t[col]

    B_[B.nrows(), B.ncols()] = 1
    yield from shortest_vectors(B_)


def closest_vectors(B, t, algorithm="embedding"):
    """
    Computes the closest vectors in a lattice to a target vector.
    :param B: the basis of the lattice
    :param t: the target vector
    :param algorithm: the algorithm to use, can be "babai" or "embedding" (default: "embedding")
    :return: a generator generating the shortest non-zero vectors
    """
    if algorithm == "babai":
        yield from _closest_vectors_babai(B, t)
    elif algorithm == "embedding":
        yield from _closest_vectors_embedding(B, t)

def attack(x, rho):
    """
    Solves the ACD problem using the simultaneous Diophantine approximation approach.
    More information: Galbraith D. S. et al., "Algorithms for the Approximate Common Divisor Problem" (Section 3)
    :param x: the x samples, with xi = p * qi + ri
    :param rho: the bit length of the r values
    :return: the secret integer p and a list containing the r values, or None if p could not be found
    """
    assert len(x) >= 2, "At least two x values are required."

    R = 2 ** (rho + 1)

    B = matrix(ZZ, len(x), len(x))
    B[0, 0] = R
    for i in range(1, len(x)):
        B[0, i] = x[i]
        B[i, i] = -x[0]

    for v in shortest_vectors(B):
        if v[0] != 0 and v[0] % R == 0:
            q0 = v[0] // R
            r0 = symmetric_mod(x[0], q0)
            p = abs((x[0] - r0) // q0)
            r = [symmetric_mod(xi, p) for xi in x]
            if all(-R < ri < R for ri in r):
                return int(p), r