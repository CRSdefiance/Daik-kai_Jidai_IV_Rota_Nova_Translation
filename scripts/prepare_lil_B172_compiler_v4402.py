"""Freeze B172's atomic compiler with source-owned names,effects and single end."""
from pathlib import Path
import re
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import save

ROOT=Path('work/analysis/lil_B172_compiler_tools_v4402')
OLD=Path('dk4tool/patch/lil_B171_editorial_v1.py')
NEW=Path('dk4tool/patch/lil_B172_editorial_v1.py')
if __name__=='__main__':
    assert not ROOT.exists() and not NEW.exists()
    text=OLD.read_text(encoding='utf-8')
    def section(start,stop,value):
        global text
        a=text.index(start);b=text.index(stop,a);text=text[:a]+value+text[b:]
    section('SELECTORS = ','\n\ndef load', '''SELECTORS = {2,26,201}
FLAGS = ['all38_commands_zero_relative_sites_zero_predicates_verified','all27_active_speech_targets_preserved',
    'all11_leaves_five_presentations_three_resources_C200_A000_and_single_end_exact','single_tail_endword_preserved',
    'no_FE_consumers_and_FI0_FA0_FO0_preserved','no_source2100_4100_or_dynamic_objects','no_source2000_pause',
    'source_C200_before_A000_raw00a0ffff010cc960_then6240_preserved','representative_shared_rules_approved']
OFFLINE = []
''')
    section("    timing = repeat['cross_language_command_timing_differences']", "    rows = doc['records']", '''    timing = repeat['cross_language_command_timing_differences']
    require(Counter(case['source']['word'] for case in timing)=={0x4000:24,0x4620:1,0x632A:1,0xC200:1,0xA000:1,0x6240:1,0:1},
        'exact24 speech/six control-end timing distinction required')
    require(repeat['paired_town9370_whole1A04_actor_models_and_captain2_equal']
        and repeat['cross_language_command_order_results_and_single_end_word_equal']
        and repeat['cross_language_exit_frames']==[9336,9335] and repeat['all_requested_same_ROM_repeat_frames_whole_RGB_equal']
        and all(all(case['component_equality'].values()) for case in repeat['paired_native_persistent_state_and_PRNG_samples'] if case['frame']<=14050),
        'explicit post-C200/A000 state and later PRNG scope required')
    require(len(native['cases'])==27 and native['current_original_macro_alignment_calls']==216
        and native['all27_current_native_speech_planes_pass'] and native['progressive_planes']==27 and native['FE_planes']==0,
        'complete native progressive proof required')
    for key,count in [('source_bound_formatter_negatives',14),('source_consumer_negative_controls',15),('source_macro_preservation_negatives',0),('source_macro_absence_negatives',3)]:
        require(len(native[key])==count and all(case['rejected'] for case in native[key]),'native rejection controls differ:'+key)
    require(len(stored['final_target_parity_cases'])==27 and stored['current_final_stored_macro_alignment_cases']==108
        and stored['new_parity_macro_alignment_cases']==68 and stored['exact_byte_identical_reused_macro_alignment_cases']==40
        and stored['all27_final_targets_complete_native_planes_equal_reviewed_planes'],'complete stored native proof required')
    require(len(controls['relocated_dispatch_cases'])==27 and not controls['relocated_predicate_pairs']
        and len(controls['all11_source_current_target_nonrelative_nonspeech_leaves'])==11
        and controls['all27_progressive_consumers_no_macros_exact'] and len(controls['relocated_C200_pairs'])==1
        and controls['original_C200_queue_and_all_unowned4MiB_preserved_at_relocated_cursor']
        and controls['source_resource30_boundary_cases_reused_only_by_exact_words_and_runtime']
        and controls['source_five_presentation_and_one_A000_structural_results_reused_only_by_exact_whole_commands_and_runtime']
        and controls['single_tail_end_and_no_source_pause_preserved'] and controls['source_C200_then_A000_then6240_and_end_preserved']
        and controls['no_source_relative_sites_or_membership_predicates'] and controls['later_older_record0D_reaudit_stays_open'],
        'complete relocated source controls required')
    require(ends['all2_declared_end_decodes_return_type0_extent4_without_post_payload_read'] and len(ends['cases'])==2
        and ends['B172_single_end_finishes_declared_logical_end'] and ends['no_relative_destination_at_or_beyond_logical_end'],
        'two guarded single-end decodes required')
    require(names['source_1A_and_C9_selectors_are_Julian26_Mihwa201_not_text_to_strip']
        and names['source_printed_Yurian_and_Mihwa_use_bound_approved_spellings'] and names['surname_not_added_to_source_given_name_addresses']
        and names['source_familiar_flirtation_does_not_establish_romantic_partnership_or_actual_date_agreement']
        and names['later_older_record0D_reaudit_stays_open'] and names['approved_prose_names']=={'2':'Lil','26':'Julian','201':'Mihwa'}
        and names['progressive_nameplate_values']==names['full_catalogue_values']=={'2':'Lil Argot','26':'Julian Lopes','201':'Mihwa'},
        'source-owned identities required')
    name_cases=names['native_six_consumer_cases']['rows']
    require(len(name_cases)==6 and {case['actor_ID'] for case in name_cases}==SELECTORS
        and all(case['all_actor_models_and_unowned4MiB_exact'] and case['source_owned_scratch_restoration_or_readonly_path_recovers_all4MiB'] for case in name_cases),
        'complete original name paths required')
    owned=[case for case in name_cases if case['actor_ID'] in {2,26}]
    readonly=[case for case in name_cases if case['actor_ID']==201]
    require(len(owned)==4 and all(case['original_scratch_rings'] and case['original_getter_writes'] for case in owned),
        'four original Lil/Julian owned scratch paths required')
    require(len(readonly)==2 and all(not case['original_scratch_rings'] and not case['original_getter_writes'] for case in readonly),
        'two original Mihwa read-only pointer paths required')
    require(sample['actual_two_disclosed_content_cold_boots_pass'] and sample['two_additional_focused_repeats_postscene_state_and_PRNG_checked']
        and sample['new_emulator_runs']==4 and sample['actual27_progressive_panels_departure_resources_C200_A000_single_end_and_normal_town_return_pass']
        and sample['no_open_translation_specific_display_or_control_finding'] and sample['original38_commands_and_single_declared_endword_preserved']
        and sample['no_B172_source_command_omitted'] and sample['single_end1880_actual'] and sample['original_B22_four_A000_initialization_commands_retained']
        and sample['source_C200_then_A000_raw00a0ffff010cc960_then6240_preserved_and_executed'] and sample['source_A000_packed_semantics_not_inferred']
        and sample['no_source_pause_invented'] and sample['two_transient_and99_later_nontext_differences_preserved_with_explicit_state_scope']
        and sample['no_natural_event_eligibility_earned_flags_full_route_or_hardware_claim']
        and sample['actual_selected_B172_source_events']==[] and sample['offline_only_display_IDs']==[],'representative actual approval required')
    actual_paths=[path for path in sample['evidence'] if path.endswith('actual_all27_presentations_resources_C200_A000_and_end.json')]
    require(len(actual_paths)==1,'one exact actual proof required')
    actual=load(actual_paths[0])
    require(sha(Path(actual_paths[0]).read_bytes())==sample['evidence'][actual_paths[0]] and not actual['failures']
        and actual['paired_region_differences']==[dict(id='DK4_MES_B172_R0007',frame=2950,native_text_plane_exact=True,paired_source_upper_or_portrait_region_differs=True,not_masked_or_retimed=True)]
        and len(actual['versions'])==2 and {version['case'] for version in actual['versions']}=={'clean_Japanese','reviewed_English'}
        and actual['complete_matching_observations']==actual['fresh_actual_unique_speech_panels']==27,'two complete actual paths required')
    require([version['fixture_exit_frame'] for version in actual['versions']]==[9336,9335],'source/English exits differ from observed pair')
    require(all(version['frames']==20001 and version['single_source_end_offset']==1880 and len(version['selected_B22_command_pairs'])==47
        and version['selected_B22_command_pairs'][-1]['result_words']==[0,0]
        and version['actual_C200']['original_source_offset']==1868 and version['actual_C200']['result_words']==[3,0]
        and version['actual_source_A000']['original_source_offset']==1870 and version['actual_source_A000']['result_words']==[3,0]
        and version['source_A000_hex']=='00a0ffff010cc960'
        and [r['word'] for r in version['actual_presentation_commands']]==[0x6000,0x45FF,0x4651,0x4620,0x6240]
        and [r['word'] for r in version['actual_resources']]==[0x6329,0x6340,0x632A] for version in actual['versions']),
        'actual presentation/resource/C200/A000/termination results differ')
    require(len(native['review_sheets'])==4 and len(sample['viewed_actual_sheets'])==5,'all viewed sheets required')
    for sheet in native['review_sheets']+sample['viewed_actual_sheets']:
        require(sheet['review'].startswith('Viewed') and sha(Path(sheet['path']).read_bytes())==sheet['sha256'],'viewed sheet changed')
''')
    section('    stops = [command for command in commands', '    restored = bytearray(logical)', '''    stops = [command for command in commands if command['word']==0]
    require([command['old_offset'] for command in stops]==[1880] and len(stops)==1
        and stops[0]['new_offset']==1930 and stops[0]['new_offset']+4==len(logical)
        and target[stops[0]['new_offset']:stops[0]['new_offset']+4]==bytes(4),'single source end differs')
    require([(command['old_offset'],command['new_offset'],4) for command in stops]
        ==[(item['source_offset'],item['target_offset'],item['extent']) for item in spec['original_declared_end_word_maps']],'end map differs')
    leaves=[command for command in commands if command['word']!=0x4000]
    exact=[(8,'0060'),(10,'ff45ffff0020'),(16,'2963'),(18,'5146f080'),(22,'4063'),(1218,'20467d80'),
        (1222,'2a63'),(1868,'00c2'),(1870,'00a0ffff010cc960'),(1878,'4062'),(1880,'00000000')]
    require([(command['old_offset'],block[command['old_offset']:command['old_offset']+command['old_native_extent']].hex()) for command in leaves]==exact,
        'eleven complete source leaves differ')
    require([command['word'] for command in leaves]==[0x6000,0x45FF,0x6329,0x4651,0x6340,0x4620,0x632A,0xC200,0xA000,0x6240,0]
        and all(command['word'] not in [0x2000,0x8000] for command in commands),'source C200 then A0006240 and no-pause scope differs')
''')
    changes={'B171':'B172',"require(macros == {b'FI': 1}":'require(not macros',
        "{'revise': 24, 'retain-wording': 13}":"{'revise': 19, 'retain-wording': 8}",
        "source_commands=45":"source_commands=38",'len(commands) == 45':'len(commands) == 38',
        'all37_progressive_speeches_macros_presentations_resource_C200_and8_leaves_preserved':'all27_progressive_speeches_zero_macros_presentations_resources_C200_A000_and11_leaves_preserved'}
    for key in changes:assert key in text,key
    text=re.sub('|'.join(re.escape(k) for k in sorted(changes,key=len,reverse=True)),lambda m:changes[m[0]],text)
    text=re.sub(r'(?<!\d)171(?!\d)','172',text)
    text=re.sub(r'(?<!\d)37(?!\d)','27',text).replace('all37','all27')
    assert not re.search(r'B171|\[171\]|== 171|all37|== 37|2112|2116|all six owned',text)
    compile(text,str(NEW),'exec');NEW.write_text(text,encoding='utf-8',newline='\n')
    ROOT.mkdir(parents=True)
    save(ROOT/'compiler_derivation.json',dict(source=str(OLD),source_sha256=sha(OLD.read_bytes()),
        target=str(NEW),target_sha256=sha(NEW.read_bytes()),producer_sha256=sha(Path(__file__).read_bytes()),
        four_owned_Lil_Julian_and_two_readonly_Mihwa_paths=True,no_shared_guard_or_metric_change=True,full_goal_complete=False))
    print('Prepared atomic B172 compiler:27 speeches,11 exact leaves,C200 then source A000,single end,and correct name ownership.')
