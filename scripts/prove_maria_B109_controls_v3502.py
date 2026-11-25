"""Bind source prefix restoration,pause andC200 without claiming UI resource execution."""
import inspect,struct
from pathlib import Path
from unicorn import UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_R0,UC_ARM_REG_R1,UC_ARM_REG_R2,UC_ARM_REG_R3,UC_ARM_REG_PC,UC_ARM_REG_LR
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts.current_common_native_context_v2677 import CurrentContext
from scripts.native_call_abi_v764 import call
from scripts.census_native_storylines_v1995 import complete_walk
from scripts.prove_lil_B139_C200_v3461e import C200
from scripts.verify_village_wrap_v608 import read,save
BASE=0x02000000;ROOT=Path('work/analysis/maria_B109_controls_v3502')
SOURCE=Path('work/analysis/maria_B109_source_v3498/all26_clean_current_complete_context.json')
def pause(arm,common,raw,plan,previous,UI_return):
    cpu,get,provider=machine(arm,common,raw,plan);stream,owner,result,length=0x02660000,0x02662000,0x02664000,0x02664100;value=b'\0\x20';cpu.mem_write(stream-16,b'\xA5'*34);cpu.mem_write(stream,value);cpu.mem_write(owner-16,b'\xA5'*64);cpu.mem_write(owner,struct.pack('<4I',0,stream,0,0));owned=bytes(cpu.mem_read(owner-16,64));before=bytes(cpu.mem_read(BASE,0x400000));calls=[]
    def boundary(u,pc,size,unused):
        args=[u.reg_read(r) for r in [UC_ARM_REG_R0,UC_ARM_REG_R1,UC_ARM_REG_R2,UC_ARM_REG_R3]];assert args==[0,0,length,stream];calls.append(dict(address=pc,args=args,original_caller_return=u.reg_read(UC_ARM_REG_LR),UI_body_unexecuted=True));u.reg_write(UC_ARM_REG_R0,UI_return);u.reg_write(UC_ARM_REG_PC,u.reg_read(UC_ARM_REG_LR))
    h=cpu.hook_add(UC_HOOK_CODE,boundary,begin=BASE+0x54E44,end=BASE+0x54E44);cpu.mem_write(result-16,b'\xA5'*80);cpu.mem_write(result,bytes(24));cpu.mem_write(length-16,b'\xA5'*36);cpu.mem_write(length,bytes(4))
    try:call(cpu,0x2A510,(result,owner,length,previous))
    finally:cpu.hook_del(h)
    extent=struct.unpack('<I',cpu.mem_read(length,4))[0];decoded=list(struct.unpack('<6I',cpu.mem_read(result,24)));assert len(calls)==1 and calls[0]['original_caller_return']==BASE+0x2A218 and extent==2 and decoded==[3,0,0,0,0,0] and bytes(cpu.mem_read(BASE,0x400000))==before and bytes(cpu.mem_read(owner-16,64))==owned and bytes(cpu.mem_read(stream,2))==value
    for at in [stream-16,stream+2,result-16,result+24,length-16,length+4]:assert bytes(cpu.mem_read(at,16))==b'\xA5'*16
    return dict(previous_result=previous,incidental_unexecuted_UI_return=UI_return,native_extent=extent,native_result=decoded,original_UI_boundary_calls=calls,no_source_resident_text_payload=True,ABI_all4MiB_owner_stream_result_length_and_boundary_guards_exact=True,full_UI_body_effects_display_and_input_behavior_not_executed=True,current_executed_instruction_addresses=len(provider.executed_current))
