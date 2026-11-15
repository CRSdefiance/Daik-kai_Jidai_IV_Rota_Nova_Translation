"""Revalidate references to the existing private table and gate on V773."""

import re
import struct
from pathlib import Path

from capstone import Cs,CS_ARCH_ARM,CS_MODE_THUMB

from dk4tool.patch import recruitment_editorial_runtime as old
from dk4tool.patch import tavern_schemes_runtime as new
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.inventory_shipyard_storage_v760 import units
from scripts.verify_scheme_input_contract_v776 import ROOT
from scripts.verify_village_wrap_v608 import read,save


def main():
    rom=NdsImage.open('out/all_routes_combined_v773_candidate.nds')
    arm=rom.read_file('/__arm9__.bin')
    assert sha(arm)==new.SOURCE
    gate=old.assemble()[old.GATE]
    table=old.assemble()[old.CONTRACTS]
    assert len(gate)==144 and len(table)==128
    assert arm[old.GATE-old.BASE:old.GATE-old.BASE+144]==gate
    assert arm[old.CONTRACTS-old.BASE:old.CONTRACTS-old.BASE+128]==table
    spans=((old.GATE,old.GATE+144),(old.CONTRACTS,old.CONTRACTS+128))
    inside=lambda pc:any(a<=pc<b for a,b in spans)
    affected=lambda pc:any(a<=pc<b for a,b in spans)
    refs=[]
    unexpected=[]
    thumb=Cs(CS_ARCH_ARM,CS_MODE_THUMB)
    for name,base,raw in units(rom):
        for m in re.finditer(rb'(?=(...\x02))',raw,re.S):
            pc=base+m.start();target=int.from_bytes(m.group(1),'little')
            if not affected(target&~1):continue
            row=['absolute',name,pc,target];refs.append(row)
            if not inside(pc) and (pc,target)!=(old.ENTRY+12,old.GATE|1):unexpected.append(row)
        for at in range(0,len(raw)-3,4):
            pc=base+at;word=struct.unpack_from('<I',raw,at)[0];kind=None
            if word&0x0E000000==0x0A000000:
                d=word&0xffffff
                if d&0x800000:d-=0x1000000
                target=pc+8+d*4;kind='ARM_branch'
            elif word&0x0E0F0000==0x020F0000 and (word>>21)&15 in(2,4):
                v,s=word&255,((word>>8)&15)*2
                if s:v=((v>>s)|(v<<(32-s)))&0xffffffff
                target=pc+8+(v if (word>>21)&15==4 else -v);kind='ADR'
            if kind and affected(target):
                row=[kind,name,pc,target];refs.append(row)
                if not inside(pc):unexpected.append(row)
        for at in range(0,len(raw)-3,2):
            a,b=struct.unpack_from('<HH',raw,at)
            if a&0xF800!=0xF000 or b&0xF800 not in(0xE800,0xF800):continue
            inst=next(thumb.disasm(raw[at:at+4],base+at),None)
            if inst is None or inst.mnemonic not in('bl','blx') or not inst.op_str.startswith('#'):continue
            target=int(inst.op_str[1:],0)&~1
            if affected(target):
                row=['Thumb_BL_BLX',name,base+at,target];refs.append(row)
                if not inside(base+at):unexpected.append(row)
    save(ROOT/'current_storage_references.json',{'source_ARM9_sha256':sha(arm),
        'existing_private_spans':spans,'references':refs,'unexpected':unexpected,
        'only_external_entry_is_original_ARM_bridge_literal':True,
        'prior_source_ownership_proof_sha256':sha(Path('work/analysis/recruitment_owned_v772/owned_runtime_plan.json').read_bytes()),
        'producer_sha256':sha(Path(__file__).read_bytes())})
    assert not unexpected,unexpected
    plan=read('work/analysis/tavern_scheme_selector_v775/two_patch_plan.json')
    assert new.code()=={r['address']:bytes.fromhex(r['target_hex']) for r in plan['patches']}
    assert len(new.code()[old.GATE])<=len(gate) and len(new.code()[old.CONTRACTS])<=len(table)
    print('Current private references close to the original bridge/table consumer;production code equals the two-patch plan.',flush=True)


if __name__=='__main__':main()
