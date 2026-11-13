"""Exercise the original item menu on the staged crew item-action candidate."""

from inspect import getsource
import json
from pathlib import Path
import sys
from types import FunctionType

from unicorn.arm_const import UC_ARM_REG_R0

from scripts import native_inventory_fixture_v481 as inventory
from scripts import replay_sailing_reactions_v1 as prior
from scripts import stage_crew_item_actions_v2 as stage
from scripts.native_call_abi_v764 import call
from scripts.source_locked_derivation_v5118 import checked_text


base = stage.first.review.prior
ROOT = stage.ROOT / 'focused_item_use'
STARTUP = stage.ROOT / 'own_startup'
PRIOR = prior.STARTUP
PAUSE = prior.PAUSE
ITEM = 23


def transfer(arm, raw, items):
    proof = base.load(stage.PROOF)
    clean = base.NdsImage.open(stage.first.review.CLEAN).read_file(stage.first.ARM)
    assert items == [ITEM] and base.sha256(arm).hexdigest() == proof['research_ARM9_sha256']
    assert arm[0x49DE8:0x4A6A0] == clean[0x49DE8:0x4A6A0]
    source = checked_text(getsource(inventory.transfer), {
        'category not in (2, 3, 4)': 'category not in (1, 9)',
    })
    env = vars(inventory) | {'SUPPORTED_ARM_SHA': (proof['research_ARM9_sha256'],)}
    exec(compile(source, __file__ + '::original-remedy-transfer', 'exec'), env)
    result, evidence = env['transfer'](arm, raw, items)
    assert evidence['items'][0]['name'] == "Hua Tuo's Tonic"
    return result, evidence


def set_condition(arm, raw, request):
    assert request == {'event': 'remedy-condition'} and len(raw) == 0x400000
    proof = base.load(stage.PROOF)
    clean = base.NdsImage.open(stage.first.review.CLEAN).read_file(stage.first.ARM)
    assert base.sha256(arm).hexdigest() == proof['research_ARM9_sha256']
    assert arm[0x4BED4:0x4BFC8] == clean[0x4BED4:0x4BFC8]
    assert arm[0x82B0C:0x82B38] == clean[0x82B0C:0x82B38]
    cpu = inventory.machine(arm)
    cpu.mem_write(inventory.BASE, raw)

    def get(offset, *args):
        call(cpu, offset, args)
        return cpu.reg_read(UC_ARM_REG_R0)

    fleet = get(0xCB1A8) + 0x2090
    before = get(0x82B30, fleet)
    assert before == 27
    get(0x82B0C, fleet, 23)
    assert get(0x82B30, fleet) == 23
    result = bytes(cpu.mem_read(inventory.BASE, len(raw)))
    changes = [dict(address=inventory.BASE + i, before=a, after=b)
               for i, (a, b) in enumerate(zip(raw, result, strict=True)) if a != b]
    assert changes and all(row['address'] in {fleet + 0x2C, *range(fleet + 0x30, fleet + 0x34)} for row in changes)
    return result, dict(original_condition_setter=0x02082B0C, fleet=fleet, previous_condition=before,
                        supplied_condition=23, natural_event_selection_verified=False, changes=changes)


def gameplay():
    assert not ROOT.exists()
    proof = base.load(stage.PROOF)
    assert base.digest(stage.ROM) == proof['research_ROM_sha256']
    terminal = base.load(prior.DONOR_REPLAY / 'terminal.json')
    assert base.digest(terminal['report']) == terminal['report_sha256']
    donor = base.load(terminal['report'])['battery_save_preloaded']
    inputs = prior.DONOR_REPLAY / 'original_input_prefix.json'
    assert base.digest(inputs) == terminal['original_input_prefix_sha256']
    assert base.digest(donor['source']) == donor['source_sha256']
    ROOT.mkdir()
    commands = ROOT / 'commands.jsonl'
    commands.write_text(json.dumps(dict(until=8700, inventory_items=[ITEM], buttons=['X'], duration=8)) + '\n',
                        encoding='utf-8')
    harness = Path('scripts/headless_desmume_v193.py')
    script = checked_text(harness.read_text(encoding='utf-8'), {
        'from scripts.native_condition_fixture_v520 import set_condition':
            'from scripts.replay_crew_item_actions_v1 import set_condition',
        'from scripts.native_inventory_fixture_v481 import transfer':
            'from scripts.replay_crew_item_actions_v1 import transfer',
    })
    args = ['--rom', str(stage.ROM), '--out', str(ROOT / 'capture'), '--frames', '16500',
        '--inputs-json', str(inputs), '--battery-save', donor['source'], '--touchscreen', '--capture-every',
        '999999', '--pause-at', str(PAUSE), '--allow-inventory-fixtures', '--allow-condition-fixtures', '--dump-pause-ram']
    previous = sys.stdin, sys.argv
    stream = prior.GrowingCommands(commands)
    try:
        sys.stdin, sys.argv = stream, [str(harness), *args]
        exec(compile(script, str(harness), 'exec'), {'__name__': '__main__', '__file__': str(harness.resolve())})
    finally:
        sys.stdin, sys.argv = previous
        stream.close()
    report_path = ROOT / 'capture/capture_report.json'
    report = base.load(report_path)
    assert report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
    assert report['ROM_sha256'] == proof['research_ROM_sha256']
    assert base.digest(donor['source']) == donor['source_sha256']
    base.save(ROOT / 'terminal.json', dict(candidate_sha256=report['ROM_sha256'],
        report=str(report_path), report_sha256=base.digest(report_path), commands=str(commands),
        commands_sha256=base.digest(commands), unchanged_original_save=True))


def cold_boot():
    boot = prior.precedent.startup
    env = vars(boot) | dict(EVIDENCE=stage.PROOF, ROM=stage.ROM, STARTUP=STARTUP, PRIOR=PRIOR)
    FunctionType(boot.main.__code__, env)()


if __name__ == '__main__':
    assert sys.argv[1:] in (['gameplay'], ['startup'])
    (gameplay if sys.argv[1] == 'gameplay' else cold_boot)()
