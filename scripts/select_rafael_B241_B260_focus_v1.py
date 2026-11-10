"""Select focused emulator sequences for the changed native display behaviors."""
from scripts.assemble_rafael_B241_B260_offline_v2 import FINAL_MANUSCRIPT, FINAL_PLAN, ROOT, digest
from scripts.audit_story_glyph_consistency import load, save


SELECTION = ROOT / 'focused_selection_v1.json'


def main():
    assert not SELECTION.exists()
    rows = load(FINAL_MANUSCRIPT)['records']

    def exchange(block, *, omit=(), menu=None):
        actions = {}
        for row in rows:
            if row['block'] != block or row['kind'] == 'typed-choice-label':
                continue
            if row.get('native_object_kind') == '4100-style-alternative':
                offset = row['source_command_offset']
                actions[offset] = dict(style=dict(block=block, source_command_offset=offset, expected_style=4))
            elif row['source_record_index'] not in omit:
                actions[row['source_reference']['header_offset']] = dict(speech=row['id'])
        if menu is not None:
            assert menu not in actions
            actions[menu] = dict(menu=dict(block=block, source_command_offset=menu))
        return [action for _, action in sorted(actions.items())]

    letters_town = exchange(247) + exchange(248) + exchange(256) + exchange(257) + exchange(259)
    rose = exchange(251, omit=(79, 84), menu=494) + exchange(253)
    figureheads = (
        exchange(254, omit=(118, 130, 139, 143, 182, 186, 190), menu=698)
        + exchange(260, omit=(122, 125, 129), menu=450)
    )
    charm = [dict(speech=f'DK4_MES_B260_R{index:04d}') for index in (122, 125, 129)]
    fixtures = [
        dict(name='rafael_letters_and_ruins_greeting', sequence=letters_town,
             purpose='Observe both native voice tables, both staged signatures, page turns and the Hatra glyph correction.'),
        dict(name='rafael_frozen_rose_town_exchange', sequence=rose,
             purpose='Observe the tavern exchange, corrected Francisca header, default menu return, and handover panel.'),
        dict(name='rafael_two_figureheads', sequence=figureheads + charm,
             purpose='Observe default menu returns, modal panels and runtime names. The separately sampled Charm ending follows the selected Luck sequence for display checks.'),
    ]
    actions = letters_town + rose + figureheads + charm
    ids = [a['speech'] for a in actions if 'speech' in a]
    assert len(ids) == len(set(ids))
    assert {r['id'] for r in rows if r.get('source_staged_progressive') or r['native_literal_tokens']} <= set(ids)
    assert sum('style' in a for a in actions) == 2 and sum('menu' in a for a in actions) == 3
    save(SELECTION, dict(format='dk4-disclosed-native-dialogue-fixture-selection-v2', fixtures=fixtures,
        no_roster_role_RNG_orcondition_override=True,
        original_locations_earned_events_and_unselected_content_unvisited=True, guide_photos=False,
        new_credit=0, evidence={str(path): digest(path) for path in (FINAL_MANUSCRIPT, FINAL_PLAN)}))
    print([(f['name'], len(f['sequence'])) for f in fixtures], flush=True)


if __name__ == '__main__':
    main()
