from clib.utils.util import get_cache_func
cache = get_cache_func(__file__)

def f():
    print("FUNCTION CALLED")
    import time
    time.sleep(5)
    return "SUCCESS"

s = cache("after5seconds",f)

print(s)