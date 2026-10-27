"""Refresh remaining clean/current leads without adding editorial credit."""
from copy import deepcopy
from pathlib import Path
from shutil import copy2
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_next44_checkpoint_v3423')
PRIOR=Path('work/analysis/editorial_handoff_verification_v3421/verified_handoff.json')
FULL=Path('work/analysis/lil_remaining_B138_B140_source_v3422/complete111_remaining_clean_current_context.json')
NEXT=FULL.with_name('next44_B138_clean_current_context.json')
SUMMARY='''V3423 preserves independently audited V3420 completion in registered experimental V3416: 4,880 fresh contextual rereads, integrated and completed, with 3,207 historically revised and 1,673 retained. Source/prose is 4,883 including 3,053 SC2 records; all 3,281 reviewed route objects are integrated. V3416 retains 523 manifest batches and 114 accepted layers, exact whole-ROM clean-input patch reconstruction, 31 fresh opening/town framebuffer matches to V3372 and a viewed six-frame sheet. The rejected V3409 profile and first hook remain preserved; the separate V3416 hook uses the validated v2 compiler. V1492 remains promoted. This source refresh adds no review or completion credit.

The remaining B138-B140 lead contains 111 physical speeches across three blocks and 257 commands. It excludes all 422 completed speeches from the prior 533-location B122-B140 inventory, including the newly completed 48 B137 speeches. Entry/copy classification still determines unique player-facing scope. All clean/current native command shapes and complete speech preambles match. Next B138 contains 44 progressive speeches, 111 commands, 45 relative sites, 10 predicates and one native event query. It has source FO1 and seven static selector values, with no FE, source00, choice, pause, dynamic-selector or 4100 objects. Current name/voice, FO macro, query, predicate and entry contracts must be bound before review. The historical London snapshot does not establish current event eligibility or earned progression. Whole clean-exchange reading, fresh glosses and older-English comparison are still pending for B138.

Continue with B138's actor/control/entry contracts, then read the complete clean exchange and write fresh glosses before comparing older English. Retain effective wording that works with individual reasons, and complete native display, relocation, reference, representative and registered-release gates. B139-B140 and every wider untouched storyline, shared shop/town dialogue, random scene and remaining player-facing prose stay in scope. COMMON750-752 callers, canonical Maria32, SourceItems/LocalProduct, five named-target leads, raw B141/SC3B109 classification and exact-record Proof of Supremacy/Proof of Conquest reconciliation remain open. Keep unresolved graphics/all 18 plaques separate and retain the later older-record technical re-audit and queued0D validation gap. Preserve every ROM, earlier translation, draft, executed producer/proof/failure and clean/canonical input. No completed record is silently renamed or recounted; no old runtime defect is asserted. Full goal active; all jobs terminal.'''

