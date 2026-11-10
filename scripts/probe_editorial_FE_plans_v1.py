"""Focused unchanged native FE painter/row probes; not macro,storage orgameplay approval."""
import argparse
from pathlib import Path
from types import FunctionType
from PIL import Image
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load,save
from scripts.registered_editorial_runtime_v2 import RegisteredRuntime
from scripts.check_editorial_compiled_pages_v6 import check_FE_rows
from scripts import square_shopkeeper_font_oracles_v7020 as font
from scripts import Rafael_B45_FE_source_painter_v7894 as native

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    for k in ['manuscript','plan','release','startup','out']:ap.add_argument('--'+k,type=Path,required=True)
    ap.add_argument('--captain',type=int,choices=range(4),required=True);ap.add_argument('--ids',nargs='+',required=True)
    args=ap.parse_args();assert not args.out.exists()
    doc,plans=map(load,[args.manuscript,args.plan]);assert plans['manuscript_sha256']==sha(args.manuscript.read_bytes())
    ctx=RegisteredRuntime(args.release,args.startup,captain=args.captain);assert ctx.receipt()==doc['runtime']
    ascii_factory=FunctionType(font.make_painter.__code__,{**font.make_painter.__globals__,'CURRENT_ARM9':sha(ctx.arm)},argdefs=font.make_painter.__defaults__)
    factory=FunctionType(native.make_source_painter.__code__,{**native.make_source_painter.__globals__,'CURRENT_ARM9':sha(ctx.arm),'ASCII_painter':ascii_factory},argdefs=native.make_source_painter.__defaults__)
    painter,calibration=factory(ctx.image);rows={r['id']:r for r in doc['records']};byid={r['id']:r for r in plans['records']}
    assert len(args.ids)==len(set(args.ids)) and set(args.ids)<=rows.keys() and set(args.ids)<=byid.keys()
    args.out.mkdir(parents=True);cases=[]
    for ident in args.ids:
        row,plan=rows[ident],byid[ident];raw=bytes.fromhex(plan['encoded_hex'])
        assert row['kind']=='system-FE' and row['source_selector']==raw[0]==254
        assert '{MACRO:' not in row['english'] and ' '.join(raw[1:].decode('ascii').split())==row['english']
        case=dict(id=ident,source_reference=row['source_reference'],current_reference=row['current_reference'],compiled_hex=raw.hex(),lines=plan['lines'])
        try:
            rendered=painter(raw[1:])
            case['diagnostic_actual_rows']={str(y):bytes(e['code'] for e in rendered['events'] if e['y']==y).decode('ascii') for y in sorted({e['y'] for e in rendered['events']})}
            case['row_comparison']=check_FE_rows(raw[1:],rendered)
        except AssertionError as exc:case.update(rejected=True,error=str(exc),native_approval=False)
        else:
            path=args.out/(ident+'.bin');path.write_bytes(rendered['physical'])
            pic=Image.new('RGB',(228,64));pic.putdata([(0,8,0) if v else (239,232,201) for v in rendered['physical']]);png=path.with_suffix('.png');pic.save(png)
            rendered.pop('physical');rendered.pop('logical');case.update(rejected=False,rendered=rendered,native_plane=str(path),native_plane_sha256=sha(path.read_bytes()),preview=str(png),preview_sha256=sha(png.read_bytes()))
        cases.append(case);save(args.out/'cases.json',dict(runtime=ctx.receipt(),cases=cases,calibration=calibration,
            all_original_native_assertions_preserved=True,no_macro_storage_or_gameplay_approval=True,new_credit=0,
            evidence={str(p):sha(p.read_bytes()) for p in [args.manuscript,args.plan,Path(__file__)]}))
        print(ident,'FAIL' if case['rejected'] else 'native FE rows/pixels/bounds pass',flush=True)
if __name__=='__main__':main()
