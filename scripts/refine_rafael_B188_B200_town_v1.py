"""Refine visible phrase breaks and isolate only changed encoded town pages."""
import sys

from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load, save
from scripts.plan_rafael_B188_B200_town_v1 import FORMATTING, PREFERENCES, ROOT


MANUSCRIPT = ROOT / 'town_formatting_manuscript_v2.json'
PREFS = ROOT / 'town_visual_preferences_v2.json'
BASE = ROOT / 'town_plans_v1/automatic_plans.json'
PLAN = ROOT / 'town_plans_v2/automatic_plans.json'
DELTA_DOC = ROOT / 'town_delta_manuscript_v1.json'
DELTA_PLAN = ROOT / 'town_delta_plan_v1.json'
CHANGES = {
    (188, 35): (None, ("It's the dawn of the banana age!",), 'Keep the comic banana-age declaration together.'),
    (189, 12): (None, ('set my heart on fire',), 'Keep the idiom intact as she remembers a passionate love.'),
    (189, 27): (None, ('pass us by, you hear?',), 'Keep the warning and tag together.'),
    (190, 21): (None, ('on the corner',), 'Keep the corner location together.'),
    (190, 40): ("Let's go buy the ingredients now.", (), 'Keep the immediate group decision to buy ingredients.'),
    (194, 14): (None, ("Just what you'd expect of the duke...",), 'Keep the full reaction about the duke together.'),
    (194, 21): (None, ('What kind of stone is it?',), 'Keep the question about the stone intact.'),
    (195, 42): (None, ('the artist who painted this one!',), 'Keep the identification of the painter intact.'),
    (195, 57): (None, ('every time they come in.',), 'Keep the recurring frequency as one phrase.'),
    (195, 73): (None, ('all the rage lately.',), 'Keep the idiom and its time frame together.'),
    (195, 83): (None, ('mince words, do you?',), 'Keep the idiom and tag together.'),
    (195, 87): ('Oops. Keep it between us, okay?', (), 'The shopkeeper catches himself and asks for discretion.'),
    (196, 33): ("We can't live without our tea.", (), 'Keep the shared joke as a declaration, as in the source.'),
    (198, 13): (None, ('Sweet is what matters.',), 'Keep the emphatic declaration of sweet together before the echo.'),
    (200, 14): (None, ('a craftsman of some renown.',), 'Keep the single description of the maker together.'),
    (200, 38): (None, ("I'll add it to my collection.",), 'Keep his collecting decision together before the command.'),
}


def digest(path):
    return sha(path.read_bytes())


def prepare():
    assert not MANUSCRIPT.exists() and not PREFS.exists()
    doc, prefs = map(load, (FORMATTING, PREFERENCES))
    seen = set()
    for row in doc['records']:
        key = row['block'], row['source_record_index']
        if key not in CHANGES:
            continue
        replacement, phrases, reason = CHANGES[key]
        if replacement is not None:
            assert row['decision'] == 'revision' and not row['native_literal_tokens']
            row.update(visual_revision_previous_English=row['english'], english=replacement,
                editorial_logical_English=replacement, planned_English_markup=f"{{SPEAKER:{row['source_selector']:02X}}}" + replacement,
                finding=reason, localization_note=reason)
        prefs['records'][row['id']] = dict(line_phrases=phrases, reason=reason,
            bindings={k: sha(row[k].encode('utf-8')) for k in ('source_hex', 'current_hex', 'english')})
        seen.add(key)
    assert seen == CHANGES.keys()
    doc.update(previous_manuscript=str(FORMATTING), previous_manuscript_sha256=digest(FORMATTING),
        directly_viewed_refinement_targets=sorted(seen), authored_breaks=0)
    save(MANUSCRIPT, doc)
    save(PREFS, prefs)


def isolate():
    assert not DELTA_DOC.exists() and not DELTA_PLAN.exists()
    doc, new, old = map(load, (MANUSCRIPT, PLAN, BASE))
    assert not new['failures'] and len(new['records']) == len(old['records']) == 157
    assert new['manuscript_sha256'] == digest(MANUSCRIPT)
    assert not any(i['severity'] in ('warning', 'error') for row in new['records'] for i in row['base_QA']['issues'])
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
    print(dict(fresh_render_records=len(ids), exact_unchanged_encodings=157-len(ids)))


if __name__ == '__main__':
    if sys.argv[1:] == ['--prepare']:
        prepare()
    else:
        isolate()
