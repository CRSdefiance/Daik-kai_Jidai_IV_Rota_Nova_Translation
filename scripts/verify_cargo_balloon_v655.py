"""Source-bound complete cargo banner/tooltip composition and glyph controls."""

import struct
from pathlib import Path

from PIL import Image
from unicorn import UC_HOOK_MEM_READ, UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_ARM_REG_R0

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.probe_button_prompt_native import BASE, call
from scripts.research_town_scene_v644 import setup
from scripts.verify_dialogue_palette_v628 import captured_rgb
from scripts.verify_regional_ui_v616 import full_cells
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/cargo_tooltip_v655')
CAP = Path('E:/Rota Nova translations/Generated/work/emulation_v193/full_fleet_victory_v654_replay')
ROM = Path('out/all_routes_combined_v653_candidate.nds')
LOWER, UPPER, FRAME_BYTES = 0x022E1794, 0x022F9794, 98304


def main():
    pre = read(ROOT / 'preflight.json')
    for path, digest in pre['release_hashes'].items():
        assert sha(Path(path).read_bytes()) == digest
    previous = read('work/analysis/full_fleet_victory_v654/proof.json')
    assert previous['report_sha256'] == sha((CAP / 'capture_report.json').read_bytes())
    report = read(CAP / 'capture_report.json')
    assert report['frames'] == 28400 and report['cold_boot'] and not report['savestate_loaded']
    shots = {r['frame']: r for r in report['frames_captured']}
    rom, clean = NdsImage.open(ROM), NdsImage.open('work/clean.nds')
    arm = rom.read_file('/__arm9__.bin')
    original = clean.read_file('/__arm9__.bin')
    # The original2px inset and all coordinate arithmetic remain unchanged.
    assert arm[0x68AC:0x6BD0] == original[0x68AC:0x6BD0]
    assert arm[0x6BE0:0x6C2C] == original[0x6BE0:0x6C2C]
    assert arm[0x589FC:0x58A04] == original[0x589FC:0x58A04]
    margin_pointer = struct.unpack_from('<I', arm, 0x6C28)[0]
    assert struct.unpack_from('<2I', arm, margin_pointer - BASE) == (2, 2)
    assert arm[margin_pointer - BASE:margin_pointer - BASE + 8] == original[margin_pointer - BASE:margin_pointer - BASE + 8]
    japanese_pointer = struct.unpack_from('<I', original, 0x15EF18 + 95 * 12)[0] - BASE
    assert original[japanese_pointer:original.index(0, japanese_pointer)].decode('cp932') == '木材'
    font = GameAsciiFont.from_arm9(arm)
    frames = [r['frame'] for r in previous['all21_original_cargo_headings_and_selected_ship_fields']]
    cases, absent = [], []
    for frame in frames:
        raw = (CAP / f'frame_{frame:06d}_arm9_ram.bin').read_bytes()
        state_path = CAP / f'native_state_{frame:06d}/native_state.json'
        state = read(state_path)
        assert state['read_only_export'] and not state['state_loaded'] and state['main_RAM_unchanged_by_export']
        blobs = {}
        for key in ('ITCM', 'DTCM', '9REG', 'LCDM'):
            row = state['regions'][key]
            blobs[key] = Path(row['path']).read_bytes()
            assert sha(blobs[key]) == row['sha256']
        matches = [off - 12 for off in range(0x17000C, len(raw) - 48, 4)
                   if struct.unpack_from('<I', raw, off)[0] == 0x02313A4C
                   and struct.unpack_from('<2I', raw, off + 28) == (256, 16)]
        assert len(matches) == 1
        view, parent = BASE + matches[0], BASE + matches[0] - 0x3070
        vt = struct.unpack_from('<I', raw, parent - BASE)[0]
        offset = struct.unpack_from('<I', raw, vt - BASE - 16)[0]
        assert offset == 0x31F8
        owner = struct.unpack_from('<I', raw, parent - BASE + offset + 20)[0]
        context = owner - 12
        assert context == 0x023117C4
        node = struct.unpack_from('<I', raw, context - BASE + 16)[0]
        nodes = []
        while node:
            assert node not in {n['node'] for n in nodes} and len(nodes) < 100
            v = struct.unpack_from('<I', raw, node - BASE)[0]
            nodes.append({'node': node, 'draw': struct.unpack_from('<I', raw, v - BASE + 12)[0]})
            node = struct.unpack_from('<I', raw, node - BASE + 8)[0]
        balloon_rows = [n for n in nodes if n['draw'] == 0x020068AC
                        and struct.unpack_from('<I', raw, n['node'] - BASE + 16)[0] == 1]
        if not balloon_rows:
            absent.append(frame)
            continue
        assert len(balloon_rows) == 1
        balloon = balloon_rows[0]['node']
        assert struct.unpack_from('<I', raw, balloon - BASE + 0x7C)[0] == 0
        rect = struct.unpack_from('<4I', raw, balloon - BASE + 32)
        crop = struct.unpack_from('<4I', raw, balloon - BASE + 0x60)
        assert rect[2] - rect[0] == 40 and rect[3] - rect[1] == 16 and crop == (0, 0, 36, 12)
        header = struct.unpack_from('<I', raw, balloon - BASE + 0x40)[0]
        flags, words, height, pd, xd = struct.unpack_from('<5I', raw, header - BASE)
        assert (flags, words, height) == (4, 52, 36)
        palette, pixels = (header + pd) & 0xFFFFFFFF, header + xd
        assert palette == 0x02125A20
        assert raw[palette - BASE:palette - BASE + 32] == arm[palette - BASE:palette - BASE + 32]
        assert struct.unpack_from('<H', raw, palette - BASE + 30)[0] == 0x8020
        source = raw[pixels - BASE:pixels - BASE + 208 * 36 // 2]
        indices = bytes(v for b in source for v in (b & 15, b >> 4))
        actual_view = b''.join(indices[y * 208:y * 208 + 36] for y in range(12))
        text = 'Timber'
        independent = bytearray(36 * 12)
        for index, char in enumerate(text):
            glyph = font.decode(char)
            for y in range(11):
                for x in range(6):
                    if glyph.getpixel((x, y)):
                        independent[y * 36 + index * 6 + x] = 15
        assert actual_view == independent
        u, mapping = setup(rom, raw, blobs['9REG'], blobs['LCDM'], blobs['DTCM'])
        u.mem_write(0x01FF0000, blobs['ITCM'])
        u.mem_write(0x01FF8000, blobs['ITCM'])
        call(u, 0xCB124, ())
        item = u.reg_read(UC_ARM_REG_R0) + 4 + 95 * 16
        item_vt = struct.unpack('<I', u.mem_read(item, 4))[0]
        getter = struct.unpack('<I', u.mem_read(item_vt + 8, 4))[0]
        assert getter == 0x020589FC
        call(u, getter - BASE, (item,))
        name_pointer = u.reg_read(UC_ARM_REG_R0)
        assert bytes(u.mem_read(name_pointer, len(text) + 1)) == text.encode() + b'\0'
        banner_node = view + 0x44
        assert next(n['draw'] for n in nodes if n['node'] == banner_node) == 0x0200CAF8
        assert next(i for i, n in enumerate(nodes) if n['node'] == banner_node) < nodes.index(balloon_rows[0])
        call(u, 0xD4170, (view,))
        resource = u.reg_read(UC_ARM_REG_R0)
        art = rom.read_file('/_pxl/senrihin.pxl')
        assert bytes(u.mem_read(resource, len(art))) == art
        vram_reads = []

        def read_vram(cpu, kind, address, size, value, unused, mapping=mapping, vram_reads=vram_reads):
            logical = (address - 0x06000000) // 16384
            physical = mapping['logical_page_to_physical_LCDC_page'][logical] * 16384 + (address & 16383)
            assert all(not (physical < hi and physical + size > lo)
                       for lo, hi in ((0x40000, 0x58000), (0x60000, 0x78000)))
            vram_reads.append([address, size, physical])

        h = u.hook_add(UC_HOOK_MEM_READ, read_vram, begin=0x06000000, end=0x067FFFFF)
        coverage = {'written': set(), 'early_reads': set()}

        def writes(cpu, kind, address, size, value, unused, coverage=coverage):
            coverage['written'].update(range(address, address + size, 2))

        def reads(cpu, kind, address, size, value, unused, coverage=coverage):
            coverage['early_reads'].update(p for p in range(address, address + size, 2)
                                           if p not in coverage['written'])

        hw = u.hook_add(UC_HOOK_MEM_WRITE, writes, begin=LOWER, end=UPPER + FRAME_BYTES - 1)
        hr = u.hook_add(UC_HOOK_MEM_READ, reads, begin=LOWER, end=UPPER + FRAME_BYTES - 1)
        guards = (bytes(u.mem_read(LOWER - 16, 16)), bytes(u.mem_read(UPPER + FRAME_BYTES, 16)))
        before_source = bytes(u.mem_read(pixels, len(source)))
        before_header, before_palette = bytes(u.mem_read(header, 20)), bytes(u.mem_read(palette, 32))

        def draw(u=u, coverage=coverage, banner_node=banner_node, context=context, balloon=balloon):
            u.mem_write(LOWER, b'\xA5' * (FRAME_BYTES * 2))
            coverage['written'].clear()
            coverage['early_reads'].clear()
            call(u, 0xCAF8, (banner_node, context), instruction_limit=1000000)
            before = bytes(u.mem_read(LOWER, FRAME_BYTES))
            call(u, 0x68AC, (balloon, context), instruction_limit=1000000)
            result = bytes(u.mem_read(LOWER, FRAME_BYTES))
            return before, result

        before, output = draw()
        actual = Image.open(shots[frame]['path']).convert('RGB')
        assert sha(Path(shots[frame]['path']).read_bytes()) == shots[frame]['PNG_sha256']
        def colors(data):
            return [captured_rgb(w) for w in struct.unpack('<49152H', data)]
        all_rgb = colors(output)
        union = {(x, y) for y in range(69, 85) for x in range(256)} | {
            (x, y) for y in range(rect[1], rect[3]) for x in range(rect[0], rect[2])}
        assert all(all_rgb[y * 256 + x] == actual.getpixel((x, y + 192)) for x, y in union)
        assert {LOWER + (y * 256 + x) * 2 for x, y in union} <= coverage['written']
        assert not coverage['early_reads']
        origin = (rect[0] + 2, 192 + rect[1] + 2)
        glyphs = full_cells(actual, font, text, *origin, captured_rgb(0x8020))
        assert bytes(u.mem_read(pixels, len(source))) == before_source
        assert bytes(u.mem_read(header, 20)) == before_header
        assert bytes(u.mem_read(palette, 32)) == before_palette
        assert bytes(u.mem_read(LOWER - 16, 16)) == guards[0]
        assert bytes(u.mem_read(UPPER + FRAME_BYTES, 16)) == guards[1]
        first_final = []
        for char_index in (0, len(text) - 1):
            modified = bytearray(source)
            ink = []
            for y in range(12):
                for x in range(char_index * 6, char_index * 6 + 6):
                    pos = y * 208 + x
                    if indices[pos]:
                        modified[pos // 2] &= ~(15 << (4 * (pos & 1)))
                        ink.append((x, y))
            assert ink
            u.mem_write(pixels, bytes(modified))
            _, negative = draw()
            changed = {(i // 2 % 256, i // 2 // 256) for i in range(0, FRAME_BYTES, 2)
                       if output[i:i + 2] != negative[i:i + 2]}
            expected = {(rect[0] + 2 + x, rect[1] + 2 + y) for x, y in ink}
            assert changed == expected
            first_final.append({'character': text[char_index], 'erased_pixels': len(ink),
                                'exact_native_destination_deletion_and_actual_mismatch': True})
            u.mem_write(pixels, source)
        u.hook_del(h)
        u.hook_del(hw)
        u.hook_del(hr)
        im = Image.new('RGB', (256, 192))
        im.putdata(all_rgb)
        im.crop((0, 69, 256, 85)).save(ROOT / f'frame_{frame:06d}_NATIVE_BANNER_COMPOSITION.png')
        im.crop(rect).save(ROOT / f'frame_{frame:06d}_NATIVE_COMPLETE_TOOLTIP.png')
        changes = sum(before[y * 512 + x * 2:y * 512 + x * 2 + 2] != output[y * 512 + x * 2:y * 512 + x * 2 + 2]
                      for y in range(69, 85) for x in range(256))
        cases.append({'frame': frame, 'actual_parent': parent, 'actual_context': context,
                      'original_scene_owner_link': owner, 'banner_node': banner_node, 'balloon_node': balloon,
                      'source_commodity95_original_name_getter': getter, 'name_pointer': name_pointer,
                      'complete_English': text, 'actual_rect_lower_coordinates': list(rect),
                      'clean_Japanese_commodity95': '木材',
                      'original_margin': [2, 2], 'source_crop': list(crop),
                      'all432_cached_text_view_indices_exact_independent_font': True,
                      'complete_tooltip_glyphs': glyphs, 'first_final_native_deletion_controls': first_final,
                      'all4096_banner_and640_tooltip_pixels_exact': True,
                      'compared_union_pixel_positions': len(union), 'banner_pixels_changed_by_popup': changes,
                      'all_union_pixels_assigned_by_native_writes_and_no_output_read_before_write': True,
                      'source_header_and_backing_and_destination_guards_and_ABI_pass': True,
                      'VRAM_reads_exclude_both_visible_framebuffers': vram_reads,
                      'RAM_sha256': sha(raw), 'native_state_manifest_sha256': sha(state_path.read_bytes())})
    assert any(r['frame'] == 23200 and r['banner_pixels_changed_by_popup'] == 369 for r in cases)
    save(ROOT / 'proof.json', {'candidate': str(ROM), 'candidate_sha256': sha(ROM.read_bytes()),
        'reused_V654_terminal_report': str(CAP / 'capture_report.json'),
        'reused_report_sha256': sha((CAP / 'capture_report.json').read_bytes()),
        'actual_original_banner_then_balloon_callbacks': cases,
        'other_sampled_cargo_frames_without_an_active_balloon': absent,
        'native_geometry_selected_from_owner_links_and_original2px_padding_not_English_ink_fit': True,
        'whole_cargo_scene_timer_and_lower_sea_context_diagnostics_not_display_clearance': True,
        'no_new_emulator_or_gameplay_or_arbitrary_constructor_input_credit': True,
        'ROM_patch_registry_and_all_release_pointers_unchanged': True,
        'all18_plaques_incomplete22_historical_scopes_preserved': True,
        'script_sha256': sha(Path(__file__).read_bytes()), 'full_goal_complete': False})
    print(f'V655: {len(cases)} actual complete tooltip/banner compositions,432-cell source masks and first/final native controls pass.')


if __name__ == '__main__':
    main()
