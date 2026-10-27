"""Read-only saved-callstack proof: region3 chose the original swamp callback."""
import struct
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_village_wrap_v608 import save

ROOT=Path('work/analysis/fatigue_search_stack_v1601')
CAP=Path('E:/Rota Nova translations/Generated/work/emulation_v193/fatigue_recovery_live_v1597c_1594')
ROM=Path('out/all_routes_combined_v1594_candidate.nds')

if __name__=='__main__':
    assert not ROOT.exists()
    arm=NdsImage.open(ROM).read_file('/__arm9__.bin')
    clean=NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    spans=[(0x5160C,0x51708),(0x793FC,0x79514),(0x797A0,0x79958),(0x79E20,0x79E98),(0x119164,0x119194)]
    for start,end in spans:assert arm[start:end]==clean[start:end]
    table=struct.unpack_from('<I',arm,0x79FEC)[0];assert table==0x02119164
    assert struct.unpack_from('<2I',arm,table-0x02000000+3*8)==(0x0207931C,0x020793FC)
    records=[]
    for frame in [5900,6700]:
        path=CAP/f'frame_{frame:06d}_arm9_ram.bin';raw=path.read_bytes()
        for start,end in spans:assert raw[start:end]==arm[start:end]
        positions=[];pos=0
        while True:
            at=raw.find(struct.pack('<I',0x02079E90),pos)
            if at<0:break
            pos=at+1;main=at+4
            if main+0xB0<=len(raw) and struct.unpack_from('<I',raw,main+0xAC)[0]==0x0207B190:positions.append(main)
        assert len(positions)==1
        main=positions[0];point=struct.unpack_from('<2i',raw,main+0x14)
        assert point==struct.unpack_from('<2i',raw,main+0x2C)
        saved_region,voice_return,role,voice_table=[struct.unpack_from('<I',raw,main+delta)[0] for delta in [-8,-0x3C,-0x38,-0x34]]
        assert (saved_region,voice_return,role,voice_table)==(3,0x02079430,1,0x02116920)
        cpu,get=get_machine(arm,raw);ptr=0x02470000;cpu.mem_write(ptr,struct.pack('<2i',*point))
        assert get(0x797A0,ptr)==saved_region
        records.append({'frame':frame,'RAM':str(path),'RAM_sha256':sha(raw),'Search_main_SP':hex(0x02000000+main),
            'Search_input_and_cached_point':list(point),'original_region':saved_region,
            'callback_saved_region':saved_region,'callback_return_to_Search':hex(0x02079E90),
            'speech_return_to_original_swamp_callback':hex(voice_return),'speech_role':role,'speech_table':hex(voice_table),
            'original_swamp_callback':hex(0x020793FC),'original_region3_other_choice_hot_spring':hex(0x0207931C),
            'no_CPU_or_game_state_mutation_saved':True})
    ROOT.mkdir(parents=True)
    save(ROOT/'actual_Search_region3_swamp_callstack_proof.json',{'candidate':str(ROM),'candidate_sha256':sha(ROM.read_bytes()),'records':records,
        'original_code_table_and_actual_RAM_spans_exact':True,
        'erratum':'Beast dialogue alone did not identify callback79224. Both live holds came through793FC, the region3 swamp callback. Saved region3 and saved speech LR79430 reconcile the original dispatch with the CPU region model.',
        'cached_and_mobile_location_coherence_remains_a_separate_fixture_improvement':True,
        'no_recovery309_or_editorial_completion_credit':True,'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    print('Both live callstacks prove original region3 swamp793FC, not beast79224;region model reconciled. No recovery credit.')
