"""Authorized source-terrain-checked village fixtures for unchanged V617."""

import struct

from ndspy.code import loadOverlayTable
from unicorn.arm_const import UC_ARM_REG_R0

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.native_village_location_v606 import relocate as source_center
from scripts.probe_button_prompt_native import BASE, call, machine

ARM = 'd1bf89d13b0094eaa27464849279e1fdb3254cc6f9f82699522adf0ae8e188df'
REFERENCE = '236c41a67fe8ddc82181b9809c82980a08154b3dc886c44d2cb0f585f202606e'
OFFSETS = ((-22, 0), (22, 0), (0, -22), (0, 22), (-16, -16), (16, -16),
           (-16, 16), (16, 16), (-28, 0), (28, 0), (0, -28), (0, 28),
           (-24, -16), (24, -16), (-24, 16), (24, 16))


def terrain_queries(arm, points):
    rom = NdsImage.open('out/all_routes_combined_v604_candidate.nds')
    assert rom.read_file('/__arm9__.bin') == arm
    source = rom.read_file('/data/WORLDMAP.DK4')
    assert source == NdsImage.open('work/clean.nds').read_file('/data/WORLDMAP.DK4')
    # Original 69C5C/69C68 compare/wrap tile X at the literal69D78 boundary.
    width = struct.unpack_from('<I', arm, 0x69D78)[0]
    assert width == 2500
    blocks = IlnkContainer.parse(source).blocks
    assert len(blocks) == 10 and width // 50 == 50
    overlay = loadOverlayTable(rom.rom.arm9OverlayTable, lambda _, fid: rom.rom.files[fid])[0]
    u = machine(arm)
    u.mem_write(overlay.ramAddress, bytes(overlay.data))
    pages = {}

    def page(px, py):
        assert 0 <= px < 50 and 0 <= py < 50
        if (px, py) not in pages:
            block = px // 5
            data = blocks[block]
            u.mem_write(0x02460000, struct.pack('<2I', block, 0x02480000))
            u.mem_write(0x02480000, data)
            u.mem_write(0x02460100, struct.pack('<2i', px, py))
            u.mem_write(0x024601F0, b'\xA5' * 2532)
            call(u, 0x01FFA10C - BASE, (0x02460000, 0x02460100, 0x02460200), instruction_limit=300000)
            assert bytes(u.mem_read(0x024601F0, 16)) == bytes(u.mem_read(0x02460BC4, 16)) == b'\xA5' * 16
            assert bytes(u.mem_read(0x02480000, len(data))) == data
            pages[px, py] = bytes(u.mem_read(0x02460200, 2500))
        return pages[px, py]

    rows = []
    for point in points:
        tx, ty = (v // 16 for v in point)
        assert 0 <= tx < width
        px, py = tx // 50, ty // 25
        for xx in (px, px - 1 if tx % 50 == 0 else px + 1):
            for yy in (py, py - 1 if ty % 25 == 0 else py + 1):
                xx %= 50
                slot = 0x02468010 + (xx & 1) * 2508 + (yy & 1) * 5016
                u.mem_write(slot, struct.pack('<2i', xx, yy) + page(xx, yy))
        u.mem_write(0x02460100, struct.pack('<2i', *point))
        call(u, 0x69B5C, (0x02468000, 0x02460100))
        result = u.reg_read(UC_ARM_REG_R0)
        rows.append({'map_point': list(point), 'native_collision_result': result, 'collision_free': result == 0})
    return {'WORLDMAP_sha256': sha(source), 'native_decoder': 0x01FFA10C, 'native_predicate': 0x02069B5C,
            'queries': rows, 'source_horizontal_wrap_tile_width': width,
            'loaded_cache_is_explicit_replay_contract': True,
            'page_hashes': {f'{x},{y}': sha(v) for (x, y), v in pages.items()}}


def relocate(arm, raw, village):
    if sha(arm) != ARM or len(raw) != 0x400000 or type(village) is not int or not 0 <= village < 24:
        raise ValueError('Village-context fixture requires pinned V617,4MiB RAM and village0..23')
    reference = NdsImage.open('out/all_routes_combined_v604_candidate.nds').read_file('/__arm9__.bin')
    assert sha(reference) == REFERENCE
    ranges = ((0xCB118, 0xCB124), (0xCACAC, 0xCACBC), (0xCB1A8, 0xCB1B4),
              (0x2E58C, 0x2E5A8), (0x36C70, 0x36C94), (0x578E0, 0x57908),
              (0x78654, 0x78840), (0x2C1C4, 0x2C204), (0x69B5C, 0x69E00))
    assert all(arm[lo:hi] == reference[lo:hi] for lo, hi in ranges)
    assert NdsImage.open('out/all_routes_combined_v617_candidate.nds').read_file('/data/WORLDMAP.DK4') == NdsImage.open('work/clean.nds').read_file('/data/WORLDMAP.DK4')
    _, proof = source_center(reference, raw, village)
    center = [v + 16 for v in proof['village_point']]
    candidates = [[center[0] + dx, center[1] + dy] for dx, dy in OFFSETS]
    terrain = terrain_queries(reference, [center, *candidates])
    water = next((r['map_point'] for r in terrain['queries'][1:] if r['collision_free']), None)
    if water is None:
        raise ValueError(f'No source-verified nearby water position among declared candidates for village{village}')
    assert sum((a - b) ** 2 for a, b in zip(center, water, strict=True)) < 32 ** 2
    offset = proof['active_ship'] - 0x02000000 + 16
    after = bytearray(raw)
    target = [v * 128 for v in water]
    struct.pack_into('<2i', after, offset, *target)
    assert raw[:offset] == after[:offset] and raw[offset + 8:] == after[offset + 8:]
    proof.update({'terrain_proof': terrain, 'village_center': center,
                  'expected_selector_point_after_original_update': water, 'after_ship_fixed_point': target,
                  'actual_candidate_ARM9_sha256': sha(arm), 'reference_fixture_ARM9_sha256': sha(reference),
                  'original_coordinate_getters_terrain_discovery_and_action_code_exact_to_reference': True,
                  'fixture_does_not_select_or_inject_an_artwork_or_event': True,
                  'changes': [{'address': 0x02000000 + i, 'before': raw[i], 'after': after[i]}
                              for i in range(offset, offset + 8) if raw[i] != after[i]],
                  'after_RAM_sha256': sha(after)})
    return bytes(after), proof
