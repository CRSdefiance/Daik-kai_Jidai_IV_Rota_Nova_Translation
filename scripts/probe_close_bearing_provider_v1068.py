"""Equal-allocation close-bearing research; no playable ROM or completed gate."""
import struct
from pathlib import Path
from ndspy.code import loadOverlayTable
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_village_wrap_v608 import read,save

BASE=0x02000000
ROOT=Path('work/analysis/sighting_provider_v1068')
ROM=Path('out/all_routes_combined_v1034_candidate.nds')


def references(data,base,target):
    arm=[];thumb=[];absolute=[]
    for at in range(0,len(data)-3):
        word=struct.unpack_from('<I',data,at)[0]
        if word==target:absolute.append(base+at)
        if (base+at)%4==0 and word>>24==0xEB:
            d=word&0xFFFFFF
            if d&0x800000:d-=1<<24
            if base+at+8+d*4==target:arm.append(base+at)
        if (base+at)%2==0:
            hi,lo=struct.unpack_from('<2H',data,at)
            if hi&0xF800==0xF000 and lo&0xF800==0xE800:
                d=((hi&0x7FF)<<12)|((lo&0x7FF)<<1)
                if d&(1<<22):d-=1<<23
                if ((base+at+4+d)&~3)==target:thumb.append(base+at)
    return {'ARM_BL':arm,'Thumb_BLX_immediate_candidates':thumb,'absolute_address_occurrences':absolute}


def main():
    assert not ROOT.exists()
    context=read('work/analysis/sighting_editorial_v1065/source_context_packet.json')
    supplement=read('work/analysis/sighting_editorial_v1066/attacked_family_and_provider_supplement.json')
    rom=NdsImage.open(ROM);arm=rom.read_file('/__arm9__.bin')
    assert sha(ROM.read_bytes())==context['candidate_sha256']
    field=context['original_bearing_getter_cases'][0];at=field['argument_address']-BASE
    old=bytes.fromhex(field['hex'])+b'\0';new=b'vicinity\0'
    assert arm[at:at+9]==old and len(old)==len(new)==9
    research=arm[:at]+new+arm[at+9:]
    assert len(research)==len(arm) and research[:at]==arm[:at] and research[at+9:]==arm[at+9:]
    raw=Path(context['source_snapshot']).read_bytes();assert sha(raw)==context['source_snapshot_sha256']
    patched=raw[:at]+new+raw[at+9:]
    source_cpu,get_source=get_machine(arm,raw);target_cpu,get_target=get_machine(research,patched)
    cases=[]
    for x in (-100,-10,-2,-1,0,1,2,10,100):
        for y in (-100,-10,-2,-1,0,1,2,10,100):
            args=(x&0xFFFFFFFF,y&0xFFFFFFFF)
            before=get_source(0x6567C,*args);after=get_target(0x6567C,*args)
            a=bytes(source_cpu.mem_read(before,64)).split(b'\0')[0]
            b=bytes(target_cpu.mem_read(after,64)).split(b'\0')[0]
            assert before==after and b==(b'vicinity' if a==old[:-1] else a)
            cases.append({'relative_vector':[x,y],'pointer':before,'source_hex':a.hex(),'research_hex':b.hex(),
                'original_getter_ABI_and_compass_values_preserved':True})
    assert any(c['research_hex']==b'vicinity'.hex() for c in cases)
    scans=[{'section':'ARM9','base':BASE,'bytes':len(arm),'sha256':sha(arm),**references(arm,BASE,BASE+0x6567C)}]
    for oid,overlay in loadOverlayTable(rom.rom.arm9OverlayTable,lambda oid,fid:rom.rom.files[fid]).items():
        data=bytes(overlay.data)
        scans.append({'section':f'ARM9 overlay{oid}','base':overlay.ramAddress,'bytes':len(data),'sha256':sha(data),
            **references(data,overlay.ramAddress,BASE+0x6567C)})
    assert scans[0]['ARM_BL']==[0x020778A8,0x02077B9C]
    assert not any(s['absolute_address_occurrences'] or s['Thumb_BLX_immediate_candidates'] for s in scans)
    assert not any(s['ARM_BL'] for s in scans[1:])
    ROOT.mkdir(parents=True)
    path=ROOT/'ARM9_PROVIDER_RESEARCH_ONLY.bin';path.write_bytes(research)
    save(ROOT/'provider_native_proof.json',{'candidate':str(ROM),'candidate_sha256':sha(ROM.read_bytes()),
        'source_ARM9_sha256':sha(arm),'research_ARM9':str(path),'research_ARM9_sha256':sha(research),
        'source_field_address':field['argument_address'],'owned_allocation_bytes':9,'source_hex':old.hex(),'research_hex':new.hex(),
        'all81_original_getter_ABI_cases':cases,'all_native_code_reference_scans':scans,
        'all_discovered_two_direct_ARM9_callers_bound_to_the_reviewed_sighting_families':True,
        'no_absolute_function_pointer_or_Thumb_BLX_or_overlay_caller_found':True,
        'source_literal_argument_pointer_and_all_native_instructions_unchanged':True,
        'no_section_pool_cache_arena_or_payload_growth':True,'no_ROM_patch_or_live_RAM_change':True,
        'full_common_substitution_wrap_fonts_registered_copy_integration_and_actual_display_pending':True,
        'completed_entries_added':0,'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    print('81 original bearing-getter cases and all ARM9/overlay call-reference scans pass;9-byte research replacement only. No ROM built.',flush=True)


if __name__=='__main__':main()
