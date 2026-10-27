#!/usr/bin/env python3
"""Whole-function enumeration against direct cascaded integer arithmetic.
The direct oracle does not use partial sums, profiles, or the counting formula.
"""
from __future__ import annotations
from collections import defaultdict
from itertools import product
from pathlib import Path
import argparse, json, random, time
from cascade import describe, arrangement_number, function_count, minimum_bits, encode_two, decode_two, rank_function, unrank_function


def direct(B, operands, bits):
    residue = operands[0]
    carries = []
    for operand, bit in zip(operands[1:], bits):
        raw = residue + operand + bit
        carries.append(int(raw >= B))
        residue = raw - B if raw >= B else raw
    return (residue, *carries)


def census(B, k, save_figure=False):
    incoming = list(product((0, 1), repeat=k))
    tables = {}
    full_by_descriptor = {}
    support = defaultdict(set)
    groups = defaultdict(list)
    for operands in product(range(B), repeat=k+1):
        table = tuple(direct(B, operands, bits) for bits in incoming)
        descriptor = describe(B, operands)
        assert tuple(descriptor.evaluate(bits) for bits in incoming) == table
        # Both directions of the correspondence are checked, not only its size.
        assert table not in tables or tables[table] == descriptor
        assert descriptor not in full_by_descriptor or full_by_descriptor[descriptor] == table
        tables[table] = descriptor
        full_by_descriptor[descriptor] = table
        carry_table = tuple(row[1:] for row in table)
        support[carry_table].add(descriptor.residue)
        if save_figure:
            groups[descriptor].append(operands)
    labels = {}
    for descriptor, table in full_by_descriptor.items():
        label=rank_function(descriptor)
        assert label not in labels, (B,k,label,'duplicate label')
        labels[label]=table
        representative=unrank_function(B,k,label)
        assert tuple(direct(B,representative,bits) for bits in incoming)==table
        assert describe(B,representative)==descriptor
    assert set(labels)==set(range(function_count(B,k)))
    assert len(tables) == function_count(B,k), (B,k,len(tables),function_count(B,k))
    if k < B:
        regular = set(range(B-k))
        regular_maps = [c for c, v in support.items() if v == regular]
        # At k=B-1 the regular interval is {0}; upper residues remain distinct.
        assert len(regular_maps) == arrangement_number(k)
        if k:
            expected_exceptional = arrangement_number(k) - arrangement_number(k-1)
            for v in range(B-k,B):
                assert sum(values == {v} for values in support.values()) == expected_exceptional
        for values in support.values():
            assert values == regular or (len(values) == 1 and next(iter(values)) >= B-k)
    if k >= B-1:
        assert all(len(values)==1 for values in support.values())
    result = {'radix':B,'stages':k,'operand_tuples':B**(k+1),
              'incoming_cases_per_tuple':2**k,'function_classes':len(tables),
              'minimum_fixed_bits':minimum_bits(B,k),'carry_maps':len(support)}
    if save_figure:
        classes=[]
        ordered=sorted(groups,key=rank_function)
        for i,d in enumerate(ordered):
            classes.append({'id':i,'residue':d.residue,'profiles':d.profiles,
                            'operands':groups[d], 'representative':groups[d][0],
                            'truth_table':[direct(B,groups[d][0],bits) for bits in incoming]})
        out=Path('evidence/figure.json');out.parent.mkdir(parents=True,exist_ok=True)
        out.write_text(json.dumps({'radix':B,'stages':k,'operand_count':B**(k+1),
                                  'function_count':len(classes),'classes':classes},separators=(',',':'))+'\n')
    return result


def main():
    p=argparse.ArgumentParser();p.add_argument('--output',default='evidence/verification.json')
    args=p.parse_args();start=time.perf_counter();rows=[]
    # Frozen scope: all listed radices/stages, bounded by 1.1m direct incoming evaluations per panel.
    for B in range(2,11):
        for k in range(0,9):
            if B**(k+1)*2**k > 1_100_000:continue
            result=census(B,k,save_figure=(B==8 and k==3));rows.append(result)
            print(json.dumps(result),flush=True)
    two_checks=0
    for B in range(2,25):
        seen=set()
        for c,s,h in product(range(B),repeat=3):
            label=encode_two(B,c,s,h);seen.add(label)
            for a,b in product((0,1),repeat=2):
                assert decode_two(B,label,a,b)==direct(B,(c,s,h),(a,b))
                two_checks+=1
        assert seen==set(range(5*B-4))
    rng=random.Random(27102026);wide=[];wide_checks=0
    for w in (8,16,32,64,128,256,512):
        B=1<<w
        for k in (1,2,3,4,7,12):
            for case in range(24):
                if case<12:
                    pool=[0,1,B-1,B-2,B-3,B//2]
                    operands=tuple(rng.choice(pool) for _ in range(k+1))
                else:operands=tuple(rng.randrange(B) for _ in range(k+1))
                desc=describe(B,operands)
                label=rank_function(desc)
                representative=unrank_function(B,k,label)
                assert describe(B,representative)==desc
                incoming=list(product((0,1),repeat=k)) if k<=4 else [tuple(rng.randrange(2) for _ in range(k)) for _ in range(32)]
                for bits in incoming:
                    assert desc.evaluate(bits)==direct(B,operands,bits);wide_checks+=1
                if k==2:
                    label=encode_two(B,*operands)
                    for bits in product((0,1),repeat=2):assert decode_two(B,label,*bits)==direct(B,operands,bits)
            wide.append({'width':w,'stages':k,'source_cases':24})
    for B,k in ((2,15),(3,12),(8,7),(8,8),(8,12),(1<<32,3),(1<<128,8),(1<<512,12)):
        count=function_count(B,k)
        for label in {0,1,count-2,count-1,*[rng.randrange(count) for _ in range(40)]}:
            representative=unrank_function(B,k,label)
            assert rank_function(describe(B,representative))==label
    numeric=[{'stages':k,'word_bits':32,'functions':function_count(2**32,k),
              'minimum_bits':minimum_bits(2**32,k),'operand_bits':32*(k+1)} for k in (1,2,3,4,5,8)]
    payload={'status':'PASS','panels':rows,'complete_operand_tuples':sum(x['operand_tuples'] for x in rows),
             'direct_incoming_evaluations':sum(x['operand_tuples']*x['incoming_cases_per_tuple'] for x in rows),
             'dense_codec_classes_checked':sum(x['function_classes'] for x in rows),
             'two_stage_codec_output_checks':two_checks,'wide_panels':wide,'wide_output_checks':wide_checks,
             'arrangement_numbers':[arrangement_number(k) for k in range(11)],'numeric_examples':numeric,
             'elapsed_seconds':time.perf_counter()-start,'scope':'Exact complete functions; finite checks supplement the general proof.'}
    out=Path(args.output);out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps(payload,indent=2)+'\n')
    print('VERIFIED',payload['complete_operand_tuples'],payload['direct_incoming_evaluations'],'wide',wide_checks,'seconds',payload['elapsed_seconds'],flush=True)

if __name__=='__main__':main()
