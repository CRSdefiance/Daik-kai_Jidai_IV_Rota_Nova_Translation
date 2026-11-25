"""Checkpoint native routing/planes research; keep84 drafts and full goal open."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/town_services_checkpoint_v2075')
LEDGER=Path('translations/editorial_review_current_v1.json')
HANDOFF=Path('docs/editorial_handoff_current.md')
DOC=Path('translations/primary_town_services_contextual_editorial_manuscript_v3.json')
PROOFS=[Path('work/analysis/town_services_native_formatter_v2067/all84_explicit_native_formatter_and_228x48_planes.json'),Path('work/analysis/town_services_callers_v2068/nine_source_table_caller_parent_contracts.json'),Path('work/analysis/town_services_current_routes_v2069b/all84_current_macro_route_outputs.json'),Path('work/analysis/town_services_runtime_v2070/runtime_plan.json'),Path('work/analysis/town_services_runtime_predicates_v2071/exact_numeric_and_monthly_predicate_preservation.json'),Path('work/analysis/town_services_research_routes_v2072/research_runtime_all84_original_BL_routes.json'),Path('work/analysis/town_services_routed_fonts_v2073/all117_nonmodal_routed_plane_bindings.json'),Path('work/analysis/town_services_runtime_references_v2074/current_research_reference_and_unowned_path_preservation.json')]
if __name__=='__main__':
 assert not ROOT.exists();ledger,doc=read(LEDGER),read(DOC);fonts,callers,current,plan,predicates,routes,routed,refs=map(read,PROOFS)
 f=ledger['contextual_story_natural_dialogue_pass_v1871'];assert(f['fresh_pass_records_explicitly_reread'],f['fresh_pass_records_integrated'],f['fresh_pass_records_pending_native_actual_release'])==(740,656,84)
 assert(ledger['records_editorially_completed'],ledger['records_revised_and_integrated'],ledger['retained_wordings_editorially_completed'],ledger['records_with_source_and_prose_pass'])==(2059,1456,603,2259)
 assert len(doc['records'])==84 and all(not r['review']['formatting']for r in doc['records'])
 assert len(fonts['cases'])==488 and len(fonts['native_font_planes'])==122 and not fonts['errors']
 assert len(callers['tables'])==9 and sum(len(r['source_callers'])for r in callers['tables'])==13
 assert predicates['total_numeric_cases']==262172 and predicates['total_monthly_cases']==16390
 assert len(routes['cases'])==148 and not routes['errors']and len(routed['cases'])==117 and routed['new_full_native_planes']==10 and routed['exact_formatted_and_unchanged_font_runtime_inherited_planes']==107
 assert len(routed['remaining_modal83_84_cases'])==5 and refs['all_external_references_exact']
 candidate=ledger['current_integrated_candidate'];assert sha(Path(candidate['path']).read_bytes())==candidate['sha256']==doc['current_ROM_sha256']
 manifest=read(candidate['manifest']);assert manifest['release_stack_sha256']==sha(Path('translations/release_stack.json').read_bytes())
 ROOT.mkdir(parents=True)
 for p in(LEDGER,HANDOFF,Path('docs/translation_progress.md'),Path('docs/editorial_review_goal.md'),Path('docs/todo.md'),Path('docs/known_issues.md')):(ROOT/(p.name+'.before')).write_bytes(p.read_bytes())
 evidence={str(p):sha(p.read_bytes())for p in(DOC,*PROOFS,Path('scripts/primary_town_runtime_v2070.py'))}
 sheets=fonts['sheets_for_visual_review']+[routed['changed_plane_review_sheet']]
 assert len(sheets)==8 and all(sha(Path(p['path']).read_bytes())==p['sha256']for p in sheets)
 style=[dict(message_ID=r['message_ID'],supplied_arguments=r['supplied_arguments'],lines=r['lines'],findings=r['style_findings'])for r in routed['cases']if r['style_findings']]
 assert len(style)==20
 save(ROOT/'visual_review.json',dict(sheets=sheets,all_eight_contact_sheets_viewed=True,all_122_prospective_and10_changed_planes_visually_reviewed=True,
  complete_glyphs_ink_shadow_bounds_and_no_blank_paper_faults_in_these_planes=True,style_findings_pending=style,
  modal5_distinct_geometry_gate_and_production_formatting_approval_pending=True,no_waiver_or_prose_change=True,full_goal_complete=False))
 summary=('Primary town-services84 remains42 proposed revisions42 justified retentions,English/manuscriptv3 unchanged. All84 prospective paragraphs pass488 explicit existing-native-formatter calls and122 full228x48/6x12 native ink/shadow planes;independent pixels,complete glyph order,bounds,whole words andinput/output guards pass. Seven contact sheets viewed. '
 'All9 sourcevoice tables nowhave13 clean-exact load/call pairs bound to originalparents:02053D24 atSP27C for02117460/02118A00/02118AA0;02053DB8 atSP27C for021174A0/02118A20/02118A40/02118A60/02118A80;02053F40 atSP274 for021189C0. These remainoffline source/native evidence,not conditional event visits. '
 'Current real BL-callsite probes148cases show thequeued paths already wrap;exclusion from thelatest selector alone didnotmean noformatting. Preserved2069 API-LR-STOP modal probe isnot anactual modal-routing claim;2069b usesoriginal54160/54798 BLreturnaddresses. '
 'Researchruntime2070 reusesonlythree existing28/12/20byte routing slots plus188byte selectorbank. Originalnumeric0..63 underdirect/Yes-No parents nowwrap;ritual64excluded. Monthly189C0 added tooriginal53F40 selector;alloldkeys andgatecode retained. Unrotated immediate TEQ preservescarry for exactrange-or-key tests. SourceARM9500b7d...;researchARM9218419fe0654cbf29bce30ba945f1907a1be9d62e1e2fe57380e6ac202e36c3d. No sections,cache,ITCM/arena or123040staged bytes grow. '
 '262172 native numeric predicate cases coverall65536lowwords plusfullword edges oncurrent/research direct/Yes-No code;allold675..681/688..741/761 and742 behavior,registers/SP/LR preserved. 16390 monthlyselector cases proveonly189C0 added withstrictalignment/highword andABI. All148 researchBLroute cases passnative memory/input/output/ABIguards;75 outputsunchanged73intentionallychanged. Freshall-unit reference census hasthree unchanged externalreferences andnointerioralias inthe newly occupiedFleet-slot4byte tail. '
 'All117 nonmodal parameter cases havefull source-bound planes:107 exact formatted/font-runtime inheritances and10 newlyexecuted228x48 native/independent planes;changed contact sheet viewed. Five receipt/rental modal cases83/84 retaincurrent behavior andneedtheir distinct geometry/native-plane proof;do notextrapolate the8observedactor-backed228x48 contexts. Twenty automaticwrap style cases remainopen (weakline endings/isolated finalwords);no waiversorEnglishrewrites. All84 formatting gates remainfalse. '
 'Repack/all3668 copy andopaque1484prefix/carrier1931 preservation,representative revisedtown transitions,registered cumulativeROM/exactclean-inputpatch remainpending. No playableROM,profile orregistry changed;V2047 stays489batches114layers withitsverified exactpatch. Source/prose2259,fresh740reread/656integrated/84pending,historical2059=1456revised603retained,200COMMON incomplete and1403historicalfreshreconciliations unchanged. Alljobs terminal. Everyremaining storyline/shared shop/town/random/playerprose,separategraphics/all18plaques,SC3B109classification andlaterolder-recordtechnicalre-audit remainopen. AllROMs/translations preserved;V1492promoted,canonicalunchanged,fullgoalactive.')
 ledger['primary_town_services_v2075']=dict(summary=summary,manuscript=str(DOC),evidence=evidence,visual_review=str(ROOT/'visual_review.json'),style_findings=style,formatting_complete=False,registered_integration_complete=False,previous_goal_turn_classification='progress:V2066 source-role/display checkpoint',goal_turn_classification='progress',full_goal_complete=False)
 ledger['primary_town_services_v2066']['superseded_research_checkpoint']='V2075'
 family=next(p for p in f['pending_contextual_families']if p['id']=='Primary-town-services84');family.update(runtime_research=str(PROOFS[3]),routed_native_plane_proof=str(PROOFS[6]),modal_parameter_cases_pending=5,style_findings_pending=20,formatting_reference_actual_release_pending=True)
 ledger['formatting_watchlist']['primary_town_consumer_v2075']=dict(physical_BL_route_proof=str(PROOFS[5]),routed_nonmodal_font_proof=str(PROOFS[6]),prospective_formatter_proof=str(PROOFS[0]),runtime_predicate_proof=str(PROOFS[4]),
  modal83_84_distinct_geometry_and_planes_pending=True,source_queued_fallback_already_formats=True,style_findings_pending=20,repacking_revised_actual_registered_release_pending=True)
 ledger['latest_checkpoint']='V2075 '+summary
 assert sum(ledger['source_prose_reviewed_counts_by_file'].values())==2259 and len(f['record_keys'])==740 and ledger['goal_status']=='active'and not ledger['full_goal_complete'];save(LEDGER,ledger)
 h=HANDOFF.read_text(encoding='utf-8').replace('# Current editorial handoff - V2066','# Current editorial handoff - V2075',1)
 marker='## Primary town-services84 measured consumer checkpoint - V2066';assert marker in h
 section='## Primary town-services84 native routing and plane research - V2075\n\n'+summary+'\n\n'
 section+='- Manuscriptv3 remains current;all84 formatting gates false. English and42/42 decisions unchanged. Prospective: `'+str(PROOFS[0])+'`;488calls122planes,7viewedsheets.\n'
 section+='- Caller map: `'+str(PROOFS[1])+'`. StaticARM literal-load reach is4095bytes;thecrowd/barter loads aremorethan1024bytes fromtheir literals. No Thumb assumption needed. All13caller spans/currentnativeentry bodies exactclean.\n'
 section+='- Runtimeproducer `scripts/primary_town_runtime_v2070.py`;plan `'+str(PROOFS[3])+'`;researchbinaryonly `work/analysis/town_services_runtime_v2070/ARM9_RUNTIME_RESEARCH_ONLY.bin`. Threecode slots:01FFC664(28),02157084(12),02151714(20);selector02147B9C(188). Code/layout growthzero. Freshcurrentreferenceproof2074checksnew4bytesinoriginalcomplete20byteFleet allocation;notarbitraryzeropadding.\n'
 section+='- Predicates: `'+str(PROOFS[4])+'`:262172numeric+16390monthlycases,0failures. Routedparagraphs: `'+str(PROOFS[5])+'`:148cases;onlyintended73outputschange. CurrentphysicalBLsource2069b: `'+str(PROOFS[2])+'`;API-only2069wrongmodalLRassumptionpreserved.\n'
 section+='- Routedfonts: `'+str(PROOFS[6])+'`;117nonmodal cases:107exact-byte/font-runtimeinheritances+10newfullnativeplanes. Eighttotalprospective/changedcontactsheets viewed: `'+str(ROOT/'visual_review.json')+'`. No hardfontgate waived. Twenty stylecases remainopen;do notchangeprosemerelytofit.\n'
 section+='- Five83/84receipt/rental modal cases remainaDISTINCTnativegeometry gate. Theiractualsource BL54798/return5479C matters;callingmacroAPIwithLR=STOP missescaller-scoped behavior. Nativeactor BL54160/return54164 frameworksarebound. Do notassume allpathsneednewrouting:54queuedsourcevoices alreadyuseoldsharedfallback;onlynumeric0..63 andmonthly selectorwerechanged.\n'
 section+='- Next: resolve83/84native modalgeometry/fullplanes andwrapstylefindings;completeguarded8KiB COMMONrepack/all3668 copies/opaque1484prefix/carrier1931;representative revisedtowntransitions;registeredlatecumulativebuild/exactclean-inputpatch. Use2070onlyafterallrequiredchecks;noROMcreatedfromit yet. Reusecompletedstory/V2047releasechecks. Fullobjectiveactive;alljobs terminal.\n\n'
 HANDOFF.write_text(h.replace(marker,section+marker,1),encoding='utf-8',newline='\n')
 for name in('editorial_review_goal.md','translation_progress.md','todo.md','known_issues.md'):
  with(Path('docs')/name).open('a',encoding='utf-8',newline='\n')as out:out.write('\n\n## V2075 Primary town-services native routing research\n\n'+summary+'\n')
 Path('docs/primary_town_services_v2075_checkpoint.md').write_text('# Primary town-services native routingV2075\n\n'+section,encoding='utf-8',newline='\n')
 save(ROOT/'checkpoint_receipt.json',dict(summary=summary,evidence=evidence,visual_review_sha256=sha((ROOT/'visual_review.json').read_bytes()),ledger_sha256=sha(LEDGER.read_bytes()),handoff_sha256=sha(HANDOFF.read_bytes()),source_prose_credit_added=0,completion_credit_added=0,registered_candidate_unchanged=True,source_prose=2259,historical_completed=2059,fresh_reread=740,fresh_integrated=656,fresh_pending=84,all_generated_ROMs_preserved=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
 print(dict(checkpoint='V2075',source_prose=2259,historical_complete=2059,fresh_pending=84,new_completion_credit=0,registered_ROM_unchanged=True))
