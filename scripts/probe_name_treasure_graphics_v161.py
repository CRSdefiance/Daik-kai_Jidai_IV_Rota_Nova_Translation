"""Native glyph-cell proof and image sizing under explicit resource contracts."""

import json
import struct
from pathlib import Path

from PIL import Image

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.graphics.pxl import PxlImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.build_integrated_release import apply_pxl_native_label_batch
from scripts.materialize_name_treasure_graphics_v161 import (
    BASE,
    NAME,
    NAME_BATCH,
    PRIOR,
    TREASURE,
    TREASURE_BATCH,
)
from scripts.probe_button_prompt_native import HEADER, STACK, call, machine

VIEW = 0x02480000  # Outside the complete 256x192 eight-bit texture allocation.


def mask_for(source, batch, row):
    font = GameAsciiFont.from_arm9(source)
    x0, y0, x1, y1 = row.get('draw_box', row['box'])
    advance = batch['advance']
    trim = batch.get('trim_blank_top_rows', 0)
    width = len(row['text']) * advance
    draw_origin = (x0 + (x1 - x0 - width) // 2, y0 + (y1 - y0 - (11 - trim)) // 2)
    if draw_origin[0] < x0 or draw_origin[1] < y0:
        raise ValueError('Complete native glyph cells escape the label')
    # Two blank scratch rows allow the complete eleven-row native cell to run
    # safely; all visible output is translated back to the actual asset origin.
    origin = (draw_origin[0], draw_origin[1] - trim + 2)
    canvas = Image.new('L', (256, 194))
    for index, character in enumerate(row['text']):
        glyph = font.decode(character).convert('L')
        bounds = glyph.getbbox()
        if trim and glyph.crop((0, 0, 6, trim)).getbbox() is not None:
            raise ValueError('Font trim would drop visible pixels')
        if bounds and bounds[2] > batch['glyph_width']:
            raise ValueError('Compact English crops a native glyph')
        canvas.paste(glyph, (origin[0] + index * advance, origin[1]))
    bounds = canvas.getbbox()
    if not (bounds and x0 <= bounds[0] < bounds[2] <= x1
            and y0 + 2 <= bounds[1] < bounds[3] <= y1 + 2):
        raise ValueError('Complete letter pixels escape the owned label rectangle')
    return canvas, origin


def glyph_case(source, batch, row, expected_mask=None):
    mask, origin = mask_for(source, batch, row)
    if expected_mask is None:
        expected_mask = mask
    # A correctly packed four-bit scratch canvas is the actual native glyph
    # primitive's format. The treasure asset is eight-bit: this proves its font
    # shapes, not a claim that this primitive directly draws eight-bit textures.
    blank = struct.pack('<5I', 4, 64, 194, 20, 52) + bytes(32 + 256 * 194 // 2)
    uc = machine(source)
    uc.mem_write(HEADER - 16, b'\xA5' * (len(blank) + 32))
    uc.mem_write(HEADER, blank)
    executed = set()
    color = batch['color_index']
    for index, character in enumerate(row['text']):
        uc.mem_write(STACK, struct.pack('<2I', ord(character), color))
        executed |= call(uc, 0xD16B4, (0, HEADER, origin[0] + index * batch['advance'], origin[1]))
    expected = bytes(color if value else 0 for value in expected_mask.tobytes())
    result = PxlImage.from_bytes(bytes(uc.mem_read(HEADER, len(blank))))
    if (bytes(result.indices) != expected or not {0x020D16B4, 0x020D1820} <= executed
            or bytes(uc.mem_read(HEADER - 16, 16)) != b'\xA5' * 16
            or bytes(uc.mem_read(HEADER + len(blank), 16)) != b'\xA5' * 16
            or result.source[:52] != blank[:52]):
        raise ValueError('Complete native English raster/first letter/header/guards differ')
    return {'id': row['id'], 'english': row['text'], 'advance': batch['advance'],
            'scratch_cell_origin': list(origin),
            'letter_pixel_bounds_in_asset': [mask.getbbox()[0], mask.getbbox()[1] - 2,
                                             mask.getbbox()[2], mask.getbbox()[3] - 2],
            'complete_native_raster_sha256': sha(expected),
            'native_all_glyph_cells_and_ABI_pass': True,
            'first_and_final_letters_exact': True}


def sizing(source, raw, selector, resource, supplied_table=False):
    uc = machine(source)
    table = 0x02115EA8
    actual_resource = int.from_bytes(uc.mem_read(table + selector * 4, 4), 'little')
    if supplied_table:
        # Treasure is not a SLACKIMG member. Run the unmodified common sizing
        # path with a controlled table input, without claiming its live consumer.
        uc.mem_write(table + selector * 4, struct.pack('<I', resource))
    elif actual_resource != resource:
        raise ValueError('Source image selector resource binding differs')
    if source[0x15EE00:0x15EE04] != struct.pack('<I', 0x020BEE88):
        raise ValueError('Existing concrete PXL getter vtable changed')
    uc.mem_write(resource, struct.pack('<5I', 0x0215EE00, HEADER, 0, 0, 0))
    uc.mem_write(HEADER, raw)
    uc.mem_write(VIEW - 16, b'\xA5' * (0x30 + 32))
    uc.mem_write(VIEW, bytes(0x30))
    call(uc, 0xD3D80, (VIEW,))
    executed = call(uc, 0x470B4, (selector, VIEW))
    image = PxlImage.from_bytes(raw)
    dimensions = struct.unpack('<2I', uc.mem_read(VIEW + 0x28, 8))
    selected = int.from_bytes(uc.mem_read(VIEW + 0xC, 4), 'little')
    if (dimensions != (image.width, image.height) or selected != resource
            or not {0x020470B4, 0x020BEE88, 0x020D4018, 0x020D3A1C} <= executed
            or bytes(uc.mem_read(VIEW - 16, 16)) != b'\xA5' * 16
            or bytes(uc.mem_read(VIEW + 0x30, 16)) != b'\xA5' * 16
            or bytes(uc.mem_read(HEADER, len(raw))) != raw):
        raise ValueError('Native full image sizing/adoption/guards differ')
    return {'selector_input': selector, 'resource': resource, 'dimensions': list(dimensions),
            'native_size_and_view_ABI_pass': True,
            'table_input': 'controlled-treasure-header-test' if supplied_table else 'exact-native-name-plaque-table',
            'header_and_resource_class': 'controlled-loaded-PXL-contract'}


def main():
    base = NdsImage.open(BASE)
    source = NdsImage.open(PRIOR).read_file('/__arm9__.bin')
    rows = []
    targets = []
    for path, batch_path in ((NAME, NAME_BATCH), (TREASURE, TREASURE_BATCH)):
        batch = json.loads(batch_path.read_text(encoding='utf-8'))
        target, _ = apply_pxl_native_label_batch(batch_path, base.read_file(path), source)
        targets.append(target)
        rows.extend(glyph_case(source, batch, row) for row in batch['records'])
    sizes = [sizing(source, targets[0], selector, 0x023131DC) for selector in range(12, 20)]
    sizes.append(sizing(source, targets[1], 20, 0x02313A10, supplied_table=True))
    report = {
        'status': 'pass-complete-native-compact-glyphs-and-source-image-size',
        'source_arm9_sha256': sha(source), 'source_rom_sha256': sha(PRIOR.read_bytes()),
        'complete_native_label_cases': rows, 'full_image_sizing_cases': sizes,
        'limitations': ['Concrete loaded resource class/header remain controlled inputs.',
                        'The treasure uses a controlled selector table input, not a proven live consumer.',
                        'Treasure glyph shapes execute in the native four-bit scratch canvas; its eight-bit texture is packed separately.',
                        'Actual loaders, live atlas crops, complete widget/GPU/palette/alpha/input and physical gameplay remain pending.']}
    Path('work/analysis/name_treasure_graphics_v161_native.json').write_text(
        json.dumps(report, indent=2) + '\n', encoding='utf-8')
    print('Pass: six complete native label rasters and nine scoped full image sizing cases.')


if __name__ == '__main__':
    main()
