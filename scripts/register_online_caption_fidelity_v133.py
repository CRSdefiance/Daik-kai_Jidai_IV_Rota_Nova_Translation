"""Register caption input reconstruction, then the complete V133 transform."""
import argparse
import copy
import hashlib
import json
from pathlib import Path

from dk4tool.rom.nds import NdsImage

BATCH = 'translations/online_caption_fidelity_arm9_v2.json'
INPUT_PROFILE = 'all-routes-v119-online-caption-input-v133'
INPUT = 'out/all_routes_v119_online_caption_input_v133.nds'


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def write(path, value):
    Path(path).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def patched_arm9(arm9, batch):
    result = bytearray(arm9)
    for row in batch['records']:
        offset = row['offset']
        old = bytes.fromhex(row['source_hex'])
        new = row['english'].encode('ascii') + b'\0'
        if len(new) > len(old) or arm9[offset:offset + len(old)] != old:
            raise ValueError('Caption source or original allocation differs')
        result[offset:offset + len(old)] = new.ljust(len(old), b'\0')
    return bytes(result)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--final', action='store_true')
    args = parser.parse_args()
    stack_path = Path('translations/release_stack.json')
    stack = json.loads(stack_path.read_text(encoding='utf-8'))
    batch = json.loads(Path(BATCH).read_text(encoding='utf-8'))
    if not args.final:
        profile = copy.deepcopy(stack['profiles']['all-routes-unified-v119'])
        profile['batches'].append(BATCH)
        profile['note'] = ('Experimental reconstruction of all V119 layers plus three '
                           'source-reviewed caption refinements; input only for the complete V133 transform.')
        stack['profiles'][INPUT_PROFILE] = profile
        write(stack_path, stack)
        print('Registered input reconstruction; build it through the integrated builder.')
        return
    old = NdsImage.open('out/all_routes_combined_v119_candidate.nds')
    stage = NdsImage.open(INPUT)
    # Prove the reconstructed parent contains all V119 files, with exactly the
    # three fixed string slots changed in ARM9. It is not a released baseline.
    old_files = {path: data for _, path, data in old.iter_files()}
    old_files.update(dict(old.iter_components()))
    stage_files = {path: data for _, path, data in stage.iter_files()}
    stage_files.update(dict(stage.iter_components()))
    if old_files.keys() != stage_files.keys():
        raise ValueError('Input file identities differ')
    for path, data in old_files.items():
        expected = patched_arm9(data, batch) if path == '/__arm9__.bin' else data
        if stage_files[path] != expected:
            raise ValueError(f'Input differs outside declared caption slots: {path}')
    config = json.loads(Path('translations/common_native_reblocking_v132.json').read_text(encoding='utf-8'))
    if sha(stage.read_file('/COMMON/MESFILE.DK4')) != config['parent_common_sha256']:
        raise ValueError('COMMON input reconstruction differs')
    config['parent_candidate'] = INPUT
    config['parent_arm9_sha256'] = sha(stage.read_file('/__arm9__.bin'))
    current = NdsImage.open('out/all_routes_combined_v132_candidate.nds')
    config['expected_arm9_sha256'] = sha(patched_arm9(current.read_file('/__arm9__.bin'), batch))
    config_path = 'translations/common_native_reblocking_v133.json'
    write(config_path, config)
    profile = copy.deepcopy(stack['profiles']['all-routes-unified-v132'])
    profile['batches'].append(BATCH)
    profile['common_native_reblocking'] = config_path
    profile['note'] = ('All V132 COMMON and inherited route/UI/graphics layers, plus three '
                       'clean-source native Online caption fidelity repairs; runtime acceptance pending.')
    stack['profiles']['all-routes-unified-v133'] = profile
    write(stack_path, stack)
    write('work/analysis/online_caption_v133_input_proof.json', {
        'input': INPUT, 'input_sha256': sha(Path(INPUT).read_bytes()),
        'all_v119_files_preserved_except_three_caption_slots': True,
        'source_arm9_sha256': config['parent_arm9_sha256'],
        'expected_final_arm9_sha256': config['expected_arm9_sha256'],
        'common_transform_and_639_authored_selections_unchanged': True,
        'canonical_baseline_unchanged': True})
    print('Registered V133 with byte-exact reconstructed input and inherited complete COMMON transform.')


if __name__ == '__main__':
    main()
