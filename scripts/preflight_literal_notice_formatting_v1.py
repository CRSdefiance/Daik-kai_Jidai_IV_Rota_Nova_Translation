"""Preflight logical shared notices through registered native varargs and wrapping."""

import struct
from collections import Counter
from pathlib import Path

from unicorn import UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_LR, UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3, UC_ARM_REG_SP

from scripts.audit_story_glyph_consistency import load, save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.probe_button_prompt_native import BASE, STACK, STOP
from scripts.registered_editorial_runtime_v2 import RegisteredRuntime
from scripts.review_literal_notice_callers_v1 import ARCHIVE, OUTPUT, RELEASE, STARTUP, WRAPPERS


TARGET = ARCHIVE / 'literal_notice_formatting_preflight.json'
VARIANTS = {
    85: [('１２',), ('１２３',)],
    86: [('１', '１', 'Sky: Sunny', 'Amsterdam'), ('１２', '３１', 'Sky: Overcast', 'Santo Domingo')],
    87: [('food',), ('drinking water',)],
    90: [('Lisbon',), ('Santo Domingo',)],
    91: [('Lisbon',), ('Santo Domingo',)],
    93: [('Lisbon', 'Castor Co.'), ('Santo Domingo', 'Bergstrom Fleet')],
    94: [('Lisbon', 'Hayreddin'), ('Santo Domingo', 'Captain Vassiliev')],
    95: [('Amsterdam', 'Argot Co.', 'Wool Cloth'), ('Santo Domingo', 'Bergstrom Fleet', 'Sandalwood')],
    96: [('Argot Co.',), ('Bergstrom Fleet',)],
    125: [('Lisbon',), ('Santo Domingo',)],
    126: [('Lisbon',), ('Santo Domingo',)],
}


def run_case(ctx, row, supplied):
    cpu, get, provider = ctx.machine(ctx.arm, ctx.common, ctx.raw, ctx.plan)
    wrapper = next(c['wrapper'] for c in row['current_copies'] if c['wrapper'] in WRAPPERS)
    template = row['english'].replace('{LB}', '\n').encode('ascii')
    test = 0x02660100
    cpu.mem_write(test-16, b'\xA5'*16 + template+b'\0' + b'\xA5'*16)
    pointers = [0x02660300+i*64 for i in range(len(supplied))]
    for address, argument in zip(pointers, supplied, strict=True):
        cpu.mem_write(address, argument.encode('cp932')+b'\0')
    padded = pointers + [0]*max(0, 3-len(pointers))
    if wrapper == BASE+0x54624:
        padded[0] = 1
    cpu.reg_write(UC_ARM_REG_SP, STACK)
    cpu.reg_write(UC_ARM_REG_LR, STOP)
    for register, value in zip([UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3],
            [row['message_ID'], *padded[:3]], strict=True):
        cpu.reg_write(register, value)
    if len(pointers) == 4:
        cpu.mem_write(STACK, struct.pack('<I', pointers[3]))
    original = bytes.fromhex(row['current_hex'])
    recorded = []

    def substitute_at_entry(u, pc, size, _):
        ptr = u.reg_read(UC_ARM_REG_R1)
        assert bytes(u.mem_read(ptr, len(original)+1)) == original+b'\0'
        vector = u.reg_read(UC_ARM_REG_R2)
        native = struct.unpack(f'<{len(pointers)}I', u.mem_read(vector, 4*len(pointers))) if pointers else ()
        assert tuple(pointers) == native
        recorded.append(dict(original_template_pointer=ptr, native_varargs_vector=vector, original_varargs_pointers=native))
        u.reg_write(UC_ARM_REG_R1, test)

    hook = cpu.hook_add(UC_HOOK_CODE, substitute_at_entry, begin=BASE+0x54774, end=BASE+0x54774)
    stop = BASE+0x5479C
    cpu.emu_start(wrapper, stop, count=3000000)
    cpu.hook_del(hook)
    assert len(recorded) == 1
    fmt, output = struct.unpack_from('<2I', ctx.arm, 0x54890)
    expanded = bytes(cpu.mem_read(fmt, 256)).split(b'\0')[0]
    display = bytes(cpu.mem_read(output, 256)).split(b'\0')[0]
    expected = template
    for argument in supplied:
        expected = expected.replace(b'%s', argument.encode('cp932'), 1)
    assert expanded == expected
    assert b' '.join(display.split()) == b' '.join(expected.split()), (row['id'], display, expected)
    assert bytes(cpu.mem_read(test-16, len(template)+33)) == b'\xA5'*16 + template+b'\0' + b'\xA5'*16
    assert bytes(cpu.mem_read(ctx.actor_root, 0x1A04)) == ctx.actor_bytes
    raw_lines = display.split(b'\n')
    lines = [raw.decode('cp932') for raw in raw_lines]
    excessive = [i+1 for i,line in enumerate(raw_lines) if len(line) > 35]
    return dict(message_ID=row['message_ID'], arguments=supplied, source_wrapper=wrapper, **recorded[0],
        expanded_hex=expanded.hex(), native_wrapper_output_hex=display.hex(), native_wrapper_lines=lines,
        native_width_units=[len(line) for line in raw_lines], lines_over_existing_35_unit_wrap_budget=excessive,
        over_three_rows=len(lines)>3, native_varargs_argument_sequence_and_complete_words_verified=True,
        scratch_template_test_before_widget_creation=True, original_storage_unmodified=True)


def main():
    assert not TARGET.exists()
    manuscript = load(OUTPUT)
    ctx = RegisteredRuntime(RELEASE, STARTUP, captain=3)
    assert ctx.receipt() == manuscript['runtime']
    results = []
    for row in manuscript['records']:
        samples = VARIANTS.get(row['message_ID'], [()])
        for supplied in samples:
            assert len(supplied) == row['native_substitution_count']
            results.append(run_case(ctx, row, supplied))
    issues = Counter(row['message_ID'] for row in results if row['lines_over_existing_35_unit_wrap_budget'] or row['over_three_rows'])
    assert len(results) == 41
    save(TARGET, dict(runtime=ctx.receipt(), cases=results, record_count=len(manuscript['records']),
        complete_native_expansion_cases=len(results), verified_original_fourth_stack_argument_for_86=True,
        records_needing_further_layout_work=sorted(issues), layout_diagnostic_count=sum(issues.values()),
        exact_template_scratch_override_only_at_original_modal_entry=True,
        distinct_consumers_andfinal_visual_and_native_formatting_still_pending=True,
        actual_gameplay=False, registered_release_pending=True, new_credit=0,
        evidence={str(p):digest(p) for p in [OUTPUT, Path(__file__)]}, full_goal_complete=False))
    print(f'All {len(results)} native format expansions pass. Width or row issues in {len(issues)} messages.')


if __name__ == '__main__':
    main()
