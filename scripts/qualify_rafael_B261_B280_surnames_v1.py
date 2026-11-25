"""Qualify Jacob's fixed surname and document Plett's relocation requirement."""
from pathlib import Path
import struct

from dk4tool.patch.main_pool_cache_visibility import BASE
from dk4tool.patch.owned_name_fields_v2 import plan_arm9_name_fields
from dk4tool.rom.nds import NdsImage
from scripts.registered_editorial_runtime_v2 import RegisteredRuntime
from scripts.write_rafael_B261_B280_contextual_v1 import LABELS, ROOT, load, save, sha


OUT = ROOT / 'surname_ownership_v1'
CLEAN = Path('work/clean.nds')


def main():
    assert not OUT.exists()
    names = load(LABELS)
    receipt = names['runtime']
    ctx = RegisteredRuntime(receipt['release_proof'], receipt['startup_proof'], captain=0)
    assert ctx.receipt() == receipt
    assert sha(CLEAN.read_bytes()) == load(receipt['release_proof'])['clean_input_sha256']
    arm = ctx.arm
    clean = NdsImage.open(CLEAN).read_file('/__arm9__.bin')
    table = struct.unpack_from('<I', arm, 0xCDAC0)[0] - BASE
    fields = [(actor, col, table + 32 * actor + col) for actor in range(207) for col in (0, 4, 8)]
    resolved = []
    for binding in names['records']:
        if binding['decision'] != 'revision':
            continue
        actor = binding['actor_ID']
        current_name = binding['current_forms']['progressive-nameplate']
        approved_name = binding['approved_forms']['progressive-nameplate']
        given, target = approved_name.split(' ', 1)
        field = next(row for row in binding['source_andcurrent_fields'] if row['column'] == 4)
        source, current = field['source'], field['current']
        assert current_name == given + ' ' + current['text']
        offset, pointer = current['field_offset'], current['pointer']
        at = pointer - BASE
        before = bytes.fromhex(current['hex'])
        assert arm[at:at + len(before) + 1] == before + bytes(1)
        assert struct.unpack_from('<I', arm, offset)[0] == pointer
        owners = []
        for owner_actor, col, owner_offset in fields:
            address = struct.unpack_from('<I', arm, owner_offset)[0]
            if pointer <= address < pointer + len(before):
                owners.append(dict(actor=owner_actor, column=col, pointer=address, field_offset=owner_offset))
        refs = []
        for index, (address,) in enumerate(struct.iter_unpack('<I', arm[:len(arm) // 4 * 4])):
            if pointer <= address < pointer + len(before):
                refs.append(dict(offset=4 * index, pointer=address))
        assert owners == [dict(actor=actor, column=4, pointer=pointer, field_offset=offset)]
        assert refs == [dict(offset=offset, pointer=pointer)]
        resolved.append(dict(
            actor=actor, column=4, table_field_offset=offset, pointer=pointer, physical_offset=at,
            source_hex=before.hex(), current_text=current['text'], target_text=target, owned_bytes=len(before),
            source_clean_component=dict(column=4, source_ARM9_field_offset=source['field_offset'],
                                        pointer=source['pointer'], offset=source['pointer'] - BASE,
                                        hex=source['hex'], text=source['text']),
            reason=binding['finding'], review=binding['review'], owners=owners, aligned_ARM9_references=refs,
            following16_hex=arm[at + len(before):at + len(before) + 16].hex(),
        ))
    plett, jacob = resolved
    assert (plett['actor'], jacob['actor']) == (65, 68)
    at = plett['physical_offset']
    assert clean[at:at + 8] == 'ペロー'.encode('cp932') + bytes(2)
    assert arm[at:at + 8] == b'Perot' + bytes(3)
    assert arm[at + 8:at + 15] == b'Sakura' + bytes(1)
    assert len(plett['target_text']) + 1 == 9
    jacob['target_hex'] = jacob['target_text'].encode('ascii').ljust(jacob['owned_bytes'], bytes(1)).hex()
    proposal = dict(format='dk4-owned-name-fields-proposal-v2', runtime=receipt, fields=[jacob], new_credit=0)
    target_arm, proof = plan_arm9_name_fields(arm, proposal, clean)
    assert proof['complete_parent_inverse_exact'] and proof['all_unowned_ARM9_bytes_sections_pointer_tables_andallocations_exact']
    OUT.mkdir()
    path = OUT / 'jacob_portunto_reference_arm9.bin'
    path.write_bytes(target_arm)
    save(OUT / 'owned_fields_proposal.json', proposal)
    save(OUT / 'ownership_verification.json', dict(
        **proof, runtime=receipt, fixed_surname_reference=str(path), fixed_surname_reference_sha256=sha(target_arm),
        plett=dict(**plett, verified_original_slot_bytes_including_terminator=8, target_bytes_including_terminator=9,
                   adjacent_protected_text='Sakura', relocation_required=True),
        live_nameplate_and_both_corrected_getters_pending=True, actual_gameplay=False, new_credit=0,
    ))
    print('Jacob: fixed field with exact ARM9 inverse. Plett: original 8-byte slot needs relocation for 9-byte target.')


if __name__ == '__main__':
    main()
