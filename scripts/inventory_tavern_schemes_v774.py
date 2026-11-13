"""Clean/current neighboring entries and numeric caller leads for Tavern schemes."""

import struct
from dataclasses import asdict
from pathlib import Path

from capstone import Cs,CS_ARCH_ARM,CS_MODE_ARM
from capstone.arm import ARM_OP_IMM,ARM_OP_MEM,ARM_REG_PC

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from scripts.verify_village_wrap_v608 import save

ROOT=Path('work/analysis/tavern_schemes_editorial_v774')
CURRENT=Path('out/all_routes_combined_v773_candidate.nds')


def main():
    ROOT.mkdir(parents=True,exist_ok=True)
    paths=[Path('work/clean.nds'),Path('out/raphael_natural_v2_accepted_base.nds'),CURRENT]
    roms=[NdsImage.open(p) for p in paths]
    arms=[r.read_file('/__arm9__.bin') for r in roms];commons=[r.read_file('/COMMON/MESFILE.DK4') for r in roms]
    entries=[common_message_entries(c,a,clean=i==0) for i,(c,a) in enumerate(zip(commons,arms))]
    rows=[]
    for n in range(904,966):
        original,canonical,current=[e[n] for e in entries]
        refs=[]
        for e in(original,current):
            row=asdict(e);row['text']=None;refs.append(row)
        rows.append({'id':n,'source_hex':original.text.hex(),'Japanese':original.text.decode('cp932'),
            'canonical_hex':canonical.text.hex(),'current_hex':current.text.hex(),'current_English':current.text.decode('cp932'),
            'source_reference':refs[0],'current_reference':refs[1]})
    pins=[{'path':str(p),'ROM_sha256':sha(p.read_bytes()),'ARM9_sha256':sha(a),'COMMON_sha256':sha(c)} for p,a,c in zip(paths,arms,commons)]
    save(ROOT/'source_and_neighbors.json',{'pins':pins,'rows':rows,'caller_context_not_inferred_from_adjacency':True})
    cs=Cs(CS_ARCH_ARM,CS_MODE_ARM);cs.detail=True;cs.skipdata=True
    refs={n:{'aligned_words':[],'instruction_leads':[]} for n in range(908,959)}
    for at in range(0,0x170000,4):
        value=struct.unpack_from('<I',arms[0],at)[0]
        if value in refs:refs[value]['aligned_words'].append(0x02000000+at)
    for inst in cs.disasm(arms[0][0x50000:0x70000],0x02050000):
        if not inst.id:continue
        values=[]
        if inst.mnemonic not in('b','bl','blx'):values += [o.imm for o in inst.operands if o.type==ARM_OP_IMM]
        if inst.mnemonic.startswith('ldr') and len(inst.operands)>1:
            op=inst.operands[1]
            if op.type==ARM_OP_MEM and op.mem.base==ARM_REG_PC:
                at=inst.address+8+op.mem.disp-0x02000000
                if 0<=at<len(arms[0])-4:values.append(struct.unpack_from('<I',arms[0],at)[0])
        for value in values:
            if value in refs:refs[value]['instruction_leads'].append({'pc':inst.address,'instruction':inst.mnemonic+' '+inst.op_str})
    save(ROOT/'caller_leads_NOT_CONTEXT.json',{'messages':refs,'scope':'Numeric/table leads only;actual caller,arguments,voice tables and control branches still require mapping.'})
    for row in rows:
        if 908<=row['id']<=958:print(row['id'],repr(row['Japanese']),repr(row['current_English']),flush=True)


if __name__=='__main__':main()
