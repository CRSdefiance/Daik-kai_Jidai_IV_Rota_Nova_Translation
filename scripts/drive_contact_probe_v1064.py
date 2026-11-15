"""Bounded original contact observation; fully declared live survival fixtures only."""
import argparse
import ctypes as ct
import json
import struct
import time
from pathlib import Path
from PIL import Image
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.reinforcement_sniping_layout_v1024 import compiled
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/reinforcement_sniping_v1064')
CAP=Path('E:/Rota Nova translations/Generated/work/emulation_v193/reinforcement_sniping_v1063_1034_regional')
JOURNAL=Path('work/analysis/reinforcement_sniping_v1063/navigation.jsonl')
ROM=Path('out/all_routes_combined_v1034_candidate.nds')
BASE=0x02000000


def main():
    global ROOT
    parser=argparse.ArgumentParser();parser.add_argument('--pid',type=int,required=True)
    parser.add_argument('--start-frame',type=int,default=6130);parser.add_argument('--cycles',type=int,default=1000)
    a=parser.parse_args();assert 1<=a.cycles<=3000 and 0<a.start_frame<90000
    ROOT=ROOT.with_name(ROOT.name+'_'+str(a.start_frame))
    assert not ROOT.exists();ROOT.mkdir(parents=True)
    kernel=ct.WinDLL('kernel32',use_last_error=True)
    kernel.OpenProcess.argtypes=[ct.c_uint,ct.c_int,ct.c_uint];kernel.OpenProcess.restype=ct.c_void_p
    kernel.GetExitCodeProcess.argtypes=[ct.c_void_p,ct.POINTER(ct.c_uint)];kernel.CloseHandle.argtypes=[ct.c_void_p]
    handle=kernel.OpenProcess(0x1000,0,a.pid);assert handle
    def alive():
        code=ct.c_uint();assert kernel.GetExitCodeProcess(handle,ct.byref(code));return code.value==259
    rom=NdsImage.open(ROM);arm=rom.read_file('/__arm9__.bin');digest=sha(ROM.read_bytes())
    assert digest==read(ROM.with_suffix('.manifest.json'))['candidate_sha256']
    doc=read('translations/reinforcement_sniping_editorial_manuscript_v2.json')
    wanted={compiled(r):r['message_id'] for r in doc['records'] if r['message_id']>=1924}
    from dk4tool.patch.reinforcement_sniping_editorial import current_entries
    auto_dismiss={b"What's happening?!",current_entries(rom.read_file('/COMMON/MESFILE.DK4'),arm)[602].text}
    owner=struct.unpack_from('<I',arm,0x552A0)[0]
    entries=[];frame=a.start_frame;stop='bounded_cycle_limit_reached';success=None
    try:
        for cycle in range(a.cycles+1):
            deadline=time.monotonic()+90;raw_path=CAP/f'frame_{frame:06d}_arm9_ram.bin'
            png=CAP/f'frame_{frame:06d}_navigation.png'
            while True:
                assert alive(),'Original emulator process is terminal;never restart from observation timeout'
                try:
                    if raw_path.stat().st_size==0x400000:
                        raw=raw_path.read_bytes();image=Image.open(png).convert('RGB');image.load()
                        assert len(raw)==0x400000 and image.size==(256,384);break
                except (FileNotFoundError,OSError,AssertionError):pass
                if time.monotonic()>=deadline:raise TimeoutError('Same live process did not reach requested pause;do not restart')
                time.sleep(0.1)
            paper=sum(1 for y in range(298,360,4) for x in range(18,242,4)
                      if (lambda c:c[0]>170 and c[1]>145 and c[0]>c[2]+20)(image.getpixel((x,y))))>450
            template=raw[owner-BASE+0x2030:owner-BASE+0x2130].split(b'\0')[0]
            cpu,get=get_machine(arm,raw);root=get(0xCB1A8)
            context=list(struct.unpack('<3I',cpu.mem_read(get(0x3F0F8)+8,12)))
            state={'cycle':cycle,'frame':frame,'RAM_sha256':sha(raw),'capture_sha256':sha(png.read_bytes()),
                'paper_navigation_heuristic':paper,'source_context':context,
                'native_Lookout_Aim':get(0x8235C,root+0x2090,7,6,0), 'current_template_hex':template.hex(),'actual_event_ID_if_exact_target_template':wanted.get(template)}
            if paper and template in auto_dismiss:
                state['normal_A_dismissal_of_previously_observed_notice']=True;entries.append(state)
                command={'until':frame+20,'buttons':['A'],'duration':8}
                with JOURNAL.open('a',encoding='utf-8') as f:f.write(json.dumps(command)+'\n')
                save(ROOT/'live_observation_journal.json',{'candidate_sha256':digest,'observations':entries,
                    'last_command':command,'emulator_PID':a.pid,'commands_are_not_execution_receipts':True})
                frame+=20;continue
            if paper:
                stop='original_target_shot_modal_observed' if template in wanted else 'other_original_modal_observed'
                if template in wanted:success={'frame':frame,'message_ID':wanted[template]}
                entries.append(state);break
            if context!=[0,1,8]:entries.append(state);stop='original_battle_context_ended';break
            assert get(0x7F244)==get(0x2E58C)==1
            assert state['native_Lookout_Aim']>150
            fleets=[root+4+n*132 for n in (1,8)]
            mobiles=[get(0x36C70,f+12) for f in fleets]
            stats=[]
            for m in mobiles:
                stats.append([get(0x5543C,m),get(0x55444,m)] if m else [0,0])
            state['own_and_opponent_live_Hull_Crew']=stats
            entries.append(state)
            if any(v<=0 for row in stats for v in row):stop='original_vessel_disabled_no_revival';break
            if cycle==a.cycles:break
            command={'until':frame+2,'duration':1,'battle_fixture':{'reinforcement_context':'trainHealthyContact'}}
            with JOURNAL.open('a',encoding='utf-8') as f:f.write(json.dumps(command)+'\n')
            save(ROOT/'live_observation_journal.json',{'candidate_sha256':digest,'observations':entries,
                'last_command':command,'emulator_PID':a.pid,'commands_are_not_execution_receipts':True})
            if cycle%10==0:print('cycle',cycle,'frame',frame,'own/opponent Hull/Crew',stats,flush=True)
            frame+=2
    finally:kernel.CloseHandle(handle)
    save(ROOT/'bounded_probe_result.json',{'candidate_sha256':digest,'emulator_PID':a.pid,
        'observations':entries,'stop_reason':stop,'exact_target_template_observed':success,
        'original_emulator_left_paused_for_visual_and_source_verification':True,
        'paper_detection_used_only_for_navigation_not_as_visual_completion_proof':True,
        'all_live_mutations_must_be_replayed_from_terminal_harness_report':True,
        'only_declared_live_vessel_health_own_provisions_both_positive_captain_HP_and_coordinates_may_change':True,
        'no_RNG_numeric_message_or_battle_result_override':True,
        'enemy_live_health_periodically_restored_to_observed_starting_bounds':True,
        'enemy_result_byte_and_actor_IDs_unchanged_by_fixtures':True,
        'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    print('Probe paused:',stop,'frame',frame,'target',success,flush=True)


if __name__=='__main__':main()
