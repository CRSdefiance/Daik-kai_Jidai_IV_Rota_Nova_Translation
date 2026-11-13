"""Use original registration for an existing Monster Fish near unchanged player ships."""
import struct
from pathlib import Path
from types import FunctionType
from capstone import Cs,CS_ARCH_ARM,CS_MODE_ARM
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts import native_ship_sinking_fixture_v1351 as terrain
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_village_wrap_v608 import read,save
ROM=Path('out/all_routes_combined_v1578_candidate.nds')
ROOT=Path('work/analysis/inspection_status_no_lookout_fixture_v1581b')
BASE=0x02000000
REQUEST={'sea_inspection_context':'register_original_Monster_Fish'}

def apply_fixture(arm,raw,request):
    assert request==REQUEST and len(raw)==0x400000
    assert sha(arm)==read('work/analysis/inspection_status_release_v1577/registered_release_verification.json')['ARM9_sha256']
    clean=NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    spans=[(0x2D1CC,0x2D268),(0x363E8,0x3648C),(0x557C8,0x55828),(0x56290,0x5636C),
        (0x56104,0x56224),(0x519D4,0x51A18),(0x348D4,0x34914),(0x36BE8,0x36C00)]
    assert all(arm[a:b]==clean[a:b] for a,b in spans)
    cpu,get=get_machine(arm,raw)
    fleets,models,world=get(0xCB1A8),get(0xCB148),get(0xCB19C)
    fleet=fleets+4+39*132;own=fleets+4+132;model=models+4+149*140
    assert get(0x2E58C)==get(0x7F244)==1 and get(0x36C94,fleet+12)==model
    assert not get(0x36C70,fleet+12) and get(0x34674,fleet)==0 and get(0x35320,fleet)==21
    assert bytes(cpu.mem_read(fleets+0x2084,1))==b'@'
    ownmobiles=[get(0x36C70,own+12+8*i) for i in range(5)]
    assert all(ownmobiles)
    ownpoint=[x//128 for x in struct.unpack('<2i',cpu.mem_read(ownmobiles[0]+16,8))]
    candidates=[[ownpoint[0]+dx,ownpoint[1]+dy] for dx,dy in [(40,0),(-40,0),(0,40),(0,-40)]]
    water=FunctionType(terrain.water.__code__,{**terrain.water.__globals__,'ROM':ROM})
    checked=water(arm,candidates)
    chosen=next(q['map_point'] for q in checked['queries'] if q['collision_free'])
    beforemodel=bytes(cpu.mem_read(model,140))
    # The only direct location write is the existing target fleet's cached point.
    cpu.mem_write(fleet+0x34,struct.pack('<2i',*chosen))
    rng=[]
    from unicorn import UC_HOOK_CODE
    def watch(uc,at,size,data):
        if at==BASE+0x519D4:rng.append(at)
    hook=cpu.hook_add(UC_HOOK_CODE,watch,begin=BASE+0x519D4,end=BASE+0x519D4)
    result=get(0x2D1CC,fleets,1,39,1)
    cpu.hook_del(hook)
    assert result==1 and get(0x34674,fleet)==115
    mobile=get(0x36C70,fleet+12)
    assert mobile==world+4+5*28 and get(0x564C8,mobile)
    assert get(0xAB128,mobile)==34
    assert bytes(cpu.mem_read(model,140))==beforemodel
    after=bytes(cpu.mem_read(BASE,len(raw)))
    # Original registration owns party1,link0's mobile index,mobile5 and its RNG state.
    regions=[('target_cached_position',fleet+0x34,8),('original_availability_flag',fleet+0x50,1),
        ('original_link_mobile_index',fleet+12+5,1),('original_party1',fleets+0x2084,4),
        ('original_mobile5',mobile,28),('original_RNG_state',0x02168EB8,4)]
    owned={at+i for label,at,n in regions for i in range(n)}
    changes=[{'address':BASE+i,'before':a,'after':b} for i,(a,b) in enumerate(zip(raw,after,strict=True)) if a!=b]
    assert all(r['address'] in owned for r in changes)
    assert all(after[m-BASE:m-BASE+28]==raw[m-BASE:m-BASE+28] for m in ownmobiles)
    return after,{'context':'original_registered_Monster_Fish_inspection','owned_bytes':sorted(owned),'changes':changes,
        'declared_regions':[{'label':label,'address':at,'bytes':n,'before_hex':raw[at-BASE:at-BASE+n].hex(),'after_hex':after[at-BASE:at-BASE+n].hex()} for label,at,n in regions],
        'original_registration_entry':BASE+0x2D1CC,'original_registration_arguments':[fleets,1,39,1],
        'original_registration_result':result,'original_RNG_calls':rng,'no_RNG_value_or_combat_outcome_forced':True,
        'original_existing_fleet_ID':39,'original_existing_model_ID':149,'original_class_ID':34,'original_company_ID':21,
        'stored_model_Hull_Crew':[get(0x183A0,model),get(0x181BC,model)],
        'original_initialized_mobile_Hull_Crew':[get(0x5543C,mobile),get(0x55444,mobile)],
        'own_five_mobile_objects_positions_health_and_equipment_exact':True,
        'source_own_point':ownpoint,'target_point':chosen,'terrain':checked,
        'all_other4MiB_bytes_exact':True,'original_source_code_spans':spans,
        'artificial_location_and_registration_not_an_earned_or_natural_spawn':True,
        'no_message_ID_renderer_target_type_actor_identity_or_result_injected':True,
        'before_RAM_sha256':sha(raw),'after_RAM_sha256':sha(after),'fixture_sha256':sha(Path(__file__).read_bytes())}

if __name__=='__main__':
    assert not ROOT.exists()
    raw=Path('E:/Rota Nova translations/Generated/work/emulation_v193/declaration_responses_v1546_1542/frame_004800_arm9_ram.bin').read_bytes()
    arm=NdsImage.open(ROM).read_file('/__arm9__.bin')
    after,proof=apply_fixture(arm,raw,REQUEST)
    ROOT.mkdir(parents=True);save(ROOT/'preflight.json',proof)
    md=Cs(CS_ARCH_ARM,CS_MODE_ARM)
    save(ROOT/'source_registration_code.json',[{'span':[BASE+a,BASE+b],'sha256':sha(arm[a:b]),'instructions':[{'address':i.address,'mnemonic':i.mnemonic,'operands':i.op_str} for i in md.disasm(arm[a:b],BASE+a)]} for a,b in proof['original_source_code_spans']])
    print('Original registration preflight:regions',len(proof['owned_bytes']),'changed',len(proof['changes']),'point',proof['target_point'],'original RNG calls',len(proof['original_RNG_calls']),'mobile stats',proof['original_initialized_mobile_Hull_Crew'])
