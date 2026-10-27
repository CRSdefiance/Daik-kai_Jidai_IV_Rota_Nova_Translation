"""Replay the actual captured upper scene; reject missing hardware/output sources."""

import struct
from pathlib import Path

from unicorn import UC_HOOK_CODE, UC_HOOK_MEM_READ, UC_HOOK_MEM_WRITE, UcError
from unicorn.arm_const import (
    UC_ARM_REG_PC,
    UC_ARM_REG_R4,
    UC_ARM_REG_R5,
    UC_ARM_REG_R6,
    UC_ARM_REG_R7,
    UC_ARM_REG_R8,
    UC_ARM_REG_R9,
    UC_ARM_REG_R10,
    UC_ARM_REG_R11,
    UC_ARM_REG_SP,
)

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.inspect_graphic_paints_v669 import ROM
from scripts.probe_button_prompt_native import BASE, STACK, machine
from scripts.run_village_visits_v664 import CAP
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/still_reveal_v675')
UPPER, SIZE, CONTEXT = 0x022F9794, 98304, 0x023117C4


def replay(rom, raw):
    arm = rom.read_file('/__arm9__.bin')
    u, original = machine(arm), machine(arm)
    u.mem_write(BASE, raw)
    nodes, node = [], struct.unpack_from('<I', raw, CONTEXT - BASE + 16)[0]
    while node:
        assert len(nodes) < 50 and node not in {n['node'] for n in nodes}
        vt = struct.unpack_from('<I', raw, node - BASE)[0]
        predicate, draw = struct.unpack_from('<2I', raw, vt - BASE + 8)
        nodes.append({'node': node, 'vtable': vt, 'predicate': predicate, 'draw': draw})
        node = struct.unpack_from('<I', raw, node - BASE + 8)[0]
    methods = {n['draw'] for n in nodes}
    assigned, executed, calls, global_writes, source_reads = bytearray(SIZE), set(), [], [], set()
    u.mem_write(UPPER - 16, b'\xA5' * (SIZE + 32))

    def code(cpu, address, size, user):
        executed.add(address)
        if address in methods:
            calls.append(address)
        assert address not in (0x020DED50, 0x020DEBDC, 0x020DEB70, 0x020DED08), 'Unexpected file operation'

    def write(cpu, access, address, size, value, user):
        if UPPER <= address < UPPER + SIZE:
            assert address + size <= UPPER + SIZE
            assigned[address - UPPER:address - UPPER + size] = b'\1' * size
        elif not STACK - 4096 <= address < STACK:
            global_writes.append({'PC': cpu.reg_read(UC_ARM_REG_PC), 'address': address,
                'bytes': size, 'value': value})
            assert BASE <= address < BASE + len(raw)

    def memory_read(cpu, access, address, size, value, user):
        assert not (0x04000000 <= address < 0x06800000), 'Hardware/VRAM source not supplied'
        assert not (0x027E0000 <= address < 0x027E4000), 'Actual DTCM source not supplied'
        if UPPER <= address < UPPER + SIZE:
            assert all(assigned[address - UPPER:address - UPPER + size]), 'Old output reused before assignment'
        source_reads.add(address)

    handles = (u.hook_add(UC_HOOK_CODE, code), u.hook_add(UC_HOOK_MEM_WRITE, write),
               u.hook_add(UC_HOOK_MEM_READ, memory_read))
    saved = {r: 0xB5B51000 + i for i, r in enumerate((UC_ARM_REG_R6, UC_ARM_REG_R7,
        UC_ARM_REG_R8, UC_ARM_REG_R9, UC_ARM_REG_R10, UC_ARM_REG_R11))}
    error = None
    try:
        for reg, value in saved.items():
            u.reg_write(reg, value)
        u.reg_write(UC_ARM_REG_R4, CONTEXT)
        u.reg_write(UC_ARM_REG_R5, CONTEXT + 12)
        u.reg_write(UC_ARM_REG_SP, STACK)
        u.emu_start(0x020D32B8, 0x020D3314, count=50000000)
        assert u.reg_read(UC_ARM_REG_PC) == 0x020D3314 and u.reg_read(UC_ARM_REG_SP) == STACK
        assert all(u.reg_read(reg) == value for reg, value in saved.items())
    except (AssertionError, ValueError, UcError) as exc:
        error = repr(exc)
    finally:
        for handle in handles:
            u.hook_del(handle)
    output = bytes(u.mem_read(UPPER, SIZE))
    known_code = []
    for address in executed:
        if bytes(u.mem_read(address, 4)) != bytes(original.mem_read(address, 4)):
            known_code.append(address)
    return output, {'error': error, 'PC': u.reg_read(UC_ARM_REG_PC), 'nodes': nodes, 'calls': calls,
        'assigned_bytes': sum(assigned), 'global_writes': global_writes,
        'executed_addresses': sorted(executed), 'nonregistered_instruction_words': known_code,
        'all_source_read_addresses': sorted(source_reads),
        'source_RAM_sha256': sha(raw), 'output_sha256': sha(output),
        'upper_guard_before': bytes(u.mem_read(UPPER - 16, 16)).hex(),
        'upper_guard_after': bytes(u.mem_read(UPPER + SIZE, 16)).hex()}


def main():
    ROOT.mkdir(parents=True, exist_ok=True)
    rom = NdsImage.open(ROM)
    frozen = read('work/analysis/confirm_material_v572/audit_scope_before.json')
    if not (ROOT / 'preflight.json').exists():
        save(ROOT / 'preflight.json', {'candidate': str(ROM), 'candidate_sha256': sha(ROM.read_bytes()),
            'release_hashes': {str(p): sha(p.read_bytes()) for p in (ROM, ROM.with_suffix('.manifest.json'),
                ROM.with_suffix('.xdelta'), Path('translations/release_stack.json'),
                Path('out/raphael_natural_v2_accepted_base.nds'))},
            'previous_goal_turn_classification': 'progress: V674 actual Maria still source, original movie request trace, corrected hypothesis and explicit reveal gap',
            'all_original_audits_before': {n: read(Path('translations') / n) for n in frozen}})
    rows = []
    for frame in (3700, 3800, 3900, 4000):
        path = CAP / f'maria_dispatch_v674_observed/frame_{frame:06d}_arm9_ram.bin'
        raw = path.read_bytes()
        output, result = replay(rom, raw)
        target = ROOT / f'{frame}_replayed_upper.bin'
        target.write_bytes(output)
        result.update({'frame': frame, 'snapshot': str(path), 'output': str(target),
            'differences_from_captured_software_words': sum(a != b for a, b in zip(output,
                raw[UPPER - BASE:UPPER - BASE + SIZE], strict=True)), 'not_final_verification': True})
        rows.append(result)
        save(ROOT / 'initial_replay_research.json', rows)
        print(frame, 'error', result['error'], 'assigned', result['assigned_bytes'],
            'byte differences', result['differences_from_captured_software_words'], 'callbacks', result['calls'], flush=True)


if __name__ == '__main__':
    main()
