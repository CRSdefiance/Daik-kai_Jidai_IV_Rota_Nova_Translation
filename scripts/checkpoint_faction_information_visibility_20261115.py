"""Compare actual DS framebuffers after replacing five original faction-panel strings."""

from pathlib import Path
from struct import unpack_from

from dk4tool.dialogue.font_audit import GameAsciiFont
from scripts import probe_faction_information_fields_20261115 as probe
from scripts import replay_faction_information_20261115 as replay
from scripts.verify_captain_biographies_v1 import captured, shots
from scripts.verify_plaque_release_v247 import find_mask


base, current = replay.base, replay.current
OUTPUT = Path('translations/editorial_checkpoints/SharedText_20261110_v1/faction_information_visibility_20261115_v1.json')
CASES = (
    ('Inn Strategist report', 'current_trace', 'probe_trace', 6800, 6000, 0x0203D70C),
    ('Fleet Info', 'fleet_trace', 'fleet_probe_trace', 17401, 17200, 0x0203D728),
)
COMMON_REQUESTS = (0x0205528C, 0x020534F4)
CONTINUATIONS = {0x0203D6A8: (48, 36), 0x0203D7FC: (36, 30)}


def capture(folder, expected, terminal):
    report = replay.ROOT / folder / 'capture/capture_report.json'
    receipt = replay.ROOT / folder / 'observer/requests.json'
    run, trace = map(base.load, (report, receipt))
    assert run['cold_boot'] and not run['savestate_loaded'] and not run['callback_errors']
    assert run['ROM_sha256'] == expected and run['frames'] == terminal
    assert run['battery_save_preloaded']['copied_byte_exact_before_cold_boot']
    donor = run['battery_save_preloaded']
    assert base.digest(donor['source']) == donor['source_sha256']
    assert trace['all_host_slots_restored_and_core_file_exact'] and not trace['errors'] and not trace['mismatches']
    return run, trace['source_requests'], {str(path): base.digest(path) for path in (report, receipt)}


