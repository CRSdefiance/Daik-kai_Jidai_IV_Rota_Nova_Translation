"""Seal Rafael B221–B240 contextual decisions before fresh display checks."""
from copy import deepcopy
from pathlib import Path
import re

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load, save
from scripts.seal_rafael_B226_B240_clean_parts_v1 import clean_keys
from scripts.write_rafael_B177_B180_contextual_v1 import GATES, MACROS

ROOT = Path('work/analysis/Rafael_B221_B240_current2952_20261106')
DRAFTS = Path('work/analysis/Rafael_B221_B240_clean_20261106/sealed_all_clean_first_v1/sealed_drafts.json')
DECISIONS = [Path(f'translations/rafael_{part}_contextual_decisions_v1.txt') for part in
             ('B221_B225', 'B226_B230', 'B231_B235', 'B236_B240')]
OUT = Path('translations/rafael_B221_B240_contextual_review_v1.json')
LABELS = Path('translations/rafael_B221_B240_scoped_names_review_v1.json')
BLOCKS = list(range(221, 241))
SIGNATURES = {(221, '33'): 'Yukihisa Genjo Shiraki', (226, '68'): 'Janus Pasar', (235, '48'): 'Ian Dukov'}
FE = {'9': 'Swan calls', '17': 'Swan calls', '24': 'Wingbeats'}
GLYPH = 'DK4_MES_B227_R0019'
UNTRANSLATED = 'DK4_MES_B224_R0072'
PUNCTUATION = 'DK4_MES_B225_R0029'
NAMES = {
    0: ('Rafael Castor', 'Keep the approved nameplate and the FI form of address in the swan and Solomon scenes.'),
    4: ('Janus Pasar', 'Keep the approved spelling in his public name and Judas letter signature.'),
    5: ('Claudio Manaus', 'Keep the public name in the comments on the swans.'),
    7: ('Cristina Erneco', 'Keep the approved Cristina spelling in the swan exchange.'),
    8: ('Arcadius Eudoxios', 'Keep the short public form for the crewman considering the Crusades account.'),
    11: ('Jam Ludwyan', 'Keep the short public form for the man puzzling over Yukihisa’s letter.'),
    12: ('Yukihisa Shiraki', 'Keep the short public form and the complete signed name with Genjo.'),
    13: ('Cesare Tony', 'Keep his public name in the Timur discussion and his exchange with Yifa.'),
    16: ('Gerhard Adernkatz', 'Keep his established full name in the Noritsune exchange.'),
    17: ('Al Shin', 'Keep the short public name in his exchange with Julian and preserve the full catalogue form.'),
    21: ('Ian Dukov', 'Keep the public name and use the same full form in his letter signature.'),
    22: ('Samwell Khan', 'Keep the public name for the armadillo storyteller and his separate full catalogue form.'),
    23: ('Manuel Almeida', 'Keep the public name in the mock battle where he tells the children about Attila.'),
    25: ('Yifa Sol', 'Keep her approved public name in the Taoist training account.'),
    26: ('Julian Lopes', 'Keep his public name across the two distinct jewelry and armor exchanges.'),
    82: ('Shopkeeper', 'Keep the source occupation for the square shop conversation without assigning a personal name.'),
    85: ('Shopkeeper', 'Keep the separate shop actor and the source occupation in the Solomon exchange.'),
    92: ('Barkeep', 'Keep the occupation for the person who doubts the Avalon account.'),
    120: ('Guard', 'Keep the source role for the man questioning the reader and for the local eyewitness; no rank is specified.'),
    149: ('Guildmaster', 'Keep the source office for the guild discussion without inventing a personal name.'),
    151: ('Sailor', 'Keep the original Sailor plate for the direct actor and the startup role fallback, with Retainer in the catalogue.'),
    162: ('Boy', 'Keep the clean boy selector for the first child in the staged battle.'),
    169: ('Alluring Woman', 'Keep the recurring descriptive plate; Vivian introduces herself in her own dialogue.'),
    170: ('Mysterious Old Man', 'Keep the source role while letting the elder explain his family connection in dialogue.'),
    197: ('Safia', 'Keep her established public name and the personal greeting she gives Julian.'),
    199: ('Lucia', 'Keep her established public name and the personal greeting she gives Julian.'),
}
FULL = {8: 'Arcadius Eirene Eudoxios', 11: 'Jam Jack Ludwyan', 12: 'Yukihisa Genjo Shiraki',
        17: 'Al Ferid Shin', 22: 'Samwell da Khan', 151: 'Retainer'}


