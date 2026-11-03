#!/usr/bin/env python3
"""Exact abstract affine-cycle certificates. Python 3.11+; standard library only.

Two paths are deliberately separate: coefficient-summary composition, and
multivariate polynomial expansion of local state/cost trajectories.
"""
from fractions import Fraction as F
from pathlib import Path
from itertools import product
import argparse
import json
import random

ROOT = Path(__file__).resolve().parent

def matrix(a): return [[F(v) for v in row] for row in a]
def vec(a): return [F(v) for v in a]
def zeros(n,m): return [[F(0) for _ in range(m)] for _ in range(n)]
def identity(n): return [[F(i==j) for j in range(n)] for i in range(n)]
def transpose(a): return list(map(list,zip(*a)))
def mm(a,b): return [[sum(x*y for x,y in zip(row,col)) for col in zip(*b)] for row in a]
def mv(a,v): return [sum(x*y for x,y in zip(row,v)) for row in a]
def dot(a,b): return sum(x*y for x,y in zip(a,b))
def add(a,b): return [[x+y for x,y in zip(u,v)] for u,v in zip(a,b)]
def sub(a,b): return [[x-y for x,y in zip(u,v)] for u,v in zip(a,b)]
def va(a,b): return [x+y for x,y in zip(a,b)]
def vs(a,b): return [x-y for x,y in zip(a,b)]

def rank(a):
    if not a: return 0
    a=[list(map(F,row)) for row in a]
    m,n=len(a),len(a[0]); r=0
    for j in range(n):
        p=next((i for i in range(r,m) if a[i][j]),None)
        if p is None: continue
        a[r],a[p]=a[p],a[r]; z=a[r][j]; a[r]=[v/z for v in a[r]]
        for i in range(m):
            if i!=r:
                z=a[i][j]; a[i]=[v-z*w for v,w in zip(a[i],a[r])]
        r+=1
        if r==m: break
    return r

def encode(x):
    if isinstance(x,F): return int(x) if x.denominator==1 else str(x)
    if isinstance(x,dict): return {str(k):encode(v) for k,v in x.items()}
    if isinstance(x,(list,tuple)): return [encode(v) for v in x]
    return x

# A summary stores x -> A x+b and x^T Q x+2u^T x+v.
def summary(A,b,r=None,constant=0,Q=None):
    d=len(b)
    return {'A':matrix(A),'b':vec(b),'Q':matrix(Q) if Q is not None else zeros(d,d),
            'u':[F(x)/2 for x in (r if r is not None else [0]*d)],'v':F(constant)}
def unit(d): return summary(identity(d),[0]*d)
def compose(p,q):
    """Chronological order: p first, q second."""
    A,b,Q,u,v=p['A'],p['b'],p['Q'],p['u'],p['v']
    B,c,K,w,z=q['A'],q['b'],q['Q'],q['u'],q['v']
    return {'A':mm(B,A),'b':va(mv(B,b),c),
            'Q':add(Q,mm(mm(transpose(A),K),A)),
            'u':va(u,mv(transpose(A),va(mv(K,b),w))),
            'v':v+dot(b,mv(K,b))+2*dot(w,b)+z}
def fold(word):
    p=unit(len(word[0]['b']))
    for s in word: p=compose(p,s)
    return p

def prefixes(word):
    out=[unit(len(word[0]['b']))]
    for s in word: out.append(compose(out[-1],s))
    return out

def state(s,x): return va(mv(s['A'],x),s['b'])
def cost(s,x): return dot(x,mv(s['Q'],x))+2*dot(s['u'],x)+s['v']
def affine_data(word):
    p=prefixes(word); full=p[-1];d=len(full['b'])
    R=[[2*t for t in e['u']] for e in p[1:-1]]
    N=sub(full['A'],identity(d)); K=mm(R,N) if R else []
    h=mv(R,full['b']) if R else []
    total=[2*t for t in full['u']]
    return {'prefixes':p,'R':R,'N':N,'K':K,'h':h,'defect_rank':rank(K),
            'prefix_rank':rank(R),'total_rank':rank([total]+K),
            'consistent':rank([row+[hi] for row,hi in zip(K,h)])==rank(K),
            'fixed_point_consistent':rank([row+[-bi] for row,bi in zip(N,full['b'])])==rank(N)}

