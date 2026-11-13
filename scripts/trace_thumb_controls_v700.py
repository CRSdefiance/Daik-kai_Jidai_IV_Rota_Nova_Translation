"""Inspect previously excluded Thumb literal/constant paths to control owners.

All halfwords are candidates, including data. This is bounded lead generation,
not proof of executable Thumb code, ordinary UI reachability or global non-use.
"""

import struct
from pathlib import Path

from capstone import CS_ARCH_ARM, CS_MODE_THUMB, Cs
from capstone.arm import ARM_OP_IMM, ARM_OP_MEM, ARM_OP_REG
from unicorn import arm_const

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.probe_button_prompt_native import machine
from scripts.run_room_gender_v694 import ROM
from scripts.trace_control_aliases_v688 import TARGETS, sections
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/thumb_controls_v700')
ALIASES = {'sb': 'r9', 'sl': 'r10', 'fp': 'r11', 'ip': 'r12'}


def analyze(parts):
    decoder = Cs(CS_ARCH_ARM, CS_MODE_THUMB)
    decoder.detail = True
    memory = [(base, base + len(blob), blob) for _, base, blob in parts]

    def word(address):
        for lo, hi, blob in memory:
            if lo <= address and address + 4 <= hi:
                return struct.unpack_from('<I', blob, address - lo)[0]
        return None

    findings, statistics = [], []
    for label, base, blob in parts:
        seeds = 0
        for offset in range(0, len(blob) - 1, 2):
            half = struct.unpack_from('<H', blob, offset)[0]
            if half & 0xF800 != 0x4800:
                continue
            seeds += 1
            pc = base + offset
            literal = ((pc + 4) & ~3) + (half & 255) * 4
            loaded = word(literal)
            if loaded is None:
                continue
            register = 'r' + str(half >> 8 & 7)
            known, chain = {register: loaded}, []
            for step in range(24):
                here = offset + step * 2
                if here + 2 > len(blob):
                    break
                ins = next(decoder.disasm(blob[here:here + 4], base + here, count=1), None)
                # ARM9's Thumb BL/BLX pairs terminate this local chain. Thumb2
                # instructions are not a supported ARM946 execution mode.
                if ins is None or ins.size != 2:
                    break
                chain.append({'PC': ins.address, 'bytes': bytes(ins.bytes).hex(),
                              'instruction': ins.mnemonic + ' ' + ins.op_str})
                op, args = ins.mnemonic, ins.operands

                def register_name(reg, ins=ins):
                    name = ins.reg_name(reg)
                    return ALIASES.get(name, name)

                def value(operand, ins=ins, known=known):
                    if operand.type == ARM_OP_IMM:
                        return operand.imm & 0xFFFFFFFF
                    if operand.type == ARM_OP_REG and not operand.shift.type:
                        name = register_name(operand.reg)
                        return ((ins.address + 4) & ~3) if name == 'pc' else known.get(name)
                    return None

                dest, result = None, None
                if op == 'ldr' and len(args) == 2 and args[1].type == ARM_OP_MEM:
                    dest = register_name(args[0].reg)
                    m = args[1].mem
                    start = ((ins.address + 4) & ~3) if register_name(m.base) == 'pc' else known.get(register_name(m.base))
                    if start is not None and not m.index and not ins.writeback:
                        result = word((start + m.disp) & 0xFFFFFFFF)
                elif op in ('mov', 'movs', 'adds', 'add', 'subs', 'sub', 'lsls', 'lsrs', 'orrs', 'ands', 'eors', 'bics'):
                    if not args or args[0].type != ARM_OP_REG:
                        break
                    dest = register_name(args[0].reg)
                    values = [value(a) for a in args[1:]]
                    if len(values) == 1 and op not in ('mov', 'movs'):
                        values.insert(0, known.get(dest))
                    if values and all(v is not None for v in values):
                        if op in ('mov', 'movs') and len(values) == 1:
                            result = values[0]
                        elif len(values) == 2:
                            a, b = values
                            result = {'adds': a + b, 'add': a + b, 'subs': a - b, 'sub': a - b,
                                'lsls': a << min(b, 32), 'lsrs': a >> min(b, 32), 'orrs': a | b,
                                'ands': a & b, 'eors': a ^ b, 'bics': a & ~b}.get(op)
                elif op in ('cmp', 'cmn', 'tst', 'nop'):
                    continue
                else:
                    # No values cross calls, branches, stores, unknown loads,
                    # stack operations, other instructions or unknown flags.
                    break
                if dest == 'pc':
                    break
                if result is not None:
                    result &= 0xFFFFFFFF
                if dest:
                    known[dest] = result
                if result is None:
                    continue
                for target, (owner, size) in TARGETS.items():
                    if owner <= result < owner + size:
                        findings.append({'section': label, 'target': target, 'PC': ins.address,
                            'register': dest, 'value': result, 'owner_field_offset': result - owner,
                            'seed_PC': pc, 'seed_literal_address': literal, 'seed_literal_value': loaded,
                            'bounded_chain': list(chain), 'candidate_only_executable_context_not_established': True})
        statistics.append({'section': label, 'base': base, 'bytes': len(blob),
            'all_aligned_halfword_positions': len(blob) // 2, 'Thumb_literal_seed_candidates': seeds,
            'sha256': sha(blob)})
    return findings, statistics


