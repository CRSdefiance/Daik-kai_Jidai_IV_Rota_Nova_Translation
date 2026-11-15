"""Bind28 speech dispatches,C200 and the opaque630A native boundary."""
import inspect,struct
from pathlib import Path
from unicorn import UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_R0,UC_ARM_REG_R1,UC_ARM_REG_R2,UC_ARM_REG_R3,UC_ARM_REG_PC,UC_ARM_REG_LR
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts import prove_lil_shrines_temples_controls_v3168c as prior
from scripts.current_common_native_context_v2677 import CurrentContext
from scripts.native_call_abi_v764 import call
from scripts.prove_lil_B139_C200_v3461e import C200
from scripts.verify_village_wrap_v608 import read,save
BASE=0x02000000
ROOT=Path('work/analysis/lil_B141_controls_v3538b')
SOURCE=Path('work/analysis/lil_B141_source_v3532b/all14_clean_current_complete_context.json')
def control630A(arm,common,raw,plan,previous,boundary_return):
    cpu,get,provider=machine(arm,common,raw,plan);stream,owner,result,length=0x02660000,0x02650000,0x02668000,0x02668100;value=bytes.fromhex('0a63')
    cpu.mem_write(stream-16,b'\xA5'*34);cpu.mem_write(stream,value);cpu.mem_write(owner-16,b'\xA5'*64);cpu.mem_write(owner,struct.pack('<4I',0,stream,0,0));guard=bytes(cpu.mem_read(owner-16,64));cpu.mem_write(result-16,b'\xA5'*80);cpu.mem_write(result,bytes(24));cpu.mem_write(length-16,b'\xA5'*36);cpu.mem_write(length,bytes(4));before=bytes(cpu.mem_read(BASE,0x400000));calls=[]
    def boundary(u,pc,size,unused):
        args=[u.reg_read(r) for r in [UC_ARM_REG_R0,UC_ARM_REG_R1,UC_ARM_REG_R2,UC_ARM_REG_R3]];assert args==[0x02386EFC,10,2,1] and u.reg_read(UC_ARM_REG_LR)==BASE+0x29A84;calls.append(dict(address=pc,args=args,source_return_address=u.reg_read(UC_ARM_REG_LR),callee_body_unexecuted=True));u.reg_write(UC_ARM_REG_R0,boundary_return);u.reg_write(UC_ARM_REG_PC,u.reg_read(UC_ARM_REG_LR))
    h=cpu.hook_add(UC_HOOK_CODE,boundary,begin=BASE+0x1096F8,end=BASE+0x1096F8)
    try:call(cpu,0x2A510,(result,owner,length,previous))
    finally:cpu.hook_del(h)
    decoded=list(struct.unpack('<6I',cpu.mem_read(result,24)));extent=struct.unpack('<I',cpu.mem_read(length,4))[0];assert len(calls)==1 and decoded==[3,0,0,0,0,0] and extent==2 and bytes(cpu.mem_read(BASE,0x400000))==before and bytes(cpu.mem_read(owner-16,64))==guard and bytes(cpu.mem_read(stream,2))==value
    for at in [stream-16,stream+2,result-16,result+24,length-16,length+4]:assert bytes(cpu.mem_read(at,16))==b'\xA5'*16
    return dict(previous_result=previous,incidental_boundary_return=boundary_return,native_result=decoded,native_extent=extent,source_command_hex=value.hex(),original_boundary_calls=calls,all4MiB_owner_input_ABI_output_and_length_guards_exact=True,no_resident_text_or_money_subtraction_at_this_decoder_boundary=True,not_callee_effects_or_actual_gameplay_proof=True,current_executed_instruction_addresses=len(provider.executed_current))
if __name__=='__main__':
    assert not ROOT.exists();packet=read(SOURCE);image,clean=NdsImage.open(packet['current_ROM']),NdsImage.open('work/clean.nds');blocks=[IlnkContainer.parse(im.read_file('/data/SC2.DK4')).blocks[141] for im in [clean,image]];ROOT.mkdir(parents=True)
    namespace={**prior.__dict__,'SOURCE':SOURCE,'CATALOG_LOOKUP':{}};adapters={}
    for name in ['bind_current_catalog','expanded_current_body','install_boundaries','dispatch']:
        text=inspect.getsource(getattr(prior,name));adapters[name]=text;exec(compile(text,str(Path(__file__))+'::'+name,'exec'),namespace)
    namespace['CATALOG_LOOKUP'],binding=namespace['bind_current_catalog'](image);assert binding['route']==2 and binding['route_mask']==4
    bp=ROOT/'current_registered_Lil_name_catalog_binding.json';save(bp,binding);ctx=CurrentContext('work/analysis/lil_B141_voices_v3533/current_native_input.json',packet['historical_snapshot_ROM'],ROOT/'current_context');speeches=[]
    for r in packet['records']:
        for version,key in [('clean-Japanese','source_hex'),('current-English','current_hex')]:
            raw=bytes.fromhex(r[key]);result=ctx.execute(namespace['dispatch'],raw[0],raw[1:]);ctx.machines.pop();assert result['resolved_actor_ID']==r['source_selector'];speeches.append(dict(id=r['id'],version=version,**result))
    c=next(c for c in packet['blocks'][0]['all_current_native_commands'] if c['word']==0xC200);ui=[]
    for label,block in zip(['clean','current'],blocks,strict=True):ui.append(dict(version=label,**ctx.execute(C200,block,c)));ctx.machines.pop()
    assert ui[0]['source_owned_UI_request_words']==ui[1]['source_owned_UI_request_words']==[1,0,13,0,0,0,1] and ui[0]['source_owned_UI_writes']==ui[1]['source_owned_UI_writes']
    effects=[]
    for previous in [0,1,2,3,0xFFFFFFFF]:
        for result in [0,0xFFFFFFFF]:effects.append(ctx.execute(control630A,previous,result));ctx.machines.pop()
    assert len(speeches)==28 and len(effects)==10 and not ctx.machines and packet['source_macro_counts']=={'FI':1,'FA':0,'FO':0}
    save(ROOT/'all14_source_current_dispatches_FI_C200_and630A_contract.json',dict(candidate=packet['current_ROM'],candidate_sha256=packet['current_ROM_sha256'],source_context=str(SOURCE),source_context_sha256=sha(SOURCE.read_bytes()),speech_dispatch_cases=speeches,source_macro_counts=packet['source_macro_counts'],source_owned_adapters={**adapters,'C200':inspect.getsource(C200),'control630A':inspect.getsource(control630A)},source_C200_cases=ui,source_630A_cases=effects,registered_catalog_binding=str(bp),registered_catalog_binding_sha256=sha(bp.read_bytes()),all_four_selectors_static_without_role_assignment=True,current_original_UI_preparation_progressive_C200_resource_and630A_callee_bodies_explicit_unexecuted=True,source_630A_not_misclassified_as_actual_payment=True,actual_payment_separate_A000_9101ffbd=True,three_other_source_A000_effects_preserved_byte_ownership_not_full_effect_execution=True,native_context_plan=str(ctx.proof_path),native_context_plan_sha256=sha(ctx.proof_path.read_bytes()),no_ROM_registry_ledger_review_orcompletion_change=True,new_emulator_runs=0,actual_selected_B141_IDs=[],producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print(dict(dispatches=28,source_FI=1,C200_source_current_pairs=1,opaque630A_decoder_cases=10,source_C200_queue=[1,0,13,0,0,0,1],review_credit=0))
