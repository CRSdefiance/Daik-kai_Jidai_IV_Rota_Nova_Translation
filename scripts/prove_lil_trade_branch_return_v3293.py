"""Original two-choice control paths and return0,without selected gameplay."""
import struct
from pathlib import Path
from unicorn import UC_HOOK_CODE
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts.native_machine_scoped_v764 import machine
from scripts.native_call_abi_v764 import call
from scripts.classify_lil_B115_tail_v3216 import ACTIVE,BASE
from scripts.prepare_lil_B122_B127_research_v3289b import ROM,PARENT,PLAN
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_trade_branch_return_v3293')
STREAM,OWNER,RESULT,LENGTH=0x02660000,0x02662000,0x02664000,0x02664100
if __name__=='__main__':
    assert not ROOT.exists();plan=read(PLAN);spec=next(b for b in plan['blocks'] if b['block']==126);mapping={r['old_offset']:r['new_offset'] for r in spec['command_map']};flow=[];returns=[]
    for version,path in [('clean',Path('work/clean.nds')),('current',PARENT),('relocated',ROM)]:
        im=NdsImage.open(path);arm=im.read_file('/__arm9__.bin');block=IlnkContainer.parse(im.read_file('/data/SC2.DK4')).blocks[126];mapped=lambda at:mapping[at] if version=='relocated' else at
        for selected,source_path,firstspeech in [(0,[240,248],344),(1,[240,244],252)]:
            cpu=machine(arm);cpu.mem_write(STREAM-16,b'\xa5'*(len(block)+32));cpu.mem_write(STREAM,block);before=bytes(cpu.mem_read(BASE,0x400000));steps=[];at=mapped(240)
            for expected in source_path:
                assert at==mapped(expected);cpu.mem_write(OWNER-16,b'\xa5'*64);cpu.mem_write(OWNER,struct.pack('<4I',0,STREAM+at,0,0));owned=bytes(cpu.mem_read(OWNER-16,64));cpu.mem_write(RESULT-16,b'\xa5'*80);cpu.mem_write(RESULT,bytes(24));cpu.mem_write(LENGTH-16,b'\xa5'*36);cpu.mem_write(LENGTH,bytes(4))
                call(cpu,0x2A510,(RESULT,OWNER,LENGTH,selected));extent=struct.unpack('<I',cpu.mem_read(LENGTH,4))[0]
                assert struct.unpack('<6I',cpu.mem_read(RESULT,24))==(3,0,0,0,0,0) and bytes(cpu.mem_read(OWNER-16,64))==owned and bytes(cpu.mem_read(BASE,0x400000))==before
                for p in [STREAM-16,STREAM+len(block),RESULT-16,RESULT+24,LENGTH-16,LENGTH+4]:assert bytes(cpu.mem_read(p,16))==b'\xa5'*16
                steps.append(dict(offset=at,extent=extent,word=struct.unpack_from('<H',block,at)[0]));at+=extent
            assert at==mapped(firstspeech) and block[at:at+5]==b'\0\x40\xff\xff\0' and bytes(cpu.mem_read(STREAM,len(block)))==block
            flow.append(dict(version=version,selection=selected,source_command_path=source_path,native_steps=steps,first_speech_offset=at,first_speech_source_offset=firstspeech,selection0_reaches_tutorial_selection1_reaches_already_know_branch=True,ABI_all4MiB_owner_stream_and_guards_exact=True))
        for source_at in [336,954]:
            at=mapped(source_at);assert block[at:at+4]==bytes(4)
            for mode in [0,1]:
                cpu=machine(arm);cpu.mem_write(STREAM-16,b'\xa5'*(len(block)+32));cpu.mem_write(STREAM,block);cpu.mem_write(OWNER-16,b'\xa5'*64);cpu.mem_write(OWNER,struct.pack('<2I',0,STREAM+at));owned=bytes(cpu.mem_read(OWNER-16,64));cpu.mem_write(ACTIVE,struct.pack('<I',1));before=bytes(cpu.mem_read(BASE,0x400000));executed=[];reads=[]
                def observe(u,pc,size,unused):
                    executed.append(pc)
                    if pc==BASE+0x2A524:reads.append(pc)
                hook=cpu.hook_add(UC_HOOK_CODE,observe)
                try:call(cpu,0x23FFC,(0,OWNER,0,mode),instruction_limit=20000)
                finally:cpu.hook_del(hook)
                assert reads==[BASE+0x2A524] and BASE+0x24098 in executed and BASE+0x240EC not in executed and bytes(cpu.mem_read(BASE,0x400000))==before and bytes(cpu.mem_read(OWNER-16,64))==owned and bytes(cpu.mem_read(STREAM,len(block)))==block
                assert bytes(cpu.mem_read(STREAM-16,16))==bytes(cpu.mem_read(STREAM+len(block),16))==b'\xa5'*16
                returns.append(dict(version=version,source_return_offset=source_at,return_offset=at,mode=mode,original_VM_returns_before_cursor_advance=True,ABI_all4MiB_owner_stream_guards_exact=True,source_owned_ACTIVE1_is_isolated_VM_input_not_gameplay_fixture=True))
    assert len(flow)==6 and len(returns)==12
    ROOT.mkdir(parents=True);save(ROOT/'original_choice_control_paths_and_both_VM_return_modes.json',dict(source_plan=str(PLAN),source_plan_sha256=sha(PLAN.read_bytes()),research_ROM=str(ROM),research_ROM_sha256=sha(ROM.read_bytes()),conditional_native_paths=flow,original_VM_return_cases=returns,selection0_skips_already_know_return_and_reaches_tutorial=True,selection1_enters_already_know_branch_and_return0=True,no_naive_linear_graph_discards_tutorial_after_conditional_return=True,source_current_target_branch_endings_preserved=True,isolated_current_native_tests_not_actual_selected_branch_gameplay=True,new_emulator_runs=0,no_ROM_registry_or_editorial_credit=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('Six clean/current/relocated choice-control paths and12 return0 VM cases pass:choice0 reaches tutorial;choice1 enters the already-know branch andreturns. Offline native scope only.')
