"""Refine phrase flow while preserving the complete English and native geometry."""
from pathlib import Path
from types import FunctionType
import sys

from dk4tool.patch.grand_race_menu_release import sha
from scripts import plan_rafael_B168_B169_display_v1 as display
from scripts.audit_story_glyph_consistency import load, save


PREFERENCES = display.ROOT / 'visual_preferences_v2.json'
PLAN = display.ROOT / 'plans_v2/automatic_plans.json'
PHRASES = {
    7: (('for me, would you?',), 'Keep the keeper’s short tag with its phrase.'),
    28: (('them to gawk at',), 'Keep Ian’s objection intact without changing his internal voice.'),
    45: (('to the table over there',), 'Keep the destination together.'),
    52: (('Pour me a drink, will you?',), 'Keep the request and tag together after the taunt.'),
    66: (('Heh heh heh...',), 'Preserve the full leering laugh on one row.'),
    86: (('treat a customer',), 'Keep the sarcastic phrase intact.'),
    94: (('Could we get a drink over here?',), 'Keep Rafael’s request together after the salutation.'),
    102: (('line of work',), 'Keep the keeper’s familiar idiom together.'),
    110: (('without drawing a sword',), 'Keep the concrete restriction intact.'),
    114: (("have to let you go.",), 'Give the dismissal one complete phrase without a two-word tail.'),
    142: (('tavern work',), 'Keep the kind of work together.'),
    176: (("I'll go for",), 'Keep Ian’s tactical decision together after his hesitation.'),
    184: (('Watching you fight gets me going.',), 'Keep the assailant’s final appraisal together.'),
    216: (("You're a little slow, huh?",), 'Keep Claudio’s aside with its short tag.'),
    245: (('Um, actually...',), 'Keep Rafael’s audible hesitation together.'),
    254: (('around the world',), 'Keep the extent of the invitation together.'),
    279: (('out of work at the moment',), 'Keep Ian’s employment qualification in one phrase.'),
    291: (('My name is Ian Dukov.',), 'Keep Ian’s full introduction intact.'),
}


def prepare():
    assert not PREFERENCES.exists()
    prefs = load(display.PREFERENCES)
    assert load(display.PLAN)['manuscript_sha256'] == sha(display.MANUSCRIPT.read_bytes())
    for row in load(display.MANUSCRIPT)['records']:
        if row['block'] != 169 or row['source_record_index'] not in PHRASES:
            continue
        phrases, reason = PHRASES[row['source_record_index']]
        prefs['records'][row['id']] = dict(line_phrases=phrases, reason=reason,
            bindings={k: sha(row[k].encode('utf-8')) for k in ('source_hex', 'current_hex', 'english')})
    save(PREFERENCES, prefs)


if __name__ == '__main__':
    if sys.argv[1:] == ['--prepare']:
        prepare()
    else:
        FunctionType(display.isolate.__code__, {**display.isolate.__globals__, 'PLAN': PLAN})()