def digest(path):
    return sha(path.read_bytes())


def read_decisions():
    decisions = {}
    for path in DECISIONS:
        block = None
        for line in path.read_text(encoding='utf-8').splitlines():
            if not line or line.startswith('#'):
                continue
            if line.isdigit():
                block = int(line)
                assert block in BLOCKS
                continue
            key, replacement, finding = (part.strip() for part in line.split('|', 2))
            assert block is not None and (block, key) not in decisions and replacement and finding
            decisions[block, key] = replacement, finding
    return decisions


def review_record(draft, current, decisions, styles):
    ident = draft['id']
    assert all(draft[k] == current[k] for k in ('file_path', 'block', 'source_reference', 'source_hex')), ident
    block, key = draft['block'], clean_keys(draft)
    raw = bytes.fromhex(draft['source_hex'])
    selector = draft.get('source_selector')
    row = {**draft, **{k: v for k, v in current.items()
                       if k.startswith('current_') or k == 'selected_native_pointer'}}
    if key.startswith('V'):
        role = styles[ident]
        assert role['source_reference'] == draft['source_reference'] and selector == role['source_selector'] == 208
        assert draft['source_header_hex'] == current['source_header_hex'] == role['source_header_hex']
        assert draft['source_style_indices'] == current['current_style_indices'] == role['source_style_indices']
        assert role['virtual_prefix_not_in_stored_body']
        body, kind, speaker = raw, 'progressive', 'Runtime-selected crew voice'
        row.update(native_object_kind=role['kind'], native_role_source_binding=role,
                   source_record_index=draft['source_reference']['physical_record_index'],
                   native_style_dispatch_andall_five_review_gates_pending=False)
    elif key.startswith('C'):
        assert draft['source_word'] == current['source_word'] in (0x2100, 0x2200)
        assert all(draft[k] == current[k] for k in ('source_choice_object_hex', 'source_command_offset', 'source_count'))
        body, kind, speaker = raw, 'typed-choice-label', 'Player choice'
    else:
        assert raw[0] == selector == current['source_selector']
        assert draft['source_complete_preamble_hex'] == current['source_complete_preamble_hex']
        body = raw[1:]
        row['source_record_index'] = int(key)
        if selector == 254:
            assert block == 223
            kind, speaker = 'system-FE', FE[key]
            row.update(source_FE_presentation_kind=speaker, FE_is_not_an_ordinary_actor_nameplate=True,
                       native_FE_presentation_binding_pending=True)
        else:
            kind, speaker = 'progressive', NAMES[selector][0]

    replacement, finding = decisions.pop((block, key))
    previous = current['current_comparison_paragraph'].strip()
    retained = replacement == '='
    english = previous if retained else draft['independent_English'] if replacement == '*' else replacement
    assert previous and english and (english == previous) == retained, (ident, previous, english)
    assert not any(char in english for char in '{}%\n\r\t'), ident
    tokens = [token.decode() for token in MACROS.findall(body)]
    assert tokens == re.findall(r'\bF[AIOU]\b', english), (ident, tokens, english)
    non_ascii = {char for char in english if not char.isascii()}
    assert not non_ascii or (retained and non_ascii == {'…'}), ident
    row.update(english=english, decision='retention' if retained else 'revision', finding=finding,
               localization_note=finding, speaker=speaker, kind=kind, native_literal_tokens=tokens,
               native_literal_token_counts={token: tokens.count(token) for token in dict.fromkeys(tokens)},
               current_English_comparison_pending=False, current_ROM_English_unconsulted=False,
               earlier_English_unconsulted=False, approved_names_terms_titles_andruntime_substitutions_pending=False,
               all_five_review_gates_pending=False, fresh_formatting_binding_pending=True,
               registered_release_and_completion_credit_pending=True,
               review={gate: gate != 'formatting' for gate in GATES}, new_credit=0)
    if retained:
        row['retention_reason'] = finding
    if non_ascii:
        row['deliberate_source_punctuation_retention'] = True
    if ident == GLYPH:
        assert previous.count('Ｉ') == 2 and previous.replace('Ｉ', 'I') == english
        row.update(current_unintended_glyphs=['U+FF29 Ｉ'], glyph_only_revision_with_wording_retained=True)
    if ident == UNTRANSLATED:
        assert any('\u3040' <= char <= '\u9fff' for char in previous) and not retained
        row['current_effective_Japanese_requires_localization'] = True
    if ident == PUNCTUATION:
        assert '？' in previous and not retained
        row['current_fullwidth_punctuation_consistency_revision'] = True
    if (block, key) in SIGNATURES:
        signature = SIGNATURES[block, key]
        assert kind == 'progressive' and english.endswith(' ' + signature)
        source_signature = draft['source_Japanese'].splitlines()[-1]
        assert source_signature.startswith('\u3000')
        row.update(source_signature_presentation_pending=True, source_letter_signature_separate_native_row=True,
                   source_signature_row=source_signature, localized_signature=signature,
                   localized_letter_close=english.removesuffix(' ' + signature))
    if (block, key) == (223, '17'):
        assert len(draft['source_Japanese'].splitlines()) == 3
        row['source_staged_effect_rows_pending'] = draft['source_Japanese'].splitlines()
    return row


