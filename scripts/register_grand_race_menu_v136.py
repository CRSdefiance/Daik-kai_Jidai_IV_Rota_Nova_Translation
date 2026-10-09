"""Reconstruct the complete transform input and register the full V136 profile."""

import argparse
import copy
import json
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.register_grand_race_help_v134 import components, patched_arm9, write

BATCH = 'translations/grand_race_menu_arm9_v2.json'
INPUT_PROFILE = 'all-routes-v119-transition-status-input-v136'
INPUT = 'out/all_routes_v119_transition_status_input_v136.nds'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--final', action='store_true')
    args = parser.parse_args()
    stack_path = Path('translations/release_stack.json')
    stack = json.loads(stack_path.read_text(encoding='utf-8'))
    old = json.loads(Path('translations/common_native_reblocking_v135.json').read_text(encoding='utf-8'))
    batch = json.loads(Path(BATCH).read_text(encoding='utf-8'))
    if not args.final:
        profile = copy.deepcopy(stack['profiles']['all-routes-v119-transition-status-input-v135'])
        if BATCH in profile['batches']:
            raise ValueError('Menu batch is already inherited')
        profile['batches'].append(BATCH)
        profile['note'] = 'Complete V135 transform input plus six reviewed complete menu labels. Experimental input only for V136.'
        stack['profiles'][INPUT_PROFILE] = profile
        write(stack_path, stack)
        print('Registered complete V136 transform input.')
        return
    previous = components(NdsImage.open(old['parent_candidate']))
    current_image = NdsImage.open(INPUT)
    current = components(current_image)
    if previous.keys() != current.keys():
        raise ValueError('Transform input file identities differ')
    for path, data in previous.items():
        expected = patched_arm9(data, batch) if path == '/__arm9__.bin' else data
        if current[path] != expected:
            raise ValueError(f'Transform input changed outside menu spans: {path}')
    if sha(current['/COMMON/MESFILE.DK4']) != old['parent_common_sha256']:
        raise ValueError('COMMON transform input changed')
    config = copy.deepcopy(old)
    config['parent_candidate'] = INPUT
    config['parent_arm9_sha256'] = sha(current['/__arm9__.bin'])
    prior_final = NdsImage.open('out/all_routes_combined_v135_candidate.nds').read_file('/__arm9__.bin')
    config['expected_arm9_sha256'] = sha(patched_arm9(prior_final, batch))
    config_path = 'translations/common_native_reblocking_v136.json'
    write(config_path, config)
    profile = copy.deepcopy(stack['profiles']['all-routes-unified-v135'])
    profile['batches'].append(BATCH)
    profile['common_native_reblocking'] = config_path
    profile['note'] = 'All V135 route/UI/graphics/shared-text layers plus six complete native menu labels. Experimental; runtime acceptance pending.'
    stack['profiles']['all-routes-unified-v136'] = profile
    write(stack_path, stack)
    write('work/analysis/grand_race_menu_v136_input_proof.json', {
        'input': INPUT, 'input_sha256': sha(Path(INPUT).read_bytes()),
        'previous_input': old['parent_candidate'],
        'all_previous_components_preserved_except_six_menu_spans': True,
        'common_transform_and_639_authored_selections_unchanged': True,
        'expected_final_arm9_sha256': config['expected_arm9_sha256']})
    print('Registered V136 with byte-exact input and unchanged complete COMMON transform.')


if __name__ == '__main__':
    main()
