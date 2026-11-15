"""Reconstruct an already-qualified registered candidate without changing its registry."""
import argparse
import gzip
import shutil
import xml.etree.ElementTree as ET
from pathlib import Path

from dk4tool.patch.xdelta import apply_xdelta
from scripts.audit_story_glyph_consistency import load, save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--release', required=True, type=Path)
    parser.add_argument('--source-package', required=True, type=Path)
    parser.add_argument('--package', required=True, type=Path)
    parser.add_argument('--out', required=True, type=Path)
    parser.add_argument('--rom-name', required=True)
    parser.add_argument('--test-report', required=True, type=Path)
    args = parser.parse_args()
    assert Path(args.rom_name).name == args.rom_name and args.rom_name.endswith('.nds')
    assert not args.out.exists() and not args.package.exists()
    registry = Path('translations/release_stack.json')
    promoted = Path('translations/promoted_build.json')
    protected = {str(p): digest(p) for p in [registry, promoted]}
    release = load(args.release)
    stack = load(registry)
    assert digest(registry) == release['registry_sha256']
    assert release['clean_input_patch_byte_exact'] and not release['own_registered_startup_pending']
    for key in ['candidate', 'manifest', 'patch', 'own_registered_startup',
                'own_registered_name_getters', 'exact_record_bindings']:
        assert digest(release[key]) == release[key + '_sha256'], key
    manifest = load(release['manifest'])
    assert manifest['profile'] == release['profile']
    assert manifest['release_stack_sha256'] == digest(registry)
    assert manifest['candidate_sha256'] == release['candidate_sha256']
    assert len(manifest['batches']) == release['registered_manifest_entries']
    assert len(manifest['checks']) == release['passing_release_checks']
    assert all(value is True for value in manifest['checks'].values())
    assert len(stack['accepted_layers']) == release['accepted_layers']
    normalize = lambda p: str(p).replace('\\', '/')
    explicit = {normalize(p) for p in manifest['batches']}
    assert manifest['base_sha256'] == stack['canonical_baseline']['sha256']
    assert digest(stack['canonical_baseline']['path']) == manifest['base_sha256']
    for layer in stack['accepted_layers']:
        assert layer['status'] == 'accepted'
        assert layer.get('baked_into_baseline') is True or normalize(layer['batch']) in explicit
    source = args.source_package
    assert gzip.decompress((source / 'build_manifest.json.gz').read_bytes()) == Path(release['manifest']).read_bytes()
    assert gzip.decompress((source / 'build_release_stack.json.gz').read_bytes()) == registry.read_bytes()
    checksums = load(source / 'checksums.json')
    assert set(checksums) == {normalize(p.relative_to(source)) for p in source.rglob('*')
                              if p.is_file() and p.name != 'checksums.json'}
    for name, expected in checksums.items():
        assert digest(source / name) == expected, name
    suites = list(ET.parse(args.test_report).getroot().iter('testsuite'))
    tests = sum(int(s.get('tests', 0)) for s in suites)
    assert tests == 27
    assert all(int(s.get(k, 0)) == 0 for s in suites for k in ['errors', 'failures', 'skipped'])
    clean = Path('work/clean.nds')
    assert digest(clean) == release['clean_input_sha256']
    assert digest(source / 'translation.xdelta') == release['patch_sha256']
    args.out.mkdir(parents=True)
    rom = args.out / args.rom_name
    apply_xdelta(clean, source / 'translation.xdelta', rom)
    assert digest(rom) == release['candidate_sha256']
    assert rom.read_bytes() == Path(release['candidate']).read_bytes()
    adjacent = rom.with_suffix('.manifest.json')
    adjacent.write_bytes(Path(release['manifest']).read_bytes())
    assert digest(adjacent) == release['manifest_sha256']
    shutil.copytree(source, args.package)
    (args.package / 'REGISTERED_RELEASE_NOTES.md').write_bytes((source / 'README.md').read_bytes())
    report = args.package / 'verification/fresh_repository_pytest.xml'
    report.write_bytes(args.test_report.read_bytes())
    receipt = dict(candidate=str(rom), candidate_sha256=digest(rom), manifest=str(adjacent),
        manifest_sha256=digest(adjacent), registered_release=str(args.release),
        registered_release_sha256=digest(args.release), profile=release['profile'],
        registry_sha256=digest(registry), clean_input_sha256=digest(clean),
        patch_sha256=release['patch_sha256'], source_package_checksums_verified=len(checksums),
        exact_registered_candidate_reconstructed_from_clean_input=True,
        byte_identical_to_registered_candidate=True, new_internal_ROM_changes=False,
        release_entries=len(manifest['batches']), accepted_layers=len(stack['accepted_layers']),
        passing_release_checks=len(manifest['checks']), fresh_repository_tests=tests,
        repository_report=str(args.test_report), repository_report_sha256=digest(args.test_report),
        pending_Lil361_not_integrated=True, new_editorial_credit=0,
        new_gameplay_claim=False, hardware_testing_claim=False, main_promoted=False,
        user_acceptance_pending=True, full_goal_complete=False,
        producer=str(Path(__file__)), producer_sha256=digest(__file__))
    save(args.out / 'promotion_reconstruction.json', receipt)
    save(args.package / 'verification/fresh_promotion_reconstruction.json', receipt)
    notes = f'''# Translation DS cumulative promotion candidate

Testing ROM: `{rom}`, with its adjacent manifest.

This fresh clean-input reconstruction is byte-identical to the latest registered Lil269 cumulative candidate. It includes all {len(manifest['batches'])} registered entries and {len(stack['accepted_layers'])} accepted layers: prior Rafael/tutorial localization, storyline/shared dialogue, Market Trade-screen correction, name/glyph fixes and ASCII right bounds. It adds no new internal ROM changes.

Apply `translation.xdelta` to the clean Japanese ROM SHA-256 `{release['clean_input_sha256']}`. Expected output SHA-256: `{release['candidate_sha256']}`. Patch SHA-256: `{release['patch_sha256']}`. The new copy matches the registered candidate byte for byte. Build-time manifest and registry are included as lossless gzip files.

All {len(manifest['checks'])} registered release checks remain bound to the exact ROM. All {tests} fresh repository tests pass with no failures, errors or skips. Existing candidate-owned startup, protected-name getter, native-page and representative gameplay evidence is reused; this packaging step adds no gameplay or hardware coverage. See REGISTERED_RELEASE_NOTES.md for observed versus offline-only coverage and unvisited conditions.

The next Lil361 B283–B298 source intake remains unfinished and excluded. Its clean-source packet and exact references are preserved in Git; no new prose or review credit is shipped. Integrated editorial reviews remain 24,744. The full editorial goal stays active.

Cold-boot this exact filename and test title/New Game, Rafael/tutorial, town/Market Trade, names, wrapping, pagination and transitions. Main remains V4701 pending your explicit acceptance. Earlier ROMs and translations are preserved. Raw ROMs remain local; this clean-input patch is committed to GitHub. Run `git lfs pull` after cloning for the coverage ledger.
'''
    (args.package / 'README.md').write_text(notes, encoding='utf-8', newline='\n')
    (args.out / 'README.md').write_text(notes, encoding='utf-8', newline='\n')
    save(args.package / 'checksums.json', {normalize(p.relative_to(args.package)): digest(p)
        for p in args.package.rglob('*') if p.is_file() and p.name != 'checksums.json'})
    for name, expected in load(args.package / 'checksums.json').items():
        assert digest(args.package / name) == expected, name
    assert all(digest(p) == expected for p, expected in protected.items())
    print(f'PASS: exact clean-input reconstruction, {len(manifest["batches"])} entries, '
          f'{len(stack["accepted_layers"])} accepted layers, {len(manifest["checks"])} release checks, {tests} fresh tests.')
    print(rom)
    print(digest(rom))


if __name__ == '__main__':
    main()
