"""Record34 fresh source/prose/native reviews; preserve pending release gates."""
from pathlib import Path
from copy import deepcopy
from shutil import copy2
from collections import Counter
from dk4tool.patch.grand_race_menu_release import sha
from scripts.reconcile_contextual_mood_retentions_v2482 import historical_key
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_Kuhn_Alliance_checkpoint_v2874')
DOC=Path('translations/lil_kuhn_alliance_editorial_manuscript_v8.json')
SOURCE=Path('work/analysis/lil_Kuhn_Alliance_source_v2846/complete82_clean_current_native_context.json')
CONTROL=Path('work/analysis/lil_Kuhn_Alliance_controls_v2848/source_bound82_preambles_and_original_conditional_predicates.json')
BRANCH=Path('work/analysis/lil_Kuhn_Alliance_branches_v2847/original_relative_skip_operand_proof.json')
FONTS=Path('work/analysis/lil_Kuhn_Alliance_fonts_v2872/current_macro_QA_and_progressive_font_proof.json')
APPROVAL=Path('work/analysis/lil_Kuhn_Alliance_font_approval_v2873/approval_receipt.json')
FAMILY='Lil-Kuhn-Alliance-B47-B48-B49-B50-82'
SUMMARY='V2874 freshly reviews 82 speeches in four complete Lil SC2 exchanges B47/B48/B49/B50: Batavia invitation, public alliance negotiation, Georg private report to Antony Kuhn, and the later alliance approach. There are 63 proposed revisions and 19 individually justified retentions. Each has exact clean/current references, a fresh gloss, complete-exchange context, localization notes and all five review gates. Preserve Jam self-important joke and pain reaction without inventing who struck him; Georg polite business voice and coercion; the 5000 currency-gold offer; conditional anti-Pereira allegations; Lil initial skepticism, interest, hurt/confusion and pressured assent; Camille private shock, trembling hands, failed explanations, hurt and departure; and every crew alternative. Private Marinus identification and unspecified arrangements do not grant Lil knowledge, prove a death or establish Pereira ties. Use approved Camille; Mr. conveys polite business address while sama does not create Lord ranks. Kuhn feminine-nickname remark stays character dialogue without added ridicule or a modern identity explanation. Original event48 requires47,49 requires48, and50 requires48 while excluding54/121/55/56; B50 is not an unconditional duplicate pact. All195 commands,82 complete preambles,60 relative sites/600 clean-current branch cases,164 historical dispatcher contexts and15 current original predicates pass; there are no8100 event queries, FE panels or choices in this batch. Source-owned alignment scratch is restored and every unowned4MiB remains exact. Historical catalog getters identify Georg56 and Antony Kuhn40; aliases/composite catalog strings do not authorize new name edits or claim observed nameplates. The local profile binds13 selectors, including printable38 Georg state. Formatting binds82 complete216x64 native planes/656 macro alignment calls and fullQA. All11 initial2854 sheets, seven changed2869 sheets and final2872 sheet3 were viewed; final proof reexecutes one plane/eight calls and reuses81 planes/648 calls by exact source/English/runtime/profile/encoded/preview identity, with the prior14 changed planes/112 calls bound in its chain. Fourteen metric/manual-layout rejections and82 complete English/control/macro invariants pass. Only22 individual ordinary Japanese/English row-count notes remain; no weak-ending, orphan, control, overflow, missing-glyph or blank-page waiver is granted. The2851/2856/2856b/2862 failed layouts are preserved. One paragraph is refined from the clean meaning to natural no-easy-task understatement; local rules improve questions, demonstratives, negation and phrasal boundaries, and avoid over-constraining heard/of. All global helpers/native bytes remain unchanged. These are offline CPU/font checks, not selected Kuhn-scene gameplay. Fresh coverage is2753 reread /2671 integrated-reconciled /82 pending; source/prose2756 including926SC2. Completion stays2671,1875 historically revised and796 retained. Routes1154 reviewed/1072 completed. Reference relocation, final parity/pagination, whole loaders/entries, representative reconciliation and guarded registered integration remain pending. Current experimental V2840 remains501 manifest batches/114 accepted layers with an exactly reconstructable clean-input patch and verified31-frame New Game/town startup. ROM/registry/builder/manifest/patch/runtime/fonts/graphics are unchanged by this checkpoint. Preserve every ROM, earlier translation, profile, clean/canonical input and executed proof; V1492 remains promoted. COMMON750-752, all untouched story/shared shop-town/random/player prose, the uncredited Source Items/Local Product terminology lead, five uncredited named-target leads, raw rejected-object classification, SC3B109, separate graphics/all18 plaques and later older-record technical re-audit stay open. The B66 and B121 true-name/backstory alternatives both still require fresh contextual review. Full goal active; all jobs terminal.'

