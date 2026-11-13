"""Select representative scene commands for an initialized emulator sequence."""
from scripts.audit_story_glyph_consistency import load, save
from scripts.seal_rafael_B301_B320_clean_v1 import MENUS, ROOT, SEALED, STYLES, digest


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
        *speech(301, 86, 109), menu(301, 1160), *speech(301, 124, 129),
        style(301, 1300), *speech(301, 163), style(301, 1958),
        *speech(302, 6), *speech(303, 9, 12),
        *speech(305, 105), menu(305, 968), *speech(305, 120), style(305, 1042), *speech(305, 164),
        *speech(306, 34, 100, 105, 109), *speech(307, 25), *speech(309, 47, 59),
        *speech(310, 57), menu(310, 514), *speech(310, 73),
        *speech(311, 6), *speech(312, 72), style(312, 602), menu(312, 878),
        *speech(312, 117, 134), style(312, 1102), style(312, 1710),
        *speech(313, 50), *speech(314, 21), *speech(316, 30, 35),
        *speech(317, 72, 79), *speech(318, 137, 146, 198, 202, 205),
        *speech(320, 82), menu(320, 538), *speech(320, 99), style(320, 616), *speech(320, 170),
    ]
    drafts = SEALED / 'sealed_drafts.json'
    draft_ids = {row['id'] for row in load(drafts)['records']}
    assert all(action['speech'] in draft_ids for action in sequence if 'speech' in action)
    menu_keys = {(row['block'], row['source_command_offset']) for row in load(MENUS)['objects']}
    assert {(a['menu']['block'], a['menu']['source_command_offset']) for a in sequence if 'menu' in a} == menu_keys
    style_keys = {(row['block'], row['source_command_offset']) for row in load(STYLES)['records']
                  if 4 in row['source_style_indices']}
    assert all((a['style']['block'], a['style']['source_command_offset']) in style_keys
               for a in sequence if 'style' in a)
    save(SELECTION, dict(format='dk4-disclosed-native-dialogue-fixture-selection-v2',
         fixtures=[dict(name='rafael_ruins_rituals_and_crossings', sequence=sequence,
                        purpose='Observe both choice layouts, route branches’ display text, cave and desert voices, names, substitutions, FE notices and page turns.')],
         chosen_fixture_path_is_a_display_sequence_not_original_branch_routing=True,
         guide_photos=False, new_credit=0,
         evidence={str(path): digest(path) for path in (drafts, MENUS, STYLES)}))
    print(f'Selected {len(sequence)} native commands for focused emulator QA.')


if __name__ == '__main__':
    main()
