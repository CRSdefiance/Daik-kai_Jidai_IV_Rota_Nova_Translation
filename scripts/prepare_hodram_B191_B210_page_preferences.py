"""Bind two observed textual page-boundary findings without changing source or prose."""
from pathlib import Path
from scripts.audit_story_glyph_consistency import load, save
from dk4tool.patch.grand_race_menu_release import sha

ROOT = Path('work/analysis/Hodram_B191_B210_formatting_20261104')

if __name__ == '__main__':
    output = ROOT / 'page_phrase_preferences_v1.json'
    assert not output.exists()
    manuscript = ROOT / 'formatting_input.json'
    initial = ROOT / 'initial/automatic_plans.json'
    rows = {r['id']: r for r in load(manuscript)['records']}
    plans = {r['id']: r for r in load(initial)['records']}
    records = {}
    for ident, phrase, reason in [
        ('DK4_MES_B200_R0074', 'You can get him', 'The initial page ends after get him and leaves to come down on the next page. Keep the complete second sentence together at the page start.'),
        ('DK4_MES_B210_R0070', "It's a quick way", 'The initial page ends with get on and separates her good side onto the next page. Keep the complete final sentence together.')]:
        row = rows[ident]
        records[ident] = dict(bindings={k: sha(row[k].encode('utf-8')) for k in ['source_hex', 'current_hex', 'english']},
            page_clause=phrase, reason=reason, initial_lines=plans[ident]['lines'],
            textual_plan_review_not_actual_gameplay_or_visual_pixel_approval=True)
    save(output, dict(records=records, manuscript=str(manuscript), manuscript_sha256=sha(manuscript.read_bytes()),
        initial_plan=str(initial), initial_plan_sha256=sha(initial.read_bytes()),
        prose_unchanged=True, no_authored_breaks_orgeometry_changes=True, new_credit=0))
