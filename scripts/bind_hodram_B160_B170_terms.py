"""Reuse the reviewed role dictionary and bind remaining source names without old dialogue."""
import struct
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.audit_native_given_name_table import string
from scripts.audit_story_glyph_consistency import load, save

ROOT = Path('work/analysis/Hodram_B151_B170_clean_20261102')


if __name__ == '__main__':
    target = ROOT / 'remaining_role_ship_and_Venice_terms_v1.json'
    assert not target.exists()
    identity = load(ROOT / 'native_identity_and_item_checkpoint_v1.json')
    runtime = identity['runtime']
    rom = Path(runtime['candidate'])
    assert sha(rom.read_bytes()) == runtime['candidate_sha256']
    current = NdsImage.open(rom).read_file('/__arm9__.bin')
    clean = NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    raw = Path(runtime['snapshot']['path']).read_bytes()
    assert sha(raw) == runtime['snapshot']['sha256']
    precedent = Path('work/analysis/crew_roles_v326/native_proof.json')
    proof = load(precedent)
    literal = proof['transform']['table_literal_field']
    table = struct.unpack_from('<I', current, literal)[0]
    roles = []
    for role in proof['transform']['roles']:
        assert string(clean, role['original_pointer'])['text'] == role['Japanese']
        at = table - 0x02000000 + 4 * role['index']
        pointer = struct.unpack_from('<I', raw, at)[0]
        start = pointer - 0x02000000
        end = raw.index(0, start)
        value = raw[start:end]
        assert value.decode('cp932') == role['stored']
        roles.append(dict(index=role['index'], Japanese=role['Japanese'], English=role['English'],
                          source_pointer=role['original_pointer'], current_entry_address=at + 0x02000000,
                          current_pointer=pointer, complete_current_string_hex=value.hex(),
                          existing_padding_not_authored_in_dialogue=True))
    assert roles[3]['English'] == 'Purser'
    # This original ship-name literal is still Japanese in its separate code consumer.
    # Elysion is a source-supported dialogue rendering, not a claim that this UI is localized.
    ship_field = 178732
    source_pointer = struct.unpack_from('<I', clean, ship_field)[0]
    current_pointer = struct.unpack_from('<I', current, ship_field)[0]
    source_ship = string(clean, source_pointer)
    current_ship = string(current, current_pointer)
    assert source_ship['text'] == current_ship['text'] == 'エリュシオン'
    needle = 'ヴェネツィア'.encode('cp932') + b'\0'
    places = []
    at = 0
    while True:
        at = clean.find(needle, at)
        if at < 0:
            break
        pointer_bytes = struct.pack('<I', at + 0x02000000)
        for field in range(1190000, 1201000, 4):
            if clean[field:field + 4] != pointer_bytes:
                continue
            pointer = struct.unpack_from('<I', current, field)[0]
            start = pointer - 0x02000000
            end = raw.index(0, start)
            value = raw[start:end]
            if value.decode('cp932') == 'Venice':
                places.append(dict(source_pointer=at + 0x02000000, source_hex=needle[:-1].hex(),
                                   pointer_field_offset=field, current_pointer=pointer,
                                   complete_current_name_hex=value.hex(), established_English='Venice'))
        at += len(needle)
    assert len(places) == 1
    save(target, dict(runtime=runtime, existing_role_proof=str(precedent), existing_role_proof_sha256=sha(precedent.read_bytes()),
                      current_role_table_literal_offset=literal, current_role_table_pointer=table, roles=roles,
                      ordinary_role_native_proofs_reused_no_new_getter_permutations=True,
                      source_主計長_uses_approved_Purser_not_improvised_Quartermaster=True,
                      ship=dict(source_field=ship_field, clean=source_ship, current_code_literal=current_ship,
                                dialogue_rendering='Elysion', Japanese_honorific_ship_suffix_号_omitted_in_English=True,
                                separate_current_code_ship_name_still_Japanese=True,
                                source_owned_consumer_scope_andEnglish_UI_repair_pending=True,
                                no_new_ship_identity_orGood_Luck_rename=True), Venice=places[0],
                      no_prior_English_dialogue_consulted=True, new_ROMs=0, new_credit=0,
                      evidence={str(p):sha(p.read_bytes()) for p in [ROOT/'native_identity_and_item_checkpoint_v1.json', precedent, Path(__file__)]}))
    print('Bound16 existing role labels,including Purser;Venice retained;Elysion source literal recorded with separate Japanese-code consumer still pending.')
