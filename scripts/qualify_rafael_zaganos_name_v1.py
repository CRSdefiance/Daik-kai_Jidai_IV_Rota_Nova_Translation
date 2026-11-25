"""Qualify the fixed surname correction and bind both original name getters."""
import inspect
from pathlib import Path
import struct

from dk4tool.patch.main_pool_cache_visibility import BASE
from dk4tool.patch.owned_name_fields_v2 import plan_arm9_name_fields
from dk4tool.rom.nds import NdsImage
from scripts.audit_story_glyph_consistency import load, save
from scripts.prove_lil_B167_names_v4124b import names
from scripts.qualify_rafael_plett_relocation_v1 import raw_hits
from scripts.registered_editorial_runtime_v2 import RegisteredRuntime
from scripts.seal_rafael_B281_B300_clean_v1 import ROOT, digest
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.write_rafael_B281_B300_contextual_v1 import LABELS


OUT = ROOT/'zaganos_name_field_v1'
CLEAN = Path('work/clean.nds')


def main():
    assert not OUT.exists()
    labels = load(LABELS)
    receipt = labels['runtime']
    ctx = RegisteredRuntime(receipt['release_proof'], receipt['startup_proof'], captain=0)
    assert ctx.receipt() == receipt
    assert digest(CLEAN) == load(receipt['release_proof'])['clean_input_sha256']
    clean = NdsImage.open(CLEAN).read_file('/__arm9__.bin')
    arm = ctx.arm
    binding = next(row for row in labels['records'] if row['actor_ID'] == 70)
    assert set(binding['approved_forms'].values()) == {'Zaganos Bey'}
    field = next(row for row in binding['source_andcurrent_fields'] if row['column'] == 4)
    source, current = field['source'], field['current']
    offset, pointer = current['field_offset'], current['pointer']
    at = pointer-BASE
    old, new = bytes.fromhex(current['hex']), b'Bey'
    assert old == b'Bei' and len(old) == len(new) and source['text'] == 'ベイ'
    assert raw_hits(arm, pointer, pointer+len(old)) == [(offset,pointer)]
    assert struct.unpack_from('<I', arm, offset)[0] == pointer
    assert arm[at:at+len(old)+1] == old+b'\0'
    row = dict(actor=70, column=4, table_field_offset=offset, pointer=pointer, physical_offset=at,
        source_hex=old.hex(), target_hex=new.hex(), current_text=current['text'], target_text='Bey',
        owned_bytes=len(old), source_clean_component=dict(column=4, source_ARM9_field_offset=source['field_offset'],
            pointer=source['pointer'], offset=source['pointer']-BASE, hex=source['hex'], text=source['text']),
        reason=binding['finding'], review=binding['review'],
        owners=[dict(actor=70,column=4,pointer=pointer,field_offset=offset)],
        aligned_ARM9_references=[dict(offset=offset,pointer=pointer)],
        following16_hex=arm[at+len(old):at+len(old)+16].hex())
    OUT.mkdir()
    clean_id = OUT/'clean_ARM9_identity.json'
    from dk4tool.patch.grand_race_menu_release import sha
    save(clean_id, dict(source_ARM9_sha256=sha(clean), source_name_ledger=str(LABELS), source_name_ledger_sha256=digest(LABELS)))
    proposal = dict(format='dk4-owned-name-fields-proposal-v2', runtime=receipt, fields=[row], clean_name_fields=str(clean_id), new_credit=0)
    _, proof = plan_arm9_name_fields(arm, proposal, clean)
    assert proof['complete_parent_inverse_exact'] and proof['changed_bytes'] == 1
    save(OUT/'proposal.json', proposal)
    save(OUT/'qualification.json', proof)
    adapter = checked_text(inspect.getsource(names), {'for ident in [2,4,13,23,109]:': 'for ident in ACTORS:'})
    save(OUT/'current_getters.json', dict(runtime=receipt,
         current_names=dict(rows=binding['current_consumers']), source_owned_current_adapter=adapter))
    print('Zaganos Bey fits the exclusive original surname field. Only one ARM9 byte changes.')


if __name__ == '__main__':
    main()
