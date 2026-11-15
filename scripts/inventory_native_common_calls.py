"""Inventory direct ARM COMMON calls, with conservative local ID resolution."""
import argparse
import hashlib
import json
import struct
from pathlib import Path

from capstone import CS_ARCH_ARM, CS_MODE_ARM, Cs
from capstone.arm import (
    ARM_CC_AL,
    ARM_INS_ADD,
    ARM_INS_B,
    ARM_INS_BL,
    ARM_INS_BLX,
    ARM_INS_BX,
    ARM_INS_LDR,
    ARM_INS_MOV,
    ARM_INS_MVN,
    ARM_INS_SUB,
    ARM_OP_IMM,
    ARM_OP_MEM,
    ARM_OP_REG,
    ARM_REG_PC,
)
from ndspy.code import loadOverlayTable

from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import CODE_LOCKS, common_message_entries

TARGETS = {
    0x0205528C: 'r0', 0x020534F4: 'r1',
    # Varargs wrappers save incoming registers, select the declared native ID,
    # then pass the returned paragraph and remaining arguments to presentation.
    0x02053F9C: 'r1', 0x02053FE4: 'r1',
    0x02054624: 'r0', 0x0205466C: 'r0', 0x020546B8: 'r0',
}
WRAPPER_LOCKS = (
    (0x53F9C, 0x53FE4, '5935dfdc64b82dda851df0bbc134bdf34e729c61b2291f1088d82b59cba66bdd'),
    (0x53FE4, 0x54020, '4c7720e486cc19d5eed0ad7db50f140bf3e68fe721e1c756afed7f4eff8978d8'),
    (0x54624, 0x5466C, 'c7473d6f724abb976360a85e0453f379b41dbc53a9d2b688bdf28d8dfd100d58'),
    (0x5466C, 0x546B8, '293978e5aea0ee1504671dbefe962f53a40e3a079ac1305cbcae773b2a45d6c1'),
    (0x546B8, 0x546F8, '2d02b5deb7b8a05ac86e3518fb646fb1b0490b01e6b5b989b9994627cbe378b9'),
)


def direct_bl_target(word, address):
    if word >> 28 == 15 or word & 0x0F000000 != 0x0B000000:
        return None
    displacement = word & 0xFFFFFF
    if displacement & 0x800000:
        displacement -= 0x1000000
    return (address + 8 + displacement * 4) & 0xFFFFFFFF


