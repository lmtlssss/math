"""Independent explicit-two-carry forward dynamic program for the local equation.
Unlike the native solver, this checker carries output carries explicitly,
uses forward weighted states, and does not use the 10-bit canonical key.
This implementation retains both output carry states explicitly.
"""
from __future__ import annotations
import time
from typing import Any

def solve(w:int,r1:int,r2:int,shift:int,D:int,S:int,seconds:float=30)->dict[str,Any]:
    if not 0<shift<r1<r2<w: raise ValueError('invalid shifts')
    h=r2-shift; hm=(1<<h)-1; m=(1<<w)-1
    D&=m;S&=m;now=time.perf_counter();count=0;witness=None;sm=0;xx=0;visited=0;peak=0
    def lbit(i:int,cur:int,hist:int)->int:
        x=cur^((hist>>(r2-r1-1))&1)
        return x^((hist>>(h-1))&1) if i+shift<w else x
    def append(d:dict,key:tuple,ct:int,rep:int,s:int,x:int)->None:
        if key in d:
            c,p,v,z=d[key];d[key]=(c+ct,p,(v+s)&((1<<64)-1),z^x)
        else:d[key]=(ct,rep,s&((1<<64)-1),x)
    for tail in range(1<<h):
        if time.perf_counter()-now>seconds:return {'complete':False,'seconds':time.perf_counter()-now,'visited':visited}
        for guessed in (0,1):
            t=guessed;tb=0
            for z in range(h):
                v=((tail>>z)&1)+((D>>(w-h+z))&1)+t;tb|=(v&1)<<z;t=v>>1
            ha=sum(((tail>>z)&1)<<(h-1-z) for z in range(h))
            hb=sum(((tb>>z)&1)<<(h-1-z) for z in range(h))
            for oc0 in (0,1):
                states={(ha,hb,0,oc0):(1,0,0,0)}
                for j in range(w):
                    i=(j-r2)%w; new={};visited+=len(states);peak=max(peak,len(states))
                    for (ah,bh,tin,oc),(ct,rep,s0,x0) in states.items():
                        if j==w-h and tin!=guessed:continue
                        values=((tail>>(j-(w-h)))&1,) if j>=w-h else (0,1)
                        for av in values:
                            ab=av+((D>>j)&1)+tin;bv=ab&1;tout=ab>>1
                            if j>=w-h and bv!=((tb>>(j-(w-h)))&1):continue
                            x=lbit(i,av,ah);y=lbit(i,bv,bh);v=x+y+oc
                            if (v&1)!=((S>>i)&1):continue
                            on=0 if i==w-1 else v>>1
                            an=((ah<<1)|av)&hm;bn=((bh<<1)|bv)&hm;bit=av<<j
                            append(new,(an,bn,tout,on),ct,rep|bit,s0+ct*bit,x0^(bit if ct&1 else 0))
                    states=new
                    if not states:break
                else:
                    for (ah,bh,t,oc),(ct,rep,s0,x0) in states.items():
                        if oc==oc0:
                            count+=ct;sm=(sm+s0)&((1<<64)-1);xx^=x0
                            if witness is None:witness=rep
    return {'complete':True,'count':str(count),'witness':witness,'sum_mod64':sm,'xor':xx&((1<<64)-1),'visited':visited,'peak_per_seed_states':peak,'seconds':time.perf_counter()-now}

if __name__=='__main__':
    import sys,json
    w,r1,r2,sh,D,S=map(int,sys.argv[1:7]);print(json.dumps(solve(w,r1,r2,sh,D,S)))
