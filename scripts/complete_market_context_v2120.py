"""Reconcile seventeen historical market entries after fresh contextual/native/actual checks."""
from pathlib import Path
from copy import deepcopy
from shutil import copy2
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.primary_town_services_reference_v2 import current_entries
from dk4tool.script.common_message_table import common_message_entries
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.rom.nds import NdsImage
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/market_context_completion_v2120')
LEDGER=Path('translations/editorial_review_current_v1.json')
HANDOFF=Path('docs/editorial_handoff_current.md')
DOC=Path('translations/market_contextual_editorial_manuscript_v1.json')
NOTES=Path('translations/market_contextual_editorial_manuscript_v2.json')
FINAL=Path('translations/market_contextual_final_review_v1.json')
PAGES=Path('work/analysis/market_context_pages_v2115/all18_market_native_pages.json')
LOOP=Path('work/analysis/market_context_page_loop_v2117/original_native_interpage_request_and_continuation_contract.json')
ACTUAL=Path('work/analysis/market_context_actual_verification_v2118/ordinary_market_actual_verification.json')
VISUAL=Path('work/analysis/market_context_visual_v2116/all_native_pages_index.json')
RUN=Path('work/analysis/market_context_actual_v2112')
CAP=Path('E:/Rota Nova translations/Generated/work/emulation_v193/market_context_live_v2112_V2097')
GUIDE=Path('E:/Rota Nova translations/Guide screenshots/V2097 Market contextual retentions verified')
IDS=set(range(745,765))-{750,751,752}
FAMILY='Market-functional-exchanges17'
SUMMARY='V2120 reconciles17 historical Market entries745-764 excluding750-752 as fresh, individually justified wording retentions. Review covers the investment offer/amount/thanks/cancellation/funds-refusal graph, trade capacity/funds warnings, seven alternative extra-stock adviser voices, facility-specific contract refusal and paid-information refusal. Source facts, uncertainty, register and original runtime facility substitution are preserved. No English, ROM, release profile or patch changes were needed. Eighteen native template/argument cases pass19 complete228x48 pages at16pixel row advance, including the two-page762 no-share prompt. Its final page contains the complete amount question; retain the faithful exchange rather than cutting it to one panel. Six clean-exact continuation-control cases preserve the original next-text pointer, termination and mode5 cancellation; UI54E44/bitmapD3718 remain explicit unexecuted ABI boundaries in that offline proof. Ordinary48500frame cold boot reaches actual763,746,747,748,764, complete amount-entry/cancel/positive-investment/low-funds/paid-map-price/refusal/return transitions, and Seoul market information. Allfive full foreground holds match native and independent planes,12 native state controls validate ordinary transactions, andfive whole-frame replay-prefix controls match the verifiedV2097 run. Existing isolated system unlock is declared andnotearned; no savestate/story/location/RNG/funds/outcome fixture. Every other conditional visit isoffline,notclaimedactual. The original donor/core are unchanged andobserver slots restored. Historical2143 completions and2259 source/prose reviews stay unchanged; fresh757 reread757 integrated/reconciled0pending,1386 otherhistorical completions stillneedfresh reconciliation,116COMMON incomplete. Three750-752 remainunmapped anduncompleted;finite constant census isnot proof ofunused text. Everyremaining storyline/shared shop/town/random/playerprose,separategraphics/all18plaques,SC3B109classification andlater older-record technical re-audit stayopen. RegisteredV2097 ROM/exactclean-inputpatch remaincurrent,V1492promoted,allROMs/earliertranslations preserved,fullgoalactive.'
if __name__=='__main__':
 assert not ROOT.exists() and not NOTES.exists() and not FINAL.exists() and not GUIDE.exists()
 ledger=read(LEDGER);f=ledger['contextual_story_natural_dialogue_pass_v1871'];doc=read(DOC);pages=read(PAGES);actual=read(ACTUAL);visual=read(VISUAL);loop=read(LOOP)
 assert ledger['records_editorially_completed']==2143 and ledger['records_reviewed']==2259 if 'records_reviewed'in ledger else ledger['records_editorially_completed']==2143
 assert f['fresh_pass_records_explicitly_reread']==f['fresh_pass_records_integrated']==740 and f['fresh_pass_records_pending_native_actual_release']==0
 assert len(doc['records'])==17 and {r['message_id']for r in doc['records']}==IDS
 assert pages['native_cases']==18 and pages['total_pages']==19 and pages['multi_page_cases']==1 and len(loop['cases'])==6
 assert len(actual['actual_holds'])==5 and {r['message_ID']for r in actual['actual_holds']}=={746,747,748,763,764} and actual['frames']==48500 and len(actual['native_state_controls'])==12 and len(actual['ordinary_prefix_controls'])==5
 assert visual['pages']==19 and len(visual['sheets'])==2
 candidate=ledger['current_integrated_candidate'];rompath=Path(candidate['path']);patchpath=Path(candidate['patch']);digest=sha(rompath.read_bytes())
 assert digest==candidate['sha256']==doc['current_ROM_sha256']==actual['candidate_sha256'] and sha(patchpath.read_bytes())==candidate['patch_sha256']
 rom=NdsImage.open(rompath);arm=rom.read_file('/__arm9__.bin');common=rom.read_file('/COMMON/MESFILE.DK4');entries=current_entries(common,arm)
 clean=NdsImage.open('work/clean.nds');source=common_message_entries(clean.read_file('/COMMON/MESFILE.DK4'),clean.read_file('/__arm9__.bin'))
 assert sha(arm)==candidate['ARM9_sha256']==pages['ARM9_sha256'] and sha(common)==candidate['MESFILE_sha256']==pages['COMMON_sha256']
 historical={}
 for family in ledger['completed_editorial_families']:
  for r in family.get('records',[]):
   if r.get('file_path','/COMMON/MESFILE.DK4')=='/COMMON/MESFILE.DK4' and r.get('message_id')in IDS:
    assert r['message_id']not in historical;historical[r['message_id']]=family['id']
 assert set(historical)==IDS
 keys={(r['file_path'],r['id'])for r in f['record_keys']};assert len(keys)==740 and not keys&{('/COMMON/MESFILE.DK4',f'COMMON_MESSAGE_{n}')for n in IDS}
 for r in doc['records']:
  n=r['message_id'];assert source[n].text.hex()==r['source_hex'] and entries[n].text.hex()==r['current_hex']
  assert ' '.join(r['english'].removesuffix('{PAD}').split())==' '.join(entries[n].text.decode('cp932').split())
  assert source[n].text.count(b'%s')==entries[n].text.count(b'%s')==(1 if n==761 else 0)
  assert r['fresh_retained_wording_justification'] and r['editorial_decision']=='retain-wording'
 ROOT.mkdir(parents=True)
 docs=[HANDOFF,Path('docs/translation_progress.md'),Path('docs/editorial_review_goal.md'),Path('docs/todo.md'),Path('docs/known_issues.md')]
 for p in [LEDGER,*docs]:(ROOT/(p.name+'.before')).write_bytes(p.read_bytes())
 notes=deepcopy(doc);notes.update(status='fresh-contextual-retentions-complete-reconciled-in-existing-registered-V2097',final_native_pages=str(PAGES),final_actual_verification=str(ACTUAL),original_page_loop=str(LOOP),no_ROM_or_registered_release_change=True)
 for r in notes['records']:
  r['status']='complete-fresh-source-context-retention-native-formatting-representative-actual-existing-registered-release';r['formatting_gate_scope']='228x48 native paper;16pixel row advance;full ordered glyphs,complete consumed input,bounds andpagination checked. Actual representative holds are listed individually.'
  r['actual_gameplay_visited']=r['message_id']in{746,747,748,763,764};r['original_historical_family']=historical[r['message_id']]
  r['native_display_evidence']=dict(native_pages=str(PAGES),actual_representative=str(ACTUAL),original_page_loop=str(LOOP))
  if r['message_id']==762:r['pagination_retention_reason']='The no-share investment offer fills three native rows and continues with the complete standalone amount question onpage2. Both pages start with visible text, consume all bytes in order andpreserve the logical explanation-to-question progression. This is offline continuation evidence; no actual zero-share762 visit is claimed.'
 validate_natural_dialogue_batch(notes);save(NOTES,notes)
 proofpaths=[DOC,NOTES,PAGES,LOOP,ACTUAL,VISUAL,RUN/'run_plan.json',RUN/'terminal.json',CAP/'capture_report.json',CAP/'common_observer/requests.json',CAP/'navigation_command_journal.json',Path('work/analysis/market_context_review_v2114b/original_market_decision_graph_current.json'),Path('work/analysis/market_unresolved_context_v2113/clean_native_constant_census.json'),Path('work/analysis/town_services_release_v2099/registered_release_verification.json'),Path('work/analysis/town_services_completion_v2107b/registered_display_verification_addendum.json'),Path('work/analysis/town_services_copies_v2093/all_native_copies_and_prefix_cache_sequence.json'),Path(candidate['manifest']),Path(__file__)]
 evidence={str(p):sha(p.read_bytes())for p in proofpaths}
 save(ROOT/'visual_review.json',dict(all19_native_pages_on_two_sheets_viewed=True,allfive_actual_holds_sheet_viewed=True,actual_map_Seoul_price_and_amount_entry_and_return_frames_viewed=True,full_glyphs_no_clipping_or_missing_leading_trailing_letters_seen=True,two_page762_final_question_retained_with_source_context_reason=True,actual_zero_share762_not_claimed=True,actual48500frame_terminal_observer_closed=True,full_goal_complete=False))
 evidence[str(ROOT/'visual_review.json')]=sha((ROOT/'visual_review.json').read_bytes())
 save(FINAL,dict(format='dk4-editorial-family-final-review-v1',family=FAMILY,file_path='/COMMON/MESFILE.DK4',native_message_IDs=sorted(IDS),revised_count=0,retained_count=17,historical_reconciliation_only=True,new_completed_records=0,records=notes['records'],summary=SUMMARY,evidence=evidence,candidate=str(rompath),candidate_sha256=digest,patch=str(patchpath),patch_sha256=candidate['patch_sha256'],no_ROM_English_or_registered_release_change=True,existing_exact_clean_input_reconstruction_reused_without_repeating_unchanged_build=True,actual_scope=dict(native_IDs=[763,746,747,748,764],complete_foreground_holds=5,executed_frames=48500,ordinary_transactions_and_Seoul_price_screen_and_return=True,native_state_controls=12,whole_prefix_frame_controls=5,existing_isolated_unlock_not_earned=True,other_conditional_lines_offline=True,no_actual_zero_share762_or_all17_individual_visit_or_hardware_claim=True),offline_scope=dict(native_template_argument_cases=18,complete_pages=19,original_continuation_cases=6,explicit_unexecuted_UI_bitmap_ABI_boundaries=True),unresolved_IDs=[750,751,752],full_goal_complete=False))
 f['record_IDs'] += [r['id']for r in notes['records']];f['record_keys'] += [dict(file_path='/COMMON/MESFILE.DK4',id=r['id'])for r in notes['records']]
 f.update(fresh_pass_records_explicitly_reread=757,fresh_pass_records_integrated=757,fresh_pass_records_pending_native_actual_release=0,historical_completed_records_outside_reconciled_fresh_pass=1386,latest_contextual_manuscript=str(NOTES),latest_contextual_retention_review=str(FINAL),latest_completed_family=FAMILY,latest_reconciled_historical_family=FAMILY,latest_final_review=str(FINAL),coverage_note='All757 file-qualified explicitly reread records integrated/reconciled. Other1386 historical completions stillrequire fresh contextual reconciliation;116COMMON incomplete andallremaining source stayin scope.')
 f['reconciled_families'].append(dict(id=FAMILY,records=17,final_review=str(FINAL),new_revisions=0,justified_retentions=17,historical_reconciliation_only=True,new_completed_records=0,all_source_native_representative_actual_and_registered_checks_complete=True))
 ledger['active_source_prose_drafts']['note']='Fresh757 integrated/reconciled throughV2120. Continue116COMMON incomplete,1386historical fresh reconciliations,andallremaining routes/shared town/random/playerprose. Three750-752 remainunmapped;thefinite clean-unit census isnot anunused-text finding.'
 ledger['market_context_v2120']=dict(final_review=str(FINAL),summary=SUMMARY,evidence=evidence,goal_turn_classification='progress',fresh_retention_reconciliations=17,new_historical_completions=0,full_goal_complete=False)
 ledger['latest_checkpoint']=SUMMARY
 ledger['formatting_watchlist']['market_context_v2120']=dict(status='fresh17-complete-at-actual228x48-paper-16pixel-row-step',native_proof=str(PAGES),actual_proof=str(ACTUAL),two_page762_question_retention_reason=next(r for r in notes['records']if r['message_id']==762)['pagination_retention_reason'],no_generalization_to_other_consumers_or_all_conditional_visits=True)
 ledger['next_market_context_packet_v2109']['reconciled_native_IDs_at_V2120']=sorted(IDS);ledger['next_market_context_packet_v2109']['remaining_unreconciled_in_packet']=sorted(set(range(656,765))-IDS)
 assert len({(r['file_path'],r['id'])for r in f['record_keys']})==len(f['record_keys'])==757
 assert ledger['records_editorially_completed']==2143==sum(len(g.get('records',[]))for g in ledger['completed_editorial_families']) and sum(ledger['source_prose_reviewed_counts_by_file'].values())==2259 and len(ledger['reviewed_but_incomplete_COMMON_IDs'])==116 and ledger['goal_status']=='active' and not ledger['full_goal_complete']
 save(LEDGER,ledger)
 section='## Market functional exchanges17 reconciled - V2120\n\n'+SUMMARY+'\n\n- Final source/current references andindividual reasons: `'+FINAL.as_posix()+'`. Notes-only manuscriptv2 retains identical English.\n- Native18cases/19pages: `'+PAGES.as_posix()+'`;actual5holds/12statecontrols: `'+ACTUAL.as_posix()+'`;original pagecontrol: `'+LOOP.as_posix()+'`. Both native contact sheets andthefive actual holds wereviewed.\n- Actual observer accepts body-pointer offsets0/2 andreads thecomplete basebuffer;theprefix2alignment primer isnot mistaken forthemessage body.\n- Broad code comparison permits onlythe registered Investment title pointer020BCA3C relocation fromV758;allother selectedsource spans areclean-exact and11decision fragments pass.\n- Restart/annoyance750/751/752: `work/analysis/market_unresolved_context_v2113/clean_native_constant_census.json`;nocaller established,nounused claim. Continue their indirect caller/script investigation alongside Square656-744 andthefull remaining inventory.\n- Current ROM/patch remainV2097 withthe exact hashes below;no newbuild wasneeded forwording retentions. Alljobs terminal.\n\n'
 handoff=HANDOFF.read_text();assert handoff.startswith('# Current editorial handoff - V2109')
 handoff=handoff.replace('# Current editorial handoff - V2109','# Current editorial handoff - V2120',1).replace('- Fresh contextual pass: **740 reread,740 integrated/reconciled,0pending.** Other1403 historical completions stillrequire fresh contextual reconciliation.','- Fresh contextual pass: **757 reread,757 integrated/reconciled,0pending.** Other1386 historical completions stillrequire fresh contextual reconciliation.',1)
 marker='## Primary town services84 complete - V2107b';assert marker in handoff;handoff=handoff.replace(marker,section+marker,1);HANDOFF.write_text(handoff,newline='\n')
 for p in docs[1:]:
  text=p.read_text();first,rest=text.split('\n',1);short='\n\n## V2120: seventeen Market contextual retentions reconciled\n\n'+SUMMARY+'\n\nSee `docs/editorial_handoff_current.md` and `translations/market_contextual_final_review_v1.json` for exact references andactual/offline scope.\n'
  p.write_text(first+short+rest,newline='\n')
 GUIDE.mkdir(parents=True);guide=[]
 images=[(Path(r['capture']),f'actual_ID{r["message_ID"]}.png','actual-gameplay')for r in actual['actual_holds']]+[(Path(actual['review_sheet']),'actual_five_holds.png','actual-gameplay')]+[(Path(r['path']),f'native_pages_{i:02d}.png','offline-native-pages')for i,r in enumerate(visual['sheets'])]+[(CAP/'frame_045300_navigation.png','actual_Seoul_200_gold_quote.png','actual-map-selection'),(CAP/'frame_045700_navigation.png','actual_Seoul_market_information.png','actual-paid-price-screen'),(CAP/'frame_048500_navigation.png','actual_return_to_town_services.png','actual-gameplay-transition')]
 for p,name,kind in images:dest=GUIDE/name;copy2(p,dest);assert sha(dest.read_bytes())==sha(p.read_bytes());guide.append(dict(path=str(dest),sha256=sha(dest.read_bytes()),kind=kind))
 save(GUIDE/'scope.json',dict(candidate=str(rompath),candidate_sha256=digest,final_review=str(FINAL),images=guide,full_goal_complete=False,actual_and_offline_labels_distinct=True))
 save(ROOT/'completion_receipt.json',dict(checkpoint='V2120',fresh_retention_reconciliations=17,fresh_integrated=757,historical_complete=2143,source_prose_reviewed=2259,COMMON_incomplete=116,other_historical_fresh_reconciliations=1386,unresolved_IDs=[750,751,752],candidate_sha256=digest,patch_sha256=candidate['patch_sha256'],guide=str(GUIDE),guide_images=len(guide),evidence=evidence,updated_files={str(p):sha(p.read_bytes())for p in[LEDGER,*docs,NOTES,FINAL]},goal_turn_classification='progress',full_goal_complete=False))
 print(dict(checkpoint='V2120',fresh_integrated=757,retentions_reconciled=17,historical_unchanged=2143,COMMON_incomplete=116,guide_images=len(guide),ROM_changed=False,full_goal_complete=False))
