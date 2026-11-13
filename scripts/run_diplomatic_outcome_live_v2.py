"""Exercise an incoming truce and refusal using the original letter dispatcher."""

import argparse
from io import StringIO
import json
from pathlib import Path
import struct
import sys

from dk4tool.rom.nds import NdsImage
from scripts.audit_story_glyph_consistency import load, save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.refine_diplomatic_outcomes_layout_v2 import EVIDENCE, ROM, ROOT
from scripts.run_battle_cooking_livestock_live_v911 import GrowingCommands
from scripts.verify_personal_gameplay_v841 import get_machine


BASE = 0x02000000
INPUTS = Path('work/analysis/letter_delivery_v791/initial_inputs.json')
DONOR = Path('E:/Rota Nova translations/Saves/Test fixtures/V751 disposable Istanbul donor.dsv')
DONOR_SHA = 'd991cb3bcdf74eed7aeb58c9a75957766b7c820d002423fd2b55cc8493cf8132'
ARM = '/__arm9__.bin'
SENDER, SLOT = 5, 4
ACTION = {'mode': 'isolated-incoming-truce'}


def set_condition(arm, raw, request):
    assert request == ACTION and len(raw) == 0x400000
    assert arm == NdsImage.open(ROM).read_file(ARM)
    clean = NdsImage.open('work/clean.nds').read_file(ARM)
    for start, end in ((0x91464, 0x91480), (0x91598, 0x91658), (0x917B0, 0x918A8),
                       (0x92D9C, 0x92EE4), (0x5466C, 0x546EC)):
        assert clean[start:end] == arm[start:end]
    cpu, get = get_machine(arm, raw)
    assert get(0xB65E4) == 22 and get(0x7F244) == 1
    company_root = get(0xCB160)
    own = get(0x397D8, company_root)
    assert own == 2
    sender = company_root + 4 + SENDER * 76
    vtable = int.from_bytes(cpu.mem_read(sender, 4), 'little')
    getter = int.from_bytes(cpu.mem_read(vtable + 8, 4), 'little')
    name = get(getter - BASE, sender)
    assert bytes(cpu.mem_read(name, 11)) == b'Speyer Co.\0'
    assert get(0x3CB30, sender, own) == 2
    clock = get(0xCB1B4)
    current_tick = int.from_bytes(cpu.mem_read(clock + 8, 4), 'little')
    pool = get(0xCB130)
    slot = pool + 4 + 16 * SLOT
    start = slot - BASE
    before = raw[start:start + 16]
    assert before == bytes.fromhex('18c614020b0000000000000000000000')
    assert get(0x91464, slot) == 0
    after = before[:4] + bytes([3, SENDER, 16, own]) + before[8:12] + struct.pack('<I', current_tick + 48)
    cpu.mem_write(slot, after)
    assert get(0x91464, slot) == 1
    changes = [dict(address=slot + index, before=old, after=new)
               for index, (old, new) in enumerate(zip(before, after, strict=True)) if old != new]
    return raw[:start] + after + raw[start + 16:], dict(
        mode=ACTION['mode'], letter_object=slot, slot_index=SLOT, type=3, sender=SENDER,
        recipient=own, sender_name='Speyer Co.', original_hostile_relation_preserved=True,
        source_dispatcher=0x020917B0, source_truce_handler=0x02092D9C,
        current_tick=current_tick, due_tick=current_tick + 48,
        original_slot_hex=before.hex(), seeded_slot_hex=after.hex(), only_letter_slot_bytes_changed=True,
        changes=changes)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--schedule', type=Path, required=True)
    parser.add_argument('--run-name', required=True, choices=('survey_retry', 'decline', 'accept'))
    parser.add_argument('--continue-at-pause', action='store_true')
    args = parser.parse_args()
    staged = load(EVIDENCE)
    assert digest(ROM) == staged['research_ROM_sha256']
    assert digest(DONOR) == DONOR_SHA
    commands = load(args.schedule)
    assert commands[0]['condition_fixture'] == ACTION
    assert args.continue_at_pause or commands[-1] == {'stop': True}
    assert sum('condition_fixture' in command for command in commands) == 1
    frames = [3200, *(command['until'] for command in commands if 'until' in command)]
    folder = ROOT / ('truce_' + args.run_name)
    folder.mkdir(exist_ok=False)
    report = folder / 'capture_report.json'
    harness = Path('scripts/headless_desmume_v193.py')
    source = harness.read_text(encoding='utf-8')
    token = 'from scripts.native_condition_fixture_v520 import set_condition'
    assert source.count(token) == 1
    effective = source.replace(token, 'from scripts.run_diplomatic_outcome_live_v2 import set_condition')
    frame_limit = 12000 if args.continue_at_pause else frames[-1] + 400
    options = ['--rom', str(ROM), '--out', str(folder), '--frames', str(frame_limit),
               '--inputs-json', str(INPUTS), '--battery-save', str(DONOR), '--touchscreen',
               '--capture-every', '999999', '--pause-at', '3200', '--allow-condition-fixtures',
               '--capture-at', *map(str, frames), '--dump-capture-ram', '--dump-pause-ram', '--dump-ram']
    navigation = folder / 'commands.jsonl'
    navigation.write_text(''.join(json.dumps(c) + '\n' for c in commands), encoding='utf-8')
    previous = sys.stdin, sys.argv
    stream = GrowingCommands(navigation) if args.continue_at_pause else StringIO(navigation.read_text(encoding='utf-8'))
    try:
        sys.stdin = stream
        sys.argv = [str(harness), *options]
        exec(compile(effective, str(harness), 'exec'),
             {'__name__': '__main__', '__file__': str(harness.resolve())})
    finally:
        sys.stdin, sys.argv = previous
        stream.close()
    assert digest(DONOR) == DONOR_SHA
    save(folder / 'terminal.json', dict(
        report=str(report), report_sha256=digest(report), candidate_sha256=digest(ROM),
        schedule=str(args.schedule), schedule_sha256=digest(args.schedule),
        final_navigation=str(navigation), final_navigation_sha256=digest(navigation),
        donor_sha256=DONOR_SHA, harness_sha256=digest(harness), producer_sha256=digest(__file__)))


if __name__ == '__main__':
    main()
