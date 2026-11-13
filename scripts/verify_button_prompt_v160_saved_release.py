"""Verify complete V159 preservation and the exact clean-ROM V160 patch."""

import json
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.xdelta import apply_xdelta, make_xdelta
from dk4tool.rom.nds import NdsImage
from scripts.build_integrated_release import (
    CANONICAL_BASELINE_SHA256,
    RELEASE_STACK_PATH,
    accepted_batch_paths,
    load_release_stack,
    resolve_release_batches,
    rom_files,
    verify_golden_content,
)
from scripts.research_button_prompt import ARCHIVE, LOOSE, ROM, SOURCE_ROM, make

CANDIDATE = Path('out/all_routes_combined_v160_candidate.nds')
PROFILE = 'all-routes-unified-v160'


def main():
    if sha(ROM.read_bytes()) != SOURCE_ROM:
        raise ValueError('Exact V159 comparison source required')
    clean_path = Path('work/clean.nds')
    if sha(clean_path.read_bytes()) != 'f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d':
        raise ValueError('Wrong clean patch source')
    old, new = NdsImage.open(ROM), NdsImage.open(CANDIDATE)
    old_manifest = json.loads(ROM.with_suffix('.manifest.json').read_text(encoding='utf-8'))
    manifest = json.loads(CANDIDATE.with_suffix('.manifest.json').read_text(encoding='utf-8'))
    stack = load_release_stack()
    base = Path(manifest['base_rom'])
    if (sha(base.read_bytes()) != CANONICAL_BASELINE_SHA256
            or manifest['base_sha256'] != CANONICAL_BASELINE_SHA256
            or manifest['candidate_sha256'] != sha(CANDIDATE.read_bytes())
            or manifest['profile'] != PROFILE
            or manifest['release_stack_sha256'] != sha(RELEASE_STACK_PATH.read_bytes())
            or manifest['batches'] != [str(p) for p in resolve_release_batches(PROFILE, [], stack)]
            or manifest['required_batches'] != [str(p) for p in accepted_batch_paths(stack)]
            or len(manifest['batches']) != 437
            or manifest['batches'][:435] != old_manifest['batches']
            or not all(manifest['checks'].values())):
        raise ValueError('V160 manifest/source/complete batch/check invariants differ')
    before, after = rom_files(old), rom_files(new)
    changed = sorted(p for p in before.keys() | after.keys() if before.get(p) != after.get(p))
    if changed != sorted([LOOSE, ARCHIVE]):
        raise ValueError('V160 changed inherited ARM9, route, COMMON or unrelated resources')
    canonical = NdsImage.open(base)
    canonical_files = rom_files(canonical)
    canonical_changed = sorted(p for p in canonical_files.keys() | after.keys()
                               if canonical_files.get(p) != after.get(p))
    if (manifest['changed_paths'] != canonical_changed
            or canonical_changed != sorted(old_manifest['changed_paths'] + [LOOSE, ARCHIVE])):
        raise ValueError('Complete canonical changed paths differ')
    if manifest['relocations'] != old_manifest['relocations']:
        raise ValueError('An inherited terminal stage or relocation report changed')
    for path, records in old_manifest['changed_records'].items():
        if manifest['changed_records'][path] != records:
            raise ValueError('Inherited changed-record lineage differs: ' + path)
    expected_loose, expected_archive, _, _ = make(old)
    if new.read_file(LOOSE) != expected_loose or new.read_file(ARCHIVE) != expected_archive:
        raise ValueError('Saved graphics differ from reviewed exact paired artwork')
    if (manifest['changed_records'][LOOSE] != ['DK4_PRESS_A_BUTTON_GRAPHIC_V1']
            or manifest['changed_records'][ARCHIVE] != ['DK4_PRESS_A_BUTTON_EMBEDDED_GRAPHIC_V1']):
        raise ValueError('Paired graphic changed records differ')
    verify_golden_content(canonical, new)
    patch = CANDIDATE.with_suffix('.xdelta')
    reconstruction = Path('work/analysis/button_prompt_v160_patch_reconstruction.nds')
    make_xdelta(clean_path, CANDIDATE, patch)
    apply_xdelta(clean_path, patch, reconstruction)
    if reconstruction.read_bytes() != CANDIDATE.read_bytes():
        raise ValueError('Clean-ROM patch does not reproduce saved V160 exactly')
    report = {
        'status': 'pass-saved-v160-paired-graphics-and-exact-clean-patch',
        'candidate': str(CANDIDATE), 'candidate_sha256': sha(CANDIDATE.read_bytes()),
        'candidate_arm9_sha256': sha(new.read_file('/__arm9__.bin')),
        'canonical_base': str(base), 'canonical_base_sha256': CANONICAL_BASELINE_SHA256,
        'previous_rom_sha256': SOURCE_ROM, 'profile': PROFILE, 'profile_status': 'experimental',
        'release_stack_sha256': manifest['release_stack_sha256'], 'batch_count': 437,
        'required_accepted_batches': manifest['required_batches'],
        'changed_paths_vs_v159': changed, 'changed_paths_vs_canonical': canonical_changed,
        'all_inherited_components_files_stages_and_records_exact': True,
        'exact_reviewed_paired_artwork': True, 'canonical_menu_graphic_checks_pass': True,
        'patch': str(patch), 'patch_bytes': patch.stat().st_size, 'patch_sha256': sha(patch.read_bytes()),
        'patch_base_sha256': sha(clean_path.read_bytes()), 'patch_reconstruction_exact': True,
        'physical_gameplay_input_palette_and_cold_boot_verified': False,
    }
    Path('work/analysis/button_prompt_v160_saved_proof.json').write_text(
        json.dumps(report, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
