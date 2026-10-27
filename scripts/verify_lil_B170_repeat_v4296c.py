"""Compare focused repeats, post-scene actor state and later same-ROM divergence."""
import json
import struct
from pathlib import Path
from scripts.verify_market_gameplay_v753 import state
from scripts.verify_shipyard_gameplay_v760 import models
from scripts.verify_tavern_gameplay_v767 import persistent_objects
from scripts.verify_followup_gameplay_v778 import tasks
from scripts.verify_ceremony_prayer_gameplay_v814 import calendar
from PIL import Image, ImageChops
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/lil_B170_repeat_verification_v4296c')
BASE = Path('E:/Rota Nova translations/Generated/work/emulation_v193')
FIXTURE = Path('work/analysis/lil_B170_display_fixture_v4291/complete_effect_preserving_B22_fixtures.json')


def trace_pairs(trace, fixture):
    source = {r['fixture_offset']: r for r in fixture['selected_original_objects']}
    rows, pairs = trace['rows'], []
    assert not trace['errors'] and not trace['mismatches'] and trace['all_host_slots_restored_and_core_file_exact']
    for row in rows:
        assert row['CPU_WRAM_DTCM_ITCM_and_configuration_unchanged_by_callback']
        if row['kind'] != 'after_command':
            continue
        entry = rows[row['entry_row']]
        if entry['source']['block'] != 22:
            continue
        at = entry['source']['instruction_offset']
        original = source.get(at)
        pairs.append(dict(source_offset=None if original is None else original['source_offset'],
            word=int(entry['source']['first_word']), start=entry['frame'], returned=row['frame'], result_words=row['result_words']))
    assert len(pairs) == 53 and pairs[-1]['source_offset'] == 1852 and pairs[-1]['returned'] == 11257
    return pairs


