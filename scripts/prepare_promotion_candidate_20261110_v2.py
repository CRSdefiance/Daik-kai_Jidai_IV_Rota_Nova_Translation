"""Reconstruct and package the registered cumulative release; preserve pending work."""
import ast
import gzip
import shutil
import xml.etree.ElementTree as ET
from pathlib import Path

from dk4tool.patch.xdelta import apply_xdelta
from scripts.audit_story_glyph_consistency import load, save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest

RELEASE = Path('work/lil382_residual_A_release_v1/registered_release_verification.json')
SOURCE = Path('releases/all_routes_editorial_20261110_lil382_candidate')
PACKAGE = Path('releases/all_routes_promotion_20261110_v2')
OUT = Path('out/promotion_ready_20261110_v2')
ROM_NAME = 'Translation_DS_All_Routes_20261110_v2_candidate.nds'


def main():
    assert not OUT.exists() and not PACKAGE.exists()
    release = load(RELEASE)
    registry = Path('translations/release_stack.json')
    assert digest(registry) == release['registry_sha256']
    stack = load(registry)
    assert stack['latest_promoted_build']['profile'] == 'all-routes-unified-v4701'
    assert (release['registered_manifest_entries'], release['accepted_layers'],
            release['passing_release_checks']) == (726, 114, 61)
    assert release['clean_input_patch_byte_exact'] and not release['own_registered_startup_pending']
    for key in ['candidate', 'manifest', 'patch', 'own_registered_startup',
                'own_registered_name_getters', 'exact_record_bindings']:
        assert digest(release[key]) == release[key + '_sha256'], key
    manifest = load(release['manifest'])
    assert manifest['profile'] == release['profile']
    assert manifest['release_stack_sha256'] == digest(registry)
    assert manifest['candidate_sha256'] == release['candidate_sha256']
    assert len(manifest['batches']) == 726
    assert len(manifest['checks']) == 61 and all(manifest['checks'].values())
    normalize = lambda p: str(p).replace('\\', '/')
    assert {normalize(x['batch']) for x in stack['accepted_layers']} <= {
        normalize(x) for x in manifest['batches']}
    assert manifest['base_sha256'] == digest('out/raphael_natural_v2_accepted_base.nds')
    assert gzip.decompress((SOURCE / 'build_manifest.json.gz').read_bytes()) == Path(release['manifest']).read_bytes()
    assert gzip.decompress((SOURCE / 'build_release_stack.json.gz').read_bytes()) == registry.read_bytes()
    checksums = load(SOURCE / 'checksums.json')
    files = {normalize(p.relative_to(SOURCE)) for p in SOURCE.rglob('*')
             if p.is_file() and p.name != 'checksums.json'}
    assert files == set(checksums)
    for name, expected in checksums.items():
        assert digest(SOURCE / name) == expected, name
    report = Path('work/promotion_20261110_v2_pytest.xml')
    suites = list(ET.parse(report).getroot().iter('testsuite'))
    assert sum(int(s.get('tests', 0)) for s in suites) == 27
    assert all(int(s.get(k, 0)) == 0 for s in suites for k in ['errors', 'failures', 'skipped'])
    producers = [Path(__file__), Path('scripts/check_editorial_three_choice_explicit_route_v1.py'),
                 Path('scripts/check_scoped_clean_menus_v4.py'), Path('scripts/refresh_reviewed_formatting_prose_v1.py')]
    for p in producers:
        ast.parse(p.read_bytes(), filename=str(p))
    clean = Path('work/clean.nds')
    assert digest(clean) == release['clean_input_sha256']
    assert digest(SOURCE / 'translation.xdelta') == release['patch_sha256']
    OUT.mkdir()
    rom = OUT / ROM_NAME
    apply_xdelta(clean, SOURCE / 'translation.xdelta', rom)
    assert digest(rom) == release['candidate_sha256']
    assert rom.read_bytes() == Path(release['candidate']).read_bytes()
    adjacent = rom.with_suffix('.manifest.json')
    adjacent.write_bytes(Path(release['manifest']).read_bytes())
    assert digest(adjacent) == release['manifest_sha256']
    shutil.copytree(SOURCE, PACKAGE)
    receipt = dict(candidate=str(rom), candidate_sha256=digest(rom),
        manifest=str(adjacent), manifest_sha256=digest(adjacent),
        registered_release=str(RELEASE), registered_release_sha256=digest(RELEASE),
        profile=release['profile'], registry_sha256=digest(registry),
        clean_input_sha256=digest(clean), patch='translation.xdelta', patch_sha256=release['patch_sha256'],
        exact_registered_candidate_reconstructed_from_clean_input=True,
        byte_identical_to_registered_Lil382=True, new_internal_ROM_changes=False,
        release_entries=726, accepted_layers=114, passing_release_checks=61,
        fresh_repository_tests=27, repository_test_failures=0,
        repository_report=str(report), repository_report_sha256=digest(report),
        parsed_producers={str(p): digest(p) for p in producers},
        pending_Lil269_excluded=True, pending_Lil269_fifth_gates_not_passed=True,
        integrated_editorial_records=24475, new_editorial_credit=0,
        new_gameplay_claim=False, hardware_testing_claim=False,
        main_promoted=False, user_acceptance_pending=True, full_goal_complete=False)
    save(OUT / 'promotion_reconstruction.json', receipt)
    save(PACKAGE / 'verification/promotion_v2_reconstruction.json', receipt)
    shutil.copyfile(report, PACKAGE / 'verification/promotion_v2_pytest.xml')
    (PACKAGE / 'PRIOR_Lil382_RELEASE_NOTES.md').write_bytes((SOURCE / 'README.md').read_bytes())
    notes = f'''# Translation DS cumulative promotion candidate — November 10, 2026

Local testing ROM: `{rom}` with its adjacent `.manifest.json`.
This is a fresh clean-input reconstruction, byte-identical to the latest registered Lil382 cumulative release. It adds no new internal ROM changes. All 726 registered entries and 114 accepted layers are included, preserving Rafael/tutorial localization, earlier storyline/shared work, Market Trade-screen correction, name fixes and the registered ASCII right-bound correction.

Apply `translation.xdelta` to the clean Japanese ROM SHA-256 `{release['clean_input_sha256']}`. Expected output SHA-256: `{release['candidate_sha256']}`. Patch SHA-256: `{release['patch_sha256']}`. The new testing copy was compared byte for byte with the registered candidate. No historical work folders are required to apply the patch. Exact build-time manifest and release registry are included as gzip files.

Fresh repository checks: 27 passed, no failures, errors or skips. All 61 registered release checks remain bound to these exact bytes. Existing emulator evidence includes the candidate's own Maria/Hangzhou cold boot, 24 protected name getters and representative Lil dialogue/menu/page transitions. This packaging step adds no gameplay or hardware coverage. Detailed observed versus offline-only coverage is in PRIOR_Lil382_RELEASE_NOTES.md and verification/.

The next 269 Lil B243–B282 reviews are preserved in Git as unfinished work and are excluded from this ROM. Their four prose gates pass; full display/storage/gameplay/release gates do not. A native FE panel complete-consumption failure remains under investigation. No pending proposal is credited or shipped.

Cold-boot this exact filename and test title/New Game, Rafael's opening/tutorial, town/Market Trade, dialogue names, wrapping and transitions. Main remains V4701 until explicit user acceptance. The integrated count is 24,475; the full editorial goal remains active. Older ROMs, translations, justified retentions and evidence remain preserved.

After cloning, run `git lfs pull` for the coverage ledger. Raw ROMs are local; the clean-input patch is committed to GitHub.
'''
    (PACKAGE / 'README.md').write_text(notes, encoding='utf-8', newline='\n')
    (OUT / 'README.md').write_text(notes, encoding='utf-8', newline='\n')
    save(PACKAGE / 'checksums.json', {normalize(p.relative_to(PACKAGE)): digest(p)
        for p in PACKAGE.rglob('*') if p.is_file() and p.name != 'checksums.json'})
    assert digest(registry) == release['registry_sha256']
    print('PASS: fresh exact cumulative reconstruction, 726 entries, 114 accepted layers, 61 release checks, 27 fresh tests.')
    print(rom)
    print(digest(rom))


if __name__ == '__main__':
    main()