def controls():
    base = 0x02000000
    # LDR r4,[pc,#8]; MOV r0,r4; ADDS r0,#32; BX lr; padding; literal.
    alias = struct.pack('<6HI', 0x4C02, 0x4620, 0x3020, 0x4770, 0, 0, 0x023139A0)
    rows, _ = analyze([('supplied_Thumb_alias', base, alias)])
    assert len(rows) == 1 and rows[0]['PC'] == base + 4 and rows[0]['value'] == TARGETS['Confirm'][0]
    # LDR r4,[pc,#8]; LDR r0,[r4]; BX lr; padding; literal table pointer/owner.
    table = struct.pack('<6H2I', 0x4C02, 0x6820, 0x4770, 0, 0, 0, base + 16, 0x023139C0)
    found, _ = analyze([('supplied_Thumb_table', base, table)])
    assert any(r['PC'] == base + 2 and r['value'] == TARGETS['Confirm'][0] for r in found)
    phased = struct.pack('<6HI', 0x46C0, 0x4C02, 0x4620, 0x3020, 0x4770, 0, 0x023139A0)
    found, _ = analyze([('halfword_phase_2', base, phased)])
    assert len(found) == 1 and found[0]['PC'] == base + 6 and found[0]['seed_literal_address'] == base + 12
    boundaries = []
    for target, (owner, size) in TARGETS.items():
        for offset in (0, size - 4, size):
            data = struct.pack('<6HI', 0x4C02, 0x4770, 0, 0, 0, 0, owner + offset)
            hits, _ = analyze([('exact_owner_boundary', base, data)])
            assert bool(hits) == (offset < size)
            boundaries.append({'target': target, 'offset': offset, 'included': bool(hits)})
    negatives = []
    for name, boundary in (('conditional_branch', 0xD100), ('store', 0x6020), ('return', 0x4770)):
        data = struct.pack('<6HI', 0x4C02, boundary, 0x3020, 0x4770, 0, 0, 0x023139A0)
        assert not analyze([(name, base, data)])[0]
        negatives.append(name)
    native = []
    arm = NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    regs = [getattr(arm_const, 'UC_ARM_REG_R' + str(i)) for i in range(13)]
    regs += [arm_const.UC_ARM_REG_SP, arm_const.UC_ARM_REG_LR]
    for name, data, start, instructions, expected_registers in (
        ('computed_alias', alias, base, 3, {0: 0x023139C0, 4: 0x023139A0}),
        ('halfword_phase_2', phased, base + 2, 3, {0: 0x023139C0, 4: 0x023139A0}),
        ('pointer_table', table, base, 2, {0: 0x023139C0, 4: base + 16})):
        u = machine(arm)
        u.mem_write(base, data)
        before = bytes(u.mem_read(base, 0x400000))
        supplied = [0x03000000 + i * 0x100 for i in range(15)]
        u.reg_write(arm_const.UC_ARM_REG_CPSR, 0x3F)
        for r, value in zip(regs, supplied, strict=True):
            u.reg_write(r, value)
        u.emu_start(start | 1, start + instructions * 2, count=instructions)
        expected = supplied[:]
        for index, value in expected_registers.items():
            expected[index] = value
        assert [u.reg_read(r) for r in regs] == expected
        assert u.reg_read(arm_const.UC_ARM_REG_PC) == start + instructions * 2
        assert u.reg_read(arm_const.UC_ARM_REG_CPSR) == 0x3F
        assert bytes(u.mem_read(base, 0x400000)) == before
        native.append({'case': name, 'all15_registers_CPSR_PC_and_full4MiB_RAM_exact': True})
    return {'positive_literal_alias_and_pointer_table_controls_pass': True,
        'negative_chain_boundaries': negatives, 'exact20_byte_owner_boundary_controls': boundaries,
        'original_ARM946_Thumb_native_controls': native}


def main():
    ROOT.mkdir(exist_ok=True)
    frozen = read('work/analysis/confirm_material_v572/audit_scope_before.json')
    paths = (ROM, ROM.with_suffix('.manifest.json'), ROM.with_suffix('.xdelta'),
        Path('translations/release_stack.json'), Path('work/clean.nds'),
        Path('out/raphael_natural_v2_accepted_base.nds'))
    save(ROOT / 'preflight.json', {'release_hashes': {str(p): sha(p.read_bytes()) for p in paths},
        'candidate': str(ROM), 'candidate_sha256': sha(ROM.read_bytes()),
        'all_original_audits_before': {n: read(Path('translations') / n) for n in frozen},
        'previous_goal_turn_classification': 'progress: V698 symbols/plaques and V699 eight actual card display fixtures',
        'full_goal_complete': False})
    checked = controls()
    versions = {}
    for name, path in (('source', Path('work/clean.nds')), ('current', ROM)):
        parts = sections(NdsImage.open(path))
        findings, statistics = analyze(parts)
        versions[name] = {'ROM': str(path), 'ROM_sha256': sha(path.read_bytes()),
            'owner_candidates': findings, 'sections': statistics}
        print('V700', name, 'Thumb candidates', len(findings), 'literal seeds',
              sum(r['Thumb_literal_seed_candidates'] for r in statistics), flush=True)
    save(ROOT / 'proof.json', {'versions': versions, 'controls': checked,
        'all_halfword_literal_seeds_and24_instruction_constant_chains_checked': True,
        'no_values_cross_calls_branches_stores_stack_unknown_or_unmodelled_instructions': True,
        'new_ordinary_control_parent_or_GPU_display_NOT_proven': True,
        'no_global_unused_art_or_full_dynamic_Thumb_coverage_claim': True,
        'source_analyzer': str(Path(__file__)), 'analyzer_sha256': sha(Path(__file__).read_bytes()),
        'full_goal_complete': False})


if __name__ == '__main__':
    main()
