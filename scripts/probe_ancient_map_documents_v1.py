"""Open the native Ancient Map document using only the original clue-bit setter."""

import builtins
from inspect import getsource
from json import dumps
from pathlib import Path
from struct import unpack_from
import sys

from unicorn.arm_const import UC_ARM_REG_R0

from scripts import headless_desmume_v193 as harness
from scripts import register_arrival_month_labels_v1 as parent
from scripts import verify_treasure_panel_v722 as prior
from scripts.probe_button_prompt_native import call, machine
from scripts.source_locked_derivation_v5118 import checked_text


base, stage = parent.base, parent.stage
ROOT = Path('out/ancient_map_current_display_20261111_v1')
ROM = parent.ROM
PAUSE, END = 9900, 11900
COMMANDS = (
    dict(until=10300, condition_fixture={'event': 'ancient_map_first_document'}, buttons=['A'], duration=8),
    dict(until=10700, buttons=['A'], duration=8),
    dict(until=11100, buttons=[], duration=8),
    dict(until=11500, buttons=['B'], duration=8),
    dict(until=END, buttons=['B'], duration=8),
    dict(stop=True),
)


def set_condition(arm, raw, request):
    assert request == {'event': 'ancient_map_first_document'}
    assert len(raw) == 0x400000 and arm == base.NdsImage.open(ROM).read_file(stage.ARM)
    original = base.NdsImage.open(stage.CLEAN).read_file(stage.ARM)
    for first, last in ((0x4A204, 0x4A230), (0x102E50, 0x10301C), (0x103058, 0x1030D8),
                        (0x1031DC, 0x10356C)):
        assert original[first:last] == arm[first:last]
    cpu = machine(arm)
    cpu.mem_write(stage.BASE, raw)

    def get(offset, *args):
        call(cpu, offset, args)
        return cpu.reg_read(UC_ARM_REG_R0)

    catalog = get(0xCB190) + 4
    items = list(range(198, 202))
    addresses = [catalog + 20 * item for item in items]
    for address in addresses:
        assert get(0x4A224, address) == 0
        get(0x4A204, address, 1)
        assert get(0x4A224, address) == 4
    after = bytes(cpu.mem_read(stage.BASE, len(raw)))
    changed = [dict(address=stage.BASE + i, before=old, after=new)
               for i, (old, new) in enumerate(zip(raw, after, strict=True)) if old != new]
    assert {row['address'] for row in changed} == {address + 0x11 for address in addresses}
    assert all(row['before'] ^ row['after'] == 4 for row in changed)
    map_table, map_index = 0x023800CC, 0x023800E0
    item_number = unpack_from('<I', raw, map_table - stage.BASE)[0]
    map_route = raw[map_index - stage.BASE]
    assert (item_number, map_route) == (189, 7)
    return after, dict(event=request['event'], original_clue_setter=0x0204A204, clue_items=items,
        changed=changed, original_clue_getter=0x0204A224,
        document_pair_index=map_route, lore_index=item_number - 188,
        actual_earned_clues_or_save_progress=False)


def main():
    assert not ROOT.exists()
    release = base.load(parent.RELEASE)
    assert base.digest(ROM) == release['candidate_sha256']
    donor_report = prior.CAP / 'capture_report.json'
    donor = base.load(donor_report)
    assert donor['cold_boot'] and not donor['savestate_loaded'] and not donor['callback_errors']
    save = donor['battery_save_preloaded']
    assert base.digest(save['source']) == save['source_sha256']
    schedule = [row for row in donor['scripted_input_schedule'] if row['start'] <= PAUSE]
    ROOT.mkdir()
    inputs, commands = ROOT / 'inputs.json', ROOT / 'commands.jsonl'
    base.save(inputs, schedule)
    commands.write_text(''.join(dumps(row) + '\n' for row in COMMANDS), encoding='utf-8')
    source = checked_text(getsource(harness.main), {
        'from scripts.native_condition_fixture_v520 import set_condition':
            'from scripts.probe_ancient_map_documents_v1 import set_condition',
    })
    environment = dict(vars(harness))
    exec(compile(source, __file__ + '::native-clue-document', 'exec'), environment)
    args = [str(Path(harness.__file__)), '--rom', str(ROM), '--out', str(ROOT / 'capture'),
            '--frames', str(END + 1), '--inputs-json', str(inputs), '--press-start', '-1',
            '--capture-every', '999999', '--pause-at', str(PAUSE), '--dump-pause-ram',
            '--allow-condition-fixtures', '--touchscreen', '--battery-save', save['source']]
    queue = iter(COMMANDS)
    original_input, original_argv = builtins.input, sys.argv
    try:
        builtins.input = lambda *unused: dumps(next(queue))
        sys.argv = args
        environment['main']()
    finally:
        builtins.input, sys.argv = original_input, original_argv
    report = ROOT / 'capture/capture_report.json'
    observed = base.load(report)
    assert observed['ROM_sha256'] == release['candidate_sha256'] and observed['frames'] == END
    assert observed['cold_boot'] and not observed['savestate_loaded'] and not observed['callback_errors']
    assert observed['battery_save_preloaded']['source_sha256'] == base.digest(save['source'])
    base.save(ROOT / 'terminal.json', dict(report=str(report), report_sha256=base.digest(report),
        original_donor_capture=str(donor_report), original_donor_sha256=base.digest(donor_report),
        commands=str(commands), commands_sha256=base.digest(commands)))


if __name__ == '__main__':
    main()
