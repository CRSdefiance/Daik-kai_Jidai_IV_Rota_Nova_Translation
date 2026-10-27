"""Verify every saved caption and all inherited full-ROM components."""

import json
import struct
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.scene_caption_release import CONFIG, MANUSCRIPT, TARGET_SHA, apply_release
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from scripts.execute_scene_caption_selection import execute
from scripts.register_grand_race_help_v134 import components

TABLES = (0x115CAC, 0x115A04, 0x115968, 0x115834)
COUNTS = (46, 41, 39, 38)


def main():
    path = Path('out/all_routes_combined_v138_candidate.nds')
    previous_path = Path('out/all_routes_combined_v137_candidate.nds')
    if sha(previous_path.read_bytes()) != '985c99f003a975d7512c249f09a13008f19ed15bb5f533d5c8f1747e6bca19fb':
        raise ValueError('Full V137 reference changed')
    previous, saved = [components(NdsImage.open(p)) for p in (previous_path, path)]
    proposed, release_report = apply_release(previous['/__arm9__.bin'], CONFIG)
    if previous.keys() != saved.keys():
        raise ValueError('Full ROM component identities differ')
    for name, data in previous.items():
        if saved[name] != (proposed if name == '/__arm9__.bin' else data):
            raise ValueError(f'Unexpected inherited component change: {name}')
    arm9 = saved['/__arm9__.bin']
    if sha(arm9) != TARGET_SHA:
        raise ValueError('Saved native caption target differs')
    rows = json.loads(MANUSCRIPT.read_text(encoding='utf-8'))['records']
    cases = []
    for row in rows:
        field = row['pointer_field']
        pointer = struct.unpack_from('<I', arm9, field)[0]
        offset = pointer - 0x02000000
        raw = row['english'].encode('ascii') + b'\0'
        if not 0 <= offset < len(arm9) or arm9[offset:offset + len(raw)] != raw:
            raise ValueError('Saved full caption loses leading/last bytes or NUL')
        route, index = row['route_index'], row['index']
        result = execute(arm9, TABLES[route], index, COUNTS[route], advance=5)
        if bytes.fromhex(result['full_text_hex']) != raw or result['pointer'] != pointer:
            raise ValueError('Saved native caption consumer differs')
        cases.append({'id': row['id'], 'pointer': pointer, 'x': result['x'], 'y': result['y']})
    old_common = common_message_entries(previous['/COMMON/MESFILE.DK4'], previous['/__arm9__.bin'], clean=False)
    new_common = common_message_entries(saved['/COMMON/MESFILE.DK4'], arm9, clean=False)
    if old_common != new_common or len(new_common) != 3668:
        raise ValueError('Inherited native COMMON selections changed')
    manifest = json.loads(path.with_suffix('.manifest.json').read_text())
    registry = Path('translations/release_stack.json')
    stack = json.loads(registry.read_text(encoding='utf-8'))
    if manifest['profile'] != 'all-routes-unified-v138' or manifest['candidate_sha256'] != sha(path.read_bytes()):
        raise ValueError('Saved full candidate manifest differs')
    if manifest['release_stack_sha256'] != sha(registry.read_bytes()):
        raise ValueError('Saved caption profile registry differs')
    expected_batches = stack['profiles']['all-routes-unified-v138']['batches']
    if [Path(p).as_posix() for p in manifest['batches']] != [Path(p).as_posix() for p in expected_batches]:
        raise ValueError('Preceding complete batch sequence changed')
    prior_manifest = json.loads(previous_path.with_suffix('.manifest.json').read_text())
    if manifest['batches'] != prior_manifest['batches']:
        raise ValueError('Actual inherited V137 batch sequence changed')
    if manifest['base_sha256'] != stack['canonical_baseline']['sha256']:
        raise ValueError('Canonical base lineage differs')
    if manifest['relocations']['/__arm9__.bin']['target_arm9_sha256'] != TARGET_SHA:
        raise ValueError('Native caption stage absent from saved manifest')
    report = {'status': 'pass-complete-saved-caption-rom-and-inherited-components',
              'candidate_sha256': sha(path.read_bytes()), 'arm9_sha256': sha(arm9),
              'caption_count': 164, 'cases': cases, 'batch_count': len(manifest['batches']),
              'inherited_common_selections': 3668, 'all_other_components_byte_exact': True,
              'release': release_report, 'runtime_verified': False}
    Path('work/analysis/scene_caption_v138_saved_rom_proof.json').write_text(json.dumps(report, indent=2) + '\n')
    print(f'All 164 saved captions and 3668 inherited COMMON selections pass; {len(manifest["batches"])} batches; all other components byte-exact.')
    print(f'Candidate SHA-256: {report["candidate_sha256"]}')


if __name__ == '__main__':
    main()
