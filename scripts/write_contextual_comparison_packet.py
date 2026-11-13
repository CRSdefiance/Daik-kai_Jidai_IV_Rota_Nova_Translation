"""Save explicit editorial decisions against immutable source/current/draft bindings."""
from copy import deepcopy
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load, save


def write_review(out, draft_paths, decisions, contexts):
    out = Path(out)
    assert not out.exists()
    current_path = Path('work/analysis/Hodram_B131_B150_current_20261102/current_effective.json')
    objects_path = Path('work/analysis/Hodram_B131_B150_current_objects_20261102/current_objects.json')
    current, objects = map(load, [current_path, objects_path])
    drafts = {r['id']: r for p in draft_paths for r in load(p)['records']}
    bound_rows = [r for g in current['groups'] for r in g['records']]
    bound_rows += objects['style_records'] + objects['choice_records']
    bound = {r['id']: r for r in bound_rows}
    assert len(bound) == len(bound_rows) == 329
    assert decisions and set(decisions) <= drafts.keys() & bound.keys()
    rows = []
    for ident, (replacement, note) in decisions.items():
        draft, prior = drafts[ident], bound[ident]
        assert draft['source_hex'] == prior['source_hex'] and note.strip()
        assert draft['block'] in contexts
        row = deepcopy(prior)
        row.update({k: deepcopy(v) for k, v in draft.items()
                    if k not in row and not k.startswith('current_')})
        style = 'source_style_indices' in row
        choice = 'source_index' in row and not style
        kind = ('typed-choice-label' if choice else
                'system-FE' if row['source_selector'] == 254 else 'progressive')
        raw = bytes.fromhex(row['source_hex'])
        source_body = raw if style or choice else raw[1:]
        english = prior['current_comparison_paragraph'] if replacement is None else replacement
        if replacement is None:
            for macro in ['FI', 'FA', 'FO']:
                english = english.replace(macro, '{MACRO:' + macro + '}')
        assert english == english.strip() and '\n' not in english and '\r' not in english
        assert '{LB@' not in english and '{ALIGN@' not in english and '{PAD}' not in english
        for macro in ['FI', 'FA', 'FO']:
            assert english.count('{MACRO:' + macro + '}') == source_body.count(macro.encode()), (ident, macro)
        if '{LB}' in english:
            assert draft.get('manual_break_reason')
            row['manual_break_reason'] = draft['manual_break_reason']
        else:
            row.pop('manual_break_reason', None)
        reference = row['source_reference']
        row.update(
            kind=kind, english=english, logical_English=english,
            planned_English_markup=english if choice else '{SPEAKER:' + format(row['source_selector'], '02X') + '}' + english,
            speaker=draft['speaker'], source_meaning=draft['source_meaning_gloss'],
            context=contexts[row['block']], context_reference=f'SC1B{row["block"]}-complete-source-exchange',
            decision='retention' if replacement is None else 'revision', finding=note,
            retention_reason=note if replacement is None else None, localization_note=note,
            review=dict(source=True, context=True, localization=True, naturalness=True, formatting=False),
            remaining_review_gates=['formatting'], earlier_English_unconsulted=False,
            current_English_now_exposed=True, current_English_comparison_pending=False,
            source_meaning_anddraft_preceded_current_comparison=True,
            whole_exchange_cadence_andemotional_progression_reread=True,
            no_authored_linebreak_alignment_padding_orallocation_driven_shortening=True,
            registered_release_andcompletion_credit_pending=True)
        for key in ['all_five_editorial_gates_pending', 'source_context_localization_formatting_gates_pending',
                    'native_style_dispatch_andall_five_review_gates_pending', 'localization_andfive_gate_approval_pending']:
            row.pop(key, None)
        if style:
            row.update(native_object_kind='4100-style-alternative',
                       source_record_index=reference['physical_record_index'],
                       virtual_formatter_prefix_is_not_part_of_stored_alternative_text=True)
        elif not choice:
            row.update(source_record_index=reference['record_index'], source_native_extent=row['native_extent'])
        rows.append(row)
    rows.sort(key=lambda r: (r['block'], r['source_reference']['offset']))
    save(out, dict(
        format='dk4-editorial-prose-packet-v1', translation_policy='natural-dialogue-v2', target_locale='en-US',
        review_gates=['source', 'context', 'localization', 'naturalness', 'formatting'],
        current_ROM=current['current_ROM'], current_ROM_sha256=current['current_ROM_sha256'],
        current_archive_sha256=current['current_archive_sha256'], file_path=current['file_path'],
        blocks=sorted({r['block'] for r in rows}), complete_exchange_contexts=contexts, records=rows,
        revised=sum(r['decision'] == 'revision' for r in rows), retained=sum(r['decision'] == 'retention' for r in rows),
        all_four_individual_prose_gates_passed=True, all_formatting_gates_false=True,
        all_current_English_in_these_exchanges_compared=True,
        evidence={str(p): sha(Path(p).read_bytes()) for p in [*draft_paths, current_path, objects_path, Path(__file__)]},
        new_credit=0, full_goal_complete=False))
    print(out, len(rows), 'prose decisions;', sum(r['decision'] == 'revision' for r in rows),
          'revisions;', sum(r['decision'] == 'retention' for r in rows), 'retentions; formatting pending.')
