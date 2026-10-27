"""Certificate geometry for the radix-eight, three-stage complete-function quotient."""
from __future__ import annotations
from collections import defaultdict
from pathlib import Path
import json

PALETTE=['#b7e3ec','#b9dad2','#d1ccdf','#e8d7af','#a9dedb','#d5bccb','#c2d4ef','#efdcac']

def geometry(data_path: Path):
    data=json.loads(data_path.read_text())
    assert data['radix']==8 and data['stages']==3
    assert data['operand_count']==4096 and data['function_count']==113
    source=[];functions=[];routes=[];seen=set();residue_offsets=defaultdict(int)
    for cell in data['classes']:
        r=cell['residue'];row=residue_offsets[r];residue_offsets[r]+=1
        target=(1305+119*r,282+46*row)
        functions.append({'id':cell['id'],'residue':r,'xy':target,'population':len(cell['operands'])})
        for i,x in enumerate(cell['operands']):
            assert tuple(x) not in seen;seen.add(tuple(x))
            point=(132+12*(x[0]+8*x[1]),270+12*(x[2]+8*x[3]))
            source.append({'operand':x,'xy':point,'residue':r,'class':cell['id'],'representative':i==0})
            routes.append({'from':point,'to':target,'class':cell['id'],'residue':r,'representative':i==0})
    assert len(source)==4096 and len(functions)==113 and len(routes)==4096
    assert [residue_offsets[r] for r in range(8)]==[16]*5+[11]*3
    return data,source,functions,routes
