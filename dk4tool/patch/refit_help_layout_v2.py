"""Expand only CRemodelCabinInfoView's owned explanation bitmap and crop.

The original five crop records contain three explanation strips, a heading and
three detail rows. A single five-line explanation crop and two retained fields
need three records. The two retired records hold the bitmap cleanup callback.
The native allocator owns the larger bitmap; no arena, autoload or pool grows.
"""

import json
import struct
from pathlib import Path

from keystone import KS_ARCH_ARM, KS_MODE_ARM, Ks
from ndspy.code import MainCodeFile

from dk4tool.patch.grand_race_menu_release import sha
from scripts.probe_common_display_name_hook import branch_link

BASE = 0x02000000
SOURCE = '7b37bf057334edd71e0b66291d8908d799a0406cf2dbdcac2846500dd25ef679'
TABLE, CLEANUP = 0x114CE8, 0x02114D3C
INIT_START, INIT_END = 0x19F90, 0x19FE8
OLD_RECTS = ((-1, 64, 80, 0, 0, 168, 12),
             (-1, 64, 96, 0, 12, 168, 12),
             (-1, 64, 112, 0, 24, 168, 12),
             (-1, 95, 2, 0, 36, 66, 12),
             (-1, 64, 32, 0, 48, 144, 36))
NEW_RECTS = ((-1, 64, 80, 0, 0, 168, 60),
             (-1, 95, 2, 0, 60, 66, 12),
             (-1, 64, 32, 0, 72, 144, 36))


def assemble(lines, address, size):
    data = bytes(Ks(KS_ARCH_ARM, KS_MODE_ARM).asm(';'.join(lines), address)[0])
    if len(data) > size or (size - len(data)) % 4:
        raise ValueError('Refit helper exceeds its exclusively owned footprint')
    return data + struct.pack('<I', 0xE1A00000) * ((size - len(data)) // 4)


def transform(source):
    if sha(source) != SOURCE:
        raise ValueError('Refit layout requires the exact complete V708 ARM9')
    rects = tuple(struct.unpack_from('<7i', source, TABLE + i * 28) for i in range(5))
    if rects != OLD_RECTS:
        raise ValueError('Original five Refit crops differ')
    owners = [(at, struct.unpack_from('<I', source, at)[0]) for at in range(len(source) - 3)
              if BASE + TABLE <= struct.unpack_from('<I', source, at)[0] < BASE + TABLE + 140]
    if owners != [(0x19D04, BASE + TABLE)]:
        raise ValueError('An additional crop-table owner needs review')
    init = assemble([
        'mov r0,#0x2300', 'add r0,r0,#0x70', 'bl 0x02005154',
        # Keep the original embedded header and palette. Only pixels are dynamic.
        'ldr r1,[pc,#0x50]', 'add r1,r5,r1', 'sub r0,r0,r1', 'str r0,[r1,#16]',
        'mov r0,#4', 'str r0,[r1]', 'mov r0,#42', 'str r0,[r1,#4]',
        'mov r0,#108', 'str r0,[r1,#8]', 'ldr r0,[pc,#0x29]',
        'sub r0,r0,r1', 'str r0,[r1,#12]', 'mov r2,#0', 'mov r3,r2',
        'add r0,r5,#16', 'bl 0x020d3abc',
    ], BASE + INIT_START, INIT_END - INIT_START)
    # Literal loads are pinned explicitly rather than relying on an assembler pool.
    init = bytearray(init)
    for off, register, literal in ((12, 1, 0x19FF8), (52, 0, 0x19FFC)):
        distance = literal - (INIT_START + off + 8)
        assert 0 <= distance < 4096 and distance % 4 == 0
        struct.pack_into('<I', init, off, 0xE59F0000 | register << 12 | distance)
    assert struct.unpack_from('<I', source, 0x19FF8)[0] == 0x1C38
    cleanup = assemble([
        'push {r4,lr}', 'mov r4,r0', 'ldr r0,[r4,#16]', 'cmp r0,#0', 'beq done',
        'ldr r1,[r0,#16]', 'add r0,r0,r1', 'bl 0x02005180',
        'mov r1,#0', 'str r1,[r4,#16]', 'done: mov r0,r4',
        'pop {r4,lr}', 'b 0x020d3bd4',
    ], CLEANUP, 56)
    changes = [(INIT_START, bytes(init)),
               (TABLE, b''.join(struct.pack('<7i', *r) for r in NEW_RECTS) + cleanup)]
    for at, old, new in ((0x19CE0, 0xE3A03005, 0xE3A03003),
                         (0x19EB8, 0xE3A00024, 0xE3A0003C),
                         (0x19EE0, 0xE3A02030, 0xE3A02048)):
        assert struct.unpack_from('<I', source, at)[0] == old
        changes.append((at, struct.pack('<I', new)))
    for at in (0x1A048, 0x1A100):
        assert struct.unpack_from('<I', source, at)[0] == branch_link(BASE + at, 0x020D3BD4)
        changes.append((at, struct.pack('<I', branch_link(BASE + at, CLEANUP))))
    result = bytearray(source)
    for at, data in changes:
        result[at:at + len(data)] = data
    restored = bytearray(result)
    for at, data in changes:
        restored[at:at + len(data)] = source[at:at + len(data)]
    assert bytes(restored) == source
    before, after = MainCodeFile(source, BASE), MainCodeFile(bytes(result), BASE)
    assert [(s.ramAddress, len(s.data), s.bssSize) for s in before.sections] == [
        (s.ramAddress, len(s.data), s.bssSize) for s in after.sections]
    assert all(a.data == b.data for a, b in zip(before.sections[1:], after.sections[1:], strict=True))
    return bytes(result), {'source_arm9_sha256': SOURCE, 'target_arm9_sha256': sha(result),
        'owned_spans': [[at, at + len(data)] for at, data in changes],
        'old_crops': OLD_RECTS, 'new_crops': NEW_RECTS, 'original_table_owners': owners,
        'bitmap_size': [168, 108], 'native_allocation_bytes': 9072,
        'original_heading_and_all_three_detail_rows_preserved': True,
        'original_font_twelve_pixel_lines_visible_in_one_five_row_crop': True,
        'two_retired_crop_records_hold_scoped_cleanup_code': [CLEANUP, CLEANUP + 56],
        'both_parent_destructors_release_pixels_and_clear_pointer_before_original_surface_cleanup': True,
        'all_unowned_bytes_sections_pool_startup_allocator_bounds_and_cache_exact': True,
        'changed_records': ['REFIT_FIVE_ROW_BITMAP_CROPS_AND_OWNED_PIXEL_LIFETIME'],
        'experimental': True, 'full_goal_complete': False}


def apply_release(source, config_path):
    config = json.loads(Path(config_path).read_text(encoding='utf-8'))
    if config['format'] == 'dk4-refit-help-layout-v1':
        from dk4tool.patch.refit_help_layout import apply_release as legacy
        return legacy(source, config_path)
    assert config['format'] == 'dk4-refit-help-layout-v2'
    target, proof = transform(source)
    assert json.loads(json.dumps(proof)) == config['proof']
    for path, digest in config['dependencies'].items():
        assert sha(Path(path).read_bytes()) == digest
    return target, proof
