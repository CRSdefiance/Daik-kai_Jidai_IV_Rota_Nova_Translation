"""Actual market labels, complete first/final glyphs and neighboring pixels."""

import json
import struct
from pathlib import Path

from ndspy.code import MainCodeFile
from PIL import Image

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_commodity_market_native_v350 import wrapped

ROOT = Path('work/analysis/commodity_private_market_v354')


def exact_label(image, font, text, origin, box, advance=5):
    x0, y0 = origin
    expected = {(x0 + n * advance + x, y0 + line * 12 + y)
                for line, row in enumerate(text.split('\n')) for n, c in enumerate(row)
                for y in range(11) for x in range(6) if font.decode(c).getpixel((x, y))}
    left, top, right, bottom = box
    assert all(left <= x < right and top <= y < bottom for x, y in expected)
    actual = {(x, y) for y in range(top, bottom) for x in range(left, right)
              if image.getpixel((x, y)) == (230, 230, 230)}
    assert actual == expected, (text, len(expected - actual), len(actual - expected))
    return {'text': text, 'origin': origin, 'box': box, 'exact_ink_pixels': len(expected),
            'first_internal_final_letters_and_blank_cells_exact': True}


def main():
    arm = (ROOT / 'research_arm9.bin').read_bytes()
    sections = MainCodeFile(arm, 0x02000000).sections
    font = GameAsciiFont.from_arm9(arm)
    payload = bytes(sections[4].data)
    parent = Image.open('work/emulation_v193/commodity_v349_market_buy/frame_017600_final.png').convert('RGB')
    captures = []
    for variant, name in [('normal', 'China'), ('long', 'Black Glacier Sword')]:
        folder = Path('work/emulation_v193/commodity_private_market_v354_' + variant)
        report = json.loads((folder / 'capture_report.json').read_text())
        fixture = ROOT / ('research_only_' + variant + '_Maria.nds')
        assert report['ROM_sha256'] == sha(fixture.read_bytes())
        assert report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
        image = Image.open(folder / 'frame_017600_final.png').convert('RGB')
        labels = [exact_label(image, font, name + '\n  Crafts 100%', [144, 126], [144, 126, 256, 162]),
                  exact_label(image, font, wrapped(name), [8, 304], [8, 304, 80, 328])]
        changed = [(x, y) for y in range(384) for x in range(256)
                   if image.getpixel((x, y)) != parent.getpixel((x, y))]
        assert all((144 <= x < 256 and 126 <= y < 162) or
                   (8 <= x < 80 and 304 <= y < 328) for x, y in changed)
        itcm = bytearray((folder / 'native_state/arm9_itcm.bin').read_bytes()[0x4000:0x4000 + len(payload)])
        pointer = struct.unpack_from('<I', itcm, 0x680)[0]
        assert 0x023A5AA0 <= pointer < pointer + 4096 <= 0x023E0000
        struct.pack_into('<I', itcm, 0x680, 0)
        assert bytes(itcm) == payload
        ram = (folder / 'final_arm9_ram.bin').read_bytes()
        assert struct.unpack_from('<3I', ram, pointer - 0x02000000) == (4, 46, 36)
        assert struct.unpack_from('<3I', ram, 0x2BD83C) == (4, 116, 96)
        earlier_matches = 0
        earlier_parent = Path('work/emulation_v193/commodity_market_v350_' + variant)
        for p in folder.glob('frame_*_cold_boot.png'):
            previous = earlier_parent / p.name
            if int(p.name.split('_')[1]) <= 16800 and previous.exists():
                assert Image.open(p).tobytes() == Image.open(previous).tobytes(), p
                earlier_matches += 1
        captures.append({'fixture': str(fixture), 'ROM_sha256': report['ROM_sha256'],
                         'capture_report': str(folder / 'capture_report.json'),
                         'capture_report_sha256': sha((folder / 'capture_report.json').read_bytes()),
                         'labels': labels, 'changed_pixels': len(changed),
                         'all_other_final_pixels_including_trade_values_and_icons_exact': True,
                         'earlier_full_frames_exact': earlier_matches,
                         'exact_autoload_payload_except_one_expected_mutable_pointer': True,
                         'private_image_header': pointer, 'old_shared_header_preserved': True})
    for p in ['translations/graphics_completion_campaign_v1.json', 'translations/graphics_visual_audit_v150.json']:
        plaques = json.loads(Path(p).read_text(encoding='utf-8'))['plaque_style_v247']['ongoing_plaque_inventory']
        assert len(plaques) == 18 and all(not row['fully_completed'] for row in plaques)
    proof = {'actual_captures': captures, 'actual_ordinary_market_navigation': True,
             'Maria_visibility_and_long_name_substitution_are_research_fixtures': True,
             'not_legitimate_unlock_or_normal_rare_stock_availability': True,
             'Shortage_and_Trending_actual_eligible_states_still_pending': True,
             'cargo_price_contexts_repeat_scene_lifetime_and_registered_release_pending': True,
             'all18_plaques_incomplete': True, 'full_goal_complete': False}
    (ROOT / 'live_proof.json').write_text(json.dumps(proof, indent=2) + '\n')
    print('Both actual market labels complete; category/percent exact, other final pixels unchanged.')


if __name__ == '__main__':
    main()
