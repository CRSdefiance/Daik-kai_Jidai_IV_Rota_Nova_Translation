"""Verify all saved viewer labels and every inherited V138 ROM component."""

import json
import struct
from pathlib import Path

from dk4tool.patch.golden_route_viewer_release import CONFIG, apply_release
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from scripts.execute_golden_route_empty_copy import execute as empty_copy
from scripts.execute_golden_route_heading import execute as heading
from scripts.execute_scene_caption_raster import execute as raster
from scripts.prepare_golden_route_viewer import MANUSCRIPT
from scripts.register_grand_race_help_v134 import components


def main():
    previous_path = Path('out/all_routes_combined_v138_candidate.nds')
    path = Path('out/all_routes_combined_v139_candidate.nds')
    if sha(previous_path.read_bytes()) != '9dd7d66ad3604c8fc2321ce07ba23c8f1dd1d010d86ff7db5a5d2751c49cde1d':
        raise ValueError('Full V138 source ROM differs')
    previous, saved = [components(NdsImage.open(p)) for p in (previous_path, path)]
    proposed, report = apply_release(previous['/__arm9__.bin'], CONFIG)
    if previous.keys() != saved.keys():
        raise ValueError('Saved ROM component identities changed')
    for name, data in previous.items():
        if saved[name] != (proposed if name == '/__arm9__.bin' else data):
            raise ValueError(f'Unexpected inherited component change: {name}')
    arm9 = saved['/__arm9__.bin']
    document = json.loads(MANUSCRIPT.read_text(encoding='utf-8'))
    cases = []
    for row in document['records']:
        pointer = struct.unpack_from('<I', arm9, row['pointer_field'])[0]
        offset = pointer - 0x02000000
        raw = row['english'].encode('ascii') + b'\0'
        if not 0 <= offset < len(arm9) or arm9[offset:offset + len(raw)] != raw:
            raise ValueError('Saved complete viewer label loses leading/last bytes/NUL')
        cases.append({'id': row['id'], 'pointer': pointer, 'english': row['english']})
    for mode in (0, 1):
        heading(arm9, mode)
    empty_copy(arm9)
    empty_copy(arm9, count=1)
    for table in (0x12EC10, 0x12EC28, 0x12EC3C):
        footer = raster(arm9, 'unused', footer_table=table, mode=4)
        if footer['footer_labels'] != list(struct.unpack_from('<6I', arm9, table)):
            raise ValueError('Saved native footer transfer differs')
    old_common = common_message_entries(previous['/COMMON/MESFILE.DK4'], previous['/__arm9__.bin'], clean=False)
    new_common = common_message_entries(saved['/COMMON/MESFILE.DK4'], arm9, clean=False)
    if old_common != new_common or len(new_common) != 3668:
        raise ValueError('Inherited native COMMON selections changed')
    # Preserve every complete native caption selection as well as its string.
    captions = json.loads(Path('translations/scene_caption_manuscript_v2.json').read_text(encoding='utf-8'))['records']
    for row in captions:
        field = row['pointer_field']
        old_pointer = struct.unpack_from('<I', previous['/__arm9__.bin'], field)[0]
        pointer = struct.unpack_from('<I', arm9, field)[0]
        raw = row['english'].encode('ascii') + b'\0'
        if pointer != old_pointer or arm9[pointer - 0x02000000:pointer - 0x02000000 + len(raw)] != raw:
            raise ValueError('Inherited complete scene caption changed')
    manifest = json.loads(path.with_suffix('.manifest.json').read_text())
    old_manifest = json.loads(previous_path.with_suffix('.manifest.json').read_text())
    registry_path = Path('translations/release_stack.json')
    registry = json.loads(registry_path.read_text(encoding='utf-8'))
    if manifest['profile'] != 'all-routes-unified-v139' or manifest['candidate_sha256'] != sha(path.read_bytes()):
        raise ValueError('Saved V139 manifest lineage differs')
    if manifest['batches'] != old_manifest['batches'] or manifest['release_stack_sha256'] != sha(registry_path.read_bytes()):
        raise ValueError('Inherited batch order/current registry differs')
    if manifest['base_sha256'] != registry['canonical_baseline']['sha256']:
        raise ValueError('Canonical base lineage differs')
    stages = manifest['relocations']['/__arm9__.bin']
    if stages['target_arm9_sha256'] != report['source_arm9_sha256'] or stages['golden_route_viewer']['target_arm9_sha256'] != report['target_arm9_sha256']:
        raise ValueError('Caption/Golden Route staged lineage differs')
    proof = {'status': 'pass-complete-saved-golden-route-viewer-and-all-inherited-components',
             'candidate_sha256': sha(path.read_bytes()), 'arm9_sha256': sha(arm9), 'cases': cases,
             'all_other_components_byte_exact': True, 'inherited_common_selections': 3668,
             'inherited_scene_captions': 164, 'batch_count': len(manifest['batches']), 'runtime_verified': False}
    Path('work/analysis/golden_route_viewer_v139_saved_rom_proof.json').write_text(json.dumps(proof, indent=2) + '\n')
    print('All six saved viewer labels/native consumers pass; all 164 captions, 3668 COMMON selections and other components are intact.')
    print(f'Candidate SHA-256: {proof["candidate_sha256"]}')


if __name__ == '__main__':
    main()
