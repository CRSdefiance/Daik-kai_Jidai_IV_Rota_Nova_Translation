"""Compare the exact stored padding failure with its approved unpadded native plane."""
from types import FunctionType
from pathlib import Path
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from dk4tool.patch.grand_race_menu_release import sha
from scripts.registered_editorial_runtime_v2 import RegisteredRuntime
from scripts import square_shopkeeper_font_oracles_v7020 as font
from scripts import Rafael_B45_FE_source_painter_v7894 as native
from scripts.check_editorial_compiled_pages_v6 import check_FE_rows

ROOT=Path('work/Maria_B152_B175_clean_20261109')


def main():
    out=ROOT/'FE_storage_diagnostic_v1.json';assert not out.exists()
    rebuiltpath=ROOT/'reconstruction_v1/reconstruction.json';rebuilt=load(rebuiltpath)
    doc=load(rebuilt['manuscript']);prior=load(rebuilt['native']);runtime=doc['runtime']
    ctx=RegisteredRuntime(runtime['release_proof'],runtime['startup_proof'],captain=3);assert ctx.receipt()==runtime
    af=FunctionType(font.make_painter.__code__,{**font.make_painter.__globals__,'CURRENT_ARM9':sha(ctx.arm)},argdefs=font.make_painter.__defaults__)
    ff=FunctionType(native.make_source_painter.__code__,{**native.make_source_painter.__globals__,'CURRENT_ARM9':sha(ctx.arm),'ASCII_painter':af},argdefs=native.make_source_painter.__defaults__)
    paint,calibration=ff(ctx.image)
    group=next(g for g in rebuilt['groups'] if g['block']==164)
    row=next(r for r in group['text_records'] if r['id']=='DK4_MES_B164_R0099')
    old=next(r for r in prior['records'] if r['id']==row['id'])
    assert row['parity_space_added'] and row['stored_hex']==row['compiled_hex']+'20'
    assert bytes.fromhex(row['compiled_hex'])[0]==254
    cases=[]
    for label,raw in [('compiled-approved',row['compiled_hex']),('stored-extra-space',row['stored_hex'])]:
        body=bytes.fromhex(raw)[1:];result=paint(body)
        try:rows=check_FE_rows(body,result)
        except AssertionError:passed=False;rows=None
        else:passed=True
        actual=[dict(y=y,ASCII=bytes(e['code'] for e in result['events'] if e['y']==y).decode('ascii')) for y in sorted({e['y'] for e in result['events']})]
        physical=result.pop('physical');logical=result.pop('logical')
        if label=='compiled-approved':
            assert passed and sha(physical)==old['complete_native_English_display']['native_plane_sha256']
        else:assert not passed and len(actual)>1
        cases.append(dict(version=label,body_hex=body.hex(),native_row_membership_pass=passed,actual_rows=actual,
            physical_sha256=sha(physical),logical_sha256=sha(logical),native_assertions=result,planned_native_row_comparison=rows))
    save(out,dict(id=row['id'],runtime=runtime,cases=cases,calibration=calibration,
        source_reference=old['source_reference'],current_reference=old['current_reference'],
        exact_stored_alignment_space_causes_extra_row=True,unpadded_compiled_plane_matches_directly_viewed_native_plane=True,
        qualified_storage_helper='dk4tool/script/reviewed_FE_storage_padding_v1.py',
        no_ROM_prose_font_geometry_orapproval_changes=True,actual_gameplay=False,new_credit=0,
        evidence={str(p):digest(p) for p in [rebuiltpath,Path(rebuilt['native']),Path('dk4tool/script/reviewed_FE_storage_padding_v1.py'),Path(__file__)]}))
    print([(c['version'],c['native_row_membership_pass'],c['actual_rows']) for c in cases])


if __name__=='__main__':main()
