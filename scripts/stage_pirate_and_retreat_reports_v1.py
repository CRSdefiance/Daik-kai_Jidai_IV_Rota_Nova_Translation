"""Verify the original pirate portraits, bearing routing and port-order wraps."""

from hashlib import sha256
from inspect import getsource
from pathlib import Path

from unicorn import UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_LR, UC_ARM_REG_PC, UC_ARM_REG_R0, UC_ARM_REG_R1
from unicorn.arm_const import UC_ARM_REG_R2, UC_ARM_REG_R3, UC_ARM_REG_R4, UC_ARM_REG_SP

from dk4tool.patch import pirate_report_bearings_v1 as bearings
from scripts import review_pirate_and_retreat_reports_v1 as review
from scripts import stage_fleet_reports_v1 as first
from scripts.probe_button_prompt_native import STACK, STOP, machine
from scripts.source_locked_derivation_v5118 import checked_text


ROOT = Path('out/pirate_and_retreat_reports_staged_20261111_v1')
ROM, PROOF = ROOT / 'pirate_and_retreat_reports_RESEARCH_ONLY.nds', ROOT / 'stored_verification.json'
OUTPUT = review.OUTPUT
PHRASES = {
    2657: ("We'll put into a nearby port", 'and wait for orders.'),
    2660: ('a nearby port for now.',),
    2661: ("Can't be helped.", "We'll put into a nearby port."),
}


def bearing_controls(arm):
    cpu = machine(arm)
    seen = []

    def stop(u, pc, size, data):
        seen.append(pc)
        u.emu_stop()

    cpu.hook_add(UC_HOOK_CODE, stop, begin=bearings.WRAPPER, end=bearings.WRAPPER)
    tests = [(table, ptr, text) for table in bearings.TABLES for ptr, _, text in bearings.BEARINGS]
    tests += [(bearings.TABLES[0], bearings.BEARINGS[0][0] + 4, None),
              (bearings.TABLES[1], bearings.BEARINGS[-1][0] + 4, None),
              (bearings.TABLES[0], bearings.BEARINGS[0][0] + 1, None),
              (0x02116A80, bearings.BEARINGS[1][0], None)]
    results = []
    registers = (UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3, UC_ARM_REG_R4)
    for table, pointer, english in tests:
        seen.clear()
        supplied = (7, table, pointer, 0x02460040, 0xA6B7C8D9)
        for reg, value in zip(registers, supplied, strict=True):
            cpu.reg_write(reg, value)
        cpu.reg_write(UC_ARM_REG_SP, STACK)
        cpu.reg_write(UC_ARM_REG_LR, STOP)
        cpu.emu_start(bearings.CALL, STOP, count=256)
        assert seen == [bearings.WRAPPER] and cpu.reg_read(UC_ARM_REG_PC) == bearings.WRAPPER
        assert cpu.reg_read(UC_ARM_REG_LR) == bearings.CALL + 4 and cpu.reg_read(UC_ARM_REG_SP) == STACK
        actual = tuple(cpu.reg_read(reg) for reg in registers)
        assert actual[:2] == supplied[:2] and actual[3:] == supplied[3:]
        if english is None:
            assert actual[2] == pointer
        else:
            assert actual[2] != pointer
            assert bytes(cpu.mem_read(actual[2], len(english) + 1)) == english + b'\0'
        results.append(dict(table=table, original_pointer=pointer, received_pointer=actual[2],
            localized_hex=english.hex() if english else None, native_wrapper_and_other_arguments_preserved=True))
    assert len(results) == 22
    return results


def stage(runtime, release, rows, groups, verified=None):
    def selector_checks(arm, execute):
        if verified is None:
            return execute(arm)
        assert sha256(arm).hexdigest() == verified['ownership']['bearing']['source_ARM9_sha256']
        return verified['ownership']['selector_checks']

    source = checked_text(getsource(first.prior.stage), {
        "group['runtime_item_name_inputs']": "group['argument_kind']",
        "allocation['touched_blocks'] == [26, 27]": "allocation['touched_blocks'] == [27, 28]",
        "checks = env['verify_scope'](arm)": "checks = check_exact_selector(arm, env['verify_scope'])",
    })
    env = vars(first.prior) | {'review': review, 'PHRASES': PHRASES, 'check_exact_selector': selector_checks}
    exec(compile(source, __file__ + '::pirate-and-port-storage', 'exec'), env)
    arm, common, storage, rebound, allocation, ownership = env['stage'](runtime, release, rows, groups)
    patched, receipt = bearings.install(arm, sha256(arm).hexdigest())
    if verified is None:
        controls = bearing_controls(patched)
    else:
        assert sha256(patched).hexdigest() == verified['research_ARM9_sha256']
        controls = verified['ownership']['bearing_controls']
    return patched, common, storage, rebound, allocation, ownership | {'bearing': receipt, 'bearing_controls': controls}


def samples(kind, argument_groups, number):
    if kind is None:
        return [None]
    names = argument_groups['pirate']
    short = next(row for row in names if row['arguments'] == [b'Jean'.hex()])
    long = max(names, key=lambda row: len(row['arguments'][0]))
    assert short['arguments'] != long['arguments']
    if kind == 'pirate':
        return [short, long]
    assert kind == 'bearing_and_pirate'
    directions = argument_groups['bearings']
    return [name | {'arguments': [direction['localized_hex'], *name['arguments']], 'bearing': direction}
            for name, direction in ((short, directions[0]), (long, max(directions, key=lambda row: len(row['localized_hex']))))]


def main():
    source = checked_text(getsource(first.main), {
        'assert len(records) == 47 and len(pages) == 89': 'assert len(records) == 48 and len(pages) == 71',
    })
    env = vars(first) | globals()
    exec(compile(source, __file__ + '::pirate-and-port-native-portraits', 'exec'), env)
    env['main']()


if __name__ == '__main__':
    main()
