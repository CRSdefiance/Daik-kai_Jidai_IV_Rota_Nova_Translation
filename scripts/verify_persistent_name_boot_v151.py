"""Verify saved combined boot repair, complete preservation and exact patch."""

import json
from pathlib import Path

from ndspy.code import MainCodeFile

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.persistent_name_boot_release import apply_release, transform
from dk4tool.patch.xdelta import apply_xdelta, make_xdelta
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from scripts.probe_persistent_name_arm7_boot_overlap import BASE, STAGE, execute
from scripts.register_grand_race_help_v134 import components


def main():
    parent = Path('out/all_routes_combined_v150_candidate.nds')
    candidate = Path('out/all_routes_combined_v151_candidate.nds')
    if sha(parent.read_bytes()) != '3a1ff1f8f1734ba41c24057cee160b6b5aa2bdbc9c38dc08da8ce896dd972a8e':
        raise ValueError('Exact preserved V150 comparison required')
    before, after = [components(NdsImage.open(p)) for p in (parent, candidate)]
    im = NdsImage.open(candidate)
    arm9, report = apply_release(before['/__arm9__.bin'],
                                'translations/persistent_name_boot_release_v1.json',
                                bytes(im.rom.arm7), im.rom.arm7RamAddress)
    if after != {**before, '/__arm9__.bin': arm9}:
        raise ValueError('Boot repair changes unrelated ROM content')
    changed9 = bytearray(before['/__arm9__.bin'])
    changed9[0x8E4] ^= 1
    changed7 = bytearray(im.rom.arm7)
    changed7[0] ^= 1
    rejected = []
    for label, input9, input7, address7 in (
        ('altered_startup_source', bytes(changed9), bytes(im.rom.arm7), im.rom.arm7RamAddress),
        ('altered_arm7_source', before['/__arm9__.bin'], bytes(changed7), im.rom.arm7RamAddress),
        ('changed_arm7_load_address', before['/__arm9__.bin'], bytes(im.rom.arm7), im.rom.arm7RamAddress + 4),
    ):
        try:
            transform(input9, input7, address7)
        except ValueError:
            rejected.append(label)
        else:
            raise ValueError('Unreviewed boot source/address was accepted')
    payload = bytes(MainCodeFile(before['/__arm9__.bin'], BASE).sections[3].data)
    native = execute(arm9, bytes(im.rom.arm7), im.rom.arm7RamAddress, STAGE + 1504, payload)
    if (native['arm7_source_changed_bytes_after_arm9_autoload'] != 0
            or not all(s['matches_original'] for s in native['arm7_native_loaded_sections'])
            or not native['repaired_pool_matches_complete_payload']
            or not native['repair_returns_with_stack_preserved']):
        raise ValueError('Saved candidate loses cross-CPU ownership or complete startup copy')
    old = common_message_entries(before['/COMMON/MESFILE.DK4'], before['/__arm9__.bin'], clean=False)
    new = common_message_entries(after['/COMMON/MESFILE.DK4'], after['/__arm9__.bin'], clean=False)
    if old != new or len(new) != 3668:
        raise ValueError('COMMON selections differ')
    manifest = json.loads(candidate.with_suffix('.manifest.json').read_text(encoding='utf-8'))
    stack = json.loads(Path('translations/release_stack.json').read_text(encoding='utf-8'))
    expected_batches = [str(Path(p)) for p in stack['profiles']['all-routes-unified-v151']['batches']]
    inherited = json.loads(parent.with_suffix('.manifest.json').read_text(encoding='utf-8'))
    if (manifest['profile'] != 'all-routes-unified-v151' or manifest['batches'] != expected_batches
            or manifest['batches'] != inherited['batches'] or len(expected_batches) != 435
            or manifest['candidate_sha256'] != sha(candidate.read_bytes())
            or manifest['release_stack_sha256'] != sha(Path('translations/release_stack.json').read_bytes())
            or manifest['base_sha256'] != stack['canonical_baseline']['sha256']):
        raise ValueError('Complete registered batch stack differs')
    clean = Path('work/clean.nds')
    if sha(clean.read_bytes()) != 'f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d':
        raise ValueError('Clean patch input differs')
    patch = candidate.with_suffix('.xdelta')
    rebuilt = Path('work/analysis/persistent_name_boot_v151_patch_roundtrip.nds')
    make_xdelta(clean, candidate, patch)
    apply_xdelta(clean, patch, rebuilt)
    if rebuilt.read_bytes() != candidate.read_bytes():
        raise ValueError('V151 patch reconstruction differs')
    report.update({'candidate_sha256': sha(candidate.read_bytes()),
                   'patch_sha256': sha(patch.read_bytes()), 'patch_bytes': patch.stat().st_size,
                   'patch_roundtrip_byte_exact': True, 'all_other_components_byte_exact': True,
                   'common_selections_preserved': len(new), 'inherited_batches_preserved': 435,
                   'physical_boot_verified': False})
    report['saved_native_boot_copy'] = native
    report['negative_source_checks_rejected'] = rejected
    Path('work/analysis/persistent_name_boot_v151_saved_proof.json').write_text(
        json.dumps(report, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
