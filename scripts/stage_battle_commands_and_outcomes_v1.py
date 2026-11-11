"""Run the native battle portraits and town-attack confirmation from stored text."""

from hashlib import sha256
from inspect import getsource
from pathlib import Path
from types import SimpleNamespace

from unicorn import UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_LR, UC_ARM_REG_PC, UC_ARM_REG_R0, UC_ARM_REG_R1
from unicorn.arm_const import UC_ARM_REG_R2, UC_ARM_REG_R3, UC_ARM_REG_R4, UC_ARM_REG_SP

from dk4tool.patch import special_battle_target_names_v1 as names
from scripts import review_battle_commands_and_outcomes_v1 as review
from scripts import stage_fleet_reports_v1 as first
from scripts.probe_button_prompt_native import STACK, STOP, machine
from scripts.source_locked_derivation_v5118 import checked_text


ROOT = Path('out/battle_commands_and_outcomes_staged_20261111_v1')
ROM, PROOF = ROOT / 'battle_commands_and_outcomes_RESEARCH_ONLY.nds', ROOT / 'stored_verification.json'
OUTPUT = review.OUTPUT
PHRASES = {2110: ('Our ram struck the enemy ship', 'square in the side!')}
MODAL_PARENT = (0x02053D24, 0x27C)


def alias_controls(arm):
    cpu = machine(arm)

    def stop(u, pc, size, data):
        u.emu_stop()

    cpu.hook_add(UC_HOOK_CODE, stop, begin=names.WRAPPER, end=names.WRAPPER)
    tests = [(old.encode('cp932'), value.encode('ascii')) for old, value in names.ALIASES]
    tests += [(b'Ghost Ship', None), (b'Ghostly', None), (b'\x89\xbb\x8b\x9b!', None), (None, None)]
    receipt = []
    registers = (UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3, UC_ARM_REG_R4)
    for old, translated in tests:
        at = 0x02470001 if old is not None else 0
        if old is not None:
            cpu.mem_write(at, old + b'\0')
        initial = (1, names.TABLE, at, 0xA5A510FF, 0xA5A540FF)
        for reg, value in zip(registers, initial, strict=True):
            cpu.reg_write(reg, value)
        cpu.reg_write(UC_ARM_REG_SP, STACK)
        cpu.reg_write(UC_ARM_REG_LR, STOP)
        cpu.emu_start(names.CALL, STOP, count=512)
        assert cpu.reg_read(UC_ARM_REG_PC) == names.WRAPPER
        assert cpu.reg_read(UC_ARM_REG_LR) == names.CALL + 4 and cpu.reg_read(UC_ARM_REG_SP) == STACK
        final = tuple(cpu.reg_read(reg) for reg in registers)
        assert final[:2] == initial[:2] and final[3:] == initial[3:]
        if translated is None:
            assert final[2] == at
        else:
            assert final[2] != at and bytes(cpu.mem_read(final[2], len(translated) + 1)) == translated + b'\0'
        receipt.append(dict(input_hex=old.hex() if old else None, localized=translated.decode('ascii') if translated else None,
            source_return_and_all_other_argument_registers_preserved=True))
    return receipt


def stage(runtime, release, rows, groups, verified=None):
    def selector_checks(arm, execute):
        if verified is None:
            return execute(arm)
        assert sha256(arm).hexdigest() == verified['ownership']['target_names']['source_ARM9_sha256']
        return verified['ownership']['selector_checks']

    source = checked_text(getsource(first.prior.stage), {
        "group['runtime_item_name_inputs']": "group['argument_kind']",
        "allocation['touched_blocks'] == [26, 27]": "allocation['touched_blocks'] == [23]",
        "checks = env['verify_scope'](arm)": "checks = check_exact_selector(arm, env['verify_scope'])",
    })
    parents = first.prior.portrait.PARENTS | {review.MODAL: MODAL_PARENT}
    env = vars(first.prior) | {'review': review, 'PHRASES': PHRASES, 'check_exact_selector': selector_checks,
                              'portrait': SimpleNamespace(PARENTS=parents)}
    exec(compile(source, __file__ + '::battle-wrap-and-storage', 'exec'), env)
    arm, common, stored, rebound, allocation, ownership = env['stage'](runtime, release, rows, groups)
    arm, names_proof = names.install(arm, sha256(arm).hexdigest())
    if verified is None:
        controls = alias_controls(arm)
    else:
        assert sha256(arm).hexdigest() == verified['research_ARM9_sha256']
        controls = verified['ownership']['target_name_controls']
    return arm, common, stored, rebound, allocation, ownership | dict(target_names=names_proof, target_name_controls=controls)


