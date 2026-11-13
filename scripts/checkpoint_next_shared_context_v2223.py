"""Audited next50 source packet; no unreviewed source or completion credit."""
from pathlib import Path
from collections import Counter
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/shared_context_handoff_v2223')
PACKET=Path('work/analysis/shared_context_source_v2222/all50_clean_current_context_catalog.json')
LEDGER=Path('translations/editorial_review_current_v1.json')
OLD=Path('translations/shared_dialogue_editorial_manuscript_v3.json')
SUMMARY=('V2223 preflights the next50 shared COMMON entries1020-1069 with exact clean/current references, immediate catalog neighbors and complete paragraph matches to the frozen speaker-corrected manuscriptv3. '
 'This extraction adds zero source/prose or fresh-pass credit. Latest completed reviews remain V2211 recruitment/schemes106 and V2221 barmaid31:137 newly reconciled justified retentions in this continuation. '
 'Fresh coverage1107 reread/1107 integrated-reconciled/0pending; historical2143,source/prose2259 and116 incompleteCOMMON unchanged. '
 'Another1036 historical completions remain:1035COMMON plus SC2B294R73. All never-reviewed routes/shared town/shop/random/player prose remain in scope. '
 'The next50 include shared warnings, village/fleet recruitment and private barmaid exchanges. Role1 must be reviewed as First Mate with original officer fallback, not Barkeep; the historical v782 correction is only context, not automatic fresh completion. '
 'Current V2171 recruitment capture2202 already observes1042 and has a complete native font continuation, actual transition images and paired state/model controls; reuse it where relevant without inventing new visits. '
 'Proceed with fresh whole-consumer/context/prose, current native layouts/full fonts and representative or already-bound gameplay evidence; no exhaustive individual conditional visits required. '
 'Registered V2171,its492batches/114accepted layers and exact clean-input patch stay unchanged. All ROMs and earlier translations preserved. V1492 stays promoted;canonical and clean input unchanged. '
 'Full objective active. Separate graphics/all18 plaques,SC3B109 classification and the later older-record technical re-audit remain open. All jobs terminal.')

if __name__=='__main__':
    assert not ROOT.exists();ROOT.mkdir(parents=True)
    l,d,old=read(LEDGER),read(PACKET),read(OLD)
    f=l['contextual_story_natural_dialogue_pass_v1871']
    assert(f['fresh_pass_records_explicitly_reread'],f['fresh_pass_records_integrated'],f['fresh_pass_records_pending_native_actual_release'])==(1107,1107,0)
    assert d['selected_IDs']==list(range(1020,1070))and len(d['records'])==50
    rows={r['message_id']:r for r in old['records']}
    assert all(r['source_hex']==rows[r['message_ID']]['source_hex']and bytes.fromhex(r['current_hex'])==b' '+rows[r['message_ID']]['english'].removesuffix('{PAD}').encode('ascii')for r in d['records'])
    inv=Path('work/analysis/barmaid_context_completion_v2221/remaining_historical_fresh_review_inventory.json');remaining=read(inv)
    assert remaining['remaining']==1036 and Counter(r['file_path']for r in remaining['records'])=={'/COMMON/MESFILE.DK4':1035,'/data/SC2.DK4':1}
    keys={(r['file_path'],r['id'])for r in f['record_keys']}
    assert not keys&{('/COMMON/MESFILE.DK4',f'COMMON_MESSAGE_{n}')for n in d['selected_IDs']}
    assert sha(Path(d['current_ROM']).read_bytes())==d['current_ROM_sha256']==l['current_integrated_candidate']['sha256']
    continuation=Path('work/analysis/recruitment_actual_continuations_v2206/actual_snapshot_native_font_continuations.json')
    native=read(continuation);case,=[r for r in native['cases']if r['message_ID']==1042]
    assert case['complete_native_return']and case['SP_preserved']and case['callee_registers_preserved']and not case['faults']and not case['error']
    docs=[Path('docs')/p for p in('editorial_handoff_current.md','translation_progress.md','editorial_review_goal.md','todo.md','known_issues.md')]
    for p in[LEDGER,*docs]:(ROOT/(p.name+'.before')).write_bytes(p.read_bytes())
    evidence_paths=[PACKET,OLD,inv,continuation,Path('work/analysis/recruitment_scheme_completion_v2211/completion_receipt.json'),Path('work/analysis/barmaid_context_completion_v2221/completion_receipt.json'),Path('work/analysis/recruitment_actual_verification_v2208/ordinary_recruitment_foreground_state_transitions.json'),Path('scripts/context_shared_dialogue_v781.py'),Path('scripts/review_shared_speaker_context_v782.py'),Path('scripts/probe_shared_layout_v781.py'),Path('scripts/verify_shared_village_gameplay_v782.py'),Path('scripts/verify_private_barmaid_gameplay_v783.py'),Path(__file__)]
    evidence={str(p):sha(p.read_bytes())for p in evidence_paths}
    proof=ROOT/'next50_preflight.json'
    save(proof,dict(summary=SUMMARY,next_IDs=list(range(1020,1070)),packet=str(PACKET),packet_sha256=sha(PACKET.read_bytes()),prior_speaker_corrected_manuscript=str(OLD),prior_manuscript_sha256=sha(OLD.read_bytes()),all50_source_and_complete_current_paragraphs_match=True,all50_source_context_prose_native_display_reconciliation_pending=True,existing1042_native_and_actual_evidence_available=True,no_new_source_prose_reread_or_completion_credit=True,current_fresh_count=1107,remaining_historical_count=1036,evidence=evidence,full_goal_complete=False))
    l['next_shared_contextual_source_packet_v2223']=dict(path=str(PACKET),sha256=sha(PACKET.read_bytes()),preflight=str(proof),preflight_sha256=sha(proof.read_bytes()),IDs=list(range(1020,1070)),source_prose_or_fresh_credit=0,role1_FirstMate_fallback_metadata_must_be_preserved=True)
    l['latest_checkpoint']=SUMMARY;save(LEDGER,l)
    section='## V2223: Next shared50 source packet; zero new credit\n\n'+SUMMARY+'\n\nExact source/current packet: '+PACKET.as_posix()+'. Preflight: '+proof.as_posix()+'. Current completed individual reviews: translations/recruitment_schemes_contextual_final_review_v1.json and translations/barmaid_contextual_final_review_v1.json. Read the next50 source and complete caller exchanges afresh; do not treat catalog adjacency or the old manuscript as an actual dialogue sequence.\n\n'
    text=docs[0].read_text();assert text.startswith('# Current editorial handoff - V2221')
    text=text.replace('# Current editorial handoff - V2221','# Current editorial handoff - V2223',1)
    first,rest=text.split('\n',1);docs[0].write_text(first+'\n\n'+section+rest,newline='\n')
    for p in docs[1:]:
        first,rest=p.read_text().split('\n',1);p.write_text(first+'\n\n'+section+rest,newline='\n')
    receipt=ROOT/'handoff_receipt.json'
    save(receipt,dict(checkpoint='V2223',classification='progress',fresh_integrated=1107,latest_completed_batches_records=137,next_source_packet_records=50,new_credit_for_packet=0,remaining_historical_fresh_reviews=1036,candidate_sha256=d['current_ROM_sha256'],evidence=evidence,updated_files={str(p):sha(p.read_bytes())for p in[LEDGER,*docs,proof]},all_jobs_terminal=True,full_goal_complete=False))
    print(dict(checkpoint='V2223',fresh_integrated=1107,next_source_records=50,new_credit=0,full_goal_complete=False),flush=True)
