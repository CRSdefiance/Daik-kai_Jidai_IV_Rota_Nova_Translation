"""Resolve phrase and substitution findings from the directly viewed story pages."""
import sys

from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load, save
from scripts.refine_rafael_B181_B187_story_v1 import OUT as PRIOR, PREFS as PRIOR_PREFS, ROOT


OUT = ROOT / 'story_formatting_manuscript_v3.json'
PREFS = ROOT / 'story_visual_preferences_v3.json'
PLAN = ROOT / 'story_plans_v3/automatic_plans.json'
OLD_PLAN = ROOT / 'story_plans_v2/automatic_plans.json'
DELTA_DOC = ROOT / 'story_delta_manuscript_v1.json'
DELTA_PLAN = ROOT / 'story_delta_plan_v1.json'
CHANGES = {
    (181,14): (None, ("I've got a bad feeling about this...",), 'Keep Claudio’s hunch intact before his suggestion.'),
    (181,27): (None, ('Why do you ask?',), 'Keep Rafael’s short question together.'),
    (181,67): (None, ("what I'm made of!",), 'Keep the idiom that ends Yifa’s boast.'),
    (181,111): (None, ("Don't blame me if you get hurt.",), 'Keep Claudio’s warning intact.'),
    (181,144): (None, ('caught me off guard!',), 'Keep Claudio’s accusation intact.'),
    (183,47): (None, ("our teacher's leave.",), 'Keep the permission phrase intact.'),
    (183,59): (None, ('a grave offense.',), 'Keep the reason for the expulsion intact.'),
    (183,75): (None, ('keep up her training,',), 'Keep the instruction to continue training intact.'),
    (183,97): ("I can feel him! My senior from the school!", ('My senior from the school!',),
        'Yifa senses the senior student before Rafael identifies him by name.'),
    (183,134): (None, ("He'll always be such a worrier.",), 'Keep Yifa’s fond characterization together.'),
    (184,27): (None, ('day or night.',), 'Keep the expression of continual preoccupation together.'),
    (184,52): (None, ('as soon as I can',), 'Keep the promise about timing together.'),
    (184,59): ("You haven't even found it yet. A bit eager, aren't you? All right, I'll think about it.",
        ("A bit eager, aren't you?",), 'Keep Mihwa’s teasing question and tentative reply.'),
    (184,85): (None, ('How about you,',), 'Keep the short invitation with its source name substitution.'),
    (184,99): (None, ('talk into things.)',), 'Keep Rafael’s idiom together in his aside.'),
    (185,18): ('Ever heard of the Silla Gold Crown?', ('Silla Gold Crown',), 'Keep Claudio’s inquiry direct and the full item name intact.'),
    (185,21): (None, ('Why do you ask?',), 'Keep Reika’s short follow-up question together.'),
    (185,28): ('Is everyone after the Silla Gold Crown these days? Someone just asked me the same thing.',
        ('Silla Gold Crown',), 'Keep the dry joke about two people looking for the crown and the reason she asks.'),
    (185,50): ("It's a historic site near here. They say you can find the Silla Gold Crown there.",
        ('the Silla Gold Crown there.',), 'Keep the site description and the location of the crown as hearsay.'),
    (186,22): (None, ("Wasn't that kind of them?",), 'Keep Julian’s pointed question intact.'),
    (186,41): (None, ('how can I repay you?',), 'Keep Julian’s offer of repayment together.'),
    (186,79): (None, ('"I\'ll give it to her myself!"',), 'Keep Claudio’s quote together.'),
    (186,114): (None, ('waste any time, do you?',), 'Keep Mihwa’s complaint and its tag together.'),
    (186,199): ("You're leaving now, aren't you? You don't have time for a date.",
        ("You're leaving now, aren't you?",), 'Keep Mihwa’s tag with her question about his immediate departure.'),
    (187,15): ("You're with {MACRO:FO}, aren't you? Fancy meeting you here.",
        ("aren't you?", 'Fancy meeting you here.'), 'Preserve Aziza’s recognition and avoid attaching an ellipsis to a faction name that already ends in a period.'),
    (187,83): (None, ("You've got guts, boy.",), 'Keep her direct compliment intact.'),
}


def digest(path):
    return sha(path.read_bytes())


def prepare():
    assert not OUT.exists() and not PREFS.exists()
    doc, prefs = map(load, (PRIOR, PRIOR_PREFS))
    seen = set()
    for row in doc['records']:
        key = row['block'], row['source_record_index']
        if key not in CHANGES:
            continue
        replacement, phrases, reason = CHANGES[key]
        if replacement is not None:
            assert row['decision'] == 'revision'
            assert all(replacement.count('{MACRO:'+token+'}') == count
                for token, count in row['native_literal_token_counts'].items())
            logical = replacement
            for token in row['native_literal_tokens']:
                logical = logical.replace('{MACRO:'+token+'}', token)
            row.update(visual_revision_previous_English=row['editorial_logical_English'], english=replacement,
                editorial_logical_English=logical, planned_English_markup=f"{{SPEAKER:{row['source_selector']:02X}}}" + replacement,
                finding=reason, localization_note=reason)
        old = prefs['records'].get(row['id'], {}).get('line_phrases', [])
        retained = [p for p in old if p in row['english'] and not any(p in q for q in phrases)]
        phrases = [*retained, *phrases]
        assert all(p in row['english'] for p in phrases)
        prefs['records'][row['id']] = dict(line_phrases=phrases, reason=reason,
            bindings={k: sha(row[k].encode('utf-8')) for k in ('source_hex','current_hex','english')})
        seen.add(key)
    assert seen == CHANGES.keys()
    doc.update(previous_manuscript=str(PRIOR), previous_manuscript_sha256=digest(PRIOR),
        directly_viewed_refinement_targets=sorted(seen), authored_breaks=0)
    save(OUT, doc)
    save(PREFS, prefs)


def isolate():
    assert not DELTA_DOC.exists() and not DELTA_PLAN.exists()
    doc, new, old = map(load, (OUT, PLAN, OLD_PLAN))
    assert not new['failures'] and len(new['records']) == len(old['records']) == 227
    assert new['manuscript_sha256'] == digest(OUT)
    assert not any(i['severity'] in ('warning','error') for row in new['records'] for i in row['base_QA']['issues'])
    changed = []
    for row, prior in zip(new['records'], old['records'], strict=True):
        assert row['id'] == prior['id'] and row['expected_native_pages'] == prior['expected_native_pages'] == 1
        if row['encoded_hex'] != prior['encoded_hex']:
            assert (row['block'], row['source_record_index']) in CHANGES
            changed.append(row)
        else:
            assert row['logical_English'] == prior['logical_English'] and row['lines'] == prior['lines']
    ids = {r['id'] for r in changed}
    save(DELTA_DOC, {**doc, 'records': [r for r in doc['records'] if r['id'] in ids], 'physical_speech_objects': len(ids)})
    save(DELTA_PLAN, {**new, 'records': changed, 'manuscript': str(DELTA_DOC),
        'manuscript_sha256': digest(DELTA_DOC), 'complete_plan_sha256': digest(PLAN)})
    print(dict(fresh_render_records=len(ids), exact_unchanged_encodings=227-len(ids)))


if __name__ == '__main__':
    if sys.argv[1:] == ['--prepare']:
        prepare()
    else:
        isolate()
