"""Register complete fleet labels after all V148 layers."""

import copy
import json
from pathlib import Path

from dk4tool.patch.fleet_name_release import apply_release
from dk4tool.rom.nds import NdsImage


def main():
    registry = Path('translations/release_stack.json')
    stack = json.loads(registry.read_text(encoding='utf-8'))
    if 'all-routes-unified-v149' in stack['profiles']:
        raise ValueError('V149 already registered; inspect current state')
    config = 'translations/fleet_name_release_v1.json'
    apply_release(NdsImage.open('out/all_routes_combined_v148_candidate.nds').read_file('/__arm9__.bin'), config)
    profile = copy.deepcopy(stack['profiles']['all-routes-unified-v148'])
    profile['fleet_name_release'] = config
    profile['note'] = ('Complete V148 stack plus full Pirate %s and Unidentified fleet labels; '
                       '456 connected native captain/name/formatter/pixel cases and ten reviewed panels '
                       'cover two mapped displays. Gameplay, live eligibility and other consumers pending.')
    stack['profiles']['all-routes-unified-v149'] = profile
    registry.write_text(json.dumps(stack, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f'V149 registered with all {len(profile["batches"])} inherited batches.')


if __name__ == '__main__':
    main()
