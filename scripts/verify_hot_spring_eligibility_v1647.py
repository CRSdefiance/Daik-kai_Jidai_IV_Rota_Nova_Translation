"""Read-only actual Search-point/land checks,including ordinary failed searches."""
import struct
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/hot_spring_eligibility_v1647')
CAP=Path('E:/Rota Nova translations/Generated/work/emulation_v193/hot_spring_notice_resilient_v1645_1637')
if __name__=='__main__':
    assert not ROOT.exists()
    arm=NdsImage.open('out/all_routes_combined_v1637_candidate.nds').read_file('/__arm9__.bin');clean=NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    assert arm[0x699F0:0x69B5C]==clean[0x699F0:0x69B5C] and arm[0x79E20:0x79E98]==clean[0x79E20:0x79E98]
    rows=[]
    for frame in [14500,21400,24400,25451]:
        path=CAP/f'frame_{frame:06d}_arm9_ram.bin';raw=path.read_bytes();main=0x18CF80
        assert struct.unpack_from('<I',raw,main+0xAC)[0]==0x0207B190
        scene=struct.unpack_from('<I',raw,main)[0];point=struct.unpack_from('<2i',raw,main+0x14)
        assert point==struct.unpack_from('<2i',raw,main+0x2C)==(33500,5464)
        cpu,get=get_machine(arm,raw);pointer=0x02470000;cpu.mem_write(pointer,struct.pack('<2i',*point))
        land=get(0x699F0,scene+0x44,pointer);region=get(0x797A0,pointer);assert (land,region)==(1,2)
        rows.append({'frame':frame,'RAM':str(path),'RAM_sha256':sha(raw),'Search_main_SP':0x02000000+main,
            'actual_Search_input_and_cached_point':list(point),'original_scene':scene,'original_Search_adjacent_land':land,'original_region':region})
    ROOT.mkdir(parents=True);save(ROOT/'actual_Search_point_land_and_region_verified.json',{'records':rows,
        'both_event_and_no_event_holds_use_exact_intended_eligible_shore':True,
        'no_evidence_that_location_drift_or_missing_land_prevents_the_optional_branch':True,
        'read_only_CPU_queries_no_state_or_cache_writes_back_to_live_game':True,'no_RNG_or_event_forcing':True,
        'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    print('Four actual Search states prove exact33500/5464,original land1,region2. Failed searches are eligible;no drift/cache fix indicated,no live writes.')
