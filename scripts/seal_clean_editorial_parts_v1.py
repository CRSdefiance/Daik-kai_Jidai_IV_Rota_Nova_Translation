"""Seal complete, ordered clean-first parts without granting any editorial gate."""
import argparse
from collections import Counter
from copy import deepcopy
from pathlib import Path
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--packet',type=Path,required=True)
    parser.add_argument('--parts',type=Path,nargs='+',required=True)
    parser.add_argument('--expected-records',type=int,required=True)
    a=parser.parse_args();root=a.packet.parent
    outputs=[root/f'all{a.expected_records}_clean_meanings_v1.json',root/f'all{a.expected_records}_independent_drafts_v1.json',root/'clean_draft_seal_v1.json']
    assert not any(p.exists() for p in outputs)
    packet=load(a.packet);assert packet['source_only_not_current_English']
    source=[r for g in packet['groups'] for r in g['records']]
    meanings=[];drafts=[];evidence={str(a.packet):digest(a.packet),str(Path(__file__)):digest(Path(__file__))}
    for part in a.parts:
        mp,dp=part/'clean_meanings.json',part/'independent_drafts.json';m,d=map(load,[mp,dp])
        assert m['current_English_not_consulted'] and d['current_English_not_consulted']
        assert d['source_meanings_sha256']==digest(mp) and mp.stat().st_mtime_ns<=dp.stat().st_mtime_ns
        assert len(m['records'])==len(d['records'])
        authored=load(d['authored']);assert authored['source_gloss_precedes_independent_draft_in_each_entry']
        for x,y in zip(m['records'],d['records'],strict=True):
            assert all(x[k]==y[k] for k in ['id','source_hex','source_reference','source_Japanese','source_meaning','whole_exchange_context'])
            assert y['english']==y['independent_English_draft'] and not any(y['review'].values())
            assert y['source_meaning_reviewed_from_complete_clean_exchange'] and y['current_English_not_consulted']
            assert y['english'].isascii() and '\n' not in y['english'] and y['logical_paragraph_without_authored_wraps']
            assert all(y['english'].count(t)==y['source_Japanese'].count(t) for t in ['FI','FA','FO','FU'])
            assert x['source_meaning'] and x['whole_exchange_context']
        meanings.extend(deepcopy(m['records']));drafts.extend(deepcopy(d['records']))
        for p in [mp,dp,Path(d['authored'])]:evidence[str(p)]=digest(p)
    assert len(source)==len(meanings)==len(drafts)==len({r['id'] for r in drafts})==a.expected_records
    for x,y,z in zip(source,meanings,drafts,strict=True):
        assert all(x[k]==y[k]==z[k] for k in ['id','source_hex','source_reference','source_Japanese'])
        z['current_English_comparison_pending']=True
    assert Counter(r['kind'] for r in source)==Counter(r['kind'] for r in drafts)
    common=dict(source_packet=str(a.packet),source_packet_sha256=digest(a.packet),blocks=packet['selected_blocks'],
        complete_exchanges=len(packet['groups']),source_objects=len(source),current_English_not_consulted=True,
        whole_clean_exchanges_read_before_drafting=True,evidence=evidence,new_credit=0,full_goal_complete=False,
        all_original_part_outputs_preserved=True,source_gloss_precedes_independent_draft_in_each_authored_entry=True,
        each_part_meanings_file_written_before_its_draft_file=True)
    save(outputs[0],dict(common,records=meanings,all_clean_meanings_saved=True))
    save(outputs[1],dict(common,records=drafts,all_independent_drafts_saved=True,source_meanings=str(outputs[0]),source_meanings_sha256=digest(outputs[0]),
        translation_policy='natural-dialogue-v2',target_locale='en-US',current_English_comparison_names_terms_consumers_andall_five_gates_pending=True))
    save(outputs[2],dict(source_objects=len(source),complete_exchanges=len(packet['groups']),source_meanings=str(outputs[0]),source_meanings_sha256=digest(outputs[0]),
        independent_drafts=str(outputs[1]),independent_drafts_sha256=digest(outputs[1]),
        source_glosses_andindependent_drafts_all_saved_before_first_current_story_English_exposure=True,
        all_five_review_gates_pending=True,no_current_story_English_read=True,new_credit=0,full_goal_complete=False,
        evidence={**evidence,**{str(p):digest(p) for p in outputs[:2]}}))
    print(f'Sealed{len(source)} clean meanings/drafts in{len(packet["groups"])} complete groups; all gates pending; no credit.')

if __name__=='__main__':main()
