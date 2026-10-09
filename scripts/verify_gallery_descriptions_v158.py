"""Verify saved combined V158, full lineage and the exact clean-ROM patch."""

import json
from pathlib import Path

from dk4tool.patch.gallery_description_release import apply_release
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.raphael_system_panel_release import reject_corrupt_panel_selectors
from dk4tool.patch.xdelta import apply_xdelta, make_xdelta
from dk4tool.rom.nds import NdsImage
from scripts.register_grand_race_help_v134 import components


def main():
    candidate = Path('out/all_routes_combined_v158_candidate.nds')
    parent = Path('out/all_routes_combined_v157_candidate.nds')
    clean = Path('work/clean.nds')
    if sha(parent.read_bytes()) != '23822596bd2fe8b486ef61f944a8077693dd1bd07c445761cc51388c985924fe':
        raise ValueError('V157 comparison identity differs')
    if sha(clean.read_bytes()) != 'f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d':
        raise ValueError('Clean patch identity differs')
    original = NdsImage.open(parent)
    before, after = components(original), components(NdsImage.open(candidate))
    config_path = 'translations/gallery_description_release_v1.json'
    saved, report = apply_release(original, NdsImage.open(clean), config_path)
    if after != {**before, '/__arm9__.bin': saved}:
        raise ValueError('V158 changes other ROM components')
    reject_corrupt_panel_selectors(after)
    registry_path = Path('translations/release_stack.json')
    registry = json.loads(registry_path.read_text(encoding='utf-8'))
    profile, previous_profile = [registry['profiles'][key] for key in ('all-routes-unified-v158', 'all-routes-unified-v157')]
    manifest = json.loads(candidate.with_suffix('.manifest.json').read_text(encoding='utf-8'))
    previous = json.loads(parent.with_suffix('.manifest.json').read_text(encoding='utf-8'))
    if (profile['status'] != 'experimental' or manifest['profile'] != 'all-routes-unified-v158'
            or manifest['batches'] != [str(Path(p)) for p in profile['batches']]
            or manifest['batches'] != previous['batches'] or len(manifest['batches']) != 435
            or manifest['required_batches'] != previous['required_batches']
            or manifest['release_stack_sha256'] != sha(registry_path.read_bytes())
            or manifest['base_sha256'] != registry['canonical_baseline']['sha256']
            or manifest['candidate_sha256'] != sha(candidate.read_bytes())
            or manifest['changed_paths'] != previous['changed_paths']
            or profile['gallery_description_release'] != config_path
            or any(profile[k] != v for k, v in previous_profile.items() if k not in ('note', 'description'))):
        raise ValueError('Complete registered V158 lineage differs')
    stage = manifest['relocations']['/__arm9__.bin']['gallery_descriptions']
    if (stage['release_config_sha256'] != sha(Path(config_path).read_bytes())
            or stage['changed_records'] != report['changed_records']
            or not set(report['changed_records']) <= set(manifest['changed_records']['/__arm9__.bin'])):
        raise ValueError('Saved gallery manifest coverage differs')
    for path, stages in previous['relocations'].items():
        for key, value in stages.items():
            if manifest['relocations'][path][key] != value:
                raise ValueError('Inherited terminal stage manifest changed')
    audit = json.loads(Path('work/analysis/all_route_system_panel_native_audit.json').read_text(encoding='utf-8'))
    if (audit['source_arm9_sha256'] != '21e2be34e965fd17fc56dd18e919e411b7da87a3c8f56f9e7e6fd8c39100940b'
            or audit['failures'] or len(audit['cases']) != 1061 or len(audit['excluded']) != 8
            or audit['source_files_sha256'] != {p: sha(after[p]) for p in audit['source_files_sha256']}):
        raise ValueError('Inherited route panel proof source files differ')
    # The deterministic transform locks all original bytes outside the listed
    # ten Gallery pointers and safe staged pool loading. All formatter code is exact.
    # Modal consumer, all four route files and fonts are exact to V157.
    patch = candidate.with_suffix('.xdelta')
    roundtrip = Path('work/analysis/gallery_v158_patch_roundtrip.nds')
    make_xdelta(clean, candidate, patch)
    apply_xdelta(clean, patch, roundtrip)
    if candidate.read_bytes() != roundtrip.read_bytes():
        raise ValueError('Clean patch reconstruction differs')
    report.update({'candidate_sha256': sha(candidate.read_bytes()), 'patch_sha256': sha(patch.read_bytes()),
                   'patch_bytes': patch.stat().st_size, 'patch_roundtrip_exact': True,
                   'arm9_sha256': sha(saved), 'common_sha256': sha(after['/COMMON/MESFILE.DK4']),
                   'canonical_base_sha256': registry['canonical_baseline']['sha256'],
                   'clean_patch_base_sha256': sha(clean.read_bytes()),
                   'all_other_components_byte_exact': True, 'inherited_batches_preserved': 435,
                   'system_panel_routes_fonts_and_consumers_preserved': True,
                   'inherited_native_panel_cases_not_rerun': 1061,
                   'physical_cold_boot_and_full_gameplay_pending': True})
    Path('work/analysis/gallery_v158_saved_proof.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({k: report[k] for k in ('candidate_sha256', 'arm9_sha256', 'patch_sha256', 'patch_bytes',
                                           'patch_roundtrip_exact', 'all_other_components_byte_exact')}, indent=2))


if __name__ == '__main__':
    main()
