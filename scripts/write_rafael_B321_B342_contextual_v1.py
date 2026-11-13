"""Bind all final-SC0 editorial decisions to their exact clean and current records."""
from copy import deepcopy
from pathlib import Path

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from scripts.audit_story_glyph_consistency import load, save
from scripts import checkpoint_rafael_B321_B331_contextual_v1 as partial
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.seal_rafael_B321_B342_clean_v1 import BLOCKS, ROOT


OUT = Path('translations/rafael_B321_B342_contextual_review_v1.json')
DECISIONS = [partial.DECISIONS, *(Path(f'translations/rafael_{part}_contextual_decisions_v1.txt') for part in (
    'B324_B325', 'B327_B329', 'B332', 'B333_B334', 'B335_B342'))]
FE = {
    325: {188: 'System captain injury notice', 300: 'System fatigue notice'},
    327: {86: 'Bat screech', 113: 'System elapsed-time notice', 181: 'System fatigue notice'},
    329: {212: 'System captain injury and one-day treatment notice', 290: 'Dropped baggage sound',
          353: 'System apparent sailor injury notice'},
    332: {172: 'System apparent sailor injury and accumulating fatigue notice',
          185: 'System elapsed-time notice', 320: 'System fatigue notice',
          383: 'First waiting panel', 387: 'Longer waiting panel', 394: 'System elapsed-time notice'},
    333: {198: 'System fatigue notice'}, 334: {77: 'System elapsed-time notice'},
    337: {36: 'System knife handover notice', 95: 'System one-point Agility increase notice'},
    338: {106: 'System one-point Agility increase notice'}, 340: {14: 'System sextant handover notice'},
}


def main():
    assert not OUT.exists()
    draft, current, objects, identity, role_report = map(load, partial.INPUTS)
    reviewed = load(partial.OUT)
    labels, terms = map(load, (partial.LABELS, partial.TERMS))
    runtime = current['runtime']
    assert all(report['runtime'] == runtime for report in (objects, identity, role_report, reviewed, labels, terms))
    for doc in (draft, reviewed, labels):
        assert all(digest(path) == checksum for path, checksum in doc['evidence'].items())
    bound = {row['id']: row for row in [*(row for group in current['groups'] for row in group['records']),
                                       *objects['style_records'], *objects['choice_records']]}
    assert len(bound) == 556 and bound.keys() == {row['id'] for row in draft['records']}
    decisions = partial.read_decisions(DECISIONS)
    assert decisions.keys() == bound.keys()
    earlier = {row['id']: row for row in reviewed['records']}
    assert len(earlier) == 65
    roles = {row['source_selector']: row for row in role_report['native_roles']['rows']}
    style_roles = {row['id']: row for row in role_report['source_records'] if '_STYLE_' in row['id']}
    names = {row['actor_ID']: row for row in labels['records']}
    review_record = partial.namespace['review_record']
    review_record.__globals__['FE'] = FE
    rows = []
    for source in draft['records']:
        ident = source['id']
        if ident in earlier:
            row = deepcopy(earlier[ident])
            assert row['source_reference'] == source['source_reference']
            assert row['current_reference'] == bound[ident]['current_reference']
        else:
            row = review_record(source, bound[ident], decisions[ident], names, roles, style_roles)
        if row['block'] == 325:
            row['context'] = (
                'A map warning precedes the wolf encounter. The crew can scare the animals off, fight or flee. '
                'Rafael is hurt while shooing them. In the fight, his hand slips and a crewmate is hurt. '
                'The crew reassures him after the animals flee. In the retreat branch they leave the group alone. '
                'The source leaves wolf number unstated; retain the existing plural English consistently.'
            )
        if row['block'] in (336, 337, 338):
            row['context'] = row['context'].replace("Tlaloc's Knife", 'the Tlaloc Knife')
        rows.append(row)
    assert len(rows) == 556 and len({row['id'] for row in rows}) == 556
    for ident, row in earlier.items():
        assert next(new for new in rows if new['id'] == ident) == row
    assert sum(row['kind'] == 'system-FE' for row in rows) == 20
    assert sum(row['kind'] == 'typed-choice-label' for row in rows) == 16
    assert all(row['review'] == {gate: gate != 'formatting' for gate in partial.namespace['GATES']} for row in rows)
    non_ascii = [dict(id=row['id'], current=row['current_comparison_paragraph'], english=row['english'])
                 for row in rows if not row['current_comparison_paragraph'].isascii()]
    assert len(non_ascii) == 10 and all(row['english'].isascii() for row in non_ascii)
    by_id = {row['id']: row for row in rows}
    for term in terms['terms']:
        for row in rows:
            if term['clean']['text'] in row['source_Japanese']:
                row.setdefault('catalogue_term_bindings', []).append(term)
    # Earlier reviewed rows remain byte-for-byte reusable. Catalogue evidence was
    # already recorded for those rows in their original checkpoint.
    for ident, row in earlier.items():
        if 'catalogue_term_bindings' in by_id[ident]:
            del by_id[ident]['catalogue_term_bindings']
        assert by_id[ident] == row
    revisions = sum(row['decision'] == 'revision' for row in rows)
    evidence = {str(path): digest(path) for path in (*partial.INPUTS, partial.OUT, partial.LABELS,
                partial.TERMS, partial.RELEASE, *DECISIONS, Path(__file__))}
    doc = dict(format='dk4-contextual-dialogue-review-v2', translation_policy='natural-dialogue-v2',
               target_locale='en-US', encoder='dialogue-relocatable-v1',
               review_gates=partial.namespace['GATES'], file_path='/data/SC0.DK4', blocks=BLOCKS,
               records=rows, runtime=runtime, source_objects=556, ordinary_speech_objects=242,
               physical_style_alternatives=298, style_objects=48, native_style_slots=384,
               typed_choice_objects=16, typed_choice_commands=7, label_free_controls=1,
               proposed_revisions=revisions, justified_retentions=556-revisions,
               exact_first_checkpoint_records_reused=65, entire_intake_non_ASCII_findings=non_ascii,
               scoped_name_review=str(partial.LABELS), scoped_name_review_sha256=digest(partial.LABELS),
               native_macro_tokens_still_require_formatter_marking=True,
               all_individual_four_prose_gates_pass=True, all_fifth_formatting_gates_pending=True,
               evidence=evidence, new_credit=0,
               **{key: current[key] for key in ('current_ROM', 'current_ROM_sha256', 'current_archive_sha256')})
    projected = deepcopy(doc)
    projected['translation_policy'] = 'natural-dialogue-v1'
    validate_natural_dialogue_batch(projected)
    try:
        validate_natural_dialogue_batch(doc)
    except ValueError as error:
        assert 'requires per-record source, context, localization, naturalness, and formatting review' in str(error)
    else:
        raise AssertionError('An unformatted record passed the release gate')
    save(OUT, doc)
    print(f'556 contextual decisions, {revisions} revisions and {556-revisions} retentions. Fresh display checks remain.')


if __name__ == '__main__':
    main()
