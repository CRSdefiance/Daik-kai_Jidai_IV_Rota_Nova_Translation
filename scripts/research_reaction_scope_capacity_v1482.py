"""Check four proven actor scopes inside existing selector bytes;no ROM mutation."""
from pathlib import Path
from scripts import ship_loss_surrender_runtime_v1442b as previous
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/battle_reaction_scope_capacity_v1482')
NEW_KEYS=(0x7F40,0x7F80,0x8000,0x8060)

def contract_rows():
    rows=[];found=False
    for parent,offset,high,keys in previous.contract_rows():
        if parent==0x02053F40:
            assert high==0x0211 and offset==0x274 and not set(keys)&set(NEW_KEYS)
            keys=tuple(sorted((*keys,*NEW_KEYS)));found=True
        rows.append((parent,offset,high,keys))
    assert found
    return rows

if __name__=='__main__':
    assert not ROOT.exists()
    rows=contract_rows();codec=previous.previous.codec
    encoded=previous.rebased(codec.encode,rows)
    decoded,end=previous.rebased(codec.decode,encoded)
    assert rows==decoded and end==len(encoded)<=188
    arm=NdsImage.open('out/all_routes_combined_v1456_candidate.nds').read_file('/__arm9__.bin')
    assert arm[previous.CONTRACTS-0x02000000:previous.CONTRACTS-0x02000000+188]==previous.table()
    gate,assembly=previous.gate()
    assert len(gate)==172 and arm[previous.GATE-0x02000000:previous.GATE-0x02000000+172]==gate
    specials={842-780,905-780,906-780,1028-780,1029-780}
    for parent,offset,high,keys in rows:
        if high:
            shift=4 if parent==0x02053C14 else 5
            assert not {(k>>shift)-896 for k in keys}&specials
    ROOT.mkdir(parents=True)
    save(ROOT/'scope_capacity.json',{'source_ARM9_sha256':sha(arm),'new_contracts':rows,
        'new_actor_tables':[0x02110000+k for k in NEW_KEYS],'old_encoded_bytes':180,
        'new_encoded_bytes':len(encoded),'owned_selector_bytes':188,'new_encoded_hex':encoded.hex(),
        'original172_byte_gate_exact_no_code_change_proposed':True,
        'all_prior_memberships_and_special_numeric_routes_preserved_by_encoding':True,
        'full_native_dispatch_ABI_wrong_parent_and_memory_regressions_still_required':True,
        'no_RAM_ROM_registry_or_completion_change':True,'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    print('Four new actor scopes fit:',len(encoded),'/188 selector bytes;existing172-byte gate exact. Full native regression still pending.')
