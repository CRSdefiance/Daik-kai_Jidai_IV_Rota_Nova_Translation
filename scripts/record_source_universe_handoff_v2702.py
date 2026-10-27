"""Checkpoint the native-source census;zero prose or completion credit."""
from pathlib import Path
from copy import deepcopy
from shutil import copy2
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/source_universe_checkpoint_v2702')
SOURCE=Path('work/analysis/editorial_source_universe_v2701c/source_universe_inventory.json')
SUMMARY=(
    'V2702 adds a clean native-source coverage inventory beyond the old decoded CSV extraction. It adds no translation or editorial completion credit. '
    'COMMON has 3,668 proven native message entries, each with exact clean/current references and bytes. The four route files contain 70,419 nonempty native NUL objects, including binary/control data; this is not a dialogue count or a whole-ROM prose denominator. '
    'Strict CP932 decoding detects Japanese in 23,552 route objects and rejects 2,278. Of the rejected objects, 103 decode to Japanese after the first byte. These are diagnostic leads requiring original-consumer and presentation-prefix classification; no ambiguous Shift-JIS byte is stripped or approved. Decoder acceptance is also not sufficient to identify prose. '
    'All 2,256 existing file-qualified completion keys reconcile: 1,599 COMMON entries, 117 SC0, 73 SC1, 429 SC2 and 38 SC3. The SC2 count includes eight previously reviewed menu-choice subobjects with separate option identifiers, whose exact source bytes, block offsets and containing NUL objects are verified. They add no new objects or review credit and do not inventory every unseen choice opcode. '
    'The preserved initial2701 census used unpadded route segment identifiers;2701b aligns their spelling with the ledger, and2701c additionally accounts for the eight existing choice subobjects. Earlier outputs remain preserved and carry no new credit. Current route files are hash-bound without inventing current record mappings. '
    'The latest completed editorial batches remain the 24 capture/surrender reports at V2693 and 32 battle reactions at V2699, all freshly retained with individual reasons and exact source/current references. Their current native/font, visual, source, registered-release and representative-sampling gates passed; independent audits2694and2700passed. '
    'Fresh coverage remains2256 reread /2256 integrated-reconciled /zero pending. Completion remains2256(1575historically revised,681retained);source/prose2259 and3incompleteCOMMON remain unchanged. Market750-752still need verified callers before final contextual authoring. Five named-target2187-2191leads remain separately uncredited. '
    'Continue source-consumer classification and untouched route/shared/town/shop/random/help/player-facing prose while resolving those market callers;the three entries do not block independent wider review. Every storyline remains in scope, including prior translations and decoder-rejected source. '
    'Registered cumulative experimentalV2674 remains494batches/114accepted layers with its exactly reconstructable clean-input patch. No ROM, prose, runtime, registry, builder, profile, manifest or patch changes and no new emulator run occur in this census checkpoint. V1492 remains promoted. All ROMs, earlier translations, canonical/clean inputs and executed proofs are preserved. '
    'Separate graphics/all18 plaques, SC3B109 classification and later older-record technical re-audit remain open. Full goal active;all jobs terminal.'
)
if __name__=='__main__':
    assert not ROOT.exists();lp=Path('translations/editorial_review_current_v1.json');ledger=read(lp);priorpath=Path('work/analysis/editorial_handoff_verification_v2700/verified_handoff.json');prior=read(priorpath);source=read(SOURCE)
    assert sha(lp.read_bytes())==prior['ledger_sha256']==source['ledger_sha256']
    assert source['completion_credit_added']==source['source_prose_credit_added']==0 and source['completed_editorial_keys']==2256
    files=source['files'];assert sum(f['native_objects'] for f in files[1:])==70419
    assert sum(f['counts'].get('strict-cp932-rejected',0) for f in files[1:])==2278 and sum(f['rejected_one_byte_suffix_Japanese_leads'] for f in files[1:])==103
    assert sum(f['completed_key_matches']+f.get('completed_choice_subobjects',0) for f in files)==2256
    for f in files:assert sha(Path(f['path']).read_bytes())==f['sha256']
    docs=[Path('docs')/n for n in ['editorial_handoff_current.md','translation_progress.md','editorial_review_goal.md','todo.md','known_issues.md']]
    assert docs[0].read_text(encoding='utf-8').startswith('# Current editorial handoff - V2699')
    ROOT.mkdir(parents=True)
    for p in [lp,*docs]:copy2(p,ROOT/(p.name+'.before'))
    evidence={str(p):sha(p.read_bytes()) for p in [SOURCE,priorpath,Path(__file__),*[Path(f['path']) for f in files]]}
    ledger['native_source_universe_inventory_v2701c']=dict(path=str(SOURCE),sha256=sha(SOURCE.read_bytes()),source_files=[f['file_path'] for f in files],COMMON_native_entries=3668,route_nonempty_NUL_objects_including_binary_controls=70419,
        route_strict_decode_rejections=2278,rejected_one_byte_suffix_Japanese_diagnostic_leads=103,completed_non_NUL_choice_subobjects=8,completed_keys_reconciled=2256,not_all_ROM_prose_or_dialogue_denominator=True,completion_credit_added=0,full_goal_complete=False)
    ledger['raw_source_coverage_revisit'].update(latest_exact_native_inventory=str(SOURCE),latest_exact_native_inventory_sha256=sha(SOURCE.read_bytes()),
        next_action=source['next_action'],classification_status='open-source-consumer-classification-required;decoder-labels-are-diagnostic-only')
    inventory=deepcopy(read(ledger['unfinished_editorial_scope_v2699']['path']));inventory['native_source_universe_inventory']=ledger['native_source_universe_inventory_v2701c']
    for unit in inventory['broader_coverage_units']:
        if unit['id']=='all-route-scenes':
            unit.update(reviewed_route_records=657,completed_route_records=657,completed_file_qualified_counts={k:v for k,v in ledger['completed_editorial_record_counts_by_file'].items() if k!='/COMMON/MESFILE.DK4'},
                note='657existing route completions include8SC2choice subobjects;all have the contextual pass. This is not complete route coverage. Untouched scenes,raw rejected objects andunseen choices require source-consumer classification andreview.',next='Continue untouched source-bound route scenes andshared/town/random prose while classifying raw native objects;do not rely on CSV acceptance as a completeness boundary.')
    inventory.update(next_focus=source['next_action'],raw_source_coverage_revisit=deepcopy(ledger['raw_source_coverage_revisit']))
    inv=ROOT/'unfinished_editorial_scope_inventory.json';save(inv,inventory)
    ledger['unfinished_editorial_scope_v2702']=dict(path=str(inv),sha256=sha(inv.read_bytes()),incomplete_COMMON=3,full_goal_complete=False)
    ledger['source_universe_checkpoint_v2702']=dict(summary=SUMMARY,evidence=evidence,new_completed_records=0,source_prose_credit_added=0,goal_turn_classification='progress',full_goal_complete=False)
    ledger['latest_checkpoint']=SUMMARY;save(lp,ledger)
    section='## V2702: Native source coverage census; wider review remains open\n\n'+SUMMARY+'\n\nNative inventory: '+SOURCE.as_posix()+'. Latest editorial final review: translations/battle_reactions_contextual_final_review_v1.json. Current parser: dk4tool.patch.surrender_advice_contextual_v1.current_entries. Current bounded context: scripts/current_common_native_context_v2677.py. Unfinished scope: '+inv.as_posix()+'.\n\n'
    for i,p in enumerate(docs):
        first,rest=p.read_text(encoding='utf-8').split('\n',1);p.write_text(('# Current editorial handoff - V2702' if i==0 else first)+'\n\n'+section+rest,encoding='utf-8',newline='\n')
    evidence[str(inv)]=sha(inv.read_bytes())
    save(ROOT/'completion_receipt.json',dict(checkpoint='V2702',summary=SUMMARY,new_completed_records=0,new_current_prose_revisions=0,fresh_justified_retentions=0,fresh_reread=2256,fresh_integrated=2256,fresh_pending=0,completed_records=2256,historical_revised=1575,historical_retained=681,source_prose_reviewed=2259,COMMON_incomplete=3,
        evidence=evidence,updated_files={str(p):sha(p.read_bytes()) for p in [lp,*docs]},source_universe=str(SOURCE),source_universe_sha256=sha(SOURCE.read_bytes()),candidate=ledger['current_integrated_candidate']['path'],candidate_sha256=ledger['current_integrated_candidate']['sha256'],patch=ledger['current_integrated_candidate']['patch'],patch_sha256=ledger['current_integrated_candidate']['patch_sha256'],goal_turn_classification='progress',new_emulator_runs=0,all_jobs_terminal=True,full_goal_complete=False))
    print('V2702source-object census recorded:2256completion keys reconcile;2278decode rejections/103suffix leads remain classification-only. No new prose/completion/ROM credit;full goal active.')
