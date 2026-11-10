"""Select whole exchanges and concrete page, role, menu and FE risks for emulator QA."""
from pathlib import Path
from scripts.audit_story_glyph_consistency import load, save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest

ROOT = Path('work/Maria_B196_B215_clean_20261110')


def main():
    out = ROOT/'display_selection_v1.json'
    assert not out.exists()
    rebuiltpath = ROOT/'reconstruction_v1/reconstruction.json'
    storedpath = ROOT/'stored_v1/stored_native_verification.json'
    rebuilt, stored = map(load, [rebuiltpath, storedpath])
    doc, native, styles = map(load, [rebuilt['manuscript'], rebuilt['native'], rebuilt['styles']])
    rolespath = ROOT/'dynamic_roles_current_v1.json'
    roles = load(rolespath)
    assert stored['reconstruction_sha256'] == digest(rebuiltpath) and stored['complete_stored_pages'] == 325
    assert stored['every_byte_consumed_andall_first_internal_final_glyphs_bounds_canaries_andpagination_pass']
    assert stored['runtime'] == roles['runtime'] == doc['runtime']
    byid = {r['id']: r for r in native['records']}
    voice = {r['source_selector']: r['source_voice_class'] for r in roles['native_roles']['rows']}
    assert voice[208] == 4
    def speech(b, n): return dict(speech=f'DK4_MES_B{b}_R{n:04d}')
    def menu(b, at): return dict(menu=dict(block=b, source_command_offset=at))
    def style(b): return dict(style=dict(block=b, source_command_offset=8, expected_style=4))
    def whole(b): return [dict(speech=r['id']) for r in doc['records'] if r['block'] == b and r.get('native_object_kind') is None and r['kind'] != 'typed-choice-label']
    prefix = [5,9,13,16,20,24,28,31,35,39,43,47,51,55,59,63]
    mainseq = [style(196), *whole(196), *whole(198), *whole(200), *whole(202)]
    mainseq += [*[speech(215,n) for n in prefix], menu(215,716),
        *[speech(215,n) for n in [78,82,86,90,94,113,125,132,136]]]
    town = [*[speech(212,n) for n in [4,8,11,15,19,23,27,31,36,40,43,47,51]], menu(212,492), speech(212,67),
        *[speech(212,n) for n in [83,87,91,94,98,101,105,109,112,116,119,123,127]], *whole(213), *whole(214)]
    refusal = [style(209), *whole(209), *[speech(215,n) for n in prefix], menu(215,716),
        *[speech(215,n) for n in [174,178,182]]]
    fixtures = []
    union = set()
    selected_styles = set()
    selected_menus = set()
    for name, sequence, choice in [
        ('Maria321_letters_training_attempt_menu0', mainseq, 0),
        ('Maria321_Francisca_recovery_menu0', town, 0),
        ('Maria321_Jam_figurehead_refusal_menu1', refusal, 1),
    ]:
        ids = []
        units = command_bytes = 0
        controls, captures, menus = [], [], []
        for action in sequence:
            if 'speech' in action:
                ident = action['speech']; row = byid[ident]
                assert not row.get('native_object_kind')
                group = next(g for g in rebuilt['groups'] if g['block'] == row['block'])
                text = next(t for t in group['text_records'] if t['id'] == ident)
                command = next(c for c in group['all_target_commands'] if c['offset'] == text['new_offset']-5)
                command_bytes += len(bytes.fromhex(command['whole_command_hex']))
                units += 1 if row['kind'] == 'system-FE' else len(row['complete_native_English_display']['pages'])
                ids.append(ident)
            elif 'style' in action:
                request = action['style']
                obj = next(o for o in styles['objects'] if o['block'] == request['block'] and o['source_command_offset'] == request['source_command_offset'])
                ident = obj['native_slots'][4]['record_id']
                ids.append(ident)
                units += len(byid[ident]['complete_native_English_display']['pages'])
                command_bytes += len(bytes.fromhex(obj['target_object_hex']))
                selected_styles.add((request['block'], request['source_command_offset']))
            else:
                request = action['menu']
                obj = next(o for o in load(rebuilt['menu'])['menus'] if o['block'] == request['block'] and o['source_command_offset'] == request['source_command_offset'])
                count = len(obj['record_ids']); assert count == 2 and choice < count
                frame = 4140 + units*240
                captures.extend([frame-40, frame+20, frame+80, frame+120])
                for step in range(choice): controls.append(dict(start=frame+60*step, duration=4, buttons=['DOWN']))
                menus.append(dict(**request, expected_index=choice, caption_count=count))
                selected_menus.add((request['block'], request['source_command_offset']))
                command_bytes += len(bytes.fromhex(obj['target_object_hex']))
                units += 1
        assert len(ids) == len(set(ids)) and set(ids) <= set(byid)
        assert command_bytes + 512 <= 9216, (name, command_bytes)
        union.update(ids)
        fixtures.append(dict(name=name, sequence=sequence, selection_source_utterances=len(ids),
            selection_expected_pages=units-len(menus), frames=4001+units*240+6000,
            extra_inputs=controls, capture_extra=sorted(set(captures)), expected_menu_selection=choice,
            expected_menu_instances=menus, selected_complete_command_bytes=command_bytes,
            purpose='Representative initialized emulator display QA: complete Ian and Jam letters, Boy/Sailor role distinction, complete training and repeated shield exchanges, the repaired strength-of-mind page, the reclaimed Jam page, Francisca recovery and FE handover, corrected Julio departure instruction, figurehead attempt/refusal and menu indices0/1, plus full original host exit. Selected complete source commands are copied into a disclosed QA host. Original conditional branches, earned geography/chronology, item/stat outcomes, natural activation, full route and hardware are not claimed.'))
    assert len(fixtures) == 3 and selected_styles == {(196,8), (209,8)}
    assert selected_menus == {(212,492), (215,716)}
    save(out, dict(fixtures=fixtures, selected_speech_ids=sorted(union), selected_source_bodies=len(union),
        planned_original_style_objects=sorted(selected_styles), planned_original_menu_objects=sorted(selected_menus),
        unvisited_source_bodies=317-len(union), all_other_content_offline_qualified_not_claimed_gameplay=True,
        unvisited_content_includes_figurehead_success_andFI_Spirit_panel=True,
        natural_activation=False, earned_chronology=False, item_stat_money_branch_outcomes_not_simulated=True,
        actual_gameplay_pending=True, new_credit=0, guide_photos=False,
        evidence={str(p):digest(p) for p in [rebuiltpath, storedpath, rolespath, ROOT/'offline_display_approval_v1.json', Path(__file__)]}))
    print([(f['name'], f['selection_source_utterances'], f['selection_expected_pages'], f['frames'], f['selected_complete_command_bytes']) for f in fixtures])


if __name__ == '__main__':
    main()
