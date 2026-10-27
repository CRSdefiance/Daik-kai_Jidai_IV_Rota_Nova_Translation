"""Copy an explicitly verified final-ROM capture into the future-guide archive."""

import argparse
import json
import shutil
from pathlib import Path

from PIL import Image

from dk4tool.patch.grand_race_menu_release import sha


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--report', type=Path, required=True)
    parser.add_argument('--frame', type=int, required=True)
    parser.add_argument('--name', required=True)
    parser.add_argument('--description', required=True)
    parser.add_argument('--verification-proof', type=Path, required=True)
    parser.add_argument('--candidate-rom', type=Path,
                        help='Registered ROM that is byte-identical to the captured ROM')
    args = parser.parse_args()
    assert Path(args.name).name == args.name and args.name.endswith('.png')
    report = json.loads(args.report.read_text(encoding='utf-8'))
    proof = json.loads(args.verification_proof.read_text(encoding='utf-8'))
    digest = report['ROM_sha256']
    assert proof['candidate_sha256'] == digest
    captured_rom = Path(report['ROM'])
    rom = args.candidate_rom or captured_rom
    assert rom.read_bytes() == captured_rom.read_bytes(), 'Registered and captured ROM bytes differ'
    manifest = json.loads(rom.with_suffix('.manifest.json').read_text(encoding='utf-8'))
    assert sha(rom.read_bytes()) == manifest['candidate_sha256'] == digest
    assert report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
    if report.get('synthetic_inventory_fixtures'):
        raise ValueError('Synthetic inventory captures belong in the test-fixture archive, not the normal-play guide')
    if report.get('synthetic_ending_fixtures'):
        raise ValueError('Synthetic ending captures belong in the test-fixture archive, not the normal-play guide')
    if report.get('synthetic_location_fixtures'):
        raise ValueError('Synthetic location captures belong in the test-fixture archive, not the normal-play guide')
    if report.get('synthetic_condition_fixtures'):
        raise ValueError('Synthetic condition captures belong in the test-fixture archive, not the normal-play guide')
    if report.get('synthetic_gallery_fixtures'):
        raise ValueError('Synthetic Gallery captures belong in the test-fixture archive, not the normal-play guide')
    captures = [r for r in report['frames_captured'] if r['frame'] == args.frame]
    assert captures
    captured = next((r for r in captures if 'final' in r['path']), captures[-1])
    source = Path(captured['path'])
    assert sha(source.read_bytes()) == captured['PNG_sha256']
    assert Image.open(source).size == (256, 384)
    root = Path('guide/screenshots')
    root.mkdir(parents=True, exist_ok=True)
    destination = root / args.name
    if destination.exists():
        assert destination.read_bytes() == source.read_bytes(), 'Use a new name for a different capture.'
    else:
        shutil.copyfile(source, destination)
    ledger = root / 'manifest.json'
    data = json.loads(ledger.read_text()) if ledger.exists() else {'purpose': 'Verified screenshots for a future game guide', 'screenshots': []}
    entry = {'file': args.name, 'description': args.description,
             'source_capture': str(source).replace('\\', '/'),
             'source_report': str(args.report).replace('\\', '/'),
             'source_report_sha256': sha(args.report.read_bytes()),
             'verification_proof': str(args.verification_proof).replace('\\', '/'),
             'verification_proof_sha256': sha(args.verification_proof.read_bytes()),
             'ROM': str(rom), 'ROM_sha256': digest, 'frame': args.frame,
             'captured_ROM': str(captured_rom),
             'registered_and_captured_ROM_byte_identical': True,
             'native_dimensions': [256, 384], 'PNG_sha256': sha(source.read_bytes()),
             'cold_boot': True, 'savestate_loaded': False,
             'copied_byte_exact_no_image_editing': True,
             'release_status': 'experimental',
             'screen_verification_is_explicit_operator_selection': True}
    data['screenshots'] = [r for r in data['screenshots'] if r['file'] != args.name] + [entry]
    ledger.write_text(json.dumps(data, indent=2) + '\n')
    print('Archived unchanged native screenshot:', destination)


if __name__ == '__main__':
    main()
