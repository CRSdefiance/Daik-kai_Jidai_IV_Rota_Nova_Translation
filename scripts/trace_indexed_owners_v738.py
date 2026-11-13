"""Bounded one-variable resource-array leads, not runtime reachability proof."""

import struct
from pathlib import Path

from capstone import CS_ARCH_ARM, CS_MODE_ARM, Cs
from capstone.arm import ARM_OP_IMM, ARM_OP_MEM, ARM_OP_REG

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.trace_control_aliases_v688 import sections
from scripts.trace_resource_owner_tables_v585 import initialize
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/indexed_owners_v738')
ROM = Path('out/all_routes_combined_v712_candidate.nds')
MASK = 0xFFFFFFFF
NAMES = ('r0', 'r1', 'r2', 'r3', 'r4', 'r5', 'r6', 'r7', 'r8', 'sb', 'sl', 'fp', 'ip', 'sp', 'lr')


def constant(number):
    number &= MASK
    return number, {}, 0x02310000 <= number < 0x02316000


def symbolic(name):
    return 0, {name: 1}, False


def multiply(value, factor):
    if value is None:
        return None
    return value[0] * factor & MASK, {k: v * factor & MASK for k, v in value[1].items()
                                     if v * factor & MASK}, value[2]


def add(left, right, sign=1):
    if left is None or right is None:
        return None
    coefficients = dict(left[1])
    for name, value in right[1].items():
        coefficients[name] = (coefficients.get(name, 0) + sign * value) & MASK
    coefficients = {k: v for k, v in coefficients.items() if v}
    if len(coefficients) > 1:
        return None
    number = (left[0] + sign * right[0]) & MASK
    return number, coefficients, left[2] or right[2] or 0x02310000 <= number < 0x02316000


def scalar(value, variable, index):
    if value is None or any(k != variable for k in value[1]):
        return None
    return (value[0] + value[1].get(variable, 0) * index) & MASK


def scan(parts, targets):
    decoder = Cs(CS_ARCH_ARM, CS_MODE_ARM)
    decoder.detail = True
    memory = [(base, base + len(data), data) for _, base, data in parts]

    def word(address):
        for lo, hi, data in memory:
            if lo <= address <= hi - 4:
                return struct.unpack_from('<I', data, address - lo)[0]
        return None

    rows, statistics = [], []
    for label, base, data in parts:
        registers = {n: symbolic(n) for n in NAMES}
        prefix = []
        decoded = 0

        def reset():
            return {n: symbolic(n) for n in NAMES}, []

        for offset in range(0, len(data) - 3, 4):
            pc = base + offset
            ins = next(decoder.disasm(data[offset:offset + 4], pc, count=1), None)
            if ins is None or int.from_bytes(ins.bytes, 'little') >> 28 != 14:
                registers, prefix = reset()
                continue
            decoded += 1
            registers['pc'] = constant(pc + 8)
            operands = ins.operands
            if (operands and operands[0].type == ARM_OP_REG
                    and ins.reg_name(operands[0].reg) == 'pc'
                    and ins.mnemonic in ('mov', 'ldr', 'add', 'sub', 'rsb', 'mul', 'lsl')):
                registers, prefix = reset()
                continue
            before = dict(registers)
            prefix.append({'PC': pc, 'bytes': bytes(ins.bytes).hex(),
                           'assembly': ins.mnemonic + ' ' + ins.op_str})
            if len(prefix) > 64:
                registers, prefix = reset()
                continue

            def operand(op, before=before, ins=ins):
                if op.type == ARM_OP_IMM:
                    return constant(op.imm)
                if op.type != ARM_OP_REG:
                    return None
                value = before.get(ins.reg_name(op.reg))
                if op.shift.type == 2 and 0 <= op.shift.value < 32:
                    return multiply(value, 1 << op.shift.value)
                return value if not op.shift.type else None

            value, dest = None, None
            if ins.mnemonic in ('mov', 'add', 'sub', 'rsb', 'mul', 'lsl') and operands[0].type == ARM_OP_REG:
                dest = ins.reg_name(operands[0].reg)
                args = [operand(op) for op in operands[1:]]
                if ins.mnemonic == 'mov':
                    value = args[0]
                elif len(args) == 2:
                    a, b = args
                    if ins.mnemonic == 'add':
                        value = add(a, b)
                    elif ins.mnemonic == 'sub':
                        value = add(a, b, -1)
                    elif ins.mnemonic == 'rsb':
                        value = add(b, a, -1)
                    elif a is not None and b is not None and not b[1]:
                        value = multiply(a, b[0]) if ins.mnemonic == 'mul' else (
                            multiply(a, 1 << b[0]) if b[0] < 32 else None)
                    elif ins.mnemonic == 'mul' and a is not None and not a[1]:
                        value = multiply(b, a[0])
                if value is not None and value[1] and value[2]:
                    variable, = value[1]
                    witnesses = []
                    for index in range(256):
                        result = scalar(value, variable, index)
                        if result in targets:
                            witnesses.append({'index': index, 'owner': result, 'filename': targets[result]})
                    if witnesses:
                        rows.append({'kind': 'affine_owner_base', 'unit': label, 'PC': pc,
                                     'assembly': ins.mnemonic + ' ' + ins.op_str, 'destination': dest,
                                     'variable': variable, 'constant': value[0], 'coefficient': value[1][variable],
                                     'witnesses': witnesses, 'before_registers': before, 'prefix': list(prefix)})
            elif ins.mnemonic == 'ldr' and len(operands) == 2 and operands[1].type == ARM_OP_MEM and not ins.writeback:
                dest = ins.reg_name(operands[0].reg)
                mem = operands[1].mem
                address = before.get(ins.reg_name(mem.base))
                if mem.index:
                    index_value = before.get(ins.reg_name(mem.index))
                    if operands[1].shift.type not in (0, 2):
                        index_value = None
                    elif operands[1].shift.type == 2:
                        index_value = multiply(index_value, 1 << operands[1].shift.value)
                    address = add(address, multiply(index_value, mem.scale))
                address = add(address, constant(mem.disp))
                if address is not None and not address[1]:
                    loaded = word(address[0])
                    value = constant(loaded) if loaded is not None else None
                elif address is not None and len(address[1]) == 1:
                    variable, = address[1]
                    witnesses = []
                    for index in range(256):
                        at = scalar(address, variable, index)
                        loaded = word(at)
                        if loaded in targets:
                            witnesses.append({'index': index, 'address': at, 'owner': loaded, 'filename': targets[loaded]})
                    if witnesses:
                        rows.append({'kind': 'indexed_source_table', 'unit': label, 'PC': pc,
                                     'assembly': ins.mnemonic + ' ' + ins.op_str, 'destination': dest,
                                     'variable': variable, 'constant': address[0], 'coefficient': address[1][variable],
                                     'witnesses': witnesses, 'before_registers': before, 'prefix': list(prefix)})
            elif ins.mnemonic in ('cmp', 'cmn', 'tst', 'teq', 'nop'):
                continue
            else:
                registers, prefix = reset()
                continue
            if dest in registers:
                registers[dest] = value
        statistics.append({'unit': label, 'base': base, 'bytes': len(data),
                           'aligned_words': len(data) // 4, 'AL_decoded_instructions': decoded,
                           'sha256': sha(data)})
    return rows, statistics


