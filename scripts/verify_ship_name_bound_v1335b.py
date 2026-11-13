"""Retain the registered atomic-append patch while proving the eighteen-byte cap.

The predecessor correctly stopped at clean/current inequality:the accepted
forty-byte atomic preflight is already present. Verify that exact replacement,
all remaining clean instructions and both actual native success/reject exits.
"""
import inspect
from pathlib import Path
from dk4tool.patch import name_editor_atomic_append as atomic
from scripts import verify_ship_name_bound_v1335 as previous

if __name__=='__main__':
    source = inspect.getsource(previous.main)
    changes = [
        ("assert arm[lo:hi]==clean[lo:hi]==raw[lo:hi]", """assert arm[lo:hi]==raw[lo:hi]
        expected = bytearray(clean[lo:hi])
        if lo <= atomic.START < atomic.END <= hi:
            expected[atomic.START-lo:atomic.END-lo] = atomic.replacement()
        assert arm[lo:hi]==bytes(expected)"""),
        ("hook = cpu.hook_add(UC_HOOK_CODE,lambda u,p,s,d:u.emu_stop(),begin=BASE+0xB0950,end=BASE+0xB0950)",
         "hooks = [cpu.hook_add(UC_HOOK_CODE,lambda u,p,s,d:u.emu_stop(),begin=p,end=p) for p in [BASE+0xB0950,BASE+0xB0A08]]"),
        ("assert cpu.reg_read(UC_ARM_REG_PC)==BASE+0xB0950", "assert cpu.reg_read(UC_ARM_REG_PC)==BASE+(0xB0A08 if len(text)>18 else 0xB0950)"),
        ("cpu.hook_del(hook)","for hook in hooks:\n            cpu.hook_del(hook)"),
        ("assert value==text[:18] and get(0xB08C8,parent+0x38)==len(value)",
         "assert value==(b'' if len(text)>18 else text) and get(0xB08C8,parent+0x38)==len(value)"),
        ("'unchanged_clean_current_captured_code_spans':spans", "'registered_atomic_preflight_and_other_clean_captured_code_spans':spans,'atomic_append_module_sha256':sha(Path(atomic.__file__).read_bytes()),'over_capacity_insert_rejected_intact_not_truncated':True,'predecessor_clean_equality_assumption_corrected':True"),
        ('original_bounded_output_hex','current_registered_atomic_output_hex'),
        ('Actual ship-rename editor cap18 bytes:original strlen and six bounded-copy probes pass;23/31-byte names are extra stress only.',
         'Actual ship-name cap18 bytes;registered atomic append preserves/rejects complete insertions;six source-bound probes pass.23/31-byte names are extra stress only.')]
    for old,new in changes:
        assert source.count(old)==1,old
        source = source.replace(old,new)
    env = {**previous.__dict__,'__file__':__file__,'atomic':atomic,
        'ROOT':Path('work/analysis/ship_name_bound_v1335b')}
    exec(compile(source,__file__,'exec'),env)
    env['main']()
