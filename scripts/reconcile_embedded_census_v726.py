"""Bind prior numeric-container evidence to current ROM and account for all57 blocks."""

import struct
from pathlib import Path

from ndspy.code import MainCodeFile

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.research_embedded_structures_v190 import paired_sections
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/embedded_census_v726')
ROM = Path('out/all_routes_combined_v712_candidate.nds')
SELECT = Path('work/analysis/self_relative_character_tables_v192.json')
DECODE = Path('work/analysis/native_compression_v192.json')
TYPED = Path('work/analysis/embedded_sync_v725/storage_proof.json')
LEGACY = Path('work/analysis/legacy_owners_v719/source_carry_forward.json')


def main():
    ROOT.mkdir(parents=True, exist_ok=True)
    assert not (ROOT / 'proof.json').exists()
    current = NdsImage.open(ROM)
    canonical_path = Path('out/raphael_natural_v2_accepted_base.nds')
    canonical = NdsImage.open(canonical_path)
    release = {str(p): sha(p.read_bytes()) for p in (ROM, ROM.with_suffix('.manifest.json'),
        ROM.with_suffix('.xdelta'), Path('translations/release_stack.json'), canonical_path)}
    assert release[str(ROM)] == '6534e5619673ea6bdffa3a2342622b99ef393bef52ef58cac131ee94ae0f4030'
    selected, decoded, typed, legacy = [read(p) for p in (SELECT, DECODE, TYPED, LEGACY)]
    assert typed['candidate_sha256'] == legacy['candidate_sha256'] == release[str(ROM)]
    arm, original = [r.read_file('/__arm9__.bin') for r in (current, canonical)]
    prefix = decoded['canonical_IWRAM_prefix_bytes']
    code = next(bytes(s.data) for s in MainCodeFile(arm, 0x02000000).sections if s.ramAddress == 0x01FF8000)
    old = next(bytes(s.data) for s in MainCodeFile(original, 0x02000000).sections if s.ramAddress == 0x01FF8000)
    assert len(old) == prefix == 6944
    assert code[:prefix] == old and sha(old) == decoded['canonical_IWRAM_prefix_sha256']
    assert sha(arm[0x8A10:0x8A2C]) == selected['native_selector_code_sha256']
    ranges = selected['native_descriptor_parser_ranges_identical_to_canonical']
    assert all(sha(arm[r['start_offset']:r['end_exclusive']]) == r['sha256'] for r in ranges)
    blocks = IlnkContainer.parse(current.read_file('/GRP/CHARA.DK4')).blocks
    original_blocks = IlnkContainer.parse(canonical.read_file('/GRP/CHARA.DK4')).blocks
    decoded_rows = {r['block_index']: r for r in decoded['results'] if r['path'] == '/GRP/CHARA.DK4'}
    containers, controls, selections = [], 0, 0
    for row in selected['containers']:
        index = row['block_index']
        assert row['path'] == '/GRP/CHARA.DK4' and 4 <= index <= 13
        assert blocks[index] == original_blocks[index]
        assert sha(blocks[index]) == row['source_block_sha256']
        if index in (4, 5):
            d = decoded_rows[index]
            assert d['native_decompression_pass'] and d['source_sha256'] == sha(blocks[index])
            data = Path(d['decoded']).read_bytes()
            assert len(data) == d['output_bytes'] and sha(data) == d['decoded_sha256']
        else:
            data = blocks[index]
        assert sha(data) == row['container_sha256']
        parsed = paired_sections(data)
        assert parsed == row['corrected_self_relative_structure']
        assert parsed['whole_block_roundtrip_exact']
        observed = []
        for group_index, group in enumerate(parsed['groups']):
            for number, relative in enumerate(group['relative_offsets']):
                payload = group['payloads'][number]
                offset = group['table_start'] + relative
                assert sha(data[offset:offset + payload['bytes']]) == payload['sha256']
                observed.append({'group': group_index, 'record': number, 'offset': offset, 'bytes': payload['bytes']})
        assert observed == row['native_selections']
        selections += len(observed)
        words_seen = 0
        for number, (parts, control) in enumerate(zip(parsed['groups'][0]['payloads'], parsed['groups'][1]['payloads'], strict=True)):
            assert parts['bytes'] % 4 == 0 and control['bytes'] % 2 == 0
            offset = parsed['groups'][1]['table_start'] + parsed['groups'][1]['relative_offsets'][number]
            words = struct.unpack_from(f'<{control["bytes"] // 2}H', data, offset)
            assert all((word & 0xFFF) + ((word >> 12) & 7) + 1 <= parts['bytes'] // 4 for word in words)
            words_seen += len(words)
        controls += words_seen
        containers.append({'path': row['path'], 'block': index, 'current_block_sha256': sha(blocks[index]),
            'decoded_or_plain_container_sha256': sha(data), 'paired_records': parsed['paired_records'],
            'historical_native_selection_payloads_exact_current': len(observed),
            'complete_numeric_control_words_bounded': words_seen,
            'whole_container_numeric_tables_and_payloads_reconstruct_exact': True,
            'source_and_all_original_decoder_selector_parser_dependencies_exact': True,
            'pixel_atlas_binding_and_ordinary_actor_display_not_inferred': True})
    assert len(containers) == 10 and selections == selected['native_selections'] == 406
    assert sum(r['paired_records'] for r in containers) == selected['paired_records'] == 203
    assert controls == selected['bounded_native_control_words'] == 8727
    all_blocks = {(r['path'], r['block']): r for r in typed['all57_block_extents_source_exact']}
    kinds = {}
    for row in typed['all31_type16_images_with_source_headers_and_palettes']:
        kinds[row['path'], row['block']] = 'bounded-type16-image-source-review-complete'
    for row in typed['three_split_palette_pixel_pairs']:
        for number in (row['palette_block'], row['pixels_block']):
            assert (row['path'], number) not in kinds
            kinds[row['path'], number] = 'external-palette-pixel-storage-source-review-complete'
    for row in containers:
        assert (row['path'], row['block']) not in kinds
        kinds[row['path'], row['block']] = 'native-numeric-actor-frame-descriptor'
    for row in legacy['eleven_reviewed_legacy_storage_interpretations']:
        pair = row['path'], row['block']
        assert pair not in kinds and all_blocks[pair]['current_sha256'] == row['current_sha256']
        kinds[pair] = 'reviewed-raw-interpretations-native-format-and-consumers-unresolved'
    assert kinds.keys() == all_blocks.keys() and len(kinds) == 57
    census = []
    for path, block in sorted(kinds):
        actual = IlnkContainer.parse(current.read_file(path)).blocks[block]
        record = all_blocks[path, block]
        assert sha(actual) == record['current_sha256'] and len(actual) == record['bytes']
        census.append({**record, 'current_storage_classification': kinds[path, block]})
    proof = {'candidate': str(ROM), 'candidate_sha256': release[str(ROM)],
        'historical_evidence_bound_by_current_data_code_and_payload_hashes': {
            str(p): sha(p.read_bytes()) for p in (SELECT, DECODE, TYPED, LEGACY)},
        'canonical6944_byte_IWRAM_prefix_exact_current': {'bytes': prefix, 'sha256': sha(old)},
        'native_selector_source_exact': {'address': 0x02008A10, 'sha256': selected['native_selector_code_sha256']},
        'native_descriptor_parser_ranges_source_exact': ranges,
        'ten_current_numeric_containers': containers, 'all57_current_block_census': census,
        'all203_record_pairs406_historical_native_selections8727_numeric_controls_bound_to_current': True,
        'numeric_metadata_not_additional_raster_or_dialogue_to_localize': True,
        'eleven_raw_interpretations_not_promoted_to_proved_native_format': True,
        'no_new_native_execution_or_actor_atlas_palette_GPU_scene_claim': True,
        'producer_sha256': sha(Path(__file__).read_bytes()), 'release_hashes_unchanged': release,
        'full_goal_complete': False}
    for path, digest in release.items():
        assert sha(Path(path).read_bytes()) == digest
    save(ROOT / 'proof.json', proof)
    print('V726: ten current numeric containers bound;203 pairs,406 prior native selections,8727 controls;all57 blocks accounted,11 raw native formats remain open.')


if __name__ == '__main__':
    main()
