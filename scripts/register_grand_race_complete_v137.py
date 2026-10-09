"""Register the complete race UI while retaining every preceding release layer."""

import argparse
import copy
from pathlib import Path

from dk4tool.patch.grand_race_complete_release import (
    CODE,
    DATA,
    DEPENDENCIES,
    PROPOSAL_SHA,
    compile_components,
    read,
    sha,
)
from dk4tool.rom.nds import NdsImage
from scripts.plan_grand_race_ui_allocation_v136 import CANDIDATE
from scripts.register_grand_race_help_v134 import components, write

INPUT_PROFILE = 'all-routes-v119-complete-race-input-v137'
INPUT = 'out/all_routes_v119_complete_race_input_v137.nds'
SHARED = DEPENDENCIES[2]
ORIGINAL_HELP = 'translations/grand_race_help_arm9_v2.json'


def extend(profile):
    result = copy.deepcopy(profile)
    if result['batches'].count(ORIGINAL_HELP) != 1:
        raise ValueError('Exactly one original help component must be replaced')
    result['batches'] = [SHARED if path == ORIGINAL_HELP else path for path in result['batches']]
    for path in (DATA, CODE, DEPENDENCIES[-1]):
        if path in result['batches']:
            raise ValueError('Complete UI component already present')
        result['batches'].append(path)
    return result


def overlay(source):
    canonical = NdsImage.open('out/raphael_natural_v2_accepted_base.nds').read_file('/__arm9__.bin')
    compiled, proposed = compile_components(canonical)
    previous = NdsImage.open(CANDIDATE).read_file('/__arm9__.bin')
    rows = compiled['data'] + compiled['code'] + read(DEPENDENCIES[-1])['records']
    rows += [row for row in read(SHARED)['records'] if row['id'].endswith('_SHARED_HELP_TITLE_POINTER')]
    rebuilt = bytearray(source)
    for row in rows:
        lo, size = row['offset'], len(bytes.fromhex(row['source_hex']))
        if source[lo:lo + size] != previous[lo:lo + size]:
            raise ValueError('Transform input has different existing race bytes')
        rebuilt[lo:lo + size] = bytes.fromhex(row['replacement_hex'])
        if rebuilt[lo:lo + size] != proposed[lo:lo + size]:
            raise ValueError('Complete overlay differs from native-reviewed proposal')
    return bytes(rebuilt)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--final', action='store_true')
    args = parser.parse_args()
    stack_path = Path('translations/release_stack.json')
    stack = read(stack_path)
    old = read('translations/common_native_reblocking_v136.json')
    if not args.final:
        profile = extend(stack['profiles']['all-routes-v119-transition-status-input-v136'])
        profile['note'] = 'Complete V136 transform input plus full race UI dependencies; experimental V137 input.'
        stack['profiles'][INPUT_PROFILE] = profile
        write(stack_path, stack)
        print('Registered complete V137 transform input; canonical baseline unchanged.')
        return
    previous = components(NdsImage.open(old['parent_candidate']))
    current = components(NdsImage.open(INPUT))
    if previous.keys() != current.keys():
        raise ValueError('Transform input component identities differ')
    for path, data in previous.items():
        expected = overlay(data) if path == '/__arm9__.bin' else data
        if current[path] != expected:
            raise ValueError(f'Complete transform input changed outside mapped race spans: {path}')
    if sha(current['/COMMON/MESFILE.DK4']) != old['parent_common_sha256']:
        raise ValueError('Existing COMMON input changed')
    if sha(overlay(NdsImage.open(CANDIDATE).read_file('/__arm9__.bin'))) != PROPOSAL_SHA:
        raise ValueError('Complete final proposal is not reproduced')
    config = copy.deepcopy(old)
    config['parent_candidate'] = INPUT
    config['parent_arm9_sha256'] = sha(current['/__arm9__.bin'])
    config['expected_arm9_sha256'] = PROPOSAL_SHA
    config_path = 'translations/common_native_reblocking_v137.json'
    write(config_path, config)
    profile = extend(stack['profiles']['all-routes-unified-v136'])
    profile['common_native_reblocking'] = config_path
    profile['note'] = 'All preceding layers plus complete 51-message race UI, shared help titles and atomic names. Experimental; gameplay pending.'
    stack['profiles']['all-routes-unified-v137'] = profile
    write(stack_path, stack)
    write('work/analysis/grand_race_complete_v137_input_proof.json', {
        'input': INPUT, 'input_sha256': sha(Path(INPUT).read_bytes()),
        'previous_input': old['parent_candidate'], 'all_other_components_byte_exact': True,
        'common_transform_and_639_authored_selections_unchanged': True,
        'expected_final_arm9_sha256': PROPOSAL_SHA})
    print('Registered complete V137 profile with unchanged COMMON transform and exact full UI proposal.')


if __name__ == '__main__':
    main()
