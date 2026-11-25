"""Review complete source names and prepare immutable no-growth UI previews."""

import argparse
import copy
import struct
from pathlib import Path

from PIL import Image
from unicorn.arm_const import UC_ARM_REG_R0

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.patch.commodity_fidelity import BASE, CHANGES, COUNT, TABLE, transform
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.execute_sailing_footer_v317 import execute
from scripts.probe_button_prompt_native import call, machine
from scripts.probe_scene_caption_raster import expected_pixels
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/commodity_fidelity_v635')
CONFIG = Path('translations/commodity_fidelity_v1.json')
MANUSCRIPT = Path('translations/commodity_fidelity_manuscript_v1.json')
FORMAT = 'dk4-commodity-fidelity-v1'
PROFILE = 'all-routes-unified-v635'
NOTES = {
    15: 'Palm oil; retain the distinction from the separate coconut-oil commodity120.',
    20: 'Shark fins as a traded food, with the complete animal and product name.',
    24: 'The spice cinnamon; replace the visibly cut-off legacy abbreviation.',
    40: 'The precious metal platinum; expand the legacy abbreviation.',
    43: 'Finished lacquered utensils/ware, not unprocessed lacquer.',
    47: 'Raw silk thread, distinguished from the separate silk-cloth commodity51.',
    49: 'Cloth woven from wool; retain the material and finished-cloth distinction.',
    50: 'Cloth woven from cotton, distinguished from raw cotton46.',
    52: 'Cloth woven from hemp, distinguished from raw hemp48.',
    60: 'Frankincense, the specific aromatic resin named in Japanese, not generic incense.',
    65: 'Tortoiseshell as the traded decorative material; replace T-Shell with its full name.',
    80: 'The spice/dye turmeric; expand the legacy abbreviation.',
    90: 'Ore containing iron, not refined iron. The original cargo tooltip confirms 鉄鉱石.',
    91: 'Ore containing copper, consistent with iron ore90 and tin ore92.',
    106: 'Whale meat as a food commodity, not the animal. Keep the separate shared Whale string intact.',
    107: 'Black wool; expand B. without adding a species or regional claim.',
    118: 'Smoked salmon. Retain both the named fish and preparation, rather than the adjective Smoked alone.',
}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--register', action='store_true')
    args = parser.parse_args()
    ROOT.mkdir(parents=True, exist_ok=True)
    parent = NdsImage.open('out/all_routes_combined_v633_candidate.nds')
    clean = NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    arm = parent.read_file('/__arm9__.bin')
    packing = read(ROOT / 'packing_plan.json')
    records, manuscript = [], []
    for i in range(COUNT):
        field = TABLE + i * 12
        old, jp = (struct.unpack_from('<I', a, field)[0] - BASE for a in (arm, clean))
        current = arm[old:arm.index(0, old)].decode('ascii')
        japanese = clean[jp:clean.index(0, jp)].decode('cp932')
        english = CHANGES.get(i, (japanese, current))[1]
        row = {'index': i, 'Japanese': japanese, 'current': current, 'English': english}
        records.append(row)
        if i in CHANGES:
            manuscript.append({**row, 'id': 'COMMODITY_COMPLETE_MEANING_' + str(i),
                               'source_name_pointer': BASE + jp, 'source_hex': clean[jp:clean.index(0, jp)].hex(),
                               'context': 'Shared commodity label used by town specialties, Goods Info, Market/Cargo, Price Info and cargo/equipment-name hints.',
                               'source_meaning': NOTES[i],
                               'localization_note': 'Complete natural US English commodity noun;no manual breaks,letter shortening,space padding or invented story facts. Existing game font and full-name consumers are retained. ' + NOTES[i],
                               'review': {'source': True, 'context': True, 'localization': True,
                                          'naturalness': True, 'formatting': args.register}})
    save(MANUSCRIPT, {'format': 'dk4-commodity-fidelity-manuscript-v1', 'target_locale': 'en-US',
                      'clean_ROM_sha256': sha(Path('work/clean.nds').read_bytes()),
                      'records': manuscript, 'other107_labels_preserved_not_newly_semantically_approved': True})
    config = {'format': FORMAT,
              'status': 'reviewed-native-previews-experimental' if args.register else 'native-previews-pending-review',
              'records': records, 'regions': packing['regions'], 'root_offsets': packing['root_offsets'],
              'manuscript': str(MANUSCRIPT), 'manuscript_sha256': sha(MANUSCRIPT.read_bytes()),
              'original_layout_proof': 'work/analysis/commodity_lazy_canvas_v349/plan.json',
              'original_layout_proof_sha256': sha(Path('work/analysis/commodity_lazy_canvas_v349/plan.json').read_bytes())}
    target, proof = transform(arm, clean, config)
    config['target_arm9_sha256'] = sha(target)
    save(CONFIG, config)
    (ROOT / 'target_arm9.bin').write_bytes(target)
    u = machine(target)
    font = GameAsciiFont.from_arm9(target)
    palette = struct.unpack_from('<I', target, 0xD181C)[0] - BASE
    ink_color = struct.unpack_from('<H', target, palette + 2)[0]
    getters, rasters = [], []
    for row in records:
        call(u, 0xCD1AC, (row['index'],))
        record = u.reg_read(UC_ARM_REG_R0)
        assert record == BASE + TABLE + row['index'] * 12
        pointer = struct.unpack('<I', u.mem_read(record, 4))[0]
        text = bytes(u.mem_read(pointer, 64)).split(b'\0')[0].decode('ascii')
        assert text == row['English']
        assert bytes(u.mem_read(record + 4, 8)) == arm[TABLE + row['index'] * 12 + 4:TABLE + row['index'] * 12 + 12]
        getters.append({'index': row['index'], 'complete_name': text, 'actual_native_pointer': pointer,
                        'all_metadata_exact': True})
        for mode in (4, 16):
            result = execute(target, text, x=0, y=72, mode=mode, tracking=0,
                             buffered_context=True, text_entry_offset=0x15BB40, compact_source_origin=True)
            assert result['pixels'] == expected_pixels(target, text, 0, 72, mode, advance=5)
            assert result['context_tracking_after_return'] == 0 and result['final_x'] == len(text) * 5 <= 95
            rasters.append({'index': row['index'], 'mode': mode, 'name': text,
                            'complete_compact_original_font_pixels_exact': True})
        if row['index'] in CHANGES:
            result = execute(target, text, x=0, y=0, mode=16, tracking=0, buffered_context=True, compact_source_origin=True)
            assert result['pixels'] == expected_pixels(target, text, 0, 0, 16, advance=6)
            image = Image.new('RGB', (128, 16), '#eadab3')
            actual_ink = set()
            for y in range(16):
                for x in range(128):
                    if struct.unpack_from('<H', result['pixels'], (y * 256 + x) * 2)[0] == ink_color:
                        actual_ink.add((x, y))
                        image.putpixel((x, y), (0, 8, 0))
            assert actual_ink == {(n * 6 + x, y) for n, c in enumerate(text)
                                  for y in range(11) for x in range(6) if font.decode(c).getpixel((x, y))}
            image.resize((768, 96), Image.Resampling.NEAREST).save(ROOT / f'name_{row["index"]:03d}_NATIVE_PREVIEW.png')
    save(ROOT / 'native_preview_proof.json', {'transform': proof, 'all124_actual_native_getters': getters,
                                            'all248_complete_town_name_rasters': rasters,
                                            'all17_full_width_native_previews': True,
                                            'other_consumers_and_actual_ROM_checks_pending': True})
    if args.register:
        registry = read('translations/release_stack.json')
        profile = copy.deepcopy(registry['profiles']['all-routes-unified-v633'])
        profile.update({'commodity_fidelity': str(CONFIG), 'status': 'experimental',
                        'description': 'Complete V633 plus17 faithful full commodity names in existing exclusively owned source spans;no memory or layout changes.',
                        'note': 'All124 names retain complete strings,metadata and native helpers;12 full suffix aliases,old shared Whale bytes preserved. Native/actual UI verification required.'})
        registry['profiles'][PROFILE] = profile
        save('translations/release_stack.json', registry)
        print('Registered', PROFILE, 'complete commodity fidelity;ARM9', sha(target))
    else:
        print('Prepared17 full-name previews;all124 native getters and248 full compact rasters pass.')


if __name__ == '__main__':
    main()
