"""Audited next79 exact source/current entries, without premature review credit."""
from pathlib import Path
from collections import Counter
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/guild_courier_context_handoff_v2234')
PACKET=Path('work/analysis/guild_courier_context_source_v2233/all79_clean_current_context_catalog.json')
LEDGER=Path('translations/editorial_review_current_v1.json')
OLD=Path('translations/item_diplomacy_editorial_manuscript_v2.json')
SUMMARY=('V2234 preflights the next79 COMMON entries346-348 and1070-1145 with exact clean/current references and immediate neighbors. '
 'These comprise27 Guild item/buy/sell/Purser-bargaining lines,3 courier notices and49 diplomatic drafting/letter lines. All76 item/diplomacy paragraphs match frozen manuscriptv2; all3 courier paragraphs match their exact historical completed-record payloads. '
 'This is an extraction/provenance preflight, adding zero source/prose, fresh reread or completion credit. '
 'V2232 completed50 fresh shared warnings/village/fleet/recruitment/private-barmaid contextual retentions, with857 current native layouts,83 full native fonts on7 viewed sheets, current reused1042 gameplay and explicitly historical eight-scenario evidence. '
 'Fresh coverage1157 reread/1157 integrated-reconciled/0pending; historical2143,source/prose2259 and116 incompleteCOMMON unchanged. Another986 historical completions remain:985COMMON plusSC2B294R73. '
 'All never-reviewed routes/shared town/shop/random/player prose remain in scope. Read the next79 Japanese and actual consumer exchanges afresh, retaining or revising only with individual source/context reasons. '
 'Do not infer courier activation from neighboring Guild IDs, confuse Guild/Purser roles, invent relationships or reuse old technical approval as fresh editorial approval. '
 'Current registered V2171,its492batches/114accepted layers and exact clean-input patch are unchanged. All ROMs/earlier translations preserved;V1492 remains promoted and canonical/clean input unchanged. '
 'Full objective active. Separate graphics/all18 plaques,SC3B109 classification and later older-record technical re-audit remain open. All jobs terminal.')

if __name__=='__main__':
    assert not ROOT.exists();ROOT.mkdir(parents=True)
    l,d,old=read(LEDGER),read(PACKET),read(OLD);f=l['contextual_story_natural_dialogue_pass_v1871']
    assert(f['fresh_pass_records_explicitly_reread'],f['fresh_pass_records_integrated'],f['fresh_pass_records_pending_native_actual_release'])==(1157,1157,0)
    ids=list(range(346,349))+list(range(1070,1146))
    assert d['selected_IDs']==ids and len(d['records'])==79
    previous={r['message_id']:r for r in old['records']};assert set(previous)==set(range(1070,1146))
    for r in d['records']:
        n=r['message_ID'];p=previous[n]if n in previous else r['historical_review']['record']
        assert r['source_hex']==p['source_hex']and bytes.fromhex(r['current_hex'])==b' '+p['english'].removesuffix('{PAD}').encode('ascii')
    inv=Path('work/analysis/shared_context_completion_v2232/remaining_historical_fresh_review_inventory.json');remaining=read(inv)
    assert remaining['remaining']==986 and Counter(r['file_path']for r in remaining['records'])=={'/COMMON/MESFILE.DK4':985,'/data/SC2.DK4':1}
    keys={(r['file_path'],r['id'])for r in f['record_keys']};assert not keys&{('/COMMON/MESFILE.DK4',f'COMMON_MESSAGE_{n}')for n in ids}
    assert sha(Path(d['current_ROM']).read_bytes())==d['current_ROM_sha256']==l['current_integrated_candidate']['sha256']
    manifest=read(Path(d['current_ROM']).with_suffix('.manifest.json'))
    stage=manifest['relocations']['/COMMON/MESFILE.DK4']['item_diplomacy_editorial'];config=Path(stage['release_config'])
    assert sha(config.read_bytes())==stage['release_config_sha256']and set(stage['proof']['changed_records'])=={f'COMMON_MESSAGE_{n}'for n in range(1070,1146)}
    docs=[Path('docs')/p for p in('editorial_handoff_current.md','translation_progress.md','editorial_review_goal.md','todo.md','known_issues.md')]
    for p in[LEDGER,*docs]:(ROOT/(p.name+'.before')).write_bytes(p.read_bytes())
    evidence_paths=[PACKET,OLD,config,inv,Path('work/analysis/shared_context_completion_v2232/completion_receipt.json'),Path('scripts/context_item_diplomacy_v784.py'),Path('scripts/probe_item_diplomacy_layout_v784.py'),Path('scripts/review_item_diplomacy_v784.py'),Path(__file__)]
    evidence={str(p):sha(p.read_bytes())for p in evidence_paths}
    proof=ROOT/'next79_preflight.json'
    save(proof,dict(summary=SUMMARY,next_IDs=ids,packet=str(PACKET),packet_sha256=sha(PACKET.read_bytes()),prior_manuscript=str(OLD),prior_manuscript_sha256=sha(OLD.read_bytes()),all76_item_diplomacy_source_and_current_paragraphs_match=True,all3_courier_source_and_current_paragraphs_match_historical_records=True,all79_fresh_whole_context_prose_native_reconciliation_pending=True,no_source_prose_reread_or_completion_credit=True,current_fresh_count=1157,remaining_historical_count=986,evidence=evidence,full_goal_complete=False))
    l['next_guild_courier_contextual_source_packet_v2234']=dict(path=str(PACKET),sha256=sha(PACKET.read_bytes()),preflight=str(proof),preflight_sha256=sha(proof.read_bytes()),IDs=ids,source_prose_or_fresh_credit=0)
    l['latest_checkpoint']=SUMMARY;save(LEDGER,l)
    section='## V2234: Next Guild/courier/letters79 source packet; zero new credit\n\n'+SUMMARY+'\n\nExact source/current packet: '+PACKET.as_posix()+'. Preflight: '+proof.as_posix()+'. Latest completed individual review: translations/shared_contextual_final_review_v1.json. Read all79 source records and complete caller exchanges afresh; branch roles, actual name/amount providers and courier consumers must be established before contextual approval.\n\n'
    text=docs[0].read_text();assert text.startswith('# Current editorial handoff - V2232')
    text=text.replace('# Current editorial handoff - V2232','# Current editorial handoff - V2234',1)
    first,rest=text.split('\n',1);docs[0].write_text(first+'\n\n'+section+rest,newline='\n')
    for p in docs[1:]:
        first,rest=p.read_text().split('\n',1);p.write_text(first+'\n\n'+section+rest,newline='\n')
    save(ROOT/'handoff_receipt.json',dict(checkpoint='V2234',classification='progress',fresh_integrated=1157,latest_completed_batch_records=50,next_source_packet_records=79,new_credit_for_packet=0,remaining_historical_fresh_reviews=986,candidate_sha256=d['current_ROM_sha256'],evidence=evidence,updated_files={str(p):sha(p.read_bytes())for p in[LEDGER,*docs,proof]},all_jobs_terminal=True,full_goal_complete=False))
    print(dict(checkpoint='V2234',fresh_integrated=1157,next_source_records=79,new_credit=0,full_goal_complete=False),flush=True)
