"""Bind Rafael B261–B280 editorial decisions to clean and registered ROM records."""
from copy import deepcopy
from pathlib import Path
import re

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load, save
from scripts.write_rafael_B177_B180_contextual_v1 import GATES, MACROS


ROOT = Path('work/Rafael_B261_B280_clean_20261106')
INPUTS = [ROOT / name for name in (
    'sealed_clean_first_v1/sealed_drafts.json', 'current_v1/current_effective.json',
    'objects_v1/current_objects.json', 'names_and_terms_v1.json', 'roles.json')]
DECISIONS = Path('translations/rafael_B261_B280_contextual_decisions_v1.txt')
OUT = Path('translations/rafael_B261_B280_contextual_review_v1.json')
LABELS = Path('translations/rafael_B261_B280_scoped_names_review_v1.json')
BLOCKS = list(range(261, 281))
PUNCTUATION = 'DK4_MES_B261_R0125'
UNTRANSLATED = {f'DK4_MES_B270_R{index:04d}' for index in (8, 15, 31)}
FE = {
    261: {
        9: 'Wall inscription', 12: 'Wall inscription', 140: 'Cracking sound',
        148: 'Figurehead voice', 155: 'Figurehead voice', 170: 'Figurehead voice',
        178: 'Figurehead voice', 195: 'Figurehead voice', 206: 'Figurehead cry',
    },
    267: {18: 'System gold receipt', 48: 'System share notice'},
    271: {15: 'System gold receipt', 45: 'System share notice'},
    276: {16: 'System gold receipt', 47: 'System share notice'},
    278: {16: 'System gold receipt', 47: 'System share notice'},
}
NAME_REVISIONS = {
    65: ('Plett Perot', 'Plett Perrault',
         'Match the established bounty spelling. Confirm ownership and capacity before changing the surname field.'),
    68: ('Jacob ポルトゥント', 'Jacob Portunto',
         'Localize the still-Japanese surname using the established quest spelling in B269 R0014.'),
}


def read_decisions():
    decisions = {}
    block = None
    for line in DECISIONS.read_text(encoding='utf-8').splitlines():
        if not line or line.startswith('#'):
            continue
        if line.isdigit():
            block = int(line)
            assert block in BLOCKS
            continue
        key, replacement, finding = (field.strip() for field in line.split('|', 2))
        ident = f'DK4_MES_B{block}_R{int(key):04d}' if key.isdigit() else key
        assert block is not None and ident not in decisions and replacement and finding
        assert f'B{block}_' in ident
        decisions[ident] = replacement, finding
    return decisions


def name_review(binding):
    actor = binding['actor_ID']
    current = {row['consumer']: row['text'] for row in binding['current_consumers']}
    assert set(current) == {'progressive-nameplate', 'full-catalogue'}
    if actor in NAME_REVISIONS:
        old, target, finding = NAME_REVISIONS[actor]
        assert set(current.values()) == {old}
        approved = dict.fromkeys(current, target)
    else:
        approved = current
        if actor in range(151, 155):
            assert list(current.values()) == ['Sailor', 'Retainer']
            finding = 'Keep Sailor in dialogue and Retainer in the catalogue as distinct source roles.'
        elif actor in (113, 147, 148, 149):
            finding = f"Keep the established occupational label {current['progressive-nameplate']}."
        else:
            finding = f"Keep the established spelling {current['progressive-nameplate']} in both consumers."
    retained = approved == current
    return dict(
        **binding, id=f'RAFAEL261_280_NAME_{actor}', current_forms=current, approved_forms=approved,
        decision='retention' if retained else 'revision', finding=finding,
        **({'retention_reason': finding} if retained else {}),
        review={gate: gate != 'formatting' for gate in GATES}, new_credit=0,
    )


