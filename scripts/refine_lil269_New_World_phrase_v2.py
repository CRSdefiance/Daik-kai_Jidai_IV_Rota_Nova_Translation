"""Keep the complete to-the-New-World phrase without waiving weak-ending checks."""
from pathlib import Path
from scripts.audit_story_glyph_consistency import load, save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest

ROOT = Path('work/Lil269_B243_B282_clean_20261110')

if __name__ == '__main__':
    before = ROOT / 'formatting_v2/viewed_preferences_v7.json'
    output = ROOT / 'formatting_v2/viewed_preferences_v8.json'
    assert not output.exists()
    issues = load(ROOT / 'plan_v7/diagnostics.json')['issues']
    warnings = [x for x in issues if x['severity'] == 'warning']
    assert len(warnings) == 1 and warnings[0]['id'] == 'DK4_MES_B243_R0018'
    assert warnings[0]['code'] == 'weak-line-ending'
    prefs = load(before)
    target = prefs['records']['DK4_MES_B243_R0018']
    target['required_pairs'].extend([['the', 'new'], ['to', 'the']])
    target['reason'] += ' Keep the complete to the New World phrase together rather than ending a row on the.'
    prefs.update(previous_preferences=str(before), previous_preferences_sha256=digest(before),
        earlier_warning_preserved_andnot_waived=True)
    save(output, prefs)
