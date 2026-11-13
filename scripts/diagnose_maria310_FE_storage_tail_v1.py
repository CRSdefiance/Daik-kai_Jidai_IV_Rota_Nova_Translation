"""Observe exact FE return pointers before unchanged native assertions reject storage padding."""
import inspect
from pathlib import Path
from types import FunctionType
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load,save
from scripts.registered_editorial_runtime_v2 import RegisteredRuntime
from scripts.source_locked_derivation_v5118 import checked_text
from scripts import square_shopkeeper_font_oracles_v7020 as font
from scripts import Rafael_B45_FE_source_painter_v7894 as native
from scripts.meaning_maria_B51_B52_clean_v1 import ROOT

def main():
    out=ROOT/'FE_storage_tail_diagnostic_v1.json';assert not out.exists()
    doc=load(ROOT/'storage_inputs_v1/storage_manuscript.json');runtime=doc['runtime']
    ctx=RegisteredRuntime(runtime['release_proof'],runtime['startup_proof'],captain=3);assert ctx.receipt()==runtime
    af=FunctionType(font.make_painter.__code__,{**font.make_painter.__globals__,'CURRENT_ARM9':sha(ctx.arm)},argdefs=font.make_painter.__defaults__)
    observed=[]
    source=checked_text(inspect.getsource(native.make_source_painter),{
        "        assert cpu.reg_read(UC_ARM_REG_R0)==string+len(text) and bytes(cpu.mem_read(string,len(text)+1))==text+b'\\0'":
        """        OBSERVATIONS.append(dict(input_hex=text.hex(),input_length=len(text),return_offset=cpu.reg_read(UC_ARM_REG_R0)-string,
            input_andterminator_after_hex=bytes(cpu.mem_read(string,len(text)+1)).hex(),events=events,
            final_guard_after_hex=bytes(cpu.mem_read(string+len(text)+1,16)).hex()))
        assert cpu.reg_read(UC_ARM_REG_R0)==string+len(text) and bytes(cpu.mem_read(string,len(text)+1))==text+b'\\0'""",
    })
    env={**native.make_source_painter.__globals__,'CURRENT_ARM9':sha(ctx.arm),'ASCII_painter':af,'OBSERVATIONS':observed}
    exec(compile(source,__file__+'::read-only-return-observer-all-original-assertions-retained','exec'),env)
    paint,calibration=env['make_source_painter'](ctx.image)
    rebuilt=load(ROOT/'reconstruction_v1/reconstruction.json');rows=[t for g in rebuilt['groups'] for t in g['text_records'] if t['id'] in ['DK4_MES_B54_R0491','DK4_MES_B54_R0507']]
    cases=[]
    for row in rows:
        body=bytes.fromhex(row['compiled_hex'])[1:]
        for extra in range(4):
            text=body+b' '*extra;case=dict(id=row['id'],extra_trailing_spaces=extra)
            start=len(observed)
            try:result=paint(text)
            except AssertionError as exc:case.update(rejected=True,error=str(exc))
            else:case.update(rejected=False,all_original_assertions_pass=True)
            assert len(observed)==start+1
            case.update(observed[-1]);case['actual_rows']={str(y):bytes(e['code'] for e in case['events'] if e['y']==y).decode('ascii') for y in sorted({e['y'] for e in case['events']})}
            cases.append(case)
    save(out,dict(runtime=runtime,cases=cases,source_owned_observer=source,all_original_assertions_retained=True,
        no_ROM_data_orapproval_change=True,no_new_images_generated=True,new_credit=0))
    for r in cases:print(r['id'],r['extra_trailing_spaces'],'len',r['input_length'],'return',r['return_offset'],'rejected',r['rejected'],'tailcodes',[e['code'] for e in r['events'][-4:]])
if __name__=='__main__':main()
