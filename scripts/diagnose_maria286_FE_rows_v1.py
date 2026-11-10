"""Focused native diagnostics for the concrete FE row-membership failure."""
from pathlib import Path
from types import FunctionType
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.registered_editorial_runtime_v2 import RegisteredRuntime
from scripts import square_shopkeeper_font_oracles_v7020 as ascii_font
from scripts import Rafael_B45_FE_source_painter_v7894 as native_FE

ROOT=Path('work/Maria_B37_B50_clean_20261109')

def main():
    out=ROOT/'FE_row_diagnostic_v1.json';assert not out.exists()
    plan_path=ROOT/'format_plan_v1/automatic_plans.json';macro_path=ROOT/'formatting_v1/native_macro_measurements.json'
    plan,macros=map(load,[plan_path,macro_path]);runtime=macros['runtime']
    ctx=RegisteredRuntime(runtime['release_proof'],runtime['startup_proof'],captain=3)
    assert ctx.receipt()==runtime
    ascii_factory=FunctionType(ascii_font.make_painter.__code__,{**ascii_font.make_painter.__globals__,'CURRENT_ARM9':sha(ctx.arm)},argdefs=ascii_font.make_painter.__defaults__)
    fe_factory=FunctionType(native_FE.make_source_painter.__code__,{**native_FE.make_source_painter.__globals__,'CURRENT_ARM9':sha(ctx.arm),'ASCII_painter':ascii_factory},argdefs=native_FE.make_source_painter.__defaults__)
    painter,calibration=fe_factory(ctx.image);rows=[]
    for planned in plan['records']:
        if planned['id'] not in ['DK4_MES_B50_R0036','DK4_MES_B50_R0043']:continue
        body=bytes.fromhex(planned['encoded_hex'])[1:]
        for token,value in macros['defaults'].items():body=body.replace(token.encode(),value['text'].encode())
        row=dict(id=planned['id'],planned_lines=planned['lines'],expanded_hex=body.hex(),
            expanded_rows=[v.decode('ascii') for v in body.split(b'\n')])
        try:result=painter(body)
        except AssertionError as e:
            row.update(original_painter_assertion_failed=True,error=str(e),no_glyph_bounds_orcomplete_plane_approval=True)
        else:
            actual={y:bytes(e['code'] for e in result['events'] if e['y']==y).decode('ascii') for y in sorted({e['y'] for e in result['events']})}
            visible={y:bytes(e['code'] for e in result['events'] if e['y']==y and e['code']!=32).decode('ascii') for y in actual}
            row.update(actual_rows=actual,actual_nonspace_codes_by_y=visible,events=result['events'],
                native_complete_glyphs_pixels_bounds_andcanaries_pass=True,
                row_membership_still_requires_resolution=True)
        rows.append(row)
    assert len(rows)==2
    save(out,dict(runtime=runtime,records=rows,calibration=calibration,
        diagnostic_only_no_guard_relaxation_orlayout_approval=True,new_credit=0,
        evidence={str(p):digest(p) for p in [plan_path,macro_path,Path(native_FE.__file__),Path(__file__)]}))
    for row in rows:print({k:v for k,v in row.items() if k not in ['events','expanded_hex']})

if __name__=='__main__':main()
