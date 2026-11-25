"""Seal the native layout review and isolate the digit-font change."""

import argparse
from inspect import getsource
from pathlib import Path
from types import FunctionType, SimpleNamespace
from xml.etree import ElementTree

from dk4tool.patch.fleet_report_amount_glyphs_v1 import AMOUNT_TABLES, BUFFER
from scripts import replay_fleet_reports_v1 as replay
from scripts import verify_item_production_advice_v1 as prior_startup
from scripts.source_locked_derivation_v5118 import checked_text


stage, base = replay.stage, replay.base
ROOT, ROM, PROOF = stage.ROOT, stage.ROM, stage.PROOF
BOOT, VISUAL = ROOT / 'own_startup_verification.json', ROOT / 'visual_layout_review_v2.json'
BIOGRAPHIES = replay.prior.STARTUP.parent
QA = Path('work/fleet_reports_repo_qa_20261111.xml')


def amount_controls(arm, ownership):
    portrait = stage.first.portrait
    selector = stage.first.prior.prior.extender
    cpu = portrait.machine(arm)
    source = checked_text(getsource(portrait.dispatch), {
        'def dispatch(cpu, address, stack, targets):': 'def dispatch(cpu, address, stack, targets, normalized=False):',
        'count=128': 'count=4096',
        '    assert cpu.reg_read(UC_ARM_REG_SP) == STACK and cpu.reg_read(UC_ARM_REG_LR) == STOP':
            '    if normalized:\n'
            '        assert cpu.reg_read(UC_ARM_REG_SP) == STACK - BUFFER - 32\n'
            '        assert selector_start <= cpu.reg_read(UC_ARM_REG_LR) < selector_stop\n'
            '    else:\n'
            '        assert cpu.reg_read(UC_ARM_REG_SP) == STACK and cpu.reg_read(UC_ARM_REG_LR) == STOP',
    })
    env = dict(portrait.dispatch.__globals__) | {'BUFFER': BUFFER, 'selector_start': ownership['selector'],
        'selector_stop': ownership['selector'] + ownership['selector_bytes']}
    exec(compile(source, __file__ + '::scoped-amount-controls', 'exec'), env)
    run = env['dispatch']
    argument = portrait.ARGS[1]
    legacy = ownership['previous_selector']
    renderer = selector.LITERAL_PARAGRAPH
    cases = []
    for value, expected in (
        (b'Lost \x82\x50 gold.', b'Lost 1 gold.'),
        (b'Gold: ' + '０１２３４５６７８９'.encode('cp932') + b'!', b'Gold: 0123456789!'),
        (b'Already 123 ASCII.', None),
        (b'Mixed \x82\x50 and \x82\x60.', None),
        (b'Unexpected \x83\x41.', None),
        (b'A' * (BUFFER - 2) + b'\x82\x50', None),
    ):
        for table in AMOUNT_TABLES:
            cpu.mem_write(argument, value + b'\0')
            target, registers = run(cpu, selector.HOOK, {0x264: 0x02053F40, 0x274: table, 0x27C: 0},
                                    (renderer, legacy), normalized=expected is not None)
            assert target == renderer and registers[0] == portrait.ARGS[0]
            assert registers[2:] == portrait.ARGS[2:]
            if expected is None:
                assert registers[1] == argument
            else:
                assert registers[1] != argument
                assert bytes(cpu.mem_read(registers[1], len(expected) + 1)) == expected + b'\0'
            assert bytes(cpu.mem_read(argument, len(value) + 1)) == value + b'\0'
            cases.append(dict(table=table, source_hex=value.hex(), normalized_hex=expected.hex() if expected else None))
    value = b'Guard \x82\x50.'
    for parent, table, offset, target in (
        (0x02053F40, 0x02117AE0, 0x274, renderer),
        (0x02053DB8, AMOUNT_TABLES[0], 0x27C, legacy),
        (0x02053F40, AMOUNT_TABLES[1] + 4, 0x274, legacy),
    ):
        cpu.mem_write(argument, value + b'\0')
        stack = {0x264: parent, 0x274: 0, 0x27C: 0} | {offset: table}
        actual, registers = run(cpu, selector.HOOK, stack, (renderer, legacy))
        assert actual == target and registers == portrait.ARGS
        cases.append(dict(table=table, parent=parent, source_hex=value.hex(), unchanged=True))
    return cases


def seal_layout(viewed):
    assert not VISUAL.exists()
    proof = base.load(PROOF)
    assert base.digest(ROM) == proof['research_ROM_sha256']
    assert base.digest(stage.OUTPUT) == proof['manuscript_sha256']
    assert viewed == [row['sha256'] for row in proof['sheets']]
    assert all(base.digest(row['path']) == row['sha256'] for row in proof['sheets'])
    assert len(proof['records']) == 47 and proof['native_pages'] == proof['native_cases'] == 89
    assert sum(len(row['messages']) for row in proof['sheets']) == 89
    tests = list(ElementTree.parse(QA).iter('testsuite'))
    assert sum(int(row.get('tests', 0)) for row in tests) == 34
    assert all(int(row.get(key, 0)) == 0 for row in tests for key in ('errors', 'failures', 'skipped'))
    arm = base.NdsImage.open(ROM).read_file(stage.first.ARM)
    amount = amount_controls(arm, proof['ownership'])
    assert len(amount) == 15
    base.save(VISUAL, dict(candidate_sha256=proof['research_ROM_sha256'], native_pages=89, stored_cases=47,
        all_pages_viewed=True, complete_glyphs_and_bounds=True, repository_tests=34,
        original_amount_control_cases=amount, original_formatter_input_unchanged=True,
        sheet_sha256=viewed, evidence={str(p): base.digest(p) for p in (PROOF, stage.OUTPUT, QA, Path(__file__))},
        representative_gameplay_and_registration_pending=True, new_credit=0))
    print('Verified all 89 viewed pages, 15 digit-scope controls and 34 repository tests.')


def verify_startup():
    loader = SimpleNamespace(load=base.load, RELEASE=stage.first.review.parent.RELEASE,
                             NdsImage=base.NdsImage, ARM=stage.first.ARM)
    FunctionType(prior_startup.verify_startup.__code__, vars(prior_startup) | globals() | {'stage': loader})()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=('layout', 'startup'))
    parser.add_argument('--viewed-sheets', nargs='+')
    args = parser.parse_args()
    if args.action == 'startup':
        verify_startup()
    else:
        seal_layout(args.viewed_sheets)
