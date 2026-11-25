"""Refine exact titles, question tags and connected phrases found on the final-size sheets."""
import sys

from scripts.audit_story_glyph_consistency import load, save
from scripts.plan_rafael_B221_B240_v1 import FORMATTING, ROOT, planner
from scripts.refine_rafael_B221_B240_wraps_v4 import PREFS as BEFORE, env
from scripts.write_rafael_B221_B240_contextual_v1 import digest

PREFS = ROOT / 'ordinary_visual_preferences_v6.json'
PLAN = ROOT / 'ordinary_plans_v6/automatic_plans.json'
PHRASES = {
    'SC0_B221_STYLE_702_270': ['through and through.'],
    'DK4_MES_B222_R0016': ['faint red tint.'],
    'DK4_MES_B223_R0047': ['Want to go look?'],
    'DK4_MES_B224_R0005': ['Romance of the Three Kingdoms?'],
    'DK4_MES_B224_R0062': ['find it.'],
    'DK4_MES_B225_R0041': ['Master of the Ocean'],
    'DK4_MES_B225_R0066': ['Shandong Peninsula.'],
    'DK4_MES_B227_R0019': ['What can I do for you?'],
    'DK4_MES_B228_R0028': ['sacred sword'],
    'DK4_MES_B230_R0013': ['Holy Spear of Ares.', 'gods of Olympus.'],
    'DK4_MES_B232_R0027': ['Empress Gown.'],
    'DK4_MES_B233_R0029': ['Holy Land, right?'],
    'DK4_MES_B234_R0055': ["didn't it, Gerhard?"],
    'DK4_MES_B235_R0034': ['coat of mail'],
    'DK4_MES_B236_R0026': ['Medusa Shield'],
    'DK4_MES_B237_R0005': ['Charles Martel'],
    'DK4_MES_B237_R0028': ['Iberian Peninsula'],
    'DK4_MES_B237_R0049': ['Charles Martel, Admiral.'],
    'DK4_MES_B238_R0040': ['nomadic horsemen', 'Asian origin.', 'They say he once',
                          'Eastern and Western', 'Roman Empires'],
    'DK4_MES_B240_R0030': ["Wouldn't you want one?", 'harder than iron!'],
}

if __name__ == '__main__':
    if sys.argv[1:] == ['--prepare']:
        assert not PREFS.exists()
        prefs = load(BEFORE)
        rows = {row['id']: row for row in load(FORMATTING)['records']}
        for ident, phrases in PHRASES.items():
            row = rows[ident]
            rule = prefs['records'].setdefault(ident, {'bindings': {
                key: planner.sha(row[key].encode('utf-8')) for key in ('source_hex', 'current_hex', 'english')
            }})
            rule.update(line_phrases=phrases, final_size_visual_review_finding='Keep the marked phrase together.',
                        reason='Keep the marked phrase together at the measured native width.')
        prefs['records']['DK4_MES_B237_R0028']['one_page'] = True
        prefs['previous_preferences_sha256'] = digest(BEFORE)
        save(PREFS, prefs)
    else:
        env['main']()

