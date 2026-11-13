"""Derive a readable B169 atomic compiler from the prior complete-block adapter."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import save

ROOT = Path('work/analysis/lil_B169_compiler_tools_v4249')
OLD = Path('dk4tool/patch/lil_B168_editorial_v1.py')
NEW = Path('dk4tool/patch/lil_B169_editorial_v1.py')

if __name__ == '__main__':
    assert not ROOT.exists() and not NEW.exists()
    text = OLD.read_text(encoding='utf-8')
    def change(old,new):
        global text
        assert old in text,old
        text = text.replace(old,new)
    def section(start,stop,new):
        global text
        a,b = text.index(start),text.index(stop,text.index(start))
        text = text[:a]+new+text[b:]
    section("    require(len(native['cases'])",'    for key, count in',
        "    require(len(native['cases']) == 36 and native['current_original_macro_alignment_calls'] == 288\n"
        "            and native['all36_current_native_speech_planes_pass'] and native['progressive_planes'] == 36\n"
        "            and native['FE_planes'] == 0, 'complete native progressive proof required')\n")
    section("    require(names['source_printable57", "    require(sample['actual_two_disclosed",
        "    require(names['source_15_selector_is_Ian21_not_literal_control_to_strip'] and names['source_printable4C_is_Mikhail76_not_literal_L']\n"
        "            and names['later_older_record0D_reaudit_stays_open'] and names['approved_prose_names'] ==\n"
        "            {'2':'Lil','6':'Julio','9':'Camille','20':'Fernando Dias','21':'Ian','76':'Mikhail'}, 'source-owned identities required')\n"
        "    name_cases = names['native_twelve_consumer_cases']['rows']\n"
        "    require(len(name_cases) == 12 and {case['actor_ID'] for case in name_cases} == SELECTORS\n"
        "            and all(case['all_actor_models_and_unowned4MiB_exact'] and case['source_owned_scratch_restoration_or_readonly_path_recovers_all4MiB'] for case in name_cases), 'complete original name paths required')\n"
        "    require(all(case['original_scratch_rings'] and case['original_getter_writes'] for case in name_cases), 'all twelve owned scratch paths required')\n")
    section("        require(case['geometry']",'        at, sa =',
        "        require(not fe and case['complete_native_independent216x64_plane_equal'], 'one progressive216x64 consumer required')\n")
    changes = {
        'Atomic complete B168 localization: progressive/FE text and source-owned control flow.':'Atomic complete B169 localization: progressive text and source-owned control flow.',
        'lil_B168_layout_v3':'lil_B169_layout_v2','lil_B168_profile':'lil_B169_profile',
        'lil_B168_editorial_release_v1':'lil_B169_editorial_release_v1',
        'SELECTORS = {2, 6, 9, 20, 76, 87, 165, 166, 254}':'SELECTORS = {2, 6, 9, 20, 21, 76}',
        'all82_commands12_relative_sites60_target_skips_verified':'all53_commands12_relative_sites60_target_skips_verified',
        'all54_active_speech_targets_preserved':'all36_active_speech_targets_preserved',
        'all16_leaves_three_predicates_four_resources_six_presentations_one_effect_and_two_ends_exact':'all5_leaves_three_predicates_one_effect_and_one_end_exact',
        'two_consecutive_declared_endwords_preserved':'single_declared_tail_endword_preserved',
        'three_FE_null_actor_consumers_and_FI7_FA1_FO1_preserved':'no_FE_consumers_and_FI5_FO2_preserved',
        "['DK4_MES_B168_R0020', 'DK4_MES_B168_R0048', 'DK4_MES_B168_R0135']":"['DK4_MES_B169_R0067', 'DK4_MES_B169_R0082', 'DK4_MES_B169_R0097']",
        'B168':'B169','all54_five_review_gates_true':'all36_five_review_gates_true',
        "'scoped_profile_module']":"'scoped_profile_module', 'source_effect_operand_notation_amendment']",
        "('source_consumer_negative_controls', 26)":"('source_consumer_negative_controls', 21)",
        "('source_macro_preservation_negatives', 3)":"('source_macro_preservation_negatives', 2)",
        "stored['current_final_stored_macro_alignment_cases'] == 216":"stored['current_final_stored_macro_alignment_cases'] == 144",
        'all54_final_targets_complete_native_planes_equal_reviewed_planes':'all36_final_targets_complete_native_planes_equal_reviewed_planes',
        "len(controls['all16_source_current_target_nonrelative_nonspeech_leaves']) == 16":"len(controls['all5_source_current_target_nonrelative_nonspeech_leaves']) == 5",
        'all51_progressive_and3_null_actor_FE_consumers_FI7_FA1_FO1_exact':'all36_progressive_consumers_FI5_FO2_exact',
        "ends['all4_declared_end_decodes_return_type0_extent4_without_post_payload_read'] and len(ends['cases']) == 4":"ends['all2_declared_end_decodes_return_type0_extent4_without_post_payload_read'] and len(ends['cases']) == 2",
        'B168_first_end_precedes_second_end_and_declared_logical_end':'B169_single_end_finishes_declared_logical_end',
        'four guarded end decodes required':'two guarded end decodes required',
        'actual51_panels_three_FE_and_normal_return_pass':'actual33_progressive_panels_and_normal_return_pass',
        "(20 if case['id'].endswith('0135') else 6)":"{'DK4_MES_B169_R0067':6,'DK4_MES_B169_R0082':21,'DK4_MES_B169_R0097':20}[case['id']]",
        'actual_progressive_FE_three_predicates_full_effect_and_return':'actual_progressive_three_predicates_full_effect_and_return',
        "actual['fresh_actual_unique_speech_panels'] == 51":"actual['fresh_actual_unique_speech_panels'] == 33",
        "version['source_end_offset'] == 2906":"version['source_end_offset'] == 2558",
        "len(version['selected_B22_command_pairs']) == 81":"len(version['selected_B22_command_pairs']) == 53",
        'actual_source_recruitment_effect':'actual_source_hex0029_0001_effect',
        "== 2582":"== 2550",
        "len(native['review_sheets']) == 7 and len(sample['viewed_actual_sheets']) == 9":"len(native['review_sheets']) == 5 and len(sample['viewed_actual_sheets']) == 6",
        "{'progressive': 51, 'system-FE': 3}":"{'progressive': 36}",
        "{'revise': 28, 'retain-wording': 26}":"{'revise': 19, 'retain-wording': 17}",
        '54 exact speech records required':'36 exact speech records required',
        "== 168":"== 169",'[168]':'[169]','block=168':'block=169',
        'complete_native_independent_plane_equal':'complete_native_independent216x64_plane_equal',
        'all_visible_origins_zero_and_native_rows_within4rows':'all_visible_origins_zero_and16px_rows_within4rows',
        "{b'FI': 7, b'FA': 1, b'FO': 1}":"{b'FI': 5, b'FO': 2}",
        'len(commands) == 82':'len(commands) == 53',
        "[2906, 2910] and len(stops) == 2":"[2558] and len(stops) == 1",
        "stops[0]['new_offset'] + 4 == stops[1]['new_offset'] and ":'',
        'consecutive source ends differ':'single source end differs',
        '== [0x6342, 0x630B, 0x6300, 0x6301]':'== []',
        'source_commands=82':'source_commands=53',
        'all54_speeches_three_FE_macros_twelve_spans_and16_leaves_preserved':'all36_progressive_speeches_macros_twelve_spans_and5_leaves_preserved',
        '== 54':'== 36',
    }
    # Longer replacements take precedence so a broad scope rename cannot hide a contract.
    import re
    for old in changes:
        assert old in text,old
    text = re.sub('|'.join(re.escape(k) for k in sorted(changes,key=len,reverse=True)),lambda m:changes[m.group()],text)
    anchor = "    native, stored, controls, sample, ends, names = [load(doc[key]) for key in proof_keys[:6]]\n"
    assert anchor in text
    text = text.replace(anchor,anchor+
        "    amendment = load(doc['source_effect_operand_notation_amendment'])\n"
        "    require(mapping['source_effect_operand_hex_values'] == amendment['operand_hex_values'] == ['0029','0001']\n"
        "            and mapping['source_effect_operand_decimal_values'] == amendment['operand_decimal_values'] == [41,1]\n"
        "            and amendment['source_command_hex'] == '00a0ffff29000100', 'source A000 operand notation differs')\n")
    assert 'B168' not in text and 'lil_B168' not in text
    compile(text,str(NEW),'exec')
    NEW.write_text(text,encoding='utf-8',newline='\n')
    ROOT.mkdir(parents=True)
    save(ROOT/'source_derivation.json',dict(previous=str(OLD),previous_sha256=sha(OLD.read_bytes()),successor=str(NEW),successor_sha256=sha(NEW.read_bytes()),
        scope=dict(speeches=36,progressive=36,commands=53,relative_sites=12,target_skip_cases=60,leaves=5,predicates=3,A000=1,ends=1,FI=5,FO=2),
        source_A000_hex_values=['0029','0001'],source_A000_decimal_values=[41,1],positive_and_negative_execution_pending=True,
        no_registry_ROM_orcredit_change=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('Readable atomic B169 compiler prepared;36 progressive objects,all53 commands and exact hex0029/0001 notation required. Execution pending.')
