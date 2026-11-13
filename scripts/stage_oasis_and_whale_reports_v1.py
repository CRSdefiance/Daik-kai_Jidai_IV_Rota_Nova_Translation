"""Verify the native dialogues and reuse the registered full region provider."""

from hashlib import sha256
from inspect import getsource
from itertools import product
from pathlib import Path
from struct import unpack_from

from unicorn import UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_LR, UC_ARM_REG_PC, UC_ARM_REG_R0, UC_ARM_REG_R1
from unicorn.arm_const import UC_ARM_REG_R2, UC_ARM_REG_R3, UC_ARM_REG_R8, UC_ARM_REG_SL, UC_ARM_REG_SP

from dk4tool.patch import compact_portrait_selector_v1 as compact
from scripts import review_oasis_and_whale_reports_v1 as review
from scripts import stage_fleet_reports_v1 as first
from scripts.probe_button_prompt_native import STACK, STOP, machine
from scripts.probe_common_display_name_hook import branch_link
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.verify_shared_crew_selector_v1 import ARGS, dispatch


ROOT = Path('out/oasis_and_whale_reports_staged_20261111_v1')
ROM, PROOF = ROOT / 'oasis_and_whale_reports_RESEARCH_ONLY.nds', ROOT / 'stored_verification.json'
OUTPUT = review.OUTPUT
BASE = review.BASE
REGION_CALL, LEGACY = 0x02079D04, 0x020945B4
PROOF_TABLE, PROOF_CALL, QUEUED = 0x02116CA0, 0x02079D2C, 0x02053D44
PHRASES = {
    2290: ('found an oasis!', 'Come on, hurry!'),
    2302: ('It looks like it was a mirage,',),
    2311: ('stuck in a bottomless bog!',),
    2312: ('stuck in a bottomless bog!',),
    2313: ('stuck in a bottomless bog!',),
    2344: ('Shall we defeat it ourselves?',),
    2345: ('what are you doing?',),
    2347: ("what's the matter?", 'Please attack, now!'),
    2352: ("The white whale's getting away...", 'where it dived!'),
    2353: ("What's that?!", 'where it dived!'),
    2356: ('where it dove!',),
    2357: ("the white whale escaped...", 'where it dove!'),
    2358: ('the white whale got away...', 'where it dove!'),
}


def install_region(arm):
    at = REGION_CALL - BASE
    before = branch_link(REGION_CALL, LEGACY).to_bytes(4, 'little')
    after = branch_link(REGION_CALL, review.REGION).to_bytes(4, 'little')
    assert arm[at:at + 4] == before
    assert unpack_from('<I', arm, 0x79FD0)[0] == PROOF_TABLE
    patched = arm[:at] + after + arm[at + 4:]
    assert patched[:at] + before + patched[at + 4:] == arm
    return patched, dict(call=REGION_CALL, old_provider=LEGACY, registered_dialogue_provider=review.REGION,
        original_call_hex=before.hex(), localized_call_hex=after.hex(),
        source_ARM9_sha256=sha256(arm).hexdigest(), target_ARM9_sha256=sha256(patched).hexdigest(),
        only_one_original_call_changed=True, exact_inverse=True)


def stage(runtime, release, rows, groups, verified=None):
    previous = review.prior.load(review.parent.VERIFICATION / 'stored_verification.json')['ownership']
    guard, previous_fallback = compact.shared_guard(runtime.arm, previous)

    def assemble_scope(parameters):
        static, dynamic = (parameters[key] for key in ('STATIC', 'DYNAMIC'))
        old_tables = {tuple(key): values for key, values in previous['literal_scopes']}
        assert not previous['dynamic_scopes']
        assert all(not set(values) & set(old_tables.get(key, ())) for scope in (static, dynamic)
                   for key, values in scope.items())
        return lambda: compact.assembly(static, dynamic, parameters['PRIOR'], guard)

    def selector_checks(arm, static, dynamic, parent):
        if verified is None:
            return verify_scope(arm, static, dynamic, parent, previous_fallback)
        assert sha256(arm).hexdigest() == verified['ownership']['region_provider']['source_ARM9_sha256']
        return verified['ownership']['selector_checks']

    source = checked_text(getsource(first.prior.stage), {
        "group['runtime_item_name_inputs']": "group['argument_kind']",
        "allocation['touched_blocks'] == [26, 27]": "allocation['touched_blocks'] == [24, 25]",
        'assemble = FunctionType(selector.assembly.__code__, vars(selector) | parameters)': 'assemble = assemble_scope(parameters)',
        "checks = env['verify_scope'](arm)": "checks = check_exact_selector(arm, static, dynamic, predecessor)",
    })
    env = vars(first.prior) | {'review': review, 'PHRASES': PHRASES, 'check_exact_selector': selector_checks,
                              'assemble_scope': assemble_scope}
    exec(compile(source, __file__ + '::oasis-and-whale-storage', 'exec'), env)
    arm, common, stored, rebound, allocation, ownership = env['stage'](runtime, release, rows, groups)
    arm, receipt = install_region(arm)
    ownership['region_provider'] = receipt
    ownership['shared_existing_static_guard'] = dict(address=guard, original_failed_guard_target=previous_fallback)
    if verified:
        assert receipt == verified['ownership']['region_provider']
        ownership['native_proof_argument_prefixes'] = verified['ownership']['native_proof_argument_prefixes']
    return arm, common, stored, rebound, allocation, ownership


