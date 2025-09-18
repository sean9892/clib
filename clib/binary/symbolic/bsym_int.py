from sage.all import GF, Integer
from typing import Iterable

CONSTANT_INTEGER_TYPES = (int,Integer)

F2 = GF(2)

class BSymInteger:
    """
    Binary Symbolic Integer

    [Warnings]
    All bits which should be assigned to an index greater or equal to `nbits` would be truncated.
        - e.g. multiplication without specifying a modulus, lshift, etc.
    `nbits` of the results are always assumed to be the largest one of operands.
    """
    @staticmethod
    def zero(nbits,parent):
        zero = parent.zero()
        return BSymInteger(nbits,[zero for _ in range(nbits)],parent=parent)

    def __init__(self,nbits,bits,parent=None):
        assert isinstance(bits,Iterable)
        assert nbits > 0
        assert len(bits) == nbits

        if parent == None:
            parent = bits[0].parent()
        self.parent = parent

        self._generators = None # compute only when it is necessary

        self.bits = list(bits)
        
    def gens(self):
        if self._generators == None:
            self._generators = self.parent.gens()
        return self._generators
    
    def resized(self,nbits):
        if self.nbits == nbits:
            return BSymInteger(nbits,self.bits[:],parent=self.parent)
        elif self.nbits < nbits:# shrinking
            return BSymInteger(nbits,self.bits[:nbits],parent=self.parent)
        else:# expanding
            zero = self.parent.zero()
            return BSymInteger(nbits,self.bits[:]+[zero for _ in range(nbits-self.nbits)],parent=self.parent)

    # ==== [Unary Operators] ====

    def __invert__(self):
        one = self.parent.one()
        return BSymInteger(self.nbits,[one+c for c in self.bits],parent=self.parent)

    # ==== [Equality Operators] ====

    def __eq__(self,other):
        if isinstance(other,BSymInteger):
            if self.parent == other.parent:
                nbits = max(self.nbits,other.nbits)
                _self = self.resized(nbits)
                _other = other.resized(nbits)
                return all(v==w for v,w in zip(_self.bits,_other.bits))
            else:
                return False
        else:
            return False
    
    def __ne__(self,other):
        return not self.__eq__(other)

    # ==== [Binary Operators] ====

    def __xor__(self,other):
        if isinstance(other,BSymInteger):
            assert self.parent == other.parent
            parent = self.parent
            zero = parent.zero()
            nbits = max(self.nbits,other.nbits)
            res = BSymInteger(nbits,[
                (self.bits[i] if i<self.nbits else zero) ^ (self.bits[i] if i<self.nbits else zero)
                for i in range(nbits)
            ],parent=parent)
            return res
        elif isinstance(other,CONSTANT_INTEGER_TYPES):
            parent = self.parent
            zero = parent.zero()
            nbits = max(self.nbits,other.bit_length())
            res = BSymInteger(nbits,[
                (self.bits[i] if i<self.nbits else zero) ^ parent((other>>i)&1)
                for i in range(nbits)
            ],parent=parent)
        else:
            raise NotImplementedError
    def __rxor__(self,other):
        return self.__xor__(other)
    def __ixor__(self,other):
        res = self.__xor__(other)
        self.nbits = res.nbits
        self.bits = res.bits
    
    def __lshift__(self,other):
        if isinstance(other,CONSTANT_INTEGER_TYPES):
            zero = self.parent.zero()
            return BSymInteger(self.nbits,[zero for _ in range(other)]+self.bits[:-other],parent=self.parent)
        else:
            raise NotImplementedError
    def __ilshift__(self,other):
        res = self.__ilshift__(other)
        self.nbits = res.nbits
        self.bits = res.bits
    
    def __rshift__(self,other):
        if isinstance(other,CONSTANT_INTEGER_TYPES):
            zero = self.parent.zero()
            return BSymInteger(self.nbits,self.bits[other:]+[zero for _ in range(other)],parent=self.parent)
        else:
            raise NotImplementedError
    def __irshift__(self,other):
        res = self.__irshift__(other)
        self.nbits = res.nbits
        self.bits = res.bits

    def __and__(self,other):
        if isinstance(other,BSymInteger):
            assert self.parent == other.parent
            parent = self.parent
            nbits = max(self.nbits,other.nbits)
            zero = parent.zero()
            return BSymInteger(nbits,[
                (self.bits[i] if i<self.nbits else zero) ^ (other.bits[i] if i<other.nbits else zero)
                for i in range(nbits)
            ],parent=parent)
        elif isinstance(other,CONSTANT_INTEGER_TYPES):
            assert self.parent == other.parent
            parent = self.parent
            nbits = max(self.nbits,other.bit_length())
            res = BSymInteger.zero(nbits,parent)
            for i in range(min(self.nbits,other.bit_length())):
                if ((other>>i)&1) == 1:
                    res.bits[i] = self.bits[i]
            return res
        else:
            raise NotImplementedError
    def __rand__(self,other):
        return self.__and__(other)
    def __iand__(self,other):
        res = self.__and__(other)
        self.nbits = res.nbits
        self.bits = res.bits

    def __mul__(self,other):
        if isinstance(other,self.parent.Element):
            return BSymInteger(self.nbits,[other*c for c in self.bits],parent=self.parent)
        elif isinstance(other,BSymInteger):
            assert self.parent == other.parent
            parent = self.parent
            nbits = max(self.nbits,other.nbits)
            _self = self.resized(nbits)
            _other = other.resized(nbits)
            res = BSymInteger.zero(nbits,parent)
            for i in range(nbits):
                res ^= ((_self<<i)*_other.bits[i])
            return res
        elif isinstance(other,CONSTANT_INTEGER_TYPES):
            parent = self.parent
            nbits = max(self.nbits,other.bit_length())
            _self = self.resized(nbits)
            res = BSymInteger.zero(nbits,parent)
            for i in range(nbits):
                if ((other>>i)&1) == 1:
                    res ^= (_self<<i)
            return res
        else:
            raise NotImplementedError
    def __rmul__(self,other):
        return self.__mul__(other)
    def __imul__(self,other):
        res = self.__mul__(other)
        self.nbits = res.nbits
        self.bits = res.bits


