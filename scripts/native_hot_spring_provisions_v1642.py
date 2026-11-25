"""User-authorized test provisions through the original supply assignment method."""
import struct
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts import native_hot_spring_notice_location_v1640 as location
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_village_wrap_v608 import read,save
ROM=location.ROM
ROOT=Path('work/analysis/hot_spring_provisions_v1642')
REQUEST={'testing_provisions':'balanced_original_capacity'}

def apply_fixture(arm,raw,request):
    if request!=REQUEST:return location.apply_fixture(arm,raw,request)
    assert len(raw)==0x400000 and sha(arm)==read('translations/hot_spring_notice_editorial_release_v1.json')['target_arm9_sha256']
    clean=NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    for lo,hi in [(0x34E60,0x34F6C),(0x60518,0x60664)]:assert arm[lo:hi]==clean[lo:hi]
    cpu,get=get_machine(arm,raw);fleet=get(0xCB1A8)+4+132*get(0x2E58C)
    assert get(0x2E58C)==get(0x7F244)==1
    assert struct.unpack('<3I',cpu.mem_read(get(0x3F0F8)+8,12))==(0,0,0)
    pointer=0x02450000;get(0x34EB0,fleet,pointer);before=struct.unpack('<2I',cpu.mem_read(pointer,8));capacity=get(0x34E60,fleet)
    assert capacity==700 and 0<before[1]<100
    owned=set();models=[]
    for slot in range(5):
        model=get(0x36C94,fleet+12+slot*8);mobile=get(0x36C70,fleet+12+slot*8)
        assert model and mobile and get(0x564C8,mobile)
        health=[get(0x5543C,mobile),get(0x55444,mobile)];assert health==([60,49] if slot==0 else [25,19])
        models.append({'slot':slot,'model':model,'mobile':mobile,'Hull_Crew_preserved':health,'original_water_food':list(struct.unpack('<2H',cpu.mem_read(model+0x3E,4)))})
        owned.update(range(model+0x3E,model+0x42))
    target=(capacity//2,capacity-capacity//2)
    get(0x60518,0,*target);get(0x34EB0,fleet,pointer);after_totals=struct.unpack('<2I',cpu.mem_read(pointer,8));assert after_totals==target
    after=bytes(cpu.mem_read(0x02000000,0x400000));changes=[{'address':0x02000000+i,'before':a,'after':b} for i,(a,b) in enumerate(zip(raw,after,strict=True)) if a!=b]
    assert len(owned)==20 and changes and all(c['address'] in owned for c in changes)
    return after,{'context':'user_authorized_artificial_test_provisions_original_supply_setter','owned_bytes':sorted(owned),'changes':changes,
        'fleet':fleet,'models':models,'original_native_assignment':0x02060518,'original_totals_getter':0x02034EB0,
        'source_HUD_bound_order':'water,food;source getters show418,63 at original20700 HUD','before_water_food':list(before),'after_water_food':list(after_totals),
        'original_capacity':capacity,'only_original_five_model_water_food_fields_owned':True,
        'all_other4MiB_bytes_including_positions_health_fatigue_actor_skills_RNG_and_event_choices_exact':True,
        'no_earned_resupply_or_discovery_claim':True,'no_actor_skill_RNG_event_or_outcome_edit':True,
        'before_RAM_sha256':sha(raw),'after_RAM_sha256':sha(after),'fixture_sha256':sha(Path(__file__).read_bytes())}

if __name__=='__main__':
    assert not ROOT.exists()
    raw=Path('E:/Rota Nova translations/Generated/work/emulation_v193/hot_spring_notice_live_v1641_1637/frame_020700_arm9_ram.bin').read_bytes()
    after,proof=apply_fixture(NdsImage.open(ROM).read_file('/__arm9__.bin'),raw,REQUEST);ROOT.mkdir(parents=True);save(ROOT/'preflight.json',proof)
    print('Original provision setter preflight:20 resource bytes only,418/63 to350/350;all other4MiB including skills/RNG/outcomes exact. Artificial refill,user-authorized.')
