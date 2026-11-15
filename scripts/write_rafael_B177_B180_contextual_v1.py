"""Save source/current editorial decisions for complete Rafael B177–B180 exchanges."""
from copy import deepcopy
from pathlib import Path
import re

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load, save

A = Path('work/analysis')
DRAFTS = A / 'Rafael_B161_B180_clean_20261105/B177_B180_clean_first_v1/sealed_drafts.json'
CURRENT = A / 'Rafael_B177_B180_current1424_20261105/current_effective.json'
CAPTIONS = CURRENT.parent / 'objects/current_objects.json'
IDENTITY = CURRENT.with_name('names_and_terms_v1.json')
DECISIONS = Path('translations/rafael_B177_B180_contextual_decisions_v1.txt')
OUT = Path('translations/rafael_B177_B180_contextual_review_v1.json')
GATES = ['source', 'context', 'localization', 'naturalness', 'formatting']
CONTEXTS = {
    177: 'In Alexandria, Cesare recognizes the Elysion and asks to sail aboard without reclaiming his ship. Janus and Cesare discover shared enthusiasm for ship fittings while Rafael tries to keep up. The separate ship-buying lesson moves from small trading ventures to refits, distant routes and naval battles.',
    178: 'Fernando wagers a drink in a take-away coin game. Janus explains the losing last coin to Rafael while Clau bristles at being left behind. After a win, Rafael asks about Fernando’s insight, watches him read a couple’s breakup and invites him aboard. Fernando ties his decision to the coin toss.',
    179: 'Manuel treats the ship as a living thing. Janus sees value in his care for ships and asks him to join. Manuel accepts warmly, then offers practical flagship refitting advice. The optional lesson covers crew assignments and room effects without conflating them with the admiral’s command.',
    180: 'A bored shipwright offers an optional sailing lesson. The party can decline with confidence or hear his plainspoken explanation of sail orientation, auxiliary fittings and wind angle. Manuel reasons through the mast example. Keep the instructor’s teasing, informal voice distinct from his listeners.',
}
MACROS = re.compile(rb'F[AIOU]')
APPROVED_PUNCTUATION = set('…！？')


def read_decisions():
    block = None
    decisions = {}
    for line in DECISIONS.read_text(encoding='utf-8').splitlines():
        if not line or line.startswith('#'):
            continue
        if line.isdigit():
            block = int(line)
            assert block in CONTEXTS
            continue
        key, replacement, finding = line.split('|', maxsplit=2)
        assert block is not None and finding.strip()
        if key.startswith('C'):
            index = int(key[1:])
            lookup = (block, 'choice', index)
        else:
            lookup = (block, 'speech', int(key))
        assert lookup not in decisions
        decisions[lookup] = replacement.strip(), finding.strip()
    return decisions


def review_record(draft, current, names, decisions):
    ident = draft['id']
    assert all(draft[key] == current[key] for key in ('file_path', 'block', 'source_reference', 'source_hex')), ident
    block = draft['block']
    selector = draft.get('source_selector')
    raw = bytes.fromhex(draft['source_hex'])
    if selector is None:
        assert draft['source_word'] == current['source_word'] == 0x2100
        assert draft['source_choice_object_hex'] == current['source_choice_object_hex']
        lookup = (block, 'choice', draft['source_index'])
        body, kind, speaker = raw, 'typed-choice-label', 'Player choice'
    else:
        assert raw[0] == selector == current['source_selector']
        assert draft['source_complete_preamble_hex'] == current['source_complete_preamble_hex']
        lookup = (block, 'speech', draft['source_reference']['record_index'])
        body = raw[1:]
        kind = 'system-FE' if selector == 254 else 'progressive'
        speaker = 'System panel' if selector == 254 else names[selector]

    replacement, finding = decisions.pop(lookup)
    previous = current['current_comparison_paragraph'].strip()
    decision = 'retention' if replacement == '=' else 'revision'
    english = previous if decision == 'retention' else (draft['independent_English'] if replacement == '*' else replacement)
    assert previous and english and (english == previous) == (decision == 'retention'), ident
    assert not any(token in english for token in ('{', '}', '%', '\n', '\r', '\t')), ident
    tokens = [token.decode() for token in MACROS.findall(body)]
    assert tokens == re.findall(r'\bF[AIOU]\b', english), (ident, tokens, english)
    non_ascii = {char for char in english if not char.isascii()}
    assert not non_ascii or (decision == 'retention' and non_ascii <= APPROVED_PUNCTUATION), ident

    row = dict(draft)
    row.update({key: value for key, value in current.items() if key.startswith('current_') or key == 'selected_native_pointer'})
    row.update(english=english, decision=decision, finding=finding, localization_note=finding,
        speaker=speaker, kind=kind, context=CONTEXTS[block], native_literal_tokens=tokens,
        native_literal_token_counts={token: tokens.count(token) for token in dict.fromkeys(tokens)},
        current_English_comparison_pending=False, current_ROM_English_unconsulted=False,
        earlier_English_unconsulted=False, approved_names_terms_titles_andruntime_substitutions_pending=False,
        source_context_localization_formatting_gates_pending=False, all_five_review_gates_pending=False,
        fresh_formatting_binding_pending=True, registered_release_and_completion_credit_pending=True,
        review={gate: gate != 'formatting' for gate in GATES}, new_credit=0)
    if selector is not None:
        row['source_record_index'] = lookup[2]
    if decision == 'retention':
        row['retention_reason'] = finding
    if non_ascii:
        row['deliberate_source_punctuation_retention'] = True
    glyph_defects = sorted({char for char in previous if not char.isascii()} - APPROVED_PUNCTUATION)
    if glyph_defects:
        assert decision == 'revision'
        row['current_unintended_glyphs'] = [f'U+{ord(char):04X} {char}' for char in glyph_defects]
        row['glyph_only_revision_with_wording_retained'] = previous.replace('Ｉ', 'I').replace('Ｆ', 'F') == english
    return row


