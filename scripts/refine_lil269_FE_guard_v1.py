"""Apply the qualified record-scoped FE reserve after confirmed native truncation."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load, save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest

ROOT = Path('work/Lil269_B243_B282_clean_20261110')


def main():
    output = ROOT / 'formatting_v2/page_preferences_v5_FE.json'
    assert not output.exists()
    before = ROOT / 'formatting_v2/page_preferences_v4.json'
    manuscript = ROOT / 'formatting_v2/formatting_input.json'
    diagnostic = ROOT / 'B251_R9_FE_failure_diagnostic_v1.json'
    failure = load(diagnostic)['diagnostic']
    assert (failure['return_consumed_bytes'], failure['intended_bytes']) == (108, 125)
    assert failure['input_unchanged']
    assert bytes(e['code'] for e in failure['events'] if e['y'] == 24) == b'  '
    prefs = load(before)
    rows = {r['id']: r for r in load(manuscript)['records']}
    plans = load(ROOT / 'plan_v4/automatic_plans.json')['records']
    wanted = {r['id'] for r in plans if r['kind'] == 'system-FE' and any(len(t.strip()) >= 36 for t in r['lines'])}
    assert wanted == {'DK4_MES_B251_R0009', 'DK4_MES_B251_R0165'}
    for ident in sorted(wanted):
        row = rows[ident]
        assert row['kind'] == 'system-FE' and row['source_selector'] == 254
        assert ident not in prefs['records']
        prefs['records'][ident] = dict(FE_planning_cells=36,
            reason='Reuse the qualified FE36 reserve after B251R9 consumes only108/125 bytes and inserts a blank row. R165 has the matching long-row risk. Preserve all prose, source controls, physical228px geometry, font and native assertions; fresh native row/consumption/pixel checks remain required.',
            bindings={k: sha(row[k].encode()) for k in ['source_hex', 'current_hex', 'english']})
    prefs.update(previous_preferences=str(before), previous_preferences_sha256=digest(before),
        concrete_native_failure=str(diagnostic), concrete_native_failure_sha256=digest(diagnostic),
        qualified_existing_recipe='scripts/refine_maria305_FE_guard_v1.py',
        no_prose_physical_geometry_font_orengine_changes=True, new_credit=0)
    save(output, prefs)
    print('Prepared two source-bound FE36 refinements; no prose, physical width or native guard change.')


if __name__ == '__main__':
    main()
