"""Exercise a two-line shore-attack report and follow it back to sailing."""

import sys
from json import dumps
from pathlib import Path
from struct import pack_into, unpack_from
from types import FunctionType
from unicodedata import normalize

from PIL import Image, ImageDraw

from scripts import replay_crew_and_shore_reports_v1 as earlier
from scripts import replay_sailing_help_20261120 as startup_runner
from scripts import stage_shore_phrase_wraps_20261121 as stage
from scripts import verify_crew_and_shore_reports_v1 as previous_check
from scripts.checkpoint_shared_notice_storage_v1 import checked_report
from scripts.verify_personal_gameplay_v841 import get_machine


base, portrait = stage.base, stage.portrait
ROOT = stage.ROOT / 'focused_attack_v3'
CAPTURE = ROOT / 'capture'
PROOF = ROOT / 'gameplay.json'
SELECT_COMMAND_END, PAGE, LOSS, RETURN = 14357, 14657, 14877, 15097
ATTACK = 2243
TABLE = 0x116E20


def role_actor(arm, raw):
    _, get = get_machine(arm, raw)
    actor = get(0x82478, get(0xCB1A8) + 0x2090, 1)
    root = get(0xCB184)
    pointer = root + (0x19E4 if actor == get(0x7F244) else 4 + 32 * actor)
    selected = get(0x53F4C, pointer, stage.BASE + TABLE)
    return actor, selected


def select(arm, raw):
    assert raw[TABLE:TABLE + 32] == arm[TABLE:TABLE + 32]
    actor, selected = role_actor(arm, raw)
    assert 2243 <= selected <= 2249
    if selected == ATTACK:
        return raw, dict(actor_ID=actor, original_message_ID=selected, selected_message_ID=selected, changed=False)
    group, = (g for g in base.load(stage.CONTEXTS[0])['native_context'] if g['first_ID'] == ATTACK)
    slot, actual = {index: (slot, n) for index, slot, n in group['original_voice_choices']}[actor]
    assert actual == selected and 0 <= slot < 8
    offset = TABLE + slot * 4
    assert unpack_from('<i', raw, offset) == (selected,)
    after = bytearray(raw)
    pack_into('<i', after, offset, ATTACK)
    assert role_actor(arm, bytes(after)) == (actor, ATTACK)
    return bytes(after), dict(actor_ID=actor, original_message_ID=selected, selected_message_ID=ATTACK,
                              selected_slot=slot, offset=offset, changed=True)


def selector_changes(before, after, record):
    if not record['changed']:
        assert before == after
        return []
    at = record['offset']
    assert before[:at] == after[:at] and before[at + 4:] == after[at + 4:]
    return [dict(address=stage.BASE + at + i, before=a, after=b)
            for i, (a, b) in enumerate(zip(before[at:at + 4], after[at:at + 4], strict=True)) if a != b]


def restore(arm, raw, record):
    if not record['changed']:
        assert raw[TABLE:TABLE + 32] == arm[TABLE:TABLE + 32]
        return raw
    offset = record['offset']
    assert unpack_from('<i', raw, offset) == (ATTACK,)
    after = bytearray(raw)
    after[offset:offset + 4] = arm[offset:offset + 4]
    assert after[TABLE:TABLE + 32] == arm[TABLE:TABLE + 32]
    assert role_actor(arm, bytes(after)) == (record['actor_ID'], record['original_message_ID'])
    return bytes(after)


def commands_for_attack():
    plan, report, _, donor, inputs, original, _ = earlier.history('attack')
    commands = [c.copy() for c in original if c.get('until', RETURN + 1) <= RETURN]
    for command in commands:
        if command['until'] == SELECT_COMMAND_END:
            command['battle_fixture'] |= {'review_shore_variant': 'select'}
        elif command['until'] == LOSS:
            command['battle_fixture'] = {'review_shore_variant': 'restore'}
    assert commands[-1]['until'] == RETURN
    return plan, report, donor, inputs, commands + [dict(stop=True)]


