"""Record the next15 source-bound special calls with zero fresh-review credit."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/duel_special_source_handoff_v2531')
SUMMARY=(
 'V2531 prepares15 original special-move calls1980-1993/2146 with exact clean/current references and four storage neighbors. Fresh current source code executes208 original101EC actor-to-method selections and15 method-specific D4D0 calls,all side0/duration120. CPU controller actor pointers are rebound to original unchanged actor objects;pose/animation bridges are explicit source-test boundaries,not actual animation or current gameplay. The corrected Angelo1988/Fernando1987 literal pairing is retained. Julio2146 is a confirmed nonadjacent special call,not generic town dialogue. Current extended numeric/table front and64-byte helper match registered bytes. All15 current paragraphs match their own registered special compiler/manuscript. This extraction/source-context packet adds zero fresh reread,source/prose or completion credit. '
 'Next review every clean utterance with its source actor,method,animation context and intent. Preserve Samwell\'s two-sword demonstration,Maria\'s playtime taunt,Cristina\'s afterimage call,Yukihisa\'s White Tree Sword Style/Twin Shadow Formation,Gerhard\'s predictable-attack challenge,Camille\'s explicit Gerhard-training comparison,other swordplay taunts,Fernando\'s showman laugh,Angelo\'s teasing boast,Al\'s battlefield-honed swordplay,Hodram\'s finisher,Emilio\'s throw,Yifa\'s Taoist arts and Julio\'s comic alcohol boast. Do not invent a weapon,kinship,rank,spell,deity,guaranteed combat result or real alcohol benefit. The school kanji White Tree is separate from the established katakana Shiraki surname. Native side0/duration120 D4D0 is a distinct numeric entry;do not reuse side1 table defaults or the timed-reaction duration60. Use24x3/208x36 full native fonts and three144x12 source crops,current exact numeric dispatch/loader/cache/ABI bounds and necessary transition checks. Historical evidence:work/analysis/duel_long_terminal_v1245b/terminal_gameplay_verification.json and work/analysis/duel_special_native_v1219b/native_font_scope_verification.json. Only1990 has individual original-special gameplay coverage there;others require honest family-sample scope. Unchanged131324 dispatch and other broad matrices need not be blindly repeated when exact current code and focused paths suffice. '
 'This goal turn reconciles16 timed reactions in V2527 and audits them in V2528. Every record has a fresh clean-source gloss,complete timed-context reading,individual retention reason,five gates and exact current integrated references. Current16 original side0/duration60 full fonts,32 selected/excluded controls,32 cold/warm copies,four historical positive/negative reaction holds,exact accepted/rejected controller schedule,12 corruption controls and four historical defeat/title transitions pass. All16 font previews and both historical sheets were viewed. Later1973 escape samples remain preservation context with no duplicate credit. The preserved pre-write reconciliation adapter failure only concerned the old context\'s current_ROM_sha256 key;its successor reads that field without altering evidence. No new emulator run or earned progression is claimed. Fresh coverage remains1984 reread /1984 integrated-reconciled /zero pending. Historical completion2143(1498 revised,645 retained),source/prose2259,incomplete COMMON116 and159 remaining historical fresh reviews(158 COMMON plus SC2B294R73) are unchanged. Registered cumulative experimental V2284 remains493 batches/114 accepted layers with its exactly reconstructable clean-input patch. ROM,runtime,geometry,registry,profile,manifest and patch are unchanged. V1492 stays promoted;canonical/clean inputs,all ROMs and earlier translations are preserved. All never-reviewed storylines,shared shop/town dialogue,random scenes and remaining player-facing prose remain in scope. Separate graphics/all18 plaques,SC3B109 classification and later older-record technical re-audit remain open. The full goal is active. All jobs are terminal.'
)
if __name__=='__main__':
 assert not ROOT.exists()
 ledgerpath=Path('translations/editorial_review_current_v1.json');ledger=read(ledgerpath);fresh=ledger['contextual_story_natural_dialogue_pass_v1871']
 assert(fresh['fresh_pass_records_explicitly_reread'],fresh['fresh_pass_records_integrated'],fresh['fresh_pass_records_pending_native_actual_release'])==(1984,1984,0)
 packetpath=Path('work/analysis/duel_special_context_source_v2529/all15_clean_current_context_catalog.json')
 contextpath=Path('work/analysis/duel_special_context_v2530/source_context_packet.json');preflightpath=Path('work/analysis/duel_special_context_v2530/next15_preflight.json')
 packet,context,preflight=map(read,(packetpath,contextpath,preflightpath))
 assert packet['selected_IDs']==[*range(1980,1994),2146]and len(context['all208_original_native_special_method_selections'])==208 and len(context['all15_original_message_call_bindings'])==15
 assert preflight['fresh_credit']==0 and preflight['all15_clean_current_registered_compilations_match']and preflight['current_extended_front_and_helper_bytes_exact']
 assert sha(packetpath.read_bytes())==preflight['packet_sha256']and sha(contextpath.read_bytes())==preflight['source_context_sha256']
 releasepath=Path('work/analysis/refit_spritsail_release_v2285b/registered_release_verification.json');release=read(releasepath)
 assert sha(Path(ledger['current_integrated_candidate']['path']).read_bytes())==release['candidate_sha256']==packet['current_ROM_sha256']
 assert sha(Path(release['patch']).read_bytes())==release['patch_sha256']and release['whole_ROM_reconstruction_byte_exact']
 docs=[Path('docs')/p for p in('editorial_handoff_current.md','translation_progress.md','editorial_review_goal.md','todo.md','known_issues.md')]
 assert docs[0].read_text().startswith('# Current editorial handoff - V2527')
 ROOT.mkdir(parents=True)
 for p in[ledgerpath,*docs]:(ROOT/(p.name+'.before')).write_bytes(p.read_bytes())
 evidencepaths=[packetpath,contextpath,preflightpath,Path(preflight['registered_config']),Path(preflight['registered_manuscript']),
  Path('work/analysis/duel_reaction_completion_v2527/completion_receipt.json'),Path('work/analysis/editorial_handoff_verification_v2528/verified_handoff.json'),
  Path('work/analysis/duel_long_terminal_v1245b/terminal_gameplay_verification.json'),releasepath,
  Path('scripts/prepare_duel_special_context_source_v2529.py'),Path('scripts/preflight_duel_special_context_v2530.py'),Path(__file__)]
 evidence={str(p):sha(p.read_bytes())for p in evidencepaths}
 ledger['next_duel_special_contextual_source_packet_v2531']=dict(path=str(packetpath),sha256=sha(packetpath.read_bytes()),source_context=str(contextpath),
  source_context_sha256=sha(contextpath.read_bytes()),preflight=str(preflightpath),preflight_sha256=sha(preflightpath.read_bytes()),native_message_IDs=packet['selected_IDs'],
  fresh_credit=0,all_editorial_current_native_historical_and_registered_reconciliation_pending=True)
 ledger['latest_checkpoint']=SUMMARY;ledger['current_integrated_candidate']['details']+=' V2531 prepares15 special-call contexts;zero added editorial credit.'
 ledger['research_checkpoints'].append(dict(id='V2531-next15-special-call-context-only',proof=str(preflightpath),source_prose_reviews_added=0,completed_entries_added=0,fresh_pass_credit_added=0,
  goal_turn_classification='progress:16 fresh timed reactions reconciled;next15 source special-call packet prepared',full_goal_complete=False))
 save(ledgerpath,ledger)
 section='## V2531: Next15 special-call source packet;zero new credit\n\n'+SUMMARY+'\n\nNext packet: '+packetpath.as_posix()+'. Source context: '+contextpath.as_posix()+'. Preflight: '+preflightpath.as_posix()+'. Latest individual review: translations/duel_reaction_contextual_final_review_v1.json. Remaining inventory: work/analysis/duel_reaction_completion_v2527/remaining_historical_fresh_review_inventory.json. Current parser: dk4tool.patch.refit_contextual_spritsail_v1.current_entries.\n\n'
 first,rest=docs[0].read_text().split('\n',1);docs[0].write_text('# Current editorial handoff - V2531\n\n'+section+rest,newline='\n')
 for p in docs[1:]:first,rest=p.read_text().split('\n',1);p.write_text(first+'\n\n'+section+rest,newline='\n')
 save(ROOT/'handoff_receipt.json',dict(checkpoint='V2531',summary=SUMMARY,completed_this_goal_turn=16,next_packet_records=15,next_packet_fresh_credit=0,
  fresh_integrated=1984,other_historical_fresh_reviews=159,candidate_sha256=release['candidate_sha256'],patch_sha256=release['patch_sha256'],
  evidence=evidence,updated_files={str(p):sha(p.read_bytes())for p in[ledgerpath,*docs]},all_jobs_terminal=True,goal_turn_classification='progress',full_goal_complete=False))
 print('V2531:16 timed reactions complete;next15 special-call context prepared,zero new credit.1984 integrated;159 historical fresh reviews remain.')