def review_record(draft, current, decision, names, roles, style_roles):
    ident = draft['id']
    assert all(draft[key] == current[key] for key in (
        'file_path', 'block', 'source_reference', 'source_hex', 'source_Japanese',
    )), ident
    block = draft['block']
    body = bytes.fromhex(draft['source_hex'])
    row = {
        **draft, **{key: value for key, value in current.items()
                    if key.startswith('current_') or key == 'selected_native_pointer'},
    }
    if ident in style_roles:
        binding = style_roles[ident]
        assert binding['source_reference'] == draft['source_reference']
        assert draft['source_selector'] == binding['source_selector'] == 208
        assert draft['source_header_hex'] == binding['source_header_hex'] == current['source_header_hex']
        assert draft['source_style_indices'] == binding['source_style_indices'] == current['current_style_indices']
        assert binding['virtual_prefix_not_in_stored_body']
        kind, speaker = 'progressive', 'Runtime-selected crew voice'
        row.update(
            native_object_kind=binding['kind'], native_role_source_binding=binding,
            source_record_index=draft['source_reference']['physical_record_index'],
            native_style_dispatch_andall_five_review_gates_pending=False,
        )
    elif '_CHOICE_' in ident:
        assert draft['source_word'] == current['source_word'] in (0x2100, 0x2200)
        assert all(draft[key] == current[key] for key in (
            'source_choice_object_hex', 'source_command_offset', 'source_count',
        ))
        kind, speaker = 'typed-choice-label', 'Player choice'
    else:
        selector = draft['source_selector']
        preamble = bytes.fromhex(draft['source_complete_preamble_hex'])
        assert preamble[:5] == bytes.fromhex('0040ffff00')
        assert len(preamble) == 6 and preamble[-1] == body[0] == selector == current['source_selector']
        assert draft['source_complete_preamble_hex'] == current['source_complete_preamble_hex']
        # The extractor includes only the selector in source_hex, and records the command separately.
        body = body[1:]
        index = row['source_record_index'] = draft['source_reference']['record_index']
        if selector == 254:
            kind, speaker = 'system-FE', FE[block][index]
            row.update(
                source_FE_presentation_kind=speaker, FE_is_not_an_ordinary_actor_nameplate=True,
                native_FE_presentation_binding_pending=True,
            )
        else:
            kind = 'progressive'
            actor = roles[selector]['resolved_actor_ID'] if selector in roles else selector
            speaker = names[actor]['approved_forms']['progressive-nameplate']
            row['speaker_name_binding'] = names[actor]['id']
            if selector in roles:
                row['native_role_source_binding'] = roles[selector]

    replacement, finding = decision
    previous = current['current_comparison_paragraph'].strip()
    retained = replacement == '='
    english = previous if retained else draft['independent_English'] if replacement == '*' else replacement
    assert previous and english and (english == previous) == retained, (ident, previous, english)
    assert english.isascii() and not any(char in english for char in '{}%\n\r\t'), ident
    tokens = [token.decode() for token in MACROS.findall(body)]
    assert tokens == re.findall(r'\bF[AIOU]\b', english), (ident, tokens, english)
    assert all(draft.get('source_macros', {}).get(token, 0) == tokens.count(token) for token in ('FI', 'FA', 'FO'))
    row.update(
        english=english, decision='retention' if retained else 'revision', finding=finding,
        localization_note=finding, speaker=speaker, kind=kind, native_literal_tokens=tokens,
        native_literal_token_counts={token: tokens.count(token) for token in dict.fromkeys(tokens)},
        current_English_comparison_pending=False, current_ROM_English_unconsulted=False,
        earlier_English_unconsulted=False, all_five_review_gates_pending=False,
        fresh_formatting_binding_pending=True, registered_release_and_completion_credit_pending=True,
        review={gate: gate != 'formatting' for gate in GATES}, new_credit=0,
    )
    if retained:
        row['retention_reason'] = finding
    if ident == PUNCTUATION:
        assert previous == '！？' and english == '?!'
        row['current_fullwidth_punctuation_consistency_revision'] = True
    if ident in UNTRANSLATED:
        assert any('\u3040' <= char <= '\u9fff' for char in previous) and not retained
        row['current_effective_Japanese_requires_localization'] = True
    return row


