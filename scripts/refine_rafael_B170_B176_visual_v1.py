"""Resolve directly observed short rows and phrase splits, then isolate fresh native work."""
import sys

from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load, save
from scripts.plan_rafael_B170_B176_display_v1 import ROOT
from scripts.refine_rafael_B170_B176_wraps_v3 import MANUSCRIPT as PRIOR, PREFERENCES as PRIOR_PREFS


MANUSCRIPT = ROOT / 'ordinary_formatting_manuscript_v4.json'
PREFERENCES = ROOT / 'ordinary_visual_preferences_v5.json'
PLAN = ROOT / 'plans_v5/automatic_plans.json'
DELTA_MANUSCRIPT = ROOT / 'visual_delta_manuscript_v1.json'
DELTA_PLAN = ROOT / 'visual_delta_plan_v1.json'

CHANGES = {
    (170,50): ("That's not it. You've got a fever. You should turn in early tonight.",
               ("You've got a fever.", "You should turn in early tonight."),
               'Keep Carlo’s observation and advice in natural spoken units.'),
    (170,174): (None, ('take care of yourselves.', 'See you around.'),
                'Keep Carlo’s parting words together.'),
    (170,201): ('I admire your knack for trade, and how you look out for people.',
                ('your knack for trade,', 'and how you look out for people.'),
                'Rafael praises Carlo’s talent without assuming his occupation before the disclosure.'),
    (171,5): ('Whew. We had quite a bit to drink.', ('quite a bit to drink.',),
              'Give Rafael one natural thought and retain the amount they drank.'),
    (171,10): (None, ('A man of the sea', 'hold his liquor.', "She's doing just fine."),
               'Keep Claudio’s seafaring boast and the idiom hold his liquor.'),
    (172,11): ("What in the world?! A cow's lying in the middle of the road!",
               ('in the middle of the road!',), 'Keep the surprise, the cow and its exact position.'),
    (172,14): ('Nothing like home, is it?', ('home, is it?',),
               'Give Julio a brief observation and keep its tag on the same row.'),
    (173,99): ('Still, he set sail all alone... What kind of person does that?',
               ('Still, he set sail all alone...', 'What kind of person does that?'),
               'Keep Rafael’s interest in the solo feat without stranding his opening adverb.'),
    (174,6): ("Looks like it hasn't come back yet.", ("hasn't come back yet.",),
              'Keep the port worker’s tentative update together.'),
    (175,6): ("Looks like it hasn't come back yet.", ("hasn't come back yet.",),
              'Use the same natural update for this independently mapped occurrence.'),
    (176,47): ("So you found it and got aboard? How'd you get it moving? You did it all by yourself, right?",
               ('found it and got aboard?', "How'd you get it moving?", 'all by yourself, right?'),
               'Keep Rafael’s three questions and the connection between finding the ship and boarding it.'),
    (176,52): ('A bit of this, a bit of that... I just sort of winged it. Yahoo!',
               ('A bit of this, a bit of that...', 'winged it.'),
               'Keep Jam’s vague explanation intact, followed by the familiar cheer.'),
    (176,86): (None, ("Where there's a will,", "there's a way, huh..."),
               'Let Rafael repeat Jam’s proverb in two balanced clauses.'),
    (176,91): (None, ("It all works out because I'm me!", 'Life should be big and short!'),
               'Keep both complete boasts together in their own lines.'),
    (176,148): (None, ("Let's do this properly.", "I'm Jam Jack Ludwyan!"),
                'Keep Jam’s full spoken introduction in one phrase.'),
}


def digest(path):
    return sha(path.read_bytes())


def prepare():
    assert not MANUSCRIPT.exists() and not PREFERENCES.exists()
    doc, prefs = map(load, (PRIOR, PRIOR_PREFS))
    seen = set()
    for r in doc['records']:
        key = r['block'], r['source_record_index']
        if key not in CHANGES:
            continue
        replacement, phrases, note = CHANGES[key]
        if replacement is not None:
            assert r['decision'] == 'revision' and not r['native_literal_tokens']
            r.update(visual_revision_previous_English=r['english'], english=replacement,
                     editorial_logical_English=replacement,
                     planned_English_markup='{SPEAKER:'+format(r['source_selector'],'02X')+'}'+replacement,
                     finding=note, localization_note=note)
        prefs['records'][r['id']] = dict(line_phrases=phrases, reason=note,
            bindings={k: sha(r[k].encode('utf-8')) for k in ('source_hex','current_hex','english')})
        seen.add(key)
    assert seen == CHANGES.keys()
    doc.update(previous_manuscript=str(PRIOR), previous_manuscript_sha256=digest(PRIOR),
               directly_viewed_refinement_targets=sorted(seen), authored_breaks=0)
    save(MANUSCRIPT, doc)
    save(PREFERENCES, prefs)


def isolate():
    assert not DELTA_MANUSCRIPT.exists() and not DELTA_PLAN.exists()
    doc, new, old = map(load, (MANUSCRIPT, PLAN, ROOT/'plans_v4/automatic_plans.json'))
    assert new['manuscript_sha256'] == digest(MANUSCRIPT)
    assert not new['failures'] and len(new['records']) == len(old['records']) == 187
    changed = []
    for r, prior in zip(new['records'], old['records'], strict=True):
        assert r['id'] == prior['id'] and r['expected_native_pages'] == prior['expected_native_pages'] == 1
        if r['encoded_hex'] != prior['encoded_hex']:
            assert (r['block'], r['source_record_index']) in CHANGES
            changed.append(r)
        else:
            assert r['logical_English'] == prior['logical_English'] and r['lines'] == prior['lines']
    ids = {r['id'] for r in changed}
    save(DELTA_MANUSCRIPT, {**doc, 'records': [r for r in doc['records'] if r['id'] in ids],
                           'physical_speech_objects': len(ids), 'ordinary_speech_objects': len(ids)})
    save(DELTA_PLAN, {**new, 'records': changed, 'manuscript': str(DELTA_MANUSCRIPT),
                     'manuscript_sha256': digest(DELTA_MANUSCRIPT), 'complete_plan_sha256': digest(PLAN)})
    print(dict(fresh_render_records=len(ids), exact_unchanged_encodings=187-len(ids)))


if __name__ == '__main__':
    if sys.argv[1:] == ['--prepare']:
        prepare()
    else:
        isolate()
