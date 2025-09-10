# QoL util functions

def partition(lst,sizes):
    assert len(lst) == sum(sizes)
    s = 0
    for sz in sizes:
        yield lst[s:s+sz]
        s += sz

def _cache(__file__,name,func,forced_renew=None):
    from hashlib import sha256
    import pickle
    identifier = sha256(name.encode()).hexdigest()
    path = f"{identifier}.cache"

    H = sha256(open(__file__,"r").read().encode()).hexdigest().encode()

    renew_computation = forced_renew
    f = None
    if renew_computation == None:
        try:
            f = open(path,"rb")
            vhash = f.read(64)
            f.close()
            if H == vhash:
                renew_computation = False
            else:
                renew_computation = True
        except FileNotFoundError:
            renew_computation = True

    if renew_computation:
        f = open(path,"wb")
        f.write(H.encode())
        value = func()
        pickle.dump(value,f)
        f.close()
        return value
    else:
        f = open(path,"rb")
        _ = f.read(64)
        value = pickle.load(f)
        f.close()
        return value

def get_cache_func(fn):
    return (lambda FILENAME: (lambda *args,**kwargs: _cache(FILENAME,*args,**kwargs)))(fn)