if __name__=='__main__':
    assert not ROOT.exists();lp=Path('translations/editorial_review_current_v1.json');ledger=read(lp);before=deepcopy(ledger)
    previous=Path('work/analysis/editorial_handoff_verification_v2845b/verified_handoff.json');assert sha(lp.read_bytes())==read(previous)['ledger_sha256']
    doc,source,control,branch,font,approval=map(read,[DOC,SOURCE,CONTROL,BRANCH,FONTS,APPROVAL]);rows=doc['records'];ids=[r['id'] for r in rows]
    assert len(rows)==len(set(ids))==82 and Counter(r['editorial_decision'] for r in rows)=={'revise':63,'retain-wording':19}
    assert all(all(r['review'].values()) and r['source_meaning'] and r['localization_note'] for r in rows)
    assert source['total_editorial_objects']==82 and sum(len(b['all_clean_native_commands']) for b in source['blocks'])==195
    assert len(branch['cases'])==600 and len(branch['operands_requiring_adjustment_when_resizing'])==60
    assert len(control['dispatch_cases'])==164 and len(control['current_original_predicate_cases'])==15 and [(q['block'],q['event']) for q in control['original_event_queries']]==[]
    assert font['manuscript_sha256']==sha(Path(doc['previous_manuscript']).read_bytes()) and len(font['cases'])==82 and font['current_original_macro_alignment_calls']==656
    assert approval['manuscript_sha256']==sha(DOC.read_bytes()) and approval['all11_review_sheets_viewed'] and approval['narrow_line_count_notes']==22
    fresh=ledger['contextual_story_natural_dialogue_pass_v1871'];assert (fresh['fresh_pass_records_explicitly_reread'],fresh['fresh_pass_records_integrated'],fresh['fresh_pass_records_pending_native_actual_release'])==(2671,2671,0)
    selected=[dict(file_path='/data/SC2.DK4',id=n) for n in ids];keys={(r['file_path'],r['id']) for r in fresh['record_keys']}
    assert not {(r['file_path'],r['id']) for r in selected}&keys
    assert {historical_key(r) for g in ledger['completed_editorial_families'] for r in g['records']}==keys
    assert ledger['records_with_source_and_prose_pass']==ledger['records_with_source_prose_drafts']==2674
    docs=[Path('docs')/n for n in ['editorial_handoff_current.md','translation_progress.md','editorial_review_goal.md','todo.md','known_issues.md']]
    assert docs[0].read_text(encoding='utf-8').startswith('# Current editorial handoff - V2844')
    ROOT.mkdir(parents=True)
    for p in [lp,*docs]:copy2(p,ROOT/(p.name+'.before'))
    ledger['records_with_source_and_prose_pass']=ledger['records_with_source_prose_drafts']=2756
    ledger['source_prose_reviewed_counts_by_file']['/data/SC2.DK4']=926
    ledger['reviewed_but_incomplete_route_record_IDs']['/data/SC2.DK4']=ids
    active=ledger['active_source_prose_drafts'];active['manuscripts'].append(str(DOC));active['route_record_subsets_pending'][str(DOC)]=ids
    active.update(status='3-reviewed-COMMON-incomplete;82-Kuhn-alliance-native-reviewed-pending-release',note='2753 fresh rereads:2671 integrated/reconciled and82 Kuhn-alliance reviews pending references, representative reconciliation and registered release. Source/prose2756; COMMON750-752 and all untouched story/shared shop-town/random/player prose remain open.')
    fresh['record_keys'].extend(selected);fresh['record_IDs'].extend(ids)
    pending=dict(id=FAMILY,file_path='/data/SC2.DK4',blocks=[47,48,49,50],records=82,record_keys=selected,manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),
        proposed_revisions=63,retentions=19,source_prose_reviews_added=82,completion_credit_added=0,native_font_proof=str(FONTS),
        pending='Complete195-command reference census,60 relative sites/300 relocated cases,15 relocated predicates,82 final parity targets/328 macro alignments,336 whole loaders/two parent modes and representative rules; guarded cumulative integration after fullV2840, exact clean patch and current startup.',
        new_emulator_runs=0)
    fresh.update(fresh_pass_records_explicitly_reread=2753,fresh_pass_records_integrated=2671,fresh_pass_records_pending_native_actual_release=82,
        pending_record_keys=selected,pending_contextual_families=[pending],latest_pending_contextual_family=FAMILY,latest_contextual_manuscript=str(DOC),latest_contextual_choice_draft=None,coverage_note=active['note'])
    for unit in ledger['coverage_units']:
        if unit['id']=='all-route-scenes':unit.update(reviewed_route_records=1154,completed_route_records=1072,next='Finish82 B47/B48/B49/B50 reference/representative/release gates,then continue every untouched storyline/shared/town/random/player prose family.')
    ledger['coverage_units'].append(dict(**pending,status='source-prose-current-native-formatting-approved;references-representative-release-pending',full_goal_complete=False))
    ledger['formatting_watchlist']['lil_Kuhn_Alliance_v2874']=dict(status='all82-current-native-fonts-and-full-QA-pass;reference-padding-and-release-pending',
        manuscript=str(DOC),source_context=str(SOURCE),control_contract=str(CONTROL),branch_proof=str(BRANCH),native_font_proof=str(FONTS),
        all11_sheets_viewed_or_exact_previously_viewed=True,source_phrase_flow_findings_resolved=True,narrow_line_count_notes=22,
        no_orphan_predicate_or_missing_glyph_waivers=True,reference_map_pending=True,representative_reconciliation_pending=True,actual_selected_Kuhn_Alliance_IDs=[],new_emulator_runs=0)
    requirements=ROOT/'next_registered_integration_requirements.json'
    save(requirements,dict(parent_profile='all-routes-unified-v2840',parent_ROM=doc['current_ROM'],parent_ROM_sha256=doc['current_ROM_sha256'],
        manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),source_context=str(SOURCE),control_contract=str(CONTROL),branch_proof=str(BRANCH),native_fonts=str(FONTS),
        blocks=[47,48,49,50],speeches=82,choices=0,FE_panels=0,commands=195,relative_sites=60,
        next='Compile82 paragraphs with the exact local lil_kuhn_alliance_layout_v4/profile. Preserve195 commands,60 relative sites/300 relocated cases,15 relocated predicates and every opaque byte. Verify336 whole loaders/two parent modes/full entry census;332 other blocks exact. Verify82 final parity planes/328 macro alignments/no blank page. Bind shared rules and V2840 actual startup; no individual conditional/nameplate visits absent a concrete risk. Register one guarded optional stage after fullV2840; expected502 batches/114 accepted layers. Build cumulative ROM, exact clean patch and current startup before completing82. Preserve original EV2 dependencies48requires47,49requires48,50requires48andnot54/121/55/56. Public/private knowledge and source nickname characterization stay distinct.',
        preserve_every_ROM_translation_profile_accepted114_and_V1492_promotion=True,
        no_actual_selected_Kuhn_Alliance_or_individual_new_nameplate_claim=True,do_not_require_every_conditional_or_speaker_visit=True,
        current_COMMON_parser_unchanged='dk4tool.patch.surrender_advice_contextual_v1.current_entries',current_context='scripts/current_common_native_context_v2677.py',full_goal_complete=False))
    inventory=deepcopy(read(ledger['unfinished_editorial_scope_v2844']['path']))
    inventory.update(incomplete_route_source_prose_groups=[dict(family=FAMILY,file_path='/data/SC2.DK4',blocks=[47,48,49,50],count=82,record_IDs=ids)],incomplete_route_source_prose_count=82,
        next_focus='Integrate82 reviewed B47/B48/B49/B50 reference/representative/release gates;continue all untouched storyline/shared shop/town/random/player prose. Market750-752 callers,raw rejected-object coverage and five uncredited named-target leads remain open.')
    for unit in inventory['broader_coverage_units']:
        if unit['id']=='all-route-scenes':unit.update(reviewed_route_records=1154,completed_route_records=1072,source_prose_pending_records=82,source_prose_pending_family=FAMILY,next=inventory['next_focus'])
    inv=ROOT/'unfinished_editorial_scope_inventory.json';save(inv,inventory)
    ledger['unfinished_editorial_scope_v2874']=dict(path=str(inv),sha256=sha(inv.read_bytes()),incomplete_COMMON=3,incomplete_route_source_prose=82,full_goal_complete=False)
    proofpaths=[DOC,SOURCE,CONTROL,BRANCH,FONTS,APPROVAL,requirements,inv,previous,Path(__file__),Path(doc['scoped_profile_module']),
        Path('work/analysis/lil_Kuhn_Alliance_layout_v2871/all82_layout_and_QA.json'),
        *[Path(s['path']) for s in font['review_sheets']]]
    evidence={str(p):sha(p.read_bytes()) for p in proofpaths}
    ledger['lil_Kuhn_Alliance_source_prose_native_v2874']=dict(summary=SUMMARY,**pending,evidence=evidence,goal_turn_classification='progress',full_goal_complete=False)
    ledger['latest_checkpoint']=SUMMARY
    for key in ['completed_editorial_families','records_editorially_completed','records_revised_and_integrated','retained_wordings_editorially_completed','completed_editorial_record_counts_by_file',
        'current_integrated_candidate','reviewed_but_incomplete_COMMON_IDs','unresolved_graphics_work','older_record_reaudit_after_full_editorial_goal']:
        assert ledger[key]==before[key],key
    assert len(fresh['record_keys'])==len({(r['file_path'],r['id']) for r in fresh['record_keys']})==2753 and len(fresh['integrated_record_keys'])==2671
    assert ledger['goal_status']=='active' and not ledger['full_goal_complete'];save(lp,ledger)
    section='## V2874:82 Kuhn alliance reviews; reference and release pending\n\n'+SUMMARY+'\n\nManuscript: '+DOC.as_posix()+'. Source: '+SOURCE.as_posix()+'. Native proof: '+FONTS.as_posix()+'. Next integration: '+requirements.as_posix()+'. Unfinished scope: '+inv.as_posix()+'.\n\n'
    for i,p in enumerate(docs):
        first,rest=p.read_text(encoding='utf-8').split('\n',1)
        # Earlier checkpoint sections remain unchanged.
        p.write_text(('# Current editorial handoff - V2874' if i==0 else first)+'\n\n'+section+rest,encoding='utf-8',newline='\n')
    candidate=ledger['current_integrated_candidate']
    save(ROOT/'checkpoint_receipt.json',dict(checkpoint='V2874',summary=SUMMARY,evidence=evidence,updated_files={str(p):sha(p.read_bytes()) for p in [lp,*docs]},
        new_completed_records=0,new_source_prose_reviews=82,proposed_revisions=63,justified_retentions=19,fresh_reread=2753,fresh_integrated=2671,fresh_pending=82,
        source_prose=2756,completed=2671,historical_revised=1875,historical_retained=796,incomplete_COMMON=3,incomplete_route=82,
        candidate=candidate['path'],candidate_sha256=candidate['sha256'],patch=candidate['patch'],patch_sha256=candidate['patch_sha256'],
        next_requirements=str(requirements),actual_selected_Kuhn_Alliance_IDs=[],new_emulator_runs=0,goal_turn_classification='progress',all_jobs_terminal=True,full_goal_complete=False))
    print('V2874:82new contextual/native reviews;63revisions/19retentions.2753reread/2671integrated/82pending;source-prose2756. V2840unchanged;full goal active.')
