"""Inspect all FE row events after a concrete native line-membership failure; never waive it."""
import argparse
from pathlib import Path
from types import FunctionType
from scripts import check_rafael_compiled_pages_v2 as native
from scripts.audit_story_glyph_consistency import load,save
from scripts.registered_editorial_runtime_v2 import RegisteredRuntime
from dk4tool.patch.grand_race_menu_release import sha

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    for name in ['plan','release','startup','out']:
        parser.add_argument('--'+name,type=Path,required=True)
    args=parser.parse_args();assert not args.out.exists()
    ctx=RegisteredRuntime(args.release,args.startup,captain=0)
    ascii_factory=FunctionType(native.old_font.make_painter.__code__,
        {**native.old_font.make_painter.__globals__,'CURRENT_ARM9':sha(ctx.arm)},argdefs=native.old_font.make_painter.__defaults__)
    factory=FunctionType(native.source_FE.make_source_painter.__code__,
        {**native.source_FE.make_source_painter.__globals__,'CURRENT_ARM9':sha(ctx.arm),'ASCII_painter':ascii_factory},
        argdefs=native.source_FE.make_source_painter.__defaults__)
    paint,calibration=factory(ctx.image);rows=[]
    for planned in load(args.plan)['records']:
        if planned['kind']!='system-FE':continue
        body=bytes.fromhex(planned['encoded_hex'])[1:]
        assert not any(m in body for m in [b'FI',b'FA',b'FO'])
        row=dict(id=planned['id'],compiled_body_hex=body.hex(),planned_lines=planned['lines'])
        try:
            rendered=paint(body)
            try:
                membership=native.check_FE_rows(body,rendered)
                row.update(planned_native_rows_pass=True,row_membership=membership)
            except AssertionError as error:
                row.update(planned_native_rows_pass=False,assertion=str(error),
                    actual_visible_rows={str(y):bytes(e['code'] for e in rendered['events'] if e['y']==y).strip(b' ').decode('ascii')
                        for y in sorted({e['y'] for e in rendered['events']})})
            row.update(complete_visible_codes_native_canaries_pixels_andbounds_pass=True,
                native_events=rendered['events'],physical_plane_sha256=sha(rendered['physical']),logical_plane_sha256=sha(rendered['logical']))
        except AssertionError as error:
            row.update(planned_native_rows_pass=False,source_painter_assertion=str(error),complete_visible_codes_native_canaries_pixels_andbounds_pass=False)
        rows.append(row)
    save(args.out,dict(plan=str(args.plan),plan_sha256=sha(args.plan.read_bytes()),runtime=ctx.receipt(),records=rows,
        failed_IDs=[r['id'] for r in rows if not r['planned_native_rows_pass']],
        original_native_checker_not_relaxed=True,original_228px_geometry_andfont_unchanged=True,
        no_whole_batch_pass_no_formatting_approval=True,new_credit=0))
    for row in rows:
        if not row['planned_native_rows_pass']:print(row['id'],row['planned_lines'],row.get('actual_visible_rows'),row.get('source_painter_assertion'))
    print(dict(FE_records=len(rows),failures=sum(not r['planned_native_rows_pass'] for r in rows),new_credit=0))

if __name__=='__main__':main()
