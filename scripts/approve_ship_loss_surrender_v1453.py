"""Native-approve24 source-faithful reports;registered/original-event gates stay open."""
from copy import deepcopy
from pathlib import Path
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.patch.grand_race_menu_release import sha
from scripts.ship_loss_surrender_native_plan_v1447 import compiled,IDS
from scripts.verify_village_wrap_v608 import read,save

ROOT = Path('work/analysis/ship_loss_surrender_native_review_v1453')
OLD = Path('translations/ship_loss_surrender_editorial_manuscript_v2.json')
NEW = Path('translations/ship_loss_surrender_editorial_manuscript_v3.json')

if __name__=='__main__':
    assert not ROOT.exists() and not NEW.exists()
    doc = read(OLD)
    fonts_path = Path('work/analysis/ship_loss_surrender_fonts_v1448/native_font_research.json')
    copies_path = Path('work/analysis/ship_loss_surrender_copies_v1451/all_native_copies_and_prefix_cache_sequence.json')
    escape_path = Path('work/analysis/ship_loss_surrender_escape_v1452/original_direct_escape_regression.json')
    runtime_path = Path('work/analysis/ship_loss_surrender_runtime_v1443b/native_runtime_verification.json')
    fonts,copies,escape,runtime = [read(p) for p in [fonts_path,copies_path,escape_path,runtime_path]]
    plan = read('work/analysis/ship_loss_surrender_payload_v1447/native_payload_plan.json')
    assert fonts['manuscript_sha256']==sha(OLD.read_bytes()) and len(fonts['cases'])==624 and not fonts['findings']
    assert len(fonts['all618_source_existing_actor_choices'])==618 and len(fonts['invalid_compiler_inputs_rejected'])==15
    assert len(fonts['CPU_only_role_counterfactuals_entire4MiB_audited'])==7
    assert copies['complete_native_copies']==7336 and len(copies['sequenced_cache_cases'])==180
    assert len(escape['all13_original_direct_pipeline_cases'])==13
    assert all(p['ARM9_sha256']==fonts['ARM9_sha256'] and p['COMMON_sha256']==fonts['COMMON_sha256'] for p in [copies,escape])
    assert runtime['native_exact_dispatch_ABI_memory_and_external_reference_proven']
    assert read('work/analysis/ship_loss_surrender_runtime_v1443b/scope_proof.json')['total_cases']==529364
    assert plan['actual_changed_message_IDs']==list(IDS)
    assert plan['shared_balance_literal_status_fonts_sections_BSS_cache_arena_ITCM_staged123040_exact']
    assert plan['runtime_plan']['owned_table_bytes']==188 and plan['runtime_plan']['encoded_table_bytes']==180
    assert plan['runtime_plan']['owned_gate_bytes']==172 and plan['runtime_plan']['native_gate_bytes']==168
    previews = []
    for case in fonts['cases']:
        assert case['full228x64_native_and_independent_font_exact']
        assert case['complete_name_leading_trailing_letters_uniform6px_margin_bounds_and_blank_paper_pass']
        assert not case['findings']
        if case['preview']:
            path = Path(case['preview']);assert sha(path.read_bytes())==case['preview_sha256']
            previews.append({'path':str(path),'sha256':case['preview_sha256']})
    assert len(previews)==192
    for sheet in fonts['sheets_for_visual_review']:
        assert sha(Path(sheet['path']).read_bytes())==sheet['sha256']
    ROOT.mkdir(parents=True)
    visual = ROOT/'visual_and_native_review.json'
    save(visual,{'all8_sheets_and192_native_panels_actually_visually_reviewed':True,
        'sheets':fonts['sheets_for_visual_review'],'previews':previews,
        'all624_native_fonts_margins_bounds_first_final_letters_and_blank_paper_pass':True,
        'all_ship_name_bytes_literal_after_original_printf':True,
        'no_isolated_non_name_final_word_or_weak_line_ending_remaining':True,
        'twenty_natural_address_moves_keep_identical_paragraph_byte_lengths':True,
        'white_flag_apparent_surrender_and_reportative_source_facts_preserved':True,
        'all_prior_scopes_and_shared_balance_literal_live_status_helpers_preserved':True,
        'only_three_proven_role_table_memberships_added_inside_existing188_172_spans':True,
        'registered_ROM_loading_GPU_and_original_loss_surrender_dismissal_return_still_pending':True,
        'producer_sha256':sha(Path(__file__).read_bytes()),'completed_entries_added':0,'full_goal_complete':False})
    native = deepcopy(doc)
    native.update(formatting_review_pending=False,status='24-loss-surrender-source-native-approved;registered-integration-original-events-pending',
        reviewed_research_manuscript=str(OLD),reviewed_research_manuscript_sha256=sha(OLD.read_bytes()),
        native_font_proof=str(fonts_path),native_font_proof_sha256=sha(fonts_path.read_bytes()),
        native_copy_proof=str(copies_path),native_copy_proof_sha256=sha(copies_path.read_bytes()),
        escape_regression_proof=str(escape_path),escape_regression_proof_sha256=sha(escape_path.read_bytes()),
        native_runtime_proof=str(runtime_path),native_runtime_proof_sha256=sha(runtime_path.read_bytes()),
        visual_review=str(visual),visual_review_sha256=sha(visual.read_bytes()))
    for row in native['records']:
        row['review']['formatting'] = True;row['compiled_hex'] = compiled(row).hex()
        row['status'] = 'native-approved;registered-integration-and-original-events-pending'
    validate_natural_dialogue_batch(native);save(NEW,native)
    ledger_path = Path('translations/editorial_review_current_v1.json');ledger = read(ledger_path);before = deepcopy(ledger)
    assert (ledger['records_editorially_completed'],ledger['records_with_source_and_prose_pass'])==(1323,1435)
    assert len(ledger['reviewed_but_incomplete_COMMON_IDs'])==112 and set(IDS)<=set(ledger['reviewed_but_incomplete_COMMON_IDs'])
    save(ROOT/'coverage_before_native_approval.json',before)
    drafts = ledger['active_source_prose_drafts'];assert str(OLD) in drafts['manuscripts'] and str(NEW) not in drafts['manuscripts']
    drafts['manuscripts'].append(str(NEW));drafts['manuscript_record_subsets_pending'][str(OLD)] = []
    drafts['manuscript_record_subsets_pending'][str(NEW)] = list(IDS)
    drafts['note'] = 'Loss/surrender24 is source/native-approved,including624 complete original font/name cases and visual review. It remains incomplete for registered ROM/exact patch/startup and representative original own-capture,own-surrender,enemy-surrender events,dismissals and transitions.16 sinking,34 aftermath38 older reviewed entries and broader shared/routes/raw prose remain open.'
    unit = next(u for u in ledger['coverage_units'] if u['id']=='Shared-ship-loss-surrender24-source-prose')
    unit.update(status='source-native-approved-registered-integration-original-events-pending',
        native_approved_manuscript=str(NEW),native_visual_review=str(visual))
    ledger['formatting_watchlist']['ship_loss_surrender_research'].update(native_approved_manuscript=str(NEW),
        visual_review=str(visual),all192_native_preview_panels_visually_reviewed=True,layout_findings_remaining=0,
        native_copy_cache_and_escape_regressions_pass=True,registered_ROM_repair_and_original_events_still_pending=True)
    summary = ('V1453 native-approves24 source-reviewed loss/surrender reports2074-2081/2090-2105,all proposed '
        'revisions,without completion credit.624 original role1/printf/macro/wrap/full228x64 independent '
        'font cases pass with literal complete names,uniform6px visible margins,bounds and zero remaining '
        'orphan/weak-end findings. All8 sheets/192 preview panels are actually inspected.20 natural '
        'end-position Admiral addresses retain identical paragraph byte lengths and preserve all source '
        'facts,white-flag observation,appearance qualifiers and2104 hearsay.618 existing actor/table '
        'choices,7 one-byte fully4MiB-audited CPU role counterfactuals and15 rejected compiler inputs '
        'are documented;no individual loss/surrender gameplay activation.529364 exact original-entry '
        'selector/ABI/guard cases,7336 full native copies180 cache sequences13 earlier direct escape '
        'pipelines pass. Existing188-byte table(180 encoded),172-byte gate(168 code),all earlier '
        'formatter/status code,3644 other message/copy spans,39 other blocks,sections/BSS/cache/arena/'
        'ITCM and123040 staged bytes are preserved. Native metadata respects COMMON22/23 boundary. '
        'The rejected768 collision and single-block assumption produced no output;780 bias and exact '
        'two-block successor are proved. Manuscriptv3 has per-record natural-dialogue-v2 gates. '
        'Registered complete-stack ROM,exact clean-input patch,ordinary startup and representative '
        'original own-capture/own-surrender/enemy-surrender events,visible text,dismissals and return '
        'remain pending. No Hull/crew/RNG/result edits or numerical emulator message injection are '
        'authorized by this proof. Counts remain1323 complete(985 revised338 retained),1435 source/prose,'
        '112 reviewed-incomplete COMMON(24 loss/surrender16 sinking34 aftermath38 older),plus broader '
        'shared/routes/raw prose. V1430 remains current playable/native parent without these research '
        'changes. Canonical,V997,separate graphics/all18 plaques and later older-record re-audit '
        'remain unchanged/open;goal active.')
    ledger['latest_checkpoint'] = summary
    ledger['research_checkpoints'].append({'id':'V1453-loss-surrender24-native-approved',
        'manuscript':str(NEW),'native_fonts':str(fonts_path),'native_copy':str(copies_path),
        'escape_regression':str(escape_path),'visual_review':str(visual),'completed_entries_added':0,
        'source_prose_reviews_added':0,'full_goal_complete':False})
    for key in ['records_editorially_completed','records_revised_and_integrated','retained_wordings_editorially_completed',
        'records_with_source_and_prose_pass','records_with_source_prose_drafts','source_prose_reviewed_counts_by_file',
        'reviewed_but_incomplete_COMMON_IDs','completed_editorial_record_counts_by_file','current_integrated_candidate',
        'current_native_relocation_reference','source_pins','unresolved_graphics_work','older_record_reaudit_after_full_editorial_goal','raw_source_coverage_revisit']:
        assert ledger[key]==before[key],key
    save(ledger_path,ledger)
    document = Path('docs/ship_loss_surrender_v1453_native_checkpoint.md');assert not document.exists()
    document.write_text('# V1453 loss and surrender24 native approval\n\n'+summary+
        '\n\n## Next required work\n\nUse `translations/ship_loss_surrender_editorial_manuscript_v3.json` '
        'and `scripts/ship_loss_surrender_native_plan_v1447.py` for a registered full V1430 successor. '
        'Bind every frozen source/prose/runtime/font/copy/escape proof,keep the optional builder stage '
        'removable,and verify all earlier accepted layers and exact clean-input patch reconstruction. '
        'Then complete ordinary cold-boot controls and representative original events for each of the '
        'three separate report families. Preserve original72484 surrender probability and party/slot/'
        'flagship branches. Source code and CPU counterfactuals do not establish an earned gameplay '
        'capture/surrender,dismissal or return. Source/native approval adds no completion credit.\n',encoding='utf-8')
    for name in ['translation_progress.md','known_issues.md','todo.md','editorial_review_goal.md']:
        with (Path('docs')/name).open('a',encoding='utf-8',newline='\n') as handle:
            handle.write('\n\n## V1453 loss/surrender24 native approval\n\n'+summary+
                '\n\nSee [checkpoint](ship_loss_surrender_v1453_native_checkpoint.md).\n')
    save(ROOT/'native_approval_receipt.json',{'native_approved_manuscript':str(NEW),
        'manuscript_sha256':sha(NEW.read_bytes()),'native_font_cases':624,'visual_panels':192,
        'native_dispatch_ABI_cases':529364,'complete_native_copies':7336,'cache_sequences':180,'escape_cases':13,
        'completed':1323,'source_prose':1435,'reviewed_incomplete_COMMON':112,
        'completed_entries_added':0,'source_prose_reviews_added':0,
        'registered_release_and_original_events_pending':True,'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    print('24 reports source/native-approved;624 fonts,192 visual panels,7336 copies and13 escapes pass. Integration and original events pending.',flush=True)
