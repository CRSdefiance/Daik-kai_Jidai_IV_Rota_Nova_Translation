"""Measure both final source/English exports without replay, retiming or simulation assumptions."""
import inspect
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_market_gameplay_v753 import state
from scripts.verify_shipyard_gameplay_v760 import models
from scripts.verify_tavern_gameplay_v767 import persistent_objects
from scripts.verify_followup_gameplay_v778 import tasks
from scripts.verify_ceremony_prayer_gameplay_v814 import calendar
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B221_later_v7005')
ACTUAL=Path('work/analysis/lil_B221_English_actual_v7004/two_English_choices_all14_speeches30_native_pages_complete_masks_and_source_differences.json')
if __name__=='__main__':
    assert not ROOT.exists()
    doc=read(ACTUAL);source=read(doc['source_actual_proof']);measurements=[];evidence=[ACTUAL,Path(doc['source_actual_proof']),Path(__file__)]
    assert not doc['failures'] and doc['all_jobs_terminal_and_reaped']
    for version in doc['versions']:
        selected=version['selected_original_option'];src=next(r for r in source['versions'] if r['selected_original_option']==selected)
        values=[];following=[]
        for language,proof,rom in [('source',src,read(source['fixture'])['fixtures'][0]['research_ROM']),('English',version,doc['research_ROM'])]:
            snap=proof['final_snapshot'];raw=Path(snap['path']).read_bytes()
            assert snap['read_only_export'] and len(raw)==4194304 and sha(raw)==snap['sha256']
            arm=NdsImage.open(rom).read_file('/__arm9__.bin')
            assert sha(arm)=='aa5a7ed159f33fb8ca5dafdfc068ebc69cf9de0469ffe8eba388d3b954e20d05'
            cpu,get=get_machine(arm,raw);root=get(0xCB184);assert get(0x7F244)==2
            groups={fn.__name__:fn(arm,raw) for fn in [state,models,persistent_objects,tasks,calendar]}
            groups['tasks']=dict(bytes=len(groups['tasks']),sha256=sha(groups['tasks']))
            values.append(dict(language=language,snapshot=snap,components=groups,
                whole_actor_sha256=sha(bytes(cpu.mem_read(root,0x1A04))),captain_ID=2,
                seed=int.from_bytes(raw[0x168EB8:0x168EBC],'little')))
            following.append(dict(language=language,B120_end_frames=[r['frame'] for r in proof['following_native_commands'] if r['block']==120 and r['word']==0 and r['native_result'][0]==0],
                all_following_commands=proof['following_native_commands']))
            evidence.append(Path(snap['path']))
        comparisons=version['command_comparison_differences']
        durations=[]
        for before,after in zip(src['command_pairs'],version['command_pairs'],strict=True):
            assert (before['source_offset'],before['word'],before['native_result'])==(after['source_offset'],after['word'],after['native_result'])
            first=before['returned']-before['start'];second=after['returned']-after['start']
            if first!=second:durations.append(dict(source_offset=before['source_offset'],word=before['word'],source_duration=first,English_duration=second,delta=second-first))
        measurements.append(dict(selected_original_option=selected,final_native_values=values,
            five_native_component_equality={k:values[0]['components'][k]==values[1]['components'][k] for k in values[0]['components']},
            whole_actor_and_captain_equal=values[0]['whole_actor_sha256']==values[1]['whole_actor_sha256'],
            final_PRNG_equal=values[0]['seed']==values[1]['seed'],final_PRNG_seeds=[v['seed'] for v in values],
            following_B120=following,source_English_scene_exits=[src['exit_frame'],version['exit_frame']],
            command_comparison_differences=comparisons,command_duration_changes=durations,
            command_result_differences=[d for d in comparisons if 'native_result' in d['different_fields']],
            command_UI_word_differences=[d for d in comparisons if 'UI_after' in d['different_fields']],
            command_timing_difference_count=sum(any(k in d['different_fields'] for k in ['start','returned']) for d in comparisons),
            command_RNG_difference_count=sum(any(k in d['different_fields'] for k in ['before_RNG','after_RNG']) for d in comparisons),
            later_sampled_RGB_differences=[r for r in version['later_sampled_whole_frame_comparisons'] if not r['whole_RGB_equal']],
            total_later_sampled_frames=len(version['later_sampled_whole_frame_comparisons'])))
    ROOT.mkdir(parents=True)
    save(ROOT/'both_choices_final_components_and_measured_timing_RNG_RGB_limits.json',dict(
        actual_proof=str(ACTUAL),actual_proof_sha256=sha(ACTUAL.read_bytes()),
        source_actual_proof=doc['source_actual_proof'],source_actual_proof_sha256=doc['source_actual_proof_sha256'],
        measurements=measurements,all_original_command_result_words_agree=True,
        native_getters_apply_only_to_readonly_exported_copies=True,
        original_final_getter_sources={fn.__name__:inspect.getsource(fn) for fn in [state,models,persistent_objects,tasks,calendar]},
        actual_body_name_page_choice_and_normal_return_checks_pass_independently=True,
        no_new_boot_state_mutation_controller_retiming_or_RNG_force=True,
        no_full_RAM_every_frame_future_sequence_broad_simulation_or_complete_causal_claim=True,
        all_measured_differences_retained_for_later_older_record_technical_reaudit=True,
        final_source_and_English_full_frames_require_explicit_visual_review=True,
        new_emulator_runs=0,new_credit=0,evidence={str(p):sha(p.read_bytes()) for p in evidence},full_goal_complete=False))
    for row in measurements:
        print(dict(choice=row['selected_original_option'],components=row['five_native_component_equality'],actors_equal=row['whole_actor_and_captain_equal'],
            seeds=row['final_PRNG_seeds'],exits=row['source_English_scene_exits'],timing=row['command_timing_difference_count'],RNG=row['command_RNG_difference_count'],
            UI_differences=len(row['command_UI_word_differences']),later_RGB_differences=len(row['later_sampled_RGB_differences']),later_samples=row['total_later_sampled_frames']))
