"""Register the cumulative equipment word-wrap stage after live verification."""

import copy
import json
from pathlib import Path

from ndspy.code import MainCodeFile

from dk4tool.patch.equipment_confirmation_wrap import apply_release
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage

ROOT = Path('work/analysis/equipment_wrap_v363')


def main():
    live = Path('work/analysis/equipment_release_v364/research_live_proof.json')
    assert json.loads(live.read_text(encoding='utf-8'))['ordinary_long_item_confirmation_verified']
    source = NdsImage.open('out/all_routes_combined_v360_candidate.nds').read_file('/__arm9__.bin')
    target = (ROOT / 'research_arm9.bin').read_bytes()
    before, after = MainCodeFile(source, 0x02000000), MainCodeFile(target, 0x02000000)
    plan = json.loads((ROOT / 'plan.json').read_text())
    dependencies = [ROOT / 'scope_proof.json', ROOT / 'pixel_proof.json',
                    Path('work/analysis/equipment_confirmation_v362/actual_geometry.json'), live]
    config = {'format': 'dk4-equipment-confirmation-wrap-v1',
              'source_arm9_sha256': sha(source), 'target_arm9_sha256': sha(target),
              'scope': plan['scope'], 'macro_call': 0x54798,
              'expected_call_hex': source[0x54798:0x5479C].hex(),
              'replacement_call_hex': target[0x54798:0x5479C].hex(),
              'original_autoload_length': len(before.sections[4].data),
              'autoload_suffix_hex': bytes(after.sections[4].data[len(before.sections[4].data):]).hex(),
              'dependencies_sha256': {str(p).replace('\\', '/'): sha(p.read_bytes()) for p in dependencies},
              'source_English_unchanged': '%s equipped %s.',
              'Japanese_source': '%sが\n%sを装備しました',
              'all18_plaques_fully_completed': False}
    path = Path('translations/equipment_confirmation_wrap_v1.json')
    path.write_text(json.dumps(config, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    assert apply_release(source, path)[0] == target
    registry = Path('translations/release_stack.json')
    stack = json.loads(registry.read_text(encoding='utf-8'))
    profile = copy.deepcopy(stack['profiles']['all-routes-unified-v360'])
    profile['equipment_confirmation_wrap'] = str(path).replace('\\', '/')
    profile['description'] = 'Full V360 stack plus scoped equipment confirmation word wrapping; experimental.'
    profile['note'] = 'All470 inherited batches and native stages retained; COMMON327 word wrapping verified in ordinary purchase/equip. Graphics and18 plaque variants remain under audit.'
    stack['profiles']['all-routes-unified-v364'] = profile
    registry.write_text(json.dumps(stack, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print('Registered V364 with every V360 batch/native stage and one equipment-only stage.')


if __name__ == '__main__':
    main()
