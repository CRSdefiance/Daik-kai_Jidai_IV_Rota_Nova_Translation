"""Bind four whole exchanges to the clean B261–B280 intake."""
from pathlib import Path
import re

from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load, save


ROOT = Path('work/Rafael_B261_B280_clean_20261106')
OUTPUT = ROOT / 'B261_B264_clean_drafts_v1.json'
DRAFT = Path('translations/rafael_B261_B264_clean_drafts_v1.txt')
PACKET = ROOT / 'clean_source_packet.json/clean_source_packet.json'
STYLES = ROOT / 'clean_style_objects.json'
MENUS = ROOT / 'clean_choice_objects.json'
BLOCKS = [261, 262, 263, 264]


def digest(path):
    return sha(Path(path).read_bytes())


def main():
    assert not OUTPUT.exists()
    packet, styles, menus = map(load, (PACKET, STYLES, MENUS))
    assert packet['clean_only_no_prior_English_ornew_editorial_credit']
    assert styles['source_packet_sha256'] == menus['source_packet_sha256'] == digest(PACKET)
    source = {
        row['id']: row for row in (
            [r for group in packet['groups'] for r in group['records']]
            + styles['records'] + menus['records'])
        if row['block'] in BLOCKS
    }
    contexts, rows = {}, []
    for line in DRAFT.read_text(encoding='utf-8').splitlines():
        if not line or line.startswith('#'):
            continue
        ident, meaning, english = line.split('|', 2)
        if ident.startswith('@'):
            block = int(ident[1:])
            assert block in BLOCKS and block not in contexts and meaning and not english
            contexts[block] = meaning
            continue
        row = source.pop(ident)
        assert row['block'] in contexts and meaning and english and english.isascii()
        assert not any(token in english for token in ('{LB', '{ALIGN', '{PAD}'))
        payload = bytes.fromhex(row['source_hex'])
        if ident.startswith('DK4_MES_'):
            assert row['source_decode_error'] is None and payload[0] == row['source_selector']
            payload = payload[1:]
        tokens = [match.decode() for match in re.findall(rb'F[A-Z]', payload)]
        assert re.findall(r'\bF[A-Z]\b', english) == tokens
        rows.append({**row, 'source_meaning': meaning, 'independent_English': english,
            'context': contexts[row['block']], 'native_literal_tokens': tokens,
            'review': dict(source=False, context=False, localization=False, naturalness=False, formatting=False),
            'current_English_comparison_pending': True, 'new_credit': 0})
    assert not source and list(contexts) == BLOCKS
    assert len(rows) == 57 and sum(row.get('kind') == 'actor-style-alternative' for row in rows) == 16
    assert sum(row.get('kind') == 'typed-choice-label' for row in rows) == 5
    save(OUTPUT, dict(records=rows, records_count=57, ordinary_speeches=36, style_alternatives=16,
        typed_captions=5, complete_blocks=BLOCKS, source_contexts=contexts, all_five_gates_pending=True,
        no_current_English_extracted_for_this_intake_before_drafts=True, guide_photos=False, new_credit=0,
        evidence={str(path): digest(path) for path in (PACKET, STYLES, MENUS, DRAFT, Path(__file__))}))
    print('Sealed 57 clean-source drafts across four complete Rafael exchanges.')


if __name__ == '__main__':
    main()
