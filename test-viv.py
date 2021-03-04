#!/usr/bin/env python3

import sys

import vivisect
from Symgrate2 import Symgrate2

LEN = 18

def functionprefix(fun):
    """Returns the first eighteen bytes of a function as ASCII."""
    B=vw.readMemory(fun, LEN)
    raw=""
    for i in range(0, LEN, 2):
        h=int(B[i+1])
        l=int(B[i])
        raw+="%02x%02x"%(l,h)
    #print("raw:     %s"%raw)
    return raw


def dumpfile(f):
    """Import a .o file to the database."""
    global vw
    vw = vivisect.VivWorkspace()
    vw.loadWorkspace(f)

    # This is the gross architecture, but individual functions might have
    # different architectures.  arm7/thumb2, for example.
    print("Loaded %s for architecture %s."%(f, vw.getMeta("Architecture")))
    
    # ## Print the recovered name of each function.
    # for f in vw.functions:
    #     pre=functionprefix(f)
    #     name=Symgrate2.queryfn(pre)
    #     if name!=None:
    #         sys.stdout.write("\n%08x %-20s" % (f.start, name))
    #     else:
    #         sys.stdout.write(".")
    #         sys.stdout.flush()
    # sys.stdout.write("\n")

    count=0
    q={}
    symg = Symgrate2()
    for f in vw.getFunctions():
        pre = functionprefix(f)
        count = count+1
        
        q[hex(f)] = pre
        
        if count & 0x3F == 0x00:
            res  =symg.queryfns(q)
            q = {}
            if res != None: 
                resprint(res)

    if len(q):
        res = symg.queryfns(q)
        if res!=None: 
            resprint(res)
            
def resprint(res):
    for key, valdict in res.items():
        print("%r: name: %r  fname: %r" % (key, valdict['Name'], valdict['Filename']))


if len(sys.argv)==1:
    print("Usage: %s foo.viv"%sys.argv[0])
else:
    for f in sys.argv[1:]:
        print("Querying %s"%f)
        dumpfile(f)


