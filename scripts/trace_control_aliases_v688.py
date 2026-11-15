"""Find bounded constant-computed control owners beyond literal owner loads.

This is lead generation, not proof of reachability or global non-use. No value
crosses a branch, call, unknown instruction, conditional write or memory store.
"""

import struct
from pathlib import Path

from capstone import CS_ARCH_ARM, CS_MODE_ARM, Cs
from capstone.arm import ARM_OP_IMM, ARM_OP_MEM, ARM_OP_REG
from ndspy.code import MainCodeFile, loadOverlayTable

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.main_pool_cache_visibility import POOL, STAGE, cache_plan
from dk4tool.rom.nds import NdsImage
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/control_aliases_v688')
TARGETS = {'Confirm': (0x023139C0, 20), 'Frame': (0x02313F60, 20)}


def sections(rom):
    arm = rom.read_file('/__arm9__.bin')
    main = MainCodeFile(arm, 0x02000000).sections
    result = [(f'main{i}', s.ramAddress, bytes(s.data)) for i, s in enumerate(main)]
    if len(main) > 3 and main[3].ramAddress == STAGE:
        plan = cache_plan(arm)
        if plan:
            result.append(('verified_startup_copy_live_POOL', POOL, bytes(main[3].data[:plan['payload_bytes']])))
    result += [(f'overlay{i}', o.ramAddress, bytes(o.data)) for i, o in loadOverlayTable(
        rom.rom.arm9OverlayTable, lambda _id, file_id: rom.rom.files[file_id]).items()]
    return result


def analyze(parts):
    decoder = Cs(CS_ARCH_ARM, CS_MODE_ARM)
    decoder.detail = True
    memory = [(base, base + len(data), data) for _, base, data in parts]

    def word_at(address):
        for start, end, data in memory:
            if start <= address and address + 4 <= end:
                return struct.unpack_from('<I', data, address - start)[0]
        return None

    findings, statistics = [], []
    for label, base, data in parts:
        known, chain = {}, []
        decoded = 0
        for offset in range(0, len(data) - 3, 4):
            address = base + offset
            ins = next(decoder.disasm(data[offset:offset + 4], address, count=1), None)
            if ins is None:
                known, chain = {}, []
                continue
            decoded += 1
            encoded = struct.unpack_from('<I', data, offset)[0]
            if encoded >> 28 != 14:
                # A conditional write can select either value. Keep no invented
                # condition/flag state or cross-conditional memory assumptions.
                known, chain = {}, []
                continue
            operands = ins.operands
            chain.append({'PC': address, 'bytes': bytes(ins.bytes).hex(),
                          'instruction': ins.mnemonic + ' ' + ins.op_str})
            if len(chain) > 96:
                known, chain = {}, chain[-1:]

            def value(operand, ins=ins, address=address, known=known):
                if operand.type == ARM_OP_IMM:
                    return operand.imm & 0xFFFFFFFF
                if operand.type != ARM_OP_REG or operand.shift.type:
                    return None
                name = ins.reg_name(operand.reg)
                return address + 8 if name == 'pc' else known.get(name)

            result, dest, source_address = None, None, None
            if ins.mnemonic in ('mov', 'mvn', 'add', 'sub', 'orr', 'eor', 'and', 'bic'):
                if operands and operands[0].type == ARM_OP_REG:
                    dest = ins.reg_name(operands[0].reg)
                    args = [value(op) for op in operands[1:]]
                    if args and all(a is not None for a in args):
                        if len(args) == 1 and ins.mnemonic in ('mov', 'mvn'):
                            result = args[0] if ins.mnemonic == 'mov' else ~args[0]
                        elif len(args) == 2:
                            a, b = args
                            result = {'add': a + b, 'sub': a - b, 'orr': a | b,
                                      'eor': a ^ b, 'and': a & b, 'bic': a & ~b}.get(ins.mnemonic)
            elif ins.mnemonic == 'ldr' and len(operands) == 2 and operands[1].type == ARM_OP_MEM:
                dest = ins.reg_name(operands[0].reg)
                mem = operands[1].mem
                reg = ins.reg_name(mem.base)
                start = address + 8 if reg == 'pc' else known.get(reg)
                if start is not None and not mem.index and not ins.writeback:
                    source_address = (start + mem.disp) & 0xFFFFFFFF
                    result = word_at(source_address)
            elif ins.mnemonic in ('cmp', 'cmn', 'tst', 'teq', 'nop'):
                continue
            else:
                # Calls, branches, stores and unmodelled instructions terminate
                # the known chain, rather than granting a callee/alias ABI.
                known, chain = {}, []
                continue
            if result is not None:
                result &= 0xFFFFFFFF
            if dest is not None:
                known[dest] = result
            if dest == 'pc':
                known, chain = {}, []
                continue
            if result is None:
                continue
            for name, (owner, size) in TARGETS.items():
                if owner <= result < owner + size:
                    findings.append({'section': label, 'target': name, 'PC': address,
                        'register': dest, 'value': result, 'owner_field_offset': result - owner,
                        'direct_literal_owner_load': ins.mnemonic == 'ldr' and source_address is not None
                            and ins.reg_name(operands[1].mem.base) == 'pc',
                        'source_word_address': source_address, 'bounded_instruction_chain': list(chain),
                        'candidate_only_executed_code_and_real_parent_not_established': True})
        statistics.append({'section': label, 'base': base, 'bytes': len(data),
                           'aligned_words': len(data) // 4, 'decoded_ARM_candidates': decoded,
                           'sha256': sha(data)})
    return findings, statistics


