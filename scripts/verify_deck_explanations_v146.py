"""Verify saved V146 inheritance, connected Deck pixels and exact patch reconstruction."""

import json
from pathlib import Path

from dk4tool.patch.deck_explanation_release import apply_release
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.xdelta import apply_xdelta, make_xdelta
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from scripts.probe_deck_explanation_connected import execute, pointer_consumers
from scripts.probe_deck_explanation_sources import ROWS
from scripts.register_grand_race_help_v134 import components


def main():
    parent = Path('out/all_routes_combined_v145_candidate.nds')
    candidate = Path('out/all_routes_combined_v146_candidate.nds')
    if sha(parent.read_bytes()) != 'f6f5e44fef6317706c8cadd9495ba1ccbe7a47b1fb3fe5d0839ee2facef241ab':
        raise ValueError('Complete V145 parent differs')
    before, after = [components(NdsImage.open(path)) for path in (parent, candidate)]
    ap, cp = '/__arm9__.bin', '/COMMON/MESFILE.DK4'
    arm9, report = apply_release(before[ap], 'translations/deck_explanation_release_v1.json')
    if after != {**before, ap: arm9}:
        raise ValueError('Saved V146 changes components beyond reviewed Deck pool/fields')
    old = common_message_entries(before[cp], before[ap], clean=False)
    new = common_message_entries(after[cp], after[ap], clean=False)
    if old != new:
        raise ValueError('Saved Deck release changes inherited COMMON selections')
    manifest = json.loads(candidate.with_suffix('.manifest.json').read_text(encoding='utf-8'))
    inherited = json.loads(parent.with_suffix('.manifest.json').read_text(encoding='utf-8'))
    registry = Path('translations/release_stack.json')
    stack = json.loads(registry.read_text(encoding='utf-8'))
    digest = sha(candidate.read_bytes())
    if (manifest['profile'] != 'all-routes-unified-v146' or manifest['batches'] != inherited['batches']
            or manifest['candidate_sha256'] != digest
            or manifest['base_sha256'] != stack['canonical_baseline']['sha256']
            or manifest['release_stack_sha256'] != sha(registry.read_bytes())):
        raise ValueError('Saved V146 identity or lineage differs')
    moves = {m['old_offset']: m for m in report['moves']}
    native = [execute(after[ap], room, state, moves[offset]) for room, offset, *_ in ROWS for state in (0, 255)]
    pool = json.loads(Path('translations/deck_explanation_pool_v1.json').read_text(encoding='utf-8'))
    pointers = pointer_consumers(after[ap], {'moves': report['moves'], 'references': pool['all_byte_position_address_candidates']})
    clean = Path('work/clean.nds')
    if sha(clean.read_bytes()) != 'f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d':
        raise ValueError('Clean patch source differs')
    patch = candidate.with_suffix('.xdelta')
    reconstructed = Path('work/analysis/deck_explanations_v146_patch_roundtrip.nds')
    make_xdelta(clean, candidate, patch)
    apply_xdelta(clean, patch, reconstructed)
    if reconstructed.read_bytes() != candidate.read_bytes():
        raise ValueError('V146 patch reconstruction differs')
    report.update({'candidate_sha256': digest, 'patch_sha256': sha(patch.read_bytes()),
                   'patch_bytes': patch.stat().st_size, 'patch_roundtrip_byte_exact': True,
                   'all_native_entries_checked': len(new), 'inherited_batches_preserved': len(manifest['batches']),
                   'all_other_rom_components_byte_exact': True, 'saved_native_connected_cases': native,
                   'saved_native_pointer_consumer_cases': pointers, 'gameplay_accepted': False})
    Path('work/analysis/deck_explanations_v146_saved_proof.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({k: v for k, v in report.items() if k not in ('moves', 'saved_native_connected_cases', 'saved_native_pointer_consumer_cases')}, indent=2))


if __name__ == '__main__':
    main()
