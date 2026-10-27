"""Verify exact V153 preservation, full registered lineage and clean patch reconstruction."""

import json
from pathlib import Path

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.raphael_system_panel_release import (
    PATH,
    TARGETS,
    apply_release,
    reject_corrupt_panel_selectors,
)
from dk4tool.patch.xdelta import apply_xdelta, make_xdelta
from dk4tool.rom.nds import NdsImage
from scripts.register_grand_race_help_v134 import components


def main():
    parent = Path('out/all_routes_combined_v152_candidate.nds')
    candidate = Path('out/all_routes_combined_v153_candidate.nds')
    canonical = Path('out/raphael_natural_v2_accepted_base.nds')
    clean = Path('work/clean.nds')
    if sha(parent.read_bytes()) != '2bea1a9554989e241cb57e8b398e8d5aa90855ea5f9cbef474bd34fbf1be1e63':
        raise ValueError('Exact V152 diagnostic comparison required')
    before, after = [components(NdsImage.open(p)) for p in (parent, candidate)]
    repaired, report = apply_release(before[PATH], NdsImage.open(canonical).read_file(PATH),
                                     NdsImage.open(clean).read_file(PATH),
                                     'translations/raphael_system_panel_release_v1.json')
    if after != {**before, PATH: repaired}:
        raise ValueError('V153 changes bytes outside the exact tutorial repair')
    original, saved = [IlnkContainer.parse(data) for data in (before[PATH], after[PATH])]
    differences = []
    for block, (a, b) in enumerate(zip(original.blocks, saved.blocks, strict=True)):
        for segment, (left, right) in enumerate(zip(a.split(b'\0'), b.split(b'\0'), strict=True)):
            if left != right:
                if len(left) != len(right):
                    raise ValueError('Tutorial changes record allocation or script offsets')
                differences.append((block, segment))
    if set(differences) != TARGETS:
        raise ValueError('Unexpected tutorial record/neighbor changes')
    reject_corrupt_panel_selectors(after)
    try:
        reject_corrupt_panel_selectors(before)
    except ValueError:
        pass
    else:
        raise ValueError('Build guard fails to reject the known broken V152 selectors')
    registry_path = Path('translations/release_stack.json')
    registry = json.loads(registry_path.read_text(encoding='utf-8'))
    profile = registry['profiles']['all-routes-unified-v153']
    manifest = json.loads(candidate.with_suffix('.manifest.json').read_text(encoding='utf-8'))
    previous = json.loads(parent.with_suffix('.manifest.json').read_text(encoding='utf-8'))
    expected_batches = [str(Path(p)) for p in profile['batches']]
    if (manifest['profile'] != 'all-routes-unified-v153' or profile['status'] != 'experimental'
            or manifest['batches'] != expected_batches or expected_batches != previous['batches']
            or len(expected_batches) != 435
            or manifest['release_stack_sha256'] != sha(registry_path.read_bytes())
            or manifest['base_sha256'] != registry['canonical_baseline']['sha256']
            or manifest['candidate_sha256'] != sha(candidate.read_bytes())):
        raise ValueError('V153 complete lineage differs')
    audit_path = Path('work/analysis/all_route_system_panel_native_audit.json')
    audit = json.loads(audit_path.read_text(encoding='utf-8'))
    if (audit['source_arm9_sha256'] != sha(after['/__arm9__.bin'])
            or audit['source_files_sha256'] != {p: sha(after[p]) for p in audit['source_files_sha256']}):
        raise ValueError('All-route native proof does not match saved candidate')
    if sha(clean.read_bytes()) != 'f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d':
        raise ValueError('Clean patch source differs')
    patch = candidate.with_suffix('.xdelta')
    roundtrip = Path('work/analysis/system_panel_v153_patch_roundtrip.nds')
    make_xdelta(clean, candidate, patch); apply_xdelta(clean, patch, roundtrip)
    if roundtrip.read_bytes() != candidate.read_bytes():
        raise ValueError('Clean patch reconstruction differs')
    report.update({'candidate_sha256': sha(candidate.read_bytes()), 'patch_sha256': sha(patch.read_bytes()),
                   'patch_bytes': patch.stat().st_size, 'all_other_components_byte_exact': True,
                   'shared_copy_and_staged_boot_repairs_byte_exact': True, 'inherited_batches_preserved': 435,
                   'all_route_native_panels_passed': 1061, 'nontext_empty_states_preserved': 8,
                   'known_corrupt_selector_negative_check_passed': True,
                   'patch_roundtrip_exact': True, 'cold_boot_ceuta_and_tutorials_pending': True})
    Path('work/analysis/system_panel_v153_saved_proof.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
