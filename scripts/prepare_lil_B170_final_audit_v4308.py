"""Derive an independent complete B170 handoff audit and preservation pins."""
import re
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import save

ROOT = Path('work/analysis/lil_B170_final_audit_tools_v4308')
NEW = Path('scripts/verify_editorial_handoff_v4308.py')

if __name__ == '__main__':
    assert not ROOT.exists() and not NEW.exists()
    old = Path('scripts/verify_editorial_handoff_v4256.py')
    text = old.read_text(encoding='utf-8')
    start = text.index("    assert stored['current_final_stored_macro_alignment_cases']")
    stop = text.index("    actual=read(", start)
    text = text[:start] + '''    assert stored['current_final_stored_macro_alignment_cases']==132
    assert (stored['new_parity_macro_alignment_cases'],stored['exact_byte_identical_reused_macro_alignment_cases'])==(76,56)
    spec=mapping['blocks'][0]
    assert len(spec['command_map'])==45 and not spec['relative_skip_fixups'] and not spec['target_native_skip_cases']
    assert spec['original_declared_end_word_maps']==[
        dict(source_offset=1852,target_offset=1742,extent=4,source_four_zero_bytes_exact=True),
        dict(source_offset=1856,target_offset=1746,extent=4,source_four_zero_bytes_exact=True)]
    assert spec['original2000_pause_and_resume_maps']==[dict(old_offset=0x24,new_offset=32,source_resume=38,target_resume=34,source_two_byte_pause_and_mapped_resumption_boundary_exact=True)]
    assert mapping['source_A000_hex']=='00a0ffff19100120' and mapping['source_A000_raw_hex_words']==['1019','2001']
    assert mapping['source_packed_semantics_not_inferred']
    control=read(doc['relocated_control_proof'])
    assert len(control['relocated_dispatch_cases'])==33 and not control['relocated_predicate_pairs']
    assert len(control['all12_source_current_target_nonrelative_nonspeech_leaves'])==12
    assert len(control['relocated_C200_pairs'])==1 and control['original_C200_queue_and_all_unowned4MiB_preserved_at_relocated_cursor']
    names=read(doc['source_nameplate_consumer_proof'])['native_four_consumer_cases']['rows']
    assert len(names)==4 and all(r['original_scratch_rings'] and r['original_getter_writes'] and r['source_owned_scratch_restoration_or_readonly_path_recovers_all4MiB'] for r in names)
    repeat=read(doc['focused_repeat_proof'])
    assert repeat['paired_post_B170_town11290_whole1A04_actor_models_and_captain2_equal']
    assert len(repeat['cross_language_speech_timing_differences'])==22 and not any(repeat['same_ROM_later_differing_frames'].values())
    assert all(all(r['component_equality'].values()) for r in repeat['paired_native_persistent_state_and_PRNG_samples'] if r['frame']<=16090)
''' + text[stop:]
    changes = {
        'editorial_handoff_verification_v4256': 'editorial_handoff_verification_v4308',
        'lil_B169_completion_v4255': 'lil_B170_completion_v4307',
        "OFFLINE = {'DK4_MES_B169_R0067','DK4_MES_B169_R0082','DK4_MES_B169_R0097'}": 'OFFLINE = set()',
        "'Lil-B169-Mikhail-Proof-legend-clues-ruins-tavern-give-and-take36'": "'Lil-B170-Yifa-collision-apology-Taoist-training-resolve-joining33'",
        'B169': 'B170', 'lil_B169': 'lil_B170',
        'release_v4252': 'release_v4304', 'startup_v4254': 'startup_v4306',
        'all_routes_combined_v4204': 'all_routes_combined_v4251',
        'lil_B169_reference_v4236': 'lil_B170_reference_v4284',
        'all-routes-unified-v4251': 'all-routes-unified-v4303',
        'all-routes-unified-v4204': 'all-routes-unified-v4251',
        'registration_v4250b': 'registration_v4302b',
        'actual_v4244/actual_progressive_three_predicates_full_effect_and_return': 'actual_v4293/actual_all33_pause_resources_A000_C200_and_first_end',
        'transition_review_v4245/all6_sheets_source_effect_and_paired_return_review': 'transition_review_v4297/all6_sheets_figure_pause_effect_C200_and_paired_return_review',
        'actual_source_hex0029_0001_effect': 'actual_source_A000_hex1019_2001',
        "[('clean_Japanese',10776),('reviewed_English',10773)]": "[('clean_Japanese',11257),('reviewed_English',11257)]",
        '(6,3,2)': '(6,4,3)',
        'all_current_requested_and_final_framebuffers_equal_V4204': 'all_current_requested_and_final_framebuffers_equal_V4251',
        '[169]': '[170]', "==169": '==170',
        '(2564,2588)': '(1860,1752)',
        '[2,6,9,20,21,76]': '[2,25]',
        "{'FI':5,'FA':0,'FO':2}": "{'FI':1,'FA':0,'FO':1}",
        "units[family['id']]['new_emulator_runs']==4": "units[family['id']]['new_emulator_runs']==6",
        "'promoted_main_build_v4226']": "'promoted_main_build_v4226','promoted_main_build_v4289']",
        'unfinished_editorial_scope_v4255': 'unfinished_editorial_scope_v4307',
        'remaining_B170_B180': 'remaining_B171_B180',
        'V4255': 'V4307', 'V4204': 'V4251',
        "len(manifest['batches'])==545": "len(manifest['batches'])==546",
        'manifest_batches=545': 'manifest_batches=546',
        'all53_commands12_spans60_skips144_stored_cases_three_predicates_names_macros_and_corrected_A000_operands_bound': 'all45_commands_zero_spans132_stored_cases_pause_resources_C200_both_ends_names_and_macros_bound',
        'three_conditional_remarks_explicitly_offline_only': 'all33_observed_second_end_explicitly_offline_only',
        '545/114 stack': '546/114 stack',
    }
    for key in changes:
        assert key in text, key
    text = re.sub('|'.join(re.escape(k) for k in sorted(changes, key=len, reverse=True)), lambda m: changes[m.group()], text)
    counts = {'5692':'5725','5695':'5728','3614':'3635','2078':'2090','3839':'3872','4093':'4126','36':'33','19':'21','17':'12','55':'63','231':'198'}
    text = re.sub(r'(?<!\d)(?:'+'|'.join(re.escape(k) for k in sorted(counts,key=len,reverse=True))+r')(?!\d)', lambda m: counts[m.group()], text)
    assert 'B169' not in text and 'B120' not in text
    compile(text,str(NEW),'exec')
    NEW.write_text(text,encoding='utf-8',newline='\n')
    tools = [dict(previous=str(old),previous_sha256=sha(old.read_bytes()),successor=str(NEW),successor_sha256=sha(NEW.read_bytes()))]
    tools.append(derive('scripts/pin_lil_B169_v4255.py','scripts/pin_lil_B170_v4307.py',{
        'all_routes_combined_v4251':'all_routes_combined_v4303',
        'lil_B169_reference_v4236':'lil_B170_reference_v4284',
        'lil_B169_display_v4241':'lil_B170_display_v4291',
        'lil_B169_release_v4252':'lil_B170_release_v4304',
        'B169 V4251':'B170 V4303',
    }))
    ROOT.mkdir(parents=True)
    save(ROOT/'source_derivation.json',dict(tools=tools,expected_reviews=5725,expected_source_prose=5728,expected_new_completions=33,
        all_prior_completions_and_wider_scope_must_match=True,main_V4251_preserved=True,no_new_credit_by_this_producer=True,full_goal_complete=False))
