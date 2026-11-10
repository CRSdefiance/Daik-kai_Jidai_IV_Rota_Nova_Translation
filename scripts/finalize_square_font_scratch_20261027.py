"""Verify the final integrated manifest and pin the repair awaiting user testing."""

import json
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.square_font_scratch_20261027 import apply_release, validate_storage
from dk4tool.rom.nds import NdsImage

ROOT = Path('work/lisbon_square_freeze_20261027')
ROM = Path('out/font_v2_square_scratch_fix_20261027_test.nds')


def read(path):
    return json.loads(path.read_text(encoding='utf-8'))


def main():
    manifest_path = ROM.with_suffix('.manifest.json')
    manifest = read(manifest_path)
    registry = Path('translations/release_stack.json')
    stack = read(registry)
    before = read(ROOT / 'release_stack_before.json')
    digest = sha(ROM.read_bytes())
    assert digest == manifest['candidate_sha256'] == '89860905d61e348ae053d40836159bc86bff5d85d3206ce3a0961a6d60142077'
    assert manifest['release_stack_sha256'] == sha(registry.read_bytes())
    arm = NdsImage.open(ROM).read_file('/__arm9__.bin')
    contract = validate_storage(arm)
    assert manifest['final_square_font_scratch_contract'] == contract
    source = NdsImage.open(Path('out/font_v2_all_punctuation_one_pixel_20261027_test.nds')).read_file('/__arm9__.bin')
    target, _ = apply_release(source, 'translations/square_font_scratch_20261027_v1.json')
    assert target == arm and all(manifest['checks'].values()) and len(manifest['batches']) == 560
    for key in ('canonical_baseline', 'accepted_layers', 'latest_promoted_build'):
        assert stack[key] == before[key]
    assert len(stack['accepted_layers']) == 114
    assert read(ROOT / 'actual_runtime_proof.json')['candidate_sha256'] == digest
    assert read(ROOT / 'integrated_build_stdout.json') == manifest
    assert '29 passed' in (ROOT / 'regression_tests.log').read_text()
    assert len(read(ROOT / 'native_repair_proof.json')['all18_caption_cases']) == 18
    receipt = dict(build_exit_code=0, candidate_sha256=digest,
        release_stack_sha256=manifest['release_stack_sha256'], manifest_sha256=sha(manifest_path.read_bytes()),
        source_dependency_locks_pass=True, collision_gate=contract,
        all560_manifest_entries_and114_baked_layers_preserved=True,
        canonical_accepted_and_promoted_unchanged=True, ROM_exact_to_cold_boot_test=True)
    (ROOT / 'final_build_receipt.json').write_text(json.dumps(receipt, indent=2) + '\n', encoding='utf-8')

    pin_path = Path('translations/rom_retention_pins.json')
    pin_bytes = pin_path.read_bytes()
    pins = json.loads(pin_bytes)
    assert isinstance(pins, list)
    physical = ROM.resolve().as_posix()
    if not any(row['path'].casefold() == physical.casefold() for row in pins):
        (ROOT / 'retention_pins_before.json').write_bytes(pin_bytes)
        pins.append(dict(path=physical,
            reason='Lisbon Square/font scratch repair awaiting user cold-boot testing; SHA256 ' + digest))
        newline = '\r\n' if b'\r\n' in pin_bytes else '\n'
        encoded = (json.dumps(pins, ensure_ascii=False, indent=2) + '\n').replace('\n', newline).encode()
        assert pin_path.read_bytes() == pin_bytes
        pin_path.write_bytes(encoded)
    print('Final manifest/source locks/collision gate pass; exact tested ROM;560 entries/114 baked layers; repair pinned; canonical/main unchanged.')


if __name__ == '__main__':
    main()
