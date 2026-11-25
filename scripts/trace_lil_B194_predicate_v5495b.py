"""Observe original unconditional calls in the unforced conditional evaluator."""
from pathlib import Path
import inspect
from scripts.prove_lil_B139_B140_conditionals_v3461c import probe
from scripts.current_build_native_context_v4774 import CurrentContext
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
ROOT=Path('work/analysis/lil_B194_predicate_trace_v5495b')
SOURCE=Path('work/analysis/lil_B194_source_v5489/all11_clean_current_complete_context.json')
if __name__=='__main__':
    assert not ROOT.exists();packet=read(SOURCE);text=inspect.getsource(probe)
    needle='    h=cpu.hook_add(UC_HOOK_CODE,trace,';assert text.count(needle)==1
    addition="""    original_calls=[]
    def observe_call(u,pc,size,unused):
        if size!=4:return
        word=int.from_bytes(u.mem_read(pc,4),'little')
        if word>>24!=0xEB:return
        displacement=word&0xFFFFFF
        if displacement&0x800000:displacement-=0x1000000
        original_calls.append(dict(PC=pc,target=(pc+8+displacement*4)&0xFFFFFFFF,args=[u.reg_read(r) for r in [UC_ARM_REG_R0,UC_ARM_REG_R1,UC_ARM_REG_R2,UC_ARM_REG_R3]]))
    observe_handle=cpu.hook_add(UC_HOOK_CODE,observe_call)
"""
    text=text.replace(needle,addition+needle).replace('finally:cpu.hook_del(h);cpu.hook_del(wh)','finally:cpu.hook_del(h);cpu.hook_del(wh);cpu.hook_del(observe_handle)')
    text=text.replace('return dict(offset=command',"return dict(original_unconditional_BL_calls=original_calls,offset=command")
    env=dict(probe.__globals__);exec(compile(text,__file__+'::read-only-call-observer','exec'),env)
    image=NdsImage.open(packet['current_ROM']);block=IlnkContainer.parse(image.read_file('/data/SC2.DK4')).blocks[194]
    command=next(c for c in packet['blocks'][0]['all_current_native_commands'] if c['word']==0x8000)
    ROOT.mkdir(parents=True);ctx=CurrentContext('work/analysis/lil_B194_voices_v5490/current_native_input.json',packet['historical_snapshot_ROM'],ROOT/'current_context')
    result=ctx.execute(env['probe'],block,command);ctx.machines.pop();assert not ctx.machines and result['no_predicate_or_event_flag_forced']
    save(ROOT/'unforced_original_calls.json',dict(source_context=str(SOURCE),source_context_sha256=sha(SOURCE.read_bytes()),result=result,source_owned_observer=text,
        original_native_calls_observed_without_replacement_or_result_forcing=True,native_context_plan=str(ctx.proof_path),native_context_plan_sha256=sha(ctx.proof_path.read_bytes()),
        producer_sha256=sha(Path(__file__).read_bytes()),new_emulator_runs=0,new_review_credit=0,full_goal_complete=False))
    for r in result['original_unconditional_BL_calls']:print(hex(r['PC']),hex(r['target']),[hex(x) for x in r['args']])
