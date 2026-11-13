"""Derive atomic negative tests and append-only cumulative registration for B167."""
import re
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B167_registration_tools_v4158')
TARGET=Path('scripts/register_lil_B167_v4159.py')
if __name__=='__main__':
    assert not ROOT.exists() and not TARGET.exists()
    compiler=derive('dk4tool/patch/lil_B167_editorial_v1.py','dk4tool/patch/lil_B167_editorial_v2.py',{
        'len(oldblocks)==216':'len(oldblocks)==336'}) # file-block count and native alignment count are separate quantities
    source=Path('scripts/register_lil_B166_v4109.py');text=source.read_text(encoding='utf-8').replace('B166','B167')
    changes={
        'lil_B167_editorial_v1':'lil_B167_editorial_v2','lil_B167_registration_v4109':'lil_B167_registration_v4159',
        "PROFILE='all-routes-unified-v4110'":"PROFILE='all-routes-unified-v4160'",'all_routes_combined_v4046':'all_routes_combined_v4110',
        'lil_B167_editorial_manuscript_v6':'lil_B167_editorial_manuscript_v13',
        'scripts/prepare_lil_B167_compiler_v4107.py':'scripts/prepare_lil_B167_compiler_v4157.py',
        'scripts/prepare_lil_B167_registration_v4108.py':'scripts/prepare_lil_B167_registration_v4158.py',
        'lil_B167_layout_v4':'lil_B167_layout_v6','lil_B167_reference_approval_v4106':'lil_B167_reference_approval_v4154',
        'lil_B167_loader_v4097':'lil_B167_loader_v4143',
        'lil_B167_transition_review_v4105/both_choices_all7_sheets_Manuel_names_figures_and_paired_returns_review':'lil_B167_transition_review_v4152/both_choices_all5_sheets_static_names_and_distinct_returns_review',
        ";deps.add(native['actual_menu_review_sheet']['path'])":'',
        "len(proof['changed_records'])==44":"len(proof['changed_records'])==29",
        'lil_manuel_advice':'lil_sail_lesson','V4046':'V4110','build_integrated_release_v4109.tmp':'build_integrated_release_v4159.tmp',
        "profile=deepcopy(registry['profiles']['all-routes-unified-v4046'])":"profile=deepcopy(registry['profiles']['all-routes-unified-v4110'])",
        "parent_profile='all-routes-unified-v4046'":"parent_profile='all-routes-unified-v4110'",
        'expected_manifest_batches=541':'expected_manifest_batches=543','positive_records=44':'positive_records=29','expected_batches=541':'expected_batches=543'
    }
    for old,new in changes.items():assert old in text,old;text=text.replace(old,new)
    pattern=r"assert sha\(raw\)=='[0-9a-f]{64}' and sha\(before\)=='[0-9a-f]{64}'"
    assert len(re.findall(pattern,text))==1
    text=re.sub(pattern,"assert sha(raw)=="+repr(sha(Path('translations/release_stack.json').read_bytes()))+" and sha(before)=="+repr(sha(Path('scripts/build_integrated_release.py').read_bytes())),text)
    start=text.index('    mutations=[');stop=text.index('    for flag in owned.FLAGS:',start)
    mutations='''    mutations=[
        ('missing_review_gate','manuscript',lambda d:d['records'][0]['review'].update(source=False)),
        ('lost_source0D','manuscript',lambda d:next(r for r in d['records'] if r['source_selector']==13).update(english='We know ships.')),
        ('wrong_legal_source0D','manuscript',lambda d:next(r for r in d['records'] if r['source_selector']==13).update(english='{SPEAKER:02}We know ships.')),
        ('source0D_stripped_as_CR','manuscript',lambda d:next(r for r in d['records'] if r['source_selector']==13).update(source_hex=next(r for r in d['records'] if r['source_selector']==13)['source_hex'][2:])),
        ('printable6D_treated_as_m','manuscript',lambda d:d['records'][0].update(english='mAdmiral!')),
        ('printable6D_stripped','manuscript',lambda d:d['records'][0].update(source_hex=d['records'][0]['source_hex'][2:])),
        ('manual_break','manuscript',lambda d:d['records'][0].update(english=d['records'][0]['english']+'{LB}')),
        ('manual_padding','manuscript',lambda d:d['records'][0].update(english=d['records'][0]['english']+'{PAD}')),
        ('invented_FI','manuscript',lambda d:d['records'][0].update(english=d['records'][0]['english']+' {MACRO:FI}')),
        ('missing_speech','manuscript',lambda d:d['records'].pop()),
        ('wrong_source_reference','manuscript',lambda d:d['records'][0]['source_reference'].update(offset=1)),
        ('wrong_current_reference','manuscript',lambda d:d['records'][0]['current_reference'].update(offset=1)),
        ('missing_choice','choices',lambda d:d['records'].pop()),
        ('swapped_choice_index','choices',lambda d:d['records'][0].update(option_index=1)),
        ('wrong_choice_label','choices',lambda d:d['records'][0].update(english='No')),
        ('wrong_choice_source_pointer','choices',lambda d:d['records'][0]['source_reference'].update(offset=1)),
        ('wrong_whole_choice','choices',lambda d:d['records'][0].update(typed_target_object_hex='002100000000')),
        ('wrong_entry','reference_map',lambda d:d.update(entry_point_offset=10)),
        ('missing_relative_edge','reference_map',lambda d:d['blocks'][0]['relative_skip_fixups'].pop()),
        ('bad_relative_target','reference_map',lambda d:d['blocks'][0]['relative_skip_fixups'][0].update(new_matched_skip_target=999)),
        ('lost_separated_end','reference_map',lambda d:d['blocks'][0]['original_declared_end_word_maps'].pop()),
        ('wrong_native_command','reference_map',lambda d:d['blocks'][0]['mapped_native_commands'][0].update(new_offset=10)),
        ('invented_pause','reference_map',lambda d:d['blocks'][0]['original2000_pause_and_resume_maps'].append({})),
        ('native_missing_plane','native_font_proof',lambda d:d['cases'].pop()),
        ('native_wrong_alignment_count','native_font_proof',lambda d:d.update(current_original_macro_alignment_calls=1)),
        ('native_missing_first_glyph','native_font_proof',lambda d:d['cases'][0].update(all_first_final_internal_glyphs_in_order_and_unique_cells=False)),
        ('native_wrong_bounds','native_font_proof',lambda d:d['cases'][0].update(all_visible_origins_zero_and16px_rows_within4rows=False)),
        ('stored_missing_target','final_padding_proof',lambda d:d['final_target_parity_cases'].pop()),
        ('stored_wrong_alignment_count','final_padding_proof',lambda d:d.update(current_final_stored_macro_alignment_cases=1)),
        ('lost_relocated_actor','relocated_control_proof',lambda d:d['relocated_dispatch_cases'].pop()),
        ('wrong_relocated_actor0D','relocated_control_proof',lambda d:next(r for r in d['relocated_dispatch_cases'] if r['source_selector']==13).update(resolved_actor_ID=2)),
        ('lost_control_leaf','relocated_control_proof',lambda d:d['all6_source_current_target_nonrelative_nonspeech_nonchoice_leaves'].pop()),
        ('lost_menu_getter_phase','relocated_control_proof',lambda d:d['relocated_choice_getter_phases'].pop()),
        ('missing_actual_boot','representative_proof',lambda d:d.update(new_emulator_runs=0)),
        ('missing_actual_Shipwright_name','representative_proof',lambda d:d.update(actual_Shipwright109_Lil2_Janus4_Manuel23_original_names_and_portraits_observed=False)),
        ('missing_actual_speech','representative_proof',lambda d:d['actual_sampled_display_IDs'].pop()),
        ('missing_actual_choice','representative_proof',lambda d:d['actual_sampled_choice_IDs'].pop()),
        ('invented_natural_source_event','representative_proof',lambda d:d.update(actual_selected_B167_source_events=[167])),
        ('flattened_choice','representative_proof',lambda d:d.update(source_two_Cesare_queries12_relative_containers_choice_and_both_ends_retained_not_flattened=False)),
        ('lost_B22_initialization','representative_proof',lambda d:d.update(original_B22_four_A000_initialization_commands_retained=False)),
        ('lost_actual_four_boots','representative_proof',lambda d:d.update(actual_four_disclosed_cold_boots_pass=False)),
        ('invented_effect_omission','representative_proof',lambda d:d.update(no_B167_effect_or_source_command_omitted=False)),
        ('wrong_Cesare_progressive_name','source_nameplate_consumer_proof',lambda d:d['native_ten_consumer_cases']['rows'][4].update(text='Cesare Tohni')),
        ('wrong_Cesare_full_name','source_nameplate_consumer_proof',lambda d:d['native_ten_consumer_cases']['rows'][5].update(text='Professor Cesare Tony')),
        ('wrong_name_scratch','source_nameplate_consumer_proof',lambda d:d['native_ten_consumer_cases']['rows'][0].update(source_owned_scratch_restoration_or_readonly_path_recovers_all4MiB=False)),
        ('Shipwright_invented_ring','source_nameplate_consumer_proof',lambda d:d['native_ten_consumer_cases']['rows'][8]['original_scratch_rings'].append({})),
        ('Shipwright_illegal_write','source_nameplate_consumer_proof',lambda d:d['native_ten_consumer_cases']['rows'][9]['original_getter_writes'].append({})),
        ('closed_older0D_audit','source_nameplate_consumer_proof',lambda d:d.update(later_older_record0D_reaudit_stays_open=False)),
        ('missing_end_decode','termination_decode_proof',lambda d:d['cases'].pop()),
        ('post_payload_end_read','termination_decode_proof',lambda d:d.update(all4_declared_end_decodes_return_type0_extent4_without_post_payload_read=False)),
        ('wrong_two_end_contract','termination_decode_proof',lambda d:d.update(B167_first_end_precedes_second_end_and_declared_logical_end=False)),
        ('lost_menu_selection_proof','native_choice_proof',lambda d:d.update(six_original_VM_selection_and_cancel_cases_pass=False)),
        ('lost_menu_glyph_proof','native_choice_proof',lambda d:d.update(eight_complete_native_style_label_planes_pass=False)),
        ('lost_Cesare_pair','relocated_control_proof',lambda d:d['relocated_predicate_pairs'].pop()),
        ('wrong_Cesare_result','relocated_control_proof',lambda d:d['relocated_predicate_pairs'][1]['relocated_case'].update(native_result=[2,9,0,0,0,0])),
        ('lost_offline_Cesare','representative_proof',lambda d:d['offline_only_display_IDs'].clear()),
        ('false_actual_Cesare','representative_proof',lambda d:d['offline_only_display_cases'][0].update(actual_display_or_byte_identical_reuse_claim=True)),
        ('wrong_offline_Cesare_actor','representative_proof',lambda d:d['offline_only_display_cases'][1].update(source_selector=2)),
    ]
    def changed_actual(sample,kind):
        old=next(p for p in sample['evidence'] if p.endswith('actual_both_choices_conditional_panels_and_distinct_returns.json'));value=read(old)
        if kind=='wrong_final_menu_word':next(v for v in value['versions'] if v['option_index']==1)['selected_B22_command_pairs'][-1]['result_words']=[0,1]
        elif kind=='wrong_refusal_end':next(v for v in value['versions'] if v['option_index']==1)['source_end_offset']=2172
        elif kind=='wrong_actual_choice':next(v for v in value['versions'] if v['option_index']==1)['actual_choice_command_pair']['result_words']=[2,0]
        else:value['versions'].pop()
        path=ROOT/kind/'actual_both_choices_conditional_panels_and_distinct_returns.json';save(path,value);sample['evidence'].pop(old);sample['evidence'][str(path)]=sha(path.read_bytes())
    mutations.extend((kind,'representative_proof',lambda d,kind=kind:changed_actual(d,kind)) for kind in ['wrong_final_menu_word','wrong_refusal_end','wrong_actual_choice','missing_actual_version'])
'''
    text=text[:start]+mutations+text[stop:]
    start=text.index("description='Full V4110 cumulative stack");end=text.index("');registry['profiles'][PROFILE]",start)
    text=text[:start]+"description='Full V4110 cumulative stack plus29 complete Lil B167 sail-lesson reviews:16 revisions/13 retentions;27 speeches/two labels,46 commands/twelve spans,two Cesare queries,two resources and two separate ends. Four retained-condition B22 cold boots:25 unique/28 observed speeches,both menu outcomes and distinct normal returns;two conditional Cesare remarks offline-only. Native first/final glyphs,full source controls and exact clean-input patch required. No natural event eligibility or hardware claim."+text[end:]
    assert '166' not in text and 'Fernando' not in text and 'Manuel' not in text
    compile(text,str(TARGET),'exec');TARGET.write_text(text,encoding='utf-8',newline='\n')
    ROOT.mkdir(parents=True);save(ROOT/'source_derivation.json',dict(previous=str(source),previous_sha256=sha(source.read_bytes()),successor=str(TARGET),successor_sha256=sha(TARGET.read_bytes()),compiler_correction=compiler,unexecuted_v1_retained_and_superseded_because_alignment_count216_is_not_file_block_count336=True,current_registry_sha256=sha(Path('translations/release_stack.json').read_bytes()),current_builder_sha256=sha(Path('scripts/build_integrated_release.py').read_bytes()),no_ROM_registry_ledger_change_yet=True))
    print('B167 compiler v2 and atomic registration/rejection suite created;V4110 inherited in full;V4046 main preserved.')
