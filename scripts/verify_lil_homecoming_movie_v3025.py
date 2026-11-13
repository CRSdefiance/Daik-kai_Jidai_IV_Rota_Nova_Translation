"""Focused original chapter6 handler at clean/current/relocated source cursors."""
import struct
from pathlib import Path
from unicorn import UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_R0,UC_ARM_REG_R1,UC_ARM_REG_R2,UC_ARM_REG_R3,UC_ARM_REG_PC,UC_ARM_REG_LR
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts.current_common_native_context_v2677 import CurrentContext
from scripts.native_call_abi_v764 import call
from scripts.prepare_lil_homecoming_ian_research_v3022 import ROM,PARENT,PLAN
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_Homecoming_Ian_movie_v3025')
BASE=0x02000000
OWNER,STREAM,RESULT,LENGTH=0x02650000,0x02660000,0x02668000,0x02668100
def chapter(arm,common,raw,plan,block,offset):
    cpu,get,provider=machine(arm,common,raw,plan)
    assert block[offset:offset+2]==b'\x06\x49'
    scene=struct.unpack('<I',cpu.mem_read(BASE+0x2A144,4))[0];assert scene==0x02276F88
    before=bytes(cpu.mem_read(BASE,0x400000));requests=[];resets=[];visited=set()
    cpu.mem_write(STREAM-16,b'\xA5'*(len(block)+32));cpu.mem_write(STREAM,block)
    cpu.mem_write(OWNER-16,b'\xA5'*64);cpu.mem_write(OWNER,struct.pack('<8I',0,STREAM+offset,0,0,0,0,0,0));owner=bytes(cpu.mem_read(OWNER-16,64))
    cpu.mem_write(RESULT-16,b'\xA5'*64);cpu.mem_write(LENGTH-16,b'\xA5'*36);cpu.mem_write(LENGTH,bytes(4))
    def observe(u,pc,size,unused):
        visited.add(pc)
        if pc not in [BASE+0xD2B1C,BASE+0x21C14]:return
        args=[u.reg_read(r) for r in [UC_ARM_REG_R0,UC_ARM_REG_R1,UC_ARM_REG_R2,UC_ARM_REG_R3]]
        (requests if pc==BASE+0xD2B1C else resets).append(dict(PC=pc,args=args))
        u.reg_write(UC_ARM_REG_R0,0);u.reg_write(UC_ARM_REG_PC,u.reg_read(UC_ARM_REG_LR))
    h=cpu.hook_add(UC_HOOK_CODE,observe)
    try:call(cpu,0x2A510,(RESULT,OWNER,LENGTH),instruction_limit=100000)
    finally:cpu.hook_del(h)
    assert requests==[dict(PC=BASE+0xD2B1C,args=[26,0,1,0])]
    assert len(resets)==1 and resets[0]['args'][:2]==[scene,1]
    assert struct.unpack('<I',cpu.mem_read(RESULT,4))[0]==3 and struct.unpack('<I',cpu.mem_read(LENGTH,4))[0]==2
    assert bytes(cpu.mem_read(scene+0x24B8,8))==struct.pack('<2I',1,1)
    after=bytearray(cpu.mem_read(BASE,0x400000));at=scene+0x24B8-BASE;after[at:at+8]=before[at:at+8];assert bytes(after)==before
    assert bytes(cpu.mem_read(OWNER-16,64))==owner and bytes(cpu.mem_read(STREAM,len(block)))==block
    for at in [STREAM-16,STREAM+len(block),RESULT-16,RESULT+4,LENGTH-16,LENGTH+4]:assert bytes(cpu.mem_read(at,16))==b'\xA5'*16
    required={BASE+x for x in [0x2A510,0x29AA0,0x2A0F8,0x28A28]};assert required<=visited
    return dict(source_cursor=STREAM+offset,offset=offset,word=0x4906,native_movie_request=requests,native_scene_reset_boundary=resets,
        complete_original_handler_and_saved_register_ABI=True,complete_block_owner_result_length_guards_exact=True,
        only_original_source_owned_scene_reset_8bytes_written_all_other4MiB_exact=True,source_owned_scene_fields_before_hex=before[at:at+8].hex() if False else before[scene+0x24B8-BASE:scene+0x24C0-BASE].hex(),
        all_required_original_handler_entries_executed=sorted(required),current_executed_instruction_addresses=len(provider.executed_current),
        only_movie_playback_and_scene_reset_bodies_explicit_unexecuted_boundaries=True)
if __name__=='__main__':
    assert not ROOT.exists();p=read(PLAN);source=read('work/analysis/lil_Homecoming_Ian_source_v3002/complete172_clean_current_native_context.json')
    spec=next(b for b in p['blocks'] if b['block']==70);offset=4324
    assert next(c for b in source['blocks'] if b['block']==70 for c in b['all_clean_native_commands'] if c['word']==0x4906)['offset']==offset
    mapped=offset+sum(r['new_length']-r['old_length'] for r in spec['text_records'] if r['old_offset']+r['old_length']<=offset)
    ROOT.mkdir(parents=True);ctx=CurrentContext('work/analysis/lil_Homecoming_Ian_fonts_v3013/current_native_input.json',source['historical_snapshot_ROM'],ROOT/'current_context');cases=[]
    for label,path,at in [('clean','work/clean.nds',offset),('current',PARENT,offset),('relocated',ROM,mapped)]:
        im=NdsImage.open(path);block=IlnkContainer.parse(im.read_file('/data/SC2.DK4')).blocks[70]
        result=ctx.execute(chapter,block,at);ctx.machines.pop();cases.append(dict(label=label,ROM=str(path),ROM_sha256=sha(Path(path).read_bytes()),block_sha256=sha(block),**result))
    assert len(cases)==3 and not ctx.machines
    save(ROOT/'original_chapter6_relocated_cursor_and_M26_arguments.json',dict(cases=cases,source_offset=offset,relocated_offset=mapped,all3_complete_current_original_movie_handler_cases_pass=True,
        original_M26_request26_0_1_0_preserved=True,all_unowned_state_and_ABI_guards_exact=True,source_plan=str(PLAN),source_plan_sha256=sha(PLAN.read_bytes()),
        native_context_plan=str(ctx.proof_path),native_context_plan_sha256=sha(ctx.proof_path.read_bytes()),wedding_actual_rule='work/analysis/lil_Homecoming_Ian_wedding_contract_v3006/historical_actual_wedding_FE_and_M26_source_contract.json',
        no_new_movie_RGB_or_selected_gameplay_or_fixture=True,new_emulator_runs=0,completion_credit_added=0,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print(dict(clean_current_movie_offset=offset,relocated_movie_offset=mapped,original_movie_arguments=[26,0,1,0],cases=3,all_unowned_state_exact=True))
