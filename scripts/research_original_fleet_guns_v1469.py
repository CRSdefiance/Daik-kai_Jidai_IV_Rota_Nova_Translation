"""Read-only original fleet census to choose a feasible combat scene test."""
import struct
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/original_fleet_guns_v1469')
ROM=Path('out/all_routes_combined_v1456_candidate.nds')
CAP=Path('E:/Rota Nova translations/Generated/work/emulation_v193/loss_surrender_control_v1461b_1456')
BASE=0x02000000

def main():
    assert not ROOT.exists()
    report=read(CAP/'capture_report.json')
    assert sha(ROM.read_bytes())==report['ROM_sha256']
    snapshot=next(r for r in report['read_only_pause_RAM_snapshots'] if r['frame']==4800)
    raw=Path(snapshot['path']).read_bytes();assert sha(raw)==snapshot['sha256']
    arm=NdsImage.open(ROM).read_file('/__arm9__.bin')
    clean=NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    spans=[(0x34674,0x34680),(0x35320,0x3532C),(0x36C70,0x36CB8),
           (0x1856C,0x18574),(0x183A0,0x183A8),(0x181BC,0x181C4),
           (0xAB784,0xAB7AC)]
    assert all(arm[a:b]==clean[a:b] for a,b in spans)
    cpu,get=get_machine(arm,raw);root=get(0xCB1A8)
    fleets=[]
    for identity in range(63):
        fleet=root+4+132*identity;ships=[]
        for slot in range(5):
            model=get(0x36C94,fleet+12+8*slot)
            if not model: continue
            mobile=get(0x36C70,fleet+12+8*slot)
            kind=get(0x1856C,model)
            name=bytes(cpu.mem_read(model+8,24)).split(b'\0')[0]
            ships.append({'slot':slot,'model':model,'mobile':mobile,'name_hex':name.hex(),
                'name':name.decode('cp932',errors='backslashreplace'),
                'original_cannon_type':kind,'native_strength':get(0xAB784,kind),
                'stored_Hull_Crew':[get(0x183A0,model),get(0x181BC,model)]})
        if not ships: continue
        vt=struct.unpack('<I',cpu.mem_read(fleet,4))[0]
        method=struct.unpack('<I',cpu.mem_read(vt+0x20,4))[0]
        get(method-BASE,0x02460000,fleet)
        point=list(struct.unpack('<2i',cpu.mem_read(0x02460000,8)))
        fleets.append({'fleet':identity,'company':get(0x35320,fleet),
            'town_or_sea':get(0x34674,fleet),'cached_map_point':point,'ships':ships})
    candidates=[f for f in fleets if f['town_or_sea']==115 and f['fleet']!=1
        and any(s['native_strength']>=2 for s in f['ships'])]
    ROOT.mkdir(parents=True)
    save(ROOT/'original_fleet_census.json',{'candidate':str(ROM),'candidate_sha256':sha(ROM.read_bytes()),
        'source_snapshot':snapshot,'fleets':fleets,'stronger_original_fleets_at_sea':candidates,
        'original_getter_spans':spans,'no_live_RAM_ROM_enemy_equipment_health_RNG_or_result_mutation':True,
        'cached_positions_are_not_proven_actual_loaded_positions':True,
        'no_original_event_or_editorial_completion_credit':True,
        'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    print('Populated fleets:',len(fleets),'stronger original fleets at sea:',len(candidates))
    for f in candidates:
        print(f['fleet'],f['company'],f['cached_map_point'],[(s['slot'],s['name'],s['original_cannon_type'],s['stored_Hull_Crew']) for s in f['ships']])

if __name__=='__main__':main()
