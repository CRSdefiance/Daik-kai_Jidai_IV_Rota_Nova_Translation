"""Prove selected private banks/tails and preserve all memory geometry."""

import re
import struct
from pathlib import Path

from capstone import CS_ARCH_ARM,CS_MODE_THUMB,Cs
from ndspy.code import MainCodeFile

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.main_pool_cache_visibility import cache_plan
from dk4tool.rom.nds import NdsImage
from scripts import recruitment_owned_runtime_v772 as runtime
from scripts.context_tavern_recruitment_v771 import CURRENT
from scripts.inventory_shipyard_storage_v760 import units
from scripts.probe_button_prompt_native import BASE
from scripts.verify_recruitment_owned_v772 import ROOT,quantity_closure
from scripts.verify_village_wrap_v608 import read,save


def main():
    ROOT.mkdir(parents=True,exist_ok=True)
    rom=NdsImage.open(CURRENT);arm=rom.read_file('/__arm9__.bin')
    clean=NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    assert sha(CURRENT.read_bytes())=='eb170a31525470658180db3bd9e0d0ae07a8cffadba5002975bf8cc97cfe0f1f'
    quantity_closure(rom)
    reports=[Path(n) for n in ('work/analysis/shipyard_storage_v760/owned_source_storage.json',
        'work/analysis/tavern_coordinates_v766/owned_runtime_plan.json','work/analysis/tavern_runtime_v769/owned_runtime_plan.json')]
    yard,tavern,continuation=map(read,reports)
    owned=yard['owned_banks']+tavern['immutable_banks']
    owned += [[r['lo'],r['hi']] for r in continuation['documented_source_tails_and_retired_spans']]
    private=[(0x02131F48,0x02132004),(0x02132020,0x02132044),(0x021478E0,0x021478E8),
        (0x0214797C,0x02147A24),(0x02147B70,0x02147B80),
        (0x02147C20,0x02147C70),(0x02147D28,0x02147D54),(0x02147E54,0x02147F00),
        (0x02156078,0x02156080),(0x02169F78,0x02169F84),(0x0216A010,0x0216A01C),
        (0x0216A05C,0x0216A068),(0x0216A0B0,0x0216A0C8),(0x0216A074,0x0216A07C)]
    assert all(any(a<=lo<hi<=b for a,b in owned) for lo,hi in private)
    tails=[];candidates=read('work/analysis/tavern_runtime_v769/padded_allocation_leads_small_NOT_FREE.json')
    for at,length in ((0x0216DCE8,10),(0x0216DE68,9),(0x02131E90,7),(0x02131ED4,6)):
        lead=next(r for r in candidates if r['lo']<=at<at+length<=r['hi'])
        source=lead['original_string_offset'];end=arm.index(0,source)
        assert BASE+end<at and set(arm[at-BASE:at-BASE+length])<={0}
        assert any(clean[source:source+len(bytes.fromhex(r['original_source_hex']))]==bytes.fromhex(r['original_source_hex']) for r in lead['lead_sources'])
        tails.append({'lo':at,'hi':at+length,'source_lead':lead,'preserved_prefix_offset':source,
            'preserved_prefix_hex':arm[source:end+1].hex()})
    all_spans=private+[(r['lo'],r['hi']) for r in tails]
    def affected(target):return any(lo<=target<hi for lo,hi in all_spans)
    def internal(pc):return any(lo<=pc<hi for lo,hi in private)
    references={'absolute':[],'ARM_branch':[],'ADR':[],'Thumb_BL_BLX':[],
        'known_private_Thumb_branch_and_literal_targets':[],'crossing_Cstrings':[]}
    rejected=[]
    cs=Cs(CS_ARCH_ARM,CS_MODE_THUMB)
    for name,base,raw in units(rom)+[('ARM7',rom.rom.arm7RamAddress,bytes(rom.rom.arm7))]:
        for m in re.finditer(rb'(?=(...\x02))',raw,re.DOTALL):
            target=int.from_bytes(m.group(1),'little');pc=base+m.start()
            if affected(target):
                references['absolute'].append([name,pc,target])
                if not internal(pc):rejected.append(['absolute',name,pc,target])
            if BASE+0x130000<=target<0x02171E48 and not internal(pc):
                end=arm.find(b'\0',target-BASE,min(len(arm),target-BASE+1024))
                crossing=[(lo,hi) for lo,hi in all_spans if target<lo<=BASE+end]
                if end<0 or not crossing:continue
                try:text=arm[target-BASE:end].decode('cp932')
                except UnicodeError:continue
                if text and all(ord(c)>=32 or c in '\r\n\t' for c in text):
                    row=[name,pc,target,BASE+end+1];references['crossing_Cstrings'].append(row);rejected.append(['crossing',*row])
        for at in range(0,len(raw)-3,4):
            word=struct.unpack_from('<I',raw,at)[0];pc=base+at;target=None;kind=None
            if word&0x0E000000==0x0A000000:
                delta=word&0xffffff
                if delta&0x800000:delta-=0x1000000
                target=pc+8+delta*4;kind='ARM_branch'
            elif word&0x0E0F0000==0x020F0000 and (word>>21)&15 in(2,4):
                v,shift=word&255,((word>>8)&15)*2
                v=((v>>shift)|(v<<(32-shift)))&0xffffffff if shift else v
                target=pc+8+(v if (word>>21)&15==4 else -v);kind='ADR'
            if target is None or not affected(target):continue
            references[kind].append([name,pc,target])
            allowed=internal(pc) or kind=='ARM_branch' and (pc==0x01FFCF3C or
                any(pc==v[1] for v in read(ROOT/'quantity_caller_closure.json')['exact_seven_ARM_BLs']))
            if not allowed:rejected.append([kind,name,pc,target])
        for at in range(0,len(raw)-3,2):
            first,second=struct.unpack_from('<HH',raw,at)
            if first&0xF800!=0xF000 or second&0xF800 not in(0xE800,0xF800):continue
            inst=next(cs.disasm(raw[at:at+4],base+at),None)
            if inst is None or inst.mnemonic not in('bl','blx') or not inst.op_str.startswith('#'):continue
            target=int(inst.op_str[1:],0)&~1
            if affected(target):
                references['Thumb_BL_BLX'].append([name,base+at,target])
                if not internal(base+at):rejected.append(['Thumb_BL_BLX',name,base+at,target])
    # V770's injected Thumb code has known exact assembler extents. Preserve
    # source-private branch/ADR/literal provenance,including the retired bridge.
    for lo,hi in ((0x02147AE4,0x02147B70),(0x02147D28,0x02147D54),(0x021478E0,0x021478E2)):
        for inst in cs.disasm(arm[lo-BASE:hi-BASE],lo):
            target=None
            if inst.mnemonic.startswith('b') and inst.op_str.startswith('#'):target=int(inst.op_str[1:],0)&~1
            elif inst.mnemonic=='adr' and ', #' in inst.op_str:target=int(inst.op_str.split('#')[-1],0)
            elif inst.mnemonic=='ldr' and '[pc,' in inst.op_str:
                delta=int(inst.op_str.split('#')[-1].split(']')[0],0)
                target=((inst.address+4)&~3)+delta
            if target is not None and affected(target):
                references['known_private_Thumb_branch_and_literal_targets'].append([inst.address,target,inst.mnemonic])
                if not internal(inst.address):rejected.append(['private_Thumb',inst.address,target,inst.mnemonic])
    save(ROOT/'storage_reference_census.json',{'private_spans':private,'new_source_tails':tails,
        'references':references,'unexpected_references':rejected})
    assert not rejected,rejected
    code=MainCodeFile(arm,BASE);before=[bytes(s.data) for s in code.sections];patches=[]
    for at,blob in runtime.assemble().items():
        index=4 if at<BASE else 0;section=code.sections[index];offset=at-section.ramAddress
        if at>=BASE:assert any(lo<=at<at+len(blob)<=hi for lo,hi in all_spans),hex(at)
        old=bytes(section.data[offset:offset+len(blob)]);assert len(old)==len(blob)
        section.data[offset:offset+len(blob)]=blob
        patches.append({'address':at,'section':index,'source_hex':old.hex(),'target_hex':blob.hex()})
    target=bytes(code.save());after=MainCodeFile(target,BASE)
    assert len(target)==len(arm) and cache_plan(target)==cache_plan(arm)
    assert [(s.ramAddress,len(s.data),s.bssSize) for s in code.sections]==[(s.ramAddress,len(s.data),s.bssSize) for s in after.sections]
    assert all(bytes(after.sections[i].data)==before[i] for i in(1,2,3))
    for i,section in enumerate(after.sections):
        restored=bytearray(section.data)
        for row in patches:
            if row['section']==i:
                offset=row['address']-section.ramAddress;raw=bytes.fromhex(row['source_hex']);restored[offset:offset+len(raw)]=raw
        assert bytes(restored)==before[i]
    for row in tails:
        at=row['preserved_prefix_offset'];raw=bytes.fromhex(row['preserved_prefix_hex']);assert target[at:at+len(raw)]==raw
    proof={'source_ROM_sha256':sha(CURRENT.read_bytes()),'source_ARM9_sha256':sha(arm),'target_ARM9_sha256':sha(target),
        'private_spans':private,'four_documented_zero_tails':tails,'patches':patches,
        'prior_source_ownership_reports':{str(p):sha(p.read_bytes()) for p in reports},
        'current_reference_census_sha256':sha((ROOT/'storage_reference_census.json').read_bytes()),
        'exact_seven_quantity_callers_verified':True,'all_section_pool_cache_BSS_geometry_preserved':True,
        'runtime_source_sha256':sha(Path(runtime.__file__).read_bytes()),
        'quantity_source_sha256':sha(Path('scripts/recruitment_quantity_v772.py').read_bytes()),
        'producer_sha256':sha(Path(__file__).read_bytes()),'registered_ROM_patch_and_gameplay_pending':True,'full_goal_complete':False}
    save(ROOT/'owned_runtime_plan.json',proof);(ROOT/'ARM9_RESEARCH_ONLY.bin').write_bytes(target)
    print(f'{len(private)} private allocations,four source tails,{len(patches)} patches;geometry exact. No playable ROM.',flush=True)


if __name__=='__main__':main()