def main():
    plan = base.load(probe.PLAN)
    release = base.load(current.RELEASE)
    assert base.digest(current.ROM) == plan['previous_ROM_sha256'] == release['candidate_sha256']
    assert base.digest(probe.ROM) == plan['research_ROM_sha256']
    assert base.digest(base.REGISTRY) == release['registry_sha256']
    assert plan['whole_parent_inverse_exact'] and plan['source_controls_and_numeric_arguments_preserved']
    old_image, new_image = [base.NdsImage.open(path) for path in (current.ROM, probe.ROM)]
    arm = current.stage.ARM
    assert GameAsciiFont.from_arm9(old_image.read_file(arm)).glyphs == GameAsciiFont.from_arm9(new_image.read_file(arm)).glyphs
    font = GameAsciiFont.from_arm9(old_image.read_file(arm))
    results = []
    evidence = {str(path): base.digest(path) for path in (current.RELEASE, probe.PLAN)}
    labels = {pc: row for row in plan['source_and_current_values'] for pc in row['native_caller_addresses']}
    for name, previous_folder, probe_folder, terminal, active_frame, power in CASES:
        old, old_calls, old_evidence = capture(previous_folder, plan['previous_ROM_sha256'], terminal)
        new, new_calls, new_evidence = capture(probe_folder, plan['research_ROM_sha256'], terminal)
        evidence.update(old_evidence | new_evidence)
        assert old['scripted_input_schedule'] == new['scripted_input_schedule']
        assert old['core_options'] == new['core_options']
        assert old['battery_save_preloaded']['source_sha256'] == new['battery_save_preloaded']['source_sha256']
        fixtures = old.get('synthetic_condition_fixtures', [])
        control = new.get('synthetic_condition_fixtures', [])
        assert len(fixtures) == len(control) == int(name == 'Inn Strategist report')
        if fixtures:
            assert fixtures[0]['changes'] == control[0]['changes'] and len(fixtures[0]['changes']) == 3
            assert fixtures[0]['frame'] == control[0]['frame'] == 3200

        old_frames, new_frames = map(shots, (old, new))
        assert old_frames.keys() == new_frames.keys()
        exact = []
        for frame, old_row in old_frames.items():
            new_row = new_frames[frame]
            assert old_row['framebuffer_sha256'] == new_row['framebuffer_sha256']
            assert captured(old_row).tobytes() == captured(new_row).tobytes()
            exact.append(frame)
        assert active_frame in exact
        assert len(old_calls) == len(new_calls)
        found, unchanged_calls, common = [], [], []
        for before, after in zip(old_calls, new_calls, strict=True):
            pc = before['PC']
            assert pc == after['PC']
            trim = ('text', 'complete_text_hex') if pc in labels else ('context_hex',) if pc in CONTINUATIONS else ()
            assert {k: v for k, v in before.items() if k not in trim} == {k: v for k, v in after.items() if k not in trim}
            if pc in CONTINUATIONS:
                a, b = [bytes.fromhex(row['context_hex']) for row in (before, after)]
                assert (unpack_from('<I', a, 36)[0], unpack_from('<I', b, 36)[0]) == CONTINUATIONS[pc]
                assert a[:36] == b[:36] and a[40:60] == b[40:60] and a[68:] == b[68:]
            if pc in labels:
                record = labels[pc]
                assert before['text'] == record['clean_Japanese'] and after['text'] == record['proposed_English']
                assert before['arguments'][1] == after['arguments'][1] == probe.BASE + record['ARM9_offset']
                found.append(dict(PC=pc, before=before, after=after))
            elif pc in COMMON_REQUESTS:
                common.append(dict(PC=pc, frame=before['frame'], message_ID=before['arguments'][1 if pc == 0x020534F4 else 0]))
            else:
                unchanged_calls.append(dict(before=before, after=after))
        assert {row['PC'] for row in found} == {0x0203D678, power, 0x0203D750, 0x0203D7B4}
        screen = captured(old_frames[active_frame])
        head = find_mask(font, 'Leader (Soldier)', screen, (72, 20, 256, 42))
        if fixtures:
            title, leader, level = 'Albuquerque', 'Dinis de Albuquerque', 'Level   36'
            assert any(row['message_ID'] == 1187 for row in common)
        else:
            title, leader, level = 'Bergstrom Fleet', 'Hodram Joakim Bergstrom', 'Level   18'
        results.append(dict(path=name, checked_two_screen_frames=exact, suppressed_label_calls=found,
            common_requests=common, unchanged_calls=unchanged_calls, active_control_frame=old_frames[active_frame],
            visible_leader_mask=head, visible_title_mask=find_mask(font, title, screen, (0, 0, 256, 16)),
            visible_person_mask=find_mask(font, leader, screen, (72, 36, 256, 59)),
            visible_level_mask=find_mask(font, level, screen, (72, 78, 256, 103)),
            fixture_changes=fixtures[0]['changes'] if fixtures else []))

    ledger = base.load(base.LEDGER)
    assert ledger['current_integrated_candidate']['sha256'] == release['candidate_sha256']
    records = []
    for field in plan['source_and_current_values']:
        observed = [row['path'] for row in results if any(call['PC'] in field['native_caller_addresses'] for call in row['suppressed_label_calls'])]
        records.append(field | dict(registered_review_credit=0, formatting_gate=False, observed_render_paths=observed,
                                    disposition='The observed callers pass the field to the renderer, with no visible effect in the controlled frame comparison.'))
    base.save(OUTPUT, dict(candidate_sha256=release['candidate_sha256'], diagnostic_ROM_sha256=plan['research_ROM_sha256'],
        records=records, gameplay=results, evidence=evidence, complete_frames_match=True, release_build_changes=0,
        current_credited_dialogue=ledger['records_editorially_completed'], pending_mapped_COMMON=ledger['pending_shared_consumer_checkpoint_20261114']['remaining_total'],
        scope='Original Inn Strategist and Fleet Info replay only. Other conditional displays and hardware remain open.'))
    print('Temporary English strings reached the original draw calls. All', sum(len(row['checked_two_screen_frames']) for row in results), 'two-screen frames match.')


if __name__ == '__main__':
    main()
