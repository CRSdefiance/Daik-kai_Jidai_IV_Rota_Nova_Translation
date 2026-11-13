"""Seal the complete Rafael B281–B300 source glosses and independent drafts."""
from pathlib import Path
import re

from scripts.audit_story_glyph_consistency import load, save
from scripts.seal_rafael_B281_B286_clean_v1 import MENUS, OUTPUT, PACKET, ROOT, STYLES
from scripts.seal_rafael_B261_B264_clean_v1 import digest


SEALED = ROOT/'sealed_clean_first_v1'
DRAFTS = [Path(f'translations/rafael_{name}_clean_drafts_v1.txt') for name in (
    'B281_B286', 'B287_B292', 'B293', 'B294_B300')]
LEDGER = Path('translations/editorial_review_current_v1.json')
BLOCKS = list(range(281, 301))
MACROS = re.compile(rb'F[AOIU]')


def main():
    assert not SEALED.exists()
    packet, styles, menus, first = map(load, (PACKET, STYLES, MENUS, OUTPUT))
    assert packet['clean_only_no_prior_English_ornew_editorial_credit']
    assert styles['source_packet_sha256'] == menus['source_packet_sha256'] == digest(PACKET)
    assert [group['block'] for group in packet['groups']] == BLOCKS
    speech = [row for group in packet['groups'] for row in group['records']]
    alternatives, captions = styles['records'], menus['records']
    assert (len(speech), len(alternatives), len(captions)) == (164, 76, 5)
    source = {row['id']: row for row in speech + alternatives + captions}
    assert len(source) == 245
    contexts, records = {}, []
    for path in DRAFTS:
        active = None
        for line in path.read_text(encoding='utf-8').splitlines():
            if not line or line.startswith('#'):
                continue
            ident, meaning, english = line.split('|', 2)
            if ident.startswith('@'):
                active = int(ident[1:])
                assert active in BLOCKS and active not in contexts and meaning and not english
                contexts[active] = meaning
                continue
            original = source.pop(ident)
            assert original['block'] == active and meaning and english and english.isascii()
            assert not any(token in english for token in ('{LB', '{ALIGN', '{PAD}', '\t'))
            raw = bytes.fromhex(original['source_hex'])
            if ident.startswith('DK4_MES_'):
                assert original['source_decode_error'] is None and raw[0] == original['source_selector']
                raw = raw[1:]
            tokens = [match.decode('ascii') for match in MACROS.findall(raw)]
            assert re.findall(r'\bF[AOIU]\b', english) == tokens, ident
            records.append({**original, 'source_meaning': meaning, 'independent_English': english,
                'context': contexts[active], 'native_literal_tokens': tokens,
                'review': dict.fromkeys(('source','context','localization','naturalness','formatting'), False),
                'current_English_comparison_pending': True, 'new_credit': 0})
    assert not source and list(contexts) == BLOCKS
    assert records[:32] == first['records']
    assert first['no_current_English_extracted_for_this_intake_before_drafts']
    assert all(digest(path) == expected for path, expected in first['evidence'].items())
    assert len(records) == 245
    key = lambda row: (row['file_path'], row['id'])
    integrated = load(LEDGER)['contextual_story_natural_dialogue_pass_v1871']['integrated_record_keys']
    assert set(map(key, records)).isdisjoint(map(key, integrated))
    by_id = {row['id']: row for row in records}
    SEALED.mkdir()
    sealed = SEALED/'sealed_drafts.json'
    save(sealed, dict(records=sorted(records, key=lambda row: (row['block'], row['source_reference']['offset'])),
        records_count=245, ordinary_speeches=164, physical_style_alternatives=76, style_objects=11,
        style_alias_slots=88, typed_captions=5, typed_choice_objects=2, complete_blocks=BLOCKS,
        source_contexts=contexts, source_meanings_andlogical_drafts_sealed_before_current_ROM_English_extraction_in_this_intake=True,
        all_individual_review_gates_pending=True, no_already_credited_record_keys=True, new_credit=0,
        evidence={str(path): digest(path) for path in (PACKET, STYLES, MENUS, OUTPUT, *DRAFTS, Path(__file__))}))
    shared = dict(source_packet=str(PACKET), source_packet_sha256=digest(PACKET),
                  all_drafts_sealed=str(sealed), all_drafts_sha256=digest(sealed), new_credit=0)
    save(SEALED/'current_binding_meanings.json', dict(records=[
        {**by_id[row['id']], 'current_ROM_English_unconsulted': True} for row in speech],
        meanings=164, no_blanket_prior_English_exposure_claim=True, **shared))
    for kind, doc in (('style', styles), ('choice', menus)):
        save(SEALED/f'{kind}_meanings.json', {**doc, **shared, 'records': [by_id[row['id']] for row in doc['records']]})
    print('Sealed all 245 independent drafts. The first 32 match the previous checkpoint exactly.')


if __name__ == '__main__':
    main()