if __name__ == '__main__':
    assert not ROOT.exists()
    fixture = read(FIXTURE)
    for case in ['clean_Japanese', 'reviewed_English']:
        assert read(Path('work/analysis/lil_B170_repeat_run_v4295_' + case) / 'terminal.json')['terminal']
    runs, states, flows, evidence = [], [], [], {str(FIXTURE): sha(FIXTURE.read_bytes())}
    for item in fixture['fixtures']:
        case = item['case']
        folder = BASE / ('lil_B170_repeat_v4295_' + case)
        run = Path('work/analysis/lil_B170_repeat_run_v4295_' + case)
        paths = [run / 'terminal.json', run / 'run_plan.json', folder / 'capture_report.json', folder / 'observer/commands.json']
        terminal, plan, report, trace = map(read, paths)
        assert terminal['terminal'] and terminal['observer_host_slots_restored']
        assert report['frames'] == 20001 and report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
        assert report['ROM_sha256'] == item['research_ROM_sha256'] == sha(Path(item['research_ROM']).read_bytes())
        assert plan['focused_repeat_for_later_sailing_divergence'] and plan['post_B170_town_RAM_requested_at11290']
        assert not any(v for k, v in report.items() if k.startswith('synthetic_'))
        assert sha(Path(plan['original_inputs']).read_bytes()) == plan['inputs_sha256']
        old_folder = BASE / ('lil_B170_display_v4292_' + case)
        old_report = read(old_folder / 'capture_report.json')
        old_trace = read(old_folder / 'observer/commands.json')
        assert report['scripted_input_schedule'] == old_report['scripted_input_schedule']
        assert report['core_DLL_sha256'] == old_report['core_DLL_sha256'] and report['core_options'] == old_report['core_options']
        current_flow, old_flow = trace_pairs(trace, item), trace_pairs(old_trace, item)
        assert current_flow == old_flow
        flows.append(current_flow)
        photographs = {p['frame']: p for p in report['frames_captured']}
        old_photos = {p['frame']: p for p in old_report['frames_captured']}
        comparisons = []
        for frame, photo in photographs.items():
            before = old_photos[frame]
            for p in [before, photo]:
                assert sha(Path(p['path']).read_bytes()) == p['PNG_sha256']
            a, b = [Image.open(p['path']).convert('RGB') for p in [before, photo]]
            diff = ImageChops.difference(a, b)
            equal = not diff.getbbox()
            if frame <= 11290:
                assert equal, (case, frame)
            comparisons.append(dict(frame=frame, first=before['path'], first_sha256=before['PNG_sha256'], repeat=photo['path'], repeat_sha256=photo['PNG_sha256'], whole_RGB_equal=equal, differing_RGB_bounds=diff.getbbox()))
        snapshot = next(s for s in report['read_only_capture_RAM_snapshots'] if s['frame'] == 11290)
        raw = Path(snapshot['path']).read_bytes()
        assert snapshot['read_only_export'] and len(raw) == 0x400000 and sha(raw) == snapshot['sha256']
        arm = NdsImage.open(item['research_ROM']).read_file('/__arm9__.bin')
        cpu, get = get_machine(arm, raw)
        root, captain = get(0xCB184), get(0x7F244)
        assert captain == 2 and 0x02000000 <= root <= 0x02400000 - 0x1A04
        model = bytes(cpu.mem_read(root, 0x1A04))
        states.append(model)
        runs.append(dict(case=case, ROM_sha256=item['research_ROM_sha256'], same_ROM_first_repeat_frame_comparisons=comparisons,
            B170_all53_command_times_results_and_first_end_equal_first_run=True,
            town11290_RAM=snapshot, native_actor_model_root=root, native_actor_model_bytes=len(model), native_actor_model_sha256=sha(model), captain_ID=captain,
            native_model_reader='original_CB184;original7F244;whole1A04_actor_model_copy',
            native_getters_run_on_exported_copy_only=True, first_report=str(old_folder / 'capture_report.json'), repeat_report=str(folder / 'capture_report.json')))
        evidence.update({str(p): sha(p.read_bytes()) for p in paths + [old_folder / 'capture_report.json', old_folder / 'observer/commands.json', Path(snapshot['path'])]})
    assert states[0] == states[1]
    shape = lambda rows: [(r['source_offset'], r['word'], r['result_words']) for r in rows]
    assert shape(flows[0]) == shape(flows[1])
    timing_differences = [dict(source=a, English=b) for a, b in zip(*flows, strict=True) if a != b]
    assert len(timing_differences) == 22 and all(r['source']['word'] == r['English']['word'] == 0x4000 for r in timing_differences)
    component_functions = [state, models, persistent_objects, tasks, calendar]
    state_samples, samples = [], []
    arms = []
    for case in ['clean_Japanese', 'reviewed_English']:
        report = read(BASE / ('lil_B170_repeat_v4295_' + case) / 'capture_report.json')
        arm = NdsImage.open(report['ROM']).read_file('/__arm9__.bin')
        arms.append(arm)
        capture_samples = {}
        for snapshot in report['read_only_capture_RAM_snapshots']:
            raw = Path(snapshot['path']).read_bytes()
            assert len(raw) == 0x400000 and sha(raw) == snapshot['sha256']
            values = {fn.__name__: fn(arm, raw) for fn in component_functions}
            capture_samples[snapshot['frame']] = dict(seed=struct.unpack_from('<I', raw, 0x168EB8)[0], values=values, RAM=snapshot)
        samples.append(capture_samples)
    assert arms[0] == arms[1]
    clean_arm = NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    source_spans = []
    for name, start, end in [('input_wait', 0xC9C80, 0xC9CD0), ('discarded_RAND_yield', 0xC9D98, 0xC9DF0), ('generator', 0xD9834, 0xD9870), ('positive_modulus_wrapper', 0x519D4, 0x51A10)]:
        assert arms[0][start:end] == clean_arm[start:end]
        source_spans.append(dict(name=name, start=0x02000000 + start, end=0x02000000 + end, clean_current_bytes_exact=True, sha256=sha(arms[0][start:end])))
    for frame, a in samples[0].items():
        b = samples[1][frame]
        equal = {key: a['values'][key] == b['values'][key] for key in a['values']}
        if frame <= 16090:
            assert all(equal.values()), (frame, equal)
        assert (a['seed'] == b['seed']) == (frame == 3250)
        state_samples.append(dict(frame=frame, source_seed=a['seed'], English_seed=b['seed'], component_equality=equal,
            source_component_hashes={key: sha(json.dumps(value, sort_keys=True).encode()) for key, value in a['values'].items()},
            English_component_hashes={key: sha(json.dumps(value, sort_keys=True).encode()) for key, value in b['values'].items()},
            source_RAM=a['RAM'], English_RAM=b['RAM']))
    assert len(state_samples) == 5
    earlier_cause = Path('docs/ceremony_random_cause_v824_checkpoint.md')
    assert '020C9DA0' in earlier_cause.read_text(encoding='utf-8')
    evidence[str(earlier_cause)] = sha(earlier_cause.read_bytes())
    repeat_variation = {r['case']: [p['frame'] for p in r['same_ROM_first_repeat_frame_comparisons'] if not p['whole_RGB_equal']] for r in runs}
    ROOT.mkdir(parents=True)
    save(ROOT / 'post_B170_actor_captain_and_same_ROM_repeat_comparison.json', dict(runs=runs,
        paired_post_B170_town11290_whole1A04_actor_models_and_captain2_equal=True,
        each_same_ROM_repeat_all53_command_times_results_and_first_end_equal=True, cross_language_command_order_results_and_first_end_equal=True, cross_language_speech_timing_differences=timing_differences,
        same_ROM_later_differing_frames=repeat_variation,
        later_sailing_divergence_reproduces_without_translation_change=any(repeat_variation.values()),
        earlier_two_runs_differ_after_B170_and_following_B120_exits=True,
        no_B170_text_pause_figure_resource_A000_C200_or_town_return_difference=True,
        paired_native_persistent_state_and_PRNG_samples=state_samples, original_input_wait_yield_generator_and_wrapper_source_spans=source_spans, prior_scheduler_entropy_evidence=str(earlier_cause), prior_scheduler_entropy_evidence_sha256=sha(earlier_cause.read_bytes()), mechanism_scope='Different speech return frames and shared PRNG seeds are observed; all persistent component fingerprints match through town return11290 and departure16090. Source wait/yield/generator spans are rebound byte-exactly to the earlier scheduler-entropy finding. This is consistent with that mechanism, not a fresh every-RAND-call B170 causal trace. No random outcomes, seed or instruction was forced.', no_RTC_or_every_RAND_call_trace_claim=True,
        raw_RAM_full_equality_not_claimed_component_scopes_explicit=True, preserved_overstrict_verifier='scripts/verify_lil_B170_repeat_v4296.py', preserved_failure_reason='All actor bytes agree. Cross-language command timestamps differ for22 speeches,so the combined strict actor-and-timing assertion failed. Same-ROM repeats and source control order/results pass.',
        fresh_cold_boots_in_this_focus=2, source_event170_eligibility_or_earned_recruitment_not_claimed=True,
        evidence={**evidence, str(Path(__file__)): sha(Path(__file__).read_bytes())}, full_goal_complete=False))
    print(dict(post_B170_actor_models_equal=True, captain=2, same_ROM_later_differing_frames=repeat_variation, new_focused_runs=2))
