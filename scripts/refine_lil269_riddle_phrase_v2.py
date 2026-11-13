"""Attach the riddle's second with to its following noun phrase."""
from pathlib import Path
from scripts.audit_story_glyph_consistency import load, save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest

ROOT = Path('work/Lil269_B243_B282_clean_20261110')

if __name__ == '__main__':
    before = ROOT / 'formatting_v2/viewed_preferences_v9.json'
    output = ROOT / 'formatting_v2/viewed_preferences_v10.json'
    assert not output.exists()
    warnings = [x for x in load(ROOT / 'plan_v9/diagnostics.json')['issues'] if x['severity'] == 'warning']
    assert len(warnings) == 1 and warnings[0]['id'] == 'DK4_MES_B251_R0009'
    assert warnings[0]['code'] == 'weak-line-ending'
    prefs = load(before)
    prefs['records']['DK4_MES_B251_R0009']['required_pairs'].append(['with', 'a'])
    prefs['records']['DK4_MES_B251_R0009']['reason'] += ' Keep with a together rather than leaving with at the end of the first row.'
    prefs.update(previous_preferences=str(before), previous_preferences_sha256=digest(before),
        earlier_weak_ending_warning_preserved_not_waived=True)
    save(output, prefs)
