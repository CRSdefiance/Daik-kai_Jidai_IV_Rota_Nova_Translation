"""Verify saved V143 tribute output and complete inherited ROM components."""

import json
from pathlib import Path

from dk4tool.patch.common_tribute_release import apply_release
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from scripts.register_grand_race_help_v134 import components


def main():
    parent = Path('out/all_routes_combined_v142_candidate.nds')
    path = Path('out/all_routes_combined_v143_candidate.nds')
    if sha(parent.read_bytes()) != 'c7691fd1455d89f7231cf5616689e4905f0141b6a939670c1550fb6a68f919e4':
        raise ValueError('Complete V142 parent ROM differs')
    before, after = [components(NdsImage.open(p)) for p in (parent, path)]
    cp, ap = '/COMMON/MESFILE.DK4', '/__arm9__.bin'
    common, arm9, report = apply_release(before[cp], before[ap], 'translations/common_tribute_release_v1.json')
    if after != {**before, cp: common, ap: arm9}:
        raise ValueError('Saved V143 changes unrelated inherited ROM components')
    manuscript = json.loads(Path('translations/common_tribute_repairs_manuscript_v2.json').read_text(encoding='utf-8'))
    expected = {r['message_id']: r['english'].removesuffix('{PAD}').encode('cp932') for r in manuscript['records']}
    old = common_message_entries(before[cp], before[ap], clean=False)
    new = common_message_entries(common, arm9, clean=False)
    for a, b in zip(old, new, strict=True):
        if ((a.message_id, a.block, a.record_index) != (b.message_id, b.block, b.record_index)
                or b.text.rstrip(b' ') != expected.get(b.message_id, a.text.rstrip(b' '))):
            raise ValueError('Saved native selection loses text, leading/final characters or identity')
    manifest = json.loads(path.with_suffix('.manifest.json').read_text(encoding='utf-8'))
    inherited = json.loads(parent.with_suffix('.manifest.json').read_text(encoding='utf-8'))
    registry_path = Path('translations/release_stack.json')
    registry = json.loads(registry_path.read_text(encoding='utf-8'))
    if (manifest['profile'] != 'all-routes-unified-v143' or manifest['batches'] != inherited['batches']
            or manifest['candidate_sha256'] != sha(path.read_bytes())
            or manifest['base_sha256'] != registry['canonical_baseline']['sha256']
            or manifest['release_stack_sha256'] != sha(registry_path.read_bytes())):
        raise ValueError('V143 manifest ancestry, stack or candidate identity differs')
    report.update({'candidate_sha256': sha(path.read_bytes()), 'all_native_entries_checked': len(new),
                   'inherited_batches_preserved': len(manifest['batches']),
                   'all_other_rom_components_byte_exact': True, 'gameplay_accepted': False})
    Path('work/analysis/common_tribute_v143_saved_rom_proof.json').write_text(
        json.dumps(report, indent=2) + '\n', encoding='utf-8')
    print(f'Saved V143 verifies {len(new)} native selections and {len(manifest["batches"])} inherited batches; all other components exact.')


if __name__ == '__main__':
    main()
