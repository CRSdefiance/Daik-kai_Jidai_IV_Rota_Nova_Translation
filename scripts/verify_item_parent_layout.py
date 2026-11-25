"""Exact native crop positions and complete glyphs in composed item text panels."""

import json
import struct
from pathlib import Path

from ndspy.code import MainCodeFile
from PIL import Image, ImageDraw

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.item_parent_layout_research import transform
from dk4tool.rom.nds import NdsImage
from scripts.probe_item_counter_canvas import verify as counter_canvas
from scripts.probe_item_parent_crops import verify as parent_crops
from scripts.probe_persistent_name_arm7_boot_overlap import execute as boot
from scripts.verify_item_interface_research import verify_page

EXPECTED = [([0, 84], [240, 12], [8, 2]), ([48, 0], [144, 12], [56, 24]),
            ([0, 12], [240, 12], [8, 64]), ([0, 24], [240, 12], [8, 80]),
            ([0, 36], [240, 12], [8, 112]), ([0, 48], [240, 12], [8, 128]),
            ([0, 60], [240, 12], [8, 144])]


def compose(native, requests):
    if len(native['pixels']) == 24576:
        # Native four-bit storage packs the even x pixel in the low nibble.
        pixels = tuple(c for value in native['pixels'] for c in (value & 15, value >> 4))
    else:
        pixels = struct.unpack('<49152H', native['pixels'])
    canvas = [0] * 49152
    cells = []
    for glyph in native['glyph_events']:
        x, y = glyph['x'], glyph['y']
        width = 6 if glyph['kind'] == 'ascii' else 12
        owners = [r for r in requests if r['source_origin'][0] <= x
                  and x + width <= r['source_origin'][0] + r['size'][0]
                  and r['source_origin'][1] <= y
                  and y + 12 <= r['source_origin'][1] + r['size'][1]]
        if len(owners) != 1:
            raise ValueError('Actual parent crops lose or duplicate a complete glyph cell')
        r = owners[0]
        dx, dy = x - r['source_origin'][0] + r['destination_origin'][0], y - r['source_origin'][1] + r['destination_origin'][1]
        if not 0 <= dx <= dx + width <= 256 or not 0 <= dy <= dy + 12 <= 192:
            raise ValueError('Actual parent placement clips a complete glyph cell')
        if dx < 52 and dx + width > 16 and dy < 60 and dy + 12 > 24:
            raise ValueError('New text position overlaps the reserved item icon area')
        cells.append({'code': glyph['code'], 'source': [x, y], 'destination': [dx, dy], 'width': width})
    for r in requests:
        sx, sy = r['source_origin']
        dx, dy = r['destination_origin']
        width, height = r['size']
        if not (0 <= dx <= dx + width <= 256 and 0 <= dy <= dy + height <= 192):
            raise ValueError('Actual parent crop extends beyond the native screen')
        for row in range(height):
            canvas[(dy + row) * 256 + dx:(dy + row) * 256 + dx + width] = pixels[(sy + row) * 256 + sx:(sy + row) * 256 + sx + width]
    for cell in cells:
        sx, sy = cell['source']
        dx, dy = cell['destination']
        for row in range(12):
            if canvas[(dy + row) * 256 + dx:(dy + row) * 256 + dx + cell['width']] != list(
                    pixels[(sy + row) * 256 + sx:(sy + row) * 256 + sx + cell['width']]):
                raise ValueError('Parent composition loses or overwrites native glyph pixels')
    return struct.pack('<49152H', *canvas), cells


