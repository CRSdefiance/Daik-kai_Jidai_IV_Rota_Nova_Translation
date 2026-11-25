"""Checkpoint measured early-town consumers without adding completion credit."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/town_services_checkpoint_v2066')
DOC=Path('translations/primary_town_services_contextual_editorial_manuscript_v3.json')
LEDGER=Path('translations/editorial_review_current_v1.json')
HANDOFF=Path('docs/editorial_handoff_current.md')
DISPLAY=Path('work/analysis/town_services_consumer_audit_v2064b/actual_eight_consumers_four12pixel_rows_and_numeric_scope.json')
VOICES=Path('work/analysis/town_services_voice_tables_v2063/nine_clean_exact_voice_tables_and_all_native_catalog_selections.json')
SELECTOR=Path('work/analysis/town_services_selector_v2061/early_numeric_parent_dispatch_contract.json')
if __name__=='__main__':
 assert not ROOT.exists();doc,ledger,display,voices,selector=map(read,(DOC,LEDGER,DISPLAY,VOICES,SELECTOR))
 assert len(doc['records'])==84 and all(not r['review']['formatting']for r in doc['records'])
 assert [r['english']for r in doc['records']]==[r['english']for r in read('translations/primary_town_services_contextual_editorial_manuscript_v1.json')['records']]
 f=ledger['contextual_story_natural_dialogue_pass_v1871'];assert(f['fresh_pass_records_explicitly_reread'],f['fresh_pass_records_integrated'],f['fresh_pass_records_pending_native_actual_release'])==(740,656,84)
 assert(ledger['records_editorially_completed'],ledger['records_revised_and_integrated'],ledger['retained_wordings_editorially_completed'],ledger['records_with_source_and_prose_pass'])==(2059,1456,603,2259)
 assert len(display['actual_font_rows'])==8 and len(display['whole_town_RGB_pairs'])==20 and len(display['font_control_capacity_cases'])==16
 assert len(selector['cases'])==172 and voices['native_selector_calls']==1863 and voices['native_voice_calls']==1863
 assert read('work/analysis/town_services_font_actual_v2060/terminal.json')['terminal']
 candidate=ledger['current_integrated_candidate'];manifest=read(candidate['manifest'])
 assert sha(Path(candidate['path']).read_bytes())==candidate['sha256']==display['candidate_sha256']
 assert manifest['release_stack_sha256']==sha(Path('translations/release_stack.json').read_bytes())
 ROOT.mkdir(parents=True)
 for path in(LEDGER,HANDOFF,Path('docs/translation_progress.md'),Path('docs/editorial_review_goal.md'),Path('docs/todo.md'),Path('docs/known_issues.md')):(ROOT/(path.name+'.before')).write_bytes(path.read_bytes())
 evidence={str(p):sha(p.read_bytes())for p in(DOC,DISPLAY,VOICES,SELECTOR,Path('work/analysis/town_services_refinement_v2065/refinement_receipt.json'),Path('work/analysis/town_services_roles_v2056b/active_eight_requests_and_tribute_payment_direction.json'),Path('work/analysis/town_services_literals_v2055/all84_original_printf_shared_expander_and_literal_guards.json'))}
 summary=('All84 primary town-service prose decisions remain42 revisions42 justified retentions. Notes-only manuscriptv3 preserves allEnglish bodies,clean/current references anddecisions;resolves stale tribute-direction notes andrecords native voice/display evidence. '
 'Ordinary currentV2047 coldboot38500frames withreadonly original COMMON/font hooks binds8 actual IDs49,8,51,53,55,56,59,61. All8 body font contexts are228x48 with6x12 font and12pixel rowstep. All20 distinct post-opening town screenshots match prior whole256x384RGB;the report has21rows because the final38500 frame islisted twice. Existing isolated systemunlock isnotearned;no savestate/story/location/RNG/funds/outcome fixture. Allhost slots/corebytes restored andalljobs terminal. '
 'Sixteen original-font-control cases across4alignments andbothfirst-row parities verify four12pixel rows at0/12/24/36;the fifth row returns unconsumed. These CPU cases deliberately return atthe glyph-paint boundary:they prove control/capacity,not full native ink/shadow pixels orrevised pagination. Unmodified native request/font clones stop atunsupported SDK/graphics memory;preserved2059/2059b/2062 attempts confer no approval. '
 'All9 clean-exact voice tables cover61 IDs;1863 nativevoice plus1863 nativeselection calls preserve every8voice alternative andminus1 fallback,with full4MiB andABI exact. These are catalog queries,not actualconditional visits oractor-placement claims. Remaining23 IDs aredirect selections;allnativeconsumer paths stillneed correctproduction routing. '
 'Current numeric gate172cases proves0..84 excluded underdirect/Yes-No parents;two knownselected controls pass. Monthly tribute76..82 hasaseparate table path. Reuse mature postmacro formatting onlyafter source-bound numeric/table routing andthe measured228x48/6x12 geometry areverified;do not prewrap literal I before macro expansion orassume228x64/16pixel rows. '
 'All84 formatting/cache/revised-gameplay/release gates remainopen. Source/prose2259,fresh740reread/656integrated/84pending,historical2059=1456revised603retained,200COMMON incomplete and1403 historical freshreconciliations unchanged. V2047 stays489batches114layers with exactclean-input patch;no ROM/profile/registry mutation. Approved-name ledger nowexplicitly includes Hodram withRafael,Joakim,Maria,Camille peruserrequest. Everyremaining storyline/shared shop/town/random/playerprose,separategraphics/all18plaques,SC3B109 classification andlater older-record technical re-audit stayopen. Preserve allROMs/translations;V1492 promoted,canonicalunchanged,fullgoalactive.')
 if 'Hodram'not in ledger['approved_names']:ledger['approved_names'].insert(1,'Hodram')
 active=ledger['active_source_prose_drafts'];active['manuscripts'].append(str(DOC))
 active['manuscript_record_subsets_pending']['translations\\primary_town_services_contextual_editorial_manuscript_v2.json']=[]
 active['manuscript_record_subsets_pending'][str(DOC)]=[r['message_id']for r in doc['records']]
 f['latest_contextual_manuscript']=str(DOC)
 family=next(r for r in f['pending_contextual_families']if r['id']=='Primary-town-services84');family.update(manuscript=str(DOC),evidence=evidence,measured_current_body_paper=[228,48],measured_current_font=[6,12])
 ledger['primary_town_services_contextual_v2058']['superseded_notes_and_display_checkpoint']='V2066'
 ledger['primary_town_services_v2066']=dict(summary=summary,manuscript=str(DOC),records=doc['records'],evidence=evidence,formatting_complete=False,goal_turn_classification='progress',full_goal_complete=False)
 ledger['formatting_watchlist']['primary_town_consumer_v2066']=dict(proof=str(DISPLAY),numeric_selector_proof=str(SELECTOR),voice_table_proof=str(VOICES),actual_current_IDs=[r['native_ID']for r in display['actual_font_rows']],paper=[228,48],font=[6,12],native_row_step=12,four_row_capacity_with_glyph_paint_boundary_only=True,revised_full_native_planes_and_pagination_still_pending=True)
 ledger['latest_checkpoint']='V2066 '+summary
 assert len(f['record_keys'])==len({(r['file_path'],r['id'])for r in f['record_keys']})==740
 assert sum(ledger['source_prose_reviewed_counts_by_file'].values())==2259 and len(ledger['reviewed_but_incomplete_COMMON_IDs'])==200
 assert ledger['goal_status']=='active'and not ledger['full_goal_complete'];save(LEDGER,ledger)
 h=HANDOFF.read_text(encoding='utf-8').replace('# Current editorial handoff - V2058','# Current editorial handoff - V2066',1)
 marker='## Primary town-services84 source/prose and native-role checkpoint - V2058';assert marker in h
 section='## Primary town-services84 measured consumer checkpoint - V2066\n\n'+summary+'\n\n'
 section+='- Current draft: `'+str(DOC)+'`;all84 formatting gates false;English unchanged fromv1. Native-role/payment proof2056b and488printf+488macro proof2055 remainvalid. Historicalsource packet2051 andnotesv1/v2 frozen.\n'
 section+='- Actual/geometry audit: `'+str(DISPLAY)+'`;8source-bound body contexts,20distinct RGBpairs,16nativecontrol capacity cases. Capacity uses explicit glyph-paint return boundaries;full revisednative pixel planes stillpending. Originalfont snapshots andallfour memory/CPU exports: `E:/Rota Nova translations/Generated/work/emulation_v193/town_services_font_actual_v2060_V2047/common_observer`. Job18219terminalexit0.\n'
 section+='- Voice tables: `'+str(VOICES)+'`;61IDs/9tables plus23directIDs. Tables:02117460crewassignment,021174A0repair,021189C0monthlytribute,02118A00docking,02118A20food,02118A40supplies,02118A60crowd,02118A80barter,02118AA0terms. All8nativevoices andminus1fallback verified oncatalogqueries;no actualconditionalvisit claim. Literal-pool references retained;bindthe exactoriginalparents before extendingruntime selection.\n'
 section+='- Numeric gate: `'+str(SELECTOR)+'`;172cases. Both02054014direct/02053FCCYes-No exclude0..84;monthly76..82 isdistinct tableparent. No productionruntime changed.\n'
 section+='- Preserved attempts:2056invalidkeyword→2056b;2059bankedSPorder→2059b SDK/graphics stoppingpoints;2062fullfontclonesunmapped→2062bexplicitglyphboundaries;2064countedduplicatefinalcapture→2064b20distinctframes. No failed gate waived andno prose changed toobtainpassingresearch.\n'
 section+='- Next: source-bound numeric/table route extension usingexistingpostmacro rules,all84fullnativeplanes atmeasuredgeometry withtypedsubstitutions andleading/trailing ink/wholewords/bounds/pagination;single8KiB guardedrepack/all3668copies/opaque1484prefix/carrier1931;representative revisedtowntransitions;registered cumulativeROM/exactclean-inputpatch. KeepallROMs;no need torepeat completedMaria/Hodram/Rafael/Stockholm orV2047release checks. Fullobjectiveactive.\n\n'
 HANDOFF.write_text(h.replace(marker,section+marker,1),encoding='utf-8',newline='\n')
 for name in('editorial_review_goal.md','translation_progress.md','todo.md','known_issues.md'):
  with(Path('docs')/name).open('a',encoding='utf-8',newline='\n')as out:out.write('\n\n## V2066 Primary town-services measured consumers\n\n'+summary+'\n')
 Path('docs/primary_town_services_v2066_checkpoint.md').write_text('# Primary town-services consumer checkpointV2066\n\n'+section,encoding='utf-8',newline='\n')
 save(ROOT/'checkpoint_receipt.json',dict(summary=summary,evidence=evidence,ledger_sha256=sha(LEDGER.read_bytes()),handoff_sha256=sha(HANDOFF.read_bytes()),new_source_prose_credit=0,new_completion_credit=0,source_prose=2259,historical_completed=2059,fresh_reread=740,fresh_integrated=656,fresh_pending=84,registered_candidate_unchanged=True,all_ROMs_and_translations_preserved=True,all_jobs_terminal=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
 print(dict(checkpoint='V2066',source_prose=2259,fresh_reread=740,integrated=656,pending=84,complete=2059,all_jobs_terminal=True))
