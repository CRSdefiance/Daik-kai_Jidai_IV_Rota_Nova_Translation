"""Native-approve32 reactions;registered integration and original scenes stay open."""
from copy import deepcopy
from pathlib import Path
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.patch.grand_race_menu_release import sha
from scripts.battle_reaction_native_plan_v1484 import compiled,IDS
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/battle_reaction_native_review_v1489')
OLD=Path('translations/battle_reactions_editorial_manuscript_v1.json')
NEW=Path('translations/battle_reactions_editorial_manuscript_v2.json')

if __name__=='__main__':
    assert not ROOT.exists() and not NEW.exists()
    doc=read(OLD)
    font_path=Path('work/analysis/battle_reaction_fonts_v1486/native_font_research.json')
    copy_path=Path('work/analysis/battle_reaction_copies_v1487/all_native_copies_and_prefix_cache_sequence.json')
    escape_path=Path('work/analysis/battle_reaction_escape_v1488/original_direct_escape_regression.json')
    runtime_path=Path('work/analysis/battle_reaction_runtime_v1485/native_runtime_verification.json')
    fonts,copies,escape,runtime=[read(p) for p in [font_path,copy_path,escape_path,runtime_path]]
    assert fonts['manuscript_sha256']==sha(OLD.read_bytes()) and len(fonts['cases'])==32 and not fonts['findings']
    assert len(fonts['all824_existing_actor_choices'])==824 and len(fonts['invalid_compiler_inputs_rejected'])==14
    assert copies['complete_native_copies']==7336 and len(copies['sequenced_cache_cases'])==180
    assert len(escape['all13_original_direct_pipeline_cases'])==13
    assert all(p['ARM9_sha256']==fonts['ARM9_sha256'] and p['COMMON_sha256']==fonts['COMMON_sha256'] for p in [copies,escape])
    assert runtime['native_exact_dispatch_ABI_memory_and_external_reference_proven']
    assert read('work/analysis/battle_reaction_runtime_v1485/scope_proof.json')['total_cases']==529416
    plan=read('work/analysis/battle_reaction_payload_v1484/native_payload_plan.json')
    assert plan['runtime_plan']['encoded_table_bytes']==184 and plan['runtime_plan']['original172_byte_gate_exact']
    assert plan['all3652_unselected_or_retained_texts_and_native_copy_spans_preserved']
    assert plan['shared_balance_literal_status_fonts_sections_BSS_cache_arena_ITCM_staged123040_exact']
    for case in fonts['cases']:
        assert case['full228x64_native_and_independent_font_exact']
        assert case['complete_first_final_letters_uniform6px_margins_bounds_and_blank_paper_pass']
        assert not case['findings'] and sha(Path(case['preview']).read_bytes())==case['preview_sha256']
    for sheet in fonts['sheets_for_visual_review']:assert sha(Path(sheet['path']).read_bytes())==sheet['sha256']
    ROOT.mkdir(parents=True);visual=ROOT/'all32_native_visual_review.json'
    save(visual,{'sheets':fonts['sheets_for_visual_review'],'all2_sheets_and32_native_panels_actually_visually_reviewed':True,
        'all32_full_glyph_planes_uniform6px_margins_complete_first_final_letters_bounds_and_blank_paper_pass':True,
        'two_line2161_break_preserves_complete_piece_of_cake_phrase_and_equal_visible_margin':True,
        'all32_original_actor_speech_contracts_and824_existing_actor_choices_proved':True,
        'remaining_layout_findings':0,'registered_ROM_original_scene_GPU_dismissal_and_transition_still_pending':True,
        'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    native=deepcopy(doc)
    native.update(formatting_review_pending=False,status='32-source-native-approved;registered-release-original-scenes-pending',
        reviewed_research_manuscript=str(OLD),reviewed_research_manuscript_sha256=sha(OLD.read_bytes()),
        native_font_proof=str(font_path),native_font_proof_sha256=sha(font_path.read_bytes()),
        native_copy_proof=str(copy_path),native_copy_proof_sha256=sha(copy_path.read_bytes()),
        escape_regression_proof=str(escape_path),escape_regression_proof_sha256=sha(escape_path.read_bytes()),
        native_runtime_proof=str(runtime_path),native_runtime_proof_sha256=sha(runtime_path.read_bytes()),
        visual_review=str(visual),visual_review_sha256=sha(visual.read_bytes()))
    for row in native['records']:
        row['review']['formatting']=True;row['compiled_hex']=compiled(row).hex()
        row['status']='native-approved;registered-release-and-original-scenes-pending'
    validate_natural_dialogue_batch(native);save(NEW,native)
    ledger_path=Path('translations/editorial_review_current_v1.json');ledger=read(ledger_path);before=deepcopy(ledger)
    assert (ledger['records_editorially_completed'],ledger['records_with_source_and_prose_pass'],len(ledger['reviewed_but_incomplete_COMMON_IDs']))==(1323,1467,144)
    save(ROOT/'coverage_before_native_approval.json',before)
    drafts=ledger['active_source_prose_drafts'];assert str(NEW) not in drafts['manuscripts']
    drafts['manuscripts'].append(str(NEW));drafts['manuscript_record_subsets_pending'][str(OLD)]=[]
    drafts['manuscript_record_subsets_pending'][str(NEW)]=list(IDS)
    drafts['note']='32 reactions are source/native-approved,including all32 full glyph planes and visual review,but need registered full-stack integration and representative original scenes/dismissals/return.24 loss/surrender are integrated in V1456 with original events pending.16 sinking,34 aftermath38 older and broader shared/routes/raw prose remain open.'
    unit=next(u for u in ledger['coverage_units'] if u['id']=='Shared-battle-reactions32-source-prose')
    unit.update(status='source-native-approved-registered-release-original-scenes-pending',native_approved_manuscript=str(NEW),native_visual_review=str(visual))
    ledger['formatting_watchlist']['battle_reactions32'].update(native_approved_manuscript=str(NEW),native_font_evidence=str(font_path),
        native_visual_review=str(visual),all32_panels_visually_reviewed=True,remaining_layout_findings=0,
        ordinary_ASCII_I_postmacro_wrap_native_font_and_margin_checks_pending=False,
        native_copy_cache_escape_and_dispatch_ABI_regressions_pass=True,
        all_native_font_visual_copy_cache_registered_release_and_original_scene_gates_open=False,
        registered_release_and_original_scene_gates_open=True)
    summary=('V1489 native-approves32 source-reviewed battle reactions2147-2178:16 proposed revisions16 retentions, '
        'without completion credit. All32 original actor-selection/printf/macro/post-expansion-wrap/full228x64 '
        'glyph planes match independent font rendering,ordered complete letters,uniform6px margins,bounds '
        'and blank paper. Both sheets/all32 panels are visually reviewed;2161 keeps piece of cake together '
        'on the aligned second line. No layout findings remain;14 invalid compiler inputs are rejected. '
        'All824 existing actor/table choices and source callback/surprise/injury branches are preserved; '
        'native probes do not establish all stored alternatives reachable through one callback. Four new '
        'actor memberships fit184 of188 selector bytes;the172-byte gate is byte-exact.529416 original-entry '
        'dispatch/ABI/guard cases,7336 complete native copies180 cache sequences13 prior direct escape '
        'pipelines pass. All3652 unselected/retained text and copy spans,40 other blocks,opaque duel prefix, '
        'earlier helpers,sections/BSS/cache/arena/ITCM and123040 staged bytes remain exact. Manuscriptv2 '
        'has all per-record natural-dialogue-v2 gates;registered full-stack ROM/exact patch,ordinary '
        'startup and representative original scene/display/dismissal/transition gates remain pending. '
        'Counts1323 complete(985 revised338 retained),1467 source/prose,144 reviewed-incomplete COMMON '
        '(32 reactions24 loss/surrender16 sinking34 aftermath38 older),plus broader shared/routes/raw prose. '
        'V1456 remains latest registered experimental integration,V1430 completed-native reference. '
        'Canonical,V997,separate graphics/all18 plaques and later older-record re-audit unchanged/open;goal active.')
    ledger['latest_checkpoint']=summary
    ledger['research_checkpoints'].append({'id':'V1489-battle-reactions32-native-approved','manuscript':str(NEW),
        'proof':str(ROOT/'native_approval_receipt.json'),'completed_entries_added':0,'source_prose_reviews_added':0,'full_goal_complete':False})
    for key in ['records_editorially_completed','records_revised_and_integrated','retained_wordings_editorially_completed',
        'records_with_source_and_prose_pass','reviewed_but_incomplete_COMMON_IDs','completed_editorial_record_counts_by_file',
        'current_integrated_candidate','current_native_relocation_reference','source_pins','unresolved_graphics_work',
        'older_record_reaudit_after_full_editorial_goal','raw_source_coverage_revisit']:
        assert ledger[key]==before[key],key
    save(ledger_path,ledger)
    document=Path('docs/battle_reactions_v1489_native_checkpoint.md');assert not document.exists()
    document.write_text('# V1489 battle reaction native approval\n\n'+summary+'\n\n'
        '## Next required work\n\nRegister the exact native-approved manuscript and frozen source/runtime/font/'
        'copy/cache/escape/visual proofs as a full V1456 successor. Preserve its24 pending loss/surrender '
        'reports and every accepted layer. Verify the exact clean-input reconstructable patch and ordinary '
        'cold boots,then representative original battle-setup,surprise and wound reaction scenes with '
        'normal dismissal and following scene. Do not force RNG or injuries or inject numerical messages. '
        'The selected64-bit/table scopes and CPU font planes are not GPU/gameplay event evidence.\n',encoding='utf-8')
    for name in ['translation_progress.md','known_issues.md','todo.md','editorial_review_goal.md']:
        with (Path('docs')/name).open('a',encoding='utf-8',newline='\n') as f:
            f.write('\n\n## V1489 battle reactions32 native approval\n\n'+summary+'\n\nSee [checkpoint](battle_reactions_v1489_native_checkpoint.md).\n')
    save(ROOT/'native_approval_receipt.json',{'native_approved_manuscript':str(NEW),'manuscript_sha256':sha(NEW.read_bytes()),
        'native_font_cases':32,'visual_panels':32,'native_dispatch_ABI_cases':529416,'complete_native_copies':7336,
        'cache_sequences':180,'escape_cases':13,'completed':1323,'source_prose':1467,'reviewed_incomplete_COMMON':144,
        'completed_entries_added':0,'source_prose_reviews_added':0,'registered_release_and_original_scenes_pending':True,
        'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    print('32 source/native-approved reactions;all32 glyphs/visuals,529416 dispatch cases,7336 copies/180 cache/13 escapes pass. Integration/events pending.')
