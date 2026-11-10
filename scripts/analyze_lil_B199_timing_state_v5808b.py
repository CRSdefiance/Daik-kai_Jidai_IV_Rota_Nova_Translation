"""Measure the actual small dialogue timing drift and final native state without masking it."""
from pathlib import Path
import inspect
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_market_gameplay_v753 import state
from scripts.verify_shipyard_gameplay_v760 import models
from scripts.verify_tavern_gameplay_v767 import persistent_objects
from scripts.verify_followup_gameplay_v778 import tasks
from scripts.verify_ceremony_prayer_gameplay_v814 import calendar
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B199_timing_state_v5808b')
ACTUAL=Path('work/analysis/lil_B199_actual_v5807/thirty_one_actual_panels_source_matched_controls_and_complete_native_holds.json')
if __name__=='__main__':
    assert not ROOT.exists();actual=read(ACTUAL);reports=[];native=[];snapshots=[];arms=[]
    for version in actual['versions']:
        report=read(version['capture_report']);snapshot=report['read_only_RAM_snapshot']
        raw=Path(snapshot['path']).read_bytes();assert snapshot['read_only_export'] and len(raw)==4194304 and sha(raw)==snapshot['sha256']
        image=NdsImage.open(report['ROM']);arm=image.read_file('/__arm9__.bin');arms.append(arm)
        assert sha(Path(report['ROM']).read_bytes())==report['ROM_sha256']
        values={fn.__name__:fn(arm,raw) for fn in [state,models,persistent_objects,tasks,calendar]}
        values['tasks']=dict(bytes=len(values['tasks']),sha256=sha(values['tasks']))
        native.append(values);reports.append(report);snapshots.append(snapshot)
    assert arms[0]==arms[1]
    equality={k:native[0][k]==native[1][k] for k in native[0]}
    first,second=[v['command_pairs'] for v in actual['versions']]
    assert [(r['source_offset'],r['word'],r['native_result']) for r in first]==[(r['source_offset'],r['word'],r['native_result']) for r in second]
    changes=[]
    for source,english in zip(first,second,strict=True):
        before,after=[v['returned']-v['start'] for v in [source,english]]
        if before!=after:
            changes.append(dict(source_offset=source['source_offset'],word=source['word'],source_duration=before,English_duration=after,duration_delta=after-before))
    assert len(changes)==6 and all(r['word']==0x4000 for r in changes)
    assert [r['duration_delta'] for r in changes]==[3,-4,3,-1,-4,5]
    assert len(actual['actual_timing_differences'])==34
    assert [v['fixture_exit_frame'] for v in actual['versions']]==[10776,10778]
    later=actual['later_whole_RGB_differences'];assert len(later)==6
    assert all(r['nontext_region_difference_bbox'] is None and
        224<=r['difference_bbox'][0]<=r['difference_bbox'][2]<=240 and
        360<=r['difference_bbox'][1]<=r['difference_bbox'][3]<=376 for r in later)
    seeds=[int.from_bytes(Path(s['path']).read_bytes()[0x168EB8:0x168EBC],'little') for s in snapshots]
    assert seeds==[2490278034,720570979]
    ROOT.mkdir(parents=True)
    save(ROOT/'six_speech_duration_changes_34_shifted_pairs_prompt_bounds_and_native_state.json',dict(
        actual_proof=str(ACTUAL),actual_proof_sha256=sha(ACTUAL.read_bytes()),
        exact_command_shape_results_and_input_schedule_equal=True,
        source_and_English_return_frames=[10776,10778],six_actual_speech_duration_changes=changes,
        shifted_start_or_return_pairs=34,all_nonspeech_pause_picture_resource_effect_and_end_durations_equal=True,
        maximum_absolute_speech_duration_delta=5,all31_complete_native_panels_and120_holds_match=True,
        later_whole_RGB_differences_unmodified=later,later_differences_bounded_to_16x16_advance_prompt_region=True,
        no_pixels_masked_retimed_or_edited=True,advance_prompt_identity_requires_returned_whole_screen_views=True,
        native_final_component_equality=equality,native_final_component_values=native,
        native_getters_applied_to_exported_copies_only=True,original_native_getters={fn.__name__:inspect.getsource(fn) for fn in [state,models,persistent_objects,tasks,calendar]},
        final_snapshots=snapshots,final_13001_PRNG_seeds=seeds,final_PRNG_seeds_equal=False,
        PRNG_difference_preserved_not_removed_or_reseeded=True,complete_RNG_timing_cause_not_traced=True,
        no_full_RAM_future_random_sequence_or_broad_world_equivalence_claim=True,
        no_new_emulator_boot_or_forced_state=True,no_review_credit=True,
        evidence={str(p):sha(p.read_bytes()) for p in [ACTUAL,Path(__file__)]},full_goal_complete=False))
    print(dict(component_equality=equality,speech_duration_changes=6,shifted_pairs=34,prompt_region_differences=6,returns=[10776,10778],PRNG=seeds))
