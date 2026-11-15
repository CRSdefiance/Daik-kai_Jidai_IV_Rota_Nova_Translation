"""Resolve the trial wrap warnings and isolate the changed native records."""
import sys

from scripts.audit_story_glyph_consistency import load, save
from scripts.refine_rafael_B241_B260_wraps_v3 import MANUSCRIPT, ROOT, digest


PREFS = ROOT / 'ordinary_visual_preferences_v6.json'
PLAN = ROOT / 'ordinary_plans_v6/automatic_plans.json'
BEFORE = ROOT / 'ordinary_plans_v3/automatic_plans.json'
DELTA_MANUSCRIPT = ROOT / 'ordinary_visual_delta_manuscript_v1.json'
DELTA = ROOT / 'ordinary_visual_delta_plan_v1.json'


def preferences():
    previous = ROOT / 'ordinary_visual_preferences_v5.json'
    assert not PREFS.exists()
    prefs = load(previous)
    rules = prefs['records']
    rules['DK4_MES_B242_R0068'].update(ordinary_boundaries=[],
        line_phrases=['you put in, Samwell,', 'about the Phoenix Bascinet.'])
    rules['DK4_MES_B252_R0116'].update(ordinary_boundaries=[],
        line_phrases=["I'm turning him", "in at the governor's office!"])
    prefs['previous_preferences_sha256'] = digest(previous)
    save(PREFS, prefs)


def isolate():
    assert not DELTA_MANUSCRIPT.exists() and not DELTA.exists()
    doc, before, after = map(load, (MANUSCRIPT, BEFORE, PLAN))
    assert before['manuscript_sha256'] == after['manuscript_sha256'] == digest(MANUSCRIPT)
    assert not after['failures']
    changes = []
    for old, new in zip(before['records'], after['records'], strict=True):
        assert old['id'] == new['id'] and old['logical_English'] == new['logical_English']
        assert all(issue['severity'] == 'info' for issue in new['base_QA']['issues'])
        if old['encoded_hex'] != new['encoded_hex']:
            changes.append(new)
    ids = {row['id'] for row in changes}
    rows = [row for row in doc['records'] if row['id'] in ids]
    assert len(rows) == len(ids) == len(changes)
    save(DELTA_MANUSCRIPT, {**doc, 'records': rows, 'blocks': sorted({r['block'] for r in rows}),
        'physical_speech_objects': len(rows), 'typed_choice_objects': 0, 'typed_choice_commands': 0})
    save(DELTA, {**after, 'records': changes, 'manuscript': str(DELTA_MANUSCRIPT),
        'manuscript_sha256': digest(DELTA_MANUSCRIPT), 'complete_plan': str(PLAN), 'complete_plan_sha256': digest(PLAN)})
    print([(row['id'], row['lines']) for row in changes], flush=True)


if __name__ == '__main__':
    if sys.argv[1:] == ['--prepare']:
        preferences()
    else:
        isolate()
