"""Attach the final short tag and retain the complete Forbidden City noun phrase."""
from pathlib import Path
from scripts.audit_story_glyph_consistency import load, save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest

ROOT = Path('work/Lil269_B243_B282_clean_20261110')

if __name__ == '__main__':
    before = ROOT / 'formatting_v2/viewed_preferences_v12.json'
    output = ROOT / 'formatting_v2/viewed_preferences_v13.json'
    assert not output.exists()
    prefs = load(before)
    for key, pairs, reason in [
        ('DK4_MES_B270_R0013', [['help', "won't"], ["won't", 'you']], ' Attach the short won\'t you tag to You\'ll help.'),
        ('DK4_MES_B271_R0067', [['the', 'forbidden'], ['to', 'the']], ' Keep to the Forbidden City together instead of ending a row on the or to.'),
    ]:
        prefs['records'][key]['required_pairs'].extend(pairs)
        prefs['records'][key]['reason'] += reason
    prefs.update(previous_preferences=str(before), previous_preferences_sha256=digest(before))
    save(output, prefs)
