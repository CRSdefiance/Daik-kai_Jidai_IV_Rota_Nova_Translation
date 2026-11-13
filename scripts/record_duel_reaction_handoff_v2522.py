"""Preserve13 completed escape retentions and prepare16 timed reactions with zero new credit."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/duel_reaction_source_handoff_v2522')
SUMMARY=(
 'V2522 prepares the next16 timed duel reactions1957-1972 with exact clean/current references and two storage neighbors. All16 current paragraphs match registered duel_bark_editorial/manuscriptv2 through duel-bark-v1200. Fresh current code passes416 original voice choices and binds both original1042C D458 calls:side0,duration60,positive table02117560 writes caller result1 and negative table021175C0 writes0. The actual input-mode/controller snapshot remains historical V1189,not a current gameplay activation. Current five-table/numeric-special front and64-byte helper exactly match their registered assembled bytes. These two tables are included now;do not carry forward the old1199 excludes-both-tables note. This registered layer uses dependencies[manuscript] and proof.native_IDs,not newer manuscript_sha256/reviewed_native_IDs keys. The preserved preflight successors finish that schema check without repeating416 completed selections. Extraction/source-context adds zero fresh reread,source/prose or completion credit. '
 'Next review these as independent positive/negative timed-action alternatives within the original duel flow,not successive conversation. Preserve anticipated moves,combat taunts,accuracy boasts,delight,self-reproach,carelessness versus a literal stumble,overconfidence,haste,defiance,evasion and personal lack of fighting confidence. Do not invent supernatural sight,a named weakness,kinship,rank,guaranteed accuracy/victory or a completed result from character speech. Native D458 must keep original side0 for both reaction families;the earlier default side1 for non-challenge static lines is not appropriate. Use the distinct24x3/208x36 static-duel consumer and original three144x12 crops,not shared portrait speech. Current full fonts,source selection/ABI/cache behavior and representative historical timing/input/outcome/transition binding remain required. Historical V1206 evidence:work/analysis/duel_bark_terminal_v1211/terminal_gameplay_verification.json;only1958 and1966 were individually observed. Its actual1973 escape samples are preservation context with no duplicate credit. All special moves1980-1993/2146 remain separate fresh-review work. '
 'This goal turn reconciles13 escape retentions in V2518 and audits them in V2519. Each has a new clean-source gloss,whole defeat-flow reading,retention reason,five gates and exact current integrated reference. Correct direct53F0C/02053F40/table+274 pipelines,416 voice choices,1423 current expansion/font cases,1021 unique native rasters,26 cold/warm copies,162 exact interjection-boundary decisions,two historical complete notice/RGB holds,six corruption controls and four historical defeat/title transitions pass. All19 logical/current-ASCII-Faticia previews and both historical sheets were viewed. The current immutable pool applies8 previously registered fullwidth-F-to-ASCII Faticia bytes only in cloned CPU models;the ROM is unchanged. Both current audited stack bridges and executed instruction bytes are checked rather than relying on stale historical formatter code. No new emulator run or earned progression is claimed. Fresh coverage remains1968 reread /1968 integrated-reconciled /zero pending. Historical completion2143(1498 revised,645 retained),source/prose2259,incomplete COMMON116 and175 remaining historical fresh reviews(174 COMMON plus SC2B294R73) are unchanged. Registered cumulative experimental V2284 remains493 batches/114 accepted layers with its exactly reconstructable clean-input patch. ROM,runtime,geometry,registry,profile,manifest and patch are unchanged. V1492 stays promoted;canonical/clean inputs,all ROMs and earlier translations are preserved. All never-reviewed storylines,shared shop/town dialogue,random scenes and remaining player-facing prose remain in scope. Separate graphics/all18 plaques,SC3B109 classification and later older-record technical re-audit remain open. The full goal is active. All jobs are terminal.'
)
if __name__=='__main__':
 assert not ROOT.exists()
 ledgerpath=Path('translations/editorial_review_current_v1.json');ledger=read(ledgerpath);fresh=ledger['contextual_story_natural_dialogue_pass_v1871']
 assert(fresh['fresh_pass_records_explicitly_reread'],fresh['fresh_pass_records_integrated'],fresh['fresh_pass_records_pending_native_actual_release'])==(1968,1968,0)
 packetpath=Path('work/analysis/duel_reaction_context_source_v2520/all16_clean_current_context_catalog.json')
 contextpath=Path('work/analysis/duel_reaction_context_v2521/source_context_packet.json');preflightpath=Path('work/analysis/duel_reaction_context_v2521/next16_preflight.json')
 packet,context,preflight=map(read,(packetpath,contextpath,preflightpath))
 assert packet['selected_IDs']==list(range(1957,1973))and len(context['all416_unchanged_native_voice_selections'])==416 and len(context['two_original_voice_call_bindings'])==2
 assert preflight['fresh_credit']==0 and preflight['all16_clean_current_registered_compilations_match']and preflight['current_registered_five_table_and_numeric_special_front_and64byte_helper_exact']
 assert sha(packetpath.read_bytes())==preflight['packet_sha256']and sha(contextpath.read_bytes())==preflight['source_context_sha256']
 releasepath=Path('work/analysis/refit_spritsail_release_v2285b/registered_release_verification.json');release=read(releasepath)
 assert sha(Path(ledger['current_integrated_candidate']['path']).read_bytes())==release['candidate_sha256']==packet['current_ROM_sha256']
 assert sha(Path(release['patch']).read_bytes())==release['patch_sha256']and release['whole_ROM_reconstruction_byte_exact']
 docs=[Path('docs')/p for p in('editorial_handoff_current.md','translation_progress.md','editorial_review_goal.md','todo.md','known_issues.md')]
 assert docs[0].read_text().startswith('# Current editorial handoff - V2518')
 ROOT.mkdir(parents=True)
 for p in[ledgerpath,*docs]:(ROOT/(p.name+'.before')).write_bytes(p.read_bytes())
 evidencepaths=[packetpath,contextpath,preflightpath,Path(preflight['registered_config']),Path(preflight['registered_manuscript']),
  Path('work/analysis/escape_completion_v2518/completion_receipt.json'),Path('work/analysis/editorial_handoff_verification_v2519/verified_handoff.json'),
  Path('work/analysis/duel_bark_terminal_v1211/terminal_gameplay_verification.json'),releasepath,
  Path('scripts/prepare_duel_reaction_context_source_v2520.py'),Path('scripts/preflight_duel_reaction_context_v2521.py'),
  Path('scripts/preflight_duel_reaction_context_v2521b.py'),Path('scripts/preflight_duel_reaction_context_v2521c.py'),Path(__file__)]
 evidence={str(p):sha(p.read_bytes())for p in evidencepaths}
 ledger['next_duel_reaction_contextual_source_packet_v2522']=dict(path=str(packetpath),sha256=sha(packetpath.read_bytes()),source_context=str(contextpath),
  source_context_sha256=sha(contextpath.read_bytes()),preflight=str(preflightpath),preflight_sha256=sha(preflightpath.read_bytes()),native_message_IDs=list(range(1957,1973)),
  fresh_credit=0,all_editorial_current_native_historical_and_registered_reconciliation_pending=True)
 ledger['latest_checkpoint']=SUMMARY;ledger['current_integrated_candidate']['details']+=' V2522 prepares16 timed-reaction contexts;zero added editorial credit.'
 ledger['research_checkpoints'].append(dict(id='V2522-next16-timed-duel-context-only',proof=str(preflightpath),source_prose_reviews_added=0,completed_entries_added=0,fresh_pass_credit_added=0,
  goal_turn_classification='progress:13 fresh escape retentions reconciled;next16 timed-action source packet prepared',full_goal_complete=False))
 save(ledgerpath,ledger)
 section='## V2522: Next16 timed duel reaction source packet;zero new credit\n\n'+SUMMARY+'\n\nNext packet: '+packetpath.as_posix()+'. Source context: '+contextpath.as_posix()+'. Preflight: '+preflightpath.as_posix()+'. Latest individual review: translations/escape_contextual_final_review_v1.json. Remaining inventory: work/analysis/escape_completion_v2518/remaining_historical_fresh_review_inventory.json. Current parser: dk4tool.patch.refit_contextual_spritsail_v1.current_entries.\n\n'
 first,rest=docs[0].read_text().split('\n',1);docs[0].write_text('# Current editorial handoff - V2522\n\n'+section+rest,newline='\n')
 for p in docs[1:]:first,rest=p.read_text().split('\n',1);p.write_text(first+'\n\n'+section+rest,newline='\n')
 save(ROOT/'handoff_receipt.json',dict(checkpoint='V2522',summary=SUMMARY,completed_this_goal_turn=13,next_packet_records=16,next_packet_fresh_credit=0,
  fresh_integrated=1968,other_historical_fresh_reviews=175,candidate_sha256=release['candidate_sha256'],patch_sha256=release['patch_sha256'],
  evidence=evidence,updated_files={str(p):sha(p.read_bytes())for p in[ledgerpath,*docs]},all_jobs_terminal=True,goal_turn_classification='progress',full_goal_complete=False))
 print('V2522:13 escape retentions complete;next16 timed-reaction context prepared,zero new credit.1968 integrated;175 historical fresh reviews remain.')
