"""Keep the source's New World name intact in the denser sailor-rumor layout."""
from pathlib import Path
from scripts.audit_story_glyph_consistency import load, save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest

ROOT = Path('work/Lil269_B243_B282_clean_20261110')

if __name__ == '__main__':
    before = ROOT / 'formatting_v2/viewed_preferences_v6.json'
    output = ROOT / 'formatting_v2/viewed_preferences_v7.json'
    assert not output.exists()
    prefs = load(before)
    target = prefs['records']['DK4_MES_B243_R0018']
    assert target['one_page'] and ['golden', 'sand'] in target['required_pairs']
    target['required_pairs'].append(['new', 'world'])
    target['reason'] += ' Keep the source New World geographic name together in the new denser rows.'
    prefs.update(previous_preferences=str(before), previous_preferences_sha256=digest(before))
    save(output, prefs)
