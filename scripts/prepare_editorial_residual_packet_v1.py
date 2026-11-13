"""Reuse an exact source census to prepare whole, entirely uncredited exchanges."""
import argparse
from collections import Counter
from pathlib import Path

from scripts.audit_story_glyph_consistency import load, save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--audit', type=Path, required=True)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    assert not args.out.exists()
    audit = load(args.audit)
    residual_path = args.audit.with_name('residual_clean_source_packet.json')
    residual = load(residual_path)
    assert not audit['inventory_failures'] and not audit['legacy_source_bindings_not_exact']
    assert digest(audit['ledger']) == audit['ledger_sha256']
    assert digest(audit['source_ROM']) == audit['source_ROM_sha256']
    archive = residual['file_path']
    ledger = load(audit['ledger'])
    credited = {(r['file_path'], r['id']) for r in ledger['contextual_story_natural_dialogue_pass_v1871']['integrated_record_keys']
                if r['file_path'] == archive}
    matched = {(archive, b['id']) for r in audit['records'] for b in r['exact_credited_source_bindings']}
    assert credited == matched
    assert all(len(r['exact_credited_source_bindings']) == 1 for r in audit['records'] if r['covered'])
    groups = []
    for original in residual['groups']:
        assert all(not r['covered'] for r in original['records'])
        block = bytes.fromhex(original['clean_block_hex'])
        commands = {r['offset']: r for r in original['all_source_commands']}
        assert all(block[c['offset']:c['offset']+c['native_extent']].hex() == c['whole_command_hex'] for c in commands.values())
        rows = []
        for record in original['records']:
            if record['kind'] != 'ordinary-speech':
                continue
            at = record['source_reference']['offset']
            raw = bytes.fromhex(record['source_hex'])
            command = commands[at-5]
            assert command['word'] == 0x4000 and block[at:at+len(raw)+1] == raw+b'\0'
            rows.append(dict(id=record['id'], file_path=archive, block=original['block'],
                source_selector=raw[0], source_hex=raw.hex(), source_Japanese=raw[1:].decode('cp932'),
                source_decode_error=None, source_complete_preamble_hex=block[at-5:at+1].hex(),
                source_reference=dict(file_path=archive, block=original['block'], offset=at,
                    header_offset=at-5, record_index=block[:at].count(b'\0'), length=len(raw)),
                source_0100_ancestors=command['ancestor_0100_offsets'], native_extent=command['native_extent'],
                source_macros={m:raw[1:].count(m.encode()) for m in ('FI','FA','FO')},
                earlier_English_unconsulted=True, source_context_localization_formatting_gates_pending=True,
                source_preamble_andname_consumer_approval_not_inferred=True))
        groups.append({**original, 'clean_block_sha256': __import__('hashlib').sha256(block).hexdigest(), 'records':rows})
    counts = Counter(r['kind'] for r in audit['missing'])
    assert sum(len(g['records']) for g in groups) == counts['ordinary-speech']
    args.out.mkdir(parents=True)
    save(args.out/'clean_source_packet.json', {**residual, 'groups':groups, 'records':counts['ordinary-speech'],
        'clean_only_no_prior_English_ornew_editorial_credit':True,
        'conditional_membership_is_structural_not_natural_activation':True,
        'complete_native_inventory_reused_not_rerun':True,
        'coverage_audit':str(args.audit), 'coverage_audit_sha256':digest(args.audit),
        'producer_sha256':digest(__file__)})
    save(args.out/'coverage_reconciliation_v1.json', dict(archive=archive,
        source_objects=len(audit['records']), exact_credited_objects=len(credited),
        missing_objects=len(audit['missing']), missing_types=dict(counts),
        all_prior_integrated_archive_keys_exactly_matched=True, duplicate_orambiguous_bindings=0,
        source_binding_failures=0, inventory_failures=0,
        complete_uncredited_blocks=[g['block'] for g in groups],
        source_only_no_meanings_drafts_comparisons_orgates_yet=True,
        not_full_player_facing_resource_orreachability_census=True,
        evidence={str(p):digest(p) for p in (args.audit,residual_path,Path(audit['ledger']),Path(__file__))},
        new_credit=0, full_goal_complete=False))
    print(dict(ordinary_speeches=counts['ordinary-speech'], physical_style_alternatives=counts['physical-style-alternative'],
        typed_captions=counts['typed-menu-caption'], complete_blocks=len(groups), prior_keys_conserved=len(credited), new_credit=0))


if __name__ == '__main__':
    main()