if __name__=='__main__':
    assert not ROOT.exists();lp=Path('translations/editorial_review_current_v1.json');ledger=read(lp);before=deepcopy(ledger)
    assert sha(lp.read_bytes())==read(PRIOR)['ledger_sha256'];full,focus=map(read,[FULL,NEXT])
    assert len(full['records'])==111 and full['completed422_source_location_speeches_excluded']==422 and sum(len(b['all_clean_native_commands']) for b in full['blocks'])==257
    assert len(focus['records'])==44 and len(focus['blocks'][0]['all_clean_native_commands'])==111
    commands=focus['blocks'][0]['all_clean_native_commands']
    assert sum(c['word'] in [0x100,0x200,0x300,0x400] for c in commands)==45 and sum(c['word']==0x8000 for c in commands)==10 and sum(c['word']==0x8100 for c in commands)==1
    assert not any(c['word'] in [0x2000,0x2100,0x4100] for c in commands)
    assert len({r['source_selector'] for r in focus['records']})==7 and {m:sum(bytes.fromhex(r['source_hex']).count(m.encode()) for r in focus['records']) for m in ['FI','FA','FO']}=={'FI':0,'FA':0,'FO':1}
    documents=[Path('docs')/n for n in ['editorial_handoff_current.md','translation_progress.md','editorial_review_goal.md','todo.md','known_issues.md']]
    assert documents[0].read_text(encoding='utf-8').startswith('# Current editorial handoff - V3420');ROOT.mkdir(parents=True)
    for p in [lp,*documents]:copy2(p,ROOT/(p.name+'.before'))
    lead=dict(status='clean-current-structural-source-lead;actors-entry-macro-query-whole-context-glosses-prose-native-release-pending',full_packet=str(FULL),full_packet_sha256=sha(FULL.read_bytes()),remaining_physical_speeches=111,remaining_blocks=[138,139,140],remaining_commands=257,completed_physical_speeches_excluded=422,unique_player_facing_count_requires_entry_copy_classification=True,next_packet=str(NEXT),next_packet_sha256=sha(NEXT.read_bytes()),next_blocks=[138],next_speeches=44,next_commands=111,next_relative_sites=45,next_predicates=10,next_event_queries=1,next_source_macro_counts={'FI':0,'FA':0,'FO':1},current_actor_voice_entry_and_macro_binding_pending=True,current_original_event_query_binding_pending=True,whole_clean_exchange_and_fresh_glosses_and_oldEnglish_comparison_pending=True,new_source_prose_reviews=0,new_completed_records=0,new_emulator_runs=0,actual_selected_next_IDs=[],full_goal_complete=False)
    ledger['lil_after_B137_next_source_lead_v3423']=lead
    inventory=deepcopy(read(ledger['unfinished_editorial_scope_v3420']['path']));inventory['next_uncredited_source_lead_v3423']=lead
    inventory['next_focus']='Bind B138 actors/voices, entry, FO1, ten predicates, one original event query and 45 relative sites. Read the complete clean exchange and write fresh glosses before older-English comparison. Review 44 speeches and all native/reference/representative/release gates; continue all 111 physical leads and the wider editorial objective. Proof consistency, Maria32 and COMMON3 remain open; graphics separate; older technical audit later.'
    inv=ROOT/'unfinished_editorial_scope_inventory.json';save(inv,inventory)
    ledger['unfinished_editorial_scope_v3423']=dict(path=str(inv),sha256=sha(inv.read_bytes()),incomplete_COMMON=3,incomplete_route_source_prose=0,next_uncredited_physical_speeches=111,next_focus_speeches=44,Proof_terminology_consistency_open=True,canonical_Maria32_pending_uncredited=True,full_goal_complete=False)
    for u in ledger['coverage_units']:
        if u['id']=='all-route-scenes':u['next']=inventory['next_focus']
    evidence={str(p):sha(p.read_bytes()) for p in [PRIOR,FULL,NEXT,inv,Path('scripts/map_lil_remaining_B138_B140_source_v3422.py'),Path(__file__)]}
    ledger['lil_next44_checkpoint_v3423']=dict(summary=SUMMARY,evidence=evidence,new_source_prose_reviews=0,new_completed_records=0,goal_turn_classification='progress',full_goal_complete=False);ledger['latest_checkpoint']=SUMMARY
    changed={'lil_after_B137_next_source_lead_v3423','unfinished_editorial_scope_v3423','coverage_units','lil_next44_checkpoint_v3423','latest_checkpoint'}
    assert all(ledger[k]==v for k,v in before.items() if k not in changed) and set(ledger)-set(before)==changed-{'coverage_units','latest_checkpoint'}
    assert ledger['goal_status']=='active' and not ledger['full_goal_complete'];save(lp,ledger)
    section='## V3423: remaining 111 source leads; V3416 completion preserved\n\n'+SUMMARY+'\n\nNext source: '+NEXT.as_posix()+'. Unfinished scope: '+inv.as_posix()+'.\n\n'
    for i,p in enumerate(documents):
        first,rest=p.read_text(encoding='utf-8').split('\n',1);p.write_text(('# Current editorial handoff - V3423' if i==0 else first)+'\n\n'+section+rest,encoding='utf-8',newline='\n')
    save(ROOT/'checkpoint_receipt.json',dict(checkpoint='V3423',evidence=evidence,updated_files={str(p):sha(p.read_bytes()) for p in [lp,*documents]},prior_verified_handoff=str(PRIOR),fresh_reread=4880,fresh_integrated=4880,fresh_pending=0,source_prose=4883,new_completed_records=0,new_source_prose_reviews=0,next_remaining_physical_speeches=111,next_focus_speeches=44,next_focus_commands=111,next_focus_relative_sites=45,next_focus_predicates=10,next_focus_event_queries=1,all_jobs_terminal=True,full_goal_complete=False))
    print('V3423 preserves 4880 completed in V3416;111 remaining physical leads,next B138 44 speeches. No new review credit;full goal active.')
