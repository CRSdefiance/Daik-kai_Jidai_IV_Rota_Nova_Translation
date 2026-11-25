"""Trace incoming references to the original shared-text forwarding routines."""

from collections import Counter
from pathlib import Path
from struct import unpack_from

from capstone import CS_AC_WRITE, CS_ARCH_ARM, CS_MODE_ARM, Cs
from capstone.arm_const import ARM_OP_MEM, ARM_REG_SP
from ndspy.rom import NintendoDSRom
from unicorn.arm_const import UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R4, UC_ARM_REG_SP

from scripts import checkpoint_shared_crew_and_wrapper_routes_20261115 as wrappers
from scripts import checkpoint_shared_message_producers_20261115 as producer
from scripts import checkpoint_shared_selector_ranges_20261115 as previous
from scripts import checkpoint_shared_table_callers_20261115 as shared
from scripts import register_market_trade_dialogue_20261115 as current
from scripts.probe_button_prompt_native import BASE, STACK, VIEW, call, machine


base = current.base
OUTPUT = previous.OUTPUT.with_name('shared_wrapper_inputs_20261115_v1.json')
ENTRIES = {BASE + row[0] for row in wrappers.WRAPPERS.values()}


def census(path):
    refs = set()
    for component, address, data in producer.inventory.components(NintendoDSRom.fromFile(path)):
        refs.update((site, entry, kind, component)
                    for site, entry, kind in producer.inventory.branch_hits(data, address, ENTRIES))
    return refs


def first_inputs(ja, en, source):
    constants = ((0x32348, 0x3234C, 0x53C24, UC_ARM_REG_R0, 469),
                 (0x58000, 0x58004, 0x53C24, UC_ARM_REG_R0, 825),
                 (0x58058, 0x5805C, 0x53C24, UC_ARM_REG_R0, 825),
                 (0x56FB8, 0x56FBC, 0x53DCC, UC_ARM_REG_R1, 1020),
                 (0x9DFE8, 0x9DFF4, 0x54624, UC_ARM_REG_R0, 120))
    cpus = [machine(raw) for raw in (ja, en)]
    rows = []
    for start, site, entry, register, expected in constants:
        locks = producer.literal_dependencies(ja, en, start, site + 4)
        for cpu in cpus:
            cpu.reg_write(UC_ARM_REG_R0, VIEW)
            cpu.reg_write(UC_ARM_REG_R1, VIEW)
            # The COMMON 120 selector has a neighboring store to r4 + 0x81c.
            if site == 0x9DFF4:
                cpu.reg_write(UC_ARM_REG_R4, VIEW)
            shared.run_to(cpu, start, site)
            assert cpu.reg_read(register) == expected
        rows.append(dict(site=BASE + site, entry=BASE + entry, supported_ids=[expected], code=locks))

    decoder = Cs(CS_ARCH_ARM, CS_MODE_ARM)
    decoder.detail = True
    start, store, read, site = 0x57524, 0x57528, 0x575EC, 0x575F0
    write_sites = [insn.address for insn in decoder.disasm(ja[store:site], BASE + store)
                   if any(op.type == ARM_OP_MEM and op.mem.base == ARM_REG_SP and op.mem.disp == 0x28
                          and op.access & CS_AC_WRITE for op in insn.operands)]
    assert write_sites == [BASE + store]
    for cpu in cpus:
        cpu.reg_write(UC_ARM_REG_SP, STACK)
        shared.run_to(cpu, start, store + 4)
        shared.run_to(cpu, read, site)
        assert cpu.reg_read(UC_ARM_REG_R1) == 904
    rows.append(dict(site=BASE + site, entry=0x02053DCC, supported_ids=[904], original_slot=0x28,
        code=producer.literal_dependencies(ja, en, start, site + 4)))

    start, site, table = 0x2C558, 0x2C560, 0x02117000
    slots = unpack_from('<8I', ja, table - BASE)
    fallback = next(value for value in slots if value != previous.FALLBACK)
    values = [fallback if value == previous.FALLBACK else value for value in slots]
    for cpu in cpus:
        shared.run_to(cpu, start, site)
        assert cpu.reg_read(UC_ARM_REG_R1) == table
        for index, value in enumerate(values):
            hook = previous.native_return(cpu, 0x7E988, index)
            call(cpu, 0x53F4C, (VIEW, table))
            cpu.hook_del(hook)
            assert cpu.reg_read(UC_ARM_REG_R0) == value
    rows.append(dict(site=BASE + site, entry=0x02053EC0, supported_ids=sorted(set(values)),
        code=producer.literal_dependencies(ja, en, start, site + 4) + [
            shared.lock(ja, en, 0x53F4C, 0x53F9C), shared.lock(ja, en, table - BASE, table - BASE + 32)],
        voice_slots=values))
    assert all((r['site'], r['entry'], 'arm_bl', 'ARM9 section 0') in source for r in rows)
    complete_entries = {r['entry'] for r in rows}
    assert {(r['site'], r['entry']) for r in rows} == {(s, e) for s, e, _, _ in source if e in complete_entries}
    return rows, sorted(complete_entries)


def main():
    assert not OUTPUT.exists()
    release, prior = map(base.load, (current.RELEASE, previous.OUTPUT))
    assert base.digest(base.REGISTRY) == release['registry_sha256']
    assert base.digest(current.ROM) == prior['candidate_sha256'] == release['candidate_sha256']
    assert base.digest(current.stage.CLEAN) == prior['clean_sha256'] == release['clean_input_sha256']
    source, target = (census(path) for path in (current.stage.CLEAN, current.ROM))
    ja, en = (base.NdsImage.open(p).read_file(current.stage.ARM) for p in (current.stage.CLEAN, current.ROM))
    arguments, complete = first_inputs(ja, en, source)
    assert {row for row in source if row[1] in complete} == {row for row in target if row[1] in complete}
    pending = set(base.load(producer.inventory.LEGACY)['pending_ids'])
    assert all(pending.isdisjoint(row['supported_ids']) for row in arguments)
    base.save(OUTPUT, dict(clean_sha256=release['clean_input_sha256'], candidate_sha256=release['candidate_sha256'],
        reference_counts=[dict(entry=entry, clean=dict(Counter(k for _, e, k, _ in source if e == entry)),
            current=dict(Counter(k for _, e, k, _ in target if e == entry))) for entry in sorted(ENTRIES)],
        all_shared_reference_candidates=sorted(source & target), clean_only_reference_candidates=sorted(source - target),
        current_only_reference_candidates=sorted(target - source), exact_argument_sources=arguments,
        complete_direct_reference_entries=complete, entries_with_other_upstream_sites=sorted(ENTRIES - set(complete)),
        remaining_shared_keys=len(pending), new_dialogue_credit=0, new_gameplay_runs=0,
        evidence={str(p): base.digest(p) for p in (current.RELEASE, previous.OUTPUT, wrappers.OUTPUT, Path(__file__))},
        scope='Aligned ARM branches, Thumb BLX immediate and exact pointer words. Computed targets and reachability require separate evidence.'))
    print(f'Bound {len(arguments)} incoming calls across {len(complete)} forwarding entries.')


if __name__ == '__main__':
    main()
