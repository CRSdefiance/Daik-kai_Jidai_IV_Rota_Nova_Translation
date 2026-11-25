"""Reconstruct the exact registered Maria315 candidate without promoting main."""
import gzip
from pathlib import Path

from dk4tool.patch.xdelta import apply_xdelta
from scripts.audit_story_glyph_consistency import load, save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest

RELEASE = Path('work/maria315_B286_B302_release_v1/registered_release_verification.json')
PACKAGE = Path('releases/all_routes_editorial_20261110_maria315_candidate')
OUT = Path('out/promotion_ready_20261110_maria315_v1')


def main():
    assert not OUT.exists()
    release = load(RELEASE)
    registry = Path('translations/release_stack.json')
    before_registry = digest(registry)
    assert before_registry == release['registry_sha256']
    assert (release['registered_manifest_entries'], release['accepted_layers'],
            release['passing_release_checks']) == (725, 114, 60)
    assert release['clean_input_patch_byte_exact'] and not release['own_registered_startup_pending']
    for key in ['candidate', 'manifest', 'patch', 'own_registered_startup',
                'own_registered_name_getters', 'exact_record_bindings']:
        assert digest(release[key]) == release[key + '_sha256'], key
    assert load(registry)['latest_promoted_build']['profile'] == 'all-routes-unified-v4701'
    clean = Path('work/clean.nds')
    patch = PACKAGE / 'translation.xdelta'
    assert digest(clean) == release['clean_input_sha256']
    assert digest(patch) == release['patch_sha256']
    checksums = load(PACKAGE / 'checksums.json')
    actual_files = {str(p.relative_to(PACKAGE)).replace('\\', '/')
                    for p in PACKAGE.rglob('*') if p.is_file() and p.name != 'checksums.json'}
    assert actual_files == set(checksums)
    for name, expected in checksums.items():
        assert digest(PACKAGE / name) == expected, name
    assert gzip.decompress((PACKAGE / 'build_manifest.json.gz').read_bytes()) == Path(release['manifest']).read_bytes()
    assert gzip.decompress((PACKAGE / 'build_release_stack.json.gz').read_bytes()) == registry.read_bytes()
    OUT.mkdir()
    rom = OUT / 'Translation_DS_Maria315_promotion_candidate.nds'
    apply_xdelta(clean, patch, rom)
    assert digest(rom) == release['candidate_sha256']
    assert rom.read_bytes() == Path(release['candidate']).read_bytes()
    manifest = rom.with_suffix('.manifest.json')
    manifest.write_bytes(Path(release['manifest']).read_bytes())
    assert digest(manifest) == release['manifest_sha256']
    receipt = dict(
        candidate=str(rom), candidate_sha256=digest(rom),
        manifest=str(manifest), manifest_sha256=digest(manifest),
        registered_release=str(RELEASE), registered_release_sha256=digest(RELEASE),
        clean_input=str(clean), clean_input_sha256=digest(clean),
        patch=str(patch), patch_sha256=digest(patch),
        exact_registered_candidate_reconstructed_from_clean_input=True,
        original_manifest_preserved_with_registered_paths=True,
        release_entries=725, accepted_layers=114, release_checks=60,
        integrated_editorial_records=24093,
        main_promoted=False, user_acceptance_pending=True,
        pending_Lil382_not_in_this_ROM=True,
        new_editorial_credit=0, new_gameplay_claim=False, full_goal_complete=False,
        producer=str(Path(__file__)), producer_sha256=digest(__file__))
    save(OUT / 'promotion_reconstruction.json', receipt)
    published = PACKAGE / 'verification/promotion_reconstruction.json'
    assert not published.exists()
    save(published, receipt)
    save(PACKAGE / 'checksums.json', {
        str(p.relative_to(PACKAGE)).replace('\\', '/'): digest(p)
        for p in PACKAGE.rglob('*') if p.is_file() and p.name != 'checksums.json'
    })
    assert digest(registry) == before_registry
    print('PASS exact clean-input reconstruction:725 entries/114 layers/60 release checks.')
    print(rom)
    print(digest(rom))


if __name__ == '__main__':
    main()
