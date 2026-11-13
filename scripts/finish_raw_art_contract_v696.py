"""Verify a complete registered rebuild adds protection without changing V692."""

from pathlib import Path

from dk4tool.graphics.raw_art_contract import verify_final_raw_art
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.verify_raw_art_final_contract_v696 import REBUILT, ROM, ROOT
from scripts.verify_village_wrap_v608 import read, save


def main():
    pre, proof = read(ROOT / 'preflight.json'), read(ROOT / 'contract_proof.json')
    for path, digest in pre['release_hashes'].items():
        assert sha(Path(path).read_bytes()) == digest
    for path, key in (('dk4tool/graphics/raw_art_contract.py', 'gate_sha256'),
                      ('scripts/build_integrated_release.py', 'builder_sha256'),
                      ('scripts/verify_raw_art_final_contract_v696.py', 'verifier_sha256')):
        assert sha(Path(path).read_bytes()) == proof[key]
    assert REBUILT.read_bytes() == ROM.read_bytes()
    manifest, prior = read(REBUILT.with_suffix('.manifest.json')), read(ROM.with_suffix('.manifest.json'))
    for key in ('candidate_sha256', 'profile', 'base_sha256', 'release_stack_sha256', 'batches',
                'required_batches', 'changed_paths', 'changed_records', 'relocations', 'story_percent_contract',
                'final_plaque_contract'):
        assert manifest[key] == prior[key], key
    assert len(manifest['batches']) == 470 and len(read('translations/release_stack.json')['accepted_layers']) == 114
    for key, value in prior['checks'].items():
        assert manifest['checks'][key] == value
    assert manifest['checks']['final_reviewed_raw_art_contract_enforced']
    actual = verify_final_raw_art(NdsImage.open(REBUILT), NdsImage.open('out/raphael_natural_v2_accepted_base.nds'),
                                  NdsImage.open('work/clean.nds'), [Path(p) for p in manifest['batches']])
    assert actual == manifest['final_raw_art_contract'] == proof['final_contract']
    save(ROOT / 'rebuild_proof.json', {'rebuild': str(REBUILT), 'rebuild_sha256': sha(REBUILT.read_bytes()),
        'manifest': str(REBUILT.with_suffix('.manifest.json')),
        'manifest_sha256': sha(REBUILT.with_suffix('.manifest.json').read_bytes()),
        'complete_ROM_exact_V692_and_all470_batches114_accepted_layers_retained': True,
        'all_prior_paths_records_relocations_plaque_story_and_other_checks_exact': True,
        'final18_comic_regions11_untouched_frames_and4320_mark_bytes_guard_in_manifest': True,
        'original_exact_V692_patch_remains_valid_no_new_patch_or_candidate_required': True,
        'no_new_cold_boot_claim_for_identical_binary_or_unknown_comic_consumer_clearance': True,
        'all18_plaques_and_broader_graphics_goal_remain_open': True,
        'verifier_sha256': sha(Path(__file__).read_bytes()), 'full_goal_complete': False})
    print('V696 full registered rebuild is byte-exact V692; final raw-art contract added to reproduction manifest; all prior content and checks retained.', flush=True)


if __name__ == '__main__':
    main()
