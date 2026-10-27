"""Complete actual help glyphs, constructed links and ordinary history controls."""

import json
import struct
from pathlib import Path

from PIL import Image

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.verify_confirmed_name_widget_pixels_v198 import complete_mask

ROOT = Path('work/analysis/trade_help_release_v430')
ROM = Path('out/all_routes_combined_v430_candidate.nds')
FIRST = Path('work/emulation_v193/trade_help_v430')
HISTORY = Path('work/emulation_v193/trade_help_history_v430')
PLAN = Path('work/analysis/trade_help_v429/page_proposal.json')
HISTORY_FRAMES = (24000, 24400)
COLORS = ((123, 246, 123), (213, 214, 213), (106, 157, 246))
FRAMES = {143: (FIRST, 21600), 148: (FIRST, 22600),
          152: (HISTORY, 23200), 191: (FIRST, 22000),
          192: (HISTORY, 24000), 193: (FIRST, 22400)}


def read(path):
    return json.loads(path.read_text(encoding='utf-8'))


def main():
    rom = NdsImage.open(ROM)
    digest = sha(ROM.read_bytes())
    arm = rom.read_file('/__arm9__.bin')
    font = GameAsciiFont.from_arm9(arm)
    plan = read(PLAN)
    pages = {p['topic_id']: p for p in plan['pages']}
    reports = {}
    for folder in (FIRST, HISTORY):
        report = read(folder / 'capture_report.json')
        assert report['ROM_sha256'] == digest and report['cold_boot']
        assert not report['savestate_loaded'] and not report['callback_errors']
        for row in report['frames_captured']:
            assert sha(Path(row['path']).read_bytes()) == row['PNG_sha256']
        reports[str(folder)] = report
    cases = []
    for topic, (folder, frame) in FRAMES.items():
        image_path = folder / f'frame_{frame:06d}_navigation.png'
        image = Image.open(image_path).convert('RGB')
        lines = []
        for row, text in enumerate(pages[topic]['visible_lines']):
            y = 192 if row == 0 else 216 + (row - 1) * 16
            ink = 0
            for column, char in enumerate(text):
                if char == ' ':
                    continue
                matches = []
                for color in COLORS:
                    try:
                        count, _bounds = complete_mask(font, char, image, column * 6, y, color)
                        matches.append(count)
                    except ValueError:
                        pass
                assert len(matches) == 1, (topic, row, column, char, matches)
                ink += matches[0]
            lines.append({'text': text, 'origin': [0, y], 'complete_ink_pixels': ink})
        snapshot = folder / f'frame_{frame:06d}_arm9_ram.bin'
        ram = snapshot.read_bytes()
        snapshot_row = next(r for r in reports[str(folder)]['read_only_pause_RAM_snapshots'] if r['frame'] == frame)
        assert sha(ram) == snapshot_row['sha256']
        vtable = struct.unpack_from('<I', arm, 0x7D40C)[0]
        child = struct.unpack_from('<I', arm, 0x7D488)[0]
        parents = []
        for offset in range(0, len(ram) - 0x6B0, 4):
            if struct.unpack_from('<I', ram, offset)[0] != vtable:
                continue
            count, depth = [struct.unpack_from('<I', ram, offset + field)[0] for field in (0x660, 0x6A8)]
            if depth > 15 or count != len(pages[topic]['links']):
                continue
            history = struct.unpack_from('<16I', ram, offset + 0x668)
            if history[depth] != topic:
                continue
            destinations = []
            for n in range(count):
                at = offset + 0xA0 + n * 0x5C
                assert struct.unpack_from('<I', ram, at)[0] == child
                destinations.append(struct.unpack_from('<I', ram, at + 8)[0])
            assert destinations == [r['id'] for r in pages[topic]['links']]
            parents.append({'address': offset + 0x02000000, 'history_depth': depth,
                            'history': list(history), 'constructed_link_destinations': destinations})
        assert len(parents) == 1, (topic, parents)
        cases.append({'topic_id': topic, 'frame': frame, 'capture': str(image_path),
                      'capture_sha256': sha(image_path.read_bytes()), 'complete_lines': lines,
                      'all_first_interior_final_glyphs_exact': True, 'actual_HELP_parent': parents[0]})
    # Same page and selection return exactly after original L/R history controls.
    a = Image.open(HISTORY / f'frame_{HISTORY_FRAMES[0]:06d}_navigation.png').convert('RGB')
    b = Image.open(HISTORY / f'frame_{HISTORY_FRAMES[1]:06d}_navigation.png').convert('RGB')
    assert a.tobytes() == b.tobytes()
    release = read(ROOT / 'release_proof.json')
    assert release['candidate_sha256'] == digest
    release['actual_cold_boot_navigation_pending'] = False
    release['actual_complete_HELP_topic_cases'] = cases
    release['actual_Link_child_creation_and_original_destinations_verified'] = True
    release['actual_L_previous_R_next_history_page_pixels_exact'] = True
    release['native_font_preview_and_actual_glyph_pixels_verified'] = True
    release['unselected_Japanese_and_generic_HELP_articles_still_pending'] = True
    (ROOT / 'release_proof.json').write_text(json.dumps(release, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'actual_complete_articles': len(cases),
                      'actual_original_link_widgets': sum(len(pages[t]['links']) for t in FRAMES),
                      'history_return_pixels_exact': True}))


if __name__ == '__main__':
    main()
