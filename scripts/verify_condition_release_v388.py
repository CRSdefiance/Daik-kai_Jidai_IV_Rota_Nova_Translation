"""Verify cumulative release, exact patch, real cold-boot memory and replays."""

import json
import struct
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.verify_fleet_release_v375 import files, match

ROM = Path('out/all_routes_combined_v388_candidate.nds')
ROOT = Path('work/analysis/condition_release_v388')


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def main():
    digest = sha(ROM.read_bytes())
    manifest = read(ROM.with_suffix('.manifest.json'))
    parent = read('out/all_routes_combined_v383_candidate.manifest.json')
    assert manifest['candidate_sha256'] == digest and manifest['profile'] == 'all-routes-unified-v388'
    assert manifest['base_sha256'] == parent['base_sha256'] == (
        '3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe')
    assert manifest['batches'] == parent['batches'] and len(manifest['batches']) == 470
    stack_path = Path('translations/release_stack.json')
    stack = read(stack_path)
    assert manifest['release_stack_sha256'] == sha(stack_path.read_bytes())
    old, new = stack['profiles']['all-routes-unified-v383'], stack['profiles']['all-routes-unified-v388']
    assert all(new[k] == v for k, v in old.items() if k not in ('note', 'description'))
    assert set(new) - set(old) == {'condition_labels'}
    a, b = files(NdsImage.open('out/all_routes_combined_v383_candidate.nds')), files(NdsImage.open(ROM))
    assert a.keys() == b.keys()
    assert [n for n in a if a[n] != b[n]] == ['/__arm9__.bin']
    assert b['/__arm9__.bin'] == Path('work/analysis/condition_labels_v387/research_arm9.bin').read_bytes()
    assert ROM.read_bytes() == Path('work/analysis/condition_labels_v387/research_only_conditions.nds').read_bytes()
    assert ROM.read_bytes() == (ROOT / 'patch_reconstruction.nds').read_bytes()
    captures = {}
    for before, after in [('tavern_new_game_v383', 'conditions_new_game_v388'),
                          ('plaque_voyage_v379', 'conditions_sailors_v388')]:
        captures[after] = match(Path('work/emulation_v193') / before,
                               Path('work/emulation_v193') / after, digest)
    report = read('work/emulation_v193/conditions_new_game_v388/capture_report.json')
    exported = report['read_only_native_state']
    assert exported['read_only_export'] and not exported['state_loaded']
    region = exported['regions']['ITCM']
    tcm = Path(region['path']).read_bytes()
    assert len(tcm) == 32768 and sha(tcm) == region['sha256']
    snapshot = report['read_only_RAM_snapshot']
    ram = Path(snapshot['path']).read_bytes()
    assert sha(ram) == snapshot['sha256'] and snapshot['read_only_export']
    labels = []
    config = read('translations/condition_labels_v1.json')
    for row in config['pointer_changes']:
        pointer = struct.unpack_from('<I', ram, row['field'])[0]
        assert pointer == row['new_pointer']
        address = pointer & 0x7FFF if pointer < 0x02000000 else pointer - 0x02000000
        memory = tcm if pointer < 0x02000000 else ram
        text = memory[address:].split(b'\0', 1)[0].decode()
        assert text == row['English']
        labels.append({'field': row['field'], 'runtime_pointer': pointer, 'runtime_text': text})
    plaques = read('translations/graphics_completion_campaign_v1.json')['plaque_style_v247']['ongoing_plaque_inventory']
    assert len(plaques) == 18 and all(not p['fully_completed'] for p in plaques)
    proof = {'candidate': str(ROM), 'candidate_sha256': digest, 'profile': manifest['profile'],
             'base': manifest['base_rom'], 'base_sha256': manifest['base_sha256'],
             'patch_sha256': sha(ROM.with_suffix('.xdelta').read_bytes()),
             'exact_clean_patch_reconstruction': True, 'all470_batches_and_all_V383_stages_retained': True,
             'only_ARM9_changed_all_graphics_COMMON_routes_and_other_components_exact': True,
             'actual_final_ROM_unchanged_replay_frames': captures,
             'actual_cold_boot_runtime_pointers_and_loaded_strings': labels,
             'native_selector_and_complete_raster_proof': 'work/analysis/condition_labels_v387/native_proof.json',
             'alternate_new_condition_gameplay_states_not_observed': True,
             'all18_plaques_incomplete': True, 'full_goal_complete': False,
             'status': 'experimental', 'canonical_promotion': False}
    (ROOT / 'release_proof.json').write_text(json.dumps(proof, indent=2) + '\n', encoding='utf-8')
    print(f'V388: exact patch, all inherited layers, runtime strings and {sum(captures.values())} unchanged final-ROM frames pass.')


if __name__ == '__main__':
    main()