def controls():
    base = 0x02000000
    # LDR r4, [pc,#8]; ADD r0,r4,#0x20; LDR r1,[r0]; BX lr; literal.
    alias = struct.pack('<5I', 0xE59F4008, 0xE2840020, 0xE5901000, 0xE12FFF1E, 0x023139A0)
    rows, _ = analyze([('supplied_alias_control', base, alias)])
    assert len(rows) == 1 and rows[0]['PC'] == base + 4 and rows[0]['value'] == TARGETS['Confirm'][0]
    assert not rows[0]['direct_literal_owner_load']
    # A conditional write, call or store cannot carry that previous value on.
    negatives = []
    for name, boundary in [('conditional', 0x12844000), ('call', 0xEB000000), ('store', 0xE5801000)]:
        data = struct.pack('<5I', 0xE59F4008, boundary, 0xE2840020, 0xE12FFF1E, 0x023139A0)
        found, _ = analyze([(name, base, data)])
        assert not found
        negatives.append(name)
    # A real read-only pointer table, reached through a literal, is resolved.
    data = struct.pack('<6I', 0xE59F4008, 0xE5940000, 0xE12FFF1E, 0, base + 20, 0x023139C0)
    rows, _ = analyze([('supplied_table_control', base, data)])
    assert len(rows) == 1 and rows[0]['PC'] == base + 4 and not rows[0]['direct_literal_owner_load']
    return {'computed_alias_and_read_only_pointer_table_controls_pass': True,
            'conditional_call_store_boundaries_clear_unknowns': negatives}


def main():
    pre = read(ROOT / 'preflight.json')
    for path, digest in pre['release_hashes'].items():
        assert sha(Path(path).read_bytes()) == digest
    checked = controls()
    versions = {}
    for name, path in [('source', Path('work/clean.nds')),
                       ('current', Path('out/all_routes_combined_v685_candidate.nds'))]:
        rom = NdsImage.open(path)
        found, statistics = analyze(sections(rom))
        versions[name] = {'ROM': str(path), 'ROM_sha256': sha(path.read_bytes()),
                          'sections': statistics, 'owner_candidates': found}
    save(ROOT / 'constant_flow_leads.json', {
        'versions': versions, 'controls': checked,
        'no_value_crosses_branch_call_unknown_instruction_conditional_or_store': True,
        'aligned_ARM_basic_blocks_only_no_Thumb_or_arbitrary_dynamic_pointer_claim': True,
        'all_candidates_need_source_execution_or_real_parent_evidence': True,
        'analyzer_sha256': sha(Path(__file__).read_bytes()), 'full_goal_complete': False})
    for name, v in versions.items():
        by = {n: [r for r in v['owner_candidates'] if r['target'] == n] for n in TARGETS}
        print(name, {n: {'all': len(rows), 'computed': sum(not r['direct_literal_owner_load'] for r in rows)}
                     for n, rows in by.items()}, flush=True)


if __name__ == '__main__':
    main()
