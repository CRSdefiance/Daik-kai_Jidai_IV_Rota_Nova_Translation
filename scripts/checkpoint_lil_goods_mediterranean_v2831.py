"""Record34 fresh source/prose/native reviews; preserve pending release gates."""
from pathlib import Path
from copy import deepcopy
from shutil import copy2
from collections import Counter
from dk4tool.patch.grand_race_menu_release import sha
from scripts.reconcile_contextual_mood_retentions_v2482 import historical_key
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_Goods_Mediterranean_checkpoint_v2831')
DOC=Path('translations/lil_goods_mediterranean_editorial_manuscript_v5.json')
SOURCE=Path('work/analysis/lil_Goods_Mediterranean_source_v2820/complete90_clean_current_native_context.json')
CONTROL=Path('work/analysis/lil_Goods_Mediterranean_controls_v2822/source_bound90_preambles_and_original_conditional_predicates.json')
BRANCH=Path('work/analysis/lil_Goods_Mediterranean_branches_v2821/original_relative_skip_operand_proof.json')
FONTS=Path('work/analysis/lil_Goods_Mediterranean_fonts_v2829/current_macro_QA_and_progressive_font_proof.json')
APPROVAL=Path('work/analysis/lil_Goods_Mediterranean_font_approval_v2830/approval_receipt.json')
FAMILY='Lil-Polder-Source-Goods-Mediterranean-B41-B43-B44-B45-B46-90'
SUMMARY='V2831 freshly reviews90 speeches in five complete LilSC2 exchanges B41/B43/B44/B45/B46: completed governor office and400,000 currency-gold gift, source-item usage and market-share strategy, Africa-and-India trade and Mediterranean return plans, Hayreddin downfall/subordination and crew leadership praise, and Pasha downfall/subordination and uncertain treasure presentation. There are67 revisions and23 individually justified retentions, each with exact clean/current source references, fresh gloss, whole-exchange context, localization note and allfive review gates. Preserve source-item versus ordinary goods, Market terminology, future funding intent, reports/rumors, distinct faction outcomes, Lil leadership credit, private Camille impressions and exact runtime substitutions; invent no romance, rank, item identity or earned progress. Mikhail native4C is source presentation state, not printable text to strip globally. Context metadata corrects the old-fellow attribution from Julio to source actor76 Mikhail; per-record gloss and English were already correct. B42 has no speech or choice and receives no credit. Older Local Product item-category wording conflicts with reviewed help Source Items and remains an exact-referenced uncredited semantic reconciliation lead. All273 native commands,90 complete preambles,128 relative sites/1280 clean-current branch cases,180 historical dispatcher contexts and32 current predicates pass; B44 queries completion20 at160/476. Only original four-byte alignment-read scratch is permitted and restoration recovers all4MiB. Local layout preserves global helpers/runtime;2824 failed compound split and original manuscript remain preserved, one conversational subject omission resolves it, and2828 keeps out-of-date, one-step-ahead, thanks-to and kind-of phrases together. All12 initial sheets and three changed successor sheets were viewed;86 exact native cases/688 alignment calls are reused andfour planes/32 calls reexecuted, binding90 complete216x64 planes/720 logical-compiled macro alignment calls. Fourteen formatter rejection tests and90 complete English/control/macro invariants pass. Only42 individual ordinary Japanese/English row-count notes are accepted, with no weak-ending, orphan, control, missing-glyph, overflow or blank-page waiver. These are offline current native CPU/font checks, not selected-scene gameplay. Fresh coverage2671 reread/2581 integrated/90 pending; source/prose2674 including844SC2. Completion stays2581,1808 historically revised and773 retained. Route1072 reviewed/982 completed. References, relocation, representative reconciliation, guarded cumulative build, exact clean patch and required current startup remain pending. Registered experimentalV2814 stays500 batches/114 accepted layers; V1492 remains promoted. Every ROM, earlier translation, source/canonical input and executed proof is preserved. COMMON750-752, all untouched story/shared shop-town/random/player prose, five uncredited named-target leads, raw rejected-object classification, SC3B109, separate graphics/all18 plaques and later older-record technical re-audit remain open. Full goal active; all jobs terminal.'

