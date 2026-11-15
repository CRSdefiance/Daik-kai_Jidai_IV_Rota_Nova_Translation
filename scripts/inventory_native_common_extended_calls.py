"""Extend native COMMON reference candidates to ARM tails/registers and Thumb."""

import json
import struct
from pathlib import Path

from capstone import CS_ARCH_ARM, CS_MODE_ARM, CS_MODE_THUMB, Cs
from capstone.arm import ARM_INS_B, ARM_INS_BL, ARM_INS_BLX, ARM_INS_BX, ARM_OP_IMM, ARM_OP_REG
from ndspy.code import MainCodeFile, loadOverlayTable

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from scripts.inventory_native_common_calls import TARGETS, WRAPPER_LOCKS, locally_resolved_argument

TABLE_TARGETS = {0x02053EC0: 'r1', 0x02053F0C: 'r1'}
ALL_TARGETS = {**TARGETS, **TABLE_TARGETS, 0x020BF328: 'r1'}
ID_ADJUSTMENTS = {0x020BF328: 137}


def joined_context_argument(context, raw, base, register):
    """Discard pre-join values instead of selecting the final linear case.

    This only detects incoming branches visible within the context window.
    External predecessors and function boundaries still need separate proof.
    """
    joins = {ins.operands[0].imm for ins in context
             if ins.id == ARM_INS_B and len(ins.operands) == 1
             and ins.operands[0].type == ARM_OP_IMM}
    start = 0
    for index, ins in enumerate(context):
        if ins.address in joins:
            start = index
    return locally_resolved_argument(context[start:], raw, base, register)


def branch(ins, context, raw, base):
    if ins.id not in (ARM_INS_B, ARM_INS_BL, ARM_INS_BLX, ARM_INS_BX) or len(ins.operands) != 1:
        return None
    operand = ins.operands[0]
    if operand.type == ARM_OP_IMM:
        target = operand.imm & 0xFFFFFFFF
        kind = 'direct-tail-branch' if ins.id == ARM_INS_B else 'direct-call'
    elif operand.type == ARM_OP_REG:
        register = ins.reg_name(operand.reg)
        target = joined_context_argument(context, raw, base, register)
        if target is None:
            return None
        kind = 'locally-resolved-register-call' if ins.id == ARM_INS_BLX else 'locally-resolved-register-tail'
    else:
        return None
    if target & ~1 not in ALL_TARGETS:
        return None
    return {'target': target & ~1, 'kind': kind, 'mode_bit': target & 1}


def arm_candidates(raw, base):
    cs = Cs(CS_ARCH_ARM, CS_MODE_ARM)
    cs.detail = True
    cs.skipdata = True
    rows = []
    for offset in range(0, len(raw) - 3, 4):
        word = struct.unpack_from('<I', raw, offset)[0]
        if not (word & 0x0E000000 == 0x0A000000 or word & 0x0FFFFFF0 in (0x012FFF10, 0x012FFF30)):
            continue
        decoded = list(cs.disasm(raw[offset:offset + 4], base + offset))
        if len(decoded) != 1 or decoded[0].id == 0:
            continue
        context = list(cs.disasm(raw[max(0, offset - 64):offset], base + max(0, offset - 64)))
        if any(ins.id == 0 for ins in context):
            context = []
        found = branch(decoded[0], context, raw, base)
        if found is None:
            continue
        value = joined_context_argument(context, raw, base, ALL_TARGETS[found['target']])
        table_address = value if found['target'] in TABLE_TARGETS else None
        if value is not None and found['target'] not in TABLE_TARGETS:
            value = (value + ID_ADJUSTMENTS.get(found['target'], 0)) & 0xFFFFFFFF
        if found['target'] in TABLE_TARGETS:
            value = None
        rows.append({'offset': offset, 'runtime_address': base + offset, 'instruction': decoded[0].mnemonic + ' ' + decoded[0].op_str,
                     **found, 'native_id_constant': value,
                     'native_table_address_constant': table_address,
                     'context': [f'{ins.address:08X} {ins.mnemonic} {ins.op_str}' for ins in context]})
    return rows


