"""Observe the failed FE row positions through the same guarded native painter."""
from types import FunctionType
from pathlib import Path
from collections import Counter
from scripts import check_editorial_compiled_pages_explicit_captain_v1 as runner
from scripts.registered_editorial_runtime_v2 import RegisteredRuntime
from scripts.meaning_maria335_B137_B151_v1 import ROOT
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest


def main():
    out=ROOT/'FE_B139_R199_diagnostic_v1';assert not out.exists()
    docpath=ROOT/'formatting_v1/formatting_input.json';planpath=ROOT/'plan_continuity_v2/automatic_plans.json'
    doc,plan=map(load,[docpath,planpath]);runtime=doc['runtime'];row=next(r for r in plan['records'] if r['id']=='DK4_MES_B139_R0199')
    ctx=RegisteredRuntime(runtime['release_proof'],runtime['startup_proof'],captain=3);assert ctx.receipt()==runtime
    old=runner.main.__globals__['old_font'];source=runner.main.__globals__['source_FE']
    af=FunctionType(old.make_painter.__code__,{**old.make_painter.__globals__,'CURRENT_ARM9':digest_bytes(ctx.arm)},argdefs=old.make_painter.__defaults__)
    ff=FunctionType(source.make_source_painter.__code__,{**source.make_source_painter.__globals__,'CURRENT_ARM9':digest_bytes(ctx.arm),'ASCII_painter':af},argdefs=source.make_source_painter.__defaults__)
    painter,calibration=ff(ctx.image);expected=bytes.fromhex(row['encoded_hex'])[1:];rendered=painter(expected)
    assert all(e['kind']=='ascii' and e['code']<128 for e in rendered['events'])
    ys=sorted({e['y'] for e in rendered['events']})
    actual=[dict(y=y,ASCII=bytes(e['code'] for e in rendered['events'] if e['y']==y).decode('ascii')) for y in ys]
    out.mkdir();physical=out/'physical.bin';logical=out/'logical.bin'
    physical.write_bytes(rendered.pop('physical'));logical.write_bytes(rendered.pop('logical'))
    save(out/'diagnostic.json',dict(id=row['id'],runtime=runtime,expected_hex=expected.hex(),planned_rows=row['lines'],
        planned_row_lengths=[len(v) for v in row['lines']],actual_rows=actual,source_guarded_native_render=rendered,calibration=calibration,
        physical_plane=str(physical),physical_plane_sha256=digest(physical),logical_plane=str(logical),logical_plane_sha256=digest(logical),
        original_row_membership_failure_not_approved=True,no_ROM_prose_font_orconsumer_changes=True,new_credit=0,
        evidence={str(p):digest(p) for p in [docpath,planpath,Path(__file__)]}))
    print(dict(planned_lengths=[len(v) for v in row['lines']],actual_rows=actual))


def digest_bytes(value):
    from hashlib import sha256
    return sha256(value).hexdigest()


if __name__=='__main__':main()
