"""Resolve the item counter in coherent current RAM, preserving the failed flat-pointer assumption."""
import inspect,struct
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.current_common_native_context_v2677 import CurrentContext
from scripts.verify_village_wrap_v608 import read,save
def bind_counter(arm,common,raw,plan,field,expected):
    cpu,get,provider=machine(arm,common,raw,plan)
    before=bytes(cpu.mem_read(0x02000000,0x400000))
    pointer=struct.unpack('<I',cpu.mem_read(0x02000000+field,4))[0]
    value=bytes(cpu.mem_read(pointer,len(expected)))
    assert value==expected and bytes(cpu.mem_read(0x02000000,0x400000))==before
    return dict(current_pointer_field=0x02000000+field,current_pointer=pointer,current_complete_cstring_hex=value.hex(),all4MiB_readonly=True,current_staged_payload_resolved_in_live_address_space=True,no_original_UI_body_executed=True)
if __name__=='__main__':
    draft=Path('scripts/reconcile_lil_B168_terms_v4176.py');text=draft.read_text(encoding='utf-8')
    changes={
        "ROOT=Path('work/analysis/lil_B168_terms_v4176')":"ROOT=Path('work/analysis/lil_B168_terms_v4176b')",
        'assert pointer==0x02000000+pos':"ctx=CurrentContext('work/analysis/lil_B168_voices_v4170/current_native_input.json',packet['historical_snapshot_ROM'],Path('work/analysis/lil_B168_terms_v4176b_context'));binding=ctx.execute(bind_counter,field,literal);ctx.machines.pop();assert not ctx.machines and pointer==binding['current_pointer']",
        "new_actual_gameplay_or_native_UI_calls=0":"current_counter_pointer_proof=binding,current_counter_readonly_adapter=inspect.getsource(bind_counter),preserved_failed_flat_pointer_assumption=str(DRAFT),preserved_failed_flat_pointer_producer_sha256=sha(DRAFT.read_bytes()),native_context_plan=str(ctx.proof_path),native_context_plan_sha256=sha(ctx.proof_path.read_bytes()),new_actual_gameplay_or_native_UI_body_calls=0",
    }
    for old,new in changes.items():assert text.count(old)==1;text=text.replace(old,new)
    exec(compile(text,__file__+'::current-staged-pointer','exec'),dict(globals(),DRAFT=draft))
