"""Authorized coherent location-only approach; original docking/events remain native."""
import struct
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.prepare_lil_lessons_research_v1739 import ROM
from scripts.native_village_contexts_v618 import terrain_queries
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_village_wrap_v608 import read, save

ROOT=Path('work/analysis/lil_Bruges_location_v1752')
REQUEST={'Lil_Bruges_approach':'coherent_location_only'}
ARM='500b7d6cea559d7252ae4e67f94540e67739428823a17cf26842b6827712a41e'

def apply_fixture(arm,raw,request):
    assert request==REQUEST and sha(arm)==ARM and len(raw)==0x400000
    cpu,get=get_machine(arm,raw)
    assert get(0x2E58C)==get(0x7F244)==2
    fleet=get(0xCB1A8)+4+2*132
    assert get(0x34674,fleet)==0x73
    city=get(0xCD6B8,3); name=struct.unpack('<I',cpu.mem_read(city,4))[0]
    assert bytes(cpu.mem_read(name,32)).split(b'\0')[0]==b'Bruges'
    port=list(struct.unpack('<2i',cpu.mem_read(city+12,8)))
    assert port==[20248,4312]
    points=[[port[0]+dx,port[1]+dy] for dx,dy in [(0,-16),(-16,0),(16,0),(0,16),(-12,-12),(12,-12)]]
    reference=NdsImage.open('out/all_routes_combined_v604_candidate.nds').read_file('/__arm9__.bin')
    assert arm[0x69B5C:0x69E00]==reference[0x69B5C:0x69E00]
    assert NdsImage.open(ROM).read_file('/data/WORLDMAP.DK4')==NdsImage.open('work/clean.nds').read_file('/data/WORLDMAP.DK4')
    terrain=terrain_queries(reference,points)
    target=next(r['map_point'] for r in terrain['queries'] if r['collision_free'])
    owned=set(); changes=[]; mobiles=[]; after=bytearray(raw)
    for slot in range(5):
        mobile=get(0x36C70,fleet+12+8*slot)
        if not mobile: continue
        assert struct.unpack('<I',cpu.mem_read(mobile,4))[0]==0x02143A80
        at=mobile+16; owned.update(range(at,at+8))
        prior=list(struct.unpack('<2i',cpu.mem_read(at,8)))
        struct.pack_into('<2i',after,at-0x02000000,*[v*128 for v in target])
        mobiles.append({'slot':slot,'mobile':mobile,'prior_fixed_point':prior,'target_fixed_point':[v*128 for v in target]})
    assert len(mobiles)==1
    vt=struct.unpack('<I',cpu.mem_read(fleet,4))[0]
    getter=struct.unpack('<I',cpu.mem_read(vt+0x20,4))[0]; assert getter==0x0202C1C4
    out=0x02640000; get(getter-0x02000000,out,fleet)
    prior_cache=list(struct.unpack('<2i',cpu.mem_read(out,8)))
    at=fleet+0x34; owned.update(range(at,at+8)); struct.pack_into('<2i',after,at-0x02000000,*target)
    assert len(owned)==16
    after=bytes(after)
    changes=[{'address':0x02000000+i,'before':a,'after':b} for i,(a,b) in enumerate(zip(raw,after,strict=True)) if a!=b]
    assert all(c['address'] in owned for c in changes)
    check,query=get_machine(arm,after); query(getter-0x02000000,out,fleet)
    assert list(struct.unpack('<2i',check.mem_read(out,8)))==target and query(0x34674,fleet)==0x73
    return after, {'fixture':'Lil_location_only_Bruges_water_approach','owned_bytes':sorted(owned),'changes':changes,
        'fleet':fleet,'mobiles':mobiles,'original_cached_point':prior_cache,'target_map_point':target,
        'original_port_town3_point':port,'original_terrain_queries':terrain,
        'only16_mobile_and_coherent_cached_coordinate_bytes_owned':True,
        'all_other4MiB_including_town_event_flags_health_inventory_RNG_and_outcomes_exact':True,
        'original_town_sentinel_115_unchanged':True,'original_docking_and_category5_event_must_run':True,
        'no_earned_travel_discovery_or_event_claim':True,'before_RAM_sha256':sha(raw),'after_RAM_sha256':sha(after),
        'fixture_sha256':sha(Path(__file__).read_bytes())}

if __name__=='__main__':
    assert not ROOT.exists()
    raw=Path('E:/Rota Nova translations/Generated/work/emulation_v193/lil_lesson_navigation_v1745_RESEARCH_ONLY/frame_030230_arm9_ram.bin').read_bytes()
    after,proof=apply_fixture(NdsImage.open(ROM).read_file('/__arm9__.bin'),raw,REQUEST)
    ROOT.mkdir(parents=True); save(ROOT/'location_only_preflight.json',proof)
    print({'owned_bytes':len(proof['owned_bytes']),'changed_bytes':len(proof['changes']),'target':proof['target_map_point']})
