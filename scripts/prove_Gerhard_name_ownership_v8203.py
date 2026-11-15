"""Bound the current12-byte surname,not the original20-byte slot nowshared withBlades."""
import struct
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/Gerhard_name_ownership_v8203')
PRIOR=Path('work/analysis/editorial_handoff_verification_v8195/verified_handoff.json')
BATCH=Path('translations/hodram_gerhard_nameplate_arm9_v1.json')
if __name__=='__main__':
    assert not ROOT.exists();prior=read(PRIOR);image=NdsImage.open(prior['candidate']);arm=image.read_file('/__arm9__.bin')
    assert sha(Path(prior['candidate']).read_bytes())==prior['candidate_sha256']
    record=read(BATCH)['records'][0];slot=record['offset'];original_size=len(bytes.fromhex(record['source_hex']))
    assert original_size==20 and slot==1435252
    raw=arm[slot:slot+original_size];old=b'Ardelknatts\0';assert raw.startswith(old) and len(old)==12 and raw[12:]==b'Blades\0\0'
    proposed=b'Adernkatz\0'+bytes(12-len(b'Adernkatz\0'));assert len(proposed)==12
    refs=[]
    for relative in range(20):
        pointer=0x02000000+slot+relative;needle=struct.pack('<I',pointer);at=arm.find(needle)
        while at>=0:
            refs.append(dict(pointer_field_offset=at,target_pointer=pointer,target_relative_to_name=relative,field_bytes=needle.hex()));at=arm.find(needle,at+1)
    name_refs=[r for r in refs if r['target_relative_to_name']==0]
    interior=[r for r in refs if 0<r['target_relative_to_name']<12]
    neighbor=[r for r in refs if r['target_relative_to_name']>=12]
    assert any(r['pointer_field_offset']==1183108 for r in name_refs) and not interior and neighbor
    assert all(r['target_relative_to_name']==12 for r in neighbor)
    changed=bytearray(arm);changed[slot:slot+12]=proposed
    assert changed[:slot]==arm[:slot] and changed[slot+12:]==arm[slot+12:] and changed[slot+12:slot+20]==b'Blades\0\0'
    restored=bytearray(changed);restored[slot:slot+12]=old;assert restored==arm
    ROOT.mkdir(parents=True);save(ROOT/'current12_byte_surname_owned_original20_contains_protected_Blades.json',dict(
        candidate=prior['candidate'],candidate_sha256=prior['candidate_sha256'],ARM9_sha256=sha(arm),source_batch=str(BATCH),source_batch_sha256=sha(BATCH.read_bytes()),
        actor_ID=16,original_source_slot=dict(offset=slot,bytes=20,clean_source_hex=record['source_hex']),
        current_owned_name_span=dict(offset=slot,bytes=12,current_hex=old.hex(),target_hex=proposed.hex()),
        protected_neighbor=dict(offset=slot+12,bytes=8,current_hex=raw[12:].hex(),text='Blades',no_write_allowed=True),
        current_literal_pointer_references=name_refs,interior_name_literal_pointer_references=interior,protected_neighbor_literal_pointer_references=neighbor,
        current_complete_ARM9_pointer_census_not_arbitrary_dynamic_pointer_proof=True,
        proposed_ARM9_sha256=sha(bytes(changed)),whole_ARM9_inverse_recovers_exact_current=True,
        all_bytes_outside_current12_byte_span_andall_pointer_fields_preserved=True,
        no_global_original20_byte_padding_ownership_assumed=True,
        actual_patch_not_applied_new_ROM_registered_release_getters_fonts_andactual_checks_pending=True,
        preserved_failure_producer='scripts/review_Gerhard_surname_v8202.py',failure='Assumed original20-byte slot remained zero-filled after surname. Current exact bytes contain separately referenced Blades after byte12;assertion stopped before any output mutation.',
        new_credit=0,new_emulator_runs=0,full_goal_complete=False,
        evidence={str(p):sha(p.read_bytes()) for p in [PRIOR,BATCH,Path(__file__)]}))
    print('Currentname12bytes;protectedBlades8bytes.Namepointers',name_refs,'neighborpointers',neighbor,'interioraliases',interior,'exact proposed inverse pass.No ROMchanged.')
