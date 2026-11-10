"""Diagnose exact FE glyph-row mismatches using the unchanged current native painter."""
import argparse
from pathlib import Path
from types import FunctionType
from collections import defaultdict
from PIL import Image,ImageDraw
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load,save
from scripts.registered_editorial_runtime_v2 import RegisteredRuntime
from scripts import square_shopkeeper_font_oracles_v7020 as old_font
from scripts import Rafael_B45_FE_source_painter_v7894 as source_FE
from scripts.check_editorial_compiled_pages_v6 import check_FE_rows

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    for key in ['manuscript','plan','identity','out']:parser.add_argument('--'+key,type=Path,required=True)
    args=parser.parse_args();assert not args.out.exists()
    doc,plan,identity=map(load,[args.manuscript,args.plan,args.identity])
    assert plan['manuscript_sha256']==sha(args.manuscript.read_bytes())
    ctx=RegisteredRuntime(identity['runtime']['release_proof'],identity['runtime']['startup_proof'],captain=0)
    assert ctx.receipt()==identity['runtime'] and doc['current_ROM_sha256']==ctx.receipt()['candidate_sha256']
    ascii_factory=FunctionType(old_font.make_painter.__code__,{**old_font.make_painter.__globals__,'CURRENT_ARM9':sha(ctx.arm)},argdefs=old_font.make_painter.__defaults__)
    factory=FunctionType(source_FE.make_source_painter.__code__,{**source_FE.make_source_painter.__globals__,'CURRENT_ARM9':sha(ctx.arm),'ASCII_painter':ascii_factory},argdefs=source_FE.make_source_painter.__defaults__)
    painter,calibration=factory(ctx.image)
    planned={r['id']:r for r in plan['records']};args.out.mkdir(parents=True)
    records=[];pictures=[]
    for row in doc['records']:
        if row['kind']!='system-FE':continue
        raw=bytes.fromhex(planned[row['id']]['encoded_hex']);assert raw[0]==254
        body=raw[1:];assert not any(v in body for v in [b'FI',b'FA',b'FO',b'FU'])
        rendered=painter(body);actual=defaultdict(bytearray)
        for event in rendered['events']:actual[event['y']].append(event['code'])
        try:membership=check_FE_rows(body,rendered);failure=None
        except AssertionError as error:membership=None;failure=repr(error)
        plane=rendered.pop('physical');logical=rendered.pop('logical')
        binary=args.out/(row['id']+'.bin');binary.write_bytes(plane)
        pic=Image.new('RGB',(228,64));pic.putdata([(0,8,0) if v else (239,232,201) for v in plane])
        png=binary.with_suffix('.png');pic.save(png);pictures.append((row['id'],pic))
        records.append(dict(id=row['id'],source_reference=row['source_reference'],current_reference=row['current_reference'],
            logical_English=row['english'],compiled_hex=raw.hex(),planned_rows=[b.decode('ascii') for b in body.split(b'\n')],
            actual_rows={str(y):bytes(v).decode('ascii') for y,v in actual.items()},row_membership=membership,
            row_membership_failure=failure,native_complete_glyph_andindependent_pixel_report=rendered,
            native_plane=str(binary),native_plane_sha256=sha(plane),preview=str(png),preview_sha256=sha(png.read_bytes())))
    sheet=Image.new('RGB',(920,160*((len(pictures)+1)//2)),'#263238');draw=ImageDraw.Draw(sheet)
    for i,(label,pic) in enumerate(pictures):
        x,y=(i%2)*460,(i//2)*160;draw.text((x+3,y+3),label+' diagnostic',fill='white');sheet.paste(pic.resize((456,128),Image.Resampling.NEAREST),(x,y+24))
    png=args.out/'FE_diagnostic_sheet.png';sheet.save(png)
    save(args.out/'FE_row_diagnostics.json',dict(runtime=ctx.receipt(),manuscript=str(args.manuscript),manuscript_sha256=sha(args.manuscript.read_bytes()),
        plan=str(args.plan),plan_sha256=sha(args.plan.read_bytes()),records=records,calibration=calibration,
        review_sheet=str(png),review_sheet_sha256=sha(png.read_bytes()),
        failed_IDs=[r['id'] for r in records if r['row_membership_failure']],no_rendering_guard_removed_or_ROM_written=True,
        diagnostic_not_a_complete_formatted_batch_or_gameplay_approval=True,new_credit=0,
        evidence={str(p):sha(p.read_bytes()) for p in [args.manuscript,args.plan,args.identity,Path(source_FE.__file__),Path(old_font.__file__),Path(__file__)]}))
    print([(r['id'],r['planned_rows'],r['actual_rows'],not r['row_membership_failure']) for r in records])
