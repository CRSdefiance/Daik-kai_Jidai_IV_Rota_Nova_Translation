"""Capture the missing C200 execution context without changing native state."""
import inspect
from pathlib import Path
from unicorn import UC_HOOK_MEM_INVALID
from unicorn.arm_const import UC_ARM_REG_LR
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.prove_lil_B139_B140_conditionals_v3461 import probe
from scripts.current_common_native_context_v2677 import CurrentContext
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B139_C200_diagnostic_v3461b')
if __name__=='__main__':
    assert not ROOT.exists();ROOT.mkdir(parents=True);packet=read('work/analysis/lil_remaining_B139_B140_source_v3456/next67_B139_B140_clean_current_context.json')
    text=inspect.getsource(probe);anchor='    stream,owner,result,length=';at=text.index(anchor)
    observer="""    def invalid(u,access,address,size,value,unused):
        save(DIAGNOSTIC,dict(command=command,access=access,address=address,size=size,value=value,PC=u.reg_read(UC_ARM_REG_PC),LR=u.reg_read(UC_ARM_REG_LR),args=[u.reg_read(r) for r in [UC_ARM_REG_R0,UC_ARM_REG_R1,UC_ARM_REG_R2,UC_ARM_REG_R3]],observer_only_no_fixture=True))
        return False
    cpu.hook_add(UC_HOOK_MEM_INVALID,invalid)
"""
    text=text[:at]+observer+text[at:];env={**probe.__globals__,'UC_HOOK_MEM_INVALID':UC_HOOK_MEM_INVALID,'UC_ARM_REG_LR':UC_ARM_REG_LR,'DIAGNOSTIC':ROOT/'first_invalid_read.json'};exec(compile(text,str(Path(__file__))+'::observed-probe','exec'),env)
    ctx=CurrentContext('work/analysis/lil_B139_B140_voices_v3460/current_native_input.json',packet['historical_snapshot_ROM'],ROOT/'current_context');block=IlnkContainer.parse(NdsImage.open(packet['current_ROM']).read_file('/data/SC2.DK4')).blocks[139];c=next(c for b in packet['blocks'] if b['block']==139 for c in b['all_current_native_commands'] if c['word']==0xC200)
    try:ctx.execute(env['probe'],block,c)
    except Exception as e:save(ROOT/'terminal.json',dict(error_type=type(e).__name__,error=str(e),observed_source=text,producer_sha256=sha(Path(__file__).read_bytes()),no_ROM_ledger_or_gameplay_state_change=True,full_goal_complete=False))
    else:raise AssertionError('Missing-context failure did not reproduce')
    print(read(ROOT/'first_invalid_read.json'))
