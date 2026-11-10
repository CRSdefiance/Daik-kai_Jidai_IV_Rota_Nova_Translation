"""Select ordinary text, original personality tables and menus for three bounded QA samples."""
from pathlib import Path
from scripts.audit_story_glyph_consistency import load, save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest

ROOT = Path('work/Lil361_B283_B298_clean_20261110')


def main():
    out = ROOT / 'display_selection_v1.json'
    assert not out.exists()
    reconstruction = ROOT / 'reconstruction_v1/reconstruction.json'
    rebuilt = load(reconstruction)
    doc = load(rebuilt['manuscript'])
    native = {r['id']: r for r in load(rebuilt['native'])['records']}
    styles = load(rebuilt['styles'])['objects']
    menus = load(rebuilt['menu'])['menus']
    roles = load(ROOT / 'dynamic_roles_current_v1.json')
    voices = {r['source_selector']: r['source_voice_class'] for r in roles['native_roles']['rows']}
    ordinary = {r['id']: r for r in doc['records'] if r['kind'] != 'typed-choice-label' and not r.get('native_object_kind')}
    specs = [
        ('Lil361_forest_London', range(283, 288), {(283, 884): 2, (283, 1938): 1}),
        ('Lil361_cave_Angkor', range(288, 293), {(288, 2436): 1}),
        ('Lil361_fog_wristband', range(293, 299), {(293, 1620): 0}),
    ]
    fixtures, selected_ids, all_menu_keys, all_style_keys = [], [], [], []
    for name, blocks, cursor_indices in specs:
        sequence, extra, captures, cursor_cases = [], [], [], []
        units, selected_pages, size = 0, 0, 0
        for group in rebuilt['groups']:
            block = group['block']
            if block not in blocks:
                continue
            speeches = {r['new_offset'] - 5: r['id'] for r in group['text_records']}
            for command in group['all_target_commands']:
                word, at = command['word'], command['offset']
                if word == 0x4000 and at in speeches:
                    ident = speeches[at]
                    assert ident in ordinary
                    sequence.append(dict(speech=ident))
                elif word == 0x4100:
                    proof = next(r for r in styles if r['block'] == block and r['target_object_hex'] == command['whole_command_hex'])
                    selector = bytes.fromhex(proof['target_object_hex'])[19]
                    style = voices[selector]
                    ident = proof['native_slots'][style]['record_id']
                    sequence.append(dict(style=dict(block=block, source_command_offset=proof['source_command_offset'], expected_style=style)))
                    all_style_keys.append((block, proof['source_command_offset']))
                elif word in [0x2100, 0x2200]:
                    proof = next(r for r in menus if r['block'] == block and r['target_object_hex'] == command['whole_command_hex'])
                    key = (block, proof['source_command_offset'])
                    index = cursor_indices[key]
                    assert index in range(proof['caption_count']) and units
                    opening = 4000 + (units - 1) * 240
                    for step in range(index):
                        extra.append(dict(start=opening + 60 * (step + 1), duration=16, buttons=['DOWN']))
                    captures.extend([opening + 30, opening + 90, opening + 150, opening + 210])
                    cursor_cases.append(dict(block=block, source_command_offset=key[1], expected_cursor_index=index,
                        opening_A_frame=opening, ordinary_selection_A_frame=opening + 240))
                    sequence.append(dict(menu=dict(block=block, source_command_offset=key[1])))
                    all_menu_keys.append(key)
                    units += 1
                    size += len(bytes.fromhex(command['whole_command_hex']))
                    continue
                else:
                    continue
                pages = 1 if native[ident]['kind'] == 'system-FE' else len(native[ident]['complete_native_English_display']['pages'])
                units += pages
                selected_pages += pages
                selected_ids.append(ident)
                size += len(bytes.fromhex(command['whole_command_hex']))
        assert size + 512 < 9216
        fixtures.append(dict(name=name, purpose='Bounded initialized display sample of exact reviewed commands, including conditional alternatives; original event activation, branch outcomes, rewards and chronology are not claimed.',
            sequence=sequence, extra_inputs=extra, capture_extra=captures, cursor_cases=cursor_cases,
            expected_body_pages=selected_pages, selected_command_bytes=size,
            frames=4001 + (units + 5) * 240))
    assert len(selected_ids) == len(set(selected_ids)) == 199
    assert set(ordinary) <= set(selected_ids) and len(ordinary) == 175
    assert len(all_style_keys) == len(set(all_style_keys)) == 24
    assert len(all_menu_keys) == len(set(all_menu_keys)) == 4
    save(out, dict(fixtures=fixtures, distinct_body_records=199, all175_ordinary_records_selected=True,
        personality_tables=24, menus=4, other153_physical_personality_alternatives_offline_only=True,
        preserve_B294_earlier_context_in_ROM_not_new_review_orfixture_coverage=True,
        no_native_state_orconditional_outcome_forcing=True, no_original_optional_event_activation_claim=True,
        new_credit=0, full_goal_complete=False,
        evidence={str(p): digest(p) for p in [reconstruction, Path(rebuilt['native']), Path(rebuilt['styles']), Path(rebuilt['menu']), Path(__file__)]}))
    print('Prepared3 bounded samples:175 ordinary bodies,24 original personality tables,4 menus;199 unique bodies.')


if __name__ == '__main__':
    main()
