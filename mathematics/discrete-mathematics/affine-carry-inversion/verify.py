#!/usr/bin/env python3
"""Whole-fiber comparison against independent forward enumeration.
No numerical approximations. Run with Python 3.10 or later.
"""
from __future__ import annotations
import argparse,json,random,time
from pathlib import Path
from atlas import inverse_fiber,inverse_rows,linear,signature_count,signatures

ROOT=Path(__file__).resolve().parent


def forward(x,D,rows):
    # Separate bit loops: does not use the solver's parity helper.
    w=len(rows);mask=(1<<w)-1
    values=[]
    for arg in (x,(x+D)&mask):
        y=0
        for i,row in enumerate(rows):
            parity=0
            for j in range(w):
                parity^=((row>>j)&1)*((arg>>j)&1)
            y|=parity<<i
        values.append(y)
    return sum(values)&mask


def expand(c):
    out=[c['base']]
    for b in c['basis']:out += [x^b for x in out]
    return out


def binary_rank(vectors):
    basis={}
    for x in vectors:
        while x:
            p=x.bit_length()-1
            if p in basis:x^=basis[p]
            else:basis[p]=x;break
    return len(basis)


def validate_cell(c,D,S,rows):
    w=len(rows);low=(1<<(w-1))-1;mask=(1<<w)-1
    k=c['signature'];delta=c['delta']
    assert linear(delta,rows)==k
    di=(delta-D)&mask;do=(S-k)&mask
    assert (di|do)&1==0
    u,v=di>>1,do>>1;m=delta&low;n=(~k)&low
    assert u&~m==0 and v&~n==0
    assert c['base']&m==u and linear(c['base'],rows)&n==v
    assert all(b&m==0 and linear(b,rows)&n==0 for b in c['basis'])
    eqrows=[1<<i for i in range(w-1) if (m>>i)&1]+[rows[i] for i in range(w-1) if (n>>i)&1]
    assert binary_rank(c['basis'])==len(c['basis'])==w-binary_rank(eqrows)
    assert c['count']==1<<len(c['basis'])


def mixed_rows(w,rng):
    a=[1<<i for i in range(w)]
    if w>1:
        for _ in range(7*w):
            i,j=rng.sample(range(w),2)
            if rng.randrange(3):a[i]^=a[j]
            else:a[i],a[j]=a[j],a[i]
    return a


def run(max_width=7):
    t=time.perf_counter();rng=random.Random(0xAFF1CE27)
    cases=0;queries=0;points=0;matrix_records=[]
    for w in range(1,max_width+1):
        M=1<<w
        for mi in range(3):
            rows=[1<<i for i in range(w)] if mi==0 else mixed_rows(w,rng)
            inv=inverse_rows(rows)
            assert all(linear(linear(1<<i,rows),inv)==1<<i for i in range(w))
            for D in range(M):
                expected=[set() for _ in range(M)]
                for x in range(M):expected[forward(x,D,rows)].add(x);points+=1
                for S in range(M):
                    cases+=1
                    for side in ('input','output','auto'):
                        result=inverse_fiber(D,S,rows,side);queries+=1
                        got=[]
                        for cell in result['cells']:
                            validate_cell(cell,D,S,rows)
                            got.extend(expand(cell))
                        assert len(got)==len(set(got))==result['count']
                        assert set(got)==expected[S],(w,mi,D,S,side)
                        if side=='auto':assert result['signatures_examined']==min(result['input_signatures'],result['output_signatures'])
            matrix_records.append({'width':w,'rows':rows,'complete_fibers':M*M})
        print('COMPLETE_WIDTH',w,'FIBERS',cases,flush=True)
    # Direct addition-derived signature sets, independent of carry enumeration.
    signature_comparisons=0
    for w in range(1,9):
        M=1<<w
        for tword in range(M):
            direct_input={x^((x+tword)&(M-1)) for x in range(M)}
            direct_output={x^((tword-x)&(M-1)) for x in range(M)}
            for side,want in [('input',direct_input),('output',direct_output)]:
                got=list(signatures(tword,w,side))
                assert set(got)==want and len(got)==len(want)==signature_count(tword,w,side)
                signature_comparisons+=1
    f0,f1=0,1;maxima=[]
    for w in range(1,17):
        f0,f1=f1,f0+f1
        observed=[max(signature_count(x,w,side) for x in range(1<<w)) for side in ('input','output')]
        assert observed==[f1,f1]
        maxima.append({'width':w,'maximum':f1})
    # A dense, invertible 32-bit map specified only by its bit operators.
    def ror(x,r):return ((x>>r)|(x<<(32-r)))&0xffffffff
    columns=[ror(1<<i,17)^ror(1<<i,19)^((1<<i)>>10) for i in range(32)]
    rows=[sum(((columns[j]>>i)&1)<<j for j in range(32)) for i in range(32)]
    inv=inverse_rows(rows);reflection=[]
    for S in (0xffffffff,0x7fffffff):
        delta=linear(S,inv);result=inverse_fiber(delta,S,rows)
        assert len(result['cells'])==1 and result['signatures_examined']==1
        c=result['cells'][0];validate_cell(c,delta,S,rows)
        all_members=expand(c)
        assert all(forward(x,delta,rows)==S for x in all_members)
        reflection.append({'width':32,'rows':rows,'D':delta,'S':S,'count':result['count'],'inverse_rows':list(inv),'base':c['base'],'basis':list(c['basis'])})
    # Wide all-solution certificates: one-cell reflection family, dimension w-1.
    wide=[]
    for w in (16,32,64,128,256,512):
        rows=[1]+[(1<<i)|1 for i in range(1,w)]
        result=inverse_fiber(1,(1<<w)-1,rows)
        assert len(result['cells'])==1 and result['count']==1<<(w-1)
        validate_cell(result['cells'][0],1,(1<<w)-1,rows)
        wide.append({'width':w,'cell_count':1,'dimension':w-1,'solution_count':str(result['count'])})
    figure=json.loads((ROOT/'evidence/figure.json').read_text())
    for c in figure['cells']:validate_cell(c,figure['D'],figure['S'],figure['rows'])
    got=set(x for c in figure['cells'] for x in expand(c))
    want={x for x in range(1<<figure['width']) if forward(x,figure['D'],figure['rows'])==figure['S']}
    assert got==want and len(got)==17
    return {'complete_fibers':cases,'solver_calls':queries,'forward_evaluations':points,
            'matrices':matrix_records,'signature_set_comparisons':signature_comparisons,
            'fibonacci_maxima':maxima,'reflection_examples':reflection,'wide_certificates':wide,
            'figure_members':sorted(got),'all_match':True,'seconds':time.perf_counter()-t}

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--max-width',type=int,default=7);p.add_argument('--output',default='evidence/verification.json');a=p.parse_args()
    report=run(a.max_width);Path(a.output).write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k not in ('matrices','reflection_examples','wide_certificates')},indent=2))
