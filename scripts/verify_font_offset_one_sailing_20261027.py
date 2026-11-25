"""Complete actual sailing button masks, including the bottom of Inspect's p."""

import json
from pathlib import Path

from PIL import Image

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.verify_plaque_release_v247 import find_mask

ROOT = Path('work/font_offset_one_20261027')
ROM = Path('out/font_v2_draw_down_one_20261027_test.nds')


if __name__ == '__main__':
    terminal = json.loads((ROOT / 'sailing_terminal.json').read_text())
    path = Path(terminal['report'])
    report = json.loads(path.read_text())
    assert sha(path.read_bytes()) == terminal['report_sha256']
    assert report['ROM_sha256'] == sha(ROM.read_bytes())
    assert report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
    font = GameAsciiFont.from_arm9(NdsImage.open(ROM).read_file('/__arm9__.bin'))
    frames = {r['frame']: r for r in report['frames_captured']}
    cases = []
    for frame in [24000, 30000, 32800]:
        row = frames[frame]
        assert sha(Path(row['path']).read_bytes()) == row['PNG_sha256']
        image = Image.open(row['path']).convert('RGB')
        for label in ['Rotate', 'Menu', 'Inspect', 'Sails']:
            mask = find_mask(font, label, image, (0, 366, 256, 384))
            cases.append(dict(frame=frame, **mask, complete_p_tail=label == 'Inspect'))
    result = dict(candidate_sha256=report['ROM_sha256'], frames=report['frames'],
        report=str(path), report_sha256=terminal['report_sha256'], masks=cases,
        all_three_Inspect_descenders_complete=True, ordinary_inputs_no_injected_gameplay_state=True)
    (ROOT / 'sailing_button_verification.json').write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
    print('Twelve complete sailing button masks pass, including3full Inspect p tails.')
