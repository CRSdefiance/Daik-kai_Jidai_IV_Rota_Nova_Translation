"""Verify saved V156 components, complete lineage and exact clean patch."""

import json
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.movement_notice_release import apply_release
from dk4tool.patch.raphael_system_panel_release import reject_corrupt_panel_selectors
from dk4tool.patch.xdelta import apply_xdelta, make_xdelta
from dk4tool.rom.nds import NdsImage
from scripts.register_grand_race_help_v134 import components


def main():
    candidate = Path('out/all_routes_combined_v156_candidate.nds')
    parent = Path('out/all_routes_combined_v155_candidate.nds')
    clean = Path('work/clean.nds')
    if sha(parent.read_bytes()) != 'd704b60955db30d27b3d48858107096934fd2af08ecd1f3bf3fc2ba4dd884b11':
        raise ValueError('V155 comparison identity differs')
    if sha(clean.read_bytes()) != 'f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d':
        raise ValueError('Clean patch identity differs')
    original = NdsImage.open(parent)
    before, after = components(original), components(NdsImage.open(candidate))
    config_path = 'translations/movement_notices_release_v1.json'
    saved, common, report = apply_release(original, NdsImage.open(clean), config_path)
    if after != {**before, '/__arm9__.bin': saved, '/COMMON/MESFILE.DK4': common}:
        raise ValueError('V156 changes other ROM components')
    reject_corrupt_panel_selectors(after)
    registry_path = Path('translations/release_stack.json')
    registry = json.loads(registry_path.read_text(encoding='utf-8'))
    profile, previous_profile = [registry['profiles'][key] for key in ('all-routes-unified-v156', 'all-routes-unified-v155')]
    manifest = json.loads(candidate.with_suffix('.manifest.json').read_text(encoding='utf-8'))
    previous = json.loads(parent.with_suffix('.manifest.json').read_text(encoding='utf-8'))
    if (profile['status'] != 'experimental' or manifest['profile'] != 'all-routes-unified-v156'
            or manifest['batches'] != [str(Path(p)) for p in profile['batches']]
            or manifest['batches'] != previous['batches'] or len(manifest['batches']) != 435
            or manifest['release_stack_sha256'] != sha(registry_path.read_bytes())
            or manifest['base_sha256'] != registry['canonical_baseline']['sha256']
            or manifest['candidate_sha256'] != sha(candidate.read_bytes())
            or manifest['changed_paths'] != previous['changed_paths']
            or profile['movement_notice_release'] != config_path
            or any(profile[k] != v for k, v in previous_profile.items() if k not in ('note', 'description'))):
        raise ValueError('Complete registered lineage differs')
    stage = manifest['relocations']['/__arm9__.bin']['movement_notices']
    if (stage['release_config_sha256'] != sha(Path(config_path).read_bytes())
            or stage['changed_records'] != report['changed_records']
            or not set(report['arm9_changed_records']) <= set(manifest['changed_records']['/__arm9__.bin'])
            or not {'COMMON_MESSAGE_' + str(mid) for mid in report['common_changed_ids']}
            <= set(manifest['changed_records']['/COMMON/MESFILE.DK4'])):
        raise ValueError('Saved movement manifest coverage differs')
    audit = json.loads(Path('work/analysis/all_route_system_panel_native_audit.json').read_text(encoding='utf-8'))
    if (audit['source_arm9_sha256'] != '21e2be34e965fd17fc56dd18e919e411b7da87a3c8f56f9e7e6fd8c39100940b'
            or audit['failures'] or len(audit['cases']) != 1061 or len(audit['excluded']) != 8
            or audit['source_files_sha256'] != {p: sha(after[p]) for p in audit['source_files_sha256']}):
        raise ValueError('Inherited route panel proof source files differ')
    # Exact transform locks and component equality preserve the modal consumer,
    # fonts and all four route files. The portrait hook delegates all FE paths.
    patch = candidate.with_suffix('.xdelta')
    roundtrip = Path('work/analysis/movement_v156_patch_roundtrip.nds')
    make_xdelta(clean, candidate, patch)
    apply_xdelta(clean, patch, roundtrip)
    if candidate.read_bytes() != roundtrip.read_bytes():
        raise ValueError('Clean patch reconstruction differs')
    report.update({'candidate_sha256': sha(candidate.read_bytes()), 'patch_sha256': sha(patch.read_bytes()),
                   'patch_bytes': patch.stat().st_size, 'patch_roundtrip_exact': True,
                   'canonical_base_sha256': registry['canonical_baseline']['sha256'],
                   'clean_patch_base_sha256': sha(clean.read_bytes()),
                   'all_other_components_byte_exact': True, 'inherited_batches_preserved': 435,
                   'system_panel_routes_fonts_and_consumers_preserved': True,
                   'inherited_native_panel_cases_not_rerun': 1061,
                   'physical_cold_boot_and_full_widget_composition_pending': True})
    Path('work/analysis/movement_v156_saved_proof.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({k: report[k] for k in ('candidate_sha256', 'patch_sha256', 'patch_bytes',
                                           'patch_roundtrip_exact', 'all_other_components_byte_exact')}, indent=2))


if __name__ == '__main__':
    main()
