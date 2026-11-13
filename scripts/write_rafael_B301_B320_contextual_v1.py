"""Seal all Rafael B301–B320 decisions against the exact registered predecessor."""
from copy import deepcopy
from pathlib import Path
from struct import unpack_from

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.rom.nds import NdsImage
from scripts.audit_story_glyph_consistency import load, save
from scripts.checkpoint_rafael_B301_B320_contextual_v1 import (
    CURRENT, DECISIONS, DRAFT, GATES, NAME_REVIEW, NAMES, OBJECTS, PARTIAL, RELEASE,
    ROLES, ROOT, env, read_decisions,
)
from scripts.seal_rafael_B301_B320_clean_v1 import BLOCKS, digest


OUT = Path('translations/rafael_B301_B320_contextual_review_v1.json')
TERMS = ROOT / 'scoped_catalogue_terms_v1.json'
ITEMS = Path('translations/all_item_names_arm9_v1.json')
FURTHER_DECISIONS = [Path(f'translations/rafael_B{start}_B{start+4}_contextual_decisions_v1.txt')
                     for start in (311, 316)]
TONIC = 'DK4_MES_B307_R0025'


def catalogue(release):
    clean, current = Path('work/clean.nds'), Path(release['candidate'])
    assert digest(clean) == release['clean_input_sha256'] and digest(current) == release['candidate_sha256']
    images = [NdsImage.open(path).read_file('/__arm9__.bin') for path in (clean, current)]
    fields = {row['id']: row for row in load(ITEMS)['records']}
    terms = []
    for item, source, english in (
        (23, '華陀の漢方薬', "Hua Tuo's Tonic"),
        (79, '千夜一夜物語', 'Arabian Nights'),
        (151, 'リグ＝ヴェーダ', 'Rigveda'),
    ):
        field = fields[f'DK4_ITEM_POINTER_{item:03d}']
        assert field['english'] == english
        at = field['offset']
        sources = {}
        for arm, key, expected in zip(images, ('clean', 'current'), (source, english), strict=True):
            pointer, = unpack_from('<I', arm, at)
            offset = pointer - 0x02000000
            raw = arm[offset:arm.index(0, offset)]
            assert raw.decode('cp932') == expected
            sources[key] = dict(pointer=pointer, offset=offset, hex=raw.hex(), text=expected)
        terms.append(dict(item=item, pointer_field_offset=at, file_path='/__arm9__.bin', **sources))
    return dict(terms=terms, clean_ROM=str(clean), clean_ROM_sha256=release['clean_input_sha256'],
                current_ROM=str(current), current_ROM_sha256=release['candidate_sha256'],
                story_activation_not_inferred_from_item_table=True, new_credit=0,
                evidence={str(path): digest(path) for path in (RELEASE, ITEMS, Path(__file__))})