def main():
    assert not OUT.exists() and not LABELS.exists()
    draft, current, objects, identity, role_report = map(load, INPUTS)
    runtime = current['runtime']
    assert all(value['runtime'] == runtime for value in (objects, identity, role_report))
    assert draft['complete_blocks'] == [group['block'] for group in current['groups']] == BLOCKS
    ordinary = [record for group in current['groups'] for record in group['records']]
    styles, choices = objects['style_records'], objects['choice_records']
    assert (len(ordinary), len(styles), len(choices)) == (114, 16, 5)
    assert sum(len(record['source_style_indices']) for record in styles) == 16
    bound = {record['id']: record for record in ordinary + styles + choices}
    decisions = read_decisions()
    assert set(bound) == set(decisions) == {record['id'] for record in draft['records']}
    assert len(bound) == 135
    roles = {row['source_selector']: row for row in role_report['native_roles']['rows']}
    assert [(role['resolved_actor_ID'], role['source_voice_class']) for role in roles.values()] == [(0, 2), (151, 4)]
    style_roles = {record['id']: record for record in role_report['source_records']
                   if record['id'] in bound and '_STYLE_' in record['id']}
    assert set(style_roles) == {record['id'] for record in styles}
    names = {binding['actor_ID']: name_review(binding) for binding in identity['name_bindings']}
    assert len(names) == 18
    records = [review_record(record, bound[record['id']], decisions[record['id']], names, roles, style_roles)
               for record in draft['records']]
    assert {(row['block'], row['source_record_index']) for row in records if row['kind'] == 'system-FE'} == {
        (block, index) for block, indices in FE.items() for index in indices
    }
    assert [row['id'] for row in records if row['native_literal_tokens']] == [
        'DK4_MES_B262_R0007', 'DK4_MES_B263_R0006', 'DK4_MES_B264_R0006',
    ]
    evidence = {path.as_posix(): sha(path.read_bytes()) for path in [*INPUTS, DECISIONS, Path(__file__).resolve().relative_to(Path.cwd())]}
    common = dict(
        translation_policy='natural-dialogue-v2', target_locale='en-US',
        encoder='dialogue-relocatable-v1', review_gates=GATES, runtime=runtime, new_credit=0,
    )
    doc = dict(
        **common, format='dk4-contextual-dialogue-review-v2', file_path='/data/SC0.DK4',
        blocks=BLOCKS, records=records, source_objects=135, ordinary_speech_objects=114,
        physical_style_alternatives=16, style_objects=2, native_style_slots=16,
        typed_choice_objects=5, typed_choice_commands=2, control_only_blocks=[],
        **{key: current[key] for key in ('current_ROM', 'current_ROM_sha256', 'current_archive_sha256')},
        proposed_revisions=sum(row['decision'] == 'revision' for row in records),
        justified_retentions=sum(row['decision'] == 'retention' for row in records),
        punctuation_consistency_revisions=[PUNCTUATION], untranslated_current_records=sorted(UNTRANSLATED),
        native_macro_tokens_still_require_formatter_marking=True,
        all_individual_four_prose_gates_pass=True, all_fifth_formatting_gates_pending=True,
        evidence=evidence,
    )
    draft_validation = deepcopy(doc)
    draft_validation['translation_policy'] = 'natural-dialogue-v1'
    validate_natural_dialogue_batch(draft_validation)
    try:
        validate_natural_dialogue_batch(doc)
    except ValueError as error:
        assert 'requires per-record source, context, localization, naturalness, and formatting review' in str(error)
    else:
        raise AssertionError('Unformatted manuscript unexpectedly passed the release gate')
    save(LABELS, dict(
        **common, format='dk4-scoped-name-contextual-review-v2', records=list(names.values()),
        all_name_formatting_gates_pending=True, scoped_name_field_corrections_pending=sorted(NAME_REVISIONS),
        evidence=evidence,
    ))
    evidence[LABELS.as_posix()] = sha(LABELS.read_bytes())
    save(OUT, doc)
    print(f"135 contextual decisions, {doc['proposed_revisions']} revisions and "
          f"{doc['justified_retentions']} retentions. {len(names)} scoped names. Formatting remains pending.")


if __name__ == '__main__':
    main()
