"""Prepare source-locked full region-family boundary repair and native previews."""

import copy
import struct
from pathlib import Path

from ndspy.code import loadOverlayTable
from PIL import Image, ImageDraw, ImageFont
from unicorn.arm_const import UC_ARM_REG_R0

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.region_name_boundaries import (
    BASE,
    END,
    LABELS,
    SOURCE,
    START,
    TABLE,
    transform,
    validate_names,
)
from dk4tool.rom.nds import NdsImage
from scripts.probe_button_prompt_native import call, machine
from scripts.verify_modal_cursor_native_v272 import raster
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/region_boundaries_v640')
CONFIG = Path('translations/region_name_boundaries_v1.json')
ROM = Path('out/all_routes_combined_v636_candidate.nds')


def main():
    ROOT.mkdir(parents=True, exist_ok=True)
    rom, clean = NdsImage.open(ROM), NdsImage.open('work/clean.nds')
    arm, japanese = rom.read_file('/__arm9__.bin'), clean.read_file('/__arm9__.bin')
    assert sha(arm) == SOURCE
    try:
        validate_names(arm)
    except ValueError as error:
        old_failure = str(error)
    else:
        raise AssertionError('Old joined Americas label was not detected')
    config = {'format': 'dk4-region-name-boundaries-v1', 'status': 'previews-pending', 'records': []}
    for index, text in enumerate(LABELS):
        old = struct.unpack_from('<I', arm, TABLE + index * 52)[0] - BASE
        jp = struct.unpack_from('<I', japanese, TABLE + index * 52)[0] - BASE
        config['records'].append({'index': index, 'source_offset': old,
            'Japanese': japanese[jp:japanese.index(0, jp)].decode('cp932'), 'English': text,
            'review': {'existing_reviewed_UI_wording_preserved': True,
                       'independent_NUL_boundary_required': True, 'adjacent_nontext_array_excluded': True}})
    target, proof = transform(arm, japanese, config)
    (ROOT / 'research_arm9.bin').write_bytes(target)
    font = GameAsciiFont.from_arm9(target)
    u = machine(target)
    previews = []
    sheet = Image.new('RGB', (620, 8 * 60 + 50), '#263238')
    draw = ImageDraw.Draw(sheet)
    caption = ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf', 17)
    draw.text((12, 8), 'All8 original shared region names; complete native strings', font=caption, fill='white')
    for index, text in enumerate(LABELS):
        call(u, 0x9458C, (index,))
        record = u.reg_read(UC_ARM_REG_R0)
        pointer = struct.unpack('<I', u.mem_read(record, 4))[0]
        assert bytes(u.mem_read(pointer, len(text) + 1)) == text.encode() + b'\0'
        pixels, _events, returned = raster(target, text.encode(), width=96, height=16,
                                          wrapping=0, native_pointer=pointer)
        expected = bytearray(96 * 16)
        for n, char in enumerate(text):
            glyph = font.decode(char)
            for y in range(11):
                for x in range(6):
                    if glyph.getpixel((x, y)):
                        expected[y * 96 + n * 6 + x] = 1
        assert pixels == expected and returned == len(text)
        preview = Image.new('RGB', (96, 16), '#263238')
        preview.putdata([(230, 230, 230) if p else (38, 50, 56) for p in pixels])
        path = ROOT / f'REGION{index}_NATIVE_PREVIEW.png'
        preview.save(path)
        y = 48 + index * 60
        draw.text((12, y), f'{index}: {text.strip()}', font=caption, fill='#dfd3ac')
        sheet.paste(preview.resize((288, 48), Image.Resampling.NEAREST), (280, y))
        previews.append({'index': index, 'English': text, 'native_pointer': pointer,
                         'all96x16_bitmap_pixels_exact': True, 'all_first_final_letters_and_blank_cells_exact': True,
                         'native_returned_bytes': returned, 'complete_foreground_pixels': sum(pixels),
                         'preview': str(path), 'sha256': sha(path.read_bytes())})
    for overlay in loadOverlayTable(rom.rom.arm9OverlayTable, lambda i, f: rom.files[f]).values():
        assert not any(BASE + START <= struct.unpack_from('<I', overlay.data, i)[0] < BASE + END
                       for i in range(len(overlay.data) - 3))
    bad = bytearray(target)
    row = next(r for r in proof['all8_final_name_owners'] if r['index'] == 6)
    bad[row['terminator'] - BASE] = ord('X')
    try:
        validate_names(bad)
    except ValueError:
        pass
    else:
        raise AssertionError('Lost terminator negative control was accepted')
    sheet.save(ROOT / 'ALL8_REGION_NAMES_NATIVE_PREVIEWS.png')
    config.update({'status': 'reviewed-native-previews-experimental', 'source_arm9_sha256': SOURCE,
                   'target_arm9_sha256': sha(target)})
    save(CONFIG, config)
    save(ROOT / 'native_preview_proof.json', {
        **proof, 'old_current_provider_rejected': old_failure,
        'corrupt_terminator_negative_control_rejected': True,
        'native_original_record_getter_and_all8_complete_bitmap_previews': previews,
        'all_overlay_every_byte_alias_census_clear': True,
        'original_legacy_batch_preserved_for_historical_reproduction': 'translations/route_forces_arm9_v1.json',
        'script_sha256': sha(Path(__file__).read_bytes()), 'full_goal_complete': False})
    stack = read('translations/release_stack.json')
    profile = copy.deepcopy(stack['profiles']['all-routes-unified-v636'])
    profile.update({'region_name_boundaries': str(CONFIG), 'status': 'experimental',
                    'description': 'Complete V636 plus complete eight-owner region-name NUL boundaries in existing storage.',
                    'note': 'Americas remains complete;all shared labels have independent terminators. Adjacent integer array, metadata and all other bytes preserved. Actual cold-boot review required.'})
    stack['profiles']['all-routes-unified-v640'] = profile
    save('translations/release_stack.json', stack)
    print('Registered V640:all8 original names fully terminated;native96x16 previews pass;no section/pool growth.')


if __name__ == '__main__':
    main()
