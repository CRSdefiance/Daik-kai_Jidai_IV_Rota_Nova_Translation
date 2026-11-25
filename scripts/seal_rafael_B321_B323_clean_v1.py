"""Seal three complete Sakura exchanges against the clean source packet."""
from pathlib import Path
import re

from scripts.audit_story_glyph_consistency import load, save
from scripts.checkpoint_rafael4347_registered_v1 import LEDGER, PACKET, ROOT
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest


DRAFT = Path('translations/rafael_B321_B323_clean_drafts_v1.txt')
SEALED = ROOT / 'B321_B323_sealed_clean_drafts_v1.json'
BLOCKS = [321, 322, 323]
MACROS = re.compile(rb'F[AOIU]')


def main():
    assert not SEALED.exists()
    packet = load(PACKET)
    assert packet['clean_only_no_prior_English_ornew_editorial_credit']
    originals = [row for group in packet['groups'] if group['block'] in BLOCKS for row in group['records']]
    contexts = {}
    records = []
    source = iter(originals)
    for line in DRAFT.read_text(encoding='utf-8').splitlines():
        if not line or line.startswith('#'):
            continue
        ident, meaning, english = line.split('|', 2)
        if ident.startswith('@'):
            block = int(ident[1:])
            assert block not in contexts and meaning and not english
            contexts[block] = meaning
            continue
        original = next(source)
        assert original['id'] == ident and original['block'] == block, ident
        assert original['source_decode_error'] is None and meaning and english and english.isascii()
        assert not any(token in english for token in ('{LB', '{ALIGN', '{PAD}', '\t'))
        raw = bytes.fromhex(original['source_hex'])
        assert raw[0] == original['source_selector']
        tokens = [token.decode('ascii') for token in MACROS.findall(raw[1:])]
        assert re.findall(r'\bF[AOIU]\b', english) == tokens, ident
        records.append({**original, 'source_meaning': meaning, 'independent_English': english,
                        'native_literal_tokens': tokens, 'context': contexts[block],
                        'review': dict.fromkeys(('source', 'context', 'localization', 'naturalness', 'formatting'), False),
                        'current_English_comparison_pending': True, 'new_credit': 0})
    assert list(contexts) == BLOCKS and next(source, None) is None and len(records) == 42
    key = lambda row: (row['file_path'], row['id'])
    integrated = load(LEDGER)['contextual_story_natural_dialogue_pass_v1871']['integrated_record_keys']
    assert set(map(key, records)).isdisjoint(map(key, integrated))
    save(SEALED, dict(records=records, records_count=len(records), complete_blocks=BLOCKS,
                      source_contexts=contexts, current_ROM_English_unconsulted=True,
                      merchandise_term_pending_game_terminology_check='chintz', new_credit=0,
                      evidence={str(path): digest(path) for path in (PACKET, DRAFT, Path(__file__))}))
    print('Sealed 42 clean-first drafts from three Sakura exchanges. No integrated credit added.')


if __name__ == '__main__':
    main()
