"""Register complete captions after the unchanged V137 combined release stack."""

import copy
import json
from pathlib import Path

from dk4tool.patch.scene_caption_release import CONFIG, apply_release
from dk4tool.rom.nds import NdsImage


def main():
    source = NdsImage.open('out/all_routes_combined_v137_candidate.nds').read_file('/__arm9__.bin')
    apply_release(source, CONFIG)
    path = Path('translations/release_stack.json')
    stack = json.loads(path.read_text(encoding='utf-8'))
    profile = copy.deepcopy(stack['profiles']['all-routes-unified-v137'])
    if 'scene_caption_release' in profile:
        raise ValueError('V137 source already contains a caption transformation')
    profile['scene_caption_release'] = CONFIG.as_posix()
    profile['note'] = ('All preceding V137 layers and unchanged COMMON rebuild, followed by all 164 '
                       'complete native scene captions and class-scoped narrow renderer. Experimental; gameplay pending.')
    stack['profiles']['all-routes-unified-v138'] = profile
    path.write_text(json.dumps(stack, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f'V138 registered: all {len(profile["batches"])} preceding batch entries plus strict complete caption stage.')


if __name__ == '__main__':
    main()
