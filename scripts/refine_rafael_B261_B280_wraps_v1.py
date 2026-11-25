"""Refine the spoken arrival and the wording of the inscribed question."""
from scripts.plan_rafael_B261_B280_v1 import FORMATTING, PREFERENCES, ROOT
from scripts.write_rafael_B261_B280_contextual_v1 import OUT, load, save, sha


REVIEW = OUT.with_name('rafael_B261_B280_contextual_review_v2.json')
MANUSCRIPT = FORMATTING.with_name('ordinary_formatting_manuscript_v2.json')
PREFS = PREFERENCES.with_name('ordinary_visual_preferences_v2.json')
DIAGNOSTICS = ROOT / 'initial_plan_v1/diagnostics.json'
JEAN = 'DK4_MES_B267_R0005'
ICE = 'DK4_MES_B261_R0009'


def main():
    assert not any(path.exists() for path in (REVIEW, MANUSCRIPT, PREFS))
    doc, formatting, prefs, diagnostics = map(load, (OUT, FORMATTING, PREFERENCES, DIAGNOSTICS))
    assert formatting['manuscript_sha256'] == sha(OUT.read_bytes())
    assert [row['id'] for row in diagnostics['issues'] if row['severity'] == 'warning'] == [ICE, JEAN]
    assert not diagnostics['failures']
    revised = "Well, they hauled Jean in."
    note = (
        "Keep the guild contact's amused recognition, Jean's name and the rough arrival. "
        "The active sentence lets Jean answer without a redundant second identification."
    )
    for packet in (doc, formatting):
        row = next(row for row in packet['records'] if row['id'] == JEAN)
        assert row['english'] == "Well, look who's been dragged in. It's Jean."
        assert row['decision'] == 'revision' and not row['review']['formatting']
        row.update(english=revised, finding=note, localization_note=note, previous_review_English=row['english'])
        if packet is formatting:
            row.update(editorial_logical_English=revised, planned_English_markup='{SPEAKER:93}' + revised)
    doc.update(
        previous_contextual_review=str(OUT), previous_contextual_review_sha256=sha(OUT.read_bytes()),
        single_read_aloud_refinement=JEAN,
    )
    doc['evidence'][str(DIAGNOSTICS)] = sha(DIAGNOSTICS.read_bytes())
    save(REVIEW, doc)
    formatting.update(manuscript_sha256=sha(REVIEW.read_bytes()), parent_contextual_proof=str(REVIEW))
    save(MANUSCRIPT, formatting)
    ice = next(row for row in formatting['records'] if row['id'] == ICE)
    prefs['records'][ICE] = dict(
        line_phrases=['the water level'], reason='Keep the object of the puzzle question together.',
        bindings={key: sha(ice[key].encode('utf-8')) for key in ('source_hex', 'current_hex', 'english')},
    )
    save(PREFS, prefs)
    print('Saved one spoken refinement and one semantic wrap preference. All other paragraphs are unchanged.')


def refine_inscription():
    review = REVIEW.with_name('rafael_B261_B280_contextual_review_v3.json')
    manuscript = MANUSCRIPT.with_name('ordinary_formatting_manuscript_v3.json')
    preferences = PREFS.with_name('ordinary_visual_preferences_v3.json')
    failed = ROOT / 'refined_plan_v1/diagnostics.json'
    assert not any(path.exists() for path in (review, manuscript, preferences))
    doc, formatting, prefs, diagnostics = map(load, (REVIEW, MANUSCRIPT, PREFS, failed))
    assert [row['id'] for row in diagnostics['issues'] if row['severity'] == 'warning'] == [ICE]
    assert not diagnostics['failures']
    revised = (
        'A vessel is filled to the brim with water. A piece of ice floats on the surface. '
        'When the ice melts, what happens to the water level?'
    )
    note = (
        'Keep the brim and floating ice as the premises. Put the condition first so the '
        'inscription asks a complete, open question without implying a change in level.'
    )
    for packet in (doc, formatting):
        row = next(row for row in packet['records'] if row['id'] == ICE)
        assert row['english'].endswith('What happens to the water level when the ice melts?')
        assert row['decision'] == 'revision' and not row['review']['formatting']
        row.update(english=revised, finding=note, localization_note=note, previous_review_English=row['english'])
        if packet is formatting:
            row.update(editorial_logical_English=revised, planned_English_markup='{SPEAKER:FE}' + revised)
    doc.update(previous_contextual_review=str(REVIEW), previous_contextual_review_sha256=sha(REVIEW.read_bytes()),
               inscription_read_aloud_refinement=ICE)
    doc['evidence'][str(failed)] = sha(failed.read_bytes())
    save(review, doc)
    formatting.update(manuscript_sha256=sha(review.read_bytes()), parent_contextual_proof=str(review))
    save(manuscript, formatting)
    prefs['records'][ICE]['bindings']['english'] = sha(revised.encode('utf-8'))
    prefs['records'][ICE]['line_phrases'] = ['what happens to the water level']
    save(preferences, prefs)


if __name__ == '__main__':
    import sys

    if sys.argv[1:] == ['--inscription']:
        refine_inscription()
    else:
        main()
