"""Read-only original region/shore predicates for a natural recovery-event fixture."""
import inspect,struct
from pathlib import Path
from types import FunctionType
from collections import Counter
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.native_village_contexts_v618 import terrain_queries as original_terrain
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/fatigue_shore_context_v1587c')
ROM=Path('out/all_routes_combined_v1578_candidate.nds')
if __name__=='__main__':
    assert not ROOT.exists()
    rom=NdsImage.open(ROM);arm=rom.read_file('/__arm9__.bin');clean=NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    assert arm[0x797A0:0x79958]==clean[0x797A0:0x79958] and arm[0x699F0:0x69B5C]==clean[0x699F0:0x69B5C]
    snapshot=Path('E:/Rota Nova translations/Generated/work/emulation_v193/fatigue_search_pilot_v1587b_1578/frame_005300_arm9_ram.bin');raw=snapshot.read_bytes()
    cpu,get=get_machine(arm,raw);pointer=0x02470000;counts=Counter();candidates=[]
    for y in range(500,20000,500):
        for x in range(500,40000,500):
            cpu.mem_write(pointer,struct.pack('<2i',x,y));region=get(0x797A0,pointer);counts[region]+=1
            if region in [2,3]:candidates.append([x,y])
    source=inspect.getsource(original_terrain)
    old="        rows.append({'map_point': list(point), 'native_collision_result': result, 'collision_free': result == 0})"
    new="""        call(u,0x699F0,(0x02468000,0x02460100))
        search_land=u.reg_read(UC_ARM_REG_R0)
        call(u,0x797A0,(0x02460100,))
        region=u.reg_read(UC_ARM_REG_R0)
        rows.append({'map_point':list(point),'native_collision_result':result,'collision_free':result==0,'original_search_has_adjacent_land':bool(search_land),'original_event_region':region})"""
    assert source.count(old)==1;source=source.replace(old,new)
    class Current:
        @staticmethod
        def open(path):return NdsImage.open(ROM if path=='out/all_routes_combined_v604_candidate.nds' else path)
    env={**original_terrain.__globals__,'NdsImage':Current};exec(compile(source,__file__,'exec'),env)
    coarse=env['terrain_queries'](arm,candidates)
    land=[q for q in coarse['queries'] if not q['collision_free']]
    assert land
    # Coarse source-owned land anchor,then refine to legal water touching native Search land.
    anchor=land[0]['map_point']
    points=[[anchor[0]+dx,anchor[1]+dy] for dy in range(-512,513,16) for dx in range(-512,513,16)]
    refined=env['terrain_queries'](arm,points)
    shores=[q for q in refined['queries'] if q['collision_free'] and q['original_search_has_adjacent_land'] and q['original_event_region'] in [2,3]]
    assert shores
    chosen=min(shores,key=lambda q:sum((a-b)**2 for a,b in zip(q['map_point'],anchor)))
    ROOT.mkdir(parents=True);save(ROOT/'original_region_land_and_legal_shore_queries.json',{'candidate':str(ROM),'candidate_sha256':sha(ROM.read_bytes()),'source_snapshot':str(snapshot),'source_snapshot_sha256':sha(raw),
        'original_region_grid_counts':dict(counts),'coarse':coarse,'land_anchor':anchor,'refined':refined,'chosen_shore':chosen,
        'only_readonly_CPU_source_queries_no_fixture_or_event_yet':True,'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    print('Original region counts',dict(counts),'land anchor',anchor,'legal Search shore',chosen,'No location/event/RNG edit performed.')