if __name__=='__main__':
    assert not ROOT.exists();packet=read(SOURCE);image,clean=NdsImage.open(packet['current_ROM']),NdsImage.open('work/clean.nds');arm,oldarm=[i.read_file('/__arm9__.bin') for i in [image,clean]];jp,current=[IlnkContainer.parse(i.read_file('/data/SC3.DK4')).blocks[109] for i in [clean,image]];finding=read(packet['source_packed_UI_control_finding']);assert sha(Path(packet['source_packed_UI_control_finding']).read_bytes())==packet['source_packed_UI_control_finding_sha256'] and finding['current_ROM_sha256']==packet['current_ROM_sha256']
    draft=bytearray(current);draft[8:18]=jp[8:18];draft=bytes(draft);assert [i for i,(a,b) in enumerate(zip(current,draft,strict=True)) if a!=b]==[13,14,15,16,17] and draft[:4]==jp[:4]==b'CS\1\1'
    source_walk=complete_walk(oldarm,jp);target_walk=complete_walk(arm,draft);assert not source_walk['errors'] and not target_walk['errors'];shape=lambda w:[(r['offset'],r['word'],r['native_extent'],r['ancestor_0100_offsets']) for r in w['commands']];assert shape(source_walk)==shape(target_walk) and len(source_walk['commands'])==34
    opaque=[]
    for a,b in zip(source_walk['commands'],target_walk['commands'],strict=True):
        if a['word']==0x4000:continue
        assert a['whole_command_hex']==b['whole_command_hex'];opaque.append(dict(offset=a['offset'],word=a['word'],native_extent=a['native_extent'],source_hex=a['whole_command_hex'],repaired_draft_hex=b['whole_command_hex'],no_prose_or_invented_control_meaning=True))
    assert len(opaque)==8 and sum(c['word']==0x2000 for c in opaque)==1 and sum(c['word']==0xC200 for c in opaque)==1 and not any(c['word'] in [0x100,0x200,0x300,0x400,0x8000,0x8100,0x2100,0x4100] for c in source_walk['commands'])
    spans=[(0x29AA0,0x2A154),(0x2A1D8,0x2A238),(0x29434,0x294D8),(0x21B80,0x21C14),(0x904BC,0x904F4)];assert all(arm[a:b]==oldarm[a:b] for a,b in spans)
    ROOT.mkdir(parents=True);blockpath=ROOT/'SC3_block109_control_restored_DRAFT_ONLY.bin';blockpath.write_bytes(draft);ctx=CurrentContext('work/analysis/maria_B109_voices_v3499/current_native_input.json',packet['historical_snapshot_ROM'],ROOT/'current_context');pauses=[]
    for previous in [0,1,2,3,0xFFFFFFFF]:
        for UI_return in [0,0xFFFFFFFF]:pauses.append(ctx.execute(pause,previous,UI_return));ctx.machines.pop()
    command=next(c for c in source_walk['commands'] if c['word']==0xC200);pair=[]
    for version,block in [('clean-control-source',jp),('repaired-control-current-English',draft)]:pair.append(dict(version=version,**ctx.execute(C200,block,command)));ctx.machines.pop()
    assert len(pauses)==10 and pair[0]['native_result']==pair[1]['native_result'] and pair[0]['source_owned_UI_writes']==pair[1]['source_owned_UI_writes'] and pair[0]['source_owned_UI_request_words']==pair[1]['source_owned_UI_request_words'] and not ctx.machines
    save(ROOT/'source_restored_UI_prefix_pause_C200_and34_commands_contract.json',dict(candidate=packet['current_ROM'],candidate_sha256=packet['current_ROM_sha256'],source_context=str(SOURCE),source_context_sha256=sha(SOURCE.read_bytes()),source_packed_UI_finding=packet['source_packed_UI_control_finding'],source_packed_UI_finding_sha256=packet['source_packed_UI_control_finding_sha256'],source_prefix_hex=jp[8:18].hex(),current_bad_prefix_hex=current[8:18].hex(),control_restored_draft=str(blockpath),control_restored_draft_sha256=sha(draft),source_block_sha256=sha(jp),current_block_sha256=sha(current),source_native_walk=source_walk,restored_native_walk=target_walk,all34_source_restored_command_shapes_and26_speech_headers_equal=True,all8_non_speech_commands_source_exact_after_prefix_restoration=opaque,source_owned_prefix_restore_span=dict(offset=8,bytes=10,source_hex=jp[8:18].hex(),previous_hex=current[8:18].hex()),only_five_current_bad_control_bytes_changed=True,no_name_text_object_in_source_prefix=True,original2000_pause_cases=pauses,source_current_C200_pair=pair,type3_only_first_result_word_semantic=True,C200_resource_bodies_explicit_unexecuted=True,portable_source_owned_adapters=dict(pause=inspect.getsource(pause),C200=inspect.getsource(C200)),source_exact_code_spans=[dict(start=a,end=b,sha256=sha(arm[a:b])) for a,b in spans],native_context_plan=str(ctx.proof_path),native_context_plan_sha256=sha(ctx.proof_path.read_bytes()),focused_actual_display_and_normal_return_still_required=True,no_ROM_registry_ledger_review_orcompletion_change=True,actual_selected_B109_IDs=[],new_emulator_runs=0,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print(dict(restored_command_shapes=34,speeches=26,source_exact_non_speech_commands=8,pause_decoder_cases=10,C200_pair=True,C200_queue=pair[0]['source_owned_UI_request_words'],draft_bytes=len(draft),only_bad_control_bytes_changed=True,actual_display_pending=True))
