# QoL util functions

def partition(lst,sizes):
    assert len(lst) == sum(sizes)
    s = 0
    for sz in sizes:
        yield lst[s:s+sz]
        s += sz