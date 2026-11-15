"""Resolve the V626 capital-I comparison using the source dialog ink palette.

This is a new verifier for existing captures, not a ROM patch or a fresh gameplay
run. The historical V257 renderer and V626 evidence are preserved unchanged.
"""

import struct
from collections import Counter
from pathlib import Path

from ndspy.code import MainCodeFile
from PIL import Image
from unicorn import UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_R0, UC_ARM_REG_R2, UC_ARM_REG_R3, UC_ARM_REG_SP

from dk4tool.patch.common_dialogue_alignment import POOL
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from scripts.probe_button_prompt_native import BASE, STACK, call, machine
from scripts.verify_regional_ui_v616 import native5
from scripts.verify_tavern_queued_native_v626 import queued_wrap
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/dialogue_palette_v628')
CAP = Path('E:/Rota Nova translations/Generated/work/emulation_v193/tavern_schemes_v626_expert')
ROM = Path('out/all_routes_combined_v627_candidate.nds')
SOURCE = Path('out/all_routes_combined_v626_candidate.nds')
PALETTE = 0x02125A20
CASES = (
    (6000, 909, 0x02118340, 0x02053DB8, []),
    (8000, 915, 0x02118320, 0x02053DB8, ['Bribe']),
    (8800, 973, 0x02118220, 0x02053DB8, []),
    (9600, 979, 0x02118200, 0x02053D24, ['Lisbon', 'Castor Co.']),
    (10000, 965, 0x02118240, 0x02053DB8, []),
    (12800, 915, 0x02118320, 0x02053DB8, ['Lure Fleet']),
    (13600, 921, 0x02118300, 0x02053DB8, []),
    (14400, 941, 0x021182A0, 0x02053D24, ['Castor Co.', 'Lisbon']),
    (17600, 915, 0x02118320, 0x02053DB8, ['Forge Papers']),
    (18400, 933, 0x021182C0, 0x02053DB8, []),
    (19200, 949, 0x02118280, 0x02053D24, ['Castor Co.', 'Albuquerque']),
    (22800, 915, 0x02118320, 0x02053DB8, ['Bad Rumors']),
    (23600, 927, 0x02117B40, 0x02053DB8, []),
    (24400, 957, 0x02118260, 0x02053D24, ['Lisbon', 'Castor Co.']),
)


def resident(arm, address, length):
    for section in MainCodeFile(arm, BASE).sections:
        offset = address - section.ramAddress
        if 0 <= offset and offset + length <= len(section.data):
            return bytes(section.data[offset:offset + length])
    raise ValueError(f'Not a complete initialized ARM9 span: {address:#x}+{length}')


