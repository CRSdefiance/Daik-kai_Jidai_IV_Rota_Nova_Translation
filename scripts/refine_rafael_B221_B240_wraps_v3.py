"""Set the final phrase boundaries from the short-line review."""
import sys
from scripts.audit_story_glyph_consistency import load, save
from scripts.refine_rafael_B221_B240_wraps_v2 import PREFS as BEFORE, ROOT, env
from scripts.write_rafael_B221_B240_contextual_v1 import digest

PREFS = ROOT / 'ordinary_visual_preferences_v4.json'
REPLACE = {
    'DK4_MES_B221_R0027': dict(page_clause='the ruler of Japan.', line_phrases=['the ruler of Japan', 'ill fortune'],
        reason='Keep the core report and Tokugawa together. His full appositive starts the continuation.'),
    'DK4_MES_B221_R0030': dict(line_phrases=['East Asia', 'I thought you should', 'have word of it.']),
    'DK4_MES_B225_R0045': dict(line_phrases=['king of the sea', 'with many foreigners', 'the gold seal']),
    'DK4_MES_B234_R0042': dict(page_clause='I feel as though', line_phrases=['spirit of the East']),
    'DK4_MES_B238_R0040': dict(page_clause='to both the Eastern', line_phrases=['nomadic horsemen',
        'Asian origin.', 'Eastern and Western', 'Roman Empires'],
        reason='Keep the two named empires together at the start of the continuation.'),
    'DK4_MES_B239_R0016': dict(line_phrases=['go in,', "You've got to have the nerve", 'to commit.']),
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

