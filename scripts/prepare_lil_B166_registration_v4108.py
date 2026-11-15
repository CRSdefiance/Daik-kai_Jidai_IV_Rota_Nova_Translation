"""Derive negative tests and append-only registration for the complete V4046 stack."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import save

ROOT = Path('work/analysis/lil_B166_registration_tools_v4108')
SOURCE = Path('scripts/register_lil_B164_v4001.py')
TARGET = Path('scripts/register_lil_B166_v4109.py')

if __name__ == '__main__':
    assert not ROOT.exists() and not TARGET.exists()
    text = SOURCE.read_text(encoding='utf-8')
    changes = {
        'lil_B164_editorial_v2':'lil_B166_editorial_v1',
        'lil_B164_registration_v4001':'lil_B166_registration_v4109',
        'all-routes-unified-v4002':'all-routes-unified-v4110',
        'all-routes-unified-v3954':'all-routes-unified-v4046',
        'all_routes_combined_v3954':'all_routes_combined_v4046',
        'lil_B164_editorial_manuscript_v10':'lil_B166_editorial_manuscript_v6',
        'lil_B164_choice_manuscript_v3':'lil_B166_choice_manuscript_v3',
        'lil_B164_editorial_relocation_map_v1':'lil_B166_editorial_relocation_map_v1',
        "prior=read('work/analysis/lil_B161_B163_registration_v3953/registration_receipt.json');assert sha(raw)==prior['registry_after_sha256'] and sha(before)==prior['builder_after_sha256']":
            "assert sha(raw)=="+repr(sha(Path('translations/release_stack.json').read_bytes()))+" and sha(before)=="+repr(sha(Path('scripts/build_integrated_release.py').read_bytes())),
        "registry['latest_promoted_build']['profile']=='all-routes-unified-v1492'":
            "registry['latest_promoted_build']['profile']=='all-routes-unified-v4046'",
        "'dk4tool/patch/lil_B164_editorial_v1.py','scripts/prepare_lil_B164_compiler_v4000.py'":
            "'scripts/prepare_lil_B166_compiler_v4107.py','scripts/prepare_lil_B166_registration_v4108.py'",
        'lil_B164_layout_v2':'lil_B166_layout_v4', 'lil_B164_profile':'lil_B166_profile',
        'lil_B164_reference_approval_v3998':'lil_B166_reference_approval_v4106',
        'lil_B164_loader_v3989/whole_SC2_and_B164_initial_entry_proof':'lil_B166_loader_v4097/whole_SC2_and_B166_initial_entry_proof',
        'lil_B164_transition_review_v3997/both_advice_choices_full_screens_all8_sheets_and_paired_returns_review':
            'lil_B166_transition_review_v4105/both_choices_all7_sheets_Manuel_names_figures_and_paired_returns_review',
        "deps.add(native['choice_review_sheet']['path'])":"deps.add(native['choice_review_sheet']['path']);deps.add(native['actual_menu_review_sheet']['path'])",
        "len(proof['changed_records'])==49":"len(proof['changed_records'])==44",
        'dk4-lil-B164-editorial-release-v1':'dk4-lil-B166-editorial-release-v1',
        "r['source_selector']==13":"r['source_selector']==23", 'source_record_index\']==92':'source_record_index\']==37',
        'all9_source_current_target_nonrelative_nonspeech_nonchoice_leaves':'all11_source_current_target_nonrelative_nonspeech_nonchoice_leaves',
        'actual_Cesare0D_original_nameplate_portrait_and_full_figure_observed':'actual_Manuel17_original_nameplate_portrait_and_full_figure_observed',
        'source_conditions_and_choice_relative_containers_retained_not_flattened':'source_Fernando_query8_relative_containers_choice_and_single_end_retained_not_flattened',
        'actual_selected_B164_source_events=[164]':'actual_selected_B166_source_events=[166]',
        "lambda d:d.update(source_current_progressive_nameplate='Cesare Tohni')":
            "lambda d:d['native_six_consumer_cases']['rows'][4].update(text='Manuel Tohni')",
        "lambda d:d.update(current_full_catalogue_name='Professor Cesare Tony')":
            "lambda d:d['native_six_consumer_cases']['rows'][5].update(text='Professor Manuel Almeida')",
        'native_four_consumer_cases':'native_six_consumer_cases',
        'scoped_current_B164_binding_does_not_close_later_older_record0D_reaudit':'later_older_record0D_reaudit_stays_open',
        'all4_declared_end_decodes_return_type0_extent4_without_post_payload_read':'all2_declared_end_decodes_return_type0_extent4_without_post_payload_read',
        'lil_cesare_advice':'lil_manuel_advice', 'lil_B164_editorial':'lil_B166_editorial',
        'V3954':'V4046', 'B164 must run once':'B166 must run once',
        'build_integrated_release_v4001.tmp':'build_integrated_release_v4109.tmp',
        "promoted_profile_unchanged='all-routes-unified-v1492'":"promoted_profile_unchanged='all-routes-unified-v4046'",
        'expected_manifest_batches=538':'expected_manifest_batches=541',
        'positive_records=49':'positive_records=44','expected_batches=538':'expected_batches=541',
    }
    replacements = []
    for old,new in changes.items():
        assert old in text, old
        text = text.replace(old,new)
        replacements.append(dict(old=old,new=new))
    start = text.index("description='Full V4046 cumulative stack")
    end = text.index("');registry['profiles'][PROFILE]",start)
    text = text[:start]+"description='Full V4046 cumulative stack plus44 contextual Lil B166 Manuel ship-care/recruitment/optional Workroom-advice reviews:24 revisions/20 retentions;42 speeches/two labels,62 commands/eight spans,FI3,one Fernando query,two resources and one late recruitment effect/single end. Four retained-condition B22 cold boots:41 unique/73 observed speeches,both advice choices and normal returns;one Fernando remark offline-only. No natural source-event or earned recruitment claim."+text[end:]
    extra = '''    mutations.extend([
        ('lost_Fernando_pair','relocated_control_proof',lambda d:d['relocated_predicate_pairs'].pop()),
        ('wrong_Fernando_result','relocated_control_proof',lambda d:d['relocated_predicate_pairs'][0]['relocated_case'].update(native_result=[2,9,0,0,0,0])),
        ('missing_source_FI','manuscript',lambda d:next(r for r in d['records'] if '{MACRO:FI}' in r['english']).update(english=next(r for r in d['records'] if '{MACRO:FI}' in r['english'])['english'].replace('{MACRO:FI}','Lil'))),
        ('lost_offline_Fernando','representative_proof',lambda d:d['offline_only_display_IDs'].clear()),
        ('false_actual_Fernando','representative_proof',lambda d:d['offline_only_display_cases'][0].update(actual_display_or_byte_identical_reuse_claim=True)),
        ('wrong_offline_Fernando_actor','representative_proof',lambda d:d['offline_only_display_cases'][0].update(source_selector=2)),
        ('lost_native_Fernando_width','source_nameplate_consumer_proof',lambda d:d.update(original_Fernando_width_forms_preserved_without_name_asset_change=False)),
        ('wrong_single_end_contract','termination_decode_proof',lambda d:d.update(B166_single_end_is_declared_logical_tail=False)),
    ])
'''
    anchor = '    for flag in owned.FLAGS:'
    assert text.count(anchor) == 1
    text = text.replace(anchor,extra+anchor)
    compile(text,str(TARGET),'exec')
    TARGET.write_text(text,encoding='utf-8',newline='\n')
    ROOT.mkdir(parents=True)
    save(ROOT/'source_derivation.json',dict(previous=str(SOURCE),previous_sha256=sha(SOURCE.read_bytes()),
        successor=str(TARGET),successor_sha256=sha(TARGET.read_bytes()),replacements=replacements,
        eight_added_B166_predicate_FI_offline_width_and_single_end_negatives=True,
        current_registry_sha256=sha(Path('translations/release_stack.json').read_bytes()),
        current_builder_sha256=sha(Path('scripts/build_integrated_release.py').read_bytes()),
        no_registration_or_ROM_change_yet=True))
    print('B166 atomic rejection/registration successor created;V4046 main pointer preserved.')
