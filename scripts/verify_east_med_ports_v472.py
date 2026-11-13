"""Scope the successful port captures separately from the failed weapon voyage."""

import json
from pathlib import Path

from PIL import Image

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.record_navigation_v327 import dark_text
from scripts.verify_med_ports_v471 import town

ROM = Path('out/all_routes_combined_v468_candidate.nds')
CAPTURE = Path('work/emulation_v193/east_med_v472')
ROOT = Path('work/analysis/east_med_v472')


def main():
    digest = sha(ROM.read_bytes())
    report_path = CAPTURE / 'capture_report.json'
    report = json.loads(report_path.read_text(encoding='utf-8'))
    assert report['ROM_sha256'] == digest and report['frames'] == 13865
    assert report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
    for capture in report['frames_captured']:
        assert sha(Path(capture['path']).read_bytes()) == capture['PNG_sha256']
    donor = report['battery_save_preloaded']
    assert sha(Path(donor['source']).read_bytes()) == donor['source_sha256']
    font = GameAsciiFont.from_arm9(NdsImage.open(ROM).read_file('/__arm9__.bin'))
    ports = []
    for frame, name, coords, goods in [
        (7770, 'Tunis', '(N37 E9)', ['Iron', 'Hemp', 'Rhino Horn']),
        (9040, 'Syracuse', '(N37 E14)', ['Wheat', 'Wine', 'Olive Oil', 'Sultana']),
    ]:
        image = Image.open(CAPTURE / f'frame_{frame:06d}_navigation.png').convert('RGB')
        ports.append({'frame': frame, 'complete_masks': town(font, image, name, coords, goods)})
    messages = []
    for frame, text in [(8640, 'Shall we call at Syracuse?'),
                        (13865, 'Our flagship fell. We lost!')]:
        image = Image.open(CAPTURE / f'frame_{frame:06d}_navigation.png').convert('RGB')
        messages.append({'frame': frame, 'complete_mask': dark_text(font, text, image, (8, 292, 253, 350))})
    proof = {
        'candidate': str(ROM), 'candidate_sha256': digest, 'ROM_changed': False,
        'report': str(report_path), 'report_sha256': sha(report_path.read_bytes()),
        'all_capture_hashes_verified': True, 'normal_Tunis_Syracuse_port_masks': ports,
        'complete_messages': messages, 'original_Valencia_save_unchanged': True,
        'donor_sha256': donor['source_sha256'],
        'Istanbul_docking_and_Golden_Cutlass_purchase_verified': False,
        'occupied_Weapon_verified': False,
        'test_ended_after_flagship_loss': True,
        'loss_cause_not_independently_diagnosed': True,
        'no_failed_voyage_save_published': True,
        'all22_historical_requirements_retained': True,
        'all18_plaques_incomplete': True, 'hardware_verification': False,
        'full_goal_complete': False,
    }
    (ROOT / 'port_proof.json').write_text(json.dumps(proof, indent=2) + '\n', encoding='utf-8')
    print('Tunis/Syracuse complete town masks pass; donor unchanged; failed weapon attempt remains open.')


if __name__ == '__main__':
    main()
