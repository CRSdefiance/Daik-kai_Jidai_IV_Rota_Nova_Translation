"""Freeze B173 atomic compilation with complete relative and retained-VM-result scope."""
from pathlib import Path
import io,re,tokenize
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import save

ROOT=Path('work/analysis/lil_B173_compiler_tools_v4443')
OLD=Path('dk4tool/patch/lil_B172_editorial_v1.py')
NEW=Path('dk4tool/patch/lil_B173_editorial_v1.py')
if __name__=='__main__':
    assert not ROOT.exists() and not NEW.exists()
    text=OLD.read_text(encoding='utf-8')
    def section(start,stop,value):
        global text
        a=text.index(start);b=text.index(stop,a);text=text[:a]+value+text[b:]
    section('SELECTORS = ','\n\ndef load', '''SELECTORS = {2,202}
FLAGS = ['all23_structural_commands_four_relative_sites_one_predicate_verified','all11_active_speech_targets_preserved',
    'all8_leaves_two_presentations_two_resources_predicate_two_A000s_and_single_end_exact','single_tail_endword_preserved',
    'no_FE_consumers_and_FI0_FA0_FO0_preserved','no_source2100_4100_or_dynamic_objects','no_source2000_pause_or_C200',
    'all_four_relative_sites20_target_cases_and_both_suffix_paths_preserved',
    'source_A000720_predicate728_conditional_A000748_then6240_and_end_preserved','representative_shared_rules_approved']
OFFLINE = []
''')
    section("    repeat = load(doc['focused_repeat_proof'])", "    rows = doc['records']", '''    observed=load(doc['postscene_native_state_proof'])
    require(observed['exact_timing_difference_counts']==dict(total=16,speech=8,control_or_end=8)
        and Counter(c['source']['word'] for c in observed['actual_timing_differences'])=={0x4000:8,0xA000:2,0x8000:1,0x200:1,0x300:1,0x100:1,0x6240:1,0:1},
        'exact eight speech/eight control-end timing distinction required')
    require(observed['all11_complete_held_planes_and_source_paired_regions_match'] and observed['all115_sampled_nontext_regions_equal']
        and len(observed['all115_sampled_nontext_region_checks'])==115 and observed['whole_RGB_town5530_and_final9001_equal']
        and all(observed['postscene9001_native_component_equality'].values()) and observed['postscene9001_whole1A04_actor_models_and_captain2_equal']
        and observed['PRNG_equality_or_future_world_equivalence_not_claimed'],'explicit actual display and postscene state scope required')
    require(len(native['cases'])==11 and native['current_original_macro_alignment_calls']==88 and native['all11_current_native_speech_planes_pass']
        and native['progressive_planes']==11 and native['FE_planes']==0,'complete native progressive proof required')
    for key,count in [('source_bound_formatter_negatives',14),('source_consumer_negative_controls',13),('source_macro_preservation_negatives',0),('source_macro_absence_negatives',3)]:
        require(len(native[key])==count and all(c['rejected'] for c in native[key]),'native rejection controls differ:'+key)
    require(len(stored['final_target_parity_cases'])==11 and stored['current_final_stored_macro_alignment_cases']==44
        and stored['new_parity_macro_alignment_cases']==24 and stored['exact_byte_identical_reused_macro_alignment_cases']==20
        and stored['all11_final_targets_complete_native_planes_equal_reviewed_planes'],'complete stored native proof required')
    require(len(controls['relocated_dispatch_cases'])==11 and len(controls['relocated_predicate_pairs'])==1
        and len(controls['all8_source_current_target_nonrelative_nonspeech_leaves'])==8 and not controls['relocated_C200_pairs']
        and controls['all11_progressive_consumers_no_macros_exact']
        and controls['original_predicate_owned_operand_scratch_and_all_unowned4MiB_preserved_at_relocated_cursor']
        and controls['source_resource20_boundary_cases_reused_only_by_exact_words_and_runtime']
        and controls['source_two_presentation_and_two_A000_structural_results_reused_only_by_exact_whole_commands_and_runtime']
        and len(controls['source_four_relative_sites20_relocated_operand_cases_and_both_boolean_suffix_paths'])==2
        and controls['source_packed_effect_and_predicate_semantics_not_inferred'] and controls['later_older_record0D_reaudit_stays_open'],
        'complete relocated source controls required')
    pair=controls['relocated_predicate_pairs'][0]
    require(pair['source_offset']==728 and pair['target_offset']==760 and len(pair['cases'])==2
        and all(c['native_result']==[2,1,0,0,0,0] and c['sole_scratch_restore_recovers_all4MiB_exact'] for c in pair['cases']),
        'unforced relocated predicate pair required')
    require(ends['all2_declared_end_decodes_return_type0_extent4_without_post_payload_read'] and len(ends['cases'])==2
        and ends['B173_single_end_finishes_declared_logical_end'] and ends['no_relative_destination_at_or_beyond_logical_end'],
        'two guarded single-end decodes required')
    require(names['source_CA_selector_is_Reika202_not_text_to_strip']
        and names['source_unnamed_feminine_voice_binds_native_Reika_without_invented_role']
        and names['source_uncertain_smooth_talking_man_report_does_not_confirm_Julian_identity_or_current_location']
        and names['later_older_record0D_reaudit_stays_open'] and names['approved_prose_names']=={'2':'Lil','202':'Reika'}
        and names['progressive_nameplate_values']==names['full_catalogue_values']=={'2':'Lil Argot','202':'Reika'},'source-owned identities required')
    cases=names['native_four_consumer_cases']['rows']
    require(len(cases)==4 and {c['actor_ID'] for c in cases}==SELECTORS
        and all(c['all_actor_models_and_unowned4MiB_exact'] and c['source_owned_scratch_restoration_or_readonly_path_recovers_all4MiB'] for c in cases),
        'complete original name paths required')
    owned=[c for c in cases if c['actor_ID']==2];readonly=[c for c in cases if c['actor_ID']==202]
    require(len(owned)==2 and all(c['original_scratch_rings'] and c['original_getter_writes'] for c in owned),'two original Lil scratch paths required')
    require(len(readonly)==2 and all(c['ownership_mode']=='original-read-only-name-pointer-without-scratch-ring'
        and not c['original_scratch_rings'] and not c['original_getter_writes'] for c in readonly),'two original Reika read-only pointers required')
    require(sample['actual_two_disclosed_content_cold_boots_pass'] and sample['content_frames_each']==9001 and sample['new_emulator_runs']==2
        and sample['all11_progressive_panels_unforced_predicate_both_effects_single_end_and_normal_town_return_pass']
        and sample['original23_structural_commands_and_single_declared_endword_preserved'] and sample['no_B173_source_command_omitted']
        and sample['source_A000720_then_predicate1_then_A0007486240_and_end_executed']
        and sample['source_relative_sites736740756_actual_744_offline_native_only']
        and sample['actual_VM_descriptor_last_result1_preserved_through_type3_and_end'] and sample['single_end762_actual']
        and sample['original_B22_four_A000_initialization_commands_retained'] and sample['no_source_pause_or_C200_invented']
        and sample['all115_sampled_nontext_regions_and_whole_RGB_town5530_and_final9001_equal']
        and sample['postscene9001_five_native_components_whole_actor_model_and_captain2_equal']
        and sample['source_packed_predicate_and_A000_semantics_not_inferred'] and sample['PRNG_and_future_world_equality_not_claimed']
        and sample['no_open_translation_specific_display_or_control_finding']
        and sample['no_natural_event_eligibility_earned_flags_full_route_or_hardware_claim']
        and sample['actual_selected_B173_source_events']==[] and sample['offline_only_display_IDs']==[],'representative actual approval required')
    paths=[p for p in sample['evidence'] if p.endswith('actual_all11_unforced_predicate_paths_effects_and_end.json')]
    require(len(paths)==1,'one exact actual proof required');actual=load(paths[0])
    require(sha(Path(paths[0]).read_bytes())==sample['evidence'][paths[0]] and not actual['failures'] and not actual['paired_region_differences']
        and actual['complete_matching_observations']==actual['fresh_actual_unique_speech_panels']==11
        and len(actual['versions'])==2 and {v['case'] for v in actual['versions']}=={'clean_Japanese','reviewed_English'}
        and actual['actual_result_words_are_player_descriptor_command_type_and_persistent_VM_last_result'], 'two complete actual paths required')
    require([v['fixture_exit_frame'] for v in actual['versions']]==[5496,5493],'source/English exits differ from observed pair')
    for version in actual['versions']:
        require(version['frames']==9001 and version['single_source_end_offset']==762 and len(version['selected_B22_command_pairs'])==31
            and version['unforced_predicate_result']==1 and version['actual_predicate']['result_words']==[2,1]
            and version['selected_B22_command_pairs'][-1]['result_words']==[0,1]
            and [r['original_source_offset'] for r in version['actual_source_A000s']]==[720,748]
            and [r['result_words'] for r in version['actual_source_A000s']]==[[3,0],[3,1]]
            and [r['original_source_offset'] for r in version['actual_source_relative_commands']]==[736,740,756]
            and all(r['result_words']==[3,1] for r in version['actual_source_relative_commands'])
            and version['source_A000_hex_by_offset']=={'720':'00a0ffff010b39a2','748':'00a0ffff010cca60'}
            and version['source_predicate_hex']=='0080ffff000cca70'
            and [r['word'] for r in version['actual_presentation_commands']]==[0x6000,0x6240]
            and version['actual_presentation_commands'][-1]['result_words']==[3,1]
            and [r['word'] for r in version['actual_resources']]==[0x6329,0x6340]
            and [r['source_offset'] for r in version['unvisited_declared_source_objects']]==[744],
            'actual unforced predicate/effect/relative/termination results differ')
    require(len(native['review_sheets'])==2 and len(sample['viewed_actual_sheets'])==2,'all viewed sheets required')
    for sheet in native['review_sheets']+sample['viewed_actual_sheets']:
        require(sheet['review'].startswith('Viewed') and sha(Path(sheet['path']).read_bytes())==sheet['sha256'],'viewed sheet changed')
''')
    section('    stops = [command for command in commands', '    restored = bytearray(logical)', '''    stops=[c for c in commands if c['word']==0]
    require([c['old_offset'] for c in stops]==[762] and len(stops)==1 and stops[0]['new_offset']==794
        and stops[0]['new_offset']+4==len(logical) and target[794:798]==bytes(4),'single source end differs')
    require([(c['old_offset'],c['new_offset'],4) for c in stops]
        ==[(c['source_offset'],c['target_offset'],c['extent']) for c in spec['original_declared_end_word_maps']],'end map differs')
    leaves=[c for c in commands if c['word'] not in [0x4000,0x100,0x200,0x300,0x400]]
    exact=[(8,'0060'),(10,'2963'),(12,'4063'),(720,'00a0ffff010b39a2'),(728,'0080ffff000cca70'),
        (748,'00a0ffff010cca60'),(760,'4062'),(762,'00000000')]
    require([(c['old_offset'],block[c['old_offset']:c['old_offset']+c['old_native_extent']].hex()) for c in leaves]==exact,'eight complete source leaves differ')
    require([c['word'] for c in leaves]==[0x6000,0x6329,0x6340,0xA000,0x8000,0xA000,0x6240,0]
        and all(c['word'] not in [0x2000,0x2100,0x4100,0xC200] for c in commands),'source effects/predicate/no-pause scope differs')
''')
    old="    require(not edges and not spec['target_native_skip_cases'] and len(logical) == mapped(end) < 0x2400, 'complete relative scope required')"
    assert old in text
    text=text.replace(old,"""    require(len(edges)==4 and [e['offset'] for e in edges]==[736,740,744,756]
        and len(spec['target_native_skip_cases'])==20 and len(logical)==mapped(end)<0x2400,'complete relative scope required')
    for edge in edges:
        cases=[c for c in spec['target_native_skip_cases'] if c['new_offset']==edge['new_offset']]
        require(len(cases)==5 and {c['last_result'] for c in cases}=={0,1,2,3,0xFFFFFFFF},'five original results per relative site required')
        for case in cases:
            last=case['last_result'];taken=edge['word']==0x100 or (edge['word']==0x200 and last==0) or (edge['word']==0x300 and last==1) or (edge['word']==0x400 and last==2)
            destination=edge['new_matched_skip_target'] if taken else edge['new_unmatched_next']
            require(edge['new_offset']+case['native_extent']==destination and case['source_target_preserved_at_mapped_native_boundary']
                and case['ABI_all4MiB_owner_stream_result_length_and_guards_exact'],'source-bound relative operand case differs')""")
    changes={'B172':'B173','focused_repeat_proof':'postscene_native_state_proof',
        "{'revise': 19, 'retain-wording': 8}":"{'revise': 8, 'retain-wording': 3}",
        'len(commands) == 38':'len(commands) == 23','source_commands=38':'source_commands=23','relative_operands=0':'relative_operands=4',
        'all27_progressive_speeches_zero_macros_presentations_resources_C200_A000_and11_leaves_preserved':'all11_progressive_speeches_zero_macros_resources_predicate_relative_suffix_two_A000s_and8_leaves_preserved',
        'actual_two_retained_B22_fixtures_plus_two_state_repeats_not_natural_source_activation':'actual_two_retained_B22_fixtures_and_postscene_exported_state_not_natural_source_activation'}
    for key in changes:assert key in text,key
    text=re.sub('|'.join(re.escape(k) for k in sorted(changes,key=len,reverse=True)),lambda m:changes[m[0]],text)
    tokens=[]
    for token in tokenize.generate_tokens(io.StringIO(text).readline):
        if token.type==tokenize.NUMBER and token.string in {'172','27'}:token=token._replace(string={'172':'173','27':'11'}[token.string])
        tokens.append(token)
    text=tokenize.untokenize(tokens).replace('all27','all11').replace('27 exact speech','11 exact speech')
    assert not re.search(r'B172|\[172\]|== 172|all27|1930|1880|focused_repeat',text)
    compile(text,str(NEW),'exec');NEW.write_text(text,encoding='utf-8',newline='\n')
    ROOT.mkdir(parents=True)
    save(ROOT/'compiler_derivation.json',dict(source=str(OLD),source_sha256=sha(OLD.read_bytes()),target=str(NEW),target_sha256=sha(NEW.read_bytes()),
        producer_sha256=sha(Path(__file__).read_bytes()),source_relative_sites=4,target_operand_cases=20,
        native_parser_outputs_and_actual_VM_descriptor_last_result_distinguished=True,Reika_readonly_names_preserved=True,
        no_shared_metric_or_guard_change=True,full_goal_complete=False))
    print('Prepared B173 atomic compiler:11 speeches,eight exact leaves,four relative sites,predicate/both effects and preserved actual VM result1.')
