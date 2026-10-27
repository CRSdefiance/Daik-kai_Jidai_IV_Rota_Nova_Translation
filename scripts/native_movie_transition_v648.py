"""Original upper transition painting in isolated captured CPU memory."""
import struct

from unicorn import UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.arm_const import (
    UC_ARM_REG_PC,
    UC_ARM_REG_R0,
    UC_ARM_REG_R1,
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

from scripts.probe_button_prompt_native import BASE, STACK
from scripts.research_town_scene_v644 import setup

LOWER, UPPER, SIZE = 0x022E1794, 0x022F9794, 98304
CONTEXTS = (0x023117AC, 0x023117C4)


def paint(rom, registered_code, raw, io, vram, dtcm, itcm, phase=None):
    u, mapping = setup(rom, raw, io, vram, dtcm)
    u.mem_write(0x01FF0000, itcm)
    u.mem_write(0x01FF8000, itcm)
    lists, methods = {}, set()
    for context in (CONTEXTS[1],):
        nodes, node = [], struct.unpack_from('<I', raw, context - BASE + 16)[0]
        while node:
            assert node not in {n['node'] for n in nodes} and len(nodes) < 50
            vt = struct.unpack_from('<I', raw, node - BASE)[0]
            predicate, draw = struct.unpack_from('<2I', raw, vt - BASE + 8)
            nodes.append({'node': node, 'predicate': predicate, 'draw': draw})
            methods.add(draw)
            node = struct.unpack_from('<I', raw, node - BASE + 8)[0]
        lists[context] = nodes
    effect = next((n['node'] for n in lists[CONTEXTS[1]] if n['draw'] == 0x020283F4), None)
    control = None
    if phase is not None:
        assert effect is not None and 0 <= phase <= 15
        progress, duration = struct.unpack_from('<2I', raw, effect - BASE + 0x38)
        assert duration == 32
        controlled = phase * 2
        u.mem_write(effect + 0x38, struct.pack('<I', controlled))
        control = {'isolated_owned_progress_address': effect + 0x38, 'before': progress,
                   'after': controlled, 'duration': duration, 'original_threshold': phase,
                   'controlled_source_phase_only_not_an_actual_CPU_callback_argument': True}
    guards = [bytes(u.mem_read(UPPER - 16, 16)), bytes(u.mem_read(UPPER + SIZE, 16))]
    u.mem_write(UPPER, b'\xA5' * SIZE)
    executed, calls, writes, io_writes = set(), [], set(), []

    def code(cpu, address, size, unused):
        executed.add(address)
        if address in methods:
            calls.append({'callback': address, 'node': cpu.reg_read(UC_ARM_REG_R0),
                          'context': cpu.reg_read(UC_ARM_REG_R1)})

    def write(cpu, kind, address, size, value, unused):
        if UPPER <= address < UPPER + SIZE:
            assert address + size <= UPPER + SIZE
            writes.update(range(address, address + size))
        elif 0x04000000 <= address < 0x06800000:
            io_writes.append([address, size, value])

    h1, h2 = u.hook_add(UC_HOOK_CODE, code), u.hook_add(UC_HOOK_MEM_WRITE, write)
    saved = {r: 0xB5B51000 + i for i, r in enumerate((UC_ARM_REG_R6, UC_ARM_REG_R7,
        UC_ARM_REG_R8, UC_ARM_REG_R9, UC_ARM_REG_R10, UC_ARM_REG_R11))}
    try:
        for context in lists:
            for reg, value in saved.items():
                u.reg_write(reg, value)
            u.reg_write(UC_ARM_REG_R4, context)
            u.reg_write(UC_ARM_REG_R5, context + 12)
            u.reg_write(UC_ARM_REG_SP, STACK)
            u.emu_start(0x020D32B8, 0x020D3314, count=50000000)
            assert u.reg_read(UC_ARM_REG_PC) == 0x020D3314 and u.reg_read(UC_ARM_REG_SP) == STACK
            assert u.reg_read(UC_ARM_REG_R4) == context and u.reg_read(UC_ARM_REG_R5) == 0
            assert all(u.reg_read(r) == v for r, v in saved.items())
    finally:
        u.hook_del(h1)
        u.hook_del(h2)
    assert not io_writes and len(writes) == SIZE
    assert bytes(u.mem_read(UPPER - 16, 16)) == guards[0]
    assert bytes(u.mem_read(UPPER + SIZE, 16)) == guards[1]
    assert bytes(u.mem_read(0x027E0000, len(dtcm))) == dtcm
    for address in executed:
        assert bytes(u.mem_read(address, 4)) == bytes(registered_code.mem_read(address, 4)), hex(address)
    assert not ({0x020DED50, 0x020DEBDC, 0x020DEB70, 0x020DED08} & executed)
    return bytes(u.mem_read(UPPER, SIZE)), bytes(u.mem_read(LOWER, SIZE)), {
        'original_scene_lists': lists, 'original_callback_sequence': calls,
        'all98304_upper_destination_bytes_assigned_over_poison': True,
        'lower_scene_not_replayed_or_claimed_by_this_source_bitmap_proof': True,
        'guards_and_original_iterator_fragment_ABI_pass': True,
        'all_executed_instruction_words_exact_registered_ROM': sorted(executed),
        'no_GPU_VRAM_or_file_getter_bridge': True, 'actual_captured_ITCM_DTCM_restored': True,
        'controlled_phase': control, 'mapping': mapping}
