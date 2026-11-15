"""Verify saved V144 narrow prompts and every complete inherited component."""

import json
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.options_narrow_release import apply_release
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from scripts.register_grand_race_help_v134 import components


def main():
    parent = Path('out/all_routes_combined_v143_candidate.nds')
    path = Path('out/all_routes_combined_v144_candidate.nds')
    if sha(parent.read_bytes()) != '2c4cf489bfaaff8b187744e085a0ee8314dc10e4054048f60e9156cf5d786984':
        raise ValueError('Complete V143 parent ROM differs')
    before, after = [components(NdsImage.open(p)) for p in (parent, path)]
    ap, cp = '/__arm9__.bin', '/COMMON/MESFILE.DK4'
    arm9, report = apply_release(before[ap], 'translations/options_narrow_release_v1.json')
    if after != {**before, ap: arm9}:
        raise ValueError('Saved V144 changes components beyond two reviewed Options slots')
    old = common_message_entries(before[cp], before[ap], clean=False)
    new = common_message_entries(after[cp], after[ap], clean=False)
    if old != new:
        raise ValueError('Saved Options layer changes inherited native COMMON selections')
    manifest = json.loads(path.with_suffix('.manifest.json').read_text(encoding='utf-8'))
    inherited = json.loads(parent.with_suffix('.manifest.json').read_text(encoding='utf-8'))
    registry = Path('translations/release_stack.json')
    stack = json.loads(registry.read_text(encoding='utf-8'))
    if (manifest['profile'] != 'all-routes-unified-v144' or manifest['batches'] != inherited['batches']
            or manifest['candidate_sha256'] != sha(path.read_bytes())
            or manifest['base_sha256'] != stack['canonical_baseline']['sha256']
            or manifest['release_stack_sha256'] != sha(registry.read_bytes())):
        raise ValueError('Saved V144 lineage, stack or candidate identity differs')
    report.update({'candidate_sha256': sha(path.read_bytes()), 'all_native_entries_checked': len(new),
                   'inherited_batches_preserved': len(manifest['batches']),
                   'all_other_rom_components_byte_exact': True, 'gameplay_accepted': False})
    Path('work/analysis/options_narrow_v144_saved_rom_proof.json').write_text(
        json.dumps(report, indent=2) + '\n', encoding='utf-8')
    print(f'Saved V144 preserves all {len(new)} native selections, {len(manifest["batches"])} batches and every other V143 component.')


if __name__ == '__main__':
    main()
