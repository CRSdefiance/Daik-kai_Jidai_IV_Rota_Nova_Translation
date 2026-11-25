"""Verify full current Town pixels from original iterator, VRAM sources and DTCM."""

import struct
from pathlib import Path

from PIL import Image
from unicorn import UC_HOOK_CODE, UC_HOOK_MEM_READ, UC_HOOK_MEM_WRITE
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

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.probe_button_prompt_native import BASE, STACK
from scripts.probe_worldmap_overlays_v638 import color5
from scripts.research_town_scene_v644 import ROM, ROOT, page_map, setup
from scripts.verify_regional_ui_v616 import glyphs
from scripts.verify_village_wrap_v608 import read, save

CONTEXT, LOWER, UPPER = 0x023117AC, 0x022E1794, 0x022F9794
FRAME_BYTES, DTCM_BASE = 98304, 0x027E0000


def replay(rom, raw, io, lcdm, dtcm, itcm):
    u, mapping = setup(rom, raw, io, lcdm, dtcm)
    # Both actual ITCM aliases are restored. Firmware/graphics code is not guessed.
    assert len(itcm) == 32768
    u.mem_write(0x01FF0000, itcm)
    u.mem_write(0x01FF8000, itcm)
    guards = (bytes(u.mem_read(LOWER - 16, 16)), bytes(u.mem_read(UPPER + FRAME_BYTES, 16)))
    u.mem_write(LOWER, b'\xA5' * (FRAME_BYTES * 2))
    nodes, node = [], struct.unpack_from('<I', raw, CONTEXT - BASE + 16)[0]
    while node:
        assert node not in {n['node'] for n in nodes} and len(nodes) < 100
        vt = struct.unpack_from('<I', raw, node - BASE)[0]
        predicate, draw = struct.unpack_from('<2I', raw, vt - BASE + 8)
        nodes.append({'node': node, 'visibility_callback': predicate, 'draw_callback': draw})
        node = struct.unpack_from('<I', raw, node - BASE + 8)[0]
    methods = {n['draw_callback'] for n in nodes}
    executed, calls, reads, vram_writes, pixels, global_writes, footer = set(), [], [], [], [], [], []

    def code(cpu, address, size, unused):
        executed.add(address)
        if address in methods:
            calls.append({'method': address, 'node': cpu.reg_read(UC_ARM_REG_R0),
                          'context': cpu.reg_read(UC_ARM_REG_R1)})
        if address == 0x020CA668:
            footer.append(cpu.reg_read(UC_ARM_REG_R0))

    def read_vram(cpu, kind, address, size, value, unused):
        logical = (address - 0x06000000) // 16384
        physical = mapping['logical_page_to_physical_LCDC_page'][logical] * 16384 + (address & 16383)
        assert all(not (physical < end and physical + size > start)
                   for start, end in ((0x40000, 0x58000), (0x60000, 0x78000)))
        reads.append({'PC': cpu.reg_read(UC_ARM_REG_PC), 'logical_address': address,
                      'physical_LCDC_offset': physical, 'size': size})

    def write(cpu, kind, address, size, value, unused):
        if 0x06000000 <= address < 0x06800000:
            vram_writes.append((address, size))
        elif LOWER <= address < UPPER + FRAME_BYTES:
            assert size == 2
            pixels.append(address)
        elif not STACK - 4096 <= address < STACK:
            global_writes.append({'address': address, 'size': size, 'value': value})

    h1 = u.hook_add(UC_HOOK_CODE, code)
    h2 = u.hook_add(UC_HOOK_MEM_READ, read_vram, begin=0x06000000, end=0x067FFFFF)
    h3 = u.hook_add(UC_HOOK_MEM_WRITE, write)
    u.reg_write(UC_ARM_REG_R4, CONTEXT)
    u.reg_write(UC_ARM_REG_R5, CONTEXT + 12)
    u.reg_write(UC_ARM_REG_SP, STACK)
    saved = {r: 0xB5B51000 + i for i, r in enumerate((UC_ARM_REG_R6, UC_ARM_REG_R7, UC_ARM_REG_R8,
                                                   UC_ARM_REG_R9, UC_ARM_REG_R10, UC_ARM_REG_R11))}
    for reg, value in saved.items():
        u.reg_write(reg, value)
    try:
        # Original traversal, original visibility calls, every selected painter,
        # then the original shared-footer call. SDK frame setup is outside scope.
        u.emu_start(0x020D32B8, 0x020D3314, count=50000000)
    finally:
        u.hook_del(h1)
        u.hook_del(h2)
        u.hook_del(h3)
    assert u.reg_read(UC_ARM_REG_PC) == 0x020D3314 and u.reg_read(UC_ARM_REG_SP) == STACK
    assert u.reg_read(UC_ARM_REG_R4) == CONTEXT and u.reg_read(UC_ARM_REG_R5) == 0
    assert all(u.reg_read(r) == v for r, v in saved.items())
    assert not vram_writes
    assert bytes(u.mem_read(LOWER - 16, 16)) == guards[0]
    assert bytes(u.mem_read(UPPER + FRAME_BYTES, 16)) == guards[1]
    assert set(pixels) == set(range(LOWER, UPPER + FRAME_BYTES, 2))
    assert all(c['context'] == CONTEXT for c in calls)
    assert len(calls) == 17 and len(nodes) == 18
    assert all(c['method'] == next(n['draw_callback'] for n in nodes if n['node'] == c['node']) for c in calls)
    for address in executed:
        if 0x01FF0000 <= address < 0x02000000:
            expected = itcm[address & 32767:(address & 32767) + 4]
        else:
            assert BASE <= address <= BASE + len(raw) - 4
            expected = raw[address - BASE:address - BASE + 4]
        assert bytes(u.mem_read(address, 4)) == expected
    assert not ({0x020DED50, 0x020DEBDC, 0x020DEB70, 0x020DED08} & executed)
    assert bytes(u.mem_read(DTCM_BASE, len(dtcm))) == dtcm
    lower = bytes(u.mem_read(LOWER, FRAME_BYTES))
    upper = bytes(u.mem_read(UPPER, FRAME_BYTES))
    return upper, lower, {'mapping': mapping, 'nodes': nodes, 'actual_original_callback_sequence': calls,
        'footer_bitmap_headers': footer, 'VRAM_reads': reads, 'VRAM_writes': vram_writes,
        'all_VRAM_reads_exclude_both_visible_framebuffers': True,
        'actual_both_main_RAM_surface_bytes_poisoned': FRAME_BYTES * 2,
        'all98304_destination_pixels_assigned_native_guards_and_fragment_ABI_pass': True,
        'all_executed_instruction_words_exact_captured_main_RAM_or_ITCM': sorted(executed),
        'native_other_nonstack_writes': global_writes}