def raster(arm, kanji, text, foreground=15):
    """Call original painters with source foreground15 and a 16px line pitch.

    The pitch is the existing controlled replay contract, independently checked
    against every captured pixel below; it is not a captured live font context.
    """
    u = machine(arm)
    u.mem_write(POOL, bytes(MainCodeFile(arm, BASE).sections[3].data[:-48]))
    header, view, ctx, string = 0x02450000, 0x02453000, 0x02454000, 0x02455000
    width, height = 228, 80
    count = width * height // 2
    original = struct.pack('<5I', 4, width // 4, height, (PALETTE - header) & 0xFFFFFFFF, 20)
    u.mem_write(header - 16, b'\xA5' * (20 + count + 32))
    u.mem_write(header, original + bytes(count))
    u.mem_write(view - 16, b'\xA5' * 80)
    call(u, 0xD3D80, (view,))
    u.mem_write(STACK, struct.pack('<4I', width, height, 0, 0))
    call(u, 0xD3AFC, (view, header, 0, 0))
    font = struct.unpack_from('<I', arm, 0xD5088)[0]
    u.mem_write(font + 4, struct.pack('<2I', 6, 16))
    u.mem_write(struct.unpack_from('<I', arm, 0xD19B8)[0], kanji)
    # 020548D4 overwrites the default constructor's color with15 before draw.
    call(u, 0xD5160, (ctx, view, foreground))
    call(u, 0xD5A10, (ctx, 1))
    u.mem_write(ctx + 28, struct.pack('<i', 0))
    u.mem_write(string, text + b'\0')
    events = []

    def observe(cpu, address, instruction_size, unused):
        if address in (BASE + 0xD16B4, 0x01FF83AC):
            code, style = struct.unpack('<2I', cpu.mem_read(cpu.reg_read(UC_ARM_REG_SP), 8))
            events.append({'code': code, 'style': style,
                           'x': cpu.reg_read(UC_ARM_REG_R2), 'y': cpu.reg_read(UC_ARM_REG_R3)})

    u.hook_add(UC_HOOK_CODE, observe)
    call(u, 0x01FFCE40 - BASE, (ctx, string), instruction_limit=600000)
    assert u.reg_read(UC_ARM_REG_R0) - string == len(text)
    assert bytes(u.mem_read(string, len(text) + 1)) == text + b'\0'
    assert bytes(u.mem_read(header, 20)) == original
    assert bytes(u.mem_read(header - 16, 16)) == bytes(u.mem_read(header + 20 + count, 16)) == b'\xA5' * 16
    assert bytes(u.mem_read(view - 16, 16)) == bytes(u.mem_read(view + 48, 16)) == b'\xA5' * 16
    assert struct.unpack('<I', u.mem_read(ctx + 0x30, 4))[0] == foreground
    packed = bytes(u.mem_read(header + 20, count))
    return bytes(n for b in packed for n in (b & 15, b >> 4)), events


def rgb5(word):
    return word & 31, (word >> 5) & 31, (word >> 10) & 31


def captured_rgb(word):
    r, g, b = rgb5(word)
    g6 = (g << 1) | (g >> 4)
    return r * 255 // 31, g6 * 255 // 63, b * 255 // 31


def main():
    ROOT.mkdir(parents=True, exist_ok=True)
    current, source, clean = (NdsImage.open(p) for p in (ROM, SOURCE, 'work/clean.nds'))
    arm, old = (r.read_file('/__arm9__.bin') for r in (current, source))
    original = clean.read_file('/__arm9__.bin')
    assert sha(ROM.read_bytes()) == '0a03862a0a0a75c748e2f806016d2316f881eb9799907590715c41d251bf2a09'
    assert sha(SOURCE.read_bytes()) == '6164af2ddc9f77475b59a0ec05c10d57a9d99fd3853859e72b0b5fcea8510388'
    spans = []
    for start, end, label in (
        (0x020548A8, 0x020548F4, 'source_dialog_context_foreground15_setup'),
        (0x020D16B4, 0x020D19B8, 'ASCII_painter_CP932_shadow_and_shadow_color_selector'),
        (0x01FF83AC, 0x01FF85C8, 'CP932_painter'),
        (PALETTE, PALETTE + 32, 'source_dialog_palette'),
    ):
        data = resident(arm, start, end - start)
        assert data == resident(old, start, end - start) == resident(original, start, end - start), label
        spans.append({'start': start, 'end': end, 'meaning': label, 'sha256': sha(data),
                      'clean_V626_V627_exact': True})
    # mov r2,#15; ...; str r2,[sp,#0x34], with context at sp+4.
    assert resident(arm, 0x020548C8, 4) == bytes.fromhex('0f20a0e3')
    assert resident(arm, 0x020548D4, 4) == bytes.fromhex('34208de5')
    u = machine(arm)
    selector = {}
    for style in (1, 15):
        call(u, 0xD1964, (style,))
        selector[style] = u.reg_read(UC_ARM_REG_R0)
    assert selector == {1: 15, 15: 14}
    palette = struct.unpack('<16H', resident(arm, PALETTE, 32))
    colors = {i: rgb5(palette[i]) for i in (14, 15)}
    assert colors == {14: (24, 24, 24), 15: (0, 1, 0)}
    rgb = {i: captured_rgb(palette[i]) for i in (14, 15)}
    assert rgb == {14: (197, 198, 197), 15: (0, 8, 0)}
    kanji = current.read_file('/GRP/KANJI.FNT')
    assert kanji == source.read_file('/GRP/KANJI.FNT') == clean.read_file('/GRP/KANJI.FNT')
    entries = common_message_entries(current.read_file('/COMMON/MESFILE.DK4'), arm, clean=False)
    previous = common_message_entries(source.read_file('/COMMON/MESFILE.DK4'), old, clean=False)
    report = read(CAP / 'capture_report.json')
    assert report['ROM_sha256'] == sha(SOURCE.read_bytes()) and report['frames'] == 24801
    assert report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
    shots = {s['frame']: s for s in report['frames_captured']}
    results = []
    for frame, number, table, parent, values in CASES:
        assert entries[number].text == previous[number].text
        text = entries[number].text.rstrip()
        for value in values:
            text = text.replace(b'%s', value.encode('ascii'), 1)
        assert b'%s' not in text
        wrapped = queued_wrap(arm, text, parent, table)
        assert wrapped == queued_wrap(old, text, parent, table)
        pixels, events = raster(arm, kanji, wrapped)
        old_style, _ = raster(arm, kanji, wrapped, foreground=1)
        assert set(pixels) <= {0, 14, 15}
        assert bytes(15 if p == 1 else 14 if p == 15 else p for p in old_style) == pixels
        shot = shots[frame]
        assert sha(Path(shot['path']).read_bytes()) == shot['PNG_sha256']
        ram_path = CAP / f'frame_{frame:06d}_arm9_ram.bin'
        ram = ram_path.read_bytes()
        assert ram[PALETTE - BASE:PALETTE - BASE + 32] == resident(arm, PALETTE, 32)
        font_address = struct.unpack_from('<I', arm, 0xD19B8)[0]
        assert ram[font_address - BASE:font_address - BASE + len(kanji)] == kanji
        im = Image.open(shot['path']).convert('RGB').crop((16, 296, 244, 376))
        actual = list(native5(im).get_flattened_data())
        actual_rgb = list(im.get_flattened_data())
        actual_masks = {index: {i for i, c in enumerate(actual) if c == color}
                        for index, color in colors.items()}

        def matches(candidate, masks=actual_masks):
            return all({i for i, p in enumerate(candidate) if p == index} == mask
                       for index, mask in masks.items())

        for index, color in colors.items():
            expected_mask = {i for i, p in enumerate(pixels) if p == index}
            actual_mask = {i for i, c in enumerate(actual) if c == color}
            assert actual_mask == expected_mask, (frame, index, sorted(actual_mask ^ expected_mask)[:10])
        assert matches(pixels)
        painted = [i for i, p in enumerate(pixels) if p]
        assert painted and all(actual[i] == colors[pixels[i]] for i in painted)
        assert all(actual_rgb[i] == rgb[pixels[i]] for i in painted)
        # Negative control reproduces the historical all-nonzero-is-black rule.
        false_differences = [i for i, p in enumerate(old_style) if bool(p) != (actual[i] == colors[15])]
        shadow = [i for i, p in enumerate(pixels) if p == 14]
        assert false_differences == shadow
        cp932 = [e for e in events if e['code'] == 0x8268]
        assert len(shadow) == len(cp932) * 9
        assert all(e['style'] == 15 for e in events)
        # Removing any first/final glyph or each CP932 shadow must fail the masks.
        visible_events = [e for e in events if e['code'] not in (0, 10, 13, 32)]
        edges = [visible_events[0], visible_events[-1]]
        edge_counts = []
        for e in edges:
            indices = [i for i in painted if e['x'] <= i % 228 < e['x'] + 6
                       and e['y'] <= i // 228 < e['y'] + 12]
            assert indices
            modified = bytearray(pixels)
            for i in indices:
                modified[i] = 0
            assert not matches(modified)
            edge_counts.append(len(indices))
        if shadow:
            erased_shadow = bytes(0 if p == 14 else p for p in pixels)
            black_shadow = bytes(15 if p == 14 else p for p in pixels)
            assert not matches(erased_shadow) and not matches(black_shadow)
        preview = Image.new('RGB', (228, 80), (238, 223, 183))
        preview.putdata([rgb[p] if p else (238, 223, 183) for p in pixels])
        preview.save(ROOT / f'frame_{frame:06d}_SOURCE_PALETTE_REPLAY.png')
        im.save(ROOT / f'frame_{frame:06d}_ACTUAL_CROP.png')
        results.append({'frame': frame, 'message_id': number, 'source_voice_table': table,
                        'source_parent': parent, 'text': text.decode('cp932'),
                        'native_formatted': wrapped.decode('cp932'),
                        'whole228x80_foreground_and_shadow_masks_exact': True,
                        'every_painted_pixel_source_palette_color_exact_native5': True,
                        'every_painted_pixel_exact_RGB565_expanded_capture_color': True,
                        'captured_RAM_font_and_palette_exact_to_source_and_current': True,
                        'captured_RAM': str(ram_path), 'captured_RAM_sha256': sha(ram),
                        'all_blank_cells_checked_for_both_ink_colors': True,
                        'first_final_glyph_erasure_controls': edge_counts,
                        'palette_index_counts': dict(Counter(pixels)), 'CP932_I_glyph_events': cp932,
                        'old_binary_rule_false_mismatch_pixels': len(false_differences),
                        'actual_shadow_RGB_values': sorted({actual_rgb[i] for i in shadow}),
                        'source_PNG': shot['path'], 'source_PNG_sha256': shot['PNG_sha256'],
                        'native_indices_sha256': sha(pixels)})
    assert sum(r['old_binary_rule_false_mismatch_pixels'] for r in results) == 45
    assert sum(bool(r['old_binary_rule_false_mismatch_pixels']) for r in results) == 4
    save(ROOT / 'palette_proof.json', {
        'format': 'dk4-dialogue-source-palette-v628', 'current_candidate': str(ROM),
        'current_candidate_sha256': sha(ROM.read_bytes()), 'captured_candidate': str(SOURCE),
        'captured_candidate_sha256': report['ROM_sha256'], 'no_ROM_or_patch_changed': True,
        'no_new_emulator_run_claimed': True, 'source_code_spans': spans,
        'kanji_font_sha256': sha(kanji), 'source_palette_address': PALETTE,
        'source_palette_BGR555A1_words': list(palette), 'native_shadow_selector': selector,
        'foreground15_shadow14_native5': colors, 'cases': results,
        'all14_full_foreground_and_shadow_planes_match_existing_GPU_captures': True,
        'all45_previously_differing_pixels_are_source_gray_shadows_not_missing_foreground': True,
        'four_CP932_I_comparison_findings_resolved_without_pixel_waivers': True,
        'historical_verifiers_and_proofs_retained': True,
        'capture_report': str(CAP / 'capture_report.json'),
        'capture_report_sha256': sha((CAP / 'capture_report.json').read_bytes()),
        'capture_fixture_disclosure': report['synthetic_strategist_room_assignment_fixtures'],
        'actual_live_font_context_not_exported_during_each_draw': True,
        'controlled_16px_line_pitch_verified_by_whole_captured_planes': True,
        'not_a_complete_route_or_hardware_test': True,
        'all18_plaques_and_all22_historical_scopes_retained': True,
        'full_goal_complete': False, 'canonical_promoted': False,
        'script_sha256': sha(Path(__file__).read_bytes())})
    print('V628:14 complete foreground/shadow planes exact;45 old false differences are source gray shadows;ROM unchanged.')


if __name__ == '__main__':
    main()
