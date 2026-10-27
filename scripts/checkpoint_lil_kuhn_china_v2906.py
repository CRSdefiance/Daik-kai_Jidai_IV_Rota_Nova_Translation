"""Record218 complete contextual/native reviews with zero integration credit."""
from pathlib import Path
from copy import deepcopy
from shutil import copy2
from collections import Counter
from dk4tool.patch.grand_race_menu_release import sha
from scripts.reconcile_contextual_mood_retentions_v2482 import historical_key
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_Kuhn_China_checkpoint_v2906')
DOC=Path('translations/lil_kuhn_china_editorial_manuscript_v6.json')
SOURCE=Path('work/analysis/lil_Kuhn_China_connected_source_v2891/complete218_clean_current_native_context.json')
CONTROL=Path('work/analysis/lil_Kuhn_China_controls_v2894/source_bound218_preambles_FE_and_original_conditional_predicates.json')
BRANCH=Path('work/analysis/lil_Kuhn_China_branches_v2892/original_relative_skip_operand_proof.json')
FONTS=Path('work/analysis/lil_Kuhn_China_fonts_v2904/current_macro_QA_and_progressive_font_proof.json')
FE=Path('work/analysis/lil_Kuhn_China_FE_v2901b/current_FE_macro_font_and_typed_paper_proof.json')
APPROVAL=Path('work/analysis/lil_Kuhn_China_font_approval_v2905/approval_receipt.json')
PREVIOUS=Path('work/analysis/lil_Kuhn_Alliance_heading_v2889/verified_handoff.json')
BLOCKS=[51,52,53,54,55,56,146,147,148]
FAMILY='Lil-Kuhn-China-B51-B52-B53-B54-B55-B56-B146-B147-B148-218'
SUMMARY='V2906 freshly reviews218 speeches across nine complete Lil SC2 exchanges B51/B52/B53/B54/B55/B56/B146/B147/B148: Georg warnings, assassination and crest inference, the anonymous woman questioning Lil ideals, the private false-flag plot, Li downfall/subordination alternatives, the declaration of war, the search for Camille and Hodram temporary voyage offer, the Hangzhou identity reveal and warning, and the bartender inquiry. There are152 revisions and66 individually justified retentions, each with exact clean/current references, source gloss, whole-exchange context, localization notes and allfive review gates. Preserve character allegations and uncertainty rather than narrator proof; Lil first-person wish to earn money and help people worldwide; anonymous FE labels until Maria introduces herself; source branch dependencies, separate crew alternatives, private knowledge, the disowned-son qualification and metaphorical keys to saving Asia. Hodram speaks his source two-part name; do not insert Joakim into that line, make him Camille father, invent romance, gender the assassin or mentor, add ranks or reveal the later birth-name/backstory early. The bartender remembered feminine nickname is translated respectfully without invented ridicule, elapsed years or destinations. BothB66 andB121 still require fresh review. All501 native commands/218 complete preambles/160 relative sites/1600 clean-current branch cases/436 historical dispatcher cases and40 current original predicates pass. Event queries56:80/232=147,146:364=27,147:1492=52 retain exact source arguments. Ordinary0A is actor10 Xien, not a dropped LF. All22 FE selectors precede fallback208 and use original24310 with null actor; FI is independently expanded to Lil. The variadic5473C entry r1 is not a geometry argument; mode1 paper comes the calibrated typed context. Current fonts bind196 progressive216x64 planes and22 FE228x48 logical/228x64 physical planes,1744 logical/compiled macro alignment cases and complete leading/interior/trailing glyph, blank-paper, bounds, return and pagination checks. All25 initial progressive sheets and3 FE sheets were viewed; revised normal sheet7 was then viewed and24 unchanged sheets match viewed predecessors exactly. Twenty-eight metric/manual-layout negatives plus11 source/speaker/consumer negatives reject; only89 individual Japanese/English row-count notes remain. No orphan, weak-ending, control, missing-glyph, overflow or blank-page waiver. One awkward claim-to-avenge construction is replaced with on-the-pretext-of-avenging, preserving the source false excuse. All executed drafts, failed producers and global helpers are preserved. These are offline CPU/font checks, not selected-scene gameplay. Fresh coverage is2971 reread /2753 integrated-reconciled /218 pending; source/prose2974 including1144SC2. Completion stays2753:1938 historically revised and815 retained. Routes1372 reviewed/1154 completed. Reference relocation, final parity, whole loaders/entry census, representative reconciliation and registered cumulative integration remain pending. Current experimentalV2883 remains502 manifest batches/114 accepted layers with its exact clean-input patch and31-frame actual coldboot startup proof. This checkpoint does not change any ROM, registry, builder, runtime, font or graphic. COMMON750-752, every untouched storyline/shared shop-town/random/player prose family, Source Items/Local Product terminology and five named-target leads, raw rejected-object classification including uncreditedB141 inventory assertion, SC3B109, separate graphics/all18 plaques and later older-record technical re-audit remain open. Preserve every ROM and earlier translation; V1492 stays promoted. Full goal active; all jobs terminal.'