def main():
    assert not OUT.exists() and not TERMS.exists()
    inputs = (DRAFT, CURRENT, OBJECTS, NAMES, ROLES, RELEASE, PARTIAL, NAME_REVIEW)
    draft, current, objects, identity, role_report, release, partial, names_doc = map(load, inputs)
    runtime = current['runtime']
    assert all(value['runtime'] == runtime for value in (objects, identity, role_report, partial, names_doc))
    assert runtime['candidate_sha256'] == release['candidate_sha256'] == current['current_ROM_sha256']
    assert digest(RELEASE) == runtime['release_proof_sha256']
    assert all(digest(path) == checksum for path, checksum in partial['evidence'].items())
    source = draft['records']
    ordinary = [row for group in current['groups'] for row in group['records']]
    styles, choices = objects['style_records'], objects['choice_records']
    assert (len(ordinary), len(styles), len(choices), objects['native_style_getter_cases']) == (297, 145, 11, 152)
    bound = {row['id']: row for row in ordinary + styles + choices}
    assert bound.keys() == {row['id'] for row in source} and len(bound) == 453
    names = {row['actor_ID']: row for row in names_doc['records']}
    roles = {row['source_selector']: row for row in role_report['native_roles']['rows']}
    style_roles = {row['id']: row for row in role_report['source_records'] if '_STYLE_' in row['id']}
    assert len(names) == 19 and style_roles.keys() == {row['id'] for row in styles}
    decisions = read_decisions([*DECISIONS, *FURTHER_DECISIONS])
    assert decisions.keys() == bound.keys()
    terms = catalogue(release)
    tonic, book, veda = terms['terms']
    decisions[TONIC] = (
        "Hua Tuo's Tonic must be what he was talking about. I've got to get it to the Istanbul guild right away.",
        "Use the exact current item label for the same clean Japanese item and restore Istanbul as the destination.",
    )
    rows = [env['review_record'](row, bound[row['id']], decisions[row['id']], names, roles, style_roles) for row in source]
    exact_reused = []
    for old, new in zip(partial['records'], rows[:229], strict=True):
        assert old['id'] == new['id']
        if old['id'] != TONIC:
            assert old == new
            exact_reused.append(old['id'])
    by_id = {row['id']: row for row in rows}
    assert tonic['clean']['text'] in by_id[TONIC]['source_Japanese']
    by_id[TONIC]['catalogue_term_binding'] = tonic
    for ident in ('DK4_MES_B317_R0079', 'DK4_MES_B317_R0083', 'DK4_MES_B317_R0100', 'DK4_MES_B318_R0101'):
        assert book['current']['text'] in by_id[ident]['english']
        by_id[ident]['catalogue_term_binding'] = book
    assert veda['clean']['text'].endswith('ヴェーダ')
    assert "the first Veda" in by_id['DK4_MES_B304_R0017']['english']
    assert len([row for row in rows if row['native_literal_tokens'] == ['FI']]) == 10
    assert sum(row['kind'] == 'system-FE' for row in rows) == 16
    assert all(row['review'] == {gate: gate != 'formatting' for gate in GATES} for row in rows)
    save(TERMS, terms)
    revisions = sum(row['decision'] == 'revision' for row in rows)
    evidence = {str(path): digest(path) for path in (*inputs, TERMS, *DECISIONS, *FURTHER_DECISIONS, Path(__file__))}
    doc = dict(translation_policy='natural-dialogue-v2', target_locale='en-US', encoder='dialogue-relocatable-v1',
        review_gates=GATES, format='dk4-contextual-dialogue-review-v2', file_path='/data/SC0.DK4',
        blocks=BLOCKS, records=rows, runtime=runtime, source_objects=453, ordinary_speech_objects=297,
        physical_style_alternatives=145, style_objects=19, native_style_slots=152, typed_choice_objects=11,
        typed_choice_commands=5, control_only_blocks=[], proposed_revisions=revisions,
        justified_retentions=len(rows)-revisions, exact_first_checkpoint_records_reused=len(exact_reused),
        later_item_catalogue_refinement=TONIC, entire_intake_non_ASCII_findings=partial['entire_intake_non_ASCII_findings'],
        scoped_name_review=str(NAME_REVIEW), scoped_name_review_sha256=digest(NAME_REVIEW),
        native_macro_tokens_still_require_formatter_marking=True, all_individual_four_prose_gates_pass=True,
        all_fifth_formatting_gates_pending=True, evidence=evidence, new_credit=0,
        **{key: current[key] for key in ('current_ROM', 'current_ROM_sha256', 'current_archive_sha256')})
    projected = deepcopy(doc)
    projected['translation_policy'] = 'natural-dialogue-v1'
    validate_natural_dialogue_batch(projected)
    try:
        validate_natural_dialogue_batch(doc)
    except ValueError as error:
        assert 'requires per-record source, context, localization, naturalness, and formatting review' in str(error)
    else:
        raise AssertionError('The unformatted manuscript passed a release gate')
    save(OUT, doc)
    print(f"453 contextual decisions, {revisions} revisions and {len(rows)-revisions} retentions. Formatting remains pending.")


if __name__ == '__main__':
    main()
