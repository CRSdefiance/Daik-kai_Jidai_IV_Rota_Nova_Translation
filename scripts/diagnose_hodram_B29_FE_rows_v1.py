"""Inspect the one failed tutorial FE row placement on the unchanged native painter."""
from pathlib import Path
from types import FunctionType
from PIL import Image
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.registered_editorial_runtime import RegisteredRuntime
from scripts import square_shopkeeper_font_oracles_v7020 as old_font
from scripts import Rafael_B45_FE_source_painter_v7894 as source_FE

ROOT=Path('work/Hodram_B0_B41_clean_20261107')
OUT=ROOT/'FE_B29_R112_diagnostic_v1'


def main():
    assert not OUT.exists()
    plan_path=ROOT/'automatic_plans_v2/automatic_plans.json';plan=load(plan_path)
    row=next(r for r in plan['records'] if r['id']=='DK4_MES_B29_R0112')
    runtime=load(ROOT/'current_v1/current_effective.json')['runtime']
    ctx=RegisteredRuntime(runtime['release_proof'],runtime['startup_proof']);assert ctx.receipt()==runtime
    ascii_factory=FunctionType(old_font.make_painter.__code__,{**old_font.make_painter.__globals__,'CURRENT_ARM9':digest_bytes(ctx.arm)},argdefs=old_font.make_painter.__defaults__)
    fe_factory=FunctionType(source_FE.make_source_painter.__code__,{**source_FE.make_source_painter.__globals__,'CURRENT_ARM9':digest_bytes(ctx.arm),'ASCII_painter':ascii_factory},argdefs=source_FE.make_source_painter.__defaults__)
    painter,calibration=fe_factory(ctx.image)
    body=bytes.fromhex(row['encoded_hex'])[1:];rendered=painter(body)
    actual={str(y):bytes(e['code'] for e in rendered['events'] if e['y']==y).decode('ascii') for y in sorted({e['y'] for e in rendered['events']})}
    physical=rendered.pop('physical');logical=rendered.pop('logical')
    OUT.mkdir();(OUT/'physical.bin').write_bytes(physical);(OUT/'logical.bin').write_bytes(logical)
    picture=Image.new('RGB',(228,64));picture.putdata([(0,8,0) if v else (239,232,201) for v in physical])
    picture.resize((912,256),Image.Resampling.NEAREST).save(OUT/'observed_rows.png')
    save(OUT/'diagnostic.json',dict(id=row['id'],plan=str(plan_path),plan_sha256=digest(plan_path),planned_lines=row['lines'],encoded_hex=row['encoded_hex'],
        actual_native_rows=actual,native_painter=rendered,calibration=calibration,runtime=runtime,
        no_ROM_orengine_font_viewport_changes=True,new_credit=0,producer_sha256=digest(__file__)))
    print(dict(planned=row['lines'],actual=actual,source_bound_risk_unresolved=True))


def digest_bytes(raw):
    from hashlib import sha256
    return sha256(raw).hexdigest()


if __name__=='__main__':main()
