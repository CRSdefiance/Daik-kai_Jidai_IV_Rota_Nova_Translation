"""Seal source glosses and independent drafts before opening the current English."""
from pathlib import Path
import re

from scripts.audit_story_glyph_consistency import load, save
from scripts.checkpoint_rafael3894_registered_v1 import LEDGER, MENUS, PACKET, ROOT, STYLES
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest


SEALED = ROOT / 'sealed_clean_first_v1'
DRAFTS = [Path(f'translations/rafael_B{start}_B{start+4}_clean_drafts_v1.txt')
          for start in range(301, 321, 5)]
BLOCKS = list(range(301, 321))
MACROS = re.compile(rb'F[AOIU]')


def main():
    assert not SEALED.exists()
    packet, styles, menus = map(load, (PACKET, STYLES, MENUS))
    assert packet['clean_only_no_prior_English_ornew_editorial_credit']
    assert styles['source_packet_sha256'] == menus['source_packet_sha256'] == digest(PACKET)
    assert [group['block'] for group in packet['groups']] == BLOCKS
    speech = [row for group in packet['groups'] for row in group['records']]
    alternatives, captions = styles['records'], menus['records']
    assert (len(speech), len(alternatives), len(captions)) == (297, 145, 11)
    source = {row['id']: row for row in speech + alternatives + captions}
    assert len(source) == 453
    contexts, records = {}, []
    last_offset = -1
    for path in DRAFTS:
        active = None
        for line in path.read_text(encoding='utf-8').splitlines():
            if not line or line.startswith('#'):
                continue
            ident, meaning, english = line.split('|', 2)
            if ident.startswith('@'):
                active = int(ident[1:])
                assert active in BLOCKS and active not in contexts and meaning and not english
                contexts[active], last_offset = meaning, -1
                continue
            original = source.pop(ident)
            assert original['block'] == active and meaning and english and english.isascii(), ident
            assert not any(token in english for token in ('{LB', '{ALIGN', '{PAD}', '\t')), ident
            offset = original['source_reference']['offset']
            assert offset > last_offset, ident
            last_offset = offset
            raw = bytes.fromhex(original['source_hex'])
            if ident.startswith('DK4_MES_'):
                assert original['source_decode_error'] is None and raw[0] == original['source_selector']
                raw = raw[1:]
            tokens = [match.decode('ascii') for match in MACROS.findall(raw)]
            assert re.findall(r'\bF[AOIU]\b', english) == tokens, ident
            records.append({**original, 'source_meaning': meaning, 'independent_English': english,
                'context': contexts[active], 'native_literal_tokens': tokens,
                'review': dict.fromkeys(('source', 'context', 'localization', 'naturalness', 'formatting'), False),
                'current_English_comparison_pending': True, 'new_credit': 0})
    assert not source and list(contexts) == BLOCKS and len(records) == 453
    def key(row):
        return row['file_path'], row['id']
    integrated = load(LEDGER)['contextual_story_natural_dialogue_pass_v1871']['integrated_record_keys']
    assert set(map(key, records)).isdisjoint(map(key, integrated))
    by_id = {row['id']: row for row in records}
    SEALED.mkdir()
    sealed = SEALED / 'sealed_drafts.json'
    save(sealed, dict(records=records, records_count=453, ordinary_speeches=297,
        physical_style_alternatives=145, style_objects=19, style_alias_slots=152,
        typed_captions=11, typed_choice_objects=5, complete_blocks=BLOCKS, source_contexts=contexts,
        source_meanings_andlogical_drafts_sealed_before_current_ROM_English_extraction_in_this_intake=True,
        all_individual_review_gates_pending=True, no_already_credited_record_keys=True, new_credit=0,
        evidence={str(path): digest(path) for path in (PACKET, STYLES, MENUS, *DRAFTS, Path(__file__))}))
    shared = dict(source_packet=str(PACKET), source_packet_sha256=digest(PACKET),
                  all_drafts_sealed=str(sealed), all_drafts_sha256=digest(sealed), new_credit=0)
    save(SEALED / 'current_binding_meanings.json', dict(records=[
        {**by_id[row['id']], 'current_ROM_English_unconsulted': True} for row in speech],
        meanings=297, no_blanket_prior_English_exposure_claim=True, **shared))
    for kind, doc in (('style', styles), ('choice', menus)):
        save(SEALED / f'{kind}_meanings.json', {**doc, **shared, 'records': [by_id[row['id']] for row in doc['records']]})
    print('Sealed 453 clean-first drafts in source order, including all crew voices and menu choices.')


if __name__ == '__main__':
    main()
