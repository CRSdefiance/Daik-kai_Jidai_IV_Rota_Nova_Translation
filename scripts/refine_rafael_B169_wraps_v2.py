"""Correct four visually identified phrase breaks with exact row-level rechecks."""
import sys

from dk4tool.patch.grand_race_menu_release import sha
from scripts import plan_rafael_B168_B169_display_v1 as display
from scripts import refine_rafael_B169_wraps_v1 as prior
from scripts.audit_story_glyph_consistency import load, save


ROOT = display.ROOT
PREFERENCES = ROOT / 'visual_preferences_v3.json'
PLAN = ROOT / 'plans_v3/automatic_plans.json'
MANUSCRIPT = ROOT / 'visual_delta_manuscript_v1.json'
DELTA = ROOT / 'visual_delta_plan_v1.json'
FINDINGS = {
    28: (('Give it a rest.', 'for them to gawk at'), 'Keep the exasperated idiom and objection intact.'),
    198: (('stand there watching', 'if I help, do you?'), 'Keep the act of watching and the invitation tag together.'),
    279: (("I'm a navigator, though", "I'm out of work at the moment..."), 'Keep both contractions with their phrases.'),
    291: (("I'd be honored", 'aboard your ship.', 'My name is Ian Dukov.'), 'Keep Ian’s formal request and full introduction together.'),
}


def prepare():
    assert not PREFERENCES.exists()
    prefs = load(prior.PREFERENCES)
    for row in load(display.MANUSCRIPT)['records']:
        n = row['source_record_index']
        if row['block'] != 169 or n not in FINDINGS:
            continue
        phrases, reason = FINDINGS[n]
        prefs['records'][row['id']] = dict(line_phrases=phrases, reason=reason,
            bindings={k: sha(row[k].encode('utf-8')) for k in ('source_hex', 'current_hex', 'english')})
    save(PREFERENCES, prefs)


def isolate():
    assert not MANUSCRIPT.exists() and not DELTA.exists()
    doc, plan, old = map(load, (display.MANUSCRIPT, PLAN, prior.PLAN))
    assert not plan['failures'] and len(plan['records']) == len(old['records']) == 115
    changed = []
    for after, before in zip(plan['records'], old['records'], strict=True):
        assert after['id'] == before['id'] and after['logical_English'] == before['logical_English']
        if after['encoded_hex'] != before['encoded_hex']:
            assert after['block'] == 169 and after['source_record_index'] in FINDINGS
            changed.append(after)
    assert len(changed) == len(FINDINGS)
    ids = {r['id'] for r in changed}
    save(MANUSCRIPT, {**doc, 'records': [r for r in doc['records'] if r['id'] in ids],
                      'physical_speech_objects': len(ids), 'ordinary_speech_objects': len(ids)})
    save(DELTA, {**plan, 'records': changed, 'manuscript': str(MANUSCRIPT), 'manuscript_sha256': sha(MANUSCRIPT.read_bytes()),
                 'complete_plan_sha256': sha(PLAN.read_bytes())})


if __name__ == '__main__':
    if sys.argv[1:] == ['--prepare']:
        prepare()
    else:
        isolate()
