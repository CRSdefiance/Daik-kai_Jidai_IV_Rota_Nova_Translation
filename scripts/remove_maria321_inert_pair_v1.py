"""Remove an unmatched phrase preference; retain the actual ordinary soft wrap."""
from pathlib import Path
from scripts.audit_story_glyph_consistency import load, save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest

ROOT = Path('work/Maria_B196_B215_clean_20261110')


def main():
    prior = ROOT/'formatting_v1/page_phrase_preferences_v3.json'
    target = ROOT/'formatting_v1/page_phrase_preferences_v4.json'
    assert not target.exists()
    prefs = load(prior)
    key = 'DK4_MES_B204_R0019'
    row = next(r for r in load(ROOT/'formatting_v1/formatting_input.json')['records'] if r['id'] == key)
    assert "a ship crew's exhaustion" in row['english']
    entry = prefs['records'][key]
    assert entry['required_pairs'] == [['ship', 'crew']]
    entry['required_pairs'] = []
    entry['reason'] = "Retain the original ordinary ship/crew's soft wrap. The earlier ship/crew pair did not match the actual possessive token and caused no compiled change; it is not a repaired defect."
    entry['justified_original_layout_retention'] = True
    prefs.update(previous_preferences=str(prior), previous_preferences_sha256=digest(prior),
        no_compiled_change_expected=True,
        evidence={str(p): digest(p) for p in [prior, ROOT/'plan_v3/automatic_plans.json', Path(__file__)]})
    save(target, prefs)
    print('Removed one inert pair; retained the actual ordinary genitive wrap. Compiled equality must still be verified.')


if __name__ == '__main__':
    main()
