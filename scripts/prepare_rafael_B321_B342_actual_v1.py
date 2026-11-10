"""Select focused native display, menu, name and pagination samples."""
from scripts.audit_story_glyph_consistency import load, save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.seal_rafael_B321_B342_clean_v1 import ROOT, SEALED, STYLES, MENUS


SELECTION = ROOT / 'focused_selection_v1.json'


def main():
    assert not SELECTION.exists()

    def speech(block, *indices):
        return [dict(speech=f'DK4_MES_B{block}_R{index:04d}') for index in indices]

    def style(block, offset):
        return dict(style=dict(block=block, source_command_offset=offset, expected_style=4))

    def menu(block, offset):
        return dict(menu=dict(block=block, source_command_offset=offset))

    sequence = [
        *speech(321, 6, 9, 12), *speech(322, 39, 44, 48),
        *speech(323, 51, 55, 64, 68),
        *speech(326, 6, 9, 13, 16), *speech(328, 6, 10),
        *speech(330, 10), *speech(331, 6, 14, 18, 22, 26),
        *speech(325, 89, 94, 99), menu(325, 748), *speech(325, 118),
        style(325, 840), *speech(325, 142, 188),
        style(324, 8), *speech(327, 86), menu(327, 720), *speech(327, 102, 113),
        *speech(329, 71, 95, 100), menu(329, 790), *speech(329, 119),
        style(329, 866), *speech(329, 142, 212, 219),
        *speech(332, 91, 95), menu(332, 856), *speech(332, 110),
        style(332, 918), *speech(332, 140, 144),
        menu(332, 1756), style(332, 1804), menu(332, 1984),
        style(332, 2026), *speech(332, 320),
        *speech(333, 97), menu(333, 736), *speech(333, 112),
        *speech(335, 5, 13), *speech(336, 5, 9, 18, 96),
        *speech(337, 17, 36, 95), *speech(339, 5),
        *speech(342, 59, 66, 70, 75, 14, 111, 114, 118, 121, 135),
    ]
    drafts = SEALED / 'sealed_drafts.json'
    draft_ids = {row['id'] for row in load(drafts)['records']}
    assert all(action['speech'] in draft_ids for action in sequence if 'speech' in action)
    menu_keys = {(row['block'], row['source_command_offset']) for row in load(MENUS)['objects']}
    assert {(row['menu']['block'], row['menu']['source_command_offset']) for row in sequence if 'menu' in row} == menu_keys
    style_keys = {(row['block'], row['source_command_offset']) for row in load(STYLES)['records']
                  if 4 in row['source_style_indices']}
    assert all((row['style']['block'], row['style']['source_command_offset']) in style_keys
               for row in sequence if 'style' in row)
    save(SELECTION, dict(
        format='dk4-disclosed-native-dialogue-fixture-selection-v2',
        fixtures=[dict(name='rafael_visits_trials_and_villages', sequence=sequence,
                       purpose='Observe seven complete menus and following dialogue, page turns, corrected I glyphs, runtime names, FE notices and scoped headers.')],
        chosen_fixture_path_is_a_display_sequence_not_original_branch_routing=True,
        guide_photos=False, new_credit=0,
        evidence={str(path): digest(path) for path in (drafts, MENUS, STYLES, __file__)},
    ))
    print(f'Selected {len(sequence)} complete native commands for focused emulator QA.')


if __name__ == '__main__':
    main()
