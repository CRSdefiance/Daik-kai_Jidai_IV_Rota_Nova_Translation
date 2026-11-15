"""Bounded ARM control-flow address candidates; no global non-use inference."""

import struct
from collections import deque
from pathlib import Path

from capstone import CS_ARCH_ARM, CS_MODE_ARM, Cs
from capstone.arm import ARM_OP_IMM, ARM_OP_MEM, ARM_OP_REG
from keystone import KS_ARCH_ARM, KS_MODE_ARM, Ks
from ndspy.code import MainCodeFile, loadOverlayTable

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.main_pool_cache_visibility import POOL, cache_plan
from dk4tool.rom.nds import NdsImage
from scripts.verify_village_wrap_v608 import save

ROOT = Path('work/analysis/owner_flow_v619')
ROM = Path('out/all_routes_combined_v617_candidate.nds')
TARGETS = {'frame': (0x02313F60, 0x02313F74), 'Confirm': (0x023139C0, 0x023139D4)}
NAMES = ('r0', 'r1', 'r2', 'r3', 'r4', 'r5', 'r6', 'r7', 'r8', 'sb', 'sl', 'fp', 'ip', 'sp', 'lr')
CAP = 4


def finite(values):
    if values is None:
        return None
    result = frozenset(v & 0xFFFFFFFF for v in values)
    return result if 0 < len(result) <= CAP else None


def combine(a, b, operation):
    if a is None or b is None:
        return None
    return finite(operation(x, y) for x in a for y in b)


def join(a, b):
    return tuple(None if x is None or y is None else finite(x | y) for x, y in zip(a, b, strict=True))


