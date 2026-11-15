"""Record the failing original FE painter return, without weakening any native assertion."""
import inspect
from pathlib import Path
from types import FunctionType
from unicorn.arm_const import UC_ARM_REG_R0
from scripts import square_shopkeeper_font_oracles_v7020 as font
from scripts import Rafael_B45_FE_source_painter_v7894 as painter
from scripts.registered_editorial_runtime_v2 import RegisteredRuntime
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest

ROOT=Path('work/Maria_B216_B252_clean_20261110')


def main():
    out=ROOT/'B221_R8_FE_failure_diagnostic_v1.json';assert not out.exists()
    planpath=ROOT/'native_inputs_v1/plans.json';plan=load(planpath)
    row=next(r for r in plan['records'] if r['id']=='DK4_MES_B221_R0008')
    ctx=RegisteredRuntime('work/maria321_B196_B215_release_v1/registered_release_verification.json',
        'work/maria321_B196_B215_release_v1/own_registered_startup_verification.json',captain=3)
    ascii_factory=FunctionType(font.make_painter.__code__,{**font.make_painter.__globals__,'CURRENT_ARM9':digest_bytes(ctx.arm)},argdefs=font.make_painter.__defaults__)
    diagnostic={}
    source=checked_text(inspect.getsource(painter.make_source_painter),{
        "        assert cpu.reg_read(UC_ARM_REG_R0)==string+len(text) and bytes(cpu.mem_read(string,len(text)+1))==text+b'\\0'":
        "        DIAGNOSTIC.update(return_consumed_bytes=cpu.reg_read(UC_ARM_REG_R0)-string,intended_bytes=len(text),events=events,input_unchanged=bytes(cpu.mem_read(string,len(text)+1))==text+b'\\0')\n        assert cpu.reg_read(UC_ARM_REG_R0)==string+len(text) and bytes(cpu.mem_read(string,len(text)+1))==text+b'\\0'",
    })
    env={**painter.make_source_painter.__globals__,'ASCII_painter':ascii_factory,'CURRENT_ARM9':digest_bytes(ctx.arm),'DIAGNOSTIC':diagnostic}
    exec(compile(source,__file__+'::original-instructions-return-observer-only','exec'),env)
    paint,calibration=env['make_source_painter'](ctx.image);raw=bytes.fromhex(row['encoded_hex']);assert raw[0]==254
    try:paint(raw[1:])
    except AssertionError:pass
    else:raise AssertionError('Expected native failure was not reproduced')
    assert diagnostic and diagnostic['return_consumed_bytes']<diagnostic['intended_bytes'] and diagnostic['input_unchanged']
    save(out,dict(id=row['id'],runtime=ctx.receipt(),plan=str(planpath),plan_sha256=digest(planpath),compiled_hex=raw.hex(),
        lines=row['lines'],diagnostic=diagnostic,calibration=calibration,observer_source=source,
        assertion_preserved=True,no_native_CODE_ROM_prose_orlayout_changes=True,no_display_approval=True,new_credit=0,
        evidence={str(p):digest(p) for p in [planpath,Path(painter.__file__),Path(__file__)]}))
    print(dict(consumed=diagnostic['return_consumed_bytes'],intended=diagnostic['intended_bytes'],
        rows=sorted({e['y'] for e in diagnostic['events']}),last_events=diagnostic['events'][-6:]))


def digest_bytes(data):
    from dk4tool.patch.grand_race_menu_release import sha
    return sha(data)


if __name__=='__main__':main()
