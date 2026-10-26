"""Record source-bound branch/native research and the remaining real FE metric gap."""
from copy import deepcopy
from pathlib import Path
import os

from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_lesson_native_checkpoint_v1727b')
FONTS=Path('work/analysis/lil_lesson_layout_v1725/all60_native_font_reconciliation.json')
ACTUAL=Path('work/analysis/lil_lesson_context_audit_v1726c/terminal_original_wind_branch_and_FE_context.json')
BRANCH=Path('work/analysis/lil_lesson_branches_v1722/original_relative_skip_operand_proof.json')
DOC=Path('translations/lil_lessons_editorial_manuscript_v2.json')


if __name__=='__main__':
    assert not ROOT.exists()
    font,actual,branch,doc=map(read,(FONTS,ACTUAL,BRANCH,DOC))
    assert len(font['cases'])==60 and len(font['FE_dispatch_cases'])==9
    assert len(branch['cases'])==360 and len(branch['operands_requiring_adjustment_when_resizing'])==36
    assert sha(DOC.read_bytes())==font['manuscript_sha256']
    assert actual['terminal_frame']==29930 and actual['all_source_observer_callbacks']==262
    assert actual['ordinary_wind_option1_selected_and_original_relative_skips4_140_observed']
    assert actual['original_B120_completed_and_returned_to_Sea_View_with_departure_log']
    assert len(actual['current_FE_font_model_findings'])==5
    assert actual['source_observer_errors_mismatches_zero_host_slots_restored']
    assert actual['font_research_alignment_address_metadata_erratum']['source_derived']==0x0239B104
    for p in font['review_sheets']:
        assert sha(Path(p['path']).read_bytes())==p['sha256']
    ledger_path=Path('translations/editorial_review_current_v1.json');raw=ledger_path.read_bytes();ledger=read(ledger_path);before=deepcopy(ledger)
    assert (ledger['records_editorially_completed'],ledger['records_with_source_and_prose_pass'])==(1424,1632)
    assert sha(Path(actual['candidate']).read_bytes())==actual['candidate_sha256']==ledger['current_integrated_candidate']['sha256']
    ROOT.mkdir(parents=True);save(ROOT/'coverage_before_checkpoint.json',before)
    save(ROOT/'native_visual_review_and_unresolved_FE_metric.json',{
        'all8_original_native_sheets60_panels_actually_viewed':True,
        'refined_sheet05_actually_viewed':True,'one_refinement':'B23R69 now states the complete Half Open rule in two lines;no isolated final adverb.',
        'no_dropped_leading_trailing_characters_or_bounds_failures_in_isolated_native_planes':True,
        '51_progressive_font_planes_verified_and_9_FE_planes_complete_under_explicit_model_initialization':True,
        'FE_model_not_yet_actual_multiline_geometry_approval':True,
        'five_multiline_current_FE_actual_ink_checks_disagree_with_model':actual['current_FE_font_model_findings'],
        'runtime_font_cell_metrics_from_captured_RAM':[6,12],
        'isolated_model_FE_row_advance12_actual_observed_row_advance16_requires_source_bound_context_resolution':True,
        'do_not_shift_pixels_to_fit_tested_glyphs_or_claim_game_defect_from_model_mismatch':True,
        'formatting_approval_registered_relocation_choice_layout_integration_and_revised_gameplay_pending':True,
        'source_native_proof':str(FONTS),'source_native_proof_sha256':sha(FONTS.read_bytes()),
        'actual_proof':str(ACTUAL),'actual_proof_sha256':sha(ACTUAL.read_bytes()),'full_goal_complete':False})
    drafts=ledger['active_source_prose_drafts'];old=next(k for k in drafts['route_record_subsets_pending'] if k.replace('\\','/')=='translations/lil_lessons_editorial_manuscript_v1.json')
    assert len(drafts['route_record_subsets_pending'][old])==60
    drafts['route_record_subsets_pending'][old]=[]
    drafts['route_record_subsets_pending'][str(DOC)]=[r['id'] for r in doc['records']]
    drafts['manuscripts'].append(str(DOC))
    unit=next(u for u in ledger['coverage_units'] if u['id']=='Lil-sailing-lessons64-source-prose')
    unit.update(manuscripts=[str(DOC),'translations/lil_lesson_choices_editorial_draft_v1.json'],
        status='source-prose-native-branch-and-isolated-font-reviewed;actual-FE-metrics-choice-layout-map-release-pending',
        native_branch_proof=str(BRANCH),native_font_research=str(FONTS),current_original_scene_proof=str(ACTUAL))
    ledger['lil_lessons_editorial_v1720'].update(speech_manuscript=str(DOC),native_branch_proof=str(BRANCH),
        native_font_research=str(FONTS),current_original_scene_proof=str(ACTUAL),
        all9_FE_dispatch_paths_source_verified=True,FE_actual_multiline_geometry_pending=True)
    ledger['formatting_watchlist']['Lil_sailing_lessons64'].update(
        status='all64-open;51-progressive-fonts-pass;9-FE-actual-context-metric-and-choice-layout-pending',
        manuscripts=[str(DOC),'translations/lil_lesson_choices_editorial_draft_v1.json'],
        all60_native_isolated_planes_and_9_FE_dispatch_paths_verified=True,
        source_bound_relative_skip_sites36_and360_native_cases=True,
        actual_original_B120_wind_option1_and_normal_return_verified=True,
        current_multiline_FE_actual_model_mismatch_not_inferred_game_defect=True,
        failed_research_metadata_alignment_address3_corrected_to_source_0239B104=str(ACTUAL))
    ledger['next_route_scene_editorial_packet'].update(manuscripts=[str(DOC),'translations/lil_lesson_choices_editorial_draft_v1.json'],
        note='Next resolve actualFE modal context line gap:font cells6x12,but current multiline actual rows16 versus isolatedmodel12. Then choice label layout,complete source-bound relative/external reference map,registered integration/exactpatch,andactualrevisedbranches. Do not resume terminal29930 or repeat B22.')
    summary=('V1727 advances Lil lesson64 native review without completion credit. All36 original0100/0200/0300 relative skip sites pass360 clean/current previous-result cases;destinations are mapped native boundaries relative to command+4. '
        'All60 draft paragraphs pass native catalog/macro alignment and complete native/independent font planes under explicit initialization;51 spoken and9 FE modal cases. All8 sheets60 panels andrefined sheet05 actually viewed. '
        'B23R69 is recast as the faithful two-line Half Open rule;59 other planes unchanged. No source facts shortened for capacity. '
        'Original FE dispatcher selects5473C with selector254;the current decoder independently supplies254. Existing ITCM01FFCE40,alignment0239B104 andbuffered cursor helpers remain byte-exact. '
        'V1724/b lacked existing helper initialization and were rejected;V1724c models exact source helpers. Its address report alone was overwritten to3 by an alignment loop;the execution environment already held0239B104 andwas correct. V1726c records the source-derived erratum. '
        'Ordinary no-save/no-fixture registeredV1711 cold boot ends29930 after selecting wind option1,native relative skips4/140,all6 B120 FE panels andnormal Sea View with departure log. 262 read-only callbacks,zero errors/mismatches,host restoration,input/PNG/4MiB snapshot audits pass. '
        'Original type0 end retains prior choice1 in its unused second word;V1726 rejected an incorrect zero-word assumption. '
        'One single-line FE actual ink plane matches;five multiline actual panels differ from the isolated model. Font cells are6x12;isolated rows12 versus actual observed16 require source-bound live-context resolution. Do not fit positions from tested glyphs,infer a game defect,orgrant FE formatting approval. '
        'All64 drafts remain incomplete,including4 choice labels. No newROM,patch,registry,global profile orrendering code change. Counts1424 complete(1076 revised348 retained),1632 source/prose,144 pendingCOMMON plus64 route drafts andbroader prose. '
        'V1711 remains current experimental,V1492 promoted;full goal active,separate graphics/all18 plaques andlater older-record re-audit remain open.')
    ledger['latest_checkpoint']=summary
    ledger['research_checkpoints'].append({'id':'V1727-Lil-lessons-native-and-current-wind-context',
        'proof':str(ROOT/'checkpoint_receipt.json'),'completed_entries_added':0,'source_prose_reviews_added':0,'full_goal_complete':False})
    for key in ['records_editorially_completed','records_revised_and_integrated','retained_wordings_editorially_completed',
        'records_with_source_and_prose_pass','completed_editorial_record_counts_by_file','source_prose_reviewed_counts_by_file',
        'reviewed_but_incomplete_COMMON_IDs','unresolved_graphics_work','current_integrated_candidate']:
        assert ledger[key]==before[key],key
    assert sum(len(v) for v in drafts['route_record_subsets_pending'].values())==64
    assert ledger['goal_status']=='active' and not ledger['full_goal_complete']
    pending=ledger_path.with_name('editorial_review_current_v1727_pending.json');assert not pending.exists() and ledger_path.read_bytes()==raw
    save(pending,ledger);assert read(pending)==ledger and ledger_path.read_bytes()==raw;os.replace(pending,ledger_path)
    handoff=Path('docs/editorial_handoff_current.md');text=handoff.read_text(encoding='utf-8');save(ROOT/'handoff_before_checkpoint.json',{'text':text,'sha256':sha(handoff.read_bytes())})
    assert text.startswith('# Current editorial handoff - V1720')
    text=text.replace('# Current editorial handoff - V1720','# Current editorial handoff - V1727',1)
    text=text.replace('It remains editorially unreviewed. B23 is a later lesson continuation;','B120/B23 source/prose is reviewed but all64 draft texts remain incomplete. B23 is a later lesson continuation;',1)
    text+='\n\n## Latest authoritative native checkpoint V1727\n\n'+summary+'\n\nCurrent manuscript is translations/lil_lessons_editorial_manuscript_v2.json (60 speech/system records);v1 is frozen/superseded. Four choices stay translations/lil_lesson_choices_editorial_draft_v1.json. Branch proof:'+str(BRANCH)+'. Native planes:'+str(FONTS)+'. Actual source context:'+str(ACTUAL)+'.\n\nNext resolve the FE parent/context line-gap from native live state independently of tested glyphs;do not treat the isolated12px model as real16px display geometry. The isolated helper initialization is documented in work/analysis/lil_lesson_fonts_v1724c/scoped_modal_adapter_source.txt;source alignment entry must be derived from ITCM01FFCF24 tail as0239B104,not stale report3. All51 spoken planes are individually verified;the9 FE planes have complete isolated glyph cells but await actual multiline-context calibration. No native-format approval or relocation map is complete. Choice record count andlabel pointers are mapped;label drawing/bounds andselected revised branches remain open. All36 branch operands must be recomputed when resizing. No global profile changes because V1710 locks existing profile source. Use a scoped source-bound post-layer.\n\nCurrent emulator34065 is TERMINAL29930;all font processes77146/89522/59364 andall other jobs are terminal. Original run captures:E:/Rota Nova translations/Generated/work/emulation_v193/lil_lesson_context_v1723_1711. Runner scripts/run_lil_lesson_context_v1723.py,input replay work/analysis/lil_lesson_context_v1723/ordinary_replay_inputs.json,journal navigation.jsonl. This is current wording context,not revised-scene approval. Full B23/Bruges andevery revised path remain totest. No finalized guide images added from this research.\n'
    handoff.write_text(text,encoding='utf-8')
    Path('docs/lil_lessons_v1727_native_checkpoint.md').write_text('# V1727 Lil lesson native checkpoint\n\n'+summary+'\n\nSee current handoff andcheckpoint receipt for exact dependencies andnext native gate.\n',encoding='utf-8')
    for name in ['translation_progress.md','known_issues.md','todo.md','editorial_review_goal.md']:
        with (Path('docs')/name).open('a',encoding='utf-8') as f:f.write('\n\n## V1727 Lil lesson native/source context\n\n'+summary+'\n\nSee [checkpoint](lil_lessons_v1727_native_checkpoint.md).\n')
    save(ROOT/'checkpoint_receipt.json',{'candidate':actual['candidate'],'candidate_sha256':actual['candidate_sha256'],
        'completed':1424,'source_prose':1632,'new_completed':0,'source_prose_added':0,'all64_lesson_drafts_still_open':True,
        'relative_skip_sites':36,'native_branch_cases':360,'isolated_native_font_cases':60,'actual_original_FE_cases':6,
        'actual_multiline_FE_model_findings':5,'all_current_jobs_terminal':True,'no_ROM_registry_profiles_or_graphics_change':True,
        'proofs':{str(p):sha(p.read_bytes()) for p in [FONTS,ACTUAL,BRANCH,DOC,ROOT/'native_visual_review_and_unresolved_FE_metric.json']},
        'ledger_sha256':sha(ledger_path.read_bytes()),'handoff_sha256':sha(handoff.read_bytes()),
        'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    print('Native checkpoint saved:36 branch sites/360 cases,60 isolated font planes,original wind branch terminal29930;FE actual multiline metric remains open.1424 complete,1632 reviewed;goal active.',flush=True)
