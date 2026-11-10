"""Finish the continuing prophecy layout using its native available width."""
import sys
from scripts.audit_story_glyph_consistency import load, save
from scripts.refine_rafael_B221_B240_wraps_v3 import PREFS as BEFORE, ROOT, env
from scripts.write_rafael_B221_B240_contextual_v1 import digest

PREFS = ROOT / 'ordinary_visual_preferences_v5.json'
if __name__ == '__main__':
    if sys.argv[1:] == ['--prepare']:
        assert not PREFS.exists()
        prefs = load(BEFORE)
        prefs['records']['DK4_MES_B225_R0045'].update(page_clause=None,
            line_phrases=['king of the sea', 'with many foreigners', 'the gold seal', 'a land I could not rule.'],
            reason='Keep each prediction’s object and the closing reference to the land intact. Use all available rows.')
        prefs['previous_preferences_sha256'] = digest(BEFORE)
        save(PREFS, prefs)
    else:
        env['main']()

