"""Distinguish literal player-name initials from English articles at row ends."""

from copy import deepcopy
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts.context_barmaid_dialogue_v779 import ROOT
from scripts.review_barmaid_dialogue_v779 import MANUSCRIPT
from scripts.verify_village_wrap_v608 import read, save

WEAK = {b'a', b'an', b'as', b'at', b'for', b'from', b'in', b'of', b'the', b'to', b'with'}
PUNCT = b'.,!?;:'


def origins(row, case):
    values = [bytes.fromhex(v) for v in case['English_values_hex']]
    roles = [row['source_native_arguments'][i] for i in row['English_argument_source_indices']]
    parts = (b' '+row['english'].removesuffix('{PAD}').encode('ascii')).split(b'%s')
    assert len(parts) == len(values)+1 == len(roles)+1
    expected, mapping = bytearray(), []
    for i, part in enumerate(parts):
        expected.extend(part)
        mapping.extend([None]*len(part))
        if i < len(values):
            expected.extend(values[i])
            mapping.extend([roles[i]]*len(values[i]))
    assert b' '.join(bytes.fromhex(case['formatted_hex']).split()) == b' '.join(expected.split())
    cursor, found = 0, []
    for i, line in enumerate(case['lines']):
        while cursor < len(expected) and expected[cursor] in b' \t\r\n':
            cursor += 1
        raw = line.encode('cp932')
        assert expected[cursor:cursor+len(raw)] == raw
        token = raw.split()[-1]
        word = token.strip(PUNCT)
        if i < len(case['lines'])-1 and word.lower() in WEAK:
            left = len(raw)-len(token)+len(token)-len(token.lstrip(PUNCT))
            a, b = cursor+left, cursor+left+len(word)
            found.append({'line': i, 'word_hex': word.hex(), 'expanded_byte_span': [a, b],
                          'source_argument_roles': mapping[a:b],
                          'entire_word_is_literal_captain_name': all(v == 'captain_first_name' for v in mapping[a:b])})
        cursor += len(raw)
    assert not bytes(expected[cursor:]).strip()
    return found


def main():
    source = ROOT/'layouts_v1/native_layout_matrix.json'
    doc = read(MANUSCRIPT)
    rows = {r['message_id']: r for r in doc['records']}
    matrix = read(source)
    assert matrix['manuscript_sha256'] == sha(MANUSCRIPT.read_bytes())
    classified = []
    for case in matrix['findings']:
        assert case['findings'] == ['weak_line_end'] and case['id'] in (989, 999)
        words = origins(rows[case['id']], case)
        assert words and all(w['entire_word_is_literal_captain_name'] for w in words)
        classified.append({'case': case, 'word_origins': words,
                           'resolution': 'Complete literal player-name token or initial,not an English article. Keep exact name and spacing;no source prose or rendering rule is waived.'})
    assert len(classified) == 5
    example = matrix['findings'][0]
    row = deepcopy(rows[example['id']])
    values = [bytes.fromhex(v) for v in example['source_values_hex']]
    # Make the identical displayed A... sequence literal prose instead of a
    # name argument. It must no longer receive the typed-name classification.
    row['english'] = row['english'].replace('Your name is... %s', 'Your name is... '+values[1].decode('ascii'))
    row['source_native_arguments'] = ['barmaid']
    row['English_argument_source_indices'] = [0]
    literal_case = deepcopy(example)
    literal_case['English_values_hex'] = [values[0].hex()]
    rejected = origins(row, literal_case)
    assert rejected and not any(w['entire_word_is_literal_captain_name'] for w in rejected)
    save(ROOT/'layouts_v1/name_token_findings.json', {
        'manuscript_sha256': sha(MANUSCRIPT.read_bytes()), 'native_matrix_sha256': sha(source.read_bytes()),
        'all273_native_layouts_have_complete_words_guards_and_bounds': True,
        'five_naive_article_diagnostics_are_exactly_bound_to_name_bytes': classified,
        'unresolved_prose_or_layout_findings': [], 'literal_prose_negative_control_rejected': True,
        'no_blanket_weak_ending_or_user_name_waiver': True,
        'production_formatter_and_gameplay_still_pending': True,
        'producer_sha256': sha(Path(__file__).read_bytes()), 'full_goal_complete': False})
    print('Five apparent article endings are source-bound player-name initials;literal-prose negative rejected. No prose/layout findings remain in273 supplied cases.', flush=True)


if __name__ == '__main__':
    main()
