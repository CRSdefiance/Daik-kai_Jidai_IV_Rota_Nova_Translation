"""Keep Rafael’s rescue offer in two complete thoughts and render that page afresh."""
import sys

from dk4tool.patch.grand_race_menu_release import sha
from scripts import plan_rafael_B168_B169_display_v1 as display
from scripts import refine_rafael_B169_wraps_v2 as prior
from scripts.audit_story_glyph_consistency import load, save


ROOT = display.ROOT
MANUSCRIPT = ROOT / 'formatting_manuscript_v2.json'
PREFERENCES = ROOT / 'visual_preferences_v4.json'
PLAN = ROOT / 'plans_v4/automatic_plans.json'
DELTA_M = ROOT / 'intervention_manuscript_v1.json'
DELTA_P = ROOT / 'intervention_plan_v1.json'
TARGET = 'DK4_MES_B169_R0198'
TEXT = "I couldn't just stand by and watch. You don't mind if I help, do you?"


def digest(path):
    return sha(path.read_bytes())


def prepare():
    assert not MANUSCRIPT.exists() and not PREFERENCES.exists()
    doc, prefs = map(load, (display.MANUSCRIPT, prior.PREFERENCES))
    row = next(r for r in doc['records'] if r['id'] == TARGET)
    old = row['english']
    assert old == "I couldn't just stand there watching. You don't mind if I help, do you?"
    note = "Keep Rafael's inability to stand by and his informal offer. The idiom gives him two complete spoken thoughts."
    row.update(english=TEXT, editorial_logical_English=TEXT, planned_English_markup='{SPEAKER:00}'+TEXT,
               finding=note, localization_note=note, visual_revision_previous_English=old)
    prefs['records'][TARGET] = dict(line_phrases=["I couldn't just stand by and watch.", "You don't mind if I help, do you?"],
        reason=note, bindings={k: sha(row[k].encode('utf-8')) for k in ('source_hex', 'current_hex', 'english')})
    save(MANUSCRIPT, {**doc, 'B169_visual_dialogue_refinement': TARGET, 'previous_manuscript_sha256': digest(display.MANUSCRIPT)})
    save(PREFERENCES, prefs)


def isolate():
    assert not DELTA_M.exists() and not DELTA_P.exists()
    doc, plan, old = map(load, (MANUSCRIPT, PLAN, prior.PLAN))
    assert plan['manuscript_sha256'] == digest(MANUSCRIPT)
    assert not plan['failures'] and len(plan['records']) == len(old['records']) == 115
    for before, after in zip(old['records'], plan['records'], strict=True):
        assert before['id'] == after['id']
        if after['id'] != TARGET:
            assert all(before[k] == after[k] for k in ('lines', 'logical_English', 'encoded_hex', 'expected_native_pages', 'base_QA'))
    delta = next(r for r in plan['records'] if r['id'] == TARGET)
    assert len(delta['lines']) == 2 and delta['expected_native_pages'] == 1
    save(DELTA_M, {**doc, 'records': [r for r in doc['records'] if r['id'] == TARGET],
                   'physical_speech_objects': 1, 'ordinary_speech_objects': 1})
    save(DELTA_P, {**plan, 'records': [delta], 'manuscript': str(DELTA_M), 'manuscript_sha256': digest(DELTA_M),
                   'complete_plan_sha256': digest(PLAN)})


if __name__ == '__main__':
    if sys.argv[1:] == ['--prepare']:
        prepare()
    else:
        isolate()