# Independent symbolic path: sparse polynomials indexed by exponent tuples.
def clean(p): return {m:c for m,c in p.items() if c}
def pc(c,d): return {(0,)*d:F(c)} if c else {}
def px(j,d): return {tuple(int(i==j) for i in range(d)):F(1)}
def pa(p,q):
    z=p.copy()
    for m,c in q.items(): z[m]=z.get(m,F(0))+c
    return clean(z)
def ps(p,a): return clean({m:c*a for m,c in p.items()})
def pm(p,q):
    z={}
    for m,a in p.items():
        for n,b in q.items():
            e=tuple(x+y for x,y in zip(m,n));z[e]=z.get(e,F(0))+a*b
    return clean(z)
def poly_apply(step,x):
    d=len(x); out=[]
    for row,b in zip(step['A'],step['b']):
        v=pc(b,d)
        for a,p in zip(row,x): v=pa(v,ps(p,a))
        out.append(v)
    return out

def poly_cost(step,x):
    d=len(x); v=pc(step['v'],d)
    for i in range(d):
        v=pa(v,ps(x[i],2*step['u'][i]))
        for j in range(d): v=pa(v,ps(pm(x[i],x[j]),step['Q'][i][j]))
    return v

def run_poly(word,x):
    acc={};prefix_states=[x]
    for s in word:
        acc=pa(acc,poly_cost(s,x));x=poly_apply(s,x);prefix_states.append(x)
    return x,acc,prefix_states

def poly_eval(p,x):
    return sum(c*product_value(v**e for v,e in zip(x,m)) for m,c in p.items())
def product_value(a):
    out=F(1)
    for x in a: out*=x
    return out

def direct_numeric(word,x):
    acc=F(0); states=[x[:]]
    for s in word: acc+=cost(s,x);x=state(s,x);states.append(x)
    return x,acc,states

def poly_gradient_rank(polys,d):
    rows={}
    for k,p in enumerate(polys):
        for m,c in p.items():
            for j,e in enumerate(m):
                if e:
                    alpha=list(m);alpha[j]-=1;key=(k,tuple(alpha))
                    rows.setdefault(key,[F(0)]*d)[j]+=e*c
    return rank(list(rows.values())), rows

def certify(word,affine=False):
    d=len(word[0]['b']); x=[px(j,d) for j in range(d)]
    final,all_cost,transported=run_poly(word,x)
    p=prefixes(word);full=p[-1]
    assert final==poly_apply(full,x)
    assert all_cost==poly_cost(full,x)
    defects=[]
    for k in range(len(word)):
        rotated=word[k:]+word[:k]
        _,r_cost,_=run_poly(rotated,transported[k])
        left=pa(r_cost,ps(all_cost,-1))
        # Boundary expression is computed from the retained prefix only.
        right=pa(poly_cost(p[k],final),ps(poly_cost(p[k],x),-1))
        assert left==right,(k,left,right)
        if k: defects.append(left)
    q,gradient_rows=poly_gradient_rank(defects,d)
    if affine:
        data=affine_data(word)
        for k,poly in enumerate(defects):
            target=pc(data['h'][k],d)
            for j,a in enumerate(data['K'][k]):target=pa(target,ps(x[j],a))
            assert target==poly
        assert q==data['defect_rank']
    # Every binary split agrees with the full chronological coefficient fold.
    for k in range(1,len(word)):
        assert compose(fold(word[:k]),fold(word[k:]))==full
    return {'dimension':d,'length':len(word),'cut_identities':len(word),
            'summary':full,'gradient_rank':q,
            'defect_polynomials':[[{'monomial':m,'coefficient':c} for m,c in sorted(poly.items())] for poly in defects],
            'gradient_coefficient_rows':list(gradient_rows.values())}

