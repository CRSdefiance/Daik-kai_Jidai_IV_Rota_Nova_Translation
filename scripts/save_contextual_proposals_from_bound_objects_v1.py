"""Save individual comparison proposals while leaving unproven name/term/display gates unpassed."""
import argparse
import importlib
from copy import deepcopy
from pathlib import Path
import re
from scripts.audit_story_glyph_consistency import load, save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ['drafts', 'current', 'objects', 'module', 'out']:
        parser.add_argument('--' + name, required=True)
    args = parser.parse_args()
    out = Path(args.out)
    assert not out.exists()
    drafts, current, objects = map(load, [args.drafts, args.current, args.objects])
    data = importlib.import_module(args.module)
    expected = {(r['block'], r['source_record_index']): r for r in drafts['records'] if r['block'] in data.DECISIONS}
    bound = {r['id']: r for g in current['groups'] for r in g['records']}
    bound.update({r['id']: r for r in objects['style_records'] + objects['choice_records']})
    assert len(bound) == len(drafts['records']) == 301
    assert current['current_ROM_sha256'] == objects['current_ROM_sha256']
    assert current['runtime'] == objects['runtime']
    decisions = {(block, index): (replacement, note) for block, rows in data.DECISIONS.items()
        for index, replacement, note in rows}
    assert len(decisions) == sum(len(rows) for rows in data.DECISIONS.values())
    assert decisions.keys() == expected.keys()
    records = []
    for key, (replacement, note) in decisions.items():
        source = expected[key]
        prior = bound[source['id']]
        assert prior['source_hex'] == source['source_hex'] and prior['source_reference'] == source['source_reference']
        assert source['independent_draft_precedes_current_English_intake'] and not any(source['review'].values())
        english = prior['current_comparison_paragraph'] if replacement is None else replacement
        assert note.strip() and english.strip() == english
        assert not any(s in english for s in ['\n', '\r', '\t', '{LB', '{ALIGN', '{PAD}'])
        assert {token: english.count(token) for token in source['source_macros']} == source['source_macros']
        assert set(re.findall(r'F[A-Z]', english)) == set(source['source_macros'])
        row = deepcopy(source)
        row.update({k: deepcopy(v) for k, v in prior.items() if k.startswith('current_') or k == 'selected_native_pointer'})
        row.update(proposed_English=english, decision='retention' if replacement is None else 'revision',
            finding=note, localization_note=note, retention_reason=note if replacement is None else None,
            contextual_comparison_saved=True, current_English_unconsulted=False,
            current_English_comparison_pending=False, native_bindings_are_not_final_editorial_approval=True,
            name_term_consumer_review_andfresh_display_still_pending=True,
            review=dict(source=False, context=False, localization=False, naturalness=False, formatting=False),
            no_proposal_may_ship_orreceive_completion_credit_yet=True, new_credit=0)
        records.append(row)
    save(out, dict(records=records, records_count=len(records), complete_exchanges=len(data.DECISIONS),
        translation_policy='natural-dialogue-v2', target_locale='en-US',
        current_ROM=current['current_ROM'], current_ROM_sha256=current['current_ROM_sha256'],
        revised=sum(r['decision']=='revision' for r in records),
        retained=sum(r['decision']=='retention' for r in records),
        all_compared_in_complete_source_andcurrent_exchange_context=True,
        all_five_gates_still_pending=True, new_credit=0, full_goal_complete=False,
        evidence={str(p): digest(p) for p in map(Path, [args.drafts, args.current, args.objects, data.__file__, __file__])}))
    print(f'Saved {len(records)} individual proposals: {sum(r["decision"]=="revision" for r in records)} revisions/{sum(r["decision"]=="retention" for r in records)} justified retentions; gates and credit pending.')


if __name__ == '__main__':
    main()
