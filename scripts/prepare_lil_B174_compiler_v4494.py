"""Freeze B174 atomic compilation with explicit conditional/native/actual contracts."""
from pathlib import Path
import re
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import save

ROOT=Path('work/analysis/lil_B174_compiler_tools_v4494')
OLD=Path('dk4tool/patch/lil_B173_editorial_v1.py')
NEW=Path('dk4tool/patch/lil_B174_editorial_v1.py')

if __name__=='__main__':
    assert not ROOT.exists() and not NEW.exists()
    text=OLD.read_text(encoding='utf-8')
    changes={
        'lil_B173_layout_v1':'lil_B174_layout_v2','lil_B173_profile':'lil_B174_profile',
        "len(rows) == len({row['id'] for row in rows}) == 11":"len(rows) == len({row['id'] for row in rows}) == 33",
        "{'progressive': 11}":"{'progressive': 33}","{'revise': 8, 'retain-wording': 3}":"{'revise': 23, 'retain-wording': 10}",
        "len(sample['represented_reviewed_display_IDs']) == 11":"len(sample['represented_reviewed_display_IDs']) == 33",
        "len({case['id'] for case in controls['relocated_dispatch_cases']}) == 11":"len({case['id'] for case in controls['relocated_dispatch_cases']}) == 33",
        "['block'] == 173":"['block'] == 174",'[173]':'[174]','block=173':'block=174',
        '[736,740,744,756]':'[882,886,890,938]',
        "len(commands) == 23 and sum(command['word'] == 0x4000 for command in commands) == 11":
            "len(commands) == 45 and sum(command['word'] == 0x4000 for command in commands) == 33",
        "[762] and len(stops)==1 and stops[0]['new_offset']==794":"[2086] and len(stops)==1 and stops[0]['new_offset']==2204",
        'target[794:798]':'target[2204:2208]','source_commands=23':'source_commands=45',
        '11 exact speech records required':'33 exact speech records required',
        'all11_progressive_speeches_zero_macros_resources_predicate_relative_suffix_two_A000s_and8_leaves_preserved':
            'all33_progressive_speeches_zero_macros_resource_optional_Emilio_two_A000s_C200_and8_leaves_preserved',
        'all11_five_review_gates_true':'all33_five_review_gates_true','B173':'B174',
    }
    for key in changes:assert key in text,key
    text=re.sub('|'.join(re.escape(k) for k in sorted(changes,key=len,reverse=True)),lambda m:changes[m[0]],text)
    def section(start,stop,value):
        global text
        a=text.index(start);b=text.index(stop,a);text=text[:a]+value+text[b:]
    section('SELECTORS = ','\n\ndef load', '''SELECTORS = {2,14,26,201}
FLAGS = ['all45_structural_commands_four_relative_sites_one_predicate_verified','all33_active_speech_targets_preserved',
    'all8_leaves_two_presentations_one_resource_predicate_two_A000s_C200_and_single_end_exact','single_tail_endword_preserved',
    'no_FE_consumers_and_FI0_FA0_FO0_preserved','no_source2100_4100_or_dynamic_objects','no_source2000_pause',
    'all_four_relative_sites20_target_cases_and_both_optional_speech_paths_preserved',
    'source_predicate874_optional_Emilio_then6240_two_A000s_C200_end_preserved','representative_shared_rules_approved']
OFFLINE = ['DK4_MES_B174_R0069']
''')
    section("    observed=load(doc['postscene_native_state_proof'])", "    rows = doc['records']", '''    observed=load(doc['postscene_native_state_proof'])
    require(observed['exact_timing_difference_counts']==dict(total=28,speech=20,control_or_end=8)
        and Counter(c['source']['word'] for c in observed['actual_timing_differences'])=={0x4000:20,0x8000:1,0x200:1,0x100:1,0x6240:1,0xA000:2,0xC200:1,0:1},
        'exact twenty speech/eight control-end timing distinction required')
    require(observed['all32_complete_held_planes_and_source_paired_regions_match'] and observed['all232_sampled_nontext_regions_equal']
        and len(observed['all232_sampled_nontext_region_checks'])==232 and observed['whole_RGB_town10810_and_final16001_equal']
        and all(observed['postscene16001_native_component_equality'].values()) and observed['postscene16001_whole1A04_actor_models_and_captain2_equal']
        and observed['PRNG_equality_or_future_world_equivalence_not_claimed'],'actual display and scoped postscene state required')
    require(observed['join_notice10570_complete_shared_text_plane_equal'] and observed['join_notice_leading_J_full_Julian_Lopes_and_trailing_exclamation_viewed']
        and observed['join_notice_full_RGB_difference_is_original_A_button_indicator']==[224,360,240,376], 'complete existing join notice and explicit indicator scope required')
    require(len(native['cases'])==33 and native['current_original_macro_alignment_calls']==264
        and native['new_current_original_macro_alignment_calls']==8 and native['reused_original_macro_alignment_calls']==256
        and native['all33_current_native_speech_planes_pass'] and native['progressive_planes']==33 and native['FE_planes']==0,'complete native progressive proof required')
    for key,count in [('source_bound_formatter_negatives',14),('source_consumer_negative_controls',17),('source_macro_preservation_negatives',0),('source_macro_absence_negatives',3)]:
        require(len(native[key])==count and all(c['rejected'] for c in native[key]),'native rejection controls differ:'+key)
    require(len(stored['final_target_parity_cases'])==33 and stored['current_final_stored_macro_alignment_cases']==132
        and stored['new_parity_macro_alignment_cases']==48 and stored['exact_byte_identical_reused_macro_alignment_cases']==84
        and stored['all33_final_targets_complete_native_planes_equal_reviewed_planes'],'complete stored native proof required')
    require(len(controls['relocated_dispatch_cases'])==33 and len(controls['relocated_predicate_pairs'])==1
        and len(controls['all8_source_current_target_nonrelative_nonspeech_leaves'])==8 and len(controls['relocated_C200_pairs'])==1
        and controls['all33_progressive_consumers_no_macros_exact'] and controls['source32_unconditional_speeches_and_optional_Emilio69_preserved']
        and controls['original_predicate_owned_operand_scratch_and_all_unowned4MiB_preserved_at_relocated_cursor']
        and controls['source_resource10_boundary_cases_reused_only_by_exact_words_and_runtime']
        and controls['source_two_presentation_and_two_A000_structural_results_reused_only_by_exact_whole_commands_and_runtime']
        and len(controls['source_four_relative_sites20_relocated_operand_cases_and_both_boolean_suffix_paths'])==2
        and controls['source_packed_effect_and_predicate_semantics_not_inferred'] and controls['later_older_record0D_reaudit_stays_open'],
        'complete relocated source controls required')
    pair=controls['relocated_predicate_pairs'][0]
    require(pair['source_offset']==874 and pair['target_offset']==904 and len(pair['cases'])==2
        and all(c['native_result']==[2,1,0,0,0,0] and c['sole_scratch_restore_recovers_all4MiB_exact'] for c in pair['cases']),
        'unforced historical native predicate pair required, distinct from actual fixture result0')
    ui=controls['relocated_C200_pairs'][0]
    require(ui['source_offset']==2084 and ui['target_offset']==2202 and len(ui['cases'])==2
        and all(c['native_result']==[3,0,0,0,0,0] and c['native_extent']==2 and c['source_owned_UI_request_words']==[1,0,13,0,0,0,1]
            and len(c['source_owned_UI_writes'])==9 and c['all_other4MiB_actor_roster_event_RNG_and_models_exact']
            and c['original_input_owner_guards_and_ABI_exact'] for c in ui['cases'])
        and ui['cases'][0]['source_owned_UI_writes']==ui['cases'][1]['source_owned_UI_writes'], 'source-owned C200 request and writes required')
    require(ends['all2_declared_end_decodes_return_type0_extent4_without_post_payload_read'] and len(ends['cases'])==2
        and ends['B174_single_end_finishes_declared_logical_end'] and ends['no_relative_destination_at_or_beyond_logical_end'], 'two guarded single-end decodes required')
    require(names['source_0E_1A_C9_selectors_are_Emilio14_Julian26_Mihwa201_not_literal_prose']
        and names['source_new_employer_and_actual_grandfather_preserved_without_romance_status_or_unconditional_date']
        and names['later_older_record0D_reaudit_stays_open'] and names['approved_prose_names']=={'2':'Lil','14':'Emilio','26':'Julian','201':'Mihwa'}
        and names['progressive_nameplate_values']==names['full_catalogue_values']=={'2':'Lil Argot','14':'Emilio Ｆerog','26':'Julian Lopes','201':'Mihwa'}, 'source-owned identities required')
    cases=names['native_eight_consumer_cases']['rows']
    require(len(cases)==8 and {c['actor_ID'] for c in cases}==SELECTORS
        and all(c['all_actor_models_and_unowned4MiB_exact'] and c['source_owned_scratch_restoration_or_readonly_path_recovers_all4MiB'] for c in cases), 'complete original name paths required')
    owned=[c for c in cases if c['actor_ID'] in [2,14,26]];readonly=[c for c in cases if c['actor_ID']==201]
    require(len(owned)==6 and all(c['original_scratch_rings'] and c['original_getter_writes'] for c in owned),'six source-owned scratch paths required')
    require(len(readonly)==2 and all(c['ownership_mode']=='original-read-only-name-pointer-without-scratch-ring'
        and not c['original_scratch_rings'] and not c['original_getter_writes'] for c in readonly),'two original Mihwa read-only pointers required')
    require(sample['actual_two_disclosed_content_cold_boots_pass'] and sample['content_frames_each']==16001 and sample['new_emulator_runs']==2
        and sample['all32_unconditional_panels_unforced_predicate_both_effects_C200_single_end_and_normal_town_return_pass']
        and sample['optional_Emilio69_offline_native_planes_names_dispatch_and_both_operand_paths_approved']
        and sample['original45_structural_commands_and_single_declared_endword_preserved'] and sample['no_B174_source_command_omitted']
        and sample['source_predicate0_then6240_A0002068_A0002076_C2002084_and_end_executed']
        and sample['source_relative_sites882890_actual_886894938_offline_native_only'] and sample['actual_source_0100_extent52_and_relocated_extent62_distinguished']
        and sample['actual_VM_descriptor_last_result0_preserved_through_type3_C200_and_end'] and sample['single_end2086_actual']
        and sample['original_B22_four_A000_initialization_commands_retained'] and sample['no_source_pause_invented_and_original_C200_retained']
        and sample['all232_sampled_nontext_regions_and_whole_RGB_town10810_and_final16001_equal']
        and sample['postscene16001_five_native_components_whole_actor_model_and_captain2_equal']
        and sample['complete_existing_join_notice_and_first_J_preserved']
        and sample['source_packed_predicate_and_A000_semantics_not_inferred'] and sample['PRNG_and_future_world_equality_not_claimed']
        and sample['no_open_translation_specific_display_or_control_finding']
        and sample['no_natural_event_eligibility_earned_flags_full_route_or_hardware_claim']
        and sample['actual_selected_B174_source_events']==[] and sample['offline_only_display_IDs']==OFFLINE,'representative actual approval required')
    paths=[p for p in sample['evidence'] if p.endswith('actual_all33_unforced_predicate_paths_effects_C200_and_end.json')]
    require(len(paths)==1,'one exact actual proof required');actual=load(paths[0])
    require(sha(Path(paths[0]).read_bytes())==sample['evidence'][paths[0]] and not actual['failures'] and not actual['paired_region_differences']
        and actual['complete_matching_observations']==actual['fresh_actual_unique_speech_panels']==32 and actual['offline_only_display_IDs']==OFFLINE
        and len(actual['versions'])==2 and {v['case'] for v in actual['versions']}=={'clean_Japanese','reviewed_English'}
        and actual['actual_result_words_are_player_descriptor_command_type_and_persistent_VM_last_result'], 'two complete actual paths required')
    require([v['fixture_exit_frame'] for v in actual['versions']]==[10776,10774],'source/English exits differ from observed pair')
    for version in actual['versions']:
        require(version['frames']==16001 and version['single_source_end_offset']==2086 and len(version['selected_B22_command_pairs'])==51
            and version['unforced_predicate_result']==0 and version['actual_predicate']['result_words']==[2,0]
            and version['selected_B22_command_pairs'][-1]['result_words']==[0,0]
            and [r['original_source_offset'] for r in version['actual_source_A000s']]==[2068,2076]
            and [r['result_words'] for r in version['actual_source_A000s']]==[[3,0],[3,0]]
            and [r['original_source_offset'] for r in version['actual_source_relative_commands']]==[882,890]
            and all(r['result_words']==[3,0] and r['extent']==r['independently_verified_native_extent'] for r in version['actual_source_relative_commands'])
            and version['source_A000_hex_by_offset']=={'2068':'00a0ffff020cc960','2076':'00a0ffff1a100120'}
            and version['source_predicate_hex']=='0080ffff0efe0030'
            and [r['word'] for r in version['actual_presentation_commands']]==[0x6000,0x6240]
            and version['actual_presentation_commands'][-1]['result_words']==[3,0]
            and [r['word'] for r in version['actual_resources']]==[0x6340]
            and len(version['actual_source_C200'])==1 and version['actual_source_C200'][0]['original_source_offset']==2084
            and version['actual_source_C200'][0]['result_words']==[3,0]
            and [r['source_offset'] for r in version['unvisited_declared_source_objects']]==[886,894,938], 'actual predicate/effect/C200/relative/end scope differs')
    require([v['actual_source_relative_commands'][1]['extent'] for v in actual['versions']]==[52,62], 'source and relocated actual skip extents required')
    require(len(native['review_sheets'])==5 and len(sample['viewed_actual_sheets'])==6,'all viewed sheets required')
    for sheet in native['review_sheets']+sample['viewed_actual_sheets']:
        require((sheet.get('viewed') is True or sheet.get('viewed_in_full_current_turn') is True)
            and sheet['review'] and sha(Path(sheet['path']).read_bytes())==sheet['sha256'],'viewed sheet changed')
''')
    # Keep the proven complete-object compiler and inverse byte reconstruction.
    section("    exact=[(8,", "    restored = bytearray(logical)", '''    exact=[(8,'0060'),(10,'4063'),(874,'0080ffff0efe0030'),(2066,'4062'),
        (2068,'00a0ffff020cc960'),(2076,'00a0ffff1a100120'),(2084,'00c2'),(2086,'00000000')]
    require([(c['old_offset'],block[c['old_offset']:c['old_offset']+c['old_native_extent']].hex()) for c in leaves]==exact,'eight complete source leaves differ')
    require([c['word'] for c in leaves]==[0x6000,0x6340,0x8000,0x6240,0xA000,0xA000,0xC200,0]
        and sum(c['word']==0xC200 for c in commands)==1 and all(c['word'] not in [0x2000,0x2100,0x4100] for c in commands), 'complete source predicate/effect/C200/no-pause scope required')
''')
    anchor="        fe = row['kind'] == 'system-FE'"
    assert text.count(anchor)==1
    text=text.replace(anchor,"""        require(row['actual_B22_display_fixture_observed']==(ident not in OFFLINE)
            and row['offline_only_native_display_checked']==(ident in OFFLINE)
            and row['current_native_UI_body_explicit_unexecuted_boundary']==(ident in OFFLINE), 'individual actual/offline scope differs')
        if ident in OFFLINE:
            require(row['source_selector']==14 and row['ancestor_0100_offsets']==[890], 'source conditional Emilio binding required')
"""+anchor)
    compile(text,str(NEW),'exec');NEW.write_text(text,encoding='utf-8',newline='\n')
    ROOT.mkdir(parents=True)
    save(ROOT/'derivation.json',dict(previous=str(OLD),previous_sha256=sha(OLD.read_bytes()),successor=str(NEW),
        successor_sha256=sha(NEW.read_bytes()),source_objects=33,actual32_offline1_explicit=True,
        original_atomic_complete_object_and_inverse_core_preserved=True,all45_commands_four_relative_sites_C200_and_two_A000s_preserved=True,
        no_registry_ROM_orledger_change=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('Prepared frozen B174 atomic compiler:33 speeches,32 actual/one offline,45 commands, four relative sites, two effects/C200 and inverse bytes.')
