"""Repeat the Madeira dock and resupply inputs on the staged price fix."""

import argparse
import json
from pathlib import Path
from struct import pack
import sys
from types import FunctionType

from scripts import headless_desmume_v193 as harness
from scripts import native_condition_fixture_v520 as adapter
from scripts import replay_swimmer_leak_square_dialogue_20261120 as voyage
from scripts import stage_madeira_resupply_numerals_20261120 as stage
from scripts.run_battle_cooking_livestock_live_v911 import GrowingCommands


REFERENCE = Path('E:/Rota Nova translations/Generated/work/swimmer_leak_square_dialogue_20261120_v2'
                 '/sea_retry_v1/mermaid/capture/capture_report.json')
JOURNAL = stage.ROOT / 'madeira_commands_v2.jsonl'
INPUTS = stage.ROOT / 'madeira_inputs_v2.json'


def dispatch_gate(arm, raw, label):
    """Supply an event when the scheduler would otherwise choose no encounter."""
    offset = 0x30F08
    skip, fall_through = pack('<I', 0x0A00001E), pack('<I', 0xE1A00000)
    source = stage.batch.NdsImage.open(stage.batch.CLEAN).read_file(stage.batch.ARM)
    assert arm[offset-4:offset+8] == source[offset-4:offset+8] and arm[offset:offset+4] == skip
    before, after = (skip, fall_through) if label in ('choose', 'select-leak') else (fall_through, skip)
    assert raw[offset:offset+4] == before
    changes = [dict(address=stage.BASE + offset + i, before=a, after=b)
               for i, (a, b) in enumerate(zip(before, after, strict=True)) if a != b]
    return raw[:offset] + after + raw[offset+4:], changes


def main(output, event=None, force_dispatch=False, *, price_only=False):
    folder = stage.PRICE_ONLY if price_only else stage.ROOT
    rom = folder / stage.ROM.name
    case = stage.batch.load(folder / stage.PROOF.name)
    assert stage.batch.digest(rom.read_bytes()) == case['candidate_sha256']
    source, donor, pause, _, initial, commands, _, setter = voyage.plan('mermaid', rom=rom)
    earlier = stage.batch.load(REFERENCE)
    assert earlier['ROM_sha256'] == case['staged_parent_sha256']
    assert stage.batch.digest(donor.read_bytes()) == earlier['battery_save_preloaded']['source_sha256']
    initialize = voyage.anchor_ship(setter, stage.batch.load(source), source_frame=8327)
    journal, inputs = folder / JOURNAL.name, folder / INPUTS.name
    if price_only:
        assert event is None
        completed = [json.loads(line) for line in JOURNAL.read_text(encoding='utf-8-sig').splitlines()]
        assert completed[:len(commands) - 1] == commands[:-1] and completed[-1] == {'stop': True}
        commands = completed
    elif event is None:
        commands = commands[:-1]
    else:
        variant = f'stocked_{event}' + ('_dispatch' if force_dispatch else '')
        journal = JOURNAL.with_name(f'{variant}_commands.jsonl')
        inputs = INPUTS.with_name(f'{variant}_inputs.json')
        prefix = [json.loads(line) for line in JOURNAL.read_text(encoding='utf-8-sig').splitlines()]
        assert prefix[:len(commands) - 1] == commands[:-1]
        end = next(i for i, command in enumerate(prefix) if command.get('until') == 13307)
        commands = prefix[:end + 1]
        assert commands[-1]['buttons'] == ['A']
        if event == 'leak':
            choose, restore = {'mode': 'select-leak'}, {'mode': 'restore-leak-selection'}
            event_setter = FunctionType(voyage.leak.set_condition.__code__, vars(voyage.leak) | {'ROM': stage.ROM})
        else:
            choose, restore = {'mode': 'choose', 'event': event}, {'mode': 'restore', 'event': event}
            event_setter = setter
        commands.append(dict(until=13907, buttons=['UP'], duration=600, condition_fixture=choose | {'after_resupply': True}))
        tail = (13907, 14247, 14587, 14927) if force_dispatch else (15107, 15447, 15787, 16127)
        if not force_dispatch:
            commands += [dict(until=14507, buttons=['UP'], duration=600), dict(until=15107, buttons=['UP'], duration=600)]
        commands += [dict(until=tail[1], buttons=['A'], duration=8, condition_fixture=restore | {'after_resupply': True}),
                     dict(until=tail[2], buttons=['A'], duration=8),
                     dict(until=tail[3], buttons=['A'], duration=8), dict(stop=True)]

        def dispatch(arm, raw, request):
            if request.get('after_resupply'):
                native_request = {key: value for key, value in request.items() if key != 'after_resupply'}
                after, receipt = event_setter(arm, raw, native_request)
                if force_dispatch:
                    after, changes = dispatch_gate(arm, after, native_request['mode'])
                    receipt['changes'] += changes
                    receipt['no_encounter_branch_temporarily_bypassed'] = True
                return after, receipt | {'provisioned_voyage_selector_only': True}
            return initialize(arm, raw, request)

    assert not journal.exists() and not inputs.exists()
    journal.write_text(''.join(json.dumps(command) + '\n' for command in commands), encoding='utf-8')
    stage.batch.write(inputs, initial)
    stream = GrowingCommands(journal)
    old = adapter.set_condition, sys.stdin, sys.argv
    try:
        adapter.set_condition, sys.stdin = dispatch if event else initialize, stream
        sys.argv = [harness.__file__, '--rom', str(rom), '--out', str(output), '--frames', '36000',
                    '--inputs-json', str(inputs), '--battery-save', str(donor), '--touchscreen',
                    '--pause-at', str(pause), '--allow-condition-fixtures', '--capture-every', '999999',
                    '--dump-pause-ram', '--dump-ram']
        harness.main()
    finally:
        adapter.set_condition, sys.stdin, sys.argv = old
        stream.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', required=True, type=Path)
    parser.add_argument('--event', choices=('mermaid', 'leak'))
    parser.add_argument('--force-dispatch', action='store_true')
    parser.add_argument('--price-only', action='store_true')
    args = parser.parse_args()
    if args.force_dispatch and not args.event:
        parser.error('--force-dispatch requires --event')
    main(args.output, args.event, args.force_dispatch, price_only=args.price_only)