def main():
    ROOT.mkdir(parents=True, exist_ok=True)
    assert not (ROOT / 'verified_leads.json').exists()
    pre = read('work/analysis/village_request_sweep_v735/preflight.json')
    for path, digest in pre['release_hashes'].items():
        assert sha(Path(path).read_bytes()) == digest
    current = NdsImage.open(ROM)
    initialized, arm, executed, writes, owners, names = initialize(current)
    original, clean_arm, original_executed, original_writes, original_owners, original_names = initialize(NdsImage.open('work/clean.nds'))
    assert names == original_names and owners == original_owners and writes == original_writes
    assert executed == original_executed
    assert all(bytes(initialized.mem_read(pc, 4)) == bytes(original.mem_read(pc, 4)) for pc in executed)
    assert arm[0x10E190:0x11155C] == clean_arm[0x10E190:0x11155C]
    previous = read('work/analysis/resource_owners_v585/owner_table_proof.json')
    wanted = set(previous['no_external_pointer_filenames']) | {'_pxl/__frame.pxl', '_pxl/logo.pxl',
        '_pxl/copyright.pxl', '_pxl/ship_eurL.pxl', '_pxl/startmenu0.pxl'}
    targets = {owner: name for owner, name in names.items() if name in wanted
               and '/' + name in current.path_map()}
    assert targets[0x023139C0] == '_pxl/kakutei.pxl' and targets[0x02313F60] == '_pxl/__frame.pxl'
    versions = {}
    for label, path in (('clean', Path('work/clean.nds')), ('current', ROM)):
        parts = sections(NdsImage.open(path))
        rows, stats = scan(parts, targets)
        versions[label] = {'candidate': str(path), 'candidate_sha256': sha(path.read_bytes()),
                           'parts': [{'name': n, 'base': b, 'bytes': len(d), 'sha256': sha(d)} for n, b, d in parts],
                           'leads': rows, 'statistics': stats}
        print(label, len(rows), 'indexed/affine leads', flush=True)
    save(ROOT / 'verified_leads.json', {'targets': {str(k): v for k, v in targets.items()}, 'versions': versions,
                               'requested_names_not_represented_by_this_owner_catalogue': sorted(wanted - set(names.values())),
                               'catalogued_names_without_exact_FNT_path_not_silently_given_runtime_aliases': sorted(
                                   name for name in wanted & set(names.values()) if '/' + name not in current.path_map()),
                               'all315_initialized_resource_names_writes_and_executed_code_clean_current_exact': True,
                               'index_window_is_supplied_0_to255_not_an_original_runtime_domain': True,
                               'straight_line_AL_one_variable_only_calls_branches_stores_and_unknowns_stop': True,
                               'initial_source_tables_not_claimed_immutable_at_runtime': True,
                               'no_ordinary_display_or_global_nonuse_claim': True,
                               'producer_sha256': sha(Path(__file__).read_bytes()),
                               'release_hashes_unchanged': pre['release_hashes'], 'full_goal_complete': False})


if __name__ == '__main__':
    main()
