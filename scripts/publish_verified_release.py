"""Copy a verified release and finalized guide archive to the user destination."""

import argparse
import json
import shutil
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha


def read(path):
    return json.loads(path.read_text(encoding='utf-8'))


def copy_exact(source, destination, replace_metadata=False):
    digest = sha(source.read_bytes())
    if destination.exists() and sha(destination.read_bytes()) != digest:
        assert replace_metadata, f'Existing artifact differs: {destination}'
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, destination)
    assert sha(destination.read_bytes()) == digest
    return {'file': str(destination), 'sha256': digest}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--proof', type=Path, required=True)
    args = parser.parse_args()
    config = read(Path('translations/release_output_destination.json'))
    assert config['user_requested'] and config['verify_every_copy_sha256']
    proof = read(args.proof)
    rom = Path(proof['candidate'])
    manifest = read(rom.with_suffix('.manifest.json'))
    assert sha(rom.read_bytes()) == proof['candidate_sha256'] == manifest['candidate_sha256']
    assert sha(rom.with_suffix('.xdelta').read_bytes()) == proof['patch_sha256']
    assert proof['exact_clean_patch_reconstruction']
    destination = Path(config['directory'])
    receipt = [copy_exact(rom.with_suffix(suffix), destination / rom.with_suffix(suffix).name)
               for suffix in config['artifacts']]
    source = Path(config['screenshots_source'])
    screenshots = Path(config['screenshots_directory'])
    for entry in read(source / 'manifest.json')['screenshots']:
        filename = entry['file']
        assert Path(filename).name == filename
        assert entry['copied_byte_exact_no_image_editing']
        assert entry.get('final_screen_verified') or entry.get('screen_verification_is_explicit_operator_selection')
        if entry.get('PNG_sha256'):
            assert sha((source / filename).read_bytes()) == entry['PNG_sha256']
        receipt.append(copy_exact(source / filename, screenshots / filename))
    for filename in ('manifest.json', 'README.md'):
        receipt.append(copy_exact(source / filename, screenshots / filename, replace_metadata=True))
    receipt_path = args.proof.parent / 'external_copy_receipt.json'
    receipt_path.write_text(json.dumps(receipt, indent=2) + '\n', encoding='utf-8')
    print(f'{len(receipt)} copies verified by SHA-256 in {destination}.')


if __name__ == '__main__':
    main()