def name_rows(identity):
    assert set(NAMES) == {row['actor_ID'] for row in identity['name_bindings']}
    records = []
    for binding in identity['name_bindings']:
        actor = binding['actor_ID']
        label, reason = NAMES[actor]
        forms = {form['consumer']: form for form in binding['current_consumers']}
        assert forms['progressive-nameplate']['text'] == label
        assert forms['full-catalogue']['text'] == FULL.get(actor, label)
        fields = [field['source'] for field in binding['source_andcurrent_fields']]
        records.append(dict(id=f'ACTOR{actor}_RAFAEL221_240_NAME', actor_ID=actor, kind='progressive-nameplate',
            english=label, speaker=label, source_meaning=fields[0]['text'],
            context='Public name or role in Rafael SC0 B221–B240.',
            decision='retention', retention_reason=reason, finding=reason, localization_note=reason,
            source_reference=dict(actor_ID=actor, fields=fields),
            current_reference=dict(actor_ID=actor, consumer='progressive-nameplate',
                                   text_hex=forms['progressive-nameplate']['text_hex']),
            current_consumers=binding['current_consumers'], fresh_getter=binding['fresh'],
            exact_dependency_reuse_reference=binding['exact_dependency_reuse_reference'],
            review={gate: gate != 'formatting' for gate in GATES}, new_credit=0))
    return records


