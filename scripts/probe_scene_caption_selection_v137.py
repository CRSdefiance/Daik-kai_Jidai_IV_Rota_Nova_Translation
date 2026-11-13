"""Execute every saved caption's actual native selection/centering/wrapper."""

import json
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.execute_scene_caption_selection import execute
from scripts.inventory_common_scene_caption_duplicates import CURRENT, CURRENT_SHA


def main():
    if sha(CURRENT.read_bytes()) != CURRENT_SHA:
        raise ValueError('Pinned combined candidate differs')
    path = Path('work/analysis/common_scene_caption_duplicates_v137.json')
    inventory = json.loads(path.read_text(encoding='utf-8'))
    if inventory['candidate_sha256'] != CURRENT_SHA or inventory['caption_count'] != 164:
        raise ValueError('Complete scene caption inventory required')
    arm9 = NdsImage.open(CURRENT).read_file('/__arm9__.bin')
    cases = []
    for row in inventory['captions']:
        case = execute(arm9, row['table_start'], row['index'],
                       inventory['route_caption_counts'][str(row['route_index'])])
        if bytes.fromhex(case['full_text_hex']) != bytes.fromhex(row['current_hex']) + b'\0':
            raise ValueError('Native consumer loses complete inventoried caption bytes')
        cases.append({'route_index': row['route_index'], **case})
    proof = {'status': 'pass-native-scene-caption-selection-centering-wrapper-with-draw-contracts',
             'candidate_sha256': CURRENT_SHA, 'arm9_sha256': sha(arm9),
             'inventory_sha256': sha(path.read_bytes()), 'case_count': len(cases),
             'cases': cases, 'runtime_verified': False,
             'limitations': ['Actual selection/strlen/centering/wrapper, explicit init/raster/destroy contracts.',
                            'No proof of the separate COMMON consumer; full scene composition and gameplay pending.']}
    Path('work/analysis/scene_caption_native_selection_v137_proof.json').write_text(json.dumps(proof, indent=2) + '\n')
    print('All 164 saved native caption selections preserve full bytes, NUL, x/y/style and caller state.')


if __name__ == '__main__':
    main()
