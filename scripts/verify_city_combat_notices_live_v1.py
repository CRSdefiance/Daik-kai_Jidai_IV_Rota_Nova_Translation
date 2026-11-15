"""Match the original regional attack replay to the staged native portraits."""

from hashlib import sha256
from json import loads
from pathlib import Path
from struct import unpack_from

from unicorn.arm_const import UC_ARM_REG_R0

from scripts import verify_city_combat_notices_v1 as checked
from scripts.native_call_abi_v764 import call
from scripts.native_inventory_fixture_v481 import machine
from scripts.verify_captain_biographies_v1 import captured


replay, stage, base = checked.replay, checked.stage, checked.base
LIVE = stage.ROOT / 'city_combat_notices_gameplay_verification.json'
CHECKPOINT = stage.ROOT / 'approved_checkpoint.json'
PAPER = (16, 296, 244, 360)


def get_state(arm, raw):
    base_address = stage.first.review.BASE
    cpu = machine(arm)
    cpu.mem_write(base_address, raw)

    def get(offset, *args):
        call(cpu, offset, args)
        return cpu.reg_read(UC_ARM_REG_R0)

    clock = unpack_from('<I', raw, get(0xCB1B4) + 8 - base_address)[0]
    fleet = get(0xCB1A8) + 4 + 57 * 132
    assert get(0x36914, fleet) and not get(0x36948, fleet)
    order = list(cpu.mem_read(fleet + 0x3E, 2))
    actor = get(0x3697C, fleet)
    voice = get(0x7E988, actor) if actor else None
    vtable = unpack_from('<I', raw, fleet - base_address)[0]
    getter = unpack_from('<I', raw, vtable + 0x20 - base_address)[0]
    scratch = 0x02460000
    get(getter - base_address, scratch, fleet)
    return dict(clock=clock, regional_fleet=57, order=order, captain_voice=voice,
                position=list(unpack_from('<2i', bytes(cpu.mem_read(scratch, 8)))))


