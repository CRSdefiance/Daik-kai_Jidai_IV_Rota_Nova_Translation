"""Register reviewed companion message after every inherited V146 stage."""

import copy
import json
from pathlib import Path

from dk4tool.patch.available_companions_release import apply_release
from dk4tool.rom.nds import NdsImage


def main():
    registry = Path('translations/release_stack.json')
    stack = json.loads(registry.read_text(encoding='utf-8'))
    if 'all-routes-unified-v147' in stack['profiles']:
        raise ValueError('V147 already registered; inspect current state')
    config = 'translations/available_companions_release_v1.json'
    apply_release(NdsImage.open('out/all_routes_combined_v146_candidate.nds').read_file('/__arm9__.bin'), config)
    profile = copy.deepcopy(stack['profiles']['all-routes-unified-v146'])
    profile['available_companions_release'] = config
    profile['note'] = 'Complete V146 stack plus full natural-English empty eligible-companion message; all neighboring Options/format owners preserved. Native layout reviewed; physical gameplay pending.'
    stack['profiles']['all-routes-unified-v147'] = profile
    registry.write_text(json.dumps(stack, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f'V147 registered with all {len(profile["batches"])} inherited batches.')


if __name__ == '__main__':
    main()
