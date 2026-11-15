"""Complete palette-normalized correspondence test for two distinct portrait stores."""

import json
import struct
from pathlib import Path

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage

ROM = Path('out/all_routes_combined_v474_candidate.nds')
ROOT = Path('work/analysis/slack_portraits_v480')


def cells(raw):
    assert len(raw) == 512 + 178 * 3584
    palette = [struct.pack('<H', word & 0x7FFF) for word in struct.unpack('<256H', raw[:512])]
    rows = []
    for index in range(178):
        offset = 512 + index * 3584
        indices = raw[offset:offset + 3584]
        colour = b''.join(palette[value] for value in indices)
        rows.append({'cell': index, 'byte_offset': offset, 'index_bytes': 3584,
                     'index_sha256': sha(indices), 'lower15_colour_sha256': sha(colour)})
    assert raw[:512] + b''.join(raw[r['byte_offset']:r['byte_offset'] + 3584] for r in rows) == raw
    return rows


def main():
    ROOT.mkdir(parents=True, exist_ok=True)
    rom, clean = NdsImage.open(ROM), NdsImage.open('work/clean.nds')
    arm, source_arm = rom.read_file('/__arm9__.bin'), clean.read_file('/__arm9__.bin')
    for begin, end in [(0x47A28, 0x47A94), (0x47B3C, 0x47B78)]:
        assert arm[begin:end] == source_arm[begin:end]
    legacy = IlnkContainer.parse(rom.read_file('/GRP/CMMNIMG.DK4')).blocks[0]
    source_legacy = IlnkContainer.parse(clean.read_file('/GRP/CMMNIMG.DK4')).blocks[0]
    native = rom.read_file('/GRP/CMMNIMG.000')
    assert legacy == source_legacy and native == clean.read_file('/GRP/CMMNIMG.000')
    assert legacy != native and len(legacy) == len(native) == 638464
    a, b = cells(legacy), cells(native)
    matches = [{'legacy_cell': x['cell'], 'native_cell': y['cell']}
               for x in a for y in b if x['lower15_colour_sha256'] == y['lower15_colour_sha256']]
    assert not matches
    reviewed = json.loads(Path('work/qa/embedded_raw_v176/portrait13/inventory.json').read_text(encoding='utf-8'))
    slack = IlnkContainer.parse(rom.read_file('/GRP/SLACKIMG.DK4')).blocks[13]
    assert sha(slack) == reviewed['source_block_sha256'] and len(reviewed['records']) == 42
    assert slack == IlnkContainer.parse(clean.read_file('/GRP/SLACKIMG.DK4')).blocks[13]
    proof = {'candidate': str(ROM), 'candidate_sha256': sha(ROM.read_bytes()), 'ROM_changed': False,
             'legacy_source_block_sha256': sha(legacy), 'native_source_file_sha256': sha(native),
             'original_native_reader_palette_prefix_bytes': 512, 'original_native_reader_face_stride_bytes': 3584,
             'original_reader_code_ranges_unchanged': [[0x47A28, 0x47A94], [0x47B3C, 0x47B78]],
             'legacy_cell_geometry_is_reviewed_storage_hypothesis_not_native_binding': True,
             'all178_legacy_cells': a, 'all178_native_store_cells': b,
             'all31684_complete_colour_hash_pairs_compared': True, 'complete_colour_matches': matches,
             'same_byte_length_not_used_as_equivalence_proof': True,
             'comparison_ignores_alpha_bit_and_does_not_prove_alpha_or_gameplay': True,
             'SLACK13_existing42_portrait_review_revalidated_not_new_clearance': {
                 'report': 'work/qa/embedded_raw_v176/portrait13/inventory.json',
                 'report_sha256': sha(Path('work/qa/embedded_raw_v176/portrait13/inventory.json').read_bytes()),
                 'source_block_sha256': sha(slack), 'Latin_El_Gato_clothing_text_retained': True},
             'original_legacy_consumers_and_palette_relationships_remain_open': True,
             'all22_historical_requirements_retained': True, 'all18_plaques_incomplete': True, 'full_goal_complete': False}
    (ROOT / 'correspondence_proof.json').write_text(json.dumps(proof, indent=2) + '\n', encoding='utf-8')
    print('178x178 full colour comparisons yield no exact legacy/native face match;source stores remain distinct.')


if __name__ == '__main__':
    main()