def main():
    assert not OUT.exists()
    drafts, effective, captions, identity = map(load, [DRAFTS, CURRENT, CAPTIONS, IDENTITY])
    current_rows = [row for group in effective['groups'] for row in group['records']] + captions['choice_records']
    current = {row['id']: row for row in current_rows}
    names = {row['actor_ID']: next(form['text'] for form in row['current_consumers']
        if form['consumer'] == 'progressive-nameplate') for row in identity['name_bindings']}
    assert len(current) == len(current_rows) == 183
    assert set(current) == {row['id'] for row in drafts['records']}
    assert identity['runtime'] == effective['runtime']
    decisions = read_decisions()
    rows = [review_record(draft, current[draft['id']], names, decisions) for draft in drafts['records']]
    assert not decisions
    rows.sort(key=lambda row: (row['block'], row['source_reference']['offset']))
    assert {block: sum(row['block'] == block for row in rows) for block in CONTEXTS} == {177: 56, 178: 65, 179: 33, 180: 29}
    assert sum(row['kind'] == 'typed-choice-label' for row in rows) == 8
    evidence = {str(path): sha(path.read_bytes()) for path in [DRAFTS, CURRENT, CAPTIONS, IDENTITY, DECISIONS, Path(__file__)]}
    document = dict(format='dk4-contextual-dialogue-review-v2', translation_policy='natural-dialogue-v2',
        target_locale='en-US', encoder='dialogue-relocatable-v1', review_gates=GATES,
        file_path='/data/SC0.DK4', blocks=sorted(CONTEXTS), records=rows, source_objects=len(rows),
        current_ROM=effective['current_ROM'], current_ROM_sha256=effective['current_ROM_sha256'],
        current_archive_sha256=effective['current_archive_sha256'], runtime=effective['runtime'],
        proposed_revisions=sum(row['decision'] == 'revision' for row in rows),
        justified_retentions=sum(row['decision'] == 'retention' for row in rows),
        current_glyph_defect_records=[row['id'] for row in rows if row.get('current_unintended_glyphs')],
        glyph_only_revisions=[row['id'] for row in rows if row.get('glyph_only_revision_with_wording_retained')],
        all_individual_four_prose_gates_pass=True, all_fifth_formatting_gates_pending=True,
        native_macro_tokens_still_require_formatter_marking=True,
        no_new_formatting_rendering_gameplay_orregistered_integration_claim=True, new_credit=0, evidence=evidence)

    projected = deepcopy(document)
    projected['translation_policy'] = 'natural-dialogue-v1'
    validate_natural_dialogue_batch(projected)
    assert all(row['source_meaning'].strip() and row['localization_note'].strip() for row in rows)
    try:
        validate_natural_dialogue_batch(document)
    except ValueError as error:
        assert 'requires per-record source, context, localization, naturalness, and formatting review' in str(error)
    else:
        raise AssertionError('Unformatted manuscript unexpectedly passed the release gate')
    save(OUT, document)
    print(f"Saved {len(rows)} complete-exchange reviews: {document['proposed_revisions']} revisions, "
        f"{document['justified_retentions']} retentions, {len(document['current_glyph_defect_records'])} glyph-defect records. "
        "Four prose gates pass; formatting, gameplay and release remain pending.")


if __name__ == '__main__':
    main()
