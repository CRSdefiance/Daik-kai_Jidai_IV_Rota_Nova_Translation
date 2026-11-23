"""Resolve local conditional and stack-held COMMON message arguments."""

from pathlib import Path
from struct import iter_unpack, unpack_from

from capstone import CS_AC_WRITE, CS_ARCH_ARM, CS_MODE_ARM, Cs
from capstone.arm import ARM_INS_LDR, ARM_INS_MOV, ARM_OP_MEM, ARM_REG_SP
from unicorn.arm_const import (
    UC_ARM_REG_CPSR, UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R4, UC_ARM_REG_R5,
    UC_ARM_REG_R6, UC_ARM_REG_R7, UC_ARM_REG_R8, UC_ARM_REG_R9, UC_ARM_REG_SP,
)

from scripts import checkpoint_shared_crew_and_wrapper_routes_20261115 as prior
from scripts import checkpoint_shared_message_producers_20261115 as producer
from scripts import checkpoint_shared_table_callers_20261115 as shared
from scripts import register_market_trade_dialogue_20261115 as current
from scripts.probe_button_prompt_native import BASE, STACK, machine


base = current.base
OUTPUT = producer.inventory.ROOT / 'shared_fixed_arguments_20261115_v1.json'
REGS = {'r4': UC_ARM_REG_R4, 'r5': UC_ARM_REG_R5, 'r6': UC_ARM_REG_R6, 'r7': UC_ARM_REG_R7,
        'r8': UC_ARM_REG_R8, 'sb': UC_ARM_REG_R9}
CONDITIONAL = {
    0x578C4: (0x578A0, 0x578A4, 'r5', (1028, 1029)),
    0x57A14: (0x579E8, 0x579F0, 'r7', (905, 906)),
    0x57C14: (0x57BE0, 0x57BE8, 'r7', (881, 882)),
    0x57C64: (0x57C44, 0x57C4C, 'r4', (1033, 1034)),
    0x57E48: (0x57E14, 0x57E1C, 'r5', (879, 880)),
    0x57E90: (0x57E70, 0x57E78, 'r4', (1031, 1032)),
    0x589D0: (0x5899C, 0x589A4, 'r6', (849, 850)),
    0x58A94: (0x58A78, 0x58A80, 'r5', (847, 848)),
    0x59ADC: (0x59AA4, 0x59AAC, 'r6', (822, 823)),
    0x59CE0: (0x59C84, 0x59C88, 'r8', (820, 821)),
    0x59E70: (0x59E54, 0x59E5C, 'r8', (54, 55)),
    0x5C6F8: (0x5C6C0, 0x5C6C8, 'sb', (1195, 1196)),
    0x5C8A8: (0x5C870, 0x5C878, 'sb', (1197, 1198)),
    0x5CA58: (0x5CA20, 0x5CA28, 'sb', (1195, 1196)),
    0x5DD1C: (0x5DCFC, 0x5DD04, 'r4', (1154, 1151)),
    0x5FBE8: (0x5FBC8, 0x5FBD0, 'r4', (654, 733)),
    0x5FC28: (0x5FC08, 0x5FC10, 'r4', (653, 655)),
}
STACKS = {
    0x31798: (0x31674, 0x31678, 0x18, 532, 0x02053FE4, UC_ARM_REG_R1),
    0x319E0: (0x316CC, 0x316D0, 0x40, 552, 0x02053FE4, UC_ARM_REG_R1),
    0x31A8C: (0x316BC, 0x316C0, 0x58, 572, 0x02053FE4, UC_ARM_REG_R1),
    0x41F6C: (0x41E38, 0x41E74, 0x20, 98, 0x020546B8, UC_ARM_REG_R0),
    0x41FD8: (0x41E30, 0x41E34, 0x28, 99, 0x020546B8, UC_ARM_REG_R0),
    0x5C404: (0x5C204, 0x5C208, 0x1C, 1072, 0x02053FE4, UC_ARM_REG_R1),
    0x5DC40: (0x5DB40, 0x5DB44, 0x8, 1168, 0x02053FE4, UC_ARM_REG_R1),
    0x7E50C: (0x7E480, 0x7E484, 0x14, 336, 0x0205528C, UC_ARM_REG_R0),
}
SENTINEL = 0xFFFFFFFF


