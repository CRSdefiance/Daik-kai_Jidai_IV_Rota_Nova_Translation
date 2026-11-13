"""Independently gate the actual/reference checkpoint while preserving unequal RNG."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read

def audit_actual(entry):
    from scripts.prepare_lil_B180_checkpoint_v4817 import EVIDENCE
    from scripts.seal_lil_B180_references_v4816 import VISUAL,ACTUAL,MAP,OUTPUT
    for p in EVIDENCE:assert entry['evidence'][str(Path(p))]==sha(Path(p).read_bytes())
    visual,actual,mapping,doc=map(read,[VISUAL,ACTUAL,MAP,OUTPUT])
    assert entry['records']==doc['records'] and entry['new_ROMs']==2 and entry['new_emulator_runs']==4
    assert entry['registered_release_pending'] and entry['relocation_actual_and_references_approved']
    assert actual['complete_matching_observations']==actual['fresh_actual_unique_speech_panels']==11
    assert not actual['failures'] and not actual['paired_region_differences']
    assert [len(v['selected_B22_command_pairs']) for v in actual['versions']]==[31,26]
    assert [v['fixture_exit_frame'] for v in actual['versions']]==[5495,5496]
    assert actual['observed_random_path_difference']['original_effects_by_case']==dict(clean_Japanese=[504],reviewed_English=[472])
    assert visual['actual_new_cold_boot_runs']==4 and visual['total_frames']==30004
    assert len(visual['all2_actual_sheets_viewed'])==2 and len(visual['paired_full_screen_views'])==9
    assert all(s['viewed'] for s in visual['all2_actual_sheets_viewed']+visual['paired_full_screen_views'])
    assert len(visual['all115_sampled_nontext_region_checks'])==visual['nontext_equal_samples']==115
    assert visual['exact_timing_difference_counts']==dict(total=12,speech=8,control_or_end=4)
    assert len(visual['sampled_postscene_whole_RGB_differences_unmasked'])==12
    assert visual['postscene9001_native_component_equality']['persistent_objects'] is False
    assert visual['PRNG_equality'] is False and visual['postscene9001_PRNG_seeds']==[2467799992,790984746]
    assert visual['measured_persistent_town_difference_resolved_to_original_effect']
    effect=read(visual['effect_boundary_proof'])
    assert effect['final9001_four_array_differences']['all90_towns']==[dict(offset=1294,before=59,after=61)]
    assert effect['no_unresolved_translation_specific_state_difference_within_checked_arrays']
    for p,h in visual['evidence'].items():assert sha(Path(p).read_bytes())==h
    for s in visual['all2_actual_sheets_viewed']+visual['paired_full_screen_views']:assert sha(Path(s['path']).read_bytes())==s['sha256']
    b=mapping['blocks'][0]
    assert b['block']==180 and len(b['command_map'])==28 and len(b['text_records'])==11
    assert len(b['relative_skip_fixups'])==10 and len(b['target_native_skip_cases'])==50
    assert mapping['actual_sampled_display_IDs']==[r['id'] for r in doc['records']]
    assert entry['approved_uncredited_objects']==11 and entry['source_prose_or_completion_credit_added']==0