def main():
    old = Path('work/analysis/item_interface_cache_research_arm9.bin').read_bytes()
    source, repair = transform(old)
    if source != Path('work/analysis/item_parent_layout_research_arm9.bin').read_bytes():
        raise ValueError('Saved parent repair differs')
    before, after = parent_crops(old), parent_crops(source)
    actual = [(r['source_origin'], r['size'], r['destination_origin']) for r in after['requests']]
    if before['destination_256x192_fit_at_native_zero_origin'] or actual != EXPECTED:
        raise ValueError('Original overflow or repaired native crops differ')
    image = NdsImage.open('out/all_routes_combined_v158_candidate.nds')
    font, common = image.read_file('/GRP/KANJI.FNT'), image.read_file('/COMMON/MESFILE.DK4')
    plan = json.loads(Path('work/analysis/item_interface_plan.json').read_text(encoding='utf-8'))
    cases = [('category-role-effect', (255, 3, 1, 7), {}), ('price', (255, 4, 1, 7), {}),
             ('crew-max-name', (0, 2), {'item_index': 24, 'crew_index': 170}),
             ('ship-max-name', (0, 3), {'item_index': 118, 'ship_index': 107}),
             ('captain-max-name', (0, 2), {'item_index': 24, 'crew_index': 0, 'player_name': b'ABCDEFGHIJKLMNOPQR'}),
             ('ship-editor-max-name', (0, 3), {'item_index': 118, 'ship_index': 49, 'ship_name': b'ABCDEFGHIJKLMNOPQR'}),
             ('real-paragraph', (0, 4), {'item_index': 22}),
             ('promotional', (0, 4), {'item_index': 197})]
    destination = Path('work/qa/item_parent_layout_native')
    destination.mkdir(parents=True, exist_ok=True)
    rows, panels = [], []
    for label, case, options in cases:
        native = verify_page(source, plan, 'main', case, font, 16,
                             common=common if 'item_index' in options else None, **options)
        composite, cells = compose(native, after['requests'])
        rows.append({'case': label, 'options': {k: v.decode('ascii') if isinstance(v, bytes) else v for k, v in options.items()},
                     'draws': native['item_draws'], 'glyph_cells': cells,
                     'source_native_pixels_sha256': sha(native['pixels']), 'composed_pixels_sha256': sha(composite),
                     'all_complete_glyphs_survive_actual_native_crop_positions_without_overlap_or_screen_clipping': True})
        panel = Image.new('RGB', (256, 192))
        panel.putdata([(255, 255, 255) if c == 0 else (128, 128, 128) if c == 14 else (0, 0, 0)
                       for c in struct.unpack('<49152H', composite)])
        panel = panel.resize((768, 576), Image.Resampling.NEAREST)
        panel.save(destination / f'panel_{len(panels)}.png')
        panels.append((label, panel))
    sheet = Image.new('RGB', (1552, 4 * 604), 'white')
    drawing = ImageDraw.Draw(sheet)
    for n, (label, panel) in enumerate(panels):
        x, y = 8 + n % 2 * 776, n // 2 * 604
        drawing.text((x, y + 2), f'{label}; native crop positions/text pixels; physical art/background pending', fill='black')
        sheet.paste(panel, (x, y + 24))
    sheet.save(destination / 'native_sheet.png')
    payload = bytes(MainCodeFile(source, 0x02000000).sections[3].data[:-48])
    loading = boot(source, bytes(image.rom.arm7), image.rom.arm7RamAddress, True, payload)
    if (loading['arm7_source_changed_bytes_after_arm9_autoload']
            or not all(r['matches_original'] for r in loading['arm7_native_loaded_sections'])
            or not all(loading[k] for k in ('repaired_pool_matches_complete_payload', 'repair_returns_with_stack_preserved',
                                            'actual_startup_call_preserves_r0_r3'))
            or not loading['late_copy_cache_model']['worst_case_dirty_data_and_stale_instruction_model_visible']):
        raise ValueError('New parent target fails full startup/cache/ARM7 proof')
    report = {'status': 'pass-native-parent-row-repair-and-composed-glyph-pixels',
              'target_arm9_sha256': sha(source), 'repair': repair, 'before': before, 'after': after,
              'cases': rows, 'boot': loading, 'counter_canvas': counter_canvas(source),
              'visual_review': {'complete': False, 'panel_count': 8, 'sheet': str(destination / 'native_sheet.png')},
              'limitations': ['Seven actual parent crop requests execute on the new target at explicit zero widget origin/layer1.',
                              'Native renderer supplies each source crop/destination; exact source glyph pixels are composed independently.',
                              'Only four descriptor position fields change; full text/helper/bootstrap code and other source crops remain exact.',
                              'Underlying standalone detail layout remains exact; full earlier rasters are preserved relevant-byte evidence.',
                              'Artwork/border/background, UI state/ancestor initialization and physical GPU composition/input remain contracts.',
                              'Full equipment-role eligibility/random/download and physical cold boot still require work.',
                              'Research only; V158 remains latest combined ROM.']}
    Path('work/analysis/item_parent_layout_native_proof.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    print('Pass: seven actual native crops now fit; eight composed complete-glyph panels; new-target startup/cache/ARM7 and counter allocation.')


if __name__ == '__main__':
    main()
