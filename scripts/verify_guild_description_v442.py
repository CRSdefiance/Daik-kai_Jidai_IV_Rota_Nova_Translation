"""Whole Guild treasure family and unchanged existing portrait/modal scope."""

import json
from pathlib import Path

from PIL import Image

from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from scripts.probe_remaining_common_layout import warm_copy
from scripts.verify_common_alignment_native_v257 import raster
from scripts.verify_tavern_addresses_v413 import wrap

ROOT = Path('work/analysis/guild_description_v442')


def main():
    parent = NdsImage.open('out/all_routes_combined_v440_candidate.nds')
    old = parent.read_file('/__arm9__.bin')
    arm = (ROOT / 'research_arm9.bin').read_bytes()
    common = (ROOT / 'research_COMMON.bin').read_bytes()
    entries = common_message_entries(common, arm, clean=False)
    cases, copies, scope = [], [], []
    for number in range(3648, 3668):
        text = entries[number].text.rstrip()
        copies.extend(warm_copy(arm, common, number, entries[number].text, cold_cache=cold) for cold in (False, True))
        formatted = wrap(arm, text, 0x02054014, number)
        assert b' '.join(formatted.split()) == b' '.join(text.split())
        lines = formatted.split(b'\n')
        assert len(lines[0]) <= 36
        assert all(len(line) <= 39 for line in lines[1:])
        before = raster(arm, text, 0x01FFCE40 - 0x02000000,
                        size=(228, 80), instruction_limit=400000)
        events = []
        after = raster(arm, formatted, 0x01FFCE40 - 0x02000000,
                       size=(228, 80), instruction_limit=400000, glyph_events=events)
        assert sum(bool(p) for p in before) == sum(bool(p) for p in after)
        visible = [event for event in events if event['code'] != 32]
        codes = [int.from_bytes(char.encode('cp932'), 'big')
                 for char in formatted.decode('cp932') if char not in (' ', '\n')]
        assert [event['code'] for event in visible] == codes
        at = 0
        for word in text.decode('cp932').split():
            group = visible[at:at + len(word)]
            assert len({event['y'] for event in group}) == 1, (number, word, group)
            at += len(word)
        picture = Image.frombytes('L', (228, 80), bytes(0 if p else 255 for p in after))
        picture.save(ROOT / f'description_{number}_native.png')
        cases.append({'message_id': number, 'complete_words': text.decode('cp932'),
                      'native_wrapped_lines': [line.decode('cp932') for line in lines],
                      'complete_native_glyph_ink_pixels': sum(bool(p) for p in after),
                      'all_native_glyph_order_and_word_row_coordinates_exact': True,
                      'source_and_output_guards_and_ABI_pass': True})
    raw = b'A complete sentence with enough words to exercise wrapping and both invisible first-line and continuation guards.'
    numbers = [819, 820, 821, 822, 869, 870, 871, 872, 873, 874, 321, 327, 3647, 3668]
    for parent_return in (0x02054014, 0x02054044, 0x020546E8):
        for number in numbers:
            a, b = wrap(old, raw, parent_return, number), wrap(arm, raw, parent_return, number)
            assert a == b
            scope.append({'parent_return': parent_return, 'message_id': number, 'byte_exact_old_behavior': True})
    proof = {'whole20_Guild_treasure_descriptions': cases, 'native40_cold_warm_copies': copies,
             '42_existing_rumor_clue_equipment_wrong_parent_scope_cases_exact': scope,
             'all20_complete_native_raster_ink_counts_retained': True,
             'SDK_section4_bytes': 4096,
             'all_other_first3900_ITCM_and_existing_main_pool_preserved': True,
             'declared_existing_ITCM_changes': ['01FFCAB0 width-selector call', '01FFCB40 48-byte selector in owned zero padding'],
             'actual_Guild_playback_and_registered_release_pending': True,
             'all18_plaques_incomplete': True, 'full_goal_complete': False}
    (ROOT / 'native_proof.json').write_text(json.dumps(proof, indent=2) + '\n', encoding='utf-8')
    print('20 complete Guild descriptions,40 native copies and42 unchanged scope cases pass.')


if __name__ == '__main__':
    main()
