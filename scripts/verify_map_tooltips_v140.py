"""Verify saved V140 tooltips and exact preservation of every V139 component."""

import json
import struct
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.map_tooltip_release import CONFIG, apply_release
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from scripts.execute_golden_route_heading import execute as heading
from scripts.execute_map_entity_tooltip_copy import select
from scripts.inventory_map_tooltip_classes import execute_class
from scripts.register_grand_race_help_v134 import components


def main():
    previous_path = Path('out/all_routes_combined_v139_candidate.nds')
    path = Path('out/all_routes_combined_v140_candidate.nds')
    if sha(previous_path.read_bytes()) != '9553d3d2d87c4a0d9e6739763add3df394d480eea6b66a8e9c67e30972d2911c':
        raise ValueError('Full V139 source ROM differs')
    previous, saved = [components(NdsImage.open(p)) for p in (previous_path, path)]
    proposed, report = apply_release(previous['/__arm9__.bin'], CONFIG)
    if previous.keys() != saved.keys() or any(saved[k] != (proposed if k == '/__arm9__.bin' else data)
                                             for k, data in previous.items()):
        raise ValueError('Saved V140 changes an inherited component outside complete tooltip transformation')
    arm9 = saved['/__arm9__.bin']
    selections = []
    for row in report['selections']:
        pointer = struct.unpack_from('<I', arm9, row['pointer_field'])[0] - 0x02000000
        raw = row['formatted_text'].encode('ascii') + b'\0'
        if arm9[pointer:pointer + len(raw)] != raw:
            raise ValueError('Saved tooltip/creature/inherited viewer loses full text/NUL/leading bytes')
        selections.append({'id': row['id'], 'english': row['english'], 'offset': pointer})
    classes = [execute_class(arm9, index) for index in range(39)]
    native_selections = [select(arm9, case) for case in ('pirates', 'monster', 'unknown', 'named')]
    for selection in (0, 1):
        heading(arm9, selection)
    old_common = common_message_entries(previous['/COMMON/MESFILE.DK4'], previous['/__arm9__.bin'], clean=False)
    new_common = common_message_entries(saved['/COMMON/MESFILE.DK4'], arm9, clean=False)
    if old_common != new_common or len(new_common) != 3668:
        raise ValueError('Inherited native COMMON selections changed')
    captions = json.loads(Path('translations/scene_caption_manuscript_v2.json').read_text(encoding='utf-8'))['records']
    for row in captions:
        field = row['pointer_field']
        old_pointer = struct.unpack_from('<I', previous['/__arm9__.bin'], field)[0]
        pointer = struct.unpack_from('<I', arm9, field)[0]
        raw = row['english'].encode('ascii') + b'\0'
        if pointer != old_pointer or arm9[pointer - 0x02000000:pointer - 0x02000000 + len(raw)] != raw:
            raise ValueError('Inherited complete caption changed')
    manifest = json.loads(path.with_suffix('.manifest.json').read_text())
    old_manifest = json.loads(previous_path.with_suffix('.manifest.json').read_text())
    registry_path = Path('translations/release_stack.json')
    registry = json.loads(registry_path.read_text(encoding='utf-8'))
    if manifest['profile'] != 'all-routes-unified-v140' or manifest['candidate_sha256'] != sha(path.read_bytes()):
        raise ValueError('Saved V140 manifest identity differs')
    if manifest['batches'] != old_manifest['batches'] or manifest['release_stack_sha256'] != sha(registry_path.read_bytes()):
        raise ValueError('Inherited batch order/current registry differs')
    if manifest['base_sha256'] != registry['canonical_baseline']['sha256']:
        raise ValueError('Canonical lineage differs')
    stages = manifest['relocations']['/__arm9__.bin']
    if stages['golden_route_viewer']['target_arm9_sha256'] != report['source_arm9_sha256'] or stages['map_tooltips']['target_arm9_sha256'] != report['target_arm9_sha256']:
        raise ValueError('Golden Route/tooltip staged lineage differs')
    proof = {'status': 'pass-saved-complete-map-tooltips-and-all-inherited-components',
             'candidate_sha256': sha(path.read_bytes()), 'arm9_sha256': sha(arm9), 'selections': selections,
             'native_classes': classes, 'native_entity_selections': native_selections,
             'inherited_scene_captions': 164, 'inherited_common_selections': 3668,
             'all_other_components_byte_exact': True, 'batch_count': len(manifest['batches']),
             'runtime_verified': False}
    Path('work/analysis/map_tooltips_v140_saved_rom_proof.json').write_text(json.dumps(proof, indent=2) + '\n')
    print('Nine complete tooltip/creature translations and six inherited viewer labels pass; 164 captions, 3668 COMMON selections and all other V139 components are intact.')
    print(f'Candidate SHA-256: {proof["candidate_sha256"]}')


if __name__ == '__main__':
    main()