def thumb_candidates(raw, base):
    # Scan potential BL/BLX pairs at every halfword boundary. These are evidence
    # candidates, not executable-function claims; ARM/data can imitate Thumb.
    cs = Cs(CS_ARCH_ARM, CS_MODE_THUMB)
    cs.detail = True
    rows = []
    for offset in range(0, len(raw) - 3, 2):
        first, second = struct.unpack_from('<2H', raw, offset)
        if first & 0xF800 != 0xF000 or second & 0xC000 != 0xC000:
            continue
        decoded = list(cs.disasm(raw[offset:offset + 4], base + offset))
        if len(decoded) != 1 or decoded[0].size != 4:
            continue
        found = branch(decoded[0], [], raw, base)
        if found:
            rows.append({'offset': offset, 'runtime_address': base + offset,
                         'instruction': decoded[0].mnemonic + ' ' + decoded[0].op_str,
                         **found, 'native_id_constant': None,
                         'context': [], 'classification': 'thumb-call-candidate-needs-function-boundary-proof'})
    return rows


def table_message_candidates(address, arm9, entries):
    """Read eight fallback slots; primary selector bounds remain unproven."""
    if address is None or address % 4:
        return None
    offset = address - 0x02000000
    if not 0 <= offset <= len(arm9) - 32:
        return None
    values = struct.unpack_from('<8I', arm9, offset)
    if any(value != 0xFFFFFFFF and value >= len(entries) for value in values):
        return None
    return [{'slot': slot, 'message_id': None if value == 0xFFFFFFFF else value,
             'source': None if value == 0xFFFFFFFF else entries[value].text.decode('cp932')}
            for slot, value in enumerate(values)]


def mapped_dynamic_producers(arm9, entries):
    """Source-pinned, individually reviewed cases; no general flow solver."""
    cs = Cs(CS_ARCH_ARM, CS_MODE_ARM)
    cs.detail = True
    if struct.unpack_from('<I', arm9, 0x59134)[0] != 0x02053FE4:
        raise ValueError('Reviewed switch tail literal differs')
    cases = []
    for offset in range(0x59064, 0x590ED, 8):
        instructions = list(cs.disasm(arm9[offset:offset + 4], 0x02000000 + offset))
        value = locally_resolved_argument(instructions, arm9, 0x02000000, 'r1')
        if value is None or not 0 <= value < len(entries):
            raise ValueError('Reviewed switch assignment differs')
        cases.append({'assignment_address': 0x02000000 + offset, 'message_id': value,
                      'source': entries[value].text.decode('cp932')})
    return {
        'status': 'reviewed-static-producers-not-gameplay-reachability-proof',
        'guarded_wrapper': {
            'caller': 0x020BE534, 'wrapper': 0x020BF328,
            'guarded_input_min': 21, 'guarded_input_max': 144,
            'caller_subtracts': 21, 'wrapper_adds': 137,
            'native_id_min': 137, 'native_id_max': 260,
            'caller_span_sha256': sha(arm9[0xBE51C:0xBE53C]),
            'wrapper_span_sha256': sha(arm9[0xBF328:0xBF338]),
            'remaining_promotional_or_scene_id_overlap': False,
        },
        'switch_tail': {
            'tail_address': 0x020590F8, 'join_address': 0x020590F0,
            'target': 0x02053FE4,
            'assignment_and_tail_span_sha256': sha(arm9[0x59064:0x59134]),
            'visible_case_assignments': cases,
            'remaining_promotional_or_scene_id_overlap': any(
                3289 <= row['message_id'] <= 3319 or 3393 <= row['message_id'] <= 3606
                for row in cases),
            'limitations': 'Selector paths and incoming callers still require separate review.',
        },
    }


def mapped_actor_table_producers(arm9, entries):
    # These alternatives were reviewed from each complete producer span, not
    # inferred by allowing conditional instructions into linear propagation.
    producers = (
        (0x0202DE94, (0x2DEEC,), 0x2DE14, 0x2DEA4,
         'fp loaded before loop and preserved across native calls'),
        (0x02030B10, (0x30FD4, 0x30FD8), 0x30B04, 0x30B14,
         'EQ/NE literal alternatives after comparing r5 with 3'),
        (0x02033E7C, (0x33EB0, 0x33EB4), 0x33E64, 0x33E80,
         'NE/EQ literal alternatives after comparing r7 with zero'),
    )
    rows = []
    for caller, literals, lo, hi, reason in producers:
        alternatives = []
        for literal in literals:
            pointer = struct.unpack_from('<I', arm9, literal)[0]
            slots = table_message_candidates(pointer, arm9, entries)
            if slots is None:
                raise ValueError('Reviewed actor-table producer differs')
            alternatives.append({'literal_offset': literal, 'table_address': pointer,
                                 'fallback_slots': slots})
        rows.append({'caller': caller, 'producer_span_sha256': sha(arm9[lo:hi]),
                     'reviewed_reason': reason, 'table_alternatives': alternatives})
    return rows


