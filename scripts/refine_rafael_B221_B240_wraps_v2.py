"""Resolve remaining phrase, short-line and page-ending findings from the first refinement."""
from pathlib import Path
import sys

from scripts.audit_story_glyph_consistency import load, save
from scripts.refine_rafael_B221_B240_wraps_v1 import PREFS as BEFORE, ROOT, env
from scripts.write_rafael_B221_B240_contextual_v1 import digest

PREFS = ROOT / 'ordinary_visual_preferences_v3.json'
REPLACE = {
    'DK4_MES_B221_R0027': dict(line_phrases=['ruler of Japan', 'the legendary Muramasa']),
    'DK4_MES_B221_R0030': dict(line_phrases=['East Asia', 'have word of it.']),
    'DK4_MES_B224_R0078': dict(line_phrases=['Zhuge Liang', 'Memorial on the Expedition', "doesn't it?"]),
    'DK4_MES_B225_R0045': dict(page_clause='Give my sword', line_phrases=['king of the sea', 'the gold seal'],
        reason='Complete the predictions about the ruler and seal before the final instruction.'),
    'DK4_MES_B234_R0042': dict(page_clause=None, line_phrases=['spirit of the East', 'a man with such nerve']),
    'DK4_MES_B238_R0040': dict(line_phrases=['nomadic horsemen', 'Asian origin.', 'Attila was their king.', 'Roman Empires']),
    'DK4_MES_B239_R0016': dict(line_phrases=['go in,', "You've got to have", 'the nerve to commit.']),
}

if __name__ == '__main__':
    if sys.argv[1:] == ['--prepare']:
        assert not PREFS.exists()
        prefs = load(BEFORE)
        for ident, changes in REPLACE.items():
            prefs['records'][ident].update(changes)
        prefs['previous_preferences_sha256'] = digest(BEFORE)
        save(PREFS, prefs)
    else:
        env['main']()

