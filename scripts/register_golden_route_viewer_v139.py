"""Register the full viewer after every preceding V138 release component."""

import copy
import json
from pathlib import Path

from dk4tool.patch.golden_route_viewer_release import CONFIG, apply_release
from dk4tool.rom.nds import NdsImage


def main():
    source = NdsImage.open('out/all_routes_combined_v138_candidate.nds').read_file('/__arm9__.bin')
    apply_release(source, CONFIG)
    path = Path('translations/release_stack.json')
    stack = json.loads(path.read_text(encoding='utf-8'))
    profile = copy.deepcopy(stack['profiles']['all-routes-unified-v138'])
    if 'golden_route_viewer_release' in profile:
        raise ValueError('V138 already contains a Golden Route viewer stage')
    profile['golden_route_viewer_release'] = CONFIG.as_posix()
    profile['note'] = ('All preceding V138 layers, unchanged COMMON rebuild and full scene captions, '
                       'followed by six complete Golden Route viewer labels. Experimental; physical gameplay pending.')
    stack['profiles']['all-routes-unified-v139'] = profile
    path.write_text(json.dumps(stack, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f'V139 registered: unchanged {len(profile["batches"])} batches, caption stage and complete Golden Route viewer stage.')


if __name__ == '__main__':
    main()
