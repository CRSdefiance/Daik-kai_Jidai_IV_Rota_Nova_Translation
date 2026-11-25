"""Prepare source-reviewed Gallery labels and unchanged native unlock predicates."""

import json
from pathlib import Path

from dk4tool.patch.gallery_menu_labels import transform
from dk4tool.rom.nds import NdsImage

ROOT = Path('work/analysis/gallery_menu_v307')
CONFIG = Path('translations/gallery_menu_labels_release_v1.json')


def main():
    ROOT.mkdir(parents=True, exist_ok=True)
    current, clean, canonical = [NdsImage.open(p) for p in ('out/all_routes_combined_v305_candidate.nds',
                                                         'work/clean.nds', 'out/raphael_natural_v2_accepted_base.nds')]
    source = current.read_file('/__arm9__.bin')
    target, proof = transform(source, clean.read_file('/__arm9__.bin'), canonical.read_file('/__arm9__.bin'))
    assert target[0x41DA4:0x41E00] == source[0x41DA4:0x41E00]
    assert target[0x46DFC:0x46E30] == source[0x46DFC:0x46E30]
    assert target[0xED708:0xED7E8] == source[0xED708:0xED7E8]
    (ROOT / 'research_arm9.bin').write_bytes(target)
    config = {'format': 'dk4-gallery-menu-label-release-v1',
              'source_arm9_sha256': proof['source_arm9_sha256'], 'target_arm9_sha256': proof['target_arm9_sha256'],
              'status': 'experimental-source-native-caller-pixel-and-current-gameplay-verification-pending',
              'source_review': {'Ruins': '史跡: historic sites; use established Ruins terminology from the actual no-ruins message.',
                                'Characters': '登場人物: characters in the game, including people beyond crew members.',
                                'Event Scenes': 'イベントシーン: event scenes; match the existing native heading and descriptions.'}}
    CONFIG.write_text(json.dumps(config, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    (ROOT / 'preparation.json').write_text(json.dumps(proof, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print('Three complete labels in original8/12/16-byte slots; all pointer owners and native unlock predicates unchanged.')


if __name__ == '__main__':
    main()
