"""Saved V161 artwork, complete prior stack and clean-ROM patch reconstruction."""

import json
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.xdelta import apply_xdelta, make_xdelta
from dk4tool.rom.nds import NdsImage
from scripts.build_integrated_release import (
    CANONICAL_BASELINE_SHA256,
    RELEASE_STACK_PATH,
    accepted_batch_paths,
    apply_ilnk_pxl_sync_batches,
    apply_pxl_native_label_batch,
    load_release_stack,
    resolve_release_batches,
    rom_files,
    verify_golden_content,
)
from scripts.materialize_name_treasure_graphics_v161 import (
    ARCHIVE,
    BASE,
    BUTTON_SYNC,
    NAME,
    NAME_BATCH,
    PRIOR,
    SYNC_BATCH,
    TREASURE,
    TREASURE_BATCH,
)

CANDIDATE = Path('out/all_routes_combined_v161_candidate.nds')
PROFILE = 'all-routes-unified-v161'


def main():
    prior_hash = '8a2cd62835ac2b5ecc3e176877fcaf2f08f45f119dff1fd64006d634a09b40e6'
    if sha(PRIOR.read_bytes()) != prior_hash or sha(BASE.read_bytes()) != CANONICAL_BASELINE_SHA256:
        raise ValueError('Exact V160 and canonical baseline required')
    base, prior, new = [NdsImage.open(path) for path in (BASE, PRIOR, CANDIDATE)]
    manifest = json.loads(CANDIDATE.with_suffix('.manifest.json').read_text(encoding='utf-8'))
    old_manifest = json.loads(PRIOR.with_suffix('.manifest.json').read_text(encoding='utf-8'))
    registry = load_release_stack()
    if (manifest['candidate_sha256'] != sha(CANDIDATE.read_bytes())
            or manifest['base_sha256'] != CANONICAL_BASELINE_SHA256 or manifest['profile'] != PROFILE
            or manifest['release_stack_sha256'] != sha(RELEASE_STACK_PATH.read_bytes())
            or manifest['batches'] != [str(p) for p in resolve_release_batches(PROFILE, [], registry)]
            or len(manifest['batches']) != 440 or manifest['batches'][:437] != old_manifest['batches']
            or manifest['required_batches'] != [str(p) for p in accepted_batch_paths(registry)]
            or not all(manifest['checks'].values())):
        raise ValueError('Complete saved V161 identity/stack/checks differ')
    before, after, canonical = rom_files(prior), rom_files(new), rom_files(base)
    changed = sorted(p for p in before.keys() | after.keys() if before.get(p) != after.get(p))
    if changed != sorted([ARCHIVE, NAME, TREASURE]):
        raise ValueError('V161 changed inherited ARM9, route/shared text or unrelated graphics')
    canonical_changed = sorted(p for p in canonical.keys() | after.keys() if canonical.get(p) != after.get(p))
    if (manifest['changed_paths'] != canonical_changed
            or canonical_changed != sorted(old_manifest['changed_paths'] + [NAME, TREASURE])):
        raise ValueError('Canonical changed path set differs')
    if manifest['relocations'] != old_manifest['relocations']:
        raise ValueError('An inherited relocation/terminal repair stage differs')
    for path, ids in old_manifest['changed_records'].items():
        expected = ids + (['DK4_NAME_ENTRY_EMBEDDED_GRAPHICS_V1'] if path == ARCHIVE else [])
        if manifest['changed_records'][path] != expected:
            raise ValueError('Inherited changed records differ: ' + path)
    expected_images = {}
    for path, batch_path in ((NAME, NAME_BATCH), (TREASURE, TREASURE_BATCH)):
        raw, ids = apply_pxl_native_label_batch(batch_path, base.read_file(path), new.read_file('/__arm9__.bin'))
        if raw != new.read_file(path) or ids != manifest['changed_records'][path]:
            raise ValueError('Saved artwork differs from complete reviewed source/font batch')
        expected_images[path] = raw
    expected_archive, ids = apply_ilnk_pxl_sync_batches([BUTTON_SYNC, SYNC_BATCH], base.read_file(ARCHIVE),
        {'/_pxl/slackimg20.pxl': prior.read_file('/_pxl/slackimg20.pxl'), NAME: expected_images[NAME]})
    if expected_archive != new.read_file(ARCHIVE) or ids != manifest['changed_records'][ARCHIVE]:
        raise ValueError('Saved archive overwrites the prior button prompt or new plaques')
    verify_golden_content(base, new)
    compatibility = Path('work/analysis/v160_sync_compatibility.nds')
    if compatibility.read_bytes() != PRIOR.read_bytes():
        raise ValueError('Final builder no longer reconstructs V160 byte-identically')
    clean = Path('work/clean.nds')
    if sha(clean.read_bytes()) != 'f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d':
        raise ValueError('Wrong clean patch base')
    patch, reconstruction = CANDIDATE.with_suffix('.xdelta'), Path('work/analysis/name_treasure_v161_patch_reconstruction.nds')
    make_xdelta(clean, CANDIDATE, patch)
    apply_xdelta(clean, patch, reconstruction)
    if reconstruction.read_bytes() != CANDIDATE.read_bytes():
        raise ValueError('V161 clean-ROM patch does not reconstruct exactly')
    report = {
        'status': 'pass-saved-v161-complete-artwork-inheritance-and-clean-patch',
        'candidate': str(CANDIDATE), 'candidate_sha256': sha(CANDIDATE.read_bytes()),
        'candidate_arm9_sha256': sha(new.read_file('/__arm9__.bin')),
        'canonical_base': str(BASE), 'canonical_base_sha256': CANONICAL_BASELINE_SHA256,
        'previous_sha256': prior_hash, 'profile': PROFILE, 'profile_status': 'experimental',
        'batch_count': 440, 'accepted_batches': manifest['required_batches'],
        'registry_sha256': manifest['release_stack_sha256'], 'builder_sha256': sha(Path('scripts/build_integrated_release.py').read_bytes()),
        'changed_paths_vs_v160': changed, 'changed_paths_vs_canonical': canonical_changed,
        'all_prior_components_resources_stages_and_records_preserved': True,
        'V160_rebuild_exact_after_builder_changes': True,
        'patch': str(patch), 'patch_bytes': patch.stat().st_size, 'patch_sha256': sha(patch.read_bytes()),
        'clean_patch_base_sha256': sha(clean.read_bytes()), 'patch_reconstruction_exact': True,
        'new_logical_labels': 6, 'physical_load_crop_palette_input_and_gameplay_verified': False,
    }
    Path('work/analysis/name_treasure_v161_saved_proof.json').write_text(
        json.dumps(report, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