def samples(kind, groups, number):
    if kind is None:
        return [None]
    if kind == 'special':
        return groups[kind]
    values = groups[kind]
    ordinary = b'Sao Tome' if kind == 'town' else b'Bergstrom Fleet'
    baseline = next(row for row in values if row['arguments'] == [ordinary.hex()])
    boundary = max((row for row in values if row['arguments'] != baseline['arguments']),
                   key=lambda row: len(row['arguments'][0]))
    return [baseline, boundary]


def original_portraits():
    portrait = first.portrait
    source = getsource(portrait.with_arguments)
    anchor = "    env = {**portrait_case.__globals__, 'ARGUMENT_MEMORY': 0x02470000}"
    source = checked_text(source, {anchor: '''    source = checked_text(source, {
        'actor_id, arguments):': 'actor_id, arguments, sample):',
        'for i, argument in enumerate(arguments):': 'for i, argument in enumerate(supplied(sample, arguments)):',
        'args = {0x53D44:': 'args = {MODAL: (1, key), 0x53D44:',
        'if pc == 0x02053D70 or': 'if pc == MODAL_ROLE or pc == 0x02053D70 or',
        'if entry == 0x53D44:\\n        hooks.append(0x02053D70)': 'if entry in (MODAL, 0x53D44):\\n        hooks.append(MODAL_ROLE if entry == MODAL else 0x02053D70)',
        'cpu.emu_start(BASE + entry, STOP, count=3000000)': 'cpu.emu_start(call_entry(group, BASE + entry), STOP, count=3000000)',
        'original_entry=BASE + entry': 'original_entry=call_entry(group, BASE + entry)',
    })
''' + anchor + "\n    env.update(extras)"})

    def supplied(sample, arguments):
        return (bytes.fromhex(sample['current_hex']),) if sample and 'model_ID' in sample else arguments

    def call_entry(group, entry):
        return names.CALL if group['argument_kind'] == 'special' else entry

    extras = dict(MODAL=review.MODAL, MODAL_ROLE=0x02053CDC, supplied=supplied, call_entry=call_entry,
                  PARENTS=portrait.portrait_case.__globals__['PARENTS'] | {review.MODAL: MODAL_PARENT})
    env = vars(portrait) | {'extras': extras}
    exec(compile(source, __file__ + '::native-modal-and-target-portraits', 'exec'), env)
    return env['with_arguments']()


def main():
    source = checked_text(getsource(first.main), {
        'ctx = portrait.with_components(runtime, arm, common)':
            'ctx = portrait.with_components(runtime, arm, common)\n'
            '    at = names.CALL - BASE\n'
            "    assert ctx.raw[at:at + 4] == bytes.fromhex(ownership['target_names']['original_call_hex'])\n"
            '    ctx.raw = ctx.raw[:at] + arm[at:at + 4] + ctx.raw[at + 4:]',
        'native = portrait.with_arguments()': 'native = original_portraits()',
        'actor, arguments)': 'actor, arguments, sample)',
        'assert len(records) == 47 and len(pages) == 89': 'assert len(records) == 29 and len(pages) == 65',
    })
    env = vars(first) | globals()
    exec(compile(source, __file__ + '::battle-command-portraits', 'exec'), env)
    env['main']()


if __name__ == '__main__':
    main()
