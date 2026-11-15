"""Independently audit every declared live fixture in the terminal contact pilot."""
from pathlib import Path
import struct
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.native_contact_live_geometry_v1062 import apply_fixture
from scripts.native_ranged_staffing_v1050b import water
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_village_wrap_v608 import read,save

BASE=0x02000000
ROOT=Path('work/analysis/contact_pilot_v1081')
CAP=Path('E:/Rota Nova translations/Generated/work/emulation_v193/reinforcement_sniping_v1063_1034_regional')
ROM=Path('out/all_routes_combined_v1034_candidate.nds')


def main():
    assert not ROOT.exists()
    report_path=CAP/'capture_report.json';report=read(report_path)
    assert report['frames']==10344 and report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
    assert not report['goal_complete'] and not report['hardware_device_verification']
    assert sha(ROM.read_bytes())==report['ROM_sha256']
    assert read('work/analysis/reinforcement_sniping_v1063/terminal_preservation.json')['source_and_disposable_donors_unchanged']
    rom=NdsImage.open(ROM);arm=rom.read_file('/__arm9__.bin')
    clean=NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    for lo,hi in ((0x7E154,0x7E1A4),(0x737C8,0x74010),(0x36A24,0x36A68),(0x519D4,0x51A28),(0xD9824,0xD9868)):
        assert arm[lo:hi]==clean[lo:hi]
    snapshots={}
    for r in report['read_only_capture_RAM_snapshots']+report['read_only_pause_RAM_snapshots']:
        if r['frame'] in snapshots:assert r['sha256']==snapshots[r['frame']]['sha256']
        snapshots[r['frame']]=r
    fixtures=report['synthetic_battle_recovery_proximity_fixtures'];assert len(fixtures)==1351
    seed,flag=[struct.unpack_from('<I',arm,n)[0] for n in (0xD9858,0x51A20)]
    results=[];points=set()
    for index,receipt in enumerate(fixtures):
        source=snapshots[receipt['frame']];raw=Path(source['path']).read_bytes()
        assert len(raw)==source['bytes']==0x400000 and sha(raw)==source['sha256']==receipt['before_RAM_sha256']
        if receipt['context']!='trainHealthyContact':
            after,proof=apply_fixture(arm,raw,{'reinforcement_context':receipt['context']})
            assert receipt=={**proof,'frame':receipt['frame']}
        else:
            cpu,get=get_machine(arm,raw);root=get(0xCB1A8)
            own,enemy=[root+4+n*132 for n in (1,8)]
            assert get(0x7F244)==get(0x2E58C)==1 and get(0x35320,own)==2 and get(0x35320,enemy)==8
            m,e=[get(0x36C70,f+12) for f in (own,enemy)];model=get(0xAB158,m)
            captain,opponent=get(0x65EEC),get(0x3697C,enemy)
            assert captain==get(0xCB184)+0x19E4 and opponent==get(0xCB184)+4+32*32
            hp=[get(0x7E19C,a) for a in (captain,opponent)]
            assert all(h>0 for h in hp) and hp==receipt['own_and_enemy_captain_HP_before']
            live=[[get(0x5543C,v),get(0x55444,v)] for v in (m,e)]
            assert live==receipt['prior_live_Hull_Crew'] and all(0<v<=b for row,bounds in zip(live,((60,124),(60,163)),strict=True) for v,b in zip(row,bounds,strict=True))
            vt=struct.unpack('<I',cpu.mem_read(e,4))[0];getter=struct.unpack('<I',cpu.mem_read(vt+0x5C,4))[0]
            assert getter==0x02036A24
            scratch=0x02470000;get(getter-BASE,scratch,e);point=struct.unpack('<2i',cpu.mem_read(scratch,8))
            points.add(point)
            fields={captain+24:struct.pack('<H',144),opponent+24:struct.pack('<H',10),
                own+0x34:struct.pack('<2i',*point),m+16:bytes(cpu.mem_read(e+16,8)),
                m+24:struct.pack('<2H',60,124),e+24:struct.pack('<2H',60,163),
                model+0x3E:struct.pack('<2H',144,142)}
            assert {str(k):v.hex() for k,v in fields.items()}==receipt['declared_fields']
            owned={a for at,data in fields.items() for a in range(at,at+len(data))}
            assert len(owned)==32 and owned==set(receipt['owned_bytes'])
            assert get(0x82478,root+0x2090,7)==16 and get(0x8235C,root+0x2090,7,6,0)>150
            after=bytearray(raw)
            for at,data in fields.items():after[at-BASE:at-BASE+len(data)]=data
            after=bytes(after)
            # Compute the entire independent delta,not merely the listed fields.
            changes=[{'address':BASE+i,'before':a,'after':b} for i,(a,b) in enumerate(zip(raw,after,strict=True)) if a!=b]
            assert changes==receipt['changes']
            assert e+13 not in owned and after[e-BASE+13]==raw[e-BASE+13]
        assert sha(after)==receipt['after_RAM_sha256']
        for at in (seed,flag):assert raw[at-BASE:at-BASE+4]==after[at-BASE:at-BASE+4]
        results.append({'frame':receipt['frame'],'context':receipt['context'],'owned_byte_count':len(receipt['owned_bytes']),
            'entire4MiB_delta_and_after_hash_independently_reconstructed':True,'RNG_seed_and_initialization_flag_exact':True})
        if (index+1)%100==0:print(index+1,'complete declared contact-fixture deltas pass',flush=True)
    terrain=water(arm,[list(p) for p in sorted(points)])
    assert len(terrain['queries'])==len(points) and all(r['collision_free'] for r in terrain['queries'])
    ROOT.mkdir(parents=True)
    save(ROOT/'terminal_pilot_verification.json',{'candidate':str(ROM),'candidate_sha256':report['ROM_sha256'],
        'terminal_report':str(report_path),'terminal_report_sha256':sha(report_path.read_bytes()),'terminal_frame':10344,
        'fixture_replays':results,'complete_fixture_count':len(results),'distinct_contact_points_native_water_rechecked':len(points),
        'terrain':terrain,'all_original_shot_selector_RNG_and_outcome_code_unchanged':True,
        'all_positive_HP_live_vessel_constraints_and_actual_captain_actor_IDs_pass':True,
        'enemy_result_byte_never_owned_or_overridden':True,'both_live_vessel_health_and_positive_captain_HP_are_explicit_synthetic_test_state':True,
        'two_original_enemy_ship_capture_notices_and_monthly_report_prompt_observed':True,
        'monthly_report_normal_No_then_normal_scene_return_before_terminal_stop':True,
        'successful_admiral_shot_not_observed_at_recorded_pauses_no_event_credit':True,
        'no_earned_battle_progression_or_whole_route_hardware_claim':True,
        'original_and_disposable_donors_unchanged':True,'no_editorial_completion_credit':True,
        'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    print('Terminal contact pilot audit passes;successful-shot event remains unverified. No editorial completion credit.',flush=True)


if __name__=='__main__':main()