def decoder():
    cpu = Cs(CS_ARCH_ARM, CS_MODE_ARM)
    cpu.detail = True
    return cpu


def writes(insn):
    return {insn.reg_name(n) for n in insn.regs_access()[1]}


def branch_targets(raw, focus):
    incoming = []
    for i, (word,) in enumerate(iter_unpack('<I', raw[:len(raw) & ~3])):
        if word >> 28 == 15 or word & 0x0E000000 != 0x0A000000:
            continue
        imm = word & 0xFFFFFF
        signed = imm - 0x1000000 if imm & 0x800000 else imm
        target = i * 4 + 8 + 4 * signed
        if target in focus:
            incoming.append((i * 4, target))
    return incoming


def conditional_tails(ja, en):
    cs = decoder()
    cpus = [machine(raw) for raw in (ja, en)]
    targets = {i for site, (first, _, _, _) in CONDITIONAL.items() for i in range(first + 4, site + 4, 4)}
    incoming = branch_targets(ja, targets)
    assert incoming == branch_targets(en, targets)
    rows = []
    for site, (first, second, carrier, outputs) in CONDITIONAL.items():
        if site == 0x59CE0:
            locks = producer.literal_dependencies(ja, en, first, 0x59CC8)
            locks.extend(producer.literal_dependencies(ja, en, 0x59CCC, site + 4))
            assert producer.inventory.disassemble(ja, 0x59CC8, 1) == ['02059cc8 bl #0x203cf70']
            assert producer.inventory.disassemble(en, 0x59CC8, 1) == ['02059cc8 bl #0x2156058']
            helper = list(cs.disasm(en[0x156058:0x156074], BASE + 0x156058))
            assert [insn.mnemonic for insn in helper] == ['ldrb', 'cmp', 'bhs', 'ldr', 'ldr', 'bx', 'b']
            assert all('r8' not in writes(insn) for insn in helper)
            assert helper[-1].op_str == '#0x203cf70'
            locks.append(dict(registered_child=0x02156058, falls_through_to_source=0x0203CF70,
                              bytes_sha256=shared.sha(en[0x156058:0x156074])))
        else:
            locks = producer.literal_dependencies(ja, en, first, site + 4)
        insns = list(cs.disasm(ja[first:site], BASE + first))
        assert len(insns) == (site - first) // 4
        indices = [insn.address - BASE for insn in insns if carrier in writes(insn)]
        assert indices == [first, second], (hex(site), indices)
        conditions = tuple(insns[(address - first) // 4] for address in indices)
        assert all(insn.id in (ARM_INS_LDR, ARM_INS_MOV) for insn in conditions)
        for insn in insns[1:(second - first) // 4]:
            assert not writes(insn) & {'cpsr', 'apsr', 'pc'} and not insn.mnemonic.startswith('b')
        # The two conditional definitions dominate the use in the local block.
        assert all(not insn.mnemonic.startswith('b') or insn.mnemonic in ('bl', 'blx') for insn in insns)
        edges = [(a, b) for a, b in incoming if first < b <= site]
        assert not edges, (hex(site), [(hex(a), hex(b)) for a,b in edges])
        to_r1 = [insn for insn in insns if 'r1' in writes(insn)][-1]
        assert to_r1.mnemonic == 'mov' and to_r1.op_str == f'r1, {carrier}'
        assert {a for a, _, _ in producer.inventory.branch_hits(ja[site:site + 4], BASE + site, {0x02053FE4})} == {BASE + site}
        variants = []
        for flags in range(16):
            expected_set = set()
            for cpu in cpus:
                values = []
                for at in indices:
                    cpu.reg_write(UC_ARM_REG_CPSR, (cpu.reg_read(UC_ARM_REG_CPSR) & 0x0FFFFFFF) | flags << 28)
                    cpu.reg_write(REGS[carrier], SENTINEL)
                    shared.run_to(cpu, at, at + 4)
                    chosen = cpu.reg_read(REGS[carrier])
                    if chosen != SENTINEL:
                        values.append(chosen)
                value, = values
                assert value in outputs
                expected_set.add(value)
            value, = expected_set
            variants.append(value)
        assert set(variants) == set(outputs)
        rows.append(dict(call_site=BASE + site, supported_ids=sorted(outputs), selector_register=carrier,
            assigned_by=[BASE + i for i in indices], mapping_by_NZCV=variants, clean_and_current_code_locks=locks))
    return rows


def stack_arguments(ja, en):
    cs = decoder()
    rows = []
    cpus = [machine(raw) for raw in (ja, en)]
    for site, (start, store, slot, value, callee, register) in STACKS.items():
        scope = producer.literal_dependencies(ja, en, start, store + 4)
        scope += shared.lock(ja, en, site - 8, site + 4),
        assert producer.inventory.branch_hits(ja[site:site + 4], BASE + site, {callee}) == [(BASE + site, callee, 'arm_bl')]
        local = list(cs.disasm(ja[store:site], BASE + store))
        assert len(local) == (site - store) // 4
        explicit_slot_writes = [insn.address for insn in local for op in insn.operands
                                if op.type == ARM_OP_MEM and op.mem.base == ARM_REG_SP and op.mem.disp == slot
                                and op.access & CS_AC_WRITE]
        assert explicit_slot_writes == [BASE + store], (hex(site), explicit_slot_writes)
        for cpu in cpus:
            cpu.reg_write(UC_ARM_REG_SP, STACK)
            shared.run_to(cpu, start, store + 4)
            assert shared.read_word(cpu, STACK + slot) == value
            read_start = site - (8 if site in (0x5C404, 0x5DC40) else 4)
            shared.run_to(cpu, read_start, site)
            assert cpu.reg_read(register) == value
        rows.append(dict(call_site=BASE + site, supported_ids=[value], target=callee, stack_displacement=slot,
            original_store_address=BASE + store, initialization_and_readback_fixture=True,
            intervening_local_code_sha256=shared.lock(ja, en, store, site)['clean_and_current_sha256'],
            code_locks=scope))
    return rows


def main():
    assert not OUTPUT.exists()
    release, before = map(base.load, (current.RELEASE, prior.OUTPUT))
    assert base.digest(base.REGISTRY) == release['registry_sha256']
    assert base.digest(current.ROM) == before['candidate_sha256'] == release['candidate_sha256']
    assert base.digest(current.stage.CLEAN) == before['clean_sha256'] == release['clean_input_sha256']
    ja, en = (base.NdsImage.open(p).read_file(current.stage.ARM) for p in (current.stage.CLEAN, current.ROM))
    conditional, stacks = conditional_tails(ja, en), stack_arguments(ja, en)
    sources = {row['call_site'] for row in conditional + stacks}
    pending = set(base.load(producer.inventory.LEGACY)['pending_ids'])
    open_sites = set(before['other_open_sites_except_forwarding'])
    assert sources <= open_sites and len(sources) == len(conditional) + len(stacks)
    assert all(pending.isdisjoint(row['supported_ids']) for row in conditional + stacks)
    base.save(OUTPUT, dict(candidate_sha256=release['candidate_sha256'], clean_sha256=release['clean_input_sha256'],
        conditional_argument_sites=conditional, stack_argument_sites=stacks, resolved_sites=sorted(sources),
        open_message_sources=sorted(open_sites - sources), forwarding_sites_open_upstream=len(before['forwarding_sites']),
        remaining_shared_keys=len(pending), new_dialogue_credit=0, new_gameplay_runs=0, full_goal_complete=False,
        evidence={str(p): base.digest(p) for p in (producer.inventory.LEGACY, prior.OUTPUT, current.RELEASE, Path(__file__))}))
    print(f'Bound {len(sources)} local COMMON arguments. {len(open_sites - sources)} possible message producers remain in this inventory.')


if __name__ == '__main__':
    main()
