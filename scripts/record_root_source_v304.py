"""Current root-image source preservation and unresolved comic-mark dossier."""

import json
import struct
from pathlib import Path

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.graphics.fls import FlsArchive
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage

ROOT = Path('work/analysis/root_fls_v304')


def main():
    current = NdsImage.open('out/all_routes_combined_v303_candidate.nds')
    clean = NdsImage.open('work/clean.nds')
    raw = current.read_file('/m02_03.fls')
    assert raw == clean.read_file('/m02_03.fls')
    a = FlsArchive(raw)
    t = a.texture(0)
    assert a.to_bytes() == raw and (t.width, t.height) == (512, 512)
    copies, inspected = [], 0
    for _, path, source in current.iter_files():
        if not path.lower().endswith('.fls'):
            continue
        f = FlsArchive(source)
        for index in range(f.count):
            s = f.texture(index)
            inspected += 1
            if (t.width, t.height, t.palette, bytes(t.indices)) == (s.width, s.height, s.palette, bytes(s.indices)):
                copies.append([path, index])
    assert copies == [['/m02_03.fls', 0]] and inspected == 261
    source = IlnkContainer.parse(clean.read_file('/GRP/SLACKIMG.DK4')).blocks[19]
    saved = IlnkContainer.parse(current.read_file('/GRP/SLACKIMG.DK4')).blocks[19]
    assert len(source) == len(saved) == 21 * 320 * 240 * 2
    retained = []
    for box in ((182, 104, 205, 126), (207, 111, 227, 137)):
        def crop(data, box=box):
            start = 6 * 320 * 240 * 2
            return b''.join(data[start + (y * 320 + box[0]) * 2:start + (y * 320 + box[2]) * 2]
                            for y in range(box[1], box[3]))
        original, actual = crop(source), crop(saved)
        assert original == actual
        retained.append({'box': list(box), 'source_BGR555_sha256': sha(original), 'pixels': len(actual) // 2,
                         'all_retained_water_mark_and_adjacent_source_pixels_exact': True})
    assert struct.unpack_from('<I', raw)[0] & 0x80 == 0
    proof = {'format': 'dk4-root-source-and-retained-mark-review-v304',
             'candidate': str(current.source), 'candidate_sha256': sha(current.source.read_bytes()),
             'root_path': '/m02_03.fls', 'root_file_sha256': sha(raw),
             'all_root_source_metadata_palette_indices_and_padding_exact_clean': True,
             'root_dimensions': [512, 512], 'root_visible_height_word': a.records[0][1] & 65535,
             'root_palette_entries': len(t.palette), 'root_palette_and_all262144_pixels_accounted': True,
             'root_roundtrip_exact': True, 'full_root_source_visually_reviewed': True,
             'root_content_decision': 'Retain original coastal scenery and padding; no readable Japanese caption or instruction observed.',
             'exact_decoded_copy_cases_in_all261_FLS_textures': copies,
             'M20_whole_texture_copy_and_regular128_tile_correspondence_not_established': True,
             'no_synchronization_or_root_native_consumer_claim': True,
             'retained_brown_mark_source_regions': retained,
             'consecutive_source_panels6_7_8_9_visually_compared': True,
             'brown_mark_reading_or_anatomical_interpretation_still_unproved': True,
             'primary_publisher_search_did_not_supply_mark_or_creator_interpretation': True,
             'source_search_queries': ['"大航海時代IV" "闘牛士" "うみうし"', '"大航海時代IV" "ウミウシ" イラスト'],
             'all11_legacy_native_layout_and_composition_gates_still_open': True,
             'ROM_modified': False, 'full_goal_complete': False}
    (ROOT / 'source_proof.json').write_text(json.dumps(proof, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print('Root262144 pixels/source palette exact; all261 FLS copies checked; both retained brown-mark regions source-exact; interpretation pending.')


if __name__ == '__main__':
    main()