def main():
    assert not LIVE.exists() and not CHECKPOINT.exists()
    proof, layout, boot = map(base.load, (stage.PROOF, checked.VISUAL, checked.BOOT))
    sha = base.digest(stage.ROM)
    assert sha == proof['research_ROM_sha256'] == layout['candidate_sha256'] == boot['candidate_sha256']
    terminal_path = replay.ROOT / 'terminal.json'
    terminal = base.load(terminal_path)
    report_path, commands = Path(terminal['report']), Path(terminal['commands'])
    assert base.digest(report_path) == terminal['report_sha256']
    assert base.digest(commands) == terminal['commands_sha256']
    report = base.load(report_path)
    assert terminal['candidate_sha256'] == report['ROM_sha256'] == sha
    assert report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
    assert not any(value for key, value in report.items() if key.startswith('synthetic_'))
    assert terminal['unchanged_original_save']
    donor = report['battery_save_preloaded']
    assert donor['copied_byte_exact_before_cold_boot'] and base.digest(donor['source']) == replay.prior.DONOR_SHA
    journal_path = report_path.with_name('navigation_command_journal.json')
    journal = base.load(journal_path)['commands_received']
    assert all(row['validation_passed'] for row in journal)
    events = [loads(line) for line in commands.read_text(encoding='utf-8').splitlines()]
    assert [row['command'] for row in journal] == events
    frames = {row['frame']: row for row in report['frames_captured'] if row['path'].endswith('_navigation.png')}
    snapshots = {row['frame']: row for row in report['read_only_pause_RAM_snapshots']}
    assert set(frames) <= snapshots.keys()
    rom = base.NdsImage.open(stage.ROM)
    arm = rom.read_file(stage.first.review.ARM)
    raster, _, _ = stage.first.first.portrait.font_tools(rom)
    kanji = rom.read_file('/GRP/KANJI.FNT')
    addresses = [unpack_from('<I', arm, offset)[0] - stage.first.review.BASE for offset in (0x5444C, 0x54450)]

    def snapshot(frame):
        row = snapshots[frame]
        assert row['read_only_export'] and base.digest(row['path']) == row['sha256']
        raw = Path(row['path']).read_bytes()
        assert len(raw) == 0x400000
        return raw

    def text(raw):
        return tuple(raw[at:at + 256].split(b'\0', 1)[0] for at in addresses)

    initial, selected = get_state(arm, snapshot(7000)), get_state(arm, snapshot(14700))
    assert initial['order'] == [1, 7] and selected['order'] == [5, 5]
    assert b'Attack orders issued.' in text(snapshot(14700))[1]
    assert b'Hamburg' in text(snapshot(14700))[1]
    observations, seen_ids = [], set()
    voice_tables = {n: group['slots'] for group in base.load(stage.OUTPUT)['native_context']
                    for n in range(group['first_ID'], group['last_ID'] + 1)}
    for frame in sorted(f for f in frames if f > 16000):
        raw = snapshot(frame)
        native_input, visible = text(raw)
        body = b' '.join(visible.split())
        compatible = []
        for row in proof['records']:
            template = bytes.fromhex(row['staged_hex'])
            start, end = template.split(b'%s')
            if not (native_input.startswith(start) and native_input.endswith(end)):
                continue
            value = native_input[len(start):len(native_input) - len(end)]
            if not value:
                continue
            if 2599 <= row['message_ID'] <= 2606:
                digits = value.decode('cp932')
                if not digits.isdecimal():
                    continue
                value = str(int(digits)).encode('ascii')
            if body == template % (value,):
                compatible.append((row['message_ID'], value))
        if not compatible:
            continue
        pixels, glyphs = stage.first.first.portrait.render_portrait(raster, arm, kanji, visible)
        live_ink = bytes(pixel == (0, 8, 0) for pixel in captured(frames[frame]).crop(PAPER).get_flattened_data())
        if live_ink != bytes(bool(pixel) for pixel in pixels):
            continue
        state = get_state(arm, raw)
        if len(compatible) > 1:
            voice = state['captain_voice']
            assert voice is not None
            compatible = [(number, value) for number, value in compatible
                          if (voice_tables[number][voice] if voice_tables[number][voice] != -1
                              else voice_tables[number][0]) == number]
        assert len(compatible) == 1, (frame, compatible)
        number, value = compatible[0]
        if number in seen_ids:
            continue
        seen_ids.add(number)
        observations.append(dict(message_ID=number, value=value.decode('cp932'), frame=frame,
            input_hex=native_input.hex(), visible_hex=visible.hex(), visible_english=body.decode('cp932'),
            complete_glyphs=len(glyphs), native_ink_sha256=sha256(live_ink).hexdigest(),
            state=state, capture=frames[frame], RAM=snapshots[frame]))
    assert any(2607 <= row['message_ID'] <= 2614 and row['value'] == 'Hamburg' for row in observations)
    retreat, docking = snapshot(25100), snapshot(25500)
    assert text(retreat)[1] == b'We have retreated...'
    assert text(docking)[1] == b"We'll call at a nearby town and await orders."
    assert get_state(arm, docking)['order'] == [6, 0]
    for context_frame in (25100, 25500):
        captured(frames[context_frame])
    end = report['frames']
    returned = get_state(arm, snapshot(end))
    last = observations[-1]
    assert end > last['frame'] and returned['clock'] > last['state']['clock']
    assert frames[end]['framebuffer_sha256'] != last['capture']['framebuffer_sha256']
    paths = (stage.PROOF, checked.VISUAL, checked.BOOT, checked.QA, Path(replay.__file__), Path(__file__),
             terminal_path, report_path, commands, journal_path)
    bindings = {str(path): base.digest(path) for path in paths}
    ids = [row['message_ID'] for row in observations]
    base.save(LIVE, dict(candidate_sha256=sha, observed_ids=ids, observations=observations,
        actual_emulator=True, hardware=False, original_attack_order_and_report=True,
        original_A_advance_and_return_to_sailing=True, initial=initial, selected=selected, returned=returned,
        linked_context=[dict(frame=frame, text=text(raw)[1].decode('ascii'), capture=frames[frame],
                             RAM=snapshots[frame], reviewed_in_current_batch=False)
                        for frame, raw in ((25100, retreat), (25500, docking))],
        returned_capture=frames[end], evidence=bindings))
    base.save(CHECKPOINT, dict(candidate_sha256=sha, approved_for_registered_successor=True,
        live_messages=ids, stored_cases=35, viewed_pages=80, evidence=bindings | {str(LIVE): base.digest(LIVE)}))
    print(f'Verified original Hamburg order, observed notices {ids}, and return to sailing.')


if __name__ == '__main__':
    main()
