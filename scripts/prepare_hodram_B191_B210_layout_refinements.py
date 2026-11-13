"""Record one observed FE failure and one visually verified premature-wrap finding."""
from copy import deepcopy
from pathlib import Path
from scripts.audit_story_glyph_consistency import load, save
from dk4tool.patch.grand_race_menu_release import sha

ROOT = Path('work/analysis/Hodram_B191_B210_formatting_20261104')

if __name__ == '__main__':
    output = ROOT / 'guard_and_opening_preferences_v2.json'
    assert not output.exists()
    initial = ROOT / 'page_phrase_preferences_v1.json'
    preferences = deepcopy(load(initial))
    manuscript = ROOT / 'formatting_input.json'
    rows = {r['id']: r for r in load(manuscript)['records']}
    def bind(ident):
        return {k: sha(rows[ident][k].encode('utf-8')) for k in ['source_hex', 'current_hex', 'english']}
    preferences['records']['DK4_MES_B208_R0065'] = dict(bindings=bind('DK4_MES_B208_R0065'), FE_planning_cells=36,
        reason='Native run74976 stops at this four-row FE letter because guard/phase bytes plus the 37-character first row exceed the source consumer\'s complete-consumption boundary. Use the previously validated scoped 36-cell planning guard, keeping the physical 228px panel and every word.')
    preferences['records']['DK4_MES_B201_R0074'] = dict(bindings=bind('DK4_MES_B201_R0074'),
        ordinary_boundaries=[['but', 'I']],
        QA_line_ending_retention=dict(line_index=0, exact_line="I'd like to buy it from you, but",
            reason='Direct visual review found an unnecessary 15-character opening and three rows for a 65-character paragraph. This exact two-row contrast places but at the first row end and keeps the complete I do not have clause together. Retain this grammatical carry across an ordinary line only; no page split, prose change or general weak-ending waiver. Fresh native proof is required.'),
        reason='Use the full available width without shortening the dialogue. A narrowly documented connective at this exact line boundary is clearer than the premature three-row layout.')
    preferences.update(previous_preferences=str(initial), previous_preferences_sha256=sha(initial.read_bytes()),
        failed_native_run=dict(session=74976, terminal=True, exit_code=1, completed_block_receipts_preserved=17),
        new_credit=0, native_fresh_checks_andvisual_review_required=True)
    save(output, preferences)