def replay():
    proof = base.load(stage.PROOF)
    assert base.digest(stage.ROM) == proof['candidate_sha256']
    plan, report, donor, inputs, commands = commands_for_attack()
    ROOT.mkdir(exist_ok=False)
    command_path = ROOT / 'commands.jsonl'
    command_path.write_text(''.join(dumps(c) + '\n' for c in commands), encoding='utf-8')
    stream = earlier.GrowingCommands(command_path)
    original_fixture = earlier.dispatch.apply_fixture
    normal = earlier.fixtures(proof['target_ARM9_sha256'])
    old = sys.stdin, sys.argv
    trial = {}

    def apply(arm, raw, request):
        approved = {k: v for k, v in request.items() if k != 'review_shore_variant'}
        marker = request.get('review_shore_variant')
        if marker is None:
            return normal(arm, raw, approved)
        if marker == 'select':
            assert not trial
            setup, evidence = normal(arm, raw, approved)
            after, decision = select(arm, setup)
            trial.update(decision)
            return after, evidence | {'test_shore_message': decision,
                                      'changes': evidence['changes'] + selector_changes(setup, after, decision)}
        assert marker == 'restore'
        after = restore(arm, raw, trial)
        return after, {'shore_selection_restored': True, 'test_shore_message': trial,
                       'changes': selector_changes(raw, after, trial)}

    try:
        sys.stdin, earlier.dispatch.apply_fixture = stream, apply
        sys.argv = [str(Path(earlier.harness.__file__)), '--rom', str(stage.ROM), '--out', str(CAPTURE),
                    '--frames', str(RETURN + 1), '--inputs-json', str(inputs), '--battery-save', str(donor),
                    '--touchscreen', '--capture-every', '999999', '--pause-at', str(plan['initial_pause_frame']),
                    '--dump-pause-ram', '--dump-ram', '--allow-battle-fixtures']
        earlier.harness.main()
    finally:
        sys.stdin, sys.argv = old
        earlier.dispatch.apply_fixture = original_fixture
        stream.close()
    assert base.digest(donor) == plan['source_donor_sha256']
    verify()


