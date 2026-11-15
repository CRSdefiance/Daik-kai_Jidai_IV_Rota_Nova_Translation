"""Verify complete registered stack, exact changed blocks and clean-input patch."""
import argparse
from collections import Counter
from pathlib import Path
import sys

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.xdelta import make_xdelta, apply_xdelta
from dk4tool.rom.nds import NdsImage
from scripts.audit_story_glyph_consistency import load, save
from scripts.verify_release_baseline import main as verify_baseline


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--candidate', type=Path, required=True)
    ap.add_argument('--out', type=Path, required=True)
    args = ap.parse_args()
    assert not args.out.exists()
    manifest_path = args.candidate.with_suffix('.manifest.json')
    manifest = load(manifest_path)
    registration = load('work/analysis/Hodram_B61_B70_release_20261101/registration.json')
    assert manifest['profile'] == registration['profile']
    assert sha(args.candidate.read_bytes()) == manifest['candidate_sha256'] == registration['expected_final_ROM_sha256']
    registry_path = Path(manifest['release_stack'])
    assert sha(registry_path.read_bytes()) == manifest['release_stack_sha256'] == registration['registry_after_sha256']
    registry = load(registry_path)
    assert all(manifest['checks'].values()) and len(manifest['checks']) == 19
    assert manifest['checks']['registered_runtime_bounds_and_complete_parent_target_inverse']
    parent_path = Path('out/all_routes_combined_lisbon_guild_fixed_20261101.nds')
    parent_manifest = load(parent_path.with_suffix('.manifest.json'))
    assert sha(parent_path.read_bytes()) == parent_manifest['candidate_sha256']
    assert manifest['batches'][:648] == parent_manifest['batches'][:648]
    assert len(manifest['batches']) == 651
    profile = registry['profiles'][registration['profile']]
    expected = [str(Path(load(s['config'])['manuscript'])) for s in profile['late_editorial_extensions'][-2:]]
    expected.append(str(Path(profile['ascii_glyph_right_bounds'])))
    assert manifest['batches'][648:] == expected
    present = {str(Path(p).resolve()).casefold() for p in manifest['batches']}
    assert len(registry['accepted_layers']) == 114
    assert manifest['base_sha256'] == registry['canonical_baseline']['sha256']
    assert sha(Path(registry['canonical_baseline']['path']).read_bytes()) == manifest['base_sha256']
    # Baked layers are carried by the exact immutable canonical image rather
    # than reapplied as separate batches. Every unbaked layer must be listed.
    assert all(r.get('baked_into_baseline') is True or
               str(Path(r['batch']).resolve()).casefold() in present
               for r in registry['accepted_layers'])
    prior_registry = load('work/analysis/Hodram_B61_B70_release_20261101/release_stack_before_registration.json')
    assert registry['accepted_layers'] == prior_registry['accepted_layers']
    candidate, parent = NdsImage.open(args.candidate), NdsImage.open(parent_path)
    changed = [p for _, p, v in parent.iter_files() if candidate.read_file(p) != v]
    assert set(changed) == {'/data/SC0.DK4', '/data/SC1.DK4'}
    assert all(candidate.read_file(p) == v for p, v in parent.iter_components())
    changed_blocks = {}
    for path, expected_blocks in [('/data/SC0.DK4', [43]), ('/data/SC1.DK4', list(range(61, 71)))]:
        old, new = [IlnkContainer.parse(i.read_file(path)).blocks for i in (parent, candidate)]
        assert len(old) == len(new)
        actual = [n for n, (a, b) in enumerate(zip(old, new, strict=True)) if a != b]
        assert actual == expected_blocks
        changed_blocks[path] = actual
        new_ids = [r['id'] for r in load(expected[0 if 'SC1' in path else 1])['records']]
        added = Counter(manifest['changed_records'][path]) - Counter(parent_manifest['changed_records'][path])
        assert added == Counter(new_ids)
    research = load('work/analysis/Julio_script_correction_20261101/reconstruction.json')
    assert args.candidate.read_bytes() == Path(research['full_research_ROM']).read_bytes()
    old_argv = sys.argv
    try:
        sys.argv = ['verify_release_baseline', str(registry['canonical_baseline']['path']), str(args.candidate)]
        for path in manifest['changed_paths']:
            sys.argv += ['--allow-path', path]
        verify_baseline()
    finally:
        sys.argv = old_argv
    clean = Path('work/clean.nds')
    assert sha(clean.read_bytes()) == 'f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d'
    patch = args.candidate.with_suffix('.xdelta')
    assert not patch.exists()
    args.out.mkdir(parents=True)
    reconstructed = args.out / 'clean_input_reconstruction_RESEARCH_ONLY.nds'
    make_xdelta(clean, args.candidate, patch)
    apply_xdelta(clean, patch, reconstructed)
    assert reconstructed.read_bytes() == args.candidate.read_bytes()
    result = dict(candidate=str(args.candidate), candidate_sha256=manifest['candidate_sha256'],
        manifest=str(manifest_path), manifest_sha256=sha(manifest_path.read_bytes()),
        profile=manifest['profile'], registry_sha256=manifest['release_stack_sha256'],
        canonical_base=manifest['base_rom'], canonical_sha256=manifest['base_sha256'],
        parent=str(parent_path), parent_sha256=parent_manifest['candidate_sha256'],
        changed_internal_files=changed, changed_blocks=changed_blocks,
        all_other_files_components_graphics_names_andruntime_exact_to_parent=True,
        complete_stack_entries=651, accepted_layers=114, passing_release_checks=19,
        new_Hodram_records=224, Julio_formatting_revisit_new_credit=0,
        byte_exact_to_checked_research_image=True,
        patch=str(patch), patch_sha256=sha(patch.read_bytes()),
        clean_input_sha256=sha(clean.read_bytes()), exact_clean_reconstruction=str(reconstructed),
        reconstructed_sha256=sha(reconstructed.read_bytes()), clean_input_patch_byte_exact=True,
        own_registered_startup_pending=True, experimental_not_promoted=True, full_goal_complete=False)
    save(args.out / 'registered_release_verification.json', result)
    print('Registered651-entry/114-accepted/19-check release and exact clean-input patch verified.')


if __name__ == '__main__':
    main()
