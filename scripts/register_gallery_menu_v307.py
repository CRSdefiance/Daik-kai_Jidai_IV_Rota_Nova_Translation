"""Register the complete inherited release with source-verified Gallery labels."""

import copy
import json
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts.prepare_gallery_menu_v307 import CONFIG, ROOT


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def main():
    proof = read(ROOT / 'native_proof.json')
    config = read(CONFIG)
    assert proof['target_arm9_sha256'] == config['target_arm9_sha256']
    assert len(proof['native_flag_cases']) == 16 and len(proof['native_label_glyph_cases']) == 3
    config['verification_evidence_sha256'] = {str(ROOT / 'native_proof.json'): sha((ROOT / 'native_proof.json').read_bytes())}
    config['status'] = 'experimental-native-labels-and-gates-verified-current-Gallery-popup-pending'
    CONFIG.write_text(json.dumps(config, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    path = Path('translations/release_stack.json')
    stack = read(path)
    parent = stack['profiles']['all-routes-unified-v305']
    profile = copy.deepcopy(parent)
    profile['gallery_menu_labels_release'] = str(CONFIG)
    profile['status'] = 'experimental'
    profile['note'] = ('Full V305 inherited stack plus three source-verified Gallery labels: Ruins, Characters, Event Scenes. '
                       'All native gates/allocations/pointers unchanged; current actual popup verification pending. '
                       'All18 plaque audits and legacy/Gallery collection gates remain open; Online low-resolution images exempt.')
    previous = stack['profiles'].get('all-routes-unified-v307')
    assert previous is None or previous == profile
    stack['profiles']['all-routes-unified-v307'] = profile
    assert profile['batches'] == parent['batches']
    path.write_text(json.dumps(stack, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print('V307 registered with all470 inherited batches and three fixed Gallery strings.')


if __name__ == '__main__':
    main()
