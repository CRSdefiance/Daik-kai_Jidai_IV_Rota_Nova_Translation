"""Bound representative whole exchanges to the checked SC2 command stream."""
from pathlib import Path
from scripts.audit_story_glyph_consistency import load, save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest

ROOT = Path('work/Lil382_residual_A_clean_20261110')


def main():
    out = ROOT/'display_selection_v1.json'
    assert not out.exists()
    rp = ROOT/'reconstruction_v2/reconstruction.json'
    sp = ROOT/'stored_v1/stored_native_verification.json'
    rebuilt, stored = map(load, (rp, sp))
    assert stored['reconstruction_sha256'] == digest(rp)
    assert stored['complete_stored_pages'] == 386
    assert stored['every_byte_consumed_andall_first_internal_final_glyphs_bounds_canaries_andpagination_pass']
    doc, native, styles, menus = map(load, (rebuilt['manuscript'], rebuilt['native'], rebuilt['styles'], rebuilt['menu']))
    byid = {r['id']: r for r in native['records']}
    cases = [('Lil382_Aziza', [12], 0),
             ('Lil382_cross_story_letters', [115, 235, 236], 0),
             ('Lil382_rose_scam_figurehead', [238, 239, 242], 1)]
    specs, union, seen_menus, seen_styles = [], set(), set(), set()
    for name, blocks, choice in cases:
        sequence = []
        for block in blocks:
            actions = [(r['source_reference']['offset'], dict(speech=r['id']))
                       for r in doc['records'] if r['block'] == block
                       and r['kind'] != 'typed-choice-label' and not r.get('native_object_kind')]
            actions += [(o['source_command_offset'], dict(style=dict(block=block,
                         source_command_offset=o['source_command_offset'], expected_style=4)))
                        for o in styles['objects'] if o['block'] == block]
            actions += [(o['source_command_offset'], dict(menu=dict(block=block,
                         source_command_offset=o['source_command_offset'])))
                        for o in menus['menus'] if o['block'] == block]
            sequence += [a for _, a in sorted(actions)]
        ids, extra, captures, declared = [], [], [], []
        units = commandbytes = 0
        for action in sequence:
            if 'speech' in action:
                ident = action['speech']; row = byid[ident]
                group = next(g for g in rebuilt['groups'] if g['block'] == row['block'])
                text = next(t for t in group['text_records'] if t['id'] == ident)
                command = next(c for c in group['all_target_commands'] if c['offset'] == text['new_offset']-5)
                commandbytes += len(bytes.fromhex(command['whole_command_hex']))
                ids.append(ident)
                units += 1 if row['kind'] == 'system-FE' else len(row['complete_native_English_display']['pages'])
            elif 'style' in action:
                req = action['style']
                obj = next(o for o in styles['objects'] if (o['block'], o['source_command_offset']) == (req['block'], req['source_command_offset']))
                ident = obj['native_slots'][4]['record_id']; ids.append(ident)
                units += len(byid[ident]['complete_native_English_display']['pages'])
                commandbytes += len(bytes.fromhex(obj['target_object_hex']))
                seen_styles.add((obj['block'], obj['source_command_offset']))
            else:
                req = action['menu']
                obj = next(o for o in menus['menus'] if (o['block'], o['source_command_offset']) == (req['block'], req['source_command_offset']))
                # First page opens before 2200; the next waits for the 4000 pulse.
                frame = 3900 + (units-1)*240
                captures += [frame-40, frame+20, frame+80, frame+120]
                extra += [dict(start=frame+60*step, duration=4, buttons=['DOWN']) for step in range(choice)]
                declared.append(dict(**req, expected_index=choice, caption_count=obj['caption_count']))
                seen_menus.add((obj['block'], obj['source_command_offset']))
                units += 1; commandbytes += len(bytes.fromhex(obj['target_object_hex']))
        assert len(ids) == len(set(ids)) and commandbytes+512 <= 9216
        union.update(ids)
        specs.append(dict(name=name, sequence=sequence, selection_source_utterances=len(ids),
            selection_expected_pages=units-len(declared), frames=4001+units*240+6000,
            extra_inputs=extra, capture_extra=sorted(set(captures)), expected_menu_selection=choice,
            expected_menu_instances=declared, selected_complete_command_bytes=commandbytes,
            purpose='Representative initialized Lil SC2 command QA: complete Aziza exchanges, owned cross-story context and letters, '
                    'both effective personality tables, Frozen Rose/Spirit notices, scam and figurehead captions/returns, '
                    'multipage continuation and native glyphs. Conditional alternatives are concatenated; previously credited '
                    'B115 context is preserved in the release and not copied into this focused sample. '
                    'No natural activation, original rewards/branch results, geography, chronology, full route or hardware claim.'))
    assert len(seen_menus) == 2 and len(seen_styles) == 2
    save(out, dict(fixtures=specs, selected_speech_ids=sorted(union), selected_source_bodies=len(union),
        planned_original_style_objects=sorted(seen_styles), planned_original_menu_objects=sorted(seen_menus),
        unvisited_source_bodies=378-len(union), all_other_content_offline_qualified_not_claimed_gameplay=True,
        natural_activation=False, earned_chronology=False, item_stat_money_branch_outcomes_not_simulated=True,
        actual_gameplay_pending=True, new_credit=0, guide_photos=False,
        evidence={str(p): digest(p) for p in [rp, sp, ROOT/'offline_display_approval_v1.json', Path(__file__)]}))
    print([(s['name'], s['selection_source_utterances'], s['selection_expected_pages'], s['frames']) for s in specs])


if __name__ == '__main__':
    main()
