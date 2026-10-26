"""Preserve an overstrict cross-language timing gate; bind actual state and PRNG."""
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import save

ROOT = Path('work/analysis/lil_B170_repeat_verifier_tools_v4296b')

if __name__ == '__main__':
    assert not ROOT.exists()
    old = Path('scripts/verify_lil_B170_repeat_v4296.py').read_text(encoding='utf-8')
    gate = "    assert states[0] == states[1] and flows[0] == flows[1]\n"
    reconciliation = '''    assert states[0] == states[1]
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
'''
    tool = derive('scripts/verify_lil_B170_repeat_v4296.py', 'scripts/verify_lil_B170_repeat_v4296b.py', {
        "from pathlib import Path": "import json\nimport struct\nfrom pathlib import Path\nfrom scripts.verify_market_gameplay_v753 import state\nfrom scripts.verify_shipyard_gameplay_v760 import models\nfrom scripts.verify_tavern_gameplay_v767 import persistent_objects\nfrom scripts.verify_followup_gameplay_v778 import tasks\nfrom scripts.verify_ceremony_prayer_gameplay_v814 import calendar",
        'repeat_verification_v4296': 'repeat_verification_v4296b',
        gate: reconciliation,
        "'all_four_runs_B17053_command_times_results_and_first_end_equal'": "'all_four_runs_B17053_command_times_results_and_first_end_equal'",
        'all_four_runs_B17053_command_times_results_and_first_end_equal=True': 'each_same_ROM_repeat_all53_command_times_results_and_first_end_equal=True, cross_language_command_order_results_and_first_end_equal=True, cross_language_speech_timing_differences=timing_differences',
        'no_seed_RTC_or_randomness_root_cause_claim=True': "paired_native_persistent_state_and_PRNG_samples=state_samples, original_input_wait_yield_generator_and_wrapper_source_spans=source_spans, prior_scheduler_entropy_evidence=str(earlier_cause), prior_scheduler_entropy_evidence_sha256=sha(earlier_cause.read_bytes()), mechanism_scope='Different speech return frames and shared PRNG seeds are observed; all persistent component fingerprints match through town return11290 and departure16090. Source wait/yield/generator spans are rebound byte-exactly to the earlier scheduler-entropy finding. This is consistent with that mechanism, not a fresh every-RAND-call B170 causal trace. No random outcomes, seed or instruction was forced.', no_RTC_or_every_RAND_call_trace_claim=True",
        "raw_RAM_full_equality_not_claimed_only_whole_original_actor_model_and_captain=True": "raw_RAM_full_equality_not_claimed_component_scopes_explicit=True, preserved_overstrict_verifier='scripts/verify_lil_B170_repeat_v4296.py', preserved_failure_reason='All actor bytes agree. Cross-language command timestamps differ for22 speeches,so the combined strict actor-and-timing assertion failed. Same-ROM repeats and source control order/results pass.'",
    })
    # The no-op replacement above documents the full literal target, but derives
    # do not recursively replace newly produced text. Validate actual final keys.
    produced = Path('scripts/verify_lil_B170_repeat_v4296b.py').read_text(encoding='utf-8')
    assert 'each_same_ROM_repeat_all53_command_times_results_and_first_end_equal=True' in produced
    assert 'all_four_runs_B17053_command_times_results_and_first_end_equal=True' not in produced
    ROOT.mkdir(parents=True)
    save(ROOT / 'source_derivation.json', dict(tool=tool, strict_v4296_preserved=True,
        correction='Actor models were already identical; the failure was the second conjunct requiring all cross-language speech return timestamps to match. Preserve22 ordinary progressive timing differences and every later sailing difference. Add current native persistent-state and PRNG checks instead of claiming whole-world equality.',
        no_new_emulator_or_ROM_change=True, full_goal_complete=False))
