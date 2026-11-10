"""Keep eleven directly observed phrases together without changing prose or width."""
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load, save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest

ROOT = Path('work/Maria_B152_B175_clean_20261109')


def main():
    output = ROOT / 'continuity_preferences_v2.json'
    findings = ROOT / 'native_layout_findings_v1.json'
    assert not output.exists() and not findings.exists()
    priorpath = ROOT / 'continuity_preferences_v1.json'
    docpath = ROOT / 'formatting_v1/formatting_input.json'
    planpath = ROOT / 'plan_continuity_v1/automatic_plans.json'
    visualpath = ROOT / 'initial_body_visual_review_v1.json'
    visual = load(visualpath)
    assert visual['body_records'] == visual['body_pages'] == 373
    assert visual['all_native_pages_bound_to_directly_viewed_exact_contact_sheet_tiles']
    pref = deepcopy(load(priorpath))
    rows = {r['id']: r for r in load(docpath)['records']}
    plans = {r['id']: r for r in load(planpath)['records']}
    viewed = {r['id']: r for r in visual['records']}
    changes = {
        (153,27): ([['next','time']], 'Keep the short next time expression together in the plan to ask about the fragrance; the viewed page splits next/time.'),
        (157,13): ([['caught','on']], 'Keep the caught on phrasal verb together in the tea-popularity question; the viewed page separates caught/on before.'),
        (168,31): ([['coming','right'],['right','up']], 'Keep the barkeeper\'s complete Coming right up call on one row rather than leaving right up as a short tail.'),
        (169,61): ([['100000','gold']], 'Keep this exact price and unit together; the viewed page ends with100000 and starts the next row with gold.'),
        (169,106): ([['70000','gold']], 'Keep this exact price and unit together; the viewed page ends with70000 and starts the next row with gold.'),
        (169,151): ([['how','about']], 'Keep the short How about question opening together rather than ending the previous row with How.'),
        (170,56): ([['handsome','man']], 'Keep the teasing handsome man phrase together, avoiding the sparse man, too final row.'),
        (170,92): ([['fall','in'],['in','love']], 'Keep fall in love together in the emotionally complete farewell; the viewed page ends with fall.'),
        (171,9): ([['any','naughty']], 'Keep each repeated Namahage call coherent rather than ending the first row with the second Any; preserve both full repetitions.'),
        (171,13): ([['any','naughty']], 'Keep each repeated Namahage call coherent rather than ending the first row with the second Any; preserve both full repetitions and source spacing.'),
        (172,12): ([['what','sort'],['sort','of']], 'Keep the short What sort of question opening together rather than separating sort/of man.'),
    }
    notes = []
    for (block, record), (pairs, reason) in changes.items():
        ident = f'DK4_MES_B{block}_R{record:04d}'
        row, oldplan, seen = rows[ident], plans[ident], viewed[ident]
        assert ident not in pref['records'] and seen['compiled_hex'] == oldplan['encoded_hex']
        pref['records'][ident] = dict(required_pairs=pairs, reason=reason,
            bindings={k: sha(row[k].encode()) for k in ['source_hex','current_hex','english']})
        notes.append(dict(id=ident, source_reference=row['source_reference'], current_reference=row['current_reference'],
            initial_lines=oldplan['lines'], initial_compiled_hex=oldplan['encoded_hex'], directly_viewed_pages=seen['pages'],
            required_pairs=pairs, finding=reason))
    assert len(notes) == 11
    pref.update(previous_preferences=str(priorpath), previous_preferences_sha256=digest(priorpath),
        no_prose_font_geometry_engine_orcontrol_changes=True, fresh_changed_native_checks_pending=True, new_credit=0)
    save(output, pref)
    save(findings, dict(records=notes, observed_phrase_refinements=11, source_objects=390, body_candidates=373,
        all_original_prose_andwidths_preserved=True, all_initial_pages_directly_viewed=True,
        all_fifth_gates_still_pending=True, new_credit=0,
        justified_layout_retentions=[dict(id='DK4_MES_B153_R0004',
            reason='The short opening Did you notice retains the complete object phrase that wonderful fragrance on row2; readable two-row question without a broken tag.')],
        evidence={str(p):digest(p) for p in [priorpath,docpath,planpath,visualpath,Path(__file__)]}))
    print('Prepared11 observed phrase refinements; original prose, widths, controls andnine prior preferences preserved.')


if __name__ == '__main__':
    main()
