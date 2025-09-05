from pwn import process, remote

class Challenge:
    def __init__(self,prc_arg,rem_arg,**kwargs):
        self.prc_arg = prc_arg
        self.rem_arg = rem_arg
        self.kwargs = kwargs
        self.current = None
        # define methods
        methods = ["close",
            "recv","recvn","recvpred","recvregex","recvrepeat","recvuntil","recvall",
            "recvline","recvline_contains","recvline_endswith","recvline_pred","recv_line_regex","recvline_startswith",
            "send","sendafter","sendline","sendlineafter","sendlinethen","sendthen",
            "interactive"
        ]
        for method in methods:
            def build_f(m):
                def f(*args,**kwargs):
                    return getattr(self.current,m)(*args,**kwargs)
                return f
            setattr(self,method,build_f(method))

    def local(self):
        if self.current:
            self.current.close()
        self.current = process(self.prc_arg,**(self.kwargs))

    def remote(self):
        if self.current:
            self.current.close()
        self.current = remote(*self.rem_arg,**(self.kwargs))