def verify_scope(arm, static, dynamic, previous, failed_guard):
    native = compact.native
    cpu = machine(arm)
    source = checked_text(getsource(dispatch), {'count=128': 'count=1024'})
    env = dict(dispatch.__globals__)
    exec(compile(source, __file__ + '::selector-controls', 'exec'), env)
    run = env['dispatch']
    scope = {key: static.get(key, ()) + dynamic.get(key, ()) for key in static.keys() | dynamic.keys()}
    keys = sorted({key + delta for values in scope.values() for key in values for delta in (-4, 0, 4)})
    parents = sorted({parent for parent, _ in scope} | {0x02053C14, 0x02053D24})
    offsets = (0x270, 0x274, 0x27C)
    compiled = (b' Whole line\n  Second row', b'W' * 36 + b'\n  Second row')
    tests = (*compiled, b'Ordinary text.', b' Unprotected\nRow', b'W' * 37 + b'\n  Second row')
    choices = dict.fromkeys((previous, failed_guard, native.LITERAL_COPY, native.LITERAL_PARAGRAPH), 0)
    for parent, offset, key, text in product(parents, offsets, keys, tests):
        cpu.mem_write(ARGS[1], text + b'\0')
        stack = {0x264: parent, **dict.fromkeys(offsets, 0), offset: key}
        if key in dynamic.get((parent, offset), ()):
            expected = native.LITERAL_PARAGRAPH
        elif key in static.get((parent, offset), ()):
            expected = native.LITERAL_COPY if text in compiled else failed_guard
        else:
            expected = previous
        target, regs = run(cpu, native.HOOK, stack, tuple(choices))
        assert target == expected and regs == ARGS, (parent, offset, key, text)
        choices[target] += 1
    assert all(choices.values())
    return dict(tested=sum(choices.values()), previous_selector=choices[previous],
                previous_guard_fallback=choices[failed_guard], literal_copy=choices[native.LITERAL_COPY],
                dynamic_paragraph=choices[native.LITERAL_PARAGRAPH], original_registers_and_stack_preserved=True)


def samples(kind, groups, number):
    if kind is None:
        return [None]
    values = groups[kind]
    if kind == 'proof':
        return values
    assert kind == 'figurehead'
    key = lambda row: len(row['arguments'][0])
    return [min(values, key=key), max(values, key=key)]


def verify_proof_prefix(ctx, samples, ownership):
    at = REGION_CALL - BASE
    assert ctx.raw[at:at + 4].hex() == ownership['original_call_hex']
    assert ctx.arm[at:at + 4].hex() == ownership['localized_call_hex']
    ctx.raw = ctx.raw[:at] + ctx.arm[at:at + 4] + ctx.raw[at + 4:]
    cpu, get, provider = ctx.machine(ctx.arm, ctx.common, ctx.raw, ctx.plan)
    root = get(0xCB190) + 4
    arguments = []

    def word(at):
        return unpack_from('<I', cpu.mem_read(at, 4))[0]

    def stop(u, pc, size, data):
        assert u.reg_read(UC_ARM_REG_R0) == 7 and u.reg_read(UC_ARM_REG_R1) == PROOF_TABLE
        fields = [u.reg_read(reg) for reg in (UC_ARM_REG_R2, UC_ARM_REG_R3)]
        values = [bytes(u.mem_read(field, 64)).split(b'\0', 1)[0].hex() for field in fields]
        arguments.append(dict(region_pointer=fields[0], item_pointer=fields[1], arguments=values))
        u.emu_stop()

    cpu.hook_add(UC_HOOK_CODE, stop, begin=QUEUED, end=QUEUED)
    for sample in samples:
        index = sample['item_ID']
        obj = root + 20 * index
        cpu.reg_write(UC_ARM_REG_R8, obj)
        cpu.reg_write(UC_ARM_REG_SL, index)
        cpu.reg_write(UC_ARM_REG_SP, STACK)
        cpu.reg_write(UC_ARM_REG_LR, STOP)
        cpu.emu_start(BASE + 0x79D00, STOP, count=10000)
        assert cpu.reg_read(UC_ARM_REG_PC) == QUEUED and cpu.reg_read(UC_ARM_REG_LR) == PROOF_CALL + 4
        assert cpu.reg_read(UC_ARM_REG_SP) == STACK
        assert arguments[-1]['arguments'] == sample['arguments']
        assert arguments[-1]['region_pointer'] == sample['dialogue_region_pointer']
        assert sample['item_name_getter'] == word(word(obj) + 8)
    assert {REGION_CALL, review.REGION, PROOF_CALL} <= provider.executed_current
    assert len(arguments) == len(samples) == 7
    ctx.calls.clear()
    return arguments


def main():
    source = checked_text(getsource(first.main), {
        '    render, _, font = portrait.font_tools(runtime.image)':
            "    source_calls = verify_proof_prefix(ctx, draft['initialized_argument_samples']['proof'], ownership['region_provider'])\n"
            '    render, _, font = portrait.font_tools(runtime.image)',
        'assert len(records) == 47 and len(pages) == 89': 'assert len(records) == 71 and len(pages) == 125',
        'allocation=allocation, ownership=ownership,':
            'allocation=allocation, ownership=ownership | {\'native_proof_argument_prefixes\': source_calls},',
    })
    env = vars(first) | globals()
    exec(compile(source, __file__ + '::oasis-and-whale-portraits', 'exec'), env)
    env['main']()


if __name__ == '__main__':
    main()
