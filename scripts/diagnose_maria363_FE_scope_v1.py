"""Check remaining FE plans once for the demonstrated native wrap/consumption risk."""
import inspect
from pathlib import Path
from types import FunctionType
from scripts import square_shopkeeper_font_oracles_v7020 as font
from scripts import Rafael_B45_FE_source_painter_v7894 as painter
from scripts.registered_editorial_runtime_v2 import RegisteredRuntime
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.check_editorial_compiled_pages_v6 import check_FE_rows
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from dk4tool.patch.grand_race_menu_release import sha

ROOT=Path('work/Maria_B216_B252_clean_20261110')


def main():
    out=ROOT/'FE_scope_diagnostic_v1.json';assert not out.exists()
    planpath=ROOT/'plan_v6/automatic_plans.json';docpath=ROOT/'formatting_v1/formatting_input.json';macpath=ROOT/'formatting_v1/native_macro_measurements.json'
    plan,doc,mac=map(load,[planpath,docpath,macpath]);byid={r['id']:r for r in plan['records']}
    ctx=RegisteredRuntime(doc['runtime']['release_proof'],doc['runtime']['startup_proof'],captain=3);assert ctx.receipt()==doc['runtime']
    ascii_factory=FunctionType(font.make_painter.__code__,{**font.make_painter.__globals__,'CURRENT_ARM9':sha(ctx.arm)},argdefs=font.make_painter.__defaults__)
    diagnostic={}
    source=checked_text(inspect.getsource(painter.make_source_painter),{
        "        assert cpu.reg_read(UC_ARM_REG_R0)==string+len(text) and bytes(cpu.mem_read(string,len(text)+1))==text+b'\\0'":
        "        DIAGNOSTIC.update(return_consumed_bytes=cpu.reg_read(UC_ARM_REG_R0)-string,intended_bytes=len(text),events=events,input_unchanged=bytes(cpu.mem_read(string,len(text)+1))==text+b'\\0')\n        assert cpu.reg_read(UC_ARM_REG_R0)==string+len(text) and bytes(cpu.mem_read(string,len(text)+1))==text+b'\\0'",
    })
    env={**painter.make_source_painter.__globals__,'ASCII_painter':ascii_factory,'CURRENT_ARM9':sha(ctx.arm),'DIAGNOSTIC':diagnostic}
    exec(compile(source,__file__+'::same-original-FE-assertions-return-observer-only','exec'),env)
    paint,calibration=env['make_source_painter'](ctx.image);rows=[];reused=0
    for row in doc['records']:
        if row['kind']!='system-FE':continue
        target=byid[row['id']];found=None
        for directory in ['native_body_v1','native_body_v2']:
            path=ROOT/directory/('complete_'+row['id']+'.json')
            if path.exists():
                proof=load(path)
                if proof['record']['compiled_hex']==target['encoded_hex']:
                    assert proof['all_original_native_glyph_pixels_consumption_canaries_bounds_androw_assertions_pass']
                    found=path;break
        if found:
            rows.append(dict(id=row['id'],passed=True,reused_complete_native_receipt=str(found),receipt_sha256=digest(found)));reused+=1;continue
        raw=bytes.fromhex(target['encoded_hex']);assert raw[0]==254;body=raw[1:]
        for token,value in mac['defaults'].items():body=body.replace(token.encode(),value['text'].encode())
        diagnostic.clear()
        try:
            result=paint(body);check_FE_rows(body,result)
        except AssertionError as exc:
            assert diagnostic and diagnostic['input_unchanged']
            rows.append(dict(id=row['id'],passed=False,compiled_hex=target['encoded_hex'],expanded_hex=body.hex(),
                lines=target['lines'],diagnostic=dict(diagnostic),failure=str(exc)))
        else:rows.append(dict(id=row['id'],passed=True,compiled_hex=target['encoded_hex'],painter_androw_membership_pass=True,
            four_ABI_alignment_andfull_native_receipt_not_provided_by_this_diagnostic=True))
    assert len(rows)==38
    save(out,dict(runtime=ctx.receipt(),records=rows,remaining_FE_scoped_to_demonstrated_auto_wrap_risk=True,
        reused_completed_receipts=reused,original_assertions_preserved=True,observer_source=source,calibration=calibration,
        no_new_fifth_gate_visual_oractual_gameplay_approval=True,new_credit=0,
        evidence={str(p):digest(p) for p in [planpath,docpath,macpath,Path(painter.__file__),Path(__file__)]}))
    print(dict(FE_records=len(rows),reused=reused,failures=[dict(id=r['id'],consumed=r['diagnostic']['return_consumed_bytes'],intended=r['diagnostic']['intended_bytes']) for r in rows if not r['passed']]))


if __name__=='__main__':main()
