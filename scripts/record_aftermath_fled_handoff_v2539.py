"""Next six report contexts, zero credit; special15 completion remains credited."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/aftermath_fled_source_handoff_v2539')
SUMMARY=(
 'V2539 prepares the next six enemy-flagship-flight/victory reports2046-2051 with exact clean/current references,two storage neighbors,208 original voice selections and three original72368 outcome prefixes. Source mode2 calls53D44 with role1/table02117900;mode0 is flagship capture and mode1 flagship defeat. The eight signed table members are2046,2047,-1,-1,2048,2049,2050,2051. Voice slots2/3 fall back to the first valid2046;there are six alternatives,not eight utterances or sequential replies. The source role1 is unassigned in the preserved snapshot and original fallback selects Charles18/2046. No actor identity,roster,RNG or result is rewritten. These isolated CPU prefixes stop before outcomes and are not current gameplay. All six current paragraphs equal their registered battle_aftermath_editorial compiler/manuscript. This packet adds zero fresh reread,source/prose or completion credit. '
 'Next freshly review each complete report:enemy flagship fleeing and our victory,formal/brisk/excited/older/informal/courteous voice,explicit Admiral addresses2048/2049/2051,and2050\'s enemy-admiral ship and recognition of victory. Do not infer death,capture,sinking,kinship or a new rank. Storage neighbor2045 is a city-defense challenge and2052 a powder-fire report;neither is a preceding/following reply. Use the distinct original228x64 portrait body and original speech role frame53DB8+27C,not the208x36 static duel widget or53F40+274 direct frame. Bind current effective formatter/loader/complete fonts/copies/ABI/bounds and necessary historical dismissal/transition evidence. Historical actual proof:work/analysis/aftermath_victory_verified_v1271/actual_fled_victory_verification.json;only2046 has an individual activation there. Other five use honest family-sample coverage plus current focused tests. Do not repeat completed31 pre-duel fixture audits or broad name matrices without a concrete new risk. '
 'This goal turn reconciles15 actor-specific special calls in V2536 and audits them in V2537. All15 retain their English with fresh individual clean-source glosses,context reasons,five gates and exact integrated references. Fernando1987 review metadata alone changes from full-width Ｆernando to Fernando,with actor20 and prior label preserved. Fifteen original numericD4D0 side0/duration120 full-font cases,six excluded callers,30 cold/warm copies,six historical Hodram1990 holds,six corruption controls and four historical combat/victory/aftermath transitions pass. All current and historical sheets were viewed. No new emulator run or earned progression is claimed. Fresh coverage remains1999 reread /1999 integrated-reconciled /zero pending. Historical completion2143(1498 revised,645 retained),source/prose2259,incomplete COMMON116 and144 remaining historical fresh reviews(143 COMMON plus SC2B294R73) are unchanged. Registered cumulative experimental V2284 remains493 batches/114 accepted layers with its exactly reconstructable clean-input patch. ROM,runtime,geometry,registry,profile,manifest and patch are unchanged. V1492 stays promoted;canonical/clean inputs,all ROMs and earlier translations are preserved. Every never-reviewed storyline,shared shop/town dialogue,random scene and remaining player-facing prose remains in scope. Separate graphics/all18 plaques,SC3B109 classification and later older-record technical re-audit remain open. The full goal is active. All jobs are terminal.'
)
if __name__=='__main__':
 assert not ROOT.exists()
 ledgerpath=Path('translations/editorial_review_current_v1.json');ledger=read(ledgerpath);fresh=ledger['contextual_story_natural_dialogue_pass_v1871']
 assert(fresh['fresh_pass_records_explicitly_reread'],fresh['fresh_pass_records_integrated'],fresh['fresh_pass_records_pending_native_actual_release'])==(1999,1999,0)
 packetpath=Path('work/analysis/aftermath_fled_context_v2538/all6_clean_current_context_catalog.json');contextpath=Path('work/analysis/aftermath_fled_context_v2538/source_context_packet.json');preflightpath=Path('work/analysis/aftermath_fled_context_v2538/next6_preflight.json')
 packet,context,preflight=map(read,(packetpath,contextpath,preflightpath))
 assert packet['selected_IDs']==list(range(2046,2052))and len(context['all208_original_voice_selections'])==208 and len(context['original_three_outcome_prefixes'])==3
 assert preflight['fresh_credit']==0 and preflight['all6_clean_current_registered_compilations_match']
 assert sha(packetpath.read_bytes())==preflight['packet_sha256']and sha(contextpath.read_bytes())==preflight['source_context_sha256']
 raw=Path(context['actual_snapshot']).read_bytes();assert sha(raw)==context['actual_snapshot_sha256']
 rom=NdsImage.open(ledger['current_integrated_candidate']['path']);_,get=get_machine(rom.read_file('/__arm9__.bin'),raw);duty=get(0xCB1A8)+0x2090
 assert get(0x82428,duty,1)==0 and get(0x82478,duty,1)==18
 releasepath=Path('work/analysis/refit_spritsail_release_v2285b/registered_release_verification.json');release=read(releasepath)
 assert sha(Path(ledger['current_integrated_candidate']['path']).read_bytes())==release['candidate_sha256']==packet['current_ROM_sha256']
 assert sha(Path(release['patch']).read_bytes())==release['patch_sha256']and release['whole_ROM_reconstruction_byte_exact']
 docs=[Path('docs')/p for p in('editorial_handoff_current.md','translation_progress.md','editorial_review_goal.md','todo.md','known_issues.md')]
 assert docs[0].read_text().startswith('# Current editorial handoff - V2536')
 ROOT.mkdir(parents=True)
 for p in[ledgerpath,*docs]:(ROOT/(p.name+'.before')).write_bytes(p.read_bytes())
 evidencepaths=[packetpath,contextpath,preflightpath,Path(preflight['registered_config']),Path(preflight['registered_manuscript']),
  Path('work/analysis/duel_special_completion_v2536/completion_receipt.json'),Path('work/analysis/editorial_handoff_verification_v2537/verified_handoff.json'),
  Path(preflight['historical_family_proof']),releasepath,Path('scripts/prepare_aftermath_fled_context_v2538.py'),Path(__file__)]
 evidence={str(p):sha(p.read_bytes())for p in evidencepaths}
 ledger['next_aftermath_fled_contextual_source_packet_v2539']=dict(path=str(packetpath),sha256=sha(packetpath.read_bytes()),source_context=str(contextpath),source_context_sha256=sha(contextpath.read_bytes()),preflight=str(preflightpath),preflight_sha256=sha(preflightpath.read_bytes()),native_message_IDs=packet['selected_IDs'],fresh_credit=0,all_editorial_current_native_historical_and_registered_reconciliation_pending=True)
 ledger['latest_checkpoint']=SUMMARY;ledger['current_integrated_candidate']['details']+=' V2539 prepares6 flee/victory report contexts;zero additional editorial credit.'
 ledger['research_checkpoints'].append(dict(id='V2539-next6-aftermath-fled-context-only',proof=str(preflightpath),source_prose_reviews_added=0,completed_entries_added=0,fresh_pass_credit_added=0,goal_turn_classification='progress:15 fresh special calls reconciled;next6 source aftermath packet prepared',full_goal_complete=False))
 save(ledgerpath,ledger)
 section='## V2539: Next6 aftermath flee/victory contexts;zero new credit\n\n'+SUMMARY+'\n\nNext packet: '+packetpath.as_posix()+'. Source context: '+contextpath.as_posix()+'. Preflight: '+preflightpath.as_posix()+'. Latest individual review: translations/duel_special_contextual_final_review_v1.json. Remaining inventory: work/analysis/duel_special_completion_v2536/remaining_historical_fresh_review_inventory.json. Current parser: dk4tool.patch.refit_contextual_spritsail_v1.current_entries.\n\n'
 first,rest=docs[0].read_text().split('\n',1);docs[0].write_text('# Current editorial handoff - V2539\n\n'+section+rest,newline='\n')
 for p in docs[1:]:first,rest=p.read_text().split('\n',1);p.write_text(first+'\n\n'+section+rest,newline='\n')
 save(ROOT/'handoff_receipt.json',dict(checkpoint='V2539',summary=SUMMARY,completed_this_goal_turn=15,speaker_metadata_corrections=1,next_packet_records=6,next_packet_fresh_credit=0,fresh_integrated=1999,other_historical_fresh_reviews=144,candidate_sha256=release['candidate_sha256'],patch_sha256=release['patch_sha256'],evidence=evidence,updated_files={str(p):sha(p.read_bytes())for p in[ledgerpath,*docs]},all_jobs_terminal=True,goal_turn_classification='progress',full_goal_complete=False))
 print('V2539:15 special calls reconciled;next6 aftermath contexts prepared,zero added credit.1999 integrated;144 historical fresh reviews remain.')
