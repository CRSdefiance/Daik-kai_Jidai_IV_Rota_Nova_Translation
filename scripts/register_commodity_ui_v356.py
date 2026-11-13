"""Materialize source-guarded integration records from verified research output."""

import argparse
import copy
import json
from pathlib import Path

from ndspy.code import MainCodeFile

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--target', type=Path, default=Path('work/analysis/commodity_private_market_v354/research_arm9.bin'))
    parser.add_argument('--config', type=Path, default=Path('translations/commodity_ui_release_v1.json'))
    parser.add_argument('--profile', default='all-routes-unified-v356')
    parser.add_argument('--evidence', action='append', default=[])
    args = parser.parse_args()
    source = NdsImage.open('out/all_routes_combined_v342_candidate.nds').read_file('/__arm9__.bin')
    target = args.target.read_bytes()
    a, b = [MainCodeFile(data, 0x02000000) for data in (source, target)]
    town = json.loads(Path('work/analysis/commodity_lazy_canvas_v349/plan.json').read_text())
    market = json.loads(Path('work/analysis/commodity_private_market_v354/plan.json').read_text(encoding='utf-8'))
    ranges = list(town['name_repack']['source_string_regions']) + [[0x15BB40, 0x15BB68]]
    ranges += [[0x15EF18 + i * 12, 0x15EF18 + i * 12 + 4] for i in range(124)]
    ranges += [[field, field + 4] for field in [0xB59AC, 0xB63D4, 0x11A650, 0xBF3DC,
                                               0xC4074, 0xC4078, 0xC407C, *market['scoped_calls'],
                                               *market['corrected_printf_fields'],
                                               *[f for r in market['statuses'] for f in r['pointer_fields']]]]
    ranges += [[0x11A73C + i * 28 + 12, 0x11A73C + i * 28 + 24] for i in range(5)]
    old, new = bytes(a.sections[0].data), bytes(b.sections[0].data)
    patches = []
    settings = set(range(a.codeSettingsOffs, a.codeSettingsOffs + 12))
    offset = 0
    while offset < len(old):
        if old[offset] == new[offset] or offset in settings:
            offset += 1
            continue
        start = offset
        while offset < len(old) and old[offset] != new[offset] and offset not in settings:
            offset += 1
        # Split diff runs at adjacent ownership boundaries when needed.
        while start < offset:
            limits = [hi for lo, hi in ranges if lo <= start < hi]
            assert limits, hex(start)
            end = min(offset, max(limits))
            patches.append({'offset': start, 'expected_hex': old[start:end].hex(), 'replacement_hex': new[start:end].hex()})
            start = end
    dependencies = ['translations/commodity_name_manuscript_v343.json',
                    'work/analysis/commodity_lazy_canvas_v349/proof.json',
                    'work/analysis/commodity_private_market_v354/native_proof.json',
                    'work/analysis/commodity_private_market_v354/live_proof.json',
                    'work/analysis/commodity_private_market_v354/native_printf_proof.json',
                    'work/analysis/commodity_private_market_v354/allocation_census.json', *args.evidence]
    config = {'format': 'dk4-commodity-ui-release-v1', 'source_arm9_sha256': sha(source),
              'target_arm9_sha256': sha(target), 'manuscript': dependencies[0],
              'dependencies_sha256': {p: sha(Path(p).read_bytes()) for p in dependencies},
              'owned_main_ranges': ranges, 'main_section_patches': patches,
              'new_autoload_section': {'ram_address': b.sections[4].ramAddress, 'data_hex': bytes(b.sections[4].data).hex()},
              'printf_pointer_fields': market['corrected_printf_fields'] +
                                      ([0xC4074] if old[0xC4074:0xC4078] != new[0xC4074:0xC4078] else []),
              'full_market_printf_guard': old[0xC4074:0xC4078] != new[0xC4074:0xC4078],
              'price_name_layout': old[0xBF3DC:0xBF3E0] != new[0xBF3DC:0xBF3E0],
              'cargo_format_layout': old[0xC4074:0xC4078] != new[0xC4074:0xC4078],
              'status': 'experimental-other-contexts-and-full-goal-pending'}
    output = args.config
    output.write_text(json.dumps(config, indent=2) + '\n')
    from dk4tool.patch.commodity_ui_release import apply_release

    built, _ = apply_release(source, NdsImage.open('work/clean.nds').read_file('/__arm9__.bin'), output)
    assert built == target
    registry_path = Path('translations/release_stack.json')
    registry = json.loads(registry_path.read_text(encoding='utf-8'))
    profile = copy.deepcopy(registry['profiles']['all-routes-unified-v342'])
    profile['commodity_ui_release'] = str(output)
    profile['note'] = 'Full V342/470-batch stack plus complete commodity names and verified town/market name layouts; remaining graphics and other commodity contexts stay under audit.'
    registry['profiles'][args.profile] = profile
    registry_path.write_text(json.dumps(registry, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print('Registered ' + args.profile + '; reproduced exact research ARM9 without unlock/stock fixtures.')


if __name__ == '__main__':
    main()
