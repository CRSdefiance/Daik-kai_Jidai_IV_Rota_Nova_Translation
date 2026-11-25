"""Bind selected Japanese item names to registered pointer labels on an exact own runtime."""
import argparse
from pathlib import Path
import struct
from dk4tool.rom.nds import NdsImage
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.registered_editorial_runtime_v2 import RegisteredRuntime
from scripts.qualify_rafael351_item_and_UI_terms_v1 import string

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    for arg in ['current','meanings','out']:ap.add_argument('--'+arg,type=Path,required=True)
    ap.add_argument('--captain',type=int,choices=range(4),required=True)
    ap.add_argument('--non-items',nargs='*',default=[])
    args=ap.parse_args();assert not args.out.exists()
    current,meanings=map(load,[args.current,args.meanings]);runtime=current['runtime']
    ctx=RegisteredRuntime(runtime['release_proof'],runtime['startup_proof'],captain=args.captain);assert ctx.receipt()==runtime
    clean=NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    wanted=set(meanings['explicit_pending_term_bindings'])-set(args.non_items)
    assert set(args.non_items)<=set(meanings['explicit_pending_term_bindings'])
    path=Path('translations/all_item_names_arm9_v1.json');items=[]
    for row in load(path)['records']:
        if 'english' not in row:continue
        at=row['offset'];sp,cp=[struct.unpack_from('<I',raw,at)[0] for raw in [clean,ctx.arm]]
        a=string(clean,sp)
        if a['text'] not in wanted:continue
        b=string(ctx.raw,cp);assert b['text']==row['english']
        assert clean[at:at+4].hex().lower()==row['source_hex'].lower()
        items.append(dict(pointer_field_offset=at,registered_record=row['id'],source=a,current=b,
            source_field_hex=clean[at:at+4].hex(),current_field_hex=ctx.arm[at:at+4].hex(),
            dependent_source_ids=[r['id'] for r in meanings['records'] if a['text'] in r['source_Japanese']]))
    assert len(items)==len(wanted) and {r['source']['text'] for r in items}==wanted
    ui=[]
    if '精神' in args.non_items:
        at=0x1483a8;sp,cp=[struct.unpack_from('<I',raw,at)[0] for raw in [clean,ctx.arm]]
        a,b=string(clean,sp),string(ctx.raw,cp);assert a['text']=='精神' and b['text']=='Spirit'
        ui.append(dict(pointer_field_offset=at,source=a,current=b,source_field_hex=clean[at:at+4].hex(),current_field_hex=ctx.arm[at:at+4].hex()))
    save(args.out,dict(runtime=runtime,items=items,UI=ui,non_item_terms=args.non_items,
        exact_registered_item_andstat_references_only=True,no_new_editorial_font_oractual_gameplay_approval=True,new_credit=0,
        evidence={str(p):digest(p) for p in [args.current,args.meanings,path,Path(__file__)]}))
    print([(r['source']['text'],r['current']['text']) for r in items]);print('UI',[(r['source']['text'],r['current']['text']) for r in ui])

if __name__=='__main__':main()
