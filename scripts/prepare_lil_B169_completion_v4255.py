"""Prepare completion producers without reading unfinished build/startup outputs."""
import re
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import save

ROOT = Path('work/analysis/lil_B169_completion_tools_v4255')
if __name__ == '__main__':
    assert not ROOT.exists()
    old = Path('scripts/complete_lil_B168_v4208.py')
    target = Path('scripts/complete_lil_B169_v4255.py')
    assert not target.exists()
    text = old.read_text(encoding='utf-8')
    a,b = text.index('    next_clean = Path('),text.index('    evidence = ',text.index('    next_clean = Path('))
    text = text[:a]+text[b:]
    a,b = text.index('    next_lead = dict('),text.index("    for unit in inventory['broader_coverage_units']:",text.index('    next_lead = dict('))
    text = text[:a]+text[b:]
    changes = {
        'lil_B168_completion_text_v4208':'lil_B169_completion_text_v4255',
        'lil_B168_completion_v4208':'lil_B169_completion_v4255',
        'lil_B168_contextual_final_review':'lil_B169_contextual_final_review',
        'lil_B168_editorial_manuscript_v8':'lil_B169_editorial_manuscript_v5',
        'lil_B168_release_v4205':'lil_B169_release_v4252',
        'lil_B168_startup_v4207':'lil_B169_startup_v4254',
        'lil_B168_actual_v4200/actual_progressive_FE_three_predicates_full_effect_and_return':'lil_B169_actual_v4244/actual_progressive_three_predicates_full_effect_and_return',
        'lil_B168_transition_review_v4201/all9_sheets_contact_FE_source_effect_and_paired_return_review':'lil_B169_transition_review_v4245/all6_sheets_source_effect_and_paired_return_review',
        'lil_B168_checkpoint_v4188':'lil_B169_reference_checkpoint_v4247',
        'lil_B168_registration_v4203':'lil_B169_registration_v4250b',
        'Lil-B168-Mikhail-recruitment-naturalist-item-information54':'Lil-B169-Mikhail-Proof-legend-clues-ruins-tavern-give-and-take36',
        "{'DK4_MES_B168_R0020', 'DK4_MES_B168_R0048', 'DK4_MES_B168_R0135'}":"{'DK4_MES_B169_R0067', 'DK4_MES_B169_R0082', 'DK4_MES_B169_R0097'}",
        "prior['updated_files'][str(path.resolve())]":"prior['updated_files'][str(path)]",
        'all544_manifest_batches_and114_accepted_layers_present':'all545_manifest_batches_and114_accepted_layers_present',
        'all_current_requested_and_final_framebuffers_equal_V4160':'all_current_requested_and_final_framebuffers_equal_V4204',
        'actual_selected_B168_IDs':'actual_selected_B169_IDs',
        "== 51":"== 33","== 57":"== 55","== 54":"== 36",
        "{'revise': 28, 'retain-wording': 26}":"{'revise': 19, 'retain-wording': 17}",
        '[168]':'[169]','block=168':'block=169','actual_source_event168_selected':'actual_source_event169_selected',
        'len(old_keys) == 5602':'len(old_keys) == 5656',
        '(5656, 5602, 54)':'(5692, 5656, 36)',
        '5659':'5695','3803':'3839',
        '# Current editorial handoff - V4188':'# Current editorial handoff - V4247',
        'revised=28, retained=26':'revised=19, retained=17',
        'source_prose_credit_already_recorded_in_V4188':'source_prose_credit_already_recorded_in_V4231',
        'all54_exact_source_predecessor_runtime_logical_and_integrated_references_bound':'all36_exact_source_predecessor_runtime_logical_and_integrated_references_bound',
        'blocks=[168]':'blocks=[169]',
        'revised_count=28, retained_count=26, fresh_revisions=28, fresh_retentions=26':'revised_count=19, retained_count=17, fresh_revisions=19, fresh_retentions=17',
        'records_editorially_completed=5656, records_revised_and_integrated=3595, retained_wordings_editorially_completed=2061':'records_editorially_completed=5692, records_revised_and_integrated=3614, retained_wordings_editorially_completed=2078',
        '5656 fresh contextual rereads integrated;source/prose5659. Remaining267 physical B169-B180':'5692 fresh contextual rereads integrated;source/prose5695. Remaining231 physical B170-B180',
        'fresh_pass_records_integrated=5656':'fresh_pass_records_integrated=5692',
        'records=54, final_review=str(FINAL), new_revisions=28, justified_retentions=26':'records=36, final_review=str(FINAL), new_revisions=19, justified_retentions=17',
        'new_completed_records=54':'new_completed_records=36',
        'dict(revised=28, retained=26)':'dict(revised=19, retained=17)',
        'actual_selected_B168_source_events':'actual_selected_B169_source_events',
        'reviewed_route_records=4057, completed_route_records=4057':'reviewed_route_records=4093, completed_route_records=4093',
        'completion_credit_added=54':'completion_credit_added=36',
        "['lil_B168_v4188']":"['lil_B169_v4231']",
        'complete-through-V4208':'complete-through-V4255',
        "['lil_B168_v4208']":"['lil_B169_v4255']",
        'all54-source-native-reference-representative-release-checks-pass':'all36-source-native-reference-representative-release-checks-pass',
        "ledger['unfinished_editorial_scope_v4188']":"ledger['unfinished_editorial_scope_v4247']",
        'lil_B168_completed_v4208':'lil_B169_completed_v4255','completed_targets=54':'completed_targets=36',
        'actual_unique_speeches=51, actual_FE_panels=3':'actual_unique_speeches=33, actual_FE_panels=0',
        'no_B168_command_omitted_in_content_fixtures':'no_B169_command_omitted_in_content_fixtures',
        'unfinished_editorial_scope_v4208':'unfinished_editorial_scope_v4255',
        'remaining_B169_B180_physical_speeches=267':'remaining_B170_B180_physical_speeches=231',
        'len(keys) == 5656':'len(keys) == 5692',
        "'promoted_main_build_v4186']":"'promoted_main_build_v4186', 'promoted_main_build_v4226']",
        '## V4208: 54 Lil B168 reviews completed in V4204':'## V4255:36 Lil B169 reviews completed in V4251',
        '# Current editorial handoff - V4208':'# Current editorial handoff - V4255',
        "checkpoint='V4208'":"checkpoint='V4255'",
        'fresh_reread=5656, fresh_integrated=5656':'fresh_reread=5692, fresh_integrated=5692',
        'completed=5656, historical_revised=3595, historical_retained=2061':'completed=5692, historical_revised=3614, historical_retained=2078',
        'manifest_batches=544':'manifest_batches=545',
        'actual_unique_speech_panels=51, actual_FE_panels=3':'actual_unique_speech_panels=33, actual_FE_panels=0',
        'V4208 completion staged':'V4255 completion staged',
    }
    for item in changes:
        assert item in text,item
    text = re.sub('|'.join(re.escape(k) for k in sorted(changes,key=len,reverse=True)),lambda m:changes[m.group()],text)
    # The source and exact operand amendment remain bound in the completed record set.
    needle = "Path(doc['representative_proof']), Path(doc['final_padding_proof']), Path(doc['source_nameplate_consumer_proof']),"
    assert text.count(needle)==1
    text = text.replace(needle,needle+" Path(doc['source_effect_operand_notation_amendment']),")
    compile(text,str(target),'exec')
    target.write_text(text,encoding='utf-8',newline='\n')
    tools = [dict(previous=str(old),previous_sha256=sha(old.read_bytes()),successor=str(target),successor_sha256=sha(target.read_bytes()))]
    tools.append(derive('scripts/seal_lil_B168_completion_v4208.py','scripts/seal_lil_B169_completion_v4255.py',{
        'lil_B168_completion_v4208':'lil_B169_completion_v4255',
        '(5656, 5656, 0)':'(5692, 5692, 0)',
        '(5659, 5656, 3595, 2061)':'(5695, 5692, 3614, 2078)',
        'V4208 completion sealed:5656 integrated,54 B168 completions,source/prose5659 unchanged.':'V4255 completion sealed:5692 integrated,36 B169 completions,source/prose5695 unchanged.',
    }))
    ROOT.mkdir(parents=True)
    save(ROOT/'source_derivation.json',dict(tools=tools,no_completion_orcredit_claim_before_execution=True,
        expected_final_counts=dict(fresh=5692,integrated=5692,pending=0,source_prose=5695,revised=3614,retained=2078),full_goal_complete=False))
    print('B169 completion/seal producers prepared;execution requires successful registered release/startup receipts.')
