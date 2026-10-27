"""Preserve the rejected index-as-ID assumption;bind original captain alias."""
from pathlib import Path


def main():
    source = Path('scripts/research_duel_scope_names_v1117.py').read_text(encoding='utf-8')
    target = Path('scripts/research_duel_scope_names_v1117b.py')
    assert not target.exists()
    changes = {
        "ROOT = Path('work/analysis/duel_scope_names_v1117')":
            "ROOT = Path('work/analysis/duel_scope_names_v1117b')",
        '        assert get(0x7EE08, obj) == actor':
            '        native_id = get(0x7EE08, obj)\n        assert native_id == (captain if actor == 207 else actor)',
        'offset = 0x24 if 28 <= actor <= 43 else 0x20':
            'offset = 0x24 if 28 <= native_id <= 43 else 0x20',
        "names.append({'actor_ID': actor,":
            "names.append({'actor_slot': actor, 'actor_ID': native_id,",
        "layouts.append({'actor_ID': actor,":
            "layouts.append({'actor_slot': actor, 'actor_ID': native_id,",
        "    assert len(names) == 208 and len(layouts) == 4160":
            "    assert len(names) == 208 and len(layouts) == 4160\n"
            "    assert {row['actor_ID'] for row in names} == set(range(207))\n"
            "    assert names[207]['object'] == names[captain]['object']",
        "'names': names, 'all4160_complete_word_layouts': layouts,":
            "'names': names, 'all4160_complete_word_layouts': layouts,\n"
            "        'native_slots208_cover207_IDs_with_slot207_aliasing_current_captain': True,\n"
            "        'predecessor_v1117_rejected_false_slot207_equals_actor207_assumption': True,",
    }
    for before, after in changes.items():
        assert source.count(before) == 1, before
        source = source.replace(before, after)
    target.write_text(source, encoding='utf-8')
    print('Created explicit successor:slot207 is current captain alias;native getter ID chooses name method.')


if __name__ == '__main__':
    main()