PRINCIPAL=[
 summary([[1,1,0],[0,1,0],[0,0,1]],[0,0,0],[1,1,0]),
 summary([[1,0,0],[0,1,0],[1,0,1]],[0,1,0],[1,0,1]),
 summary([[1,0,0],[0,1,0],[0,-1,1]],[0,0,0],[3,0,-2]),
 summary([[2,-2,0],[0,1,0],[-1,1,1]],[2,0,0],[-2,4,3]),
]
INCONSISTENT=PRINCIPAL.copy()
INCONSISTENT[2]=summary([[1,0,0],[0,1,0],[0,-1,1]],[0,0,0],[3,1,-2])
SINGULAR=[summary([[1,0],[0,0]],[0,0],[1,1]),summary([[0,0],[0,1]],[0,1],[2,1])]
# F(x,y)=(x+1,y), prefix C_1(x,y)=x*y.  Defect y retains one scalar.
QUADRATIC=[summary([[1,0],[0,1]],[0,0],Q=[[0,F(1,2)],[F(1,2),0]]),
           summary([[1,0],[0,1]],[1,0])]
# F(x,y)=(2x,y), C_1(x,y)=x*y. Defect x*y has minimal dimension two,
# although the linear cycle displacement has rank one.
QUADRATIC_FULL=[summary([[1,0],[0,1]],[0,0],Q=[[0,F(1,2)],[F(1,2),0]]),
                summary([[2,0],[0,1]],[0,0])]

def make_grid():
    rows=[]; p=affine_data(PRINCIPAL);full=p['prefixes'][-1]
    for x in product(range(-3,4),repeat=3):
        x=vec(x);end,total,states=direct_numeric(PRINCIPAL,x)
        cuts=[]
        for k in range(4):
            _,c,_=direct_numeric(PRINCIPAL[k:]+PRINCIPAL[:k],states[k]);cuts.append(c)
        ds=vs(cuts[1:],[total]*3);t=x[0]+1
        assert ds==[t,2*t,3*t]
        assert end==[2*x[0],x[1]+1,x[2]]
        assert total==4*x[0]+5*x[1]+2*x[2]+1
        rows.append({'state':x,'summary':x[0],'t':t,'cost':total,'transported_cut_costs':cuts,
                     'defects':ds,'cut_invariant':all(a==0 for a in ds)})
    levels=[]
    for t in range(-2,5):
        selected=[r for r in rows if r['t']==t]
        assert len(selected)==49
        levels.append({'t':t,'summary':t-1,'defects':[t,2*t,3*t],'multiplicity':len(selected)})
    return {'title':'Affine Cycles: Exact Cut Defects and Minimal Retained State',
            'doi':'10.5281/zenodo.23931722','example':{
                'dimension':3,'cycle_length':4,'state_count':len(rows),'defect_value_count':7,
                'cut_invariant_count':sum(r['cut_invariant'] for r in rows),'prefix_rank':p['prefix_rank'],
                'defect_rank':p['defect_rank'],'total_rank':p['total_rank'],'R':p['R'],'N':p['N'],
                'K':p['K'],'h':p['h'],'cycle':full,'levels':levels},'states':rows}