def rgb5(data):
    return [w & 32767 for w in struct.unpack('<49152H', data)]


def main():
    pre = read(ROOT / 'preflight.json')
    for p, digest in pre['release_hashes'].items():
        assert sha(Path(p).read_bytes()) == digest
    for p, digest in pre['source_files'].items():
        assert sha(Path(p).read_bytes()) == digest
    prior = Path(pre['source_prior_proof'])
    assert sha(prior.read_bytes()) == pre['source_prior_proof_sha256']
    old = read(prior)
    report_path = Path(old['report'])
    assert sha(report_path.read_bytes()) == old['report_sha256']
    report = read(report_path)
    assert report['ROM_sha256'] == pre['candidate_sha256'] and report['frames'] == 15700
    assert report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
    native = next(s for s in report['read_only_capture_native_states'] if s['frame'] == 15700)
    assert native['read_only_export'] and not native['state_loaded'] and native['main_RAM_unchanged_by_export']
    assert native['serialized_RAM_matches_same_frame_direct_export'] and native['DTCM_region'] == DTCM_BASE
    assert sha(Path(native['path']).read_bytes()) == native['sha256']
    for row in native['regions'].values():
        assert sha(Path(row['path']).read_bytes()) == row['sha256']
    ram_row = next(r for r in report['read_only_pause_RAM_snapshots'] if r['frame'] == 15700)
    raw = Path(ram_row['path']).read_bytes()
    assert sha(raw) == ram_row['sha256']
    io, lcdm, dtcm, itcm = [Path(native['regions'][key]['path']).read_bytes() for key in ('9REG', 'LCDM', 'DTCM', 'ITCM')]
    rom, clean = NdsImage.open(ROM), NdsImage.open('work/clean.nds')
    arm = rom.read_file('/__arm9__.bin')
    assert arm[0xD31EC:0xD331C] == clean.read_file('/__arm9__.bin')[0xD31EC:0xD331C]
    upper, lower, execution = replay(rom, raw, io, lcdm, dtcm, itcm)
    shot = next(s for s in report['frames_captured'] if s['frame'] == 15700)
    assert sha(Path(shot['path']).read_bytes()) == shot['PNG_sha256']
    image = Image.open(shot['path']).convert('RGB')
    expected = [[color5(image.getpixel((x, y + sy))) for y in range(192) for x in range(256)] for sy in (0, 192)]
    assert [rgb5(upper), rgb5(lower)] == expected
    assert upper == lcdm[0x40000:0x40000 + FRAME_BYTES]
    assert lower == lcdm[0x60000:0x60000 + FRAME_BYTES]
    for offset, frame in ((0x40000, expected[0]), (0x60000, expected[1])):
        assert [w & 32767 for w in struct.unpack_from('<49152H', lcdm, offset)] == frame
    # Independently verify all cached footer cells; bitmap origin is an actual native argument.
    assert execution['footer_bitmap_headers'] == [0x022CF7DC]
    fh = execution['footer_bitmap_headers'][0]
    header = struct.unpack_from('<5I', raw, fh - BASE)
    assert header[:3] == (4, 64, 12)
    pixels = (fh + header[4]) & 0xFFFFFFFF
    palette = (fh + header[3]) & 0xFFFFFFFF
    assert pixels == DTCM_BASE and BASE <= palette < BASE + len(arm) - 32
    source_indices = bytes(n for b in dtcm[:1536] for n in (b & 15, b >> 4))
    font = GameAsciiFont.from_arm9(arm)
    mask = glyphs(font, 'SelectMenu')
    complete = bytes(int((x, y) in mask) for y in range(12) for x in range(256))
    assert len(mask) == 140
    assert all(source_indices[y * 256 + x] == complete[y * 256 + x]
               for y in range(12) for x in range(60))
    inactive_ink = sum(bool(source_indices[y * 256 + x]) for y in range(12) for x in range(60, 256))
    pointers = struct.unpack_from('<6I', raw, fh - BASE + 20)
    strings = [raw[p - BASE:].split(b'\0')[0].decode('ascii') if p else None for p in pointers]
    assert strings == [None, None, 'Menu', None, None, 'Select']
    metadata = list(struct.unpack_from('<18h', raw, fh - BASE + 44))
    assert metadata[6:9] == [157, 24, 36] and metadata[15:18] == [203, 36, 0]
    controls = []
    for label, start, letter in (('Select_first_S', 0, 'S'), ('Select_final_t', 30, 't'),
                                 ('Menu_first_M', 36, 'M'), ('Menu_final_u', 54, 'u')):
        bad = bytearray(dtcm)
        for y in range(12):
            for x in range(start, start + 6):
                i = y * 256 + x
                bad[i // 2] &= 0x0F if i & 1 else 0xF0
        a, b, _ = replay(rom, raw, io, lcdm, bytes(bad), itcm)
        assert rgb5(a) == expected[0]
        different = sum(x != y for x, y in zip(rgb5(b), expected[1], strict=True))
        assert different == len(glyphs(font, letter))
        controls.append({'erased_source_cell': label, 'whole_lower_RGB5_differences': different,
                         'all_other_pixels_exact': True, 'rejected': True})
    blank = bytes(1536) + dtcm[1536:]
    a, b, _ = replay(rom, raw, io, lcdm, blank, itcm)
    assert rgb5(a) == expected[0]
    assert sum(x != y for x, y in zip(rgb5(b), expected[1], strict=True)) == 140
    # Erasing only visible video outputs cannot change the reconstruction; no output is an input.
    no_display = bytearray(lcdm)
    for start in (0x40000, 0x60000):
        no_display[start:start + FRAME_BYTES] = bytes(FRAME_BYTES)
    a, b, _ = replay(rom, raw, io, bytes(no_display), dtcm, itcm)
    assert (a, b) == (upper, lower)
    bad_io = bytearray(io)
    bad_io[0x243] = 0
    try:
        page_map(bad_io)
    except ValueError:
        pass
    else:
        raise AssertionError('Unreviewed bank configuration accepted')
    # Store an unscaled derivative only; original full capture stays separate.
    replay_image = Image.new('RGB', (256, 384))
    for data, sy in ((upper, 0), (lower, 192)):
        for i, c in enumerate(rgb5(data)):
            replay_image.putpixel((i % 256, i // 256 + sy),
                ((c & 31) * 255 // 31, ((((c >> 5) & 31) << 1) | (((c >> 5) & 31) >> 4)) * 255 // 63,
                 ((c >> 10) & 31) * 255 // 31))
    assert replay_image.tobytes() == image.tobytes()
    replay_path = ROOT / 'complete_both_screens_NATIVE_REPLAY_RGB8.png'
    replay_image.save(replay_path)
    words_path = ROOT / 'complete_native_surface_words_UPPER_THEN_LOWER.bin'
    words_path.write_bytes(upper + lower)
    proof = {'candidate': str(ROM), 'candidate_sha256': pre['candidate_sha256'],
        'reused_actual_report': str(report_path), 'reused_actual_report_sha256': old['report_sha256'],
        'reused_frame': shot, 'new_emulator_run_claimed': False, 'RAM_sha256': sha(raw),
        'read_only_native_state': {'path': native['path'], 'sha256': native['sha256']},
        'original_iterator_and_footer_execution': execution,
        'full98304_upper_and_lower_RGB5_pixels_exact_no_exclusions': True,
        'all98304_full16bit_output_words_exact_physical_VRAM_including_bit15': True,
        'all98304_full_RGB888_capture_pixels_exact_via_original_RGB565_expansion': True,
        'all98304_actual_physical_VRAM_pixels_exact_to_capture': True,
        'footer_active720_source_cells140_ink_complete_Select_Menu_and_blank_cells_exact': True,
        'inactive_cached_tail_nonzero_cells_preserved_not_rendered_by_actual_metadata': inactive_ink,
        'footer_native_source_metadata': {'header': fh, 'words': list(header), 'pixels': pixels,
            'palette': palette, 'label_pointers': list(pointers), 'strings': strings, 'metadata': metadata},
        'four_leading_and_final_footer_glyph_deletions_rejected': controls,
        'missing_DTCM_negative_reproduces_exact140_missing_footer_ink_points': True,
        'erasing_both_captured_visible_VRAM_outputs_has_no_effect_on_reconstruction': True,
        'unsupported_bank_configuration_rejected_unmapped_pages_not_filled': True,
        'all_source_VRAM_reads_only_offscreen_cache_and_no_VRAM_writes': True,
        'complete_native_source_replay_RGB8_PNG': str(replay_path), 'replay_PNG_sha256': sha(replay_path.read_bytes()),
        'native_surface_words': str(words_path), 'native_surface_words_sha256': sha(words_path.read_bytes()),
        'SDK_frame_setup_GPU_hardware_timing_other_scenes_and_every_state_not_verified': True,
        'all18_plaques_incomplete_all22_historical_scopes_retained': True,
        'ROM_patch_registry_canonical_and_all_release_pointers_unchanged': True,
        'ordinary_card_miniature_Confirm_legacy_and_remaining_graphics_gates_open': True,
        'full_goal_complete': False, 'scripts': {str(p): sha(p.read_bytes()) for p in
            (Path(__file__), Path('scripts/research_town_scene_v644.py'))}}
    save(ROOT / 'complete_town_scene_proof.json', proof)
    print('Original iterator17 painters+footer rebuild both poisoned surfaces:98304 exact pixels;140 cached footer strokes;all4 first/final deletions rejected;visible-output erasure unchanged.')


if __name__ == '__main__':
    main()
