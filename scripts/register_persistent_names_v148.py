"""Register reserved persistent names after the complete V147 stack."""

import copy
import json
from pathlib import Path

from dk4tool.patch.persistent_name_release import apply_release
from dk4tool.rom.nds import NdsImage


def main():
    registry = Path('translations/release_stack.json')
    stack = json.loads(registry.read_text(encoding='utf-8'))
    if 'all-routes-unified-v148' in stack['profiles']:
        raise ValueError('V148 already registered; inspect current state')
    config = 'translations/persistent_name_release_v1.json'
    apply_release(NdsImage.open('out/all_routes_combined_v147_candidate.nds').read_file('/__arm9__.bin'), config)
    profile = copy.deepcopy(stack['profiles']['all-routes-unified-v147'])
    profile['persistent_name_release'] = config
    profile['note'] = ('Complete V147 stack plus separately reserved persistent item/entity names, '
                       'restored native DTCM scratch, 239 repaired references and ten complete '
                       'Square Shopkeeper names. Native persistence/consumer/layout reviewed; gameplay pending.')
    stack['profiles']['all-routes-unified-v148'] = profile
    registry.write_text(json.dumps(stack, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f'V148 registered with all {len(profile["batches"])} inherited batches.')


if __name__ == '__main__':
    main()
