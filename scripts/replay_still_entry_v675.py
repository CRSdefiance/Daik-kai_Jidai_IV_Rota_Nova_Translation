"""Original scene replay using exact before-paint RAM, TCM and source VRAM mapping."""

import struct
from pathlib import Path

from ndspy.code import loadOverlayTable
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
from scripts.probe_button_prompt_native import BASE, STACK, machine
from scripts.research_still_reveal_v675 import CONTEXT, ROOT, SIZE, UPPER
from scripts.research_town_scene_v644 import setup
from scripts.run_village_visits_v664 import CAP
from scripts.verify_village_wrap_v608 import read, save


def replay(rom, raw, regions):
    arm = rom.read_file('/__arm9__.bin')
    u, mapping = setup(rom, raw, regions['9REG'], regions['LCDM'], regions['DTCM'])
    u.mem_write(0x01FF0000, regions['ITCM'])
    u.mem_write(0x01FF8000, regions['ITCM'])
    original = machine(arm)
    overlay = loadOverlayTable(rom.rom.arm9OverlayTable, lambda i, f: rom.files[f])[0]
    original.mem_write(overlay.ramAddress, bytes(overlay.data))
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
        'upper_guard_after': bytes(u.mem_read(UPPER + SIZE, 16)).hex(), 'source_VRAM_mapping': mapping}

def main():
    pre = read(ROOT / 'preflight.json')
    rom = NdsImage.open(pre['candidate'])
    folder = CAP / 'still_reveal_v675_before_iterator_v3'
    observer = read(folder / 'before_paint/observer.json')
    report = read(folder / 'capture_report.json')
    afters = {s['frame']: s for s in report['read_only_capture_RAM_snapshots']}
    rows = []
    for event in observer['rows']:
        frame = event['frame']
        regions = {k: Path(v['path']).read_bytes() for k, v in event['files'].items()}
        assert all(sha(regions[k]) == v['sha256'] for k, v in event['files'].items())
        output, result = replay(rom, regions['WRAM'], regions)
        after = Path(afters[frame]['path']).read_bytes()
        target = ROOT / f'{frame}_before_entry_native_upper.bin'
        target.write_bytes(output)
        result.update({'frame': frame, 'event': event, 'output': str(target),
            'differences_from_after_frame_software_bytes': sum(a != b for a, b in zip(output,
                after[UPPER-BASE:UPPER-BASE+SIZE], strict=True)), 'not_final_verification': True})
        rows.append(result)
        save(ROOT / 'before_entry_replay_research.json', rows)
        print(frame, 'error', result['error'], 'assigned', result['assigned_bytes'],
            'diff', result['differences_from_after_frame_software_bytes'],
            'unregistered', len(result['nonregistered_instruction_words']), flush=True)


if __name__ == '__main__':
    main()
