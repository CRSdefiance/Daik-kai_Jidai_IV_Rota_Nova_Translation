"""Use original known-town docking center, not the separate port spawn point."""
import inspect
import struct
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts import native_lil_Bruges_location_v1752 as original_fixture
from scripts.native_lil_Bruges_location_v1752c import source_bound_terrain
from scripts.prepare_lil_lessons_research_v1739 import ROM
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_village_wrap_v608 import save

ROOT=Path('work/analysis/lil_Bruges_location_v1754')
REQUEST=original_fixture.REQUEST

def apply_fixture(arm,raw,request):
    clean=NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    ranges=[(0x78C60,0x78E80),(0xB566C,0xB5688),(0xB521C,0xB5230),(0x655B8,0x65620),
            (0x69B5C,0x69E00),(0xCB1A8,0xCB1B4),(0x2E58C,0x2E598),
            (0x36C70,0x36C94),(0x2C1C4,0x2C204),(0x34674,0x3468C),(0xCD6B8,0xCD6CC)]
    assert all(arm[a:b]==clean[a:b] for a,b in ranges)
    cpu,get=get_machine(arm,raw)
    town=get(0xCB178)+4+3*108
    vt=struct.unpack('<I',cpu.mem_read(town,4))[0]
    position_getter=struct.unpack('<I',cpu.mem_read(vt+0x20,4))[0]
    assert position_getter==0x020B566C
    out=0x02640000;get(position_getter-0x02000000,out,town)
    top_left=list(struct.unpack('<2i',cpu.mem_read(out,8)))
    assert top_left==[20224,4320] and get(0xB521C,town)==0
    assert get(0xB50D8,town)!=0
    center=[v+16 for v in top_left]
    points=[[center[0]+dx,center[1]+dy] for dx,dy in [(0,-24),(-24,0),(24,0),(0,-16),(-16,-16),(16,-16)]]
    source=inspect.getsource(original_fixture.apply_fixture)
    anchor="reference=NdsImage.open('out/all_routes_combined_v604_candidate.nds').read_file('/__arm9__.bin')"
    assert source.count(anchor)==1
    source=source.replace(anchor,'reference=arm')
    old="points=[[port[0]+dx,port[1]+dy] for dx,dy in [(0,-16),(-16,0),(16,0),(0,16),(-12,-12),(12,-12)]]"
    assert source.count(old)==1
    source=source.replace(old,'points=SOURCE_DOCKING_POINTS')
    source=source.replace('terrain=terrain_queries(reference,points)','terrain=source_bound_terrain(arm,points)')
    env={**original_fixture.__dict__,'__file__':__file__,
         'SOURCE_DOCKING_POINTS':points,'source_bound_terrain':source_bound_terrain}
    exec(compile(source,__file__,'exec'),env)
    after,proof=env['apply_fixture'](arm,raw,request)
    check,query=get_machine(arm,after)
    detected=query(0x78C60,1)
    assert detected==3
    assert bytes(check.mem_read(0x02000000,0x400000))==after
    target=proof['target_map_point']
    assert sum((a-b)**2 for a,b in zip(target,center,strict=True))<=32**2
    proof.update(original_source_getter_and_docking_ranges=ranges,original_town_position_getter=position_getter,
        original_town_top_left=top_left,original_native_town_center=center,
        original_known_town_scan_returns_Bruges3_without_any_state_edit=True,
        original_scan_keeps_all_input4MiB_exact=True,
        earlier_spawn_point_based_north16_target_outside_real_town_radius={'target':[20248,4296],
            'distance_squared':1664,'original_radius_squared':1024},
        actual_docking_and_category5_entry_still_pending=True)
    return after,proof

if __name__=='__main__':
    assert not ROOT.exists()
    raw=Path('E:/Rota Nova translations/Generated/work/emulation_v193/lil_crew_lesson_v1753_RESEARCH_ONLY/frame_030651_arm9_ram.bin').read_bytes()
    after,proof=apply_fixture(NdsImage.open(ROM).read_file('/__arm9__.bin'),raw,REQUEST)
    ROOT.mkdir(parents=True);save(ROOT/'source_docking_center_and_location_preflight.json',proof)
    print({'target':proof['target_map_point'],'native_known_town_scan':3,'owned_bytes':len(proof['owned_bytes'])})
