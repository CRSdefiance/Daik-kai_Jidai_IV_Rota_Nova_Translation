"""Capture the original query result before the inherited boolean-result assertion."""
import inspect
from pathlib import Path
from capstone import Cs,CS_ARCH_ARM,CS_MODE_ARM
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.prove_lil_crew_items_controls_v3114 import predicate
from scripts.current_common_native_context_v2677 import CurrentContext
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B138_query_diagnostic_v3426b')
SOURCE=Path('work/analysis/lil_remaining_B138_B140_source_v3422/next44_B138_clean_current_context.json')
if __name__=='__main__':
    assert not ROOT.exists();ROOT.mkdir(parents=True);packet=read(SOURCE);image=NdsImage.open(packet['current_ROM']);b=packet['blocks'][0];c=next(c for c in b['all_current_native_commands'] if c['word']==0x8100)
    arm=image.read_file('/__arm9__.bin');text=inspect.getsource(predicate);needle="assert values[0]==2 and values[1] in [0,1] and extent==command['native_extent']";assert text.count(needle)==1
    t=text.replace(needle,"save(DIAGNOSTIC,dict(command=command,values=list(values),extent=extent,event_calls=calls,producer_sha256=sha(Path(DIAGNOSTIC_PRODUCER).read_bytes()),no_predicate_or_event_flag_forced=True)); "+needle)
    env={**predicate.__globals__,'save':save,'sha':sha,'Path':Path,'DIAGNOSTIC':ROOT/'query_before_original_assertion.json','DIAGNOSTIC_PRODUCER':__file__};exec(compile(t,str(Path(__file__))+'::captured-predicate','exec'),env)
    from dk4tool.formats.ilnk import IlnkContainer
    ctx=CurrentContext('work/analysis/lil_B138_voices_v3425/current_native_input.json',packet['historical_snapshot_ROM'],ROOT/'current_context')
    try:ctx.execute(env['predicate'],IlnkContainer.parse(image.read_file('/data/SC2.DK4')).blocks[138],c)
    except AssertionError:pass
    else:raise AssertionError('Expected inherited assertion did not reproduce')
    current=NdsImage.open(packet['current_ROM']).read_file('/__arm9__.bin');clean=NdsImage.open('work/clean.nds').read_file('/__arm9__.bin');assert current[0x23840:0x238C0]==clean[0x23840:0x238C0] and current[0x2A530:0x2A600]==clean[0x2A530:0x2A600]
    decoder=Cs(CS_ARCH_ARM,CS_MODE_ARM);out=[]
    for start,end in [(0x23840,0x238C0),(0x2A530,0x2A600)]:
        out.extend(f'{i.address:08X} {i.bytes.hex()} {i.mnemonic} {i.op_str}' for i in decoder.disasm(current[start:end],0x02000000+start))
    p=ROOT/'original_query_and_conditional_handlers.txt';p.write_text('\n'.join(out)+'\n',encoding='utf-8')
    save(ROOT/'diagnostic_receipt.json',dict(result=str(ROOT/'query_before_original_assertion.json'),result_sha256=sha((ROOT/'query_before_original_assertion.json').read_bytes()),disassembly=str(p),disassembly_sha256=sha(p.read_bytes()),inherited_helper=str(Path(predicate.__globals__['__file__'])),inherited_helper_sha256=sha(Path(predicate.__globals__['__file__']).read_bytes()),instrumented_source=t,source_context=str(SOURCE),source_context_sha256=sha(SOURCE.read_bytes()),no_ROM_ledger_or_source_mutation=True,full_goal_complete=False))
    print(read(ROOT/'query_before_original_assertion.json'))
