"""Source-locked confirmation label, complete native raster and inherited profile."""

import copy
import json
from pathlib import Path

from dk4tool.patch.auto_move_caption import transform
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.verify_modal_cursor_native_v272 import verify_ascii

ROOT = Path('work/analysis/auto_move_caption_v316')
CONFIG = Path('translations/auto_move_caption_release_v1.json')


def main():
    ROOT.mkdir(parents=True, exist_ok=True)
    source, clean, canonical = [NdsImage.open(path).read_file('/__arm9__.bin') for path in
                               ('out/all_routes_combined_v309_candidate.nds', 'work/clean.nds',
                                'out/raphael_natural_v2_accepted_base.nds')]
    target, plan = transform(source, clean, canonical)
    (ROOT / 'research_arm9.bin').write_bytes(target)
    proof = {**plan, 'native_complete_label_raster': verify_ascii(target, b'Auto Move'),
             'source_actual_capture': 'work/emulation_v193/ordinary_voyage_v315/frame_006000_navigation.png',
             'source_reading_meaning_reviewed': True, 'matches_existing_port_command': 'Auto Move',
             'actual_current_confirmation_pending': True, 'full_goal_complete': False}
    proof_path = ROOT / 'native_proof.json'
    proof_path.write_text(json.dumps(proof, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    config = {'format': 'dk4-auto-move-caption-release-v1', 'source_arm9_sha256': sha(source),
              'target_arm9_sha256': sha(target), 'source_review': '自動移動 means automatic movement; match the established Auto Move command.',
              'verification_evidence_sha256': {str(proof_path): sha(proof_path.read_bytes())},
              'status': 'experimental-source-native-verified-current-confirmation-pending'}
    CONFIG.write_text(json.dumps(config, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print('Complete Auto Move label in original12 bytes; native raster passes; current replay pending.')


def register():
    path = Path('translations/release_stack.json')
    stack = json.loads(path.read_text(encoding='utf-8'))
    profile = copy.deepcopy(stack['profiles']['all-routes-unified-v309'])
    profile['auto_move_caption_release'] = str(CONFIG)
    profile['status'] = 'experimental'
    profile['note'] = ('Complete V309 inheritance plus the observed Auto Move confirmation label in its original12-byte slot. '
                       'Source/native raster verified; actual ordinary save/confirmation replay pending. '
                       'All18 plaques and broader graphics gates remain open; Online low resolution images exempt.')
    previous = stack['profiles'].get('all-routes-unified-v316')
    assert previous is None or previous == profile
    stack['profiles']['all-routes-unified-v316'] = profile
    path.write_text(json.dumps(stack, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    main()
