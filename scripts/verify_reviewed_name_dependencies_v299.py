"""Verify all shared getters, COMMON copies/glyphs and unchanged HELP evidence."""

import json
from pathlib import Path

from dk4tool.patch.confirmed_character_names import FIELDS
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from scripts.execute_reviewed_name_modal_v299 import execute as modal_execute
from scripts.prepare_reviewed_name_release_v299 import ROOT, read
from scripts.probe_map_tooltip_cp932_pixels import expected_pixels as modal_expected_pixels
from scripts.probe_remaining_common_layout import warm_copy
from scripts.verify_confirmed_name_fields_v198 import accessor
from scripts.verify_ordinary_name_fidelity_research import initialized


def main():
    proof = read(ROOT / 'transform_proof.json')
    arm = (ROOT / 'catalog_arm9_research_only.bin').read_bytes()
    assert sha(arm) == proof['target_file_sha256']['/__arm9__.bin']
    source = NdsImage.open('out/all_routes_combined_v298_candidate.nds').read_file('/__arm9__.bin')
    before, after = initialized(source), initialized(arm)
    expected = {(row[1], row[2]): row[-1].encode('ascii') for row in FIELDS}
    getters = []
    for index in range(207):
        for column, address in ((0, 0x7EB0C), (4, 0x7EAF4), (8, 0x7EADC)):
            old_pointer, old = accessor(source, before, index, address)
            pointer, text = accessor(arm, after, index, address)
            assert pointer == old_pointer and text == expected.get((index, column), old)
            getters.append({'index': index, 'column': column, 'pointer': pointer, 'before_hex': old.hex(), 'after_hex': text.hex()})
    common = (ROOT / 'MESFILE.DK4.research_only').read_bytes()
    entries = common_message_entries(common, arm, clean=False)
    authored = proof['COMMON']['message_IDs']
    neighbors = sorted({n for index in authored for n in (index - 1, index + 1) if n not in authored})
    copies = [warm_copy(arm, common, index, entries[index].text, cold_cache=cold) for index in authored for cold in (False, True)]
    copies.extend(warm_copy(arm, common, index, entries[index].text) for index in neighbors)
    glyphs = []
    font = NdsImage.open('work/clean.nds').read_file('/GRP/KANJI.FNT')
    for index in authored:
        text = entries[index].text
        for mode in (4, 16):
            for portrait in (False, True):
                native = modal_execute(arm, text.decode('cp932'), modal=True, mode=mode,
                                       kanji_font=font, portrait=portrait)
                visible = [e for e in native['glyph_events'] if e['code'] != 32]
                assert [e['code'] for e in visible] == [int.from_bytes(c.encode('cp932'), 'big')
                                                       for c in text.decode('cp932') if c not in ' \n']
                assert all(e['x'] >= 0 and e['y'] >= 0 and e['x'] + (12 if e['kind'] == 'cp932' else 6) <= 256
                           and e['y'] + 12 <= 96 for e in visible)
                assert native['pixels'] == modal_expected_pixels(arm, font, native['glyph_events'], mode, background=9)
                assert {0x548A8, 0xD5160, 0xD5A10, 0xD5A18, 0xD5A2C, 0xD5404, 0xD16B4, 0xD5140} <= set(native['executed_offsets'])
                assert not native['cp932_pixel_painter_is_contract']
                glyphs.append({'message_ID': index, 'complete_text_hex': text.hex(), 'mode': mode, 'portrait': portrait,
                               'visible_glyphs': len([e for e in native['glyph_events'] if e['code'] != 32]),
                               'pixels_sha256': sha(native['pixels']),
                               'complete_first_internal_final_letters_ink_bounds_and_guards_pass': True})
    lookup = {bytes.fromhex(r['key_hex']): r for r in proof['catalog']['records']}
    unintended = []
    for entry in entries:
        for form, key in [('whole', entry.text), ('body', entry.text[1:])]:
            if key in lookup:
                unintended.append({'COMMON_message_ID': entry.message_id, 'form': form,
                                   'route_mask': lookup[key]['route_mask']})
    assert not unintended, unintended
    help_raw = (ROOT / 'HELP.DK4.research_only').read_bytes()
    assert help_raw == Path('work/analysis/help_display_v282/help_navigation_research_only.bin').read_bytes()
    help_display = read('work/analysis/help_display_v282/final_navigation_display_proof.json')
    output = {'format': 'dk4-reviewed-name-dependencies-v299', 'target_ARM9_sha256': sha(arm),
              'native_getter_cases': getters, 'changed_getters': 5, 'unchanged_getters': 616,
              'COMMON_native_copy_cases': copies, 'COMMON_full_native_glyph_cases': glyphs,
              'COMMON_catalog_unintended_matches': unintended,
              'all_HELP_bytes_exact_previous_actual_navigation_fixture': True,
              'previous_HELP_display_proof_sha256': sha(Path('work/analysis/help_display_v282/final_navigation_display_proof.json').read_bytes()),
              'previous_HELP_display_proof_format': help_display.get('format'),
              'fresh_current_HELP_gameplay_pending': True,
              'full_registered_release_and_cold_boot_pending': True,
              'all18_plaque_hint_entries_and_variants_incomplete': True, 'full_goal_complete': False}
    (ROOT / 'dependency_native_proof.json').write_text(json.dumps(output, indent=2) + '\n', encoding='utf-8')
    print(f'621 shared getters; {len(copies)} COMMON warm/cold/neighbor copies; {len(glyphs)} actual modal-pipeline glyph cases; HELP bytes exact.', flush=True)


if __name__ == '__main__':
    main()
