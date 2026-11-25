"""Original Town traversal with actual variable facility-node visibility."""

import struct

from unicorn import UC_HOOK_CODE, UC_HOOK_MEM_READ, UC_HOOK_MEM_WRITE
from unicorn.arm_const import (
    UC_ARM_REG_PC,
    UC_ARM_REG_R0,
    UC_ARM_REG_R1,
    UC_ARM_REG_R2,
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

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.rom.nds import NdsImage
from scripts.probe_button_prompt_native import BASE, STACK, call
from scripts.research_town_scene_v644 import setup
from scripts.verify_regional_ui_v616 import glyphs
from scripts.verify_town_scene_v644 import CONTEXT, FRAME_BYTES, LOWER, UPPER


def replay(rom, raw, io, lcdm, dtcm, itcm):
    u, mapping = setup(rom, raw, io, lcdm, dtcm)
    assert len(itcm) == 32768
    u.mem_write(0x01FF0000, itcm)
    u.mem_write(0x01FF8000, itcm)
    arm = rom.read_file('/__arm9__.bin')
    clean = NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    assert all(arm[a:b] == clean[a:b] for a, b in ((0xCA890, 0xCAA4C), (0xC9DC4, 0xC9DD4),
                                                  (0xCA668, 0xCA778), (0xD32B8, 0xD3314)))
    # CA668 consumes and clears a transient submission pointer after drawing.
    # Re-register the actual cached footer through the complete original API;
    # a post-draw capture can legitimately have an empty submission queue.
    slot = struct.unpack_from('<I', arm, 0xD334C)[0]
    queued = struct.unpack('<I', u.mem_read(slot, 4))[0]
    footer = queued or 0x022CF7DC
    assert footer == 0x022CF7DC and struct.unpack('<3I', u.mem_read(footer, 12)) == (4, 64, 12)
    assert struct.pack('<I', footer) in arm
    pending_slot = struct.unpack_from('<I', arm, 0xCA778)[0]
    pending = struct.unpack('<I', u.mem_read(pending_slot, 4))[0]
    assert pending in (0, footer)
    cached = bytes(u.mem_read(footer + 20, 24))
    descriptors = [BASE + at for at in range(0, len(arm) - 24, 4) if arm[at:at + 24] == cached]
    assert descriptors == [0x0211A8B8]
    pointers = struct.unpack('<6I', cached)
    strings = [raw[p - BASE:].split(b'\0')[0].decode('ascii') if p else None for p in pointers]
    assert strings == [None, None, 'Menu', None, None, 'Select']
    indices = bytes(n for b in dtcm[:1536] for n in (b & 15, b >> 4))
    font_mask = glyphs(GameAsciiFont.from_arm9(arm), 'SelectMenu')
    assert len(font_mask) == 140
    assert all(indices[y * 256 + x] == int((x, y) in font_mask) for y in range(12) for x in range(60))
    before_registration = bytes(u.mem_read(BASE, len(raw)))
    registration_code = call(u, 0xCA890, (footer, descriptors[0]))
    owner = footer - 0x58
    assert struct.unpack('<I', u.mem_read(owner, 4))[0] == struct.unpack_from('<I', arm, 0xCA46C)[0]
    assert struct.unpack('<I', u.mem_read(owner + 12, 4))[0] == struct.unpack_from('<I', arm, 0xCA470)[0]
    # Original CPage submission fragment: r4 is its initialized actual owner.
    # Stop before the following system/input call, which is outside this draw.
    u.reg_write(UC_ARM_REG_R4, owner)
    u.emu_start(0x020C9DC4, 0x020C9DD4, count=16)
    assert u.reg_read(UC_ARM_REG_PC) == 0x020C9DD4 and u.reg_read(UC_ARM_REG_R4) == owner
    assert struct.unpack('<I', u.mem_read(pending_slot, 4))[0] == footer
    restored = bytearray(u.mem_read(BASE, len(raw)))
    restored[pending_slot - BASE:pending_slot - BASE + 4] = struct.pack('<I', pending)
    assert bytes(restored) == before_registration
    assert bytes(u.mem_read(0x027E0000, len(dtcm))) == dtcm
    assert all(bytes(u.mem_read(a, 4)) == raw[a - BASE:a - BASE + 4] for a in registration_code)
    assert bytes(u.mem_read(0x020C9DC4, 16)) == arm[0xC9DC4:0xC9DD4]
    guards = bytes(u.mem_read(LOWER - 16, 16)), bytes(u.mem_read(UPPER + FRAME_BYTES, 16))
    u.mem_write(LOWER, b'\xA5' * (2 * FRAME_BYTES))
    nodes, node = [], struct.unpack_from('<I', raw, CONTEXT - BASE + 16)[0]
    while node:
        assert node not in {r['node'] for r in nodes} and len(nodes) < 100
        vt, enabled = struct.unpack_from('<I', raw, node - BASE)[0], struct.unpack_from('<I', raw, node - BASE + 16)[0]
        predicate, draw = struct.unpack_from('<2I', raw, vt - BASE + 8)
        nodes.append({'node': node, 'enabled': enabled, 'visibility_callback': predicate, 'draw_callback': draw})
        node = struct.unpack_from('<I', raw, node - BASE + 8)[0]
    by_node = {r['node']: r for r in nodes}
    traversed, predicates, draws, executed, vram_reads = [], [], [], set(), []
    assigned, old_output_reads, vram_writes = bytearray(2 * FRAME_BYTES), [], []

    def code(cpu, address, size, _):
        executed.add(address)
        if address == 0x020D32C4:
            traversed.append(cpu.reg_read(UC_ARM_REG_R5))
        elif address == 0x020D32E0:
            predicates.append({'node': cpu.reg_read(UC_ARM_REG_R5), 'result': cpu.reg_read(UC_ARM_REG_R0)})
        elif address == 0x020D32F8:
            n, c, target = [cpu.reg_read(r) for r in (UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2)]
            assert n in by_node and c == CONTEXT and target == by_node[n]['draw_callback']
            draws.append({'node': n, 'context': c, 'method': target})

    def read_vram(cpu, kind, address, size, value, _):
        page = (address - 0x06000000) // 16384
        physical = mapping['logical_page_to_physical_LCDC_page'][page] * 16384 + (address & 16383)
        assert all(not (physical < b and physical + size > a)
                   for a, b in ((0x40000, 0x58000), (0x60000, 0x78000)))
        vram_reads.append({'PC': cpu.reg_read(UC_ARM_REG_PC), 'physical_LCDC_offset': physical, 'size': size})

    def read_output(cpu, kind, address, size, value, _):
        if not all(assigned[address - LOWER:address - LOWER + size]):
            old_output_reads.append({'PC': cpu.reg_read(UC_ARM_REG_PC), 'address': address, 'size': size})

    def write(cpu, kind, address, size, value, _):
        if LOWER <= address < UPPER + FRAME_BYTES:
            assert size == 2 and address + size <= UPPER + FRAME_BYTES
            assigned[address - LOWER:address - LOWER + size] = b'\1' * size
        elif 0x06000000 <= address < 0x06800000:
            vram_writes.append([address, size])

    hooks = [u.hook_add(UC_HOOK_CODE, code), u.hook_add(UC_HOOK_MEM_WRITE, write),
        u.hook_add(UC_HOOK_MEM_READ, read_vram, begin=0x06000000, end=0x067FFFFF),
        u.hook_add(UC_HOOK_MEM_READ, read_output, begin=LOWER, end=UPPER + FRAME_BYTES - 1)]
    u.reg_write(UC_ARM_REG_R4, CONTEXT)
    u.reg_write(UC_ARM_REG_R5, CONTEXT + 12)
    u.reg_write(UC_ARM_REG_SP, STACK)
    saved = {r: 0xB5B51000 + i for i, r in enumerate((UC_ARM_REG_R6, UC_ARM_REG_R7, UC_ARM_REG_R8,
                                                    UC_ARM_REG_R9, UC_ARM_REG_R10, UC_ARM_REG_R11))}
    for reg, value in saved.items():
        u.reg_write(reg, value)
    try:
        u.emu_start(0x020D32B8, 0x020D3314, count=50000000)
    finally:
        for h in hooks:
            u.hook_del(h)
    assert u.reg_read(UC_ARM_REG_PC) == 0x020D3314 and u.reg_read(UC_ARM_REG_SP) == STACK
    assert u.reg_read(UC_ARM_REG_R4) == CONTEXT and u.reg_read(UC_ARM_REG_R5) == 0
    assert all(u.reg_read(r) == v for r, v in saved.items())
    assert traversed == [r['node'] for r in nodes]
    assert [r['node'] for r in predicates] == [r['node'] for r in nodes if r['enabled']]
    assert [r['node'] for r in draws] == [r['node'] for r in predicates if r['result']]
    assert all(assigned) and not old_output_reads and not vram_writes
    assert (bytes(u.mem_read(LOWER - 16, 16)), bytes(u.mem_read(UPPER + FRAME_BYTES, 16))) == guards
    assert bytes(u.mem_read(0x027E0000, len(dtcm))) == dtcm
    for address in executed:
        expected = (itcm[address & 32767:(address & 32767) + 4] if 0x01FF0000 <= address < BASE
                    else raw[address - BASE:address - BASE + 4])
        assert len(expected) == 4 and bytes(u.mem_read(address, 4)) == expected
    return bytes(u.mem_read(UPPER, FRAME_BYTES)), bytes(u.mem_read(LOWER, FRAME_BYTES)), {
        'mapping': mapping, 'nodes': nodes, 'source_visibility_returns': predicates,
        'actual_original_callback_sequence': draws, 'VRAM_reads': vram_reads,
        'all_native_nodes_and_enabled_predicates_traversed_in_original_order': True,
        'actual_draws_exactly_match_nonzero_original_predicates': True,
        'original_cached_footer_registration': {'method': 0x020CA890, 'actual_bitmap_header': footer,
            'original_submission_fragment': [0x020C9DC4, 0x020C9DD4], 'actual_initialized_owner': owner,
            'unique_original_static_descriptor': descriptors[0], 'pending_queue_field': pending_slot,
            'captured_pending_pointer': pending, 'only_transient_queue_word_changes_in_isolated_registration': True,
            'all720_active_footer_cache_cells140_English_ink_pixels_exact_independent_ROM_font': True,
            'all_cached_strings_geometry_palette_pixels_and_DTCM_preserved': True,
            'provided_native_registration_contract_not_a_new_gameplay_or_timing_claim': True},
        'all196608_destination_bytes_poisoned_and_written_before_any_read': True,
        'no_visible_VRAM_output_reads_no_VRAM_writes_ABI_guards_and_code_identity_pass': True,
        'executed_addresses': sorted(executed)}