def locally_resolved_argument(instructions, raw, base, register):
    known = {}
    for ins in instructions:
        if ins.id in (ARM_INS_B, ARM_INS_BX):
            known.clear()
            continue
        if ins.id in (ARM_INS_BL, ARM_INS_BLX):
            for name in ('r0', 'r1', 'r2', 'r3', 'ip', 'lr'):
                known.pop(name, None)
            continue
        _, writes = ins.regs_access()
        value = None
        operands = ins.operands
        if ins.cc == ARM_CC_AL and operands and operands[0].type == ARM_OP_REG:
            if ins.id in (ARM_INS_MOV, ARM_INS_MVN) and len(operands) == 2:
                operand = operands[1]
                if not operand.shift.type:
                    value = (operand.imm if operand.type == ARM_OP_IMM else
                             known.get(ins.reg_name(operand.reg)) if operand.type == ARM_OP_REG else None)
                    if value is not None and ins.id == ARM_INS_MVN:
                        value = ~value & 0xFFFFFFFF
            elif ins.id in (ARM_INS_ADD, ARM_INS_SUB) and len(operands) == 3:
                left, right = operands[1:]
                if left.type == ARM_OP_REG and right.type == ARM_OP_IMM and not right.shift.type:
                    a = known.get(ins.reg_name(left.reg))
                    if a is not None:
                        value = (a + right.imm if ins.id == ARM_INS_ADD else a - right.imm) & 0xFFFFFFFF
            elif ins.id == ARM_INS_LDR and len(operands) == 2 and operands[1].type == ARM_OP_MEM:
                mem = operands[1].mem
                if mem.base == ARM_REG_PC and not mem.index:
                    offset = ins.address + 8 + mem.disp - base
                    if 0 <= offset <= len(raw) - 4:
                        value = struct.unpack_from('<I', raw, offset)[0]
        for reg in writes:
            known.pop(ins.reg_name(reg), None)
        if value is not None:
            known[ins.reg_name(operands[0].reg)] = value
    return known.get(register)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--rom', type=Path, default=Path('work/clean.nds'))
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    rom = NdsImage.open(args.rom)
    arm9 = rom.read_file('/__arm9__.bin')
    for lo, hi, digest in (*CODE_LOCKS, *WRAPPER_LOCKS):
        if hashlib.sha256(arm9[lo:hi]).hexdigest() != digest:
            raise ValueError('Mapped native accessor code differs')
    entries = common_message_entries(rom.read_file('/COMMON/MESFILE.DK4'), arm9)
    components = [('arm9', 0x02000000, arm9)]
    overlays = loadOverlayTable(rom.rom.arm9OverlayTable, lambda oid, fid: rom.files[fid])
    for oid, overlay in overlays.items():
        components.append((f'arm9_overlay_{oid}', overlay.ramAddress, bytes(overlay.data)))
    cs = Cs(CS_ARCH_ARM, CS_MODE_ARM)
    cs.detail = True
    cs.skipdata = True
    calls = []
    for name, base, raw in components:
        for offset in range(0, len(raw) - 3, 4):
            target = direct_bl_target(struct.unpack_from('<I', raw, offset)[0], base + offset)
            if target not in TARGETS:
                continue
            lo = max(0, offset - 64)
            context = list(cs.disasm(raw[lo:offset], base + lo))
            # Skip-data pseudo instructions do not expose operand/register detail.
            if any(i.id == 0 for i in context):
                value = None
            else:
                value = locally_resolved_argument(context, raw, base, TARGETS[target])
            message_id = value if value is not None and 0 <= value < len(entries) else None
            calls.append({'component': name, 'file_offset': offset, 'runtime_address': base + offset,
                          'return_address': base + offset + 4, 'target': target,
                          'argument_register': TARGETS[target], 'local_constant_value': value,
                          'message_id': message_id,
                          'source': entries[message_id].text.decode('cp932') if message_id is not None else None,
                          'context': [f'{i.address:#010x} {i.mnemonic} {i.op_str}' for i in context]})
    report = {
        'status': 'static-call-inventory-not-an-unused-text-proof',
        'source_rom_sha256': hashlib.sha256(args.rom.read_bytes()).hexdigest(),
        'components': [{'name': n, 'runtime_base': b, 'size': len(r),
                        'sha256': hashlib.sha256(r).hexdigest()} for n, b, r in components],
        'native_id_targets': {hex(target): register for target, register in TARGETS.items()},
        'wrapper_code_hashes_verified': True,
        'direct_arm_call_count': len(calls),
        'locally_resolved_native_id_calls': sum(c['message_id'] is not None for c in calls),
        'unresolved_id_calls': sum(c['message_id'] is None for c in calls),
        'promotional_id_calls': [c for c in calls if c['message_id'] is not None and 3289 <= c['message_id'] <= 3319],
        'scene_label_id_calls': [c for c in calls if c['message_id'] is not None and 3393 <= c['message_id'] <= 3606],
        'calls': calls,
        'limitations': ['Direct ARM BL scan only; indirect and Thumb calls are not covered.',
                        'Local constant resolution does not recover incoming registers, stack values or tables.',
                        'Scanning component data can produce unclassified instruction-like words.',
                        'Absent resolved IDs do not establish that native promotional text is unused.'],
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({k: report[k] for k in ('direct_arm_call_count', 'locally_resolved_native_id_calls',
                                           'unresolved_id_calls')}))
    print('Resolved promotional call sites:', len(report['promotional_id_calls']))


if __name__ == '__main__':
    main()
