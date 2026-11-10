"""Apply only visual refinements that fit naturally within the existing native pages."""
import sys

from scripts.audit_story_glyph_consistency import load, save
from scripts.refine_rafael_B221_B240_wraps_v5 import PREFS as BEFORE, ROOT, env
from scripts.write_rafael_B221_B240_contextual_v1 import digest

PREFS = ROOT / 'ordinary_visual_preferences_v7.json'
PLAN = ROOT / 'ordinary_plans_v7/automatic_plans.json'
BASE = ROOT / 'ordinary_plans_v5/automatic_plans.json'

if __name__ == '__main__':
    if sys.argv[1:] == ['--prepare']:
        assert not PREFS.exists()
        prefs = load(BEFORE)
        records = prefs['records']
        for ident in ('DK4_MES_B225_R0066', 'DK4_MES_B232_R0027'):
            del records[ident]
        records['DK4_MES_B237_R0028'].update(one_page=False, line_phrases=['Tours and Poitiers', 'Iberian Peninsula'],
            reason='Retain two pages to keep both location names and the reviewed sentence intact.')
        records['DK4_MES_B237_R0049']['line_phrases'] = ['of Charles Martel']
        records['DK4_MES_B230_R0013']['line_phrases'] = ['They call it', 'the Holy Spear of Ares.', 'gods of Olympus.']
        records['DK4_MES_B224_R0062']['line_phrases'] = ['Never did find it.']
        records['DK4_MES_B225_R0041']['line_phrases'] = ['Two hundred years from now,', 'Master of the Ocean']
        prefs['previous_preferences_sha256'] = digest(BEFORE)
        save(PREFS, prefs)
    else:
        env['main']()

