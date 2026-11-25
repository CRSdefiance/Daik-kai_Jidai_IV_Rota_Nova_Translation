"""Bounded original-image instruction fixtures; never playable release candidates."""
import argparse
import json
import struct
from pathlib import Path

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage

ROOT = Path('work/analysis/name_gradients_v558')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--version', type=int, choices=(557, 558), required=True)
    version = parser.parse_args().version
    parent_path = Path(f'out/all_routes_combined_v{version}_candidate.nds')
    parent = NdsImage.open(parent_path)
    before = {p: d for _, p, d in parent.iter_files()} | dict(parent.iter_components())
    clean = NdsImage.open('work/clean.nds')
    template = IlnkContainer.parse(clean.read_file('/data/SC1.DK4')).blocks[296][12:16]
    assert template == bytes.fromhex('304808ab')
    script = before['/data/SC0.DK4']
    container = IlnkContainer.parse(script)
    assert container.blocks[44][30:34] == bytes.fromhex('20460180')
    offset = struct.unpack_from('<I', script, 8 + 44 * 4)[0] + 30
    for index in (12, 19):
        replacement = bytearray(template)
        replacement[2] = index
        patched = bytearray(script)
        patched[offset:offset + 4] = replacement
        assert patched[:offset] == script[:offset] and patched[offset + 4:] == script[offset + 4:]
        fixture = NdsImage.open(parent_path)
        fixture.replace_file('/data/SC0.DK4', bytes(patched))
        target = ROOT / f'V{version}_index{index}_RESEARCH_ONLY.nds'
        assert not target.exists()
        fixture.save(target)
        saved = NdsImage.open(target)
        after = {p: d for _, p, d in saved.iter_files()} | dict(saved.iter_components())
        assert before.keys() == after.keys() and [p for p in before if before[p] != after[p]] == ['/data/SC0.DK4']
        proof = {'research_only': True, 'not_playable_distribution': True, 'parent': str(parent_path),
                 'parent_sha256': sha(parent_path.read_bytes()), 'fixture': str(target),
                 'fixture_sha256': sha(target.read_bytes()), 'index': index,
                 'only_changed_file': '/data/SC0.DK4', 'block': 44, 'block_offset': 30,
                 'replacement': bytes(replacement).hex(), 'all_other_bytes_and_art_exact_parent': True}
        target.with_suffix('.fixture.json').write_text(json.dumps(proof, indent=2) + '\n', encoding='utf-8')
    original_inputs = json.loads(Path('work/analysis/movie_gpu_fixture_v336/opening_inputs.json').read_text(encoding='utf-8'))
    inputs = [e for e in original_inputs if e['start'] <= 4800]
    (ROOT / 'native_inputs.json').write_text(json.dumps(inputs, indent=2) + '\n', encoding='utf-8')
    (ROOT / 'fresh_inputs.json').write_bytes(Path('work/analysis/ship_plaque_release_v557/fresh_inputs.json').read_bytes())
    print(f'Prepared V{version} research source-opcode fixtures12/19; production ROM unchanged.')


if __name__ == '__main__':
    main()
