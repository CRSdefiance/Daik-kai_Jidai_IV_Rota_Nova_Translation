"""Capture a concrete FE row mismatch without changing geometry or suppressing its guard."""
from pathlib import Path
from types import FunctionType
from PIL import Image
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load,save
from scripts.registered_editorial_runtime_v2 import RegisteredRuntime
from scripts.source_locked_derivation_v5118 import checked_text
from scripts import check_rafael_compiled_pages_v2 as checked

ROOT=Path('work/analysis/Rafael_B61_B80_formatting_20261104')
RELEASE=Path('work/analysis/Rafael_B51_B60_release_verified_20261104/registered_release_verification.json')

if __name__=='__main__':
    output=ROOT/'Charlotte_FE_R87_row_finding_v1.json';assert not output.exists()
    plan_path=ROOT/'automatic_v5/automatic_plans.json';plan=load(plan_path)
    row=next(r for r in plan['records'] if r['id']=='DK4_MES_B69_R0087')
    raw=bytes.fromhex(row['encoded_hex']);assert raw[0]==254
    ctx=RegisteredRuntime(RELEASE,RELEASE.with_name('own_registered_startup_verification.json'),captain=0)
    macros=load(checked.MACROS)
    adapter=checked_text(macros['source_owned_FE_adapter'],{
        "b'Hodram'":"b'Rafael'","b'Bergstrom'":"b'Castor'","b'Bergstrom Fleet'":"b'Castor Co.'"})
    env=dict(checked.FE_expand.__globals__)
    exec(compile(adapter,__file__+'::same-own-Rafael-null-source-actor-expansion','exec'),env)
    aligned=ctx.execute(env['expand'],raw[1:])
    assert len(aligned['cases'])==4
    body=bytes.fromhex(aligned['cases'][0]['output_hex'])
    assert all(r['output_hex']==body.hex() for r in aligned['cases'])
    ascii_factory=FunctionType(checked.old_font.make_painter.__code__,
        {**checked.old_font.make_painter.__globals__,'CURRENT_ARM9':sha(ctx.arm)},argdefs=checked.old_font.make_painter.__defaults__)
    factory=FunctionType(checked.source_FE.make_source_painter.__code__,
        {**checked.source_FE.make_source_painter.__globals__,'CURRENT_ARM9':sha(ctx.arm),'ASCII_painter':ascii_factory},
        argdefs=checked.source_FE.make_source_painter.__defaults__)
    painter,calibration=factory(ctx.image);rendered=painter(body)
    plane=rendered.pop('physical');logical=rendered.pop('logical')
    assert rendered['all_first_internal_final_ASCII_CP932_codes_andindependent_logical_plane_exact']
    events=rendered['events'];ys=sorted({e['y'] for e in events})
    actual=[dict(y=y,text=bytes(e['code'] for e in events if e['y']==y).decode('ascii')) for y in ys]
    png=ROOT/'Charlotte_FE_R87_row_finding_v1.png'
    picture=Image.new('RGB',(228,64));picture.putdata([(0,8,0) if v else (239,232,201) for v in plane]);picture.resize((912,256),Image.Resampling.NEAREST).save(png)
    save(output,dict(runtime=ctx.receipt(),id=row['id'],compiled_hex=raw.hex(),planned_lines=row['lines'],
        planned_native_y=[12*i for i in range(len(row['lines']))],actual_rows=actual,
        all_glyphs_consumed_but_row_membership_mismatched=True,native_macro_alignments=aligned,
        complete_native_guarded_painter=rendered,calibration=calibration,
        native_physical_sha256=sha(plane),native_logical_sha256=sha(logical),
        preview=str(png),preview_sha256=sha(png.read_bytes()),
        source_owned_FE_default_adapter=adapter,
        no_geometry_code_font_control_orROM_changes=True,no_actual_CG_gameplay_claim=True,
        new_credit=0,evidence={str(p):sha(p.read_bytes()) for p in [plan_path,RELEASE,checked.MACROS,Path(__file__)]}))
    print('Charlotte FE R87 planned:',row['lines'],'actual:',actual,flush=True)
