"""Prepare/preview the complete shared heading within existing owned storage."""

import argparse
import copy
import struct
from pathlib import Path

from ndspy.code import MainCodeFile
from PIL import Image
from unicorn.arm_const import UC_ARM_REG_PC, UC_ARM_REG_R8, UC_ARM_REG_SP

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.ship_info_title_crop import NEW_RECT, OLD_RECT, transform
from dk4tool.rom.nds import NdsImage
from scripts.probe_button_prompt_native import BASE, STACK, call, machine
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/ship_title_v633')
CAPTURE = Path('E:/Rota Nova translations/Generated/work/emulation_v193/selection_consumers_v633_current')
CONFIG = Path('translations/ship_info_title_crop_v1.json')


def title_raster(arm, raw, mode):
    u = machine(arm)
    u.mem_write(BASE, raw)
    for section in MainCodeFile(arm, BASE).sections:
        u.mem_write(section.ramAddress, bytes(section.data))
    # Real captured168x84 view/header; identify it through its native header.
    needle = struct.pack('<3I', 4, 42, 84)
    matches = [at for at in range(len(raw) - 20) if raw[at:at + 12] == needle]
    assert len(matches) == 1
    header = BASE + matches[0]
    obj = header - 0x1C38
    pixels = (header + struct.unpack_from('<I', raw, matches[0] + 16)[0]) & 0xFFFFFFFF
    assert pixels == obj + 0xA8
    u.mem_write(pixels, bytes(168 * 84 // 2))
    u.mem_write(obj + 0xA4, struct.pack('<I', mode))
    font_pointer = struct.unpack_from('<I', arm, 0xD5088)[0]
    u.mem_write(font_pointer + 4, struct.pack('<2I', 6, 12))
    ctx = STACK + 0x410
    call(u, 0xD5160, (ctx, obj + 0x10, 1))
    u.reg_write(UC_ARM_REG_SP, STACK)
    u.reg_write(UC_ARM_REG_R8, obj)
    u.emu_start(BASE + 0x19EB4, BASE + 0x19EDC, count=300000)
    assert u.reg_read(UC_ARM_REG_PC) == BASE + 0x19EDC and u.reg_read(UC_ARM_REG_SP) == STACK
    packed = bytes(u.mem_read(pixels, 168 * 84 // 2))
    plane = bytes(n for b in packed for n in (b & 15, b >> 4))
    text_pointer = struct.unpack_from('<I', arm, 0x19F18 if mode else 0x19F1C)[0] - BASE
    text = arm[text_pointer:arm.index(0, text_pointer)].decode('ascii')
    font = GameAsciiFont.from_arm9(arm)
    expected = {(i * 6 + x, 36 + y) for i, char in enumerate(text)
                for y in range(11) for x in range(6) if font.decode(char).getpixel((x, y))}
    assert {(i % 168, i // 168) for i, p in enumerate(plane) if p} == expected
    return plane, text, obj, pixels


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--register', action='store_true')
    args = parser.parse_args()
    ROOT.mkdir(parents=True, exist_ok=True)
    parent = NdsImage.open('out/all_routes_combined_v627_candidate.nds')
    arm = parent.read_file('/__arm9__.bin')
    old = read('work/analysis/deck_explanations_v146_saved_proof.json')
    original = read('translations/deck_explanation_pool_v1.json')
    owners = [{'offset': m['new_offset'], 'text': m['complete_text']} for m in old['moves']]
    by_old = {m['old_offset']: m['new_offset'] for m in old['moves']}
    refs = [{'field': r['field_offset'], 'pointer': BASE + by_old[r['owner_offset']]}
            for r in original['all_byte_position_address_candidates']]
    target, proof = transform(arm, {'owners': owners, 'references': refs})
    (ROOT / 'target_arm9.bin').write_bytes(target)
    raw = (CAPTURE / 'frame_005600_arm9_ram.bin').read_bytes()
    previews = []
    for mode in (0, 1):
        for label, code, rect in (('V627', arm, OLD_RECT), ('V633', target, NEW_RECT)):
            plane, text, obj, pixels = title_raster(code, raw, mode)
            crop = [plane[y * 168 + x] for y in range(36, 48) for x in range(rect[5])]
            expected_ink = sum(bool(p) for p in plane)
            visible_ink = sum(bool(p) for p in crop)
            if label == 'V633':
                assert visible_ink == expected_ink
            elif mode == 0:
                assert expected_ink == 98 and visible_ink == 74
            image = Image.new('RGB', (256, 16), (123, 157, 123))
            for y in range(12):
                for x in range(rect[5]):
                    if crop[y * rect[5] + x]:
                        image.putpixel((rect[1] + x, rect[2] + y), (230, 230, 230))
            path = ROOT / f'{label}_mode{mode}_NATIVE_TITLE_PREVIEW.png'
            image.resize((1024, 64), Image.Resampling.NEAREST).save(path)
            previews.append({'version': label, 'mode': mode, 'text': text, 'title_rect': rect,
                             'complete_cached_ink': expected_ink, 'visible_ink': visible_ink,
                             'source_object': obj, 'source_pixels': pixels,
                             'path': str(path), 'sha256': sha(path.read_bytes())})
    save(ROOT / 'native_preview_proof.json', {'transform': proof, 'previews': previews,
                                            'original_bitmap168x84_all_title_glyphs_retained': True,
                                            'all_other_30_owned_texts_exact': True,
                                            'only_UI_centering_padding_not_new_dialogue': True})
    if args.register:
        save(CONFIG, {'format': 'dk4-ship-info-title-crop-v1', 'status': 'reviewed-native-previews-experimental',
                      'target_arm9_sha256': sha(target), 'plan': {'owners': owners, 'references': refs}})
        registry = read('translations/release_stack.json')
        profile = copy.deepcopy(registry['profiles']['all-routes-unified-v627'])
        profile.update({'ship_info_title_crop': str(CONFIG), 'status': 'experimental',
                        'description': 'Complete V627 plus full shared Ship Info/Refit headings in the existing168x84 bitmap.',
                        'note': 'Title crop widened48 to66 and centered;Refit UI spaces funded by exactly4 source padding bytes. No pool or section growth. Actual cold-boot checks required.'})
        registry['profiles']['all-routes-unified-v633'] = profile
        save('translations/release_stack.json', registry)
        print('Registered V633;native complete title previews pass;ARM9', sha(target))
    else:
        print('Prepared native Ship Info/Refit previews;V627 drops24 cached f/o pixels;V633 preserves complete headings.')


if __name__ == '__main__':
    main()
