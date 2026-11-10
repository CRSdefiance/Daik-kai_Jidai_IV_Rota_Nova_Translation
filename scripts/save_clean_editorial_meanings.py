"""Bind authored whole-exchange source meanings to exact clean records, before English comparison."""
import argparse
from pathlib import Path
from scripts.audit_story_glyph_consistency import load, save
from dk4tool.patch.grand_race_menu_release import sha


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ['packet', 'decisions', 'out']:
        parser.add_argument('--' + name, type=Path, required=True)
    args = parser.parse_args()
    assert not args.out.exists()
    packet, decisions = map(load, [args.packet, args.decisions])
    groups = {g['block']: g for g in packet['groups']}
    rows = []
    for block_string, decision in decisions['blocks'].items():
        block = int(block_string)
        group = groups[block]
        assert len(group['records']) == len(decision['meanings'])
        assert decision['context'].strip()
        for source, meaning in zip(group['records'], decision['meanings'], strict=True):
            assert isinstance(meaning, str) and meaning.strip()
            assert bytes.fromhex(source['source_hex'])[1:].decode('cp932') == source['source_Japanese']
            rows.append(dict(id=source['id'], file_path=source['file_path'], block=block,
                source_reference=source['source_reference'], source_hex=source['source_hex'], source_Japanese=source['source_Japanese'],
                source_selector=source['source_selector'], source_complete_preamble_hex=source['source_complete_preamble_hex'],
                source_0100_ancestors=source['source_0100_ancestors'], source_macros=source['source_macros'],
                source_meaning=meaning, exchange_context=decision['context'],
                earlier_English_unconsulted=True, native_identity_terms_localization_andformatting_pending=True, new_credit=0))
    assert len(rows) == len({r['id'] for r in rows})
    save(args.out, dict(source_packet=str(args.packet), source_packet_sha256=sha(args.packet.read_bytes()),
        authored_decisions=str(args.decisions), authored_decisions_sha256=sha(args.decisions.read_bytes()),
        records=rows, complete_exchanges=[int(k) for k in decisions['blocks']], source_meanings=len(rows),
        source_fidelity_notes={k: v.get('notes', []) for k, v in decisions['blocks'].items()},
        not_final_localized_English_orfive_gate_approval=True, earlier_English_unconsulted=True, new_credit=0,
        producer_sha256=sha(Path(__file__).read_bytes())))
    print(dict(clean_meanings=len(rows), complete_blocks=[int(k) for k in decisions['blocks']], no_prior_English=True, new_credit=0))


if __name__ == '__main__':
    main()
