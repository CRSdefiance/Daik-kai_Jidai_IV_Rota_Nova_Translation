"""Check remaining caller leads with bounded original conditional fragments."""

from pathlib import Path
from struct import pack, unpack_from

from unicorn import UC_HOOK_CODE
from unicorn.arm_const import (
    UC_ARM_REG_LR, UC_ARM_REG_PC, UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R3,
    UC_ARM_REG_R4, UC_ARM_REG_R5, UC_ARM_REG_R6, UC_ARM_REG_R7, UC_ARM_REG_SP,
)

from scripts import checkpoint_pending_shared_native_20261115 as prior
from scripts import register_market_trade_dialogue_20261115 as current
from scripts.probe_button_prompt_native import BASE, STACK, VIEW, call, machine


base, sha = current.base, prior.sha
OUTPUT = prior.ROOT / 'shared_conditional_callers_20261115_v1.json'
DEFAULT = 0xFFFFFFFF
REGISTER_CASES = {
    0x1351C: (0x1350C, UC_ARM_REG_R4, {14: 1358, 15: 1357, 16: 1358, DEFAULT: 1358}),
    0x13668: (0x13658, UC_ARM_REG_R0, {0: 1360, 1: 1359, DEFAULT: 1359}),
    0x5E11C: (0x5E10C, UC_ARM_REG_R0, {0: 1159, 1: 1163, DEFAULT: 1163}),
    0x5FBB8: (0x5FBA8, UC_ARM_REG_R4, {0x80000000: 734, 134: 734, 135: 732, 0x7FFFFFFF: 732, DEFAULT: 734}),
    0xBA37C: (0xBA354, UC_ARM_REG_R0, {0: 771, 1: 8, 2: 8, 3: 772, 4: 773, 5: 8, DEFAULT: 8}),
}
MEMORY_CASES = {
    0x59D78: (0x59D64, VIEW + 8, (819, 818)),
    0x59D94: (0x59D80, VIEW + 8, (53, 52)),
    0x59F04: (0x59EF0, VIEW + 8, (61, 60)),
    0xBBEE8: (0xBBED4, STACK + 0x10, (778, 775)),
    0xBC0A8: (0xBC094, STACK + 0x10, (783, 782)),
    0xBC0D8: (0xBC0C4, STACK + 0x10, (9, 10)),
}


def bounds(clean, arm, start, site):
    assert clean[start:site + 4] == arm[start:site + 4]
    target, = prior.branch_hits(clean[start:site + 4], BASE + start, {0x02053FE4})
    assert target == (BASE + site, 0x02053FE4, 'arm_bl')
    literals = []
    for i in range(start, site, 4):
        instruction, = unpack_from('<I', clean, i)
        if instruction >> 28 == 15 or instruction & 0x0F7F0000 != 0x051F0000:
            continue
        displacement = instruction & 0xFFF
        address = i + 8 + (displacement if instruction & 0x800000 else -displacement)
        assert clean[address:address + 4] == arm[address:address + 4]
        literals.append(dict(offset=address, word=unpack_from('<I', clean, address)[0]))
    return dict(start=BASE + start, call_site=BASE + site, pc_relative_literals=literals,
                clean_code_sha256=sha(clean[start:site + 4]))


def run_cases(clean, arm, pending):
    cpus = [machine(raw) for raw in (clean, arm)]
    rows = []
    for site in sorted(REGISTER_CASES.keys() | MEMORY_CASES.keys()):
        if site in REGISTER_CASES:
            start, register, cases = REGISTER_CASES[site]
            memory = None
        else:
            start, memory, (zero, other) = MEMORY_CASES[site]
            register, cases = None, {0: zero, 1: other, DEFAULT: other}
        source = bounds(clean, arm, start, site)
        assert set(cases.values()).isdisjoint(pending)
        for cpu in cpus:
            cpu.reg_write(UC_ARM_REG_SP, STACK)
            cpu.reg_write(UC_ARM_REG_R7, VIEW)
            cpu.mem_write(STACK + 0xC, pack('<I', VIEW))
            for value, expected in cases.items():
                if register:
                    cpu.reg_write(register, value)
                else:
                    cpu.mem_write(memory, pack('<I', value))
                cpu.emu_start(BASE + start, BASE + site, count=32)
                assert cpu.reg_read(UC_ARM_REG_PC) == BASE + site
                assert cpu.reg_read(UC_ARM_REG_R1) == expected, (hex(site), value, cpu.reg_read(UC_ARM_REG_R1))
        rows.append(source | dict(test_values=cases, input_register=register, input_fixture_address=memory,
                                  distinct_message_IDs=sorted(set(cases.values()))))
    return rows


