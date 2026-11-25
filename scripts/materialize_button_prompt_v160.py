"""Register both source-locked copies of the reviewed English button prompt."""

import copy
import json
import zlib
from pathlib import Path

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.graphics.pxl import PxlImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.build_integrated_release import apply_ilnk_pxl_sync_batch, apply_pxl_native_label_batch
from scripts.research_button_prompt import ARCHIVE, BLOCK, BOX, LOOSE, ROM, TEXT, make

LABEL = Path('translations/button_prompt_graphics_v1.json')
SYNC = Path('translations/button_prompt_embedded_sync_v1.json')


def save(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def main():
    base = NdsImage.open('out/raphael_natural_v2_accepted_base.nds')
    prior = NdsImage.open(ROM)
    for name in (LOOSE, ARCHIVE):
        if base.read_file(name) != prior.read_file(name):
            raise ValueError('Canonical source artwork must equal V159')
    loose, archive, mask, _origin = make(prior)
    p = PxlImage.from_bytes(loose)
    background = bytearray(p.indices)
    for i, value in enumerate(mask.tobytes()):
        if value:
            background[i] = 0  # Font faces must be drawn by the native-label compiler.
    left, top, right, bottom = BOX
    cropped = bytes(background[y * 156 + x] for y in range(top, bottom) for x in range(left, right))
    label = {
        'format': 'dk4-pxl-native-label-batch-v1', 'file_path': LOOSE,
        'source_file_sha256': sha(base.read_file(LOOSE)),
        'font_file_path': '/__arm9__.bin',
        'font_sha256': '427776b1266289206333d94cf27c292df0d15d6f26f7c52f3846fee641c32058',
        'target_locale': 'en-US', 'editorial_policy': 'natural-dialogue-v2',
        'scope': 'Complete original generic button instruction in both graphics resources',
        'glyph_width': 6, 'advance': 6, 'color_index': 14, 'erase_palette_indices': [14],
        'records': [{
            'id': 'DK4_PRESS_A_BUTTON_GRAPHIC_V1', 'box': list(BOX), 'text': TEXT,
            'background_indices_zlib_hex': zlib.compress(cropped).hex(),
            'source_japanese': 'ボタンを押してください！',
            'source_meaning': 'Please press a button.',
            'context': 'Shared generic button prompt graphic, image slot 20.',
            'localization_note': 'Natural concise English preserves the unspecified button and exclamation.',
            'artwork_note': 'Retains dimensions/palette/side margins; reconstructs owned baked lettering background with ordered dithering, dark outline and lower/right shadow.',
            'review': {'source': True, 'localization': True, 'naturalness': True, 'visual': True,
                       'storage': True, 'native_glyphs': True, 'physical_gameplay': False},
        }],
    }
    save(LABEL, label)
    actual, ids = apply_pxl_native_label_batch(LABEL, base.read_file(LOOSE), base.read_file('/__arm9__.bin'))
    if actual != loose or ids != ['DK4_PRESS_A_BUTTON_GRAPHIC_V1']:
        raise ValueError('Native graphic batch differs from reviewed complete artwork')
    old_block = IlnkContainer.parse(base.read_file(ARCHIVE)).blocks[BLOCK]
    sync = {
        'format': 'dk4-ilnk-pxl-sync-v1', 'file_path': ARCHIVE,
        'id': 'DK4_PRESS_A_BUTTON_EMBEDDED_GRAPHIC_V1',
        'source_file_sha256': sha(base.read_file(ARCHIVE)),
        'source_block_sha256': sha(old_block),
        'source_image_path': LOOSE, 'source_image_sha256': sha(loose),
        'block_index': BLOCK, 'block_header_size': 64,
        'target_width': 156, 'target_height': 24, 'target_x': 0, 'target_y': 0,
        'target_locale': 'en-US',
        'scope': 'Synchronize only slot 20 pixel payload; preserve embedded metadata and palette.',
    }
    save(SYNC, sync)
    actual, ids = apply_ilnk_pxl_sync_batch(SYNC, base.read_file(ARCHIVE), loose)
    if actual != archive or ids != ['DK4_PRESS_A_BUTTON_EMBEDDED_GRAPHIC_V1']:
        raise ValueError('Embedded sync differs from reviewed exact paired artwork')
    path = Path('translations/release_stack.json')
    registry = json.loads(path.read_text(encoding='utf-8'))
    profile = copy.deepcopy(registry['profiles']['all-routes-unified-v159'])
    profile['batches'] += [LABEL.as_posix(), SYNC.as_posix()]
    profile['note'] = 'Preserves V159 and confirmed shared-copy/Ceuta repairs. Both English button graphic copies are experimental; no canonical promotion.'
    profile['description'] = ('Complete 435-batch V159 stack and all terminal stages plus two source-locked '
                              'button-prompt graphics batches. Complete natural English glyphs and scoped '
                              'native sizing verified; physical resource/palette/input checks pending.')
    registry['profiles']['all-routes-unified-v160'] = profile
    save(path, registry)
    print('Registered experimental all-routes-unified-v160, 437 batches, two paired graphic copies.')


if __name__ == '__main__':
    main()