if __name__=='__main__':
    assert not ROOT.exists();lp=Path('translations/editorial_review_current_v1.json');ledger=read(lp);before=deepcopy(ledger)
    assert sha(lp.read_bytes())==read(PREVIOUS)['ledger_sha256']
    doc,source,control,branch,font,fe,approval=map(read,[DOC,SOURCE,CONTROL,BRANCH,FONTS,FE,APPROVAL]);rows=doc['records'];ids=[r['id'] for r in rows]
    assert len(rows)==len(set(ids))==218 and Counter(r['editorial_decision'] for r in rows)=={'revise':152,'retain-wording':66}
    assert all(all(r['review'].values()) and r['source_meaning'] and r['localization_note'] and r['context'] for r in rows)
    assert source['total_editorial_objects']==218 and sum(len(b['all_clean_native_commands']) for b in source['blocks'])==501
    assert len(branch['cases'])==1600 and len(branch['operands_requiring_adjustment_when_resizing'])==160
    assert len(control['dispatch_cases'])==436 and len(control['current_original_predicate_cases'])==40
    assert [(q['block'],q['offset'],q['event']) for q in control['original_event_queries']]==[(56,80,147),(56,232,147),(146,364,27),(147,1492,52)]
    assert len(font['cases'])==196 and font['current_original_macro_alignment_calls']==1568 and len(fe['cases'])==22 and fe['current_original_null_actor_macro_alignment_cases']==176
    assert approval['manuscript_sha256']==sha(DOC.read_bytes()) and approval['all28_review_sheets_viewed'] and approval['narrow_line_count_notes']==89
    fresh=ledger['contextual_story_natural_dialogue_pass_v1871'];assert (fresh['fresh_pass_records_explicitly_reread'],fresh['fresh_pass_records_integrated'],fresh['fresh_pass_records_pending_native_actual_release'])==(2753,2753,0)
    selected=[dict(file_path='/data/SC2.DK4',id=n) for n in ids];keys={historical_key(r) for r in fresh['record_keys']}
    assert not {historical_key(r) for r in selected}&keys and {historical_key(r) for g in ledger['completed_editorial_families'] for r in g['records']}==keys
    assert ledger['records_with_source_and_prose_pass']==ledger['records_with_source_prose_drafts']==2756
    docs=[Path('docs')/n for n in ['editorial_handoff_current.md','translation_progress.md','editorial_review_goal.md','todo.md','known_issues.md']]
    assert docs[0].read_text(encoding='utf-8').startswith('# Current editorial handoff - V2887')
    ROOT.mkdir(parents=True)
    for p in [lp,*docs]:copy2(p,ROOT/(p.name+'.before'))
    ledger['records_with_source_and_prose_pass']=ledger['records_with_source_prose_drafts']=2974
    ledger['source_prose_reviewed_counts_by_file']['/data/SC2.DK4']=1144
    ledger['reviewed_but_incomplete_route_record_IDs']['/data/SC2.DK4']=ids
    active=ledger['active_source_prose_drafts'];active['manuscripts'].append(str(DOC));active['route_record_subsets_pending'][str(DOC)]=ids
    active.update(status='3-reviewed-COMMON-incomplete;218-Kuhn-China-native-reviewed-pending-release',note='2971 fresh rereads:2753 integrated/reconciled and218 Kuhn/China reviews pending references, representative reconciliation and registered release. Source/prose2974; COMMON750-752 and all untouched story/shared shop-town/random/player prose remain open.')
    fresh['record_keys'].extend(selected);fresh['record_IDs'].extend(ids)
    pending=dict(id=FAMILY,file_path='/data/SC2.DK4',blocks=BLOCKS,records=218,record_keys=selected,manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),
        proposed_revisions=152,retentions=66,source_prose_reviews_added=218,completion_credit_added=0,native_font_proof=str(FONTS),native_FE_font_proof=str(FE),
        pending='Complete501-command reference census,160 relative sites/800 relocated cases,40 relocated predicates and4 event queries,218 final parity targets/872 macro alignments,336 whole loaders/two parent modes and representative rules; guarded cumulative integration after fullV2883, exact clean patch and current startup.',new_emulator_runs=0)
    fresh.update(fresh_pass_records_explicitly_reread=2971,fresh_pass_records_integrated=2753,fresh_pass_records_pending_native_actual_release=218,
        pending_record_keys=selected,pending_contextual_families=[pending],latest_pending_contextual_family=FAMILY,latest_contextual_manuscript=str(DOC),latest_contextual_choice_draft=None,coverage_note=active['note'])
    for unit in ledger['coverage_units']:
        if unit['id']=='all-route-scenes':unit.update(reviewed_route_records=1372,completed_route_records=1154,next='Finish218 Kuhn/China reference/representative/release gates,then continue every untouched storyline/shared/town/random/player prose family.')
    ledger['coverage_units'].append(dict(**pending,status='source-prose-current-native-formatting-approved;references-representative-release-pending',full_goal_complete=False))
    ledger['formatting_watchlist']['lil_Kuhn_China_v2906']=dict(status='all218-current-native-fonts-and-full-QA-pass;reference-padding-and-release-pending',manuscript=str(DOC),source_context=str(SOURCE),control_contract=str(CONTROL),branch_proof=str(BRANCH),native_font_proof=str(FONTS),native_FE_font_proof=str(FE),
        all28_sheets_viewed_or_exact_previously_viewed=True,source_phrase_flow_findings_resolved=True,narrow_line_count_notes=89,no_orphan_predicate_or_missing_glyph_waivers=True,reference_map_pending=True,representative_reconciliation_pending=True,actual_selected_Kuhn_China_IDs=[],new_emulator_runs=0)
    requirements=ROOT/'next_registered_integration_requirements.json'
    save(requirements,dict(parent_profile='all-routes-unified-v2883',parent_ROM=doc['current_ROM'],parent_ROM_sha256=doc['current_ROM_sha256'],manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),source_context=str(SOURCE),control_contract=str(CONTROL),branch_proof=str(BRANCH),native_fonts=str(FONTS),native_FE_fonts=str(FE),
        blocks=BLOCKS,speeches=218,choices=0,FE_panels=22,commands=501,relative_sites=160,
        next='Compile218 with exact local lil_kuhn_china_layout_v1/profile. Preserve501 commands,160 relative sites/800 relocated cases,40 original predicates/four source event queries and every opaque byte. Verify336 whole loaders/two parent modes/full entry census;327 other blocks exact. Verify218 final parity planes/872 macro alignments/no blank page,including22 null-actor FE/one FI. Bind unchanged shared rules and V2883 actual startup; no individual conditional/nameplate visits absent a concrete risk. Register one guarded optional stage after fullV2883; expected503 batches/114 accepted layers. Build cumulative ROM, exact clean patch and current startup before completing218. Preserve original EV2 dependencies, uncertain allegations, private knowledge, both missing backstory branches and literal FE labels.',
        preserve_every_ROM_translation_profile_accepted114_and_V1492_promotion=True,no_actual_selected_Kuhn_China_or_individual_new_nameplate_claim=True,do_not_require_every_conditional_or_speaker_visit=True,current_COMMON_parser_unchanged='dk4tool.patch.surrender_advice_contextual_v1.current_entries',current_context='scripts/current_common_native_context_v2677.py',full_goal_complete=False))
    inventory=deepcopy(read(ledger['unfinished_editorial_scope_v2887']['path']))
    inventory.update(incomplete_route_source_prose_groups=[dict(family=FAMILY,file_path='/data/SC2.DK4',blocks=BLOCKS,count=218,record_IDs=ids)],incomplete_route_source_prose_count=218,next_focus='Integrate218 reviewed Kuhn/China reference/representative/release gates;continue all untouched storyline/shared shop/town/random/player prose. B66/B121 backstory,market750-752callers,raw rejected-object coverage and five uncredited named-target leads remain open.')
    lead=dict(file_path='/data/SC2.DK4',block=141,source_ROM='work/clean.nds',source_ROM_sha256=doc['source_ROM_sha256'],producer='scripts/inventory_lil_lessons_v1717.py',producer_sha256=sha(Path('scripts/inventory_lil_lessons_v1717.py').read_bytes()),location='inventory:43;raw_headers==assertion',status='uncredited-source-consumer-classification-lead;outside-selected-nine-blocks',finding='Exploratory inventory of cleanB141 raised raw_headers assertion. No rejected object is silently skipped and no review/completion credit is assigned.',completion_credit_added=0)
    inventory['raw_source_coverage_revisit'].setdefault('additional_exact_uncredited_leads',[]).append(lead)
    ledger['raw_source_coverage_revisit'].setdefault('additional_exact_uncredited_leads',[]).append(deepcopy(lead))
    for unit in inventory['broader_coverage_units']:
        if unit['id']=='all-route-scenes':unit.update(reviewed_route_records=1372,completed_route_records=1154,source_prose_pending_records=218,source_prose_pending_family=FAMILY,next=inventory['next_focus'])
    inv=ROOT/'unfinished_editorial_scope_inventory.json';save(inv,inventory)
    ledger['unfinished_editorial_scope_v2906']=dict(path=str(inv),sha256=sha(inv.read_bytes()),incomplete_COMMON=3,incomplete_route_source_prose=218,full_goal_complete=False)
    proofpaths=[DOC,SOURCE,CONTROL,BRANCH,FONTS,FE,APPROVAL,requirements,inv,PREVIOUS,Path(__file__),Path(doc['scoped_profile_module']),Path(doc['native_formatter_module']),Path('work/analysis/lil_Kuhn_China_layout_v2903/all218_layout_and_QA.json'),*[Path(s['path']) for s in approval['review_sheets']]]
    evidence={str(p):sha(p.read_bytes()) for p in proofpaths}
    ledger['lil_Kuhn_China_source_prose_native_v2906']=dict(summary=SUMMARY,**pending,evidence=evidence,goal_turn_classification='progress',full_goal_complete=False)
    ledger['latest_checkpoint']=SUMMARY
    for key in ['completed_editorial_families','records_editorially_completed','records_revised_and_integrated','retained_wordings_editorially_completed','completed_editorial_record_counts_by_file','current_integrated_candidate','reviewed_but_incomplete_COMMON_IDs','unresolved_graphics_work','older_record_reaudit_after_full_editorial_goal']:
        assert ledger[key]==before[key],key
    assert len(fresh['record_keys'])==len({historical_key(r) for r in fresh['record_keys']})==2971 and len(fresh['integrated_record_keys'])==2753
    assert ledger['goal_status']=='active' and not ledger['full_goal_complete'];save(lp,ledger)
    section='## V2906:218 Kuhn/China reviews; reference and release pending\n\n'+SUMMARY+'\n\nManuscript: '+DOC.as_posix()+'. Source: '+SOURCE.as_posix()+'. Ordinary native proof: '+FONTS.as_posix()+'. FE native proof: '+FE.as_posix()+'. Next integration: '+requirements.as_posix()+'. Unfinished scope: '+inv.as_posix()+'.\n\n'
    for i,p in enumerate(docs):
        first,rest=p.read_text(encoding='utf-8').split('\n',1)
        p.write_text(('# Current editorial handoff - V2906' if i==0 else first)+'\n\n'+section+rest,encoding='utf-8',newline='\n')
    candidate=ledger['current_integrated_candidate']
    save(ROOT/'checkpoint_receipt.json',dict(checkpoint='V2906',summary=SUMMARY,evidence=evidence,updated_files={str(p):sha(p.read_bytes()) for p in [lp,*docs]},new_completed_records=0,new_source_prose_reviews=218,proposed_revisions=152,justified_retentions=66,fresh_reread=2971,fresh_integrated=2753,fresh_pending=218,source_prose=2974,completed=2753,historical_revised=1938,historical_retained=815,incomplete_COMMON=3,incomplete_route=218,
        candidate=candidate['path'],candidate_sha256=candidate['sha256'],patch=candidate['patch'],patch_sha256=candidate['patch_sha256'],next_requirements=str(requirements),actual_selected_Kuhn_China_IDs=[],new_emulator_runs=0,goal_turn_classification='progress',all_jobs_terminal=True,full_goal_complete=False))
    print('V2906:218 new contextual/native reviews;152revisions/66retentions.2971reread/2753integrated/218pending;source-prose2974. V2883 unchanged;full goal active.')
