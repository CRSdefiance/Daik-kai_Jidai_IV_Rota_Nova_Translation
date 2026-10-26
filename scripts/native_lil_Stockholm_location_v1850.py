"""Three explicit town fixtures, each owning only16 coherent coordinate bytes."""
import struct
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.native_lil_Bruges_location_v1754 import REQUEST as BRUGES
from scripts.native_lil_Amsterdam_location_v1833c import apply_fixture as previous, REQUEST as AMSTERDAM
from scripts.native_lil_Bruges_location_v1752c import source_bound_terrain
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_village_wrap_v608 import save

ROOT=Path('work/analysis/lil_Stockholm_location_v1850')
REQUEST={'Lil_Stockholm_approach':'coherent_location_only'}
BASE=0x02000000

def apply_fixture(arm,raw,request):
    if request in (BRUGES,AMSTERDAM):return previous(arm,raw,request)
    assert request==REQUEST and len(raw)==0x400000
    assert sha(arm)=='500b7d6cea559d7252ae4e67f94540e67739428823a17cf26842b6827712a41e'
    clean=NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    ranges=[(0x78C60,0x78E80),(0xB566C,0xB5688),(0xB521C,0xB5230),(0x69B5C,0x69E00)]
    assert all(arm[a:b]==clean[a:b]for a,b in ranges)
    cpu,get=get_machine(arm,raw)
    assert get(0x2E58C)==get(0x7F244)==2
    fleet=get(0xCB1A8)+4+2*132
    assert get(0x34674,fleet)==115
    town=get(0xCB178)+4+7*108
    out=0x02640000
    get(0xB566C,out,town)
    top=list(struct.unpack('<2i',cpu.mem_read(out,8)))
    assert top==[22032,3376] and get(0xB521C,town)==1 and get(0xB50D8,town)==0
    center=[v+24 for v in top]
    offsets=sorted([(dx,dy)for dx in range(-40,41,8)for dy in range(-40,41,8)if dx*dx+dy*dy<=40**2],key=lambda xy:(xy[0]**2+xy[1]**2,xy))
    points=[[center[0]+dx,center[1]+dy]for dx,dy in offsets]
    terrain=source_bound_terrain(arm,points)
    target=next(r['map_point']for r in terrain['queries']if r['collision_free'])
    owned=set(range(fleet+0x34,fleet+0x3C));after=bytearray(raw);mobiles=[]
    struct.pack_into('<2i',after,fleet+0x34-BASE,*target)
    for slot in range(5):
        mobile=get(0x36C70,fleet+12+slot*8)
        if not mobile:continue
        assert struct.unpack('<I',cpu.mem_read(mobile,4))[0]==0x02143A80
        owned.update(range(mobile+16,mobile+24))
        prior=list(struct.unpack('<2i',cpu.mem_read(mobile+16,8)))
        struct.pack_into('<2i',after,mobile+16-BASE,*[v*128 for v in target])
        mobiles.append({'slot':slot,'mobile':mobile,'prior_fixed_point':prior,'target_fixed_point':[v*128 for v in target]})
    assert len(mobiles)==1 and len(owned)==16
    after=bytes(after)
    changes=[{'address':BASE+i,'before':a,'after':b}for i,(a,b)in enumerate(zip(raw,after,strict=True))if a!=b]
    assert all(r['address']in owned for r in changes)
    check,query=get_machine(arm,after)
    assert query(0x34674,fleet)==115 and query(0xB50D8,town)==0
    assert bytes(check.mem_read(BASE,0x400000))==after
    assert sum((a-b)**2 for a,b in zip(center,target,strict=True))<=40**2
    return after,{'fixture':'Lil_location_only_Stockholm_water_approach','owned_bytes':sorted(owned),'changes':changes,
        'fleet':fleet,'mobiles':mobiles,'target_map_point':target,'original_town_top_left':top,'native_center':center,
        'source_water_queries':terrain,'original_town7_known_flag0_preserved_native_discovery_and_docking_required':True,
        'original_town_sentinel115_unchanged':True,'all_other4MiB_exact':True,
        'only16_mobile_and_coherent_cached_coordinate_bytes_owned':True,
        'no_event_RNG_health_inventory_actor_message_or_outcome_ownership':True,
        'no_earned_travel_claim_normal_docking_and_event_activation_required':True,
        'before_RAM_sha256':sha(raw),'after_RAM_sha256':sha(after),'fixture_sha256':sha(Path(__file__).read_bytes())}

if __name__=='__main__':
    assert not ROOT.exists()
    raw=Path('E:/Rota Nova translations/Generated/work/emulation_v193/lil_B24_research_run_v1831_RESEARCH_ONLY/frame_043120_arm9_ram.bin').read_bytes()
    arm=NdsImage.open('out/all_routes_combined_v1807_candidate.nds').read_file('/__arm9__.bin')
    after,proof=apply_fixture(arm,raw,REQUEST)
    ROOT.mkdir(parents=True);save(ROOT/'coordinate_only_preflight.json',proof)
    print({'owned_bytes':len(proof['owned_bytes']),'target':proof['target_map_point'],'native_town7_discovery_still_required':True},flush=True)
