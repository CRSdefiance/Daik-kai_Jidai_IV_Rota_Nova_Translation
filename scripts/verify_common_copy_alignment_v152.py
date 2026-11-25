"""Verify saved V152, complete translation preservation, manifest and patch."""

import json
from pathlib import Path

from dk4tool.patch.common_copy_alignment_release import apply_release
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.xdelta import apply_xdelta, make_xdelta
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from scripts.register_grand_race_help_v134 import components


def main():
    parent = Path('out/all_routes_combined_v151_candidate.nds')
    candidate = Path('out/all_routes_combined_v152_candidate.nds')
    if sha(parent.read_bytes()) != 'd61241e3f9d29debcc41cedcf7824aa06ac36e5e07643c714e7b045465c40345':
        raise ValueError('Exact V151 diagnostic comparison required')
    before, after = [components(NdsImage.open(path)) for path in (parent, candidate)]
    repaired, report = apply_release(before['/__arm9__.bin'], 'translations/common_copy_alignment_release_v1.json')
    if after != {**before, '/__arm9__.bin': repaired}:
        raise ValueError('Shared copy repair changes unrelated components')
    old, new = [common_message_entries(files['/COMMON/MESFILE.DK4'], files['/__arm9__.bin'], clean=False)
                for files in (before, after)]
    if old != new or len(new) != 3668:
        raise ValueError('Shared copy repair changes message selection or text')
    manifest = json.loads(candidate.with_suffix('.manifest.json').read_text(encoding='utf-8'))
    inherited = json.loads(parent.with_suffix('.manifest.json').read_text(encoding='utf-8'))
    registry = Path('translations/release_stack.json')
    stack = json.loads(registry.read_text(encoding='utf-8'))
    profile = stack['profiles']['all-routes-unified-v152']
    expected = [str(Path(p)) for p in profile['batches']]
    if (manifest['profile'] != 'all-routes-unified-v152' or profile['status'] != 'experimental'
            or manifest['batches'] != expected or expected != inherited['batches'] or len(expected) != 435
            or manifest['base_sha256'] != stack['canonical_baseline']['sha256']
            or manifest['release_stack_sha256'] != sha(registry.read_bytes())
            or manifest['candidate_sha256'] != sha(candidate.read_bytes())):
        raise ValueError('Saved candidate does not match the complete registered lineage')
    clean = Path('work/clean.nds')
    if sha(clean.read_bytes()) != 'f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d':
        raise ValueError('Clean patch input changed')
    patch = candidate.with_suffix('.xdelta')
    rebuilt = Path('work/analysis/common_copy_alignment_v152_patch_roundtrip.nds')
    make_xdelta(clean, candidate, patch)
    apply_xdelta(clean, patch, rebuilt)
    if rebuilt.read_bytes() != candidate.read_bytes():
        raise ValueError('Clean-ROM patch reconstruction differs')
    report.update({'candidate_sha256': sha(candidate.read_bytes()),
                   'patch_sha256': sha(patch.read_bytes()), 'patch_bytes': patch.stat().st_size,
                   'other_components_byte_exact': True, 'common_selections_preserved': 3668,
                   'inherited_batches_preserved': 435, 'patch_roundtrip_exact': True,
                   'cold_boot_and_user_regression_screens_pending': True})
    Path('work/analysis/common_copy_alignment_v152_saved_proof.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
