"""Prepare B173 source-bound positive and negative gates before registry mutation."""
from pathlib import Path
import re
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import save

ROOT=Path('work/analysis/lil_B173_registration_tools_v4444')
SOURCE=Path('scripts/register_lil_B172_v4403.py')
TARGET=Path('scripts/register_lil_B173_v4444.py')
if __name__=='__main__':
    assert not ROOT.exists() and not TARGET.exists()
    text=SOURCE.read_text(encoding='utf-8')
    a=text.index('    mutations = [');b=text.index("    for macro in ['FI','FA','FO']:",a)
    text=text[:a]+'''    mutations = [
        ('missing_gate','manuscript',lambda v:v['records'][0]['review'].update(source=False)),
        ('missing_speech','manuscript',lambda v:v['records'].pop()),
        ('wrong_source','manuscript',lambda v:v['records'][0]['source_reference'].update(offset=1)),
        ('wrong_current','manuscript',lambda v:v['records'][0]['current_reference'].update(offset=1)),
        ('wrong_selector','manuscript',lambda v:v['records'][0].update(english='{SPEAKER:CA}Hello.')),
        ('Reika_selector_as_text','manuscript',lambda v:v['records'][1].update(english='Reika says hello.')),
        ('manual_break','manuscript',lambda v:v['records'][0].update(english=v['records'][0]['english']+'{LB}')),
        ('manual_padding','manuscript',lambda v:v['records'][0].update(english=v['records'][0]['english']+'{PAD}')),
        ('missing_relative','reference_map',lambda v:v['blocks'][0]['relative_skip_fixups'].pop()),
        ('wrong_relative_span','reference_map',lambda v:v['blocks'][0]['relative_skip_fixups'][0].update(target_span=2)),
        ('wrong_relative_offset','reference_map',lambda v:v['blocks'][0]['relative_skip_fixups'][0].update(new_offset=0)),
        ('wrong_relative_destination','reference_map',lambda v:v['blocks'][0]['relative_skip_fixups'][0].update(new_matched_skip_target=0)),
        ('missing_target_operand_case','reference_map',lambda v:v['blocks'][0]['target_native_skip_cases'].pop()),
        ('lost_relative_memory_guard','reference_map',lambda v:v['blocks'][0]['target_native_skip_cases'][0].update(ABI_all4MiB_owner_stream_result_length_and_guards_exact=False)),
        ('invented_pause','reference_map',lambda v:v['blocks'][0]['original2000_pause_and_resume_maps'].append({})),
        ('extra_A000','reference_map',lambda v:v['blocks'][0]['mapped_native_commands'].append(dict(word=0xA000))),
        ('missing_end','reference_map',lambda v:v['blocks'][0]['original_declared_end_word_maps'].pop()),
        ('wrong_end','reference_map',lambda v:v['blocks'][0]['original_declared_end_word_maps'][0].update(target_offset=0)),
        ('wrong_entry','reference_map',lambda v:v.update(entry_point_offset=10)),
        ('invented_choice','reference_map',lambda v:v['blocks'][0]['choice_commands'].append({})),
        ('wrong_command','reference_map',lambda v:v['blocks'][0]['mapped_native_commands'][0].update(new_offset=10)),
        ('wrong_command_word','reference_map',lambda v:v['blocks'][0]['mapped_native_commands'][0].update(word=0x6001)),
        ('wrong_resource_extent','reference_map',lambda v:v['blocks'][0]['mapped_native_commands'][1].update(old_native_extent=4)),
        ('missing_native_plane','native_font_proof',lambda v:v['cases'].pop()),
        ('lost_internal_glyph','native_font_proof',lambda v:v['cases'][0].update(all_first_final_internal_glyphs_in_order_and_unique_cells=False)),
        ('lost_native_bounds','native_font_proof',lambda v:v['cases'][0].update(all_visible_origins_zero_and16px_rows_within4rows=False)),
        ('lost_macro_negative','native_font_proof',lambda v:v['source_macro_absence_negatives'].pop()),
        ('lost_stored_plane','final_padding_proof',lambda v:v['final_target_parity_cases'].pop()),
        ('lost_dispatch','relocated_control_proof',lambda v:v['relocated_dispatch_cases'].pop()),
        ('lost_predicate','relocated_control_proof',lambda v:v['relocated_predicate_pairs'].pop()),
        ('wrong_predicate_result','relocated_control_proof',lambda v:v['relocated_predicate_pairs'][0]['cases'][1].update(native_result=[2,0,0,0,0,0])),
        ('wrong_predicate_ownership','relocated_control_proof',lambda v:v.update(original_predicate_owned_operand_scratch_and_all_unowned4MiB_preserved_at_relocated_cursor=False)),
        ('wrong_resource_reuse','relocated_control_proof',lambda v:v.update(source_resource20_boundary_cases_reused_only_by_exact_words_and_runtime=False)),
        ('lost_opaque_leaf','relocated_control_proof',lambda v:v['all8_source_current_target_nonrelative_nonspeech_leaves'].pop()),
        ('lost_suffix_path','relocated_control_proof',lambda v:v['source_four_relative_sites20_relocated_operand_cases_and_both_boolean_suffix_paths'].pop()),
        ('lost_name_path','source_nameplate_consumer_proof',lambda v:v['native_four_consumer_cases']['rows'].pop()),
        ('lost_owned_scratch','source_nameplate_consumer_proof',lambda v:v['native_four_consumer_cases']['rows'][0].update(original_scratch_rings=[])),
        ('lost_end_decode','termination_decode_proof',lambda v:v['cases'].pop()),
        ('post_payload_read','termination_decode_proof',lambda v:v.update(all2_declared_end_decodes_return_type0_extent4_without_post_payload_read=False)),
        ('lost_actual_single_end','representative_proof',lambda v:v.update(single_end762_actual=False)),
        ('omitted_effect','representative_proof',lambda v:v.update(no_B173_source_command_omitted=False)),
        ('invented_earned_effect','representative_proof',lambda v:v.update(no_natural_event_eligibility_earned_flags_full_route_or_hardware_claim=False)),
        ('lost_offline_jump_scope','representative_proof',lambda v:v.update(source_relative_sites736740756_actual_744_offline_native_only=False)),
        ('lost_actual_VM_last_result_scope','representative_proof',lambda v:v.update(actual_VM_descriptor_last_result1_preserved_through_type3_and_end=False)),
        ('lost_postscene_actor_state','postscene_native_state_proof',lambda v:v.update(postscene9001_whole1A04_actor_models_and_captain2_equal=False)),
        ('lost_postscene_component_state','postscene_native_state_proof',lambda v:v['postscene9001_native_component_equality'].update(models=False)),
        ('lost_timing_distinction','postscene_native_state_proof',lambda v:v['actual_timing_differences'].pop()),
        ('lost_PRNG_scope','postscene_native_state_proof',lambda v:v.update(PRNG_equality_or_future_world_equivalence_not_claimed=False)),
    ]
''' + text[b:]
    a=text.index('    def changed_actual(');b=text.index("    mutations.extend(('map_'",a)
    text=text[:a]+'''    def changed_actual(value,label):
        old=next(p for p in value['evidence'] if p.endswith('actual_all11_unforced_predicate_paths_effects_and_end.json'))
        actual=read(old);version=actual['versions'][0]
        if label=='wrong_actual_presentation':version['actual_presentation_commands'][0]['word']=0x6001
        elif label=='wrong_actual_end':version['single_source_end_offset']=766
        elif label=='wrong_actual_predicate':version['actual_predicate']['result_words']=[2,0]
        elif label=='wrong_actual_A000':version['source_A000_hex_by_offset']['748']='00a0ffff00000000'
        elif label=='reset_actual_effect_last_result':version['actual_source_A000s'][1]['result_words']=[3,0]
        elif label=='reset_actual_end_last_result':version['selected_B22_command_pairs'][-1]['result_words']=[0,0]
        elif label=='reset_actual_relative_last_result':version['actual_source_relative_commands'][0]['result_words']=[3,0]
        elif label=='wrong_actual_resource':version['actual_resources'][0]['word']=0x6326
        else:actual['versions'].pop()
        destination=ROOT/label/'actual_all11_unforced_predicate_paths_effects_and_end.json';destination.parent.mkdir()
        save(destination,actual);value['evidence'].pop(old);value['evidence'][str(destination)]=sha(destination.read_bytes())
    mutations.extend((label,'representative_proof',lambda value,label=label:changed_actual(value,label)) for label in [
        'wrong_actual_presentation','wrong_actual_end','wrong_actual_predicate','wrong_actual_resource','wrong_actual_A000',
        'reset_actual_effect_last_result','reset_actual_end_last_result','reset_actual_relative_last_result','missing_actual_version'])
''' + text[b:]
    a=text.index('    profile.update(status=');b=text.index("    registry['profiles'][PROFILE]",a)
    text=text[:a]+'''    profile.update(status='experimental',lil_B173_editorial=owned.CONFIG,
        description='Full V4404 cumulative stack plus11 B173 crown inquiry/Reika tomb-lead reviews:eight revisions/three retentions,11 progressive speeches,23 structural commands,eight numeric leaves,four relative sites/20 target cases,one predicate andtwo A000s. Two9001-frame unforced content boots observe all11 panels,predicate1,both effects,single end andnormal return;115 nontext regions match. Actual VM last-result1 survives type3/end;unvisited jump744 has offline native coverage. Exported postscene state is compared without PRNG/future-world equality or natural eligibility claims.',
        note='B173 source/native/reference/representative approved;registered build,exact patch andfresh startup pending.')
''' + text[b:]
    changes={'B172':'B173','registration_v4403':'registration_v4444','build_integrated_release_v4403.tmp':'build_integrated_release_v4444.tmp',
        'all-routes-unified-v4404':'all-routes-unified-v4445','all_routes_combined_v4353':'all_routes_combined_v4404',
        'all-routes-unified-v4353':'all-routes-unified-v4404',
        "registry['latest_promoted_build']['profile'] == 'all-routes-unified-v4353'":"registry['latest_promoted_build']['profile'] == 'all-routes-unified-v4353'",
        "promoted_profile_unchanged='all-routes-unified-v4353'":"promoted_profile_unchanged='all-routes-unified-v4353'",
        'reference_checkpoint_v4400':'reference_checkpoint_v4441','reference_approval_v4399':'reference_approval_v4440',
        'loader_v4385':'loader_v4432','editorial_handoff_verification_v4401b':'editorial_handoff_verification_v4442b',
        'focused_repeat_proof':'postscene_native_state_proof',
        'transition_review_v4398/all5_sheets_departure_C200_A000_and_paired_return_review':'actual_review_v4439/all2_actual_sheets_unforced_suffix_paired_return_and_final_state',
        "visual['English_full_screen_views'] + visual['Japanese_full_screen_views']":"visual['paired_full_screen_views']",
        "    deps.update(row['path'] for row in visual['all4_paired_full_screen_sheets_viewed'])\n":'',
        "len(proof['changed_records']) == 27":"len(proof['changed_records']) == 11",
        'invented_Mihwa':'invented_Reika','native_six_consumer_cases':'native_four_consumer_cases',"r['actor_ID']==201":"r['actor_ID']==202",
        'V4353 stack':'V4404 stack','after_full_V4353':'after_full_V4404',
        'expected_manifest_batches=547':'expected_manifest_batches=549','expected_batches=548':'expected_batches=549','positive_records=27':'positive_records=11',
    }
    for key in changes:assert key in text,key
    text=re.sub('|'.join(re.escape(k) for k in sorted(changes,key=len,reverse=True)),lambda m:changes[m[0]],text)
    assert not re.search(r'B172|focused_repeat|Mihwa|source_C200|native_six|paired_town9370',text)
    compile(text,str(TARGET),'exec');TARGET.write_text(text,encoding='utf-8',newline='\n')
    ROOT.mkdir(parents=True)
    save(ROOT/'derivation.json',dict(source=str(SOURCE),source_sha256=sha(SOURCE.read_bytes()),target=str(TARGET),target_sha256=sha(TARGET.read_bytes()),
        producer_sha256=sha(Path(__file__).read_bytes()),relative_predicate_effect_VM_last_result_and_readonly_name_negatives=True,
        positive_and_all_negatives_precede_registry_builder_writes=True,expected_batches=549,full_goal_complete=False))
    print('Prepared B173 atomic registration and source-bound negatives after full V4404;main V4353 preserved.')
