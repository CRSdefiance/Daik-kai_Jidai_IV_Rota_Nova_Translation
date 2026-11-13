"""Research-only original event-still operands for eight village cards; never a release."""

import argparse
import json
import struct
from pathlib import Path

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage

PARENT = Path('out/all_routes_combined_v546_candidate.nds')
OUT = Path('work/analysis/village_card_gpu_v549/fixtures')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--indices', nargs='+', type=int, required=True)
    args = parser.parse_args()
    assert len(set(args.indices)) == len(args.indices) and all(i in (168,169,170,171,206,207,208,209) for i in args.indices)
    OUT.mkdir(parents=True, exist_ok=True)
    parent = NdsImage.open(PARENT)
    digest = sha(PARENT.read_bytes())
    assert digest == '499e0ad767b1badf899ab6873ad787f171651035c7d6316012af2b8afc8c77d3'
    registry = Path('translations/release_stack.json')
    manifest = json.loads(PARENT.with_suffix('.manifest.json').read_text(encoding='utf-8'))
    assert manifest['candidate_sha256'] == digest and len(manifest['batches']) == 470
    before = {p: data for _, p, data in parent.iter_files()} | dict(parent.iter_components())
    path = '/data/SC0.DK4'
    clean = NdsImage.open('work/clean.nds')
    template = IlnkContainer.parse(clean.read_file('/data/SC0.DK4')).blocks[44][30:34]
    assert template == bytes.fromhex('20460180')
    container = IlnkContainer.parse(before[path])
    original = container.blocks[44][30:34]
    assert original == bytes.fromhex('20460180')
    opening = json.loads(Path('work/analysis/movie_gpu_fixture_v336/opening_inputs.json').read_text(encoding='utf-8'))
    (OUT / 'opening_inputs.json').write_text(json.dumps(opening, indent=2) + '\n', encoding='utf-8')
    for index in args.indices:
        data = bytearray(before[path])
        offsets = struct.unpack_from('<344I', data, 8)
        target = offsets[44] + 30
        assert data[target:target + 4] == original
        packet = bytearray(template)
        packet[2] = index
        data[target:target + 4] = packet
        parsed = IlnkContainer.parse(data)
        assert len(parsed.blocks[44]) == len(container.blocks[44])
        assert parsed.blocks[44][:30] == container.blocks[44][:30]
        assert parsed.blocks[44][34:] == container.blocks[44][34:]
        assert all(a == b for i, (a, b) in enumerate(zip(parsed.blocks, container.blocks)) if i != 44)
        fixture = NdsImage.open(PARENT)
        fixture.replace_file(path, bytes(data))
        destination = OUT / f'index{index:03d}_RESEARCH_ONLY.nds'
        assert not destination.exists()
        fixture.save(destination)
        saved = NdsImage.open(destination)
        after = {p: raw for _, p, raw in saved.iter_files()} | dict(saved.iter_components())
        assert before.keys() == after.keys() and [p for p in before if before[p] != after[p]] == [path]
        assert saved.read_file(path) == data
        selected = index
        proof = {'research_only': True, 'not_playable_distribution_or_registered_candidate': True,
                 'parent': str(PARENT), 'parent_sha256': digest,
                 'parent_profile': manifest['profile'], 'release_stack_sha256': sha(registry.read_bytes()),
                 'inherited_batches': len(manifest['batches']),
                 'research_ROM': str(destination), 'research_ROM_sha256': sha(destination.read_bytes()),
                 'only_changed_file': path, 'block': 44, 'block_offset': 30,
                 'original_scene_packet': original.hex(), 'replacement_event_still_packet': bytes(packet).hex(),
                 'template_clean_source': '/data/SC0.DK4 block44 offset30',
                 'template_source_packet': template.hex(), 'requested_image_index': index,
                 'expected_source_image': f'/evstill/evstill{selected:03d}.pxl',
                 'all_instruction_offsets_lengths_route_prose_controls_and_other_files_unchanged': True,
                 'source_event_reachability_or_raw_comic_display_verified': False,
                 'production_ROM_unchanged': True}
        destination.with_suffix('.fixture.json').write_text(json.dumps(proof, indent=2) + '\n', encoding='utf-8')
        print('Prepared research village-card fixture', index, flush=True)
    assert sha(PARENT.read_bytes()) == digest


if __name__ == '__main__':
    main()