def main():
    assert not OUT.exists() and not LABELS.exists()
    inputs = [DRAFTS, *(ROOT / name for name in ('current_effective.json', 'objects/current_objects.json',
               'names_and_terms_v1.json', 'roles.json', 'item_title_bindings_v1.json'))]
    drafts, current, objects, identity, roles, items = map(load, inputs)
    runtime = current['runtime']
    assert all(value['runtime'] == runtime for value in (objects, identity, roles, items))
    assert drafts['complete_blocks'] == [group['block'] for group in current['groups']] == BLOCKS
    ordinary = [row for group in current['groups'] for row in group['records']]
    assert (len(ordinary), len(objects['style_records']), len(objects['choice_records'])) == (234, 29, 7)
    assert sum(len(row['source_style_indices']) for row in objects['style_records']) == 32
    bound = {row['id']: row for row in ordinary + objects['style_records'] + objects['choice_records']}
    assert set(bound) == {row['id'] for row in drafts['records']} and len(bound) == 270
    styles = {row['id']: row for row in roles['source_records']}
    assert set(styles) == {row['id'] for row in objects['style_records']}
    assert [(row['source_selector'], row['resolved_actor_ID'], row['source_voice_class'])
            for row in roles['native_roles']['rows']] == [(207, 0, 2), (208, 151, 4)]
    decisions = read_decisions()
    records = [review_record(row, bound[row['id']], decisions, styles) for row in drafts['records']]
    assert not decisions and len(records) == 270
    by_id = {row['id']: row for row in records}
    assert [row['id'] for row in records if row.get('current_unintended_glyphs')] == [GLYPH]
    assert [row['id'] for row in records if row.get('deliberate_source_punctuation_retention')] == [
        'DK4_MES_B234_R0005', 'DK4_MES_B236_R0011']
    assert [row['id'] for row in records if row['kind'] == 'system-FE'] == [
        'DK4_MES_B223_R0009', 'DK4_MES_B223_R0017', 'DK4_MES_B223_R0024']
    assert [row['native_literal_tokens'] for row in records if row['native_literal_tokens']] == [
        ['FI'], ['FA'], ['FI', 'FA'], ['FA'], ['FO']]
    for item in items['items']:
        for ident in item['scoped_dialogue_ids']:
            row = by_id[ident]
            assert item['current']['text'] in row['english'], (ident, item['current']['text'], row['english'])
            row['approved_item_binding'] = item
    evidence = {str(path): digest(path) for path in [*inputs, *DECISIONS, Path(__file__)]}
    doc = dict(format='dk4-contextual-dialogue-review-v2', translation_policy='natural-dialogue-v2',
        target_locale='en-US', encoder='dialogue-relocatable-v1', review_gates=GATES, file_path='/data/SC0.DK4',
        blocks=BLOCKS, records=records, source_objects=270, ordinary_speech_objects=234,
        physical_style_alternatives=29, style_objects=4, native_style_slots=32,
        typed_choice_objects=7, typed_choice_commands=3, control_only_blocks=[231],
        **{k: current[k] for k in ('current_ROM', 'current_ROM_sha256', 'current_archive_sha256', 'runtime')},
        proposed_revisions=sum(row['decision'] == 'revision' for row in records),
        justified_retentions=sum(row['decision'] == 'retention' for row in records),
        current_glyph_defect_records=[GLYPH], punctuation_consistency_revisions=[PUNCTUATION],
        untranslated_current_records=[UNTRANSLATED], native_macro_tokens_still_require_formatter_marking=True,
        all_individual_four_prose_gates_pass=True, all_fifth_formatting_gates_pending=True, new_credit=0,
        evidence=evidence)
    projected = deepcopy(doc)
    projected['translation_policy'] = 'natural-dialogue-v1'
    validate_natural_dialogue_batch(projected)
    try:
        validate_natural_dialogue_batch(doc)
    except ValueError as error:
        assert 'requires per-record source, context, localization, naturalness, and formatting review' in str(error)
    else:
        raise AssertionError('Unformatted manuscript unexpectedly passed the release gate')
    labels = name_rows(identity)
    save(LABELS, dict(format='dk4-scoped-name-contextual-review-v2', translation_policy='natural-dialogue-v2',
        target_locale='en-US', encoder='dialogue-relocatable-v1', review_gates=GATES, records=labels,
        runtime=runtime, all_name_formatting_gates_pending=True, no_global_name_table_changes=True,
        new_credit=0, evidence=evidence))
    doc['evidence'][str(LABELS)] = digest(LABELS)
    save(OUT, doc)
    print(f"270 contextual decisions: {doc['proposed_revisions']} revisions, {doc['justified_retentions']} retentions, "
          f"{len(labels)} scoped names. Formatting remains pending.")


if __name__ == '__main__':
    main()

