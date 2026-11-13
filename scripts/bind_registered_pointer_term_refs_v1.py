"""Bind explicit clean/current pointer terms without claiming new widget gameplay."""
import argparse
import struct
from pathlib import Path
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.qualify_rafael351_item_and_UI_terms_v1 import string
from scripts.registered_editorial_runtime_v2 import RegisteredRuntime
from dk4tool.rom.nds import NdsImage


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    for arg in ['current','specs','out']:ap.add_argument('--'+arg,type=Path,required=True)
    ap.add_argument('--captain',type=int,choices=range(4),required=True)
    args=ap.parse_args();assert not args.out.exists()
    current,specs=map(load,[args.current,args.specs]);runtime=current['runtime']
    ctx=RegisteredRuntime(runtime['release_proof'],runtime['startup_proof'],captain=args.captain)
    assert ctx.receipt()==runtime
    clean=NdsImage.open('work/clean.nds').read_file('/__arm9__.bin');rows=[]
    for spec in specs['records']:
        field=spec['pointer_field'];assert field%4==0
        source=string(clean,struct.unpack_from('<I',clean,field)[0])
        target=string(ctx.raw,struct.unpack_from('<I',ctx.arm,field)[0])
        assert source['text']==spec['Japanese'] and target['text']==spec['English'],spec
        rows.append(dict(spec,source=source,current=target,source_field_hex=clean[field:field+4].hex(),
            current_field_hex=ctx.arm[field:field+4].hex(),current_literal_rebound_to_registered_own_RAM=True))
    assert len(rows)==len({r['pointer_field'] for r in rows})
    save(args.out,dict(runtime=runtime,records=rows,exact_bound_terms=len(rows),
        remaining_unbound_terms=specs.get('remaining_unbound_terms',[]),prose_alias_notes=specs.get('prose_alias_notes',[]),
        static_reference_not_fresh_native_getter_font_orwidget_approval=True,no_new_gameplay_orcredit=True,new_credit=0,
        evidence={str(p):digest(p) for p in [args.current,args.specs,Path(__file__)]}))
    print(dict(exact_bound_terms=len(rows),remaining_unbound_terms=len(specs.get('remaining_unbound_terms',[])),new_credit=0))


if __name__=='__main__':main()
