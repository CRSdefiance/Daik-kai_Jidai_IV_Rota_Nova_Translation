"""Next54 provenance preflight, without advancing editorial coverage."""
from pathlib import Path
from collections import Counter
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/palace_inn_context_handoff_v2249')
PACKET=Path('work/analysis/palace_inn_context_source_v2248/all54_clean_current_context_catalog.json')
LEDGER=Path('translations/editorial_review_current_v1.json')
OLD=[Path('translations/palace_editorial_manuscript_v4.json'),Path('translations/inn_editorial_manuscript_v5.json')]
SUMMARY=('V2249 prepares the next54 COMMON entries1146-1199:31 Palace and23 Inn records with exact clean/current spans and immediate neighbors. All54 complete paragraphs match frozen Palacev4/Innv5. '
 'This is source extraction/provenance only and adds zero source/prose, fresh-reread or completion credit. The next whole-consumer review must establish introduction versus recommendation letters, market-share and contract constraints, defense/treasure monthly payment context, stay-length grammar and actual time providers, rumor argument order, officer voices and departure branches. '
 'Do not infer dialogue chronology from catalog adjacency or count historical native approval as a fresh editorial pass. Auxiliary Palace menu labels and Inn time phrases need source/context review as applicable, without duplicate COMMON credit. '
 'Latest V2247 reconciles79 Guild/courier/letter retentions with individual source glosses/reasons,2823 current native layouts,186 complete native font samples on16 viewed sheets, a fixture-free15601frame current Seoul run with11 holds/six reviewed IDs,10 paired state controls and8 menu/return frames, plus35 explicitly historical holds across21 IDs. '
 'Fresh coverage1236 reread/1236 integrated-reconciled/0pending. Historical2143=1498revised+645retained,source/prose2259 and116 incompleteCOMMON unchanged. Another907 historical completions remain:906COMMON andSC2B294R73. All never-reviewed storylines/shared town/shop/random/player prose remain in scope. '
 'Current registered V2171 remains492batches/114accepted layers with exactly reconstructable clean-input patch. No new ROM/profile/registry/manifest/patch is needed for retained wording. All generated ROMs and earlier translations preserved;V1492 remains promoted and canonical/clean input unchanged. '
 'Full objective active. Separate graphics/all18 plaques,SC3B109 classification and later older-record technical re-audit remain open. All jobs terminal.')
if __name__=='__main__':
    assert not ROOT.exists()
    l,d=read(LEDGER),read(PACKET);f=l['contextual_story_natural_dialogue_pass_v1871'];ids=list(range(1146,1200))
    assert(f['fresh_pass_records_explicitly_reread'],f['fresh_pass_records_integrated'],f['fresh_pass_records_pending_native_actual_release'])==(1236,1236,0)
    assert d['selected_IDs']==ids and len(d['records'])==54
    previous={r['message_id']:r for p in OLD for r in read(p)['records']};assert set(previous)==set(ids)
    for r in d['records']:
        p=previous[r['message_ID']];assert r['source_hex']==p['source_hex']and bytes.fromhex(r['current_hex'])==b' '+p['english'].removesuffix('{PAD}').encode('ascii')
    inv=Path('work/analysis/guild_courier_completion_v2247/remaining_historical_fresh_review_inventory.json');remaining=read(inv)
    assert remaining['remaining']==907 and Counter(r['file_path']for r in remaining['records'])=={'/COMMON/MESFILE.DK4':906,'/data/SC2.DK4':1}
    keys={(r['file_path'],r['id'])for r in f['record_keys']};assert not keys&{('/COMMON/MESFILE.DK4',f'COMMON_MESSAGE_{n}')for n in ids}
    assert sha(Path(d['current_ROM']).read_bytes())==d['current_ROM_sha256']==l['current_integrated_candidate']['sha256']
    manifest=read(Path(d['current_ROM']).with_suffix('.manifest.json'));configs=[]
    for stage,selected in [('palace_editorial',range(1146,1177)),('inn_editorial',range(1177,1200))]:
        s=manifest['relocations']['/COMMON/MESFILE.DK4'][stage];p=Path(s['release_config']);assert sha(p.read_bytes())==s['release_config_sha256']and set(s['proof']['changed_records'])=={f'COMMON_MESSAGE_{n}'for n in selected};configs.append(p)
    docs=[Path('docs')/p for p in('editorial_handoff_current.md','translation_progress.md','editorial_review_goal.md','todo.md','known_issues.md')]
    ROOT.mkdir(parents=True)
    for p in[LEDGER,*docs]:(ROOT/(p.name+'.before')).write_bytes(p.read_bytes())
    paths=[PACKET,*OLD,*configs,inv,Path('work/analysis/guild_courier_completion_v2247/completion_receipt.json'),Path('scripts/context_palace_v795.py'),Path('scripts/context_inn_v801.py'),Path('translations/palace_menu_labels_manuscript_v1.json'),Path('translations/inn_time_phrases_manuscript_v2.json'),Path(__file__)]
    evidence={str(p):sha(p.read_bytes())for p in paths};proof=ROOT/'next54_preflight.json'
    save(proof,dict(summary=SUMMARY,next_IDs=ids,packet=str(PACKET),packet_sha256=sha(PACKET.read_bytes()),all54_source_and_complete_current_paragraphs_match=True,all54_fresh_whole_context_prose_native_reconciliation_pending=True,no_source_prose_reread_or_completion_credit=True,current_fresh_count=1236,remaining_historical_count=907,evidence=evidence,full_goal_complete=False))
    l['next_guild_courier_contextual_source_packet_v2234']['resolved_in_v2247']='translations/guild_courier_contextual_final_review_v1.json'
    l['next_palace_inn_contextual_source_packet_v2249']=dict(path=str(PACKET),sha256=sha(PACKET.read_bytes()),preflight=str(proof),preflight_sha256=sha(proof.read_bytes()),IDs=ids,source_prose_or_fresh_credit=0)
    l['latest_checkpoint']=SUMMARY;save(LEDGER,l)
    section='## V2249: Next Palace31 and Inn23 source packet; zero new credit\n\n'+SUMMARY+'\n\nExact source/current packet: '+PACKET.as_posix()+'. Preflight: '+proof.as_posix()+'. Latest completed individual review: translations/guild_courier_contextual_final_review_v1.json. Read source and complete native consumer exchanges afresh; previous notes and technical checks are context, not automatic fresh completion. Current parser: dk4tool.patch.town_trade_port_contextual_reference_v1.current_entries.\n\n'
    text=docs[0].read_text();assert text.startswith('# Current editorial handoff - V2247');first,rest=text.split('\n',1);docs[0].write_text('# Current editorial handoff - V2249\n\n'+section+rest,newline='\n')
    for p in docs[1:]:
        first,rest=p.read_text().split('\n',1);p.write_text(first+'\n\n'+section+rest,newline='\n')
    save(ROOT/'handoff_receipt.json',dict(checkpoint='V2249',classification='progress',fresh_integrated=1236,latest_completed_batch_records=79,next_source_packet_records=54,new_credit_for_packet=0,remaining_historical_fresh_reviews=907,candidate_sha256=d['current_ROM_sha256'],evidence=evidence,updated_files={str(p):sha(p.read_bytes())for p in[LEDGER,*docs,proof]},all_jobs_terminal=True,full_goal_complete=False))
    print(dict(checkpoint='V2249',fresh_integrated=1236,next_source_records=54,new_credit=0,full_goal_complete=False))
