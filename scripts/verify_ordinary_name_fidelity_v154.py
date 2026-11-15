"""Verify saved V154 changes only reviewed ARM9 names and rebuild its clean patch."""

import json
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.ordinary_name_fidelity_release import apply_release
from dk4tool.patch.raphael_system_panel_release import reject_corrupt_panel_selectors
from dk4tool.patch.xdelta import apply_xdelta, make_xdelta
from dk4tool.rom.nds import NdsImage
from scripts.register_grand_race_help_v134 import components


def main():
    candidate = Path('out/all_routes_combined_v154_candidate.nds')
    parent = Path('out/all_routes_combined_v153_candidate.nds')
    clean = Path('work/clean.nds')
    if sha(parent.read_bytes()) != 'f9cf6468637e0b578088e4b844fea431806de6827add2388b8cae2e214fb4178':
        raise ValueError('V153 comparison identity differs')
    if sha(clean.read_bytes()) != 'f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d':
        raise ValueError('Clean patch identity differs')
    before, after = [components(NdsImage.open(p)) for p in (parent, candidate)]
    saved, report = apply_release(before['/__arm9__.bin'], NdsImage.open(clean).read_file('/__arm9__.bin'),
                                  'translations/ordinary_name_fidelity_release_v1.json')
    if after != {**before, '/__arm9__.bin': saved}:
        raise ValueError('V154 changes other ROM components')
    reject_corrupt_panel_selectors(after)
    registry_path = Path('translations/release_stack.json')
    registry = json.loads(registry_path.read_text(encoding='utf-8'))
    profile = registry['profiles']['all-routes-unified-v154']
    manifest = json.loads(candidate.with_suffix('.manifest.json').read_text(encoding='utf-8'))
    previous = json.loads(parent.with_suffix('.manifest.json').read_text(encoding='utf-8'))
    if (profile['status'] != 'experimental' or manifest['profile'] != 'all-routes-unified-v154'
            or manifest['batches'] != [str(Path(p)) for p in profile['batches']]
            or manifest['batches'] != previous['batches'] or len(manifest['batches']) != 435
            or manifest['release_stack_sha256'] != sha(registry_path.read_bytes())
            or manifest['base_sha256'] != registry['canonical_baseline']['sha256']
            or manifest['candidate_sha256'] != sha(candidate.read_bytes())):
        raise ValueError('Complete registered lineage differs')
    audit = json.loads(Path('work/analysis/all_route_system_panel_native_audit.json').read_text(encoding='utf-8'))
    if (audit['source_arm9_sha256'] != sha(before['/__arm9__.bin']) or audit['failures']
            or len(audit['cases']) != 1061 or len(audit['excluded']) != 8
            or audit['source_files_sha256'] != {p: sha(after[p]) for p in audit['source_files_sha256']}):
        raise ValueError('Inherited panel proof source/files differ')
    # The transform enforces whole main-code preservation outside reviewed
    # pointer/static name spans, heap limit and startup hook; ITCM/DTCM are exact.
    # Consequently the existing panel consumer/font proof is preserved, not rerun.
    patch = candidate.with_suffix('.xdelta')
    roundtrip = Path('work/analysis/ordinary_name_v154_patch_roundtrip.nds')
    make_xdelta(clean, candidate, patch)
    apply_xdelta(clean, patch, roundtrip)
    if candidate.read_bytes() != roundtrip.read_bytes():
        raise ValueError('Clean patch reconstruction differs')
    report.update({'candidate_sha256': sha(candidate.read_bytes()), 'patch_sha256': sha(patch.read_bytes()),
                   'patch_bytes': patch.stat().st_size, 'patch_roundtrip_exact': True,
                   'all_other_components_byte_exact': True, 'inherited_batches_preserved': 435,
                   'system_panel_routes_fonts_and_consumers_preserved': True,
                   'inherited_native_panel_cases_not_rerun': 1061,
                   'physical_cold_boot_and_changed_nameplates_pending': True})
    Path('work/analysis/ordinary_name_v154_saved_proof.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
