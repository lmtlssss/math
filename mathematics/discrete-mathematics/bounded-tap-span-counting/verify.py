#!/usr/bin/env python3
"""Replay exact counting checks without network access. Author: lmtlssss🜐."""
from __future__ import annotations
import hashlib,itertools,json,random,subprocess,time,argparse
from pathlib import Path
from count import count_fiber,linear_word
from reference import solve as explicit_count
ROOT=Path(__file__).resolve().parent
BUILD=ROOT.parent/'build'

def main() -> None:
    p=argparse.ArgumentParser();p.add_argument('--start',type=int,default=0);p.add_argument('--stop',type=int,default=54);p.add_argument('--bootstrap',action='store_true');a=p.parse_args()
    BUILD.mkdir(exist_ok=True)
    start=time.perf_counter()
    output=ROOT/'evidence/verification.json'
    receipt=json.loads(output.read_text()) if output.exists() else {'checks':{},'scope':'Exact source replay. Recorded times are not performance claims.'}
    if a.bootstrap or not (BUILD/'frontier').exists():
        for src,name in [('frontier.cpp','frontier'),('check_small.cpp','small')]:
            subprocess.run(['g++','-O3','-std=c++17',str(ROOT/src),'-o',str(BUILD/name)],check=True)
        receipt['checks']['complete_small']=json.loads(subprocess.check_output([str(BUILD/'small')],text=True))
        rng=random.Random(0x46524f4e54494552); tested=0
        for w in range(4,9):
            m=(1<<w)-1
            for s,r1,r2 in itertools.combinations(range(1,w),3):
                contexts=[(0,0),(m,m),(1,0),(m,0)]
                contexts += [(rng.randrange(m+1),rng.randrange(m+1)) for _ in range(8)]
                for D,S in contexts:
                    want=[x for x in range(m+1) if (linear_word((x+D)&m,w,r1,r2,s)+linear_word(x,w,r1,r2,s))&m==S]
                    got=count_fiber(w,r1,r2,s,D,S)
                    assert int(got['count'])==len(want),(w,r1,r2,s,D,S)
                    assert (got['witness'] is None if not want else int(got['witness']) in want)
                    tested+=1
        receipt['checks']['all_small_tap_triples']={'queries':tested,'widths':[4,8],'all_equal':True}
        print('SMALL_CHECKS',receipt['checks'],flush=True)
    cases=json.loads((ROOT/'evidence/cases.json').read_text())
    records={x['case']:x for x in receipt['checks'].get('archived_wide_cases',[])}
    for c in cases[a.start:a.stop]:
        w,D,S=c['width'],int(c['D']),int(c['S'])
        native=json.loads(subprocess.check_output([str(BUILD/'frontier'),str(w),'17','19','10',str(D),str(S),'1','20000000','20'],text=True))
        canonical=count_fiber(w,17,19,10,D,S)
        explicit=explicit_count(w,17,19,10,D,S,seconds=60)
        assert native['complete'] and explicit['complete']
        assert native['count']==canonical['count']==explicit['count']==c['count']
        records[c['id']]={'case':c['id'],'width':w,'count':native['count'],'native_states':native['nodes'],'canonical_states':canonical['states'],'explicit_states':explicit['visited'],'all_equal':True}
        receipt['checks']['archived_wide_cases']=sorted(records.values(),key=lambda x:x['case'])
        receipt['checks']['all_54_wide_equal']=len(records)==54
        output.write_text(json.dumps(receipt,indent=2)+'\n')
        print('CASE',c['id'],w,native['count'],flush=True)
    receipt['checks']['archived_wide_cases']=sorted(records.values(),key=lambda x:x['case'])
    receipt['checks']['all_54_wide_equal']=len(records)==54
    receipt['source_sha256']={q.name:hashlib.sha256(q.read_bytes()).hexdigest() for q in [ROOT/'count.py',ROOT/'frontier.cpp',ROOT/'reference.py',ROOT/'check_small.cpp']}
    receipt['last_pass_seconds']=round(time.perf_counter()-start,3)
    output.write_text(json.dumps(receipt,indent=2)+'\n')
    print('VERIFIED_RECORDS',len(records),flush=True)

if __name__=='__main__': main()
