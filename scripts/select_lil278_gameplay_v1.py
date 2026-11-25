"""Select a focused Lil cold-boot sample with all three menus and a host exit."""

from pathlib import Path

from scripts.audit_story_glyph_consistency import load, save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest


ROOT = Path('work/Lil278_B299_B311_clean_20261110')
SAMPLE = {
    299: ('R0057', 'R0061', 'S590', 'R0093', 'M908', 'R0166', 'R0181', 'R0161', 'R0229', 'R0405'),
    300: ('R0009', 'R0013', 'R0017'),
    301: ('R0071', 'R0074', 'S666', 'R0109', 'R0113', 'M918', 'R0145', 'R0152', 'S1466'),
    304: ('R0008', 'R0015', 'R0029', 'R0032', 'R0036', 'R0039', 'R0051'),
    305: ('R0185', 'R0198', 'R0221', 'R0232'),
    306: ('R0065', 'S362', 'R0089', 'M706', 'R0155', 'R0159', 'R0162', 'R0166', 'R0174', 'R0149', 'R0179'),
    309: ('R0018', 'R0022', 'R0026', 'R0043'),
    310: ('R0073', 'R0081', 'R0087', 'R0094', 'R0106', 'R0110'),
    311: ('S8',),
}


def main():
    out = ROOT / 'display_selection_v1.json'
    assert not out.exists()
    rebuilt_path = ROOT / 'reconstruction_v1/reconstruction.json'
    roles_path = ROOT / 'formatting_v1/role_bindings_v2.json'
    rebuilt, roles = map(load, (rebuilt_path, roles_path))
    native_path = Path(rebuilt['native'])
    styles_path = Path(rebuilt['styles'])
    menus_path = Path(rebuilt['menu'])
    native = {row['id']: row for row in load(native_path)['records']}
    styles = {(row['block'], row['source_command_offset']): row for row in load(styles_path)['objects']}
    menus = {(row['block'], row['source_command_offset']): row for row in load(menus_path)['menus']}
    voices = {row['source_selector']: row['source_voice_class'] for row in roles['native_roles']['rows']}
    ordinary = {row['id'] for group in rebuilt['groups'] for row in group['text_records']}

    sequence, extra, captures, cursors, selected = [], [], [], [], []
    units = pages = 0
    for block, items in SAMPLE.items():
        for item in items:
            if item.startswith('R'):
                ident = f'DK4_MES_B{block}_{item}'
                assert ident in ordinary
                sequence.append(dict(speech=ident))
            else:
                offset = int(item[1:])
                if item.startswith('M'):
                    assert menus[block, offset]['caption_count'] == 2 and units
                    opening = 4000 + (units - 1) * 240
                    extra.append(dict(start=opening + 60, duration=16, buttons=['DOWN']))
                    captures.extend(opening + delta for delta in (30, 90, 150, 210))
                    cursors.append(dict(block=block, source_command_offset=offset, expected_cursor_index=1,
                                        opening_A_frame=opening, ordinary_selection_A_frame=opening + 240))
                    sequence.append(dict(menu=dict(block=block, source_command_offset=offset)))
                    units += 1
                    continue
                assert item.startswith('S')
                style = styles[block, offset]
                selector = bytes.fromhex(style['target_object_hex'])[19]
                voice = voices[selector]
                ident = style['native_slots'][voice]['record_id']
                sequence.append(dict(style=dict(block=block, source_command_offset=offset, expected_style=voice)))
            assert ident not in selected
            selected.append(ident)
            row = native[ident]
            count = 1 if row['kind'] == 'system-FE' else len(row['complete_native_English_display']['pages'])
            units += count
            pages += count

    assert {(row['block'], row['source_command_offset']) for row in cursors} == set(menus)
    assert {key for key, row in native.items() if row['kind'] == 'system-FE'} <= set(selected)
    assert pages > len(selected)
    fixture = dict(
        name='Lil278_expedition_spices_temple',
        purpose='Native display sample of exact reviewed commands. Conditional alternatives are combined in the Lil B22 host.',
        sequence=sequence, extra_inputs=extra, capture_extra=captures, cursor_cases=cursors,
        expected_body_pages=pages, frames=4001 + (units + 30) * 240,
    )
    save(out, dict(
        fixtures=[fixture], selected_body_ids=selected, body_records=len(selected), body_pages=pages,
        all_eight_FE_texts_selected=True, all_three_two_choice_menus_selected=True,
        later_host_exit_requested=True, no_natural_activation_or_branch_outcome_claim=True, new_credit=0,
        evidence={str(path): digest(path) for path in
                  (rebuilt_path, roles_path, native_path, styles_path, menus_path, Path(__file__))},
    ))
    print(len(selected), 'bodies,', pages, 'pages, three menus and an extended host exit schedule.')


if __name__ == '__main__':
    main()