if __name__=='__main__':
    assert not ROOT.exists();lp=Path('translations/editorial_review_current_v1.json');ledger=read(lp);before=deepcopy(ledger)
    previous=Path('work/analysis/editorial_handoff_verification_v2819/verified_handoff.json');assert sha(lp.read_bytes())==read(previous)['ledger_sha256']
    doc,source,control,branch,font,approval=map(read,[DOC,SOURCE,CONTROL,BRANCH,FONTS,APPROVAL]);rows=doc['records'];ids=[r['id'] for r in rows]
    assert len(rows)==len(set(ids))==90 and Counter(r['editorial_decision'] for r in rows)=={'revise':67,'retain-wording':23}
    assert all(all(r['review'].values()) and r['source_meaning'] and r['localization_note'] for r in rows)
    assert source['total_editorial_objects']==90 and sum(len(b['all_clean_native_commands']) for b in source['blocks'])==273
    assert len(branch['cases'])==1280 and len(branch['operands_requiring_adjustment_when_resizing'])==128
    assert len(control['dispatch_cases'])==180 and len(control['current_original_predicate_cases'])==32 and [(q['block'],q['event']) for q in control['original_event_queries']]==[(44,20),(44,20)]
    assert font['manuscript_sha256']==sha(Path(doc['previous_manuscript']).read_bytes()) and len(font['cases'])==90 and font['current_original_macro_alignment_calls']==720
    assert approval['manuscript_sha256']==sha(DOC.read_bytes()) and approval['all12_review_sheets_viewed'] and approval['narrow_line_count_notes']==42
    fresh=ledger['contextual_story_natural_dialogue_pass_v1871'];assert (fresh['fresh_pass_records_explicitly_reread'],fresh['fresh_pass_records_integrated'],fresh['fresh_pass_records_pending_native_actual_release'])==(2581,2581,0)
    selected=[dict(file_path='/data/SC2.DK4',id=n) for n in ids];keys={(r['file_path'],r['id']) for r in fresh['record_keys']}
    assert not {(r['file_path'],r['id']) for r in selected}&keys
    assert {historical_key(r) for g in ledger['completed_editorial_families'] for r in g['records']}==keys
    assert ledger['records_with_source_and_prose_pass']==ledger['records_with_source_prose_drafts']==2584
    docs=[Path('docs')/n for n in ['editorial_handoff_current.md','translation_progress.md','editorial_review_goal.md','todo.md','known_issues.md']]
    assert docs[0].read_text(encoding='utf-8').startswith('# Current editorial handoff - V2818')
    ROOT.mkdir(parents=True)
    for p in [lp,*docs]:copy2(p,ROOT/(p.name+'.before'))
    ledger['records_with_source_and_prose_pass']=ledger['records_with_source_prose_drafts']=2674
    ledger['source_prose_reviewed_counts_by_file']['/data/SC2.DK4']=844
    ledger['reviewed_but_incomplete_route_record_IDs']['/data/SC2.DK4']=ids
    active=ledger['active_source_prose_drafts'];active['manuscripts'].append(str(DOC));active['route_record_subsets_pending'][str(DOC)]=ids
    active.update(status='3-reviewed-COMMON-incomplete;90-polder-source-item-Mediterranean-native-reviewed-pending-release',note='2671 fresh rereads:2581 integrated/reconciled and90 polder/source-item/Mediterranean reviews pending references, representative reconciliation and registered release. Source/prose2674; market COMMON750-752 and every untouched storyline/shared shop-town/random/player prose remain open.')
    fresh['record_keys'].extend(selected);fresh['record_IDs'].extend(ids)
    pending=dict(id=FAMILY,file_path='/data/SC2.DK4',blocks=[41,43,44,45,46],records=90,record_keys=selected,manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),
        proposed_revisions=67,retentions=23,source_prose_reviews_added=90,completion_credit_added=0,native_font_proof=str(FONTS),
        pending='Complete relocation/reference census and all128 resized relative sites/640 relocated branch cases and32 relocated original predicates; final parity/pagination; whole-script loader/entry proofs; representative shared-rule reconciliation; optional registered cumulative stage afterV2814, exact clean patch and required startup.',
        new_emulator_runs=0)
    fresh.update(fresh_pass_records_explicitly_reread=2671,fresh_pass_records_integrated=2581,fresh_pass_records_pending_native_actual_release=90,
        pending_record_keys=selected,pending_contextual_families=[pending],latest_pending_contextual_family=FAMILY,latest_contextual_manuscript=str(DOC),latest_contextual_choice_draft=None,coverage_note=active['note'])
    for unit in ledger['coverage_units']:
        if unit['id']=='all-route-scenes':unit.update(reviewed_route_records=1072,completed_route_records=982,next='Finish90 B41/B43/B44/B45/B46 reference/representative/release gates,then continue every untouched storyline/shared/town/random/player prose family.')
    ledger['coverage_units'].append(dict(**pending,status='source-prose-current-native-formatting-approved;references-representative-release-pending',full_goal_complete=False))
    ledger['formatting_watchlist']['lil_Goods_Mediterranean_v2831']=dict(status='all90-current-native-fonts-and-full-QA-pass;reference-padding-and-release-pending',
        manuscript=str(DOC),source_context=str(SOURCE),control_contract=str(CONTROL),branch_proof=str(BRANCH),native_font_proof=str(FONTS),
        all12_sheets_viewed_or_exact_previously_viewed=True,source_phrase_flow_findings_resolved=True,narrow_line_count_notes=42,
        no_orphan_predicate_or_missing_glyph_waivers=True,reference_map_pending=True,representative_reconciliation_pending=True,actual_selected_Goods_Mediterranean_IDs=[],new_emulator_runs=0)
    requirements=ROOT/'next_registered_integration_requirements.json'
    save(requirements,dict(parent_profile='all-routes-unified-v2814',parent_ROM=doc['current_ROM'],parent_ROM_sha256=doc['current_ROM_sha256'],
        manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),source_context=str(SOURCE),control_contract=str(CONTROL),branch_proof=str(BRANCH),native_fonts=str(FONTS),
        blocks=[41,43,44,45,46],speeches=90,choices=0,FE_panels=0,commands=273,relative_sites=128,
        next='Compile90 paragraphs through the exact local layout_v2/profile. Preserve273 commands,128 relative sites/640 relocated branch cases,32 relocated predicates and all opaque bytes. Prove336 whole-block loaders/two parent modes, shipped-entry census,331 other blocks exact,90 final parity planes/360 macro alignments/no extra page. Inherit exact shared native rules and V2814 actual startup; no individual conditional or nameplate visits absent a concrete risk. Register one guarded stage after fullV2814, expected501 batches/114 accepted layers; build cumulative candidate, exact clean-input patch and current startup before completion. Event44 completion20 queries and faction outcome alternatives remain exact.',
        preserve_every_ROM_translation_profile_accepted114_and_V1492_promotion=True,
        no_actual_selected_Goods_Mediterranean_or_individual_new_nameplate_claim=True,do_not_require_every_conditional_or_speaker_visit=True,
        current_COMMON_parser_unchanged='dk4tool.patch.surrender_advice_contextual_v1.current_entries',current_context='scripts/current_common_native_context_v2677.py',full_goal_complete=False))
    inventory=deepcopy(read(ledger['unfinished_editorial_scope_v2818']['path']))
    inventory.update(incomplete_route_source_prose_groups=[dict(family=FAMILY,file_path='/data/SC2.DK4',blocks=[41,43,44,45,46],count=90,record_IDs=ids)],incomplete_route_source_prose_count=90,
        next_focus='Integrate90 reviewed B41/B43/B44/B45/B46 reference/representative/release gates;continue all untouched storyline/shared shop/town/random/player prose. Market750-752 callers,raw rejected-object coverage and five uncredited named-target leads remain open.')
    for unit in inventory['broader_coverage_units']:
        if unit['id']=='all-route-scenes':unit.update(reviewed_route_records=1072,completed_route_records=982,source_prose_pending_records=90,source_prose_pending_family=FAMILY,next=inventory['next_focus'])
    inventory['source_item_UI_terminology_uncredited_lead']=dict(evidence='work/analysis/lil_Goods_Mediterranean_source_v2820/source_item_terminology_and_empty_B42_context.json',help_record='HELP_TOPIC_194',help_heading='Source Items',item_record='ITEM_CATEGORY_00',current_item_label='Local Product',source_prose_credit=0,completion_credit=0,next='Fresh semantic reconciliation of item-category wording against clean Japanese and reviewed help; keep later older-record technical re-audit separate.')
    inv=ROOT/'unfinished_editorial_scope_inventory.json';save(inv,inventory)
    ledger['unfinished_editorial_scope_v2831']=dict(path=str(inv),sha256=sha(inv.read_bytes()),incomplete_COMMON=3,incomplete_route_source_prose=90,full_goal_complete=False)
    proofpaths=[DOC,SOURCE,CONTROL,BRANCH,FONTS,APPROVAL,requirements,inv,previous,Path(__file__),Path(doc['scoped_profile_module']),
        Path('work/analysis/lil_Goods_Mediterranean_layout_v2828/all90_layout_and_QA.json'),
        *[Path(s['path']) for s in font['review_sheets']]]
    evidence={str(p):sha(p.read_bytes()) for p in proofpaths}
    ledger['lil_Goods_Mediterranean_source_prose_native_v2831']=dict(summary=SUMMARY,**pending,evidence=evidence,goal_turn_classification='progress',full_goal_complete=False)
    ledger['latest_checkpoint']=SUMMARY
    for key in ['completed_editorial_families','records_editorially_completed','records_revised_and_integrated','retained_wordings_editorially_completed','completed_editorial_record_counts_by_file',
        'current_integrated_candidate','reviewed_but_incomplete_COMMON_IDs','unresolved_graphics_work','older_record_reaudit_after_full_editorial_goal']:
        assert ledger[key]==before[key],key
    assert len(fresh['record_keys'])==len({(r['file_path'],r['id']) for r in fresh['record_keys']})==2671 and len(fresh['integrated_record_keys'])==2581
    assert ledger['goal_status']=='active' and not ledger['full_goal_complete'];save(lp,ledger)
    section='## V2831:90 polder, source-item and Mediterranean reviews; reference and release pending\n\n'+SUMMARY+'\n\nManuscript: '+DOC.as_posix()+'. Source: '+SOURCE.as_posix()+'. Native proof: '+FONTS.as_posix()+'. Next integration: '+requirements.as_posix()+'. Unfinished scope: '+inv.as_posix()+'.\n\n'
    for i,p in enumerate(docs):
        first,rest=p.read_text(encoding='utf-8').split('\n',1)
        # Earlier checkpoint sections remain unchanged.
        p.write_text(('# Current editorial handoff - V2831' if i==0 else first)+'\n\n'+section+rest,encoding='utf-8',newline='\n')
    candidate=ledger['current_integrated_candidate']
    save(ROOT/'checkpoint_receipt.json',dict(checkpoint='V2831',summary=SUMMARY,evidence=evidence,updated_files={str(p):sha(p.read_bytes()) for p in [lp,*docs]},
        new_completed_records=0,new_source_prose_reviews=90,proposed_revisions=67,justified_retentions=23,fresh_reread=2671,fresh_integrated=2581,fresh_pending=90,
        source_prose=2674,completed=2581,historical_revised=1808,historical_retained=773,incomplete_COMMON=3,incomplete_route=90,
        candidate=candidate['path'],candidate_sha256=candidate['sha256'],patch=candidate['patch'],patch_sha256=candidate['patch_sha256'],
        next_requirements=str(requirements),actual_selected_Goods_Mediterranean_IDs=[],new_emulator_runs=0,goal_turn_classification='progress',all_jobs_terminal=True,full_goal_complete=False))
    print('V2831:90new contextual/native reviews;67revisions/23retentions.2671reread/2581integrated/90pending;source-prose2674. V2814unchanged;full goal active.')