def scan(units):
    decoder = Cs(CS_ARCH_ARM, CS_MODE_ARM)
    decoder.detail, decoder.skipdata = True, True
    instructions, labels, chunks, seeds = {}, {}, [], set()
    for label, base, data in units:
        chunks.append((base, base + len(data), data))
        seeds.add(base)
        for ins in decoder.disasm(data, base):
            if ins.size != 4 or not ins.id or ins.address % 4:
                continue
            instructions[ins.address] = ins
            labels[ins.address] = label
            word = int.from_bytes(ins.bytes, 'little')
            if word & 0xFFFF4000 == 0xE92D4000:
                seeds.add(ins.address)
            if word & 0x0F000000 == 0x0B000000:
                delta = word & 0xFFFFFF
                delta -= 0x1000000 if delta & 0x800000 else 0
                seeds.add(ins.address + 8 + delta * 4)

    def load(address):
        for lo, hi, data in chunks:
            if lo <= address <= hi - 4:
                return struct.unpack_from('<I', data, address - lo)[0]
        return None

    seeds.intersection_update(instructions)
    unknown = (None,) * len(NAMES)
    states = {pc: unknown for pc in seeds}
    queue, queued = deque(sorted(seeds)), set(seeds)
    visits, transfers, indexed_reads, nonliteral_reads = 0, set(), set(), set()
    candidates = {}

    def note(pc, kind, values):
        if values is None:
            return
        for target, (lo, hi) in TARGETS.items():
            hits = sorted(v for v in values if lo <= v < hi)
            if hits:
                ins = instructions[pc]
                key = (pc, target, kind)
                row = {'unit': labels[pc], 'instruction': pc, 'assembly': ins.mnemonic + ' ' + ins.op_str,
                       'target': target, 'kind': kind, 'addresses': hits,
                       'all_possible_values_in_target': all(lo <= v < hi for v in values),
                       'possible_values': sorted(values)}
                candidates[key] = row

    final_pass = False
    while queue or not final_pass:
        if not queue:
            final_pass = True
            candidates.clear()
            queue.extend(sorted(states))
            queued.update(states)
        pc = queue.popleft()
        queued.discard(pc)
        visits += 1
        assert visits < 8000000, 'Bounded flow did not converge'
        ins, state = instructions[pc], states[pc]
        word = int.from_bytes(ins.bytes, 'little')
        condition, ops = word >> 28, ins.operands
        current = dict(zip(NAMES, state, strict=True))
        current['pc'] = frozenset((pc + 8,))

        def operand(op, current=current, ins=ins):
            if op.type == ARM_OP_IMM:
                return finite((op.imm,))
            if op.type != ARM_OP_REG:
                return None
            values = current.get(ins.reg_name(op.reg))
            if not op.shift.type:
                return values
            shift = op.shift.value
            if values is None or op.shift.type not in (1, 2, 3, 4):
                return None
            if op.shift.type == 1:
                return finite(((v - 0x100000000 if v & 0x80000000 else v) >> min(shift, 32)) for v in values)
            if op.shift.type == 2:
                return finite(v << min(shift, 32) for v in values)
            if op.shift.type == 3:
                return finite(v >> min(shift, 32) for v in values)
            shift %= 32
            return finite((v >> shift) | (v << ((32 - shift) % 32)) for v in values)

        before, after = list(state), list(state)
        written = {ins.reg_name(reg) for reg in ins.regs_access()[1]}
        for reg in ins.regs_access()[1]:
            name = ins.reg_name(reg)
            if name in NAMES:
                after[NAMES.index(name)] = None
        destination, result = None, None
        if ops and ops[0].type == ARM_OP_REG and ins.reg_name(ops[0].reg) in written:
            destination = ins.reg_name(ops[0].reg)
        mnemonic = ins.mnemonic
        # Condition suffixes are removed only for modeled integer/load families.
        base_op = mnemonic
        for stem in ('mov', 'mvn', 'add', 'sub', 'rsb', 'orr', 'and', 'eor', 'bic', 'lsl', 'lsr', 'mul', 'ldr', 'str'):
            if mnemonic.startswith(stem) and mnemonic[len(stem):] in ('', 's', 'eq', 'ne', 'lt', 'le', 'gt', 'ge', 'lo', 'ls', 'hi', 'hs'):
                base_op = stem
                break
        if base_op in ('mov', 'mvn') and len(ops) == 2:
            value = operand(ops[1])
            result = value if base_op == 'mov' or value is None else finite(~v for v in value)
        elif base_op in ('add', 'sub', 'rsb', 'orr', 'and', 'eor', 'bic', 'lsl', 'lsr', 'mul') and len(ops) == 3:
            funcs = {'add': lambda a, b: a + b, 'sub': lambda a, b: a - b, 'rsb': lambda a, b: b - a,
                     'orr': lambda a, b: a | b, 'and': lambda a, b: a & b, 'eor': lambda a, b: a ^ b,
                     'bic': lambda a, b: a & ~b, 'lsl': lambda a, b: a << min(b, 32),
                     'lsr': lambda a, b: a >> min(b, 32), 'mul': lambda a, b: a * b}
            result = combine(operand(ops[1]), operand(ops[2]), funcs[base_op])
        for op in ops:
            if op.type != ARM_OP_MEM:
                continue
            base = current.get(ins.reg_name(op.mem.base))
            if op.mem.index:
                index = current.get(ins.reg_name(op.mem.index))
                if op.shift.type not in (0, 2):
                    index = None
                if index is not None:
                    index = finite(v << op.shift.value for v in index)
                addresses = combine(base, index, lambda a, b, scale=op.mem.scale, disp=op.mem.disp: a + b * scale + disp)
                indexed_reads.add(pc)
            else:
                addresses = None if base is None else finite(v + op.mem.disp for v in base)
            if ins.reg_name(op.mem.base) != 'pc':
                note(pc, 'resolved_memory_address', addresses)
            if base_op == 'ldr' and not ins.writeback and addresses is not None:
                values = [load(address) for address in addresses]
                result = None if any(v is None for v in values) else finite(values)
                if ins.reg_name(op.mem.base) != 'pc' and result is not None:
                    nonliteral_reads.add(pc)
                    note(pc, 'source_table_load_candidate', result)
        if destination in NAMES:
            after[NAMES.index(destination)] = result
            if base_op != 'ldr':
                note(pc, 'arithmetic_or_register_copy', result)
        is_call = (word & 0x0F000000 == 0x0B000000 or word & 0x0FFFFFF0 == 0x012FFF30
                   or word & 0xFE000000 == 0xFA000000)
        is_branch = word & 0x0E000000 == 0x0A000000 and not is_call
        if is_call:
            for name in ('r0', 'r1', 'r2', 'r3', 'ip', 'lr'):
                after[NAMES.index(name)] = None
            # r4-r11 and SP retain their input constants under the original ARM ABI.
        if condition not in (14, 15) and not is_branch:
            after = list(join(tuple(before), tuple(after)))
        successors = []
        if is_call:
            successors.append(pc + 4)
        elif is_branch:
            delta = word & 0xFFFFFF
            delta -= 0x1000000 if delta & 0x800000 else 0
            successors.append(pc + 8 + delta * 4)
            if condition != 14:
                successors.append(pc + 4)
        elif word & 0x0FFFFFF0 == 0x012FFF10 or 'pc' in [ins.reg_name(r) for r in ins.regs_access()[1]]:
            transfers.add(pc)
            if condition != 14:
                successors.append(pc + 4)
        else:
            successors.append(pc + 4)
        for target in successors:
            if target not in instructions:
                continue
            old = states.get(target)
            revised = tuple(after) if old is None else join(old, tuple(after))
            if revised != old:
                assert not final_pass, 'Final-state pass found unconverged input facts'
                states[target] = revised
                if target not in queued:
                    queue.append(target)
                    queued.add(target)
    return {'decoded_instructions': len(instructions), 'seeded_entries': len(seeds), 'visited_instructions': len(states),
            'worklist_evaluations': visits, 'terminal_or_unresolved_PC_transfer_sites_including_returns': len(transfers),
            'indexed_memory_sites_visited': len(indexed_reads), 'source_table_reads_resolved': len(nonliteral_reads),
            'candidates': sorted(candidates.values(), key=lambda r: (r['instruction'], r['kind'], r['target'])),
            'candidate_rows_recomputed_only_after_fixed_point_converged': True,
            'candidate_rows_still_require_native_followup_and_reachability': True}


