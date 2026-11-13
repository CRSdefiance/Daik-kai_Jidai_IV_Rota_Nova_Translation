"""Source-owned constant tails,exact UI strings and unchanged memory geometry."""

import re
import struct
from pathlib import Path

from ndspy.code import MainCodeFile

from dk4tool.patch import tavern_coordinate_runtime as previous
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.main_pool_cache_visibility import cache_plan
from dk4tool.patch.region_name_boundaries import LABELS,START,END,TABLE
from dk4tool.rom.nds import NdsImage
from scripts.inventory_shipyard_storage_v760 import units
from scripts.tavern_continuation_runtime_v769 import *
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/tavern_runtime_v769')
CURRENT=Path('out/all_routes_combined_v767_candidate.nds')


def main():
    rom=NdsImage.open(CURRENT);arm=rom.read_file('/__arm9__.bin')
    clean=NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    assert sha(arm)==SOURCE
    candidates=read(ROOT/'padded_allocation_leads_small_NOT_FREE.json')
    rows=[]
    for lo,hi in TAILS:
        lead=dict(next(r for r in candidates if r['lo']==lo and r['hi']>=hi))
        lead['hi']=hi;lead['bytes']=hi-lo
        at=lead['original_string_offset'];end=arm.index(0,at)
        assert BASE+end<lo
        assert set(arm[lo-BASE:hi-BASE]) <= {0}
        assert any(clean[at:at+len(bytes.fromhex(r['original_source_hex']))]==bytes.fromhex(r['original_source_hex']) for r in lead['lead_sources']),hex(lo)
        lead['preserved_active_prefix_hex']=arm[at:end+1].hex()
        rows.append(lead)
    for lo,hi,label in ((UNWIND,UNWIND+8,'prior owned40-byte type helper unused tail'),
            (BRIDGE,BRIDGE+8,'retired village answer23'),(NORTH,NORTH+16,'retired village answer15')):
        rows.append({'lo':lo,'hi':hi,'bytes':hi-lo,'id':label})
    all_units=units(rom)+[('ARM7',rom.rom.arm7RamAddress,bytes(rom.rom.arm7))]
    for row in rows:row.update({'aliases':[],'branches':[],'adr':[],'crossing_strings':[]})
    region_aliases=[]
    for name,base,raw in all_units:
        for m in re.finditer(rb'(?=(...\x02))',raw,re.DOTALL):
            target=int.from_bytes(m.group(1),'little')
            if BASE+START<=target<BASE+END:region_aliases.append([name,base+m.start(),target])
            for row in rows:
                if row['lo']<=target<row['hi']:row['aliases'].append([name,base+m.start(),target])
            if not BASE+0x130000<=target<0x02171E48:continue
            end=arm.find(b'\0',target-BASE,min(len(arm),target-BASE+1024))
            if end<0:continue
            affected=[r for r in rows if target<r['lo']<=BASE+end]
            if not affected:continue
            try:
                text=arm[target-BASE:end].decode('cp932')
                textual=bool(text) and all(ord(c)>=32 or c in '\r\n\t' for c in text)
            except UnicodeError:textual=False
            if textual:
                for row in affected:row['crossing_strings'].append([name,base+m.start(),target,BASE+end+1])
        for at in range(0,len(raw)-3,4):
            word=struct.unpack_from('<I',raw,at)[0]
            if word&0x0E000000==0x0A000000:
                delta=word&0xffffff
                if delta&0x800000:delta-=0x1000000
                target=base+at+8+4*delta
                for row in rows:
                    if row['lo']<=target<row['hi']:row['branches'].append([name,base+at,target])
            if word&0x0E0F0000==0x020F0000 and (word>>21)&15 in (2,4):
                v,shift=word&255,((word>>8)&15)*2
                v=((v>>shift)|(v<<(32-shift)))&0xffffffff if shift else v
                target=base+at+8+(v if (word>>21)&15==4 else -v)
                for row in rows:
                    if row['lo']<=target<row['hi']:row['adr'].append([name,base+at,target])
    save(ROOT/'current_tail_census.json',rows)
    assert all(not row[k] for row in rows for k in ('aliases','branches','adr','crossing_strings')),[(hex(r['lo']),{k:r[k] for k in ('aliases','branches','adr','crossing_strings') if r[k]}) for r in rows if any(r[k] for k in ('aliases','branches','adr','crossing_strings'))]
    assert sorted((name,at) for name,at,_ in region_aliases)==[('section0',BASE+TABLE+i*52) for i in range(8)]
    # The excluded interior Load prompt pointer at169F48 is precisely outside
    # the narrowed12-byte tail. Never overwrite its word or subsequent bytes.
    assert struct.unpack_from('<I',arm,0xEE678)[0]==0x02169F48
    assert (REGION,REGION+12) in TAILS and REGION+12==0x02169F48
    original=previous.assemble()
    for at in (GATE,GIFT,old.TYPE_HELPER):
        assert arm[at-BASE:at-BASE+len(original[at])]==original[at]
    blobs=assemble(arm);target=bytearray(arm);patches=[]
    for at,blob in blobs.items():
        assert not any(at<b and a<at+len(blob) for a,b in [(p['address'],p['address']+p['bytes']) for p in patches])
        target[at-BASE:at-BASE+len(blob)]=blob
        patches.append({'address':at,'bytes':len(blob),'source_hex':arm[at-BASE:at-BASE+len(blob)].hex(),'target_hex':blob.hex()})
    target=bytes(target)
    for row in rows:
        if 'preserved_active_prefix_hex' in row:
            at=row['original_string_offset'];prefix=bytes.fromhex(row['preserved_active_prefix_hex'])
            assert target[at:at+len(prefix)]==prefix
    assert target[0x169F48:0x169F4C]==arm[0x169F48:0x169F4C]
    assert target[END:END+28]==arm[END:END+28]
    shared={AFRICA:b'Africa',SOUTHEAST:b'Southeast Asia',EAST:b'East Asia',NEW_WORLD:b'the New World'}
    for at,text in shared.items():assert arm[at-BASE:at-BASE+len(text)+1]==text+b'\0'
    for i,text in enumerate(LABELS):
        field=TABLE+i*52;pointer=struct.unpack_from('<I',target,field)[0]
        assert target[pointer-BASE:target.index(0,pointer-BASE)]==text.encode('ascii')
        assert target[field+4:field+52]==arm[field+4:field+52]
    code1,code2=[MainCodeFile(a,BASE) for a in (arm,target)]
    assert [(s.ramAddress,len(s.data),s.bssSize) for s in code1.sections]==[(s.ramAddress,len(s.data),s.bssSize) for s in code2.sections]
    assert all(bytes(a.data)==bytes(b.data) for a,b in zip(code1.sections[1:],code2.sections[1:],strict=True))
    assert cache_plan(arm)==cache_plan(target) and len(arm)==len(target)
    # Validate the four intentionally changed source instructions against clean.
    ks=Ks(KS_ARCH_ARM,KS_MODE_ARM)
    for at in (0x020582BC,0x02059968):assert arm[at-BASE:at-BASE+4]==bytes(ks.asm('bl 0x020945b4',at)[0])
    for at,instruction in ((0x02058070,'mov r2,r0'),(0x02058078,'mov r3,r6')):
        assert arm[at-BASE:at-BASE+4]==clean[at-BASE:at-BASE+4]==bytes(ks.asm(instruction,at)[0])
    save(ROOT/'owned_runtime_plan.json',{'source_ROM_sha256':sha(CURRENT.read_bytes()),'source_ARM9_sha256':sha(arm),
        'target_ARM9_sha256':sha(target),'documented_source_tails_and_retired_spans':rows,
        'region_source_aliases_exact8_owner_fields':region_aliases,'borrowed_immutable_complete_strings':{hex(a):v.decode() for a,v in shared.items()},
        'all_active_prefixes_and_all8_short_UI_names_and_geometry_exact':True,
        'all_selected_tails_have_zero_absolute_branch_ADR_crossing_string_references':True,
        'Load_prompt_interior_alias169F48_and_unused_Online_intro_tail_excluded':True,
        'all_section_sizes_autoload_ITCM_pool_cache_geometry_preserved':True,
        'patches':patches,'runtime_module_sha256':sha(Path('scripts/tavern_continuation_runtime_v769.py').read_bytes()),
        'producer_sha256':sha(Path(__file__).read_bytes()),'no_playable_ROM_or_gameplay_approval':True})
    (ROOT/'ARM9_RESEARCH_ONLY.bin').write_bytes(target)
    print(f'{len(rows)} source-owned spans,all8 unchanged UI labels,and{len(patches)} exact patches;no growth or ROM emitted.',flush=True)


if __name__=='__main__':main()
