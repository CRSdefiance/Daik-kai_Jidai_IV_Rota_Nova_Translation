"""Saved character-name candidate preservation, inherited consumers and exact patch."""

import json
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.residual_character_name_release import apply_release
from dk4tool.patch.xdelta import apply_xdelta, make_xdelta
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from scripts.probe_available_companions import empty_branch, parenthesized_format
from scripts.probe_options_narrow_prompts import execute, respond
from scripts.register_grand_race_help_v134 import components


def main():
    parent = Path('out/all_routes_combined_v149_candidate.nds')
    candidate = Path('out/all_routes_combined_v150_candidate.nds')
    if sha(parent.read_bytes()) != '7261f62222a055b7265fe93e6afc1471926c997b792fdbe722a5d70daee950ad':
        raise ValueError('Exact complete V149 parent required')
    before, after = [components(NdsImage.open(path)) for path in (parent, candidate)]
    ap, cp = '/__arm9__.bin', '/COMMON/MESFILE.DK4'
    arm9, report = apply_release(before[ap], 'translations/residual_character_names_release_v1.json')
    if after != {**before, ap: arm9}:
        raise ValueError('Saved V150 changes components beyond reviewed two character-name owners')
    old = common_message_entries(before[cp], before[ap], clean=False)
    new = common_message_entries(after[cp], after[ap], clean=False)
    if old != new or len(new) != 3668:
        raise ValueError('Saved V150 changes inherited COMMON selections')
    manifest = json.loads(candidate.with_suffix('.manifest.json').read_text(encoding='utf-8'))
    inherited = json.loads(parent.with_suffix('.manifest.json').read_text(encoding='utf-8'))
    registry = Path('translations/release_stack.json')
    stack = json.loads(registry.read_text(encoding='utf-8'))
    digest = sha(candidate.read_bytes())
    if (manifest['profile'] != 'all-routes-unified-v150' or manifest['batches'] != inherited['batches']
            or manifest['candidate_sha256'] != digest
            or manifest['base_sha256'] != stack['canonical_baseline']['sha256']
            or manifest['release_stack_sha256'] != sha(registry.read_bytes())):
        raise ValueError('Saved V150 identity or complete lineage differs')
    report['saved_native_empty_branch'] = empty_branch(arm9)
    report['saved_native_options_cases'] = [execute(arm9, kind, flags) for kind in ('sailing', 'reports')
                                           for flags in (0, 1, 2, 3, 255)]
    report['saved_native_options_responses'] = [respond(arm9, kind, flags, accepted)
                                               for kind in ('sailing', 'reports')
                                               for flags in (0, 1, 2, 3, 255) for accepted in (False, True)]
    report['saved_native_parenthesized_cases'] = [parenthesized_format(arm9, name)
                                                 for name in ('', 'A', 'Even', 'Fleet', '海', 'Indigo海')]
    clean = Path('work/clean.nds')
    if sha(clean.read_bytes()) != 'f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d':
        raise ValueError('Clean patch source differs')
    patch = candidate.with_suffix('.xdelta')
    reconstructed = Path('work/analysis/residual_character_names_v150_patch_roundtrip.nds')
    make_xdelta(clean, candidate, patch)
    apply_xdelta(clean, patch, reconstructed)
    if reconstructed.read_bytes() != candidate.read_bytes():
        raise ValueError('V150 patch reconstruction differs')
    report.update({'candidate_sha256': digest, 'patch_sha256': sha(patch.read_bytes()),
                   'patch_bytes': patch.stat().st_size, 'patch_roundtrip_byte_exact': True,
                   'all_native_entries_checked': len(new), 'inherited_batches_preserved': len(manifest['batches']),
                   'all_other_rom_components_byte_exact': True, 'gameplay_accepted': False})
    Path('work/analysis/residual_character_names_v150_saved_proof.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({k: v for k, v in report.items() if k != 'moves' and not k.startswith('saved_native_')}, indent=2))


if __name__ == '__main__':
    main()