def verify():
    digest = base.digest(stage.ROM)
    terminal = CAPTURE / 'capture_report.json'
    report, last = checked_report(terminal, digest, RETURN)
    plan, old_report, donor, inputs, commands = commands_for_attack()
    assert report['battery_save_preloaded']['source_sha256'] == base.digest(donor)
    journal = CAPTURE / 'navigation_command_journal.json'
    received = base.load(journal)['commands_received']
    assert all(c['validation_passed'] for c in received) and [c['command'] for c in received] == commands
    assert not any(v for k, v in report.items() if k.startswith('synthetic_') and k != 'synthetic_battle_recovery_proximity_fixtures')
    snapshots = {row['frame']: row for row in report['read_only_pause_RAM_snapshots']}
    frames = {row['frame']: row for row in report['frames_captured'] if row['path'].endswith('_navigation.png')}

    def raw(frame):
        row = snapshots[frame]
        assert row['read_only_export'] and base.digest(row['path']) == row['sha256']
        content = Path(row['path']).read_bytes()
        assert len(content) == 0x400000
        return content

    image = base.NdsImage.open(stage.ROM)
    arm = image.read_file(stage.ARM)
    proof = base.load(stage.PROOF)
    owner, wrapped, modal = [unpack_from('<I', arm, at)[0] - stage.BASE for at in (0x552A0, 0x54450, 0x54894)]
    fixtures = {case['frame']: case for case in report['synthetic_battle_recovery_proximity_fixtures']}
    normal = earlier.fixtures(proof['target_ARM9_sha256'])
    for entry in received:
        command = entry['command']
        request = command.get('battle_fixture')
        if not request:
            continue
        frame = entry['frame']
        original = {k: v for k, v in request.items() if k != 'review_shore_variant'}
        if frame == PAGE:
            continue
        after, case = normal(arm, raw(frame), original)
        if request.get('review_shore_variant') == 'select':
            selected, decision = select(arm, after)
            case |= {'test_shore_message': decision, 'changes': case['changes'] + selector_changes(after, selected, decision)}
        assert fixtures[frame] == case | {'frame': frame}
    restored = restore(arm, raw(PAGE), decision)
    assert fixtures[PAGE] == {'frame': PAGE, 'shore_selection_restored': True, 'test_shore_message': decision,
                               'changes': selector_changes(raw(PAGE), restored, decision)}
    assert restored[TABLE:TABLE + 32] == arm[TABLE:TABLE + 32]
    assert raw(LOSS)[TABLE:TABLE + 32] == last[TABLE:TABLE + 32] == arm[TABLE:TABLE + 32]
    assert raw(RETURN) == last
    assert role_actor(arm, raw(PAGE)) == (decision['actor_ID'], ATTACK)

    def value(payload, at):
        return payload[at:at + 512].split(b'\0', 1)[0]

    staged, = (r for r in proof['records'] if r['message_ID'] == ATTACK)
    assert value(raw(PAGE), owner + 0x2030).hex() == staged['staged_hex']
    display = value(raw(PAGE), wrapped)
    assert display.hex() == staged['display_hex']
    font, _, _ = portrait.font_tools(image)
    pixels, glyphs = portrait.render_portrait(font, arm, image.read_file('/GRP/KANJI.FNT'), display)
    assert stage.sha256(pixels).hexdigest() == staged['native_ink_sha256']
    shot = previous_check.city.captured(frames[PAGE])
    mask = bytes(pixel == (0, 8, 0) for pixel in shot.crop(previous_check.city.PAPER).get_flattened_data())
    assert mask == bytes(bool(pixel) for pixel in pixels)
    assert value(raw(LOSS), owner + 0x2030) == b'Sailors lost: %s.'
    notice = normalize('NFKC', value(raw(LOSS), modal).decode('cp932')).strip()
    before, after = previous_check.fleet_state(arm, raw(PAGE)), previous_check.fleet_state(arm, raw(RETURN))
    lost = sum(before['crew']) - sum(after['crew'])
    assert lost > 0 and notice == f'Sailors lost: {lost}.'
    assert after['original_mode'] == [0, 0, 0] and not previous_check.visible_paper(frames[RETURN]['path'])
    path = ROOT / 'attack_and_sailing_return.png'
    sheet = Image.new('RGB', (768, 216), '#263238')
    draw = ImageDraw.Draw(sheet)
    for i, (frame, label) in enumerate(((PAGE, 'Shore attack'), (LOSS, 'Original sailor-loss notice'), (RETURN, 'Return to sailing'))):
        draw.text((i * 256 + 4, 4), label, fill='white')
        sheet.paste(previous_check.city.captured(frames[frame]).crop((0, 192, 256, 384)), (i * 256, 22))
    sheet.save(path)
    base.save(PROOF, dict(candidate_sha256=digest, actual_emulator=True, hardware=False,
                          revised_message_ID=ATTACK, verified_glyph_count=len(glyphs), selector_restored=True,
                          test_variant=decision, ordinary_outcome_trigger_preserved=True,
                          shore_provision_and_location_fixtures_reused=True, original_sailor_loss=lost,
                          message_frame=PAGE, notice_frame=LOSS, return_frame=RETURN,
                          sheet={'path': str(path), 'sha256': base.digest(path)},
                          evidence={str(p): base.digest(p) for p in (terminal, journal, old_report, donor, inputs, path)}))
    print(f'Observed the revised shore attack, the original loss of {lost} sailors and the return to sailing.')


if __name__ == '__main__':
    if sys.argv[1:] == ['startup']:
        FunctionType(startup_runner.startup.__code__, startup_runner.env | {'parent': stage.parent, 'stage': stage})()
    elif sys.argv[1:] == ['verify']:
        verify()
    else:
        assert sys.argv[1:] == ['play']
        replay()

