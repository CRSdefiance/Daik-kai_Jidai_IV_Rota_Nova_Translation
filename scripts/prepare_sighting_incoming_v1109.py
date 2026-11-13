"""Pair the proven compass approach with original incoming-attack prerequisites."""
from pathlib import Path


def main():
    target=Path('scripts/native_sighting_context_v1109.py');assert not target.exists()
    body=Path('scripts/native_sighting_context_v1087b.py').read_text(encoding='utf-8')
    body=body.replace('out/all_routes_combined_v1086_candidate.nds','out/all_routes_combined_v1105_candidate.nds').replace(
        'translations/sighting_editorial_release_v1.json','translations/sighting_grammar_editorial_release_v1.json')
    before="{'sighting_context':'compassReady8'})";assert body.count(before)==1
    body=body.replace(before,"{'sighting_context':'compassReady8'},{'sighting_context':'compassAttack8'})")
    before="incoming=context=='closeAttack8'";assert body.count(before)==1
    body=body.replace(before,"incoming=context in ('closeAttack8','compassAttack8')")
    before="context!='compassReady8'";assert body.count(before)==1
    body=body.replace(before,"context not in ('compassReady8','compassAttack8')")
    target.write_text(body,encoding='utf-8')
    target=Path('scripts/run_sighting_incoming_v1109.py');assert not target.exists()
    body=Path('scripts/run_sighting_grammar_gameplay_v1106b.py').read_text(encoding='utf-8')
    body=body.replace('sighting_grammar_gameplay_v1106b_','sighting_incoming_v1109_').replace(
        'sighting_grammar_v1106b_1105_','sighting_incoming_v1109_1105_').replace(
        'scripts.native_sighting_grammar_fixture_v1106b','scripts.native_sighting_context_v1109').replace(
        'scripts/native_sighting_grammar_fixture_v1106b.py','scripts/native_sighting_context_v1109.py').replace(
        'compassReady8','compassAttack8')
    target.write_text(body,encoding='utf-8')
    target=Path('scripts/verify_sighting_incoming_v1109.py');assert not target.exists()
    body=Path('scripts/verify_sighting_grammar_gameplay_v1106b.py').read_text(encoding='utf-8')
    body=body.replace('sighting_grammar_actual_v1106b','sighting_incoming_actual_v1109').replace(
        'sighting_grammar_v1106b_1105_','sighting_incoming_v1109_1105_').replace(
        'sighting_grammar_gameplay_v1106b_','sighting_incoming_v1109_').replace(
        'scripts.native_sighting_grammar_fixture_v1106b','scripts.native_sighting_context_v1109').replace(
        'compassReady8','compassAttack8').replace('614','622').replace('0x02118560','0x02118540').replace(
        "len(r['owned_bytes'])==17", "len(r['owned_bytes'])==19").replace(
        'one_exact17_byte_location_and_original_hostility_precondition_replay','one_exact19_byte_location_and_original_hostility_attack_order_precondition_replay').replace(
        'one exact17-byte fixture','one exact19-byte fixture').replace(
        'Actual622 compass','Actual622 incoming attack')
    target.write_text(body,encoding='utf-8')
    print('Prepared19-byte incoming counterpart;original first-sighting,AI order,dialogue selection and outcomes stay native.')


if __name__=='__main__':main()