def numeric_use(clean, arm):
    spans = ((0x5F4AC, 0x5F4CC), (0x5F5B4, 0x5F5D8), (0x5F60C, 0x5F614),
             (0x316F0, 0x316F8), (0x3182C, 0x31834), (0x7E1BC, 0x7E24C), (0x7E24C, 0x7E2DC))
    assert all(clean[a:b] == arm[a:b] for a, b in spans)
    samples = (-10001, -101, -100, -1, 0, 1, 99, 100, 101, 10001)
    for raw in (clean, arm):
        cpu = machine(raw)
        for start, end, source_reg in ((0x5F4AC, 0x5F4CC, UC_ARM_REG_R3), (0x5F5B4, 0x5F5D8, UC_ARM_REG_R7)):
            for value in samples:
                cpu.reg_write(source_reg, value & DEFAULT)
                cpu.emu_start(BASE + start, BASE + end, count=16)
                signed_remainder = abs(value) % 100 * (-1 if value < 0 else 1)
                assert cpu.reg_read(UC_ARM_REG_PC) == BASE + end
                assert cpu.reg_read(UC_ARM_REG_R6) == signed_remainder & DEFAULT

        cpu.reg_write(UC_ARM_REG_SP, STACK)
        cpu.emu_start(BASE + 0x316F0, BASE + 0x316F8, count=4)
        cpu.emu_start(BASE + 0x3182C, BASE + 0x31830, count=4)
        assert cpu.reg_read(UC_ARM_REG_R1) == 300
        assert prior.branch_hits(raw[0x31830:0x31834], BASE + 0x31830, {0x0207E1BC}) == [
            (BASE + 0x31830, 0x0207E1BC, 'arm_bl')]
        helper_calls = []

        def stable_level(u, address, _size, _data):
            helper_calls.append(address)
            u.reg_write(UC_ARM_REG_R0, 1)
            u.reg_write(UC_ARM_REG_PC, u.reg_read(UC_ARM_REG_LR))

        hook = cpu.hook_add(UC_HOOK_CODE, stable_level, begin=BASE + 0x7E6E4, end=BASE + 0x7E6E4)
        try:
            cpu.mem_write(VIEW, bytes(0x20))
            cpu.mem_write(VIEW + 0x10, pack('<I', 800))
            before = bytes(cpu.mem_read(VIEW, 0x20))
            call(cpu, 0x7E1BC, (VIEW, 300, 0))
            assert helper_calls == [BASE + 0x7E6E4] * 2
            assert bytes(cpu.mem_read(VIEW, 0x20)) == before[:0x10] + pack('<I', 1100) + before[0x14:]
        finally:
            cpu.hook_del(hook)
    return [dict(id=100, locations=[0x0205F4BC, 0x0205F5C8], purpose='Signed remainder divisor', input_samples=samples),
            dict(id=300, locations=[0x020316F0, 0x02031830], purpose='Adds 300 to the original crew object field at +0x10',
                 helper_return_supplied=True, isolated_object_fixture=True)]


def main():
    assert not OUTPUT.exists()
    release, census = map(base.load, (current.RELEASE, prior.LEGACY))
    assert base.digest(base.REGISTRY) == release['registry_sha256']
    assert base.digest(current.ROM) == release['candidate_sha256']
    assert base.digest(current.stage.CLEAN) == release['clean_input_sha256']
    ja, en = (base.NdsImage.open(p).read_file(current.stage.ARM) for p in (current.stage.CLEAN, current.ROM))
    assert sha(en) == release['target_ARM9_sha256']
    rows = run_cases(ja, en, set(census['pending_ids']))
    scoped = {r['call_site'] for r in rows}
    historical = set(census['unresolved_candidate_calls'])
    assert scoped <= historical and len(scoped) == 11
    collisions = numeric_use(ja, en)
    base.save(OUTPUT, dict(candidate_sha256=release['candidate_sha256'], clean_sha256=release['clean_input_sha256'],
        conditional_selectors=rows, pending_literal_collisions=collisions, historical_unresolved_site_count=len(historical),
        unresolved_sites_after_this_receipt=sorted(historical - scoped), other_classifications_open=True,
        new_gameplay_runs=0, new_editorial_credit=0, full_goal_complete=False,
        evidence={str(path): base.digest(path) for path in (current.RELEASE, prior.LEGACY, Path(__file__))}))
    print(f'Bound {len(scoped)} conditional call sites and checked three numeric coincidences in both ROMs.')


if __name__ == '__main__':
    main()
