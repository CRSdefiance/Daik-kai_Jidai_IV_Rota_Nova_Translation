"""Select focused original consumers and representative town exchanges for cold-boot QA."""
from scripts.assemble_rafael_B221_B240_offline_v2 import FINAL_MANUSCRIPT, FINAL_PLAN, ROOT
from scripts.audit_story_glyph_consistency import load, save
from scripts.write_rafael_B221_B240_contextual_v1 import digest

SELECTION = ROOT / 'focused_selection_v1.json'


def main():
    assert not SELECTION.exists()
    rows = load(FINAL_MANUSCRIPT)['records']
    def speech(block, index):
        row = next(r for r in rows if r['block'] == block and r['kind'] != 'typed-choice-label'
                   and not r.get('native_object_kind') and r['source_record_index'] == index)
        return dict(speech=row['id'])

    def exchange(block, low=0):
        actions = {}
        for row in rows:
            if row['block'] != block or row['kind'] == 'typed-choice-label':
                continue
            if row.get('native_object_kind') == '4100-style-alternative':
                at = row['source_command_offset']
                if low == 0:
                    actions[at] = dict(style=dict(block=block, source_command_offset=at, expected_style=4))
            elif row['source_record_index'] >= low:
                actions[row['source_reference']['header_offset']] = dict(speech=row['id'])
        return [action for _, action in sorted(actions.items())]

    def menu(block, offset):
        return dict(menu=dict(block=block, source_command_offset=offset))

    story = (exchange(221) + exchange(223)
             + [dict(style=dict(block=226, source_command_offset=8, expected_style=4))]
             + exchange(226, 62) + exchange(227) + exchange(235)
             + [speech(238, 51)])
    choice = ([speech(224, 5), menu(224, 64), speech(224, 32), menu(224, 242)]
              + [speech(224, i) for i in (51, 54, 58, 62)]
              + [speech(233, i) for i in (5, 8, 13)] + [menu(233, 136)]
              + [speech(233, i) for i in (29, 41, 44, 49, 52, 55, 60, 64, 67, 72)]
              + [speech(224, 72)] + exchange(237) + [speech(240, 23), speech(240, 26)])
    fixtures = [
        dict(name='rafael_letters_swans_and_names', sequence=story,
             purpose='Verify all four complete voice commands at the original default class, page turns, three '
                     'signatures, three FE swan panels, corrected narrow I glyphs, and FI, FA and FO substitutions.'),
        dict(name='rafael_books_guard_and_town', sequence=choice,
             purpose='Verify the default returns of all three menus, the independently sampled restored Guan Yu line, '
                     'the town mock battle and the shield name. The copied commands do not simulate choice branches.'),
    ]
    actions = story + choice
    assert {(a['style']['block'], a['style']['source_command_offset']) for a in actions if 'style' in a} == {
        (221, 8), (221, 702), (226, 8), (235, 8)}
    assert {(a['menu']['block'], a['menu']['source_command_offset']) for a in actions if 'menu' in a} == {
        (224, 64), (224, 242), (233, 136)}
    ids = [a['speech'] for a in actions if 'speech' in a]
    assert len(ids) == len(set(ids))
    assert {r['id'] for r in rows if r.get('source_staged_FE') or r.get('source_staged_progressive')
            or r['native_literal_tokens']} <= set(ids)
    save(SELECTION, dict(format='dk4-disclosed-native-dialogue-fixture-selection-v2', fixtures=fixtures,
        no_roster_role_RNG_orcondition_override=True, original_locations_earned_events_and_unselected_content_unvisited=True,
        guide_photos=False, new_credit=0,
        evidence={str(p): digest(p) for p in (FINAL_MANUSCRIPT, FINAL_PLAN)}))
    print([(f['name'], len(f['sequence'])) for f in fixtures], flush=True)


if __name__ == '__main__':
    main()

