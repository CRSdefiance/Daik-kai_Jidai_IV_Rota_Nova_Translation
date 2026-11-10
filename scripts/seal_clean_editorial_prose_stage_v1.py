"""Seal complete clean meanings or independent drafts from readable sectioned data."""
import argparse
from copy import deepcopy
from pathlib import Path
import re
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest


def row_key(row):
    if row['kind']=='ordinary-speech':return str(int(row['id'].rsplit('_R',1)[1]))
    return 'C'+row['id'].split('_CHOICE_',1)[1]


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--stage',choices=['meanings','drafts'],required=True)
    for name in ['input','data','out']:ap.add_argument('--'+name,type=Path,required=True)
    ap.add_argument('--expected-records',type=int,required=True)
    args=ap.parse_args();assert not args.out.exists()
    source=load(args.input);parsed={};contexts={};block=None
    for line in args.data.read_text(encoding='utf-8').splitlines():
        if not line.strip():continue
        key,value=line.split('|',1);assert value.strip() and value==value.strip()
        if key.startswith('@'):
            block=int(key[1:]);assert block not in parsed
            contexts[block]=value;parsed[block]={}
        else:
            assert block is not None and key not in parsed[block]
            parsed[block][key]=value
    if args.stage=='meanings':
        assert source['source_only_not_current_English']
        originals=[r for g in source['groups'] for r in g['records']]
        groups={g['block']:g for g in source['groups']}
    else:
        assert source['source_meanings_sealed_before_independent_drafts'] and source['no_current_story_English_read']
        originals=source['records'];groups=None
    assert len(originals)==args.expected_records and len({r['id'] for r in originals})==len(originals)
    assert set(parsed)=={r['block'] for r in originals}
    for number in parsed:
        assert set(parsed[number])=={row_key(r) for r in originals if r['block']==number},number
    rows=[]
    for original in originals:
        row=deepcopy(original);number=row['block'];text=parsed[number][row_key(row)]
        if args.stage=='meanings':
            blockbytes=bytes.fromhex(groups[number]['clean_block_hex'])
            at=row['source_reference']['offset'];raw=bytes.fromhex(row['source_hex'])
            assert blockbytes[at:at+len(raw)]==raw and not row['covered']
            row.update(source_meaning=text,whole_exchange_context=contexts[number],
                source_meaning_reviewed_from_complete_clean_exchange=True,current_English_not_consulted=True,
                independent_draft_pending=True,contextual_comparison_pending=True,new_credit=0)
            if row['kind']=='ordinary-speech':
                row.update(source_selector=raw[0],source_complete_preamble_hex=blockbytes[at-5:at+1].hex())
        else:
            assert text.isascii() and not any(v in text for v in ['\n','{LB','{ALIGN','{PAD}'])
            macros=re.findall(rb'F[IAOU]',bytes.fromhex(row['source_hex']))
            assert re.findall(r'\bF[IAOU]\b',text)==[m.decode() for m in macros],(row['id'],macros,text)
            assert contexts[number]==row['whole_exchange_context']
            row.update(english=text,independent_draft_pending=False,
                localized_independently_from_sealed_clean_meaning=True,logical_paragraph_without_authored_wraps=True,
                names_andUI_terms_provisional_until_consumer_binding=True,contextual_comparison_pending=True,
                review=dict(source=False,context=False,localization=False,naturalness=False,formatting=False),new_credit=0)
        rows.append(row)
    result=dict(records=rows,source_objects=len(rows),complete_exchanges=len(parsed),no_current_story_English_read=True,
        all_five_gates_pending=True,new_credit=0,full_goal_complete=False,
        evidence={str(p):digest(p) for p in [args.input,args.data,Path(__file__)]})
    if args.stage=='meanings':result.update(source_meanings_sealed_before_independent_drafts=True)
    else:result.update(all_independent_drafts_sealed_before_current_comparison=True,
        current_source_bindings_terms_names_andcontextual_comparisons_pending=True,
        source_meaning_file=str(args.input),source_meaning_file_sha256=digest(args.input))
    save(args.out,result)
    print(dict(stage=args.stage,records=len(rows),complete_exchanges=len(parsed),current_English_not_consulted=True,new_credit=0))


if __name__=='__main__':main()