def controls():
    assembler = Ks(KS_ARCH_ARM, KS_MODE_ARM)
    base = 0x02000000
    snippets = {
        'cross_branch_and_preserved_register_call': '''
            ldr r4, source
            cmp r0, #0
            beq one
            add r4, r4, #16
            b two
        one: add r4, r4, #16
        two: bl 0x02100000
            mov r0, r4
            bx lr
        source: .word 0x023139B0
        ''',
        'indexed_table': '''
            adr r4, table
            mov r5, #1
            ldr r0, [r4, r5, lsl #2]
            add r0, r0, #4
            bx lr
        table: .word 0,0x023139C0
        ''',
        'interworking_call_preserves_saved_register': '''
            ldr r4, source
            blx 0x02100000
            mov r0, r4
            bx lr
        source: .word 0x023139C0
        ''',
        'clobbered_argument_negative': '''
            ldr r0, source
            bl 0x02100000
            add r0, r0, #4
            bx lr
        source: .word 0x023139C0
        ''',
        'unknown_index_negative': '''
            adr r4, table
            ldr r0, [r4, r5, lsl #2]
            add r0, r0, #4
            bx lr
        table: .word 0,0x023139C0
        ''',
        'unknown_branch_join_negative': '''
            ldr r4, source
            cmp r0, #0
            beq final
            mov r4, r1
        final: mov r0, r4
            bx lr
        source: .word 0x023139C0
        ''',
    }
    rows = []
    for name, assembly in snippets.items():
        data = bytes(assembler.asm(assembly, base)[0])
        result = scan([(name, base, data)])
        hits = [r for r in result['candidates'] if r['target'] == 'Confirm']
        assert bool(hits) == ('negative' not in name), (name, hits)
        if name == 'cross_branch_and_preserved_register_call':
            assert any(r['instruction'] == base + 0x1C and r['addresses'] == [0x023139C0] for r in hits)
        elif name == 'indexed_table':
            assert any(r['instruction'] == base + 8 and r['kind'] == 'source_table_load_candidate' for r in hits)
        elif name == 'interworking_call_preserves_saved_register':
            assert any(r['instruction'] == base + 8 and r['addresses'] == [0x023139C0] for r in hits)
        rows.append({'name': name, 'input_sha256': sha(data), 'bytes_hex': data.hex(),
                     'expected_candidate_behavior_verified': True, 'hits': hits})
    return rows


def main():
    ROOT.mkdir(parents=True, exist_ok=True)
    checks = controls()
    rom = NdsImage.open(ROM)
    digest = sha(ROM.read_bytes())
    assert digest == '0575673e6a742055d3c6960dbe39ea2479d4c7b9ffc3f9c4b75a3fd2b5e005bc'
    arm = rom.read_file('/__arm9__.bin')
    sections = MainCodeFile(arm, 0x02000000).sections
    units = [(f'main{i}', s.ramAddress, bytes(s.data)) for i, s in enumerate(sections)]
    plan = cache_plan(arm)
    assert plan and len(sections[3].data) == plan['payload_bytes'] + 48
    units.append(('runtime_pool_copy', POOL, bytes(sections[3].data[:plan['payload_bytes']])))
    units += [(f'overlay{i}', s.ramAddress, bytes(s.data)) for i, s in loadOverlayTable(
        rom.rom.arm9OverlayTable, lambda _, fid: rom.rom.files[fid]).items()]
    result = scan(units)
    save(ROOT / 'flow_candidates.json', {'candidate': str(ROM), 'candidate_sha256': digest,
         'source_units': [{'name': n, 'base': b, 'bytes': len(d), 'sha256': sha(d)} for n, b, d in units],
         'synthetic_analysis_controls': checks, 'flow': result, 'max_constant_set': CAP,
         'limitations': ['ARM-aligned candidate entries include possible data; no ordinary reachability claim.',
                         'Opaque calls use ARM callee-saved register assumptions; arguments/results are not propagated through callees.',
                         'Stack memory, mutable runtime reads, Thumb and unresolved indirect/switch destinations remain unknown.',
                         'Nonliteral source-file-backed reads are initial-storage candidates,not proven immutable runtime tables.',
                         'Candidate rows are recomputed from final states but still need native follow-up; absence is not global non-use.'],
         'production_ROM_and_patch_unchanged': True, 'all18_plaques_incomplete': True,
         'full_goal_complete': False, 'script_sha256': sha(Path(__file__).read_bytes())})
    print({k: v for k, v in result.items() if k != 'candidates'})
    print('Owner candidate rows:', len(result['candidates']))


if __name__ == '__main__':
    main()
