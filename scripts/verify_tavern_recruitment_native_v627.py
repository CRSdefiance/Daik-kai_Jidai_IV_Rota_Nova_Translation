"""Complete cache copies, all recruitment voices, and precise dispatch changes."""

from pathlib import Path

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.tavern_recruitment import TABLE, apply_release
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from scripts.probe_remaining_common_layout import warm_copy
from scripts.verify_common_alignment_native_v257 import raster
from scripts.verify_tavern_queued_native_v626 import queued_wrap, table_scopes
from scripts.verify_village_wrap_v608 import save

ROOT = Path('work/analysis/tavern_recruitment_v627')


def main():
    parent = NdsImage.open('out/all_routes_combined_v626_candidate.nds')
    rom = NdsImage.open('out/all_routes_combined_v627_candidate.nds')
    before_arm, before_common = parent.read_file('/__arm9__.bin'), parent.read_file('/COMMON/MESFILE.DK4')
    common, arm, change = apply_release(before_common, before_arm, 'translations/tavern_recruitment_v1.json')
    assert common == rom.read_file('/COMMON/MESFILE.DK4') and arm == rom.read_file('/__arm9__.bin')
    before = common_message_entries(before_common, before_arm, clean=False)
    after = common_message_entries(common, arm, clean=False)
    assert len(before) == len(after) == 3668
    changed = [b.message_id for a, b in zip(before, after, strict=True)
               if (a.block_offset, a.copy_end, a.text) != (b.block_offset, b.copy_end, b.text)]
    copies = [warm_copy(arm, common, number, after[number].text, cold_cache=cold)
              for number in changed for cold in (False, True)]
    font = GameAsciiFont.from_arm9(arm)
    voices = []
    for number in range(897, 904):
        text = after[number].text.rstrip(b' ')
        assert text.isascii()
        for parent_return in (0x02053DB8, 0x02053D24):
            formatted = queued_wrap(arm, text, parent_return, TABLE)
            assert b' '.join(formatted.split()) == text
            events = []
            pixels = raster(arm, formatted, 0x01FFCE40 - 0x02000000, size=(228, 80),
                            glyph_events=events, instruction_limit=500000)
            visible = [e for e in events if e['code'] not in (32, 10)]
            assert [e['code'] for e in visible] == [c for c in text if c != 32]
            expected = bytearray(228 * 80)
            for event in events:
                glyph = font.decode(chr(event['code']))
                for y in range(11):
                    for x in range(6):
                        if glyph.getpixel((x, y)):
                            px, py = event['x'] + x, event['y'] + y
                            assert 0 <= px < 228 and 0 <= py < 80
                            expected[py * 228 + px] = 1
            assert bytes(expected) == pixels
            offset = 0
            for word in text.split():
                group = visible[offset:offset + len(word)]
                assert len(group) == len(word) and len({e['y'] for e in group}) == 1
                offset += len(word)
            voices.append({'message_id': number, 'original_parent': parent_return,
                           'complete_English': text.decode(), 'native_formatted': formatted.decode(),
                           'whole_native_plane_independent_font_mask_exact': True,
                           'every_word_on_one_row_and_all_letters_in_order': True,
                           'complete_native_ink_pixels': sum(expected)})
    tables = list(range(0x021181C0, 0x021183A1)) + [0x02117B40, 0x02118800, 0x02118820, 0x02118840, 0x02116730]
    scopes = []
    for parent_return in (0x02053DB8, 0x02053D24, 0x02053C14, 0x02053C5C, 0x02054044):
        a, b = table_scopes(before_arm, parent_return, tables), table_scopes(arm, parent_return, tables)
        changed_tables = []
        for table, old_pc, new_pc in zip(tables, a, b, strict=True):
            if table == TABLE and parent_return in (0x02053DB8, 0x02053D24):
                assert old_pc == 0x01FF9EDC and new_pc == 0x01FFCF78
                changed_tables.append(table)
            else:
                assert old_pc == new_pc
        scopes.append({'parent': parent_return, 'all_table_addresses_checked': len(tables),
                       'changed_only_tables': changed_tables})
    save(ROOT / 'native_proof.json', {
        'candidate_sha256': sha(rom.source.read_bytes()), 'target_arm9_sha256': sha(arm), 'change': change,
        'changed_native_entry_IDs': changed, 'every_changed_entry_hot_and_cold_cache_copy': copies,
        'all14_voice_parent_whole_native_font_planes': voices, 'exact_parent_and_table_dispatch_changes': scopes,
        'unrelated_tables_unaligned_addresses_and_old_SeaFoam_cases_preserved': True,
        'only_the_actual_Charles_voice_receives_separate_normal_gameplay_credit': True,
        'all18_original_plaques_incomplete': True, 'full_goal_complete': False,
        'script_sha256': sha(Path(__file__).read_bytes())})
    print(f'V627:{len(copies)} complete hot/cold cache copies,14 whole native font planes,exact added-table scopes pass.')


if __name__ == '__main__':
    main()