def sparse_replacement_certificate():
    old=PRINCIPAL;new=INCONSISTENT
    # Prefix first two maps, one changed map, then last suffix.
    p=fold(old[:2]);v=old[2];w=new[2];s=old[3]
    x=[px(j,3) for j in range(3)];y=poly_apply(p,x)
    oldmid=poly_apply(v,y);newmid=poly_apply(w,y)
    boundary=pa(pa(poly_cost(w,y),ps(poly_cost(v,y),-1)),
                pa(poly_cost(s,newmid),ps(poly_cost(s,oldmid),-1)))
    _,c_old,_=run_poly(old,x);_,c_new,_=run_poly(new,x)
    assert pa(c_new,ps(c_old,-1))==boundary
    return {'cost_difference':[{'monomial':m,'coefficient':c} for m,c in sorted(boundary.items())]}

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--output',default=str(ROOT/'evidence/verification.json'))
    args=parser.parse_args()
    named={}
    for name,w,aff in [('principal',PRINCIPAL,True),('inconsistent',INCONSISTENT,True),
                       ('singular_prefix',SINGULAR,True),('quadratic_translation',QUADRATIC,False),
                       ('quadratic_full_summary',QUADRATIC_FULL,False)]:
        c=certify(w,aff);c['word']=w
        if aff:
            a=affine_data(w);c.update({k:v for k,v in a.items() if k!='prefixes'})
        named[name]=c
    assert named['principal']['R']==matrix([[1,1,0],[2,2,1],[3,3,-1]])
    assert named['principal']['defect_rank']==1 and named['principal']['total_rank']==2
    assert named['principal']['consistent'] and not named['principal']['fixed_point_consistent']
    assert not named['inconsistent']['consistent']
    assert rank(PRINCIPAL[0]['A'])==3 and rank(SINGULAR[0]['A'])==1
    assert named['quadratic_translation']['gradient_rank']==1
    assert named['quadratic_full_summary']['gradient_rank']==2
    # Deterministic exact words: coefficients in {-2,-1,0,1,2}/ {1,2,3}.
    rng=random.Random(23931722);random_cases=[]
    for index in range(64):
        d=1+index%3;n=1+index%6;w=[]
        for _ in range(n):
            A=[[F(rng.randrange(-2,3),rng.randrange(1,4)) for _ in range(d)] for _ in range(d)]
            b=[F(rng.randrange(-2,3),rng.randrange(1,4)) for _ in range(d)]
            r=[F(rng.randrange(-2,3),rng.randrange(1,4)) for _ in range(d)]
            Q=zeros(d,d)
            if index%2:
                for i in range(d):
                    for j in range(i,d):Q[i][j]=Q[j][i]=F(rng.randrange(-2,3),rng.randrange(1,4))
            w.append(summary(A,b,r,F(rng.randrange(-2,3),rng.randrange(1,4)),Q))
        random_cases.append({'case':index,**certify(w,index%2==0)})
    grid=make_grid()
    out={'schema_version':1,'arithmetic':'fractions.Fraction; all coefficient equalities exact',
         'scope':'Abstract affine state maps and polynomial accumulated costs',
         'named':named,'coefficient_cases':random_cases,
         'coefficient_comparison_case_count':len(random_cases)+len(named),
         'cut_identity_count':sum(c['cut_identities'] for c in named.values())+sum(c['cut_identities'] for c in random_cases),
         'nontrivial_cut_identity_count':sum(c['cut_identities']-1 for c in named.values())+sum(c['cut_identities']-1 for c in random_cases),
         'zero_cut_normalization_count':len(named)+len(random_cases),
         'generator_seed':23931722,
         'sparse_replacement':sparse_replacement_certificate(),
         'grid':{'state_count':343,'distinct_defects':7,'fibre_cardinality':49,'zero_defect_states':49},
         'proof_scope':'Theorems are established in paper.tex; finite certificates confirm their named and stated rational instances.'}
    Path(args.output).parent.mkdir(parents=True,exist_ok=True)
    Path(args.output).write_text(json.dumps(encode(out),ensure_ascii=False,indent=2)+'\n')
    (ROOT/'evidence/figure.json').write_text(json.dumps(encode(grid),ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:out[k] for k in ['coefficient_comparison_case_count','cut_identity_count','grid']},indent=2))

if __name__=='__main__':main()
