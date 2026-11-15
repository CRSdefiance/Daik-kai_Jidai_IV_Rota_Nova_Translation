"""Add independent logical drafts to whole-exchange meanings without review credit."""
import argparse
import importlib
import re
from copy import deepcopy
from pathlib import Path
from scripts.audit_story_glyph_consistency import load, save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for key in ['meanings', 'module', 'out']:
        parser.add_argument('--' + key, required=True)
    args = parser.parse_args()
    meanings_path, out = Path(args.meanings), Path(args.out)
    assert not out.exists()
    meanings = load(meanings_path)
    data = importlib.import_module(args.module)
    assert meanings['current_English_unconsulted']
    expected = {(r['block'], r['source_record_index']): r for r in meanings['records']}
    authored = {(block, index): draft for block, rows in data.DRAFTS.items() for index, draft in rows}
    assert len(authored) == sum(len(rows) for rows in data.DRAFTS.values()) == len(expected)
    assert authored.keys() == expected.keys()
    records = []
    for key, source in expected.items():
        assert source['source_first_independent_meaning_saved'] and not any(source['review'].values())
        draft = authored[key]
        assert draft and draft == draft.strip() and draft.isascii()
        assert not any(s in draft for s in ['\n', '\r', '\t', '{LB', '{PAD}', '{ALIGN'])
        raw = bytes.fromhex(source['source_hex'])
        body = raw[1:] if source['kind'] == 'ordinary-speech' else raw
        macros = {t.decode(): body.count(t) for t in sorted(set(re.findall(rb'F[A-Z]', body)))}
        assert {t: draft.count(t) for t in macros} == macros, source['id']
        assert set(re.findall(r'F[A-Z]', draft)) == set(macros), source['id']
        row = deepcopy(source)
        row.update(independent_English_draft=draft, localized_draft_pending=False,
            independent_draft_precedes_current_English_intake=True,
            source_macros=macros, current_English_comparison_pending=True,
            name_term_control_consumer_andfresh_formatting_approval_pending=True,
            no_blanket_historical_English_unexposure_claim=True, new_credit=0)
        records.append(row)
    save(out, dict(records=records, records_count=len(records), blocks=list(data.DRAFTS),
        translation_policy='natural-dialogue-v2', target_locale='en-US',
        clean_source_packet=meanings['clean_source_packet'],
        clean_source_packet_sha256=meanings['clean_source_packet_sha256'],
        current_English_unconsulted=True, all_logical_drafts_from_complete_clean_exchanges=True,
        no_source_meaning_orcontrol_modified=True, all_five_gates_still_pending=True,
        no_ROM_registry_orcompletion_credit_changes=True, new_credit=0,
        evidence={str(p): digest(p) for p in [meanings_path, Path(data.__file__), Path(__file__)]}))
    print(f'Sealed {len(records)} independent logical drafts in {len(data.DRAFTS)} complete exchanges; zero credit.')


if __name__ == '__main__':
    main()
