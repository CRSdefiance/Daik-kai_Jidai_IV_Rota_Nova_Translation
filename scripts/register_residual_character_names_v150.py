"""Register Vels/Akaboo after every V149 stage."""

import copy
import json
from pathlib import Path

from dk4tool.patch.residual_character_name_release import apply_release
from dk4tool.rom.nds import NdsImage


def main():
    registry = Path('translations/release_stack.json')
    stack = json.loads(registry.read_text(encoding='utf-8'))
    if 'all-routes-unified-v150' in stack['profiles']:
        raise ValueError('V150 already registered; inspect current state')
    config = 'translations/residual_character_names_release_v1.json'
    apply_release(NdsImage.open('out/all_routes_combined_v149_candidate.nds').read_file('/__arm9__.bin'), config)
    profile = copy.deepcopy(stack['profiles']['all-routes-unified-v149'])
    profile['residual_character_names_release'] = config
    profile['note'] = ('Complete V149 stack plus source-faithful Vels and phonetic Akaboo labels; '
                       '207 native name getters, four paired rows and four fleet rasters verified. '
                       'Older role fidelity and physical gameplay remain pending.')
    stack['profiles']['all-routes-unified-v150'] = profile
    registry.write_text(json.dumps(stack, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f'V150 registered with all {len(profile["batches"])} inherited batches.')


if __name__ == '__main__':
    main()
