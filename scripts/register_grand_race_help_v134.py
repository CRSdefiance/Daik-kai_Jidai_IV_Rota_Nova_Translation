"""Register the complete V134 help layer and its reconstructed transform input."""

import argparse
import copy
import json
from pathlib import Path

from dk4tool.patch.grand_race_help_release import sha
from dk4tool.rom.nds import NdsImage

BATCH = 'translations/grand_race_help_arm9_v2.json'
INPUT_PROFILE = 'all-routes-v119-grand-race-help-input-v134'
INPUT = 'out/all_routes_v119_grand_race_help_input_v134.nds'


def write(path, value):
    Path(path).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def patched_arm9(arm9, batch):
    rebuilt = bytearray(arm9)
    for row in batch['records']:
        offset, old = row['offset'], bytes.fromhex(row['source_hex'])
        if arm9[offset:offset + len(old)] != old:
            raise ValueError('Help patch source span differs from transform input')
        new = bytes.fromhex(row['replacement_hex']) if 'replacement_hex' in row else row['english'].encode('ascii').ljust(len(old), b'\0')
        if len(new) != len(old):
            raise ValueError('Help patch changes span length')
        rebuilt[offset:offset + len(old)] = new
    return bytes(rebuilt)


def components(image):
    result = {path: data for _, path, data in image.iter_files()}
    result.update(dict(image.iter_components()))
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--final', action='store_true')
    args = parser.parse_args()
    stack_path = Path('translations/release_stack.json')
    stack = json.loads(stack_path.read_text(encoding='utf-8'))
    batch = json.loads(Path(BATCH).read_text(encoding='utf-8'))
    old_config = json.loads(Path('translations/common_native_reblocking_v133.json').read_text(encoding='utf-8'))
    if not args.final:
        profile = copy.deepcopy(stack['profiles']['all-routes-v119-online-caption-input-v133'])
        profile['batches'].append(BATCH)
        profile['note'] = 'All V119 input layers and V133 caption refinements plus complete race help. Experimental input only for the complete V134 COMMON transform.'
        stack['profiles'][INPUT_PROFILE] = profile
        write(stack_path, stack)
        print('Registered V134 transform input; build it through the integrated builder.')
        return
    previous_input = NdsImage.open(old_config['parent_candidate'])
    current_input = NdsImage.open(INPUT)
    previous_files, current_files = components(previous_input), components(current_input)
    if previous_files.keys() != current_files.keys():
        raise ValueError('Input file identities differ')
    for path, data in previous_files.items():
        expected = patched_arm9(data, batch) if path == '/__arm9__.bin' else data
        if current_files[path] != expected:
            raise ValueError(f'Input differs outside declared race-help spans: {path}')
    if sha(current_input.read_file('/COMMON/MESFILE.DK4')) != old_config['parent_common_sha256']:
        raise ValueError('COMMON transform input changed')
    config = copy.deepcopy(old_config)
    config['parent_candidate'] = INPUT
    config['parent_arm9_sha256'] = sha(current_input.read_file('/__arm9__.bin'))
    previous = NdsImage.open('out/all_routes_combined_v133_candidate.nds')
    config['expected_arm9_sha256'] = sha(patched_arm9(previous.read_file('/__arm9__.bin'), batch))
    config_path = 'translations/common_native_reblocking_v134.json'
    write(config_path, config)
    profile = copy.deepcopy(stack['profiles']['all-routes-unified-v133'])
    profile['batches'].append(BATCH)
    profile['common_native_reblocking'] = config_path
    profile['note'] = 'All V133 route/UI/graphics/COMMON layers plus nine complete natural-English Grand Race instruction pages and eight headings, with build-time page formatting and source checks. Experimental; runtime acceptance pending.'
    stack['profiles']['all-routes-unified-v134'] = profile
    write(stack_path, stack)
    write('work/analysis/grand_race_help_v134_input_proof.json', {
        'input': INPUT, 'input_sha256': sha(Path(INPUT).read_bytes()),
        'previous_input': old_config['parent_candidate'],
        'all_previous_input_components_preserved_except_help_spans': True,
        'common_transform_and_639_authored_selections_unchanged': True,
        'input_arm9_sha256': config['parent_arm9_sha256'],
        'expected_final_arm9_sha256': config['expected_arm9_sha256']})
    print('Registered full V134 with byte-exact reconstructed input and inherited COMMON transform.')


if __name__ == '__main__':
    main()