def main():
    path = Path('work/clean.nds')
    rom = NdsImage.open(path)
    arm9 = rom.read_file('/__arm9__.bin')
    if sha(path.read_bytes()) != 'f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d':
        raise ValueError('Exact clean ROM required')
    for lo, hi, digest in WRAPPER_LOCKS:
        if sha(arm9[lo:hi]) != digest:
            raise ValueError('Native accessor wrapper differs')
    entries = common_message_entries(rom.read_file('/COMMON/MESFILE.DK4'), arm9)
    sections = MainCodeFile(arm9, 0x02000000).sections
    components = [(f'arm9_autoload_{i}', s.ramAddress, bytes(s.data)) for i, s in enumerate(sections)]
    overlays = loadOverlayTable(rom.rom.arm9OverlayTable, lambda oid, fid: rom.files[fid])
    components += [(f'arm9_overlay_{oid}', overlay.ramAddress, bytes(overlay.data)) for oid, overlay in overlays.items()]
    rows = []
    for name, base, raw in components:
        for mode, scanner in (('arm', arm_candidates), ('thumb', thumb_candidates)):
            for row in scanner(raw, base):
                value = row['native_id_constant']
                message_id = value if value is not None and 0 <= value < len(entries) else None
                rows.append({'component': name, 'instruction_mode': mode, **row, 'message_id': message_id,
                             'fallback_table_candidates': table_message_candidates(
                                 row.get('native_table_address_constant'), arm9, entries),
                             'source': entries[message_id].text.decode('cp932') if message_id is not None else None})
    extended = [row for row in rows if row['instruction_mode'] == 'thumb' or row['kind'] != 'direct-call'
                or row['component'] not in ('arm9_autoload_0', 'arm9_overlay_0')]
    report = {'status': 'extended-common-reference-candidates-not-unused-text-proof',
              'source_rom_sha256': sha(path.read_bytes()), 'candidate_count': len(rows),
              'additional_wrapper': {'entry': 0x020BF328, 'argument_register': 'r1',
                                     'native_id_addend': 137, 'forwarded_target': 0x020546B8,
                                     'code_sha256': sha(arm9[0xBF328:0xBF338])},
              'extended_candidate_count': len(extended), 'extended_candidates': extended,
              'promotional_candidates': [row for row in rows if row['message_id'] is not None and 3289 <= row['message_id'] <= 3319],
              'scene_label_candidates': [row for row in rows if row['message_id'] is not None and 3393 <= row['message_id'] <= 3606],
              'mapped_dynamic_producers': mapped_dynamic_producers(arm9, entries),
              'actor_variant_table_candidates': [row for row in rows if row['target'] in TABLE_TARGETS],
              'reviewed_actor_table_producers': mapped_actor_table_producers(arm9, entries),
              'actor_variant_code_spans': [
                  {'start_offset': lo, 'end_offset': hi, 'sha256': sha(arm9[lo:hi])}
                  for lo, hi in ((0x53EC0, 0x53F0C), (0x53F0C, 0x53F4C),
                                 (0x53F4C, 0x53F9C), (0x7E988, 0x7E9A0))],
              'components': [{'name': n, 'runtime_base': b, 'bytes': len(r), 'sha256': sha(r)} for n, b, r in components],
              'candidates': rows,
              'limitations': ['Function/data boundaries require individual verification.',
                             'Unknown register targets, vtables, incoming IDs and script/table producers remain unresolved.',
                             'Thumb local ID propagation is deliberately not guessed.',
                             'Actor variant tables list eight fallback slots; primary selector bounds remain unproven.',
                             'Visible branch joins discard prior values; external predecessors remain unproven.',
                             'Absent resolved IDs do not prove unused promotional or caption copies.']}
    out = Path('work/analysis/native_common_extended_calls_clean.json')
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({key: report[key] for key in ('candidate_count', 'extended_candidate_count')}))
    for row in extended:
        print(row['component'], row['instruction_mode'], hex(row['runtime_address']), row['kind'], row['message_id'])


if __name__ == '__main__':
    main()
