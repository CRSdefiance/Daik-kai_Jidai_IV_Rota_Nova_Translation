"""Verify the clearly named current combined build without promoting it."""

import json
from pathlib import Path
import subprocess
import sys

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.square_font_scratch_20261027 import validate_storage
from dk4tool.rom.nds import NdsImage

ROOT = Path('work/combined_handoff_20261027')
ROM = Path('out/all_routes_combined_font_and_square_fixed_20261027.nds')
PREVIOUS = Path('out/font_v2_square_scratch_fix_20261027_test.nds')
PROFILE = 'font-v2-square-scratch-fix-20261027'
EXPECTED = '89860905d61e348ae053d40836159bc86bff5d85d3206ce3a0961a6d60142077'


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def main():
    ROOT.mkdir(exist_ok=False)
    manifest_path = ROM.with_suffix('.manifest.json')
    manifest, previous = read(manifest_path), read(PREVIOUS.with_suffix('.manifest.json'))
    registry_path = Path('translations/release_stack.json')
    stack = read(registry_path)
    assert sha(ROM.read_bytes()) == sha(PREVIOUS.read_bytes()) == EXPECTED
    assert manifest['candidate_sha256'] == EXPECTED
    assert Path(manifest['candidate_rom']).resolve() == ROM.resolve()
    assert manifest['profile'] == PROFILE
    assert manifest['release_stack_sha256'] == sha(registry_path.read_bytes())
    assert all(manifest['checks'].values())
    assert manifest['batches'] == previous['batches'] and len(manifest['batches']) == 560
    assert manifest['required_batches'] == previous['required_batches']
    integrated = stack['profiles']['all-routes-unified-v4749']
    combined = stack['profiles'][PROFILE]
    assert all(combined.get(k) == v for k,v in integrated.items() if k not in ('description','note'))
    additions = {k:combined[k] for k in combined if k not in integrated}
    assert set(additions) == {'experimental_ascii_font_v2','ascii_draw_offset_one_20261027',
        'ascii_punctuation_20261027','ascii_punctuation_all_20261027','square_font_scratch_20261027'}
    assert all(str(Path(p)) in manifest['batches'] for p in additions.values())
    assert len(stack['accepted_layers']) == 114
    assert sha(Path(stack['canonical_baseline']['path']).read_bytes()) == stack['canonical_baseline']['sha256']
    arm = NdsImage.open(ROM).read_file('/__arm9__.bin')
    assert sha(arm) == '39b11636e9b9904f96e18691154c813ebcad6e61647db412fa60b7344221b4a1'
    assert sha(GameAsciiFont.from_arm9(arm).glyphs) == 'e63b0fc168b31383938d6212724bf7292300b9f41b936044515e78ce85d757f0'
    collision = validate_storage(arm)
    assert collision['applicable'] and collision['runtime_code_and_bitmap_disjoint']
    assert collision == manifest['final_square_font_scratch_contract']
    args = [sys.executable,'scripts/verify_release_baseline.py',manifest['base_rom'],str(ROM)]
    for name in manifest['changed_paths']:
        args += ['--allow-path',name]
    with (ROOT/'baseline.log').open('w',encoding='utf-8') as log:
        subprocess.run(args,check=True,stdout=log,stderr=subprocess.STDOUT)
    receipt = dict(status='pass',candidate=str(ROM),candidate_sha256=EXPECTED,
        manifest=str(manifest_path),manifest_sha256=sha(manifest_path.read_bytes()),
        registry_sha256=sha(registry_path.read_bytes()),all560_manifest_entries_preserved=True,
        accepted_baked_layers=114,latest_integrated_profile='all-routes-unified-v4749',
        latest_integrated_settings_preserved=True,additional_repair_layers=additions,
        final_square_storage_contract=collision,byte_exact_to_prior_repaired_ROM=True,
        baseline_verifier_passed=True,profile_status=combined['status'],
        exact_tutorial_crowd_gameplay_acceptance_pending=True,
        promoted_main_unchanged=stack['latest_promoted_build'])
    (ROOT/'verification.json').write_text(json.dumps(receipt,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(receipt,indent=2))


if __name__ == '__main__':
    main()
