#!/usr/bin/env python3
"""Complete-function experiments using ordinary arithmetic as a separate oracle."""
import argparse, itertools, json, random, time
from collections import Counter
from pathlib import Path
from state import encode, evaluate, normal_form, representative, multiplicity, compose
R=Path(__file__).resolve().parent

def forward(B,C,S,H,a,b):
    first=C+S+a
    first_carry=first//B
    second=first-first_carry*B+H+b
    second_carry=second//B
    return second-second_carry*B,first_carry,second_carry

def function(B,C,S,H):
    return tuple(forward(B,C,S,H,a,b) for a in (0,1) for b in (0,1))

def experiment():
    started=time.perf_counter();rows=[];total=0;figure=[]
    for B in range(2,21):
        observed={};counts=Counter();hist=Counter()
        for C,S,H in itertools.product(range(B),repeat=3):
            label=encode(B,C,S,H);expected=function(B,C,S,H)
            got=tuple(evaluate(B,label,a,b) for a in (0,1) for b in (0,1))
            assert got==expected,(B,C,S,H,label)
            assert label not in observed or observed[label]==expected
            observed[label]=expected;counts[label]+=1
            hist[len({(x[1],x[2]) for x in expected})]+=1
            if B==8:figure.append([C,S,H,label])
        assert len(observed)==5*B-4 and len(set(observed.values()))==5*B-4
        assert set(observed)==set(range(5*B-4))
        for label in observed:
            assert counts[label]==multiplicity(B,label)
            assert function(B,*representative(B,label))==observed[label]
        assert dict(hist)=={k:v for k,v in {1:B*(B-1)*(B-2),2:3*B*B-4*B,3:2*B}.items() if v}
        total+=B**3
        rows.append({'radix':B,'triples':B**3,'classes':len(observed),
                     'minimum_bits':(5*B-5).bit_length(),'carry_image_histogram':dict(hist)})
    rng=random.Random(20261027);wide=0
    for w in (1,2,3,8,16,32,64,128,256,512):
        B=1<<w
        triples=[(0,0,0),(0,B-1,0),(B-1,B-1,B-1),(0,B-1,B-1),
                 (B-1,0,1),(B-1,B-1,1)]
        triples += [(rng.randrange(B),rng.randrange(B),rng.randrange(B)) for _ in range(128)]
        for C,S,H in triples:
            label=encode(B,C,S,H)
            assert tuple(evaluate(B,label,a,b) for a in (0,1) for b in (0,1))==function(B,C,S,H)
            assert encode(B,*representative(B,label))==label
            wide+=1
    stage_cases=0
    for bases in ((2,2,2,2),(8,8,8),(256,256,256,256),(3,5,7),(10,10,10)):
        for _ in range(128):
            triples=[tuple(rng.randrange(B) for _ in range(3)) for B in bases]
            labels=[encode(B,*t) for B,t in zip(bases,triples)]
            for a,b in itertools.product((0,1),repeat=2):
                x,y=a,b;expected=0;scale=1;trace=[]
                for B,(C,S,H) in zip(bases,triples):
                    digit,x,y=forward(B,C,S,H,x,y);expected+=scale*digit;scale*=B;trace.append((x,y))
                assert compose(bases,labels,a,b)==(expected,x,y,tuple(trace))
                stage_cases+=1
    classes=[]
    for label in range(36):
        v,table=normal_form(8,label)
        classes.append({'label':label,'residue':v,'carry_table':list(table),
                        'representative':list(representative(8,label)),
                        'multiplicity':multiplicity(8,label)})
    (R/'evidence').mkdir(exist_ok=True)
    (R/'evidence/figure.json').write_text(json.dumps({'radix':8,'triples':figure,'classes':classes},indent=2)+'\n')
    result={'status':'PASS','complete_arbitrary_radix_triples':total,
       'complete_function_responses':4*total,'radix_census':rows,
       'wide_triples_through_512_bits':wide,'mixed_radix_four_input_comparisons':stage_cases,
       'binary32_states':5*(1<<32)-4,'binary32_minimum_bits':35,
       'byte_states':1276,'four_byte_independently_recoverable_states':1276**4,
       'four_byte_minimum_bits':(1276**4-1).bit_length(),
       'elapsed_seconds':time.perf_counter()-started}
    return result
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',default='evidence/verification.json');a=p.parse_args()
    result=experiment();Path(a.output).parent.mkdir(parents=True,exist_ok=True)
    Path(a.output).write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='radix_census'},indent=2))
