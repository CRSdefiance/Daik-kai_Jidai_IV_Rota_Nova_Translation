"""Bind the four revised item titles to clean pointer fields and Rafael2952 runtime strings."""
from pathlib import Path
import struct

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.audit_story_glyph_consistency import load, save
from scripts.qualify_rafael351_item_and_UI_terms_v1 import string
from scripts.registered_editorial_runtime_v2 import RegisteredRuntime


ROOT=Path('work/analysis/Rafael_B221_B240_current2952_20261106')
CURRENT=ROOT/'current_effective.json'
OUT=ROOT/'item_title_bindings_v1.json'
CATALOGUE=Path('translations/all_item_names_arm9_v1.json')
ITEMS={
    46:('アレスの聖槍','Holy Spear of Ares',['DK4_MES_B230_R0013'],218),
    50:('アルマジロの鉄皮','Armadillo Hide',['DK4_MES_B240_R0023'],228),
    67:('女帝のガウン','Empress Gown',['DK4_MES_B232_R0027','DK4_MES_B232_R0031'],220),
    70:('メデューサの盾','Medusa Shield',['DK4_MES_B236_R0026'],224),
}


def main():
    assert not OUT.exists()
    current, catalogue=map(load,(CURRENT,CATALOGUE))
    rt=current['runtime']
    ctx=RegisteredRuntime(rt['release_proof'],rt['startup_proof'],captain=0)
    assert ctx.receipt()==rt
    clean=NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    catalog={r['id']:r for r in catalogue['records']}
    rows=[]
    evidence_paths=[CURRENT,CATALOGUE,Path(__file__)]
    for ident,(japanese,english,speeches,other_block) in ITEMS.items():
        row=catalog[f'DK4_ITEM_POINTER_{ident:03d}']
        at=row['offset']
        assert clean[at:at+4].hex()==row['source_hex'].lower() and row['english']==english
        source=string(clean,struct.unpack_from('<I',clean,at)[0])
        target=string(ctx.raw,struct.unpack_from('<I',ctx.arm,at)[0])
        assert source['text']==japanese and target['text']==english
        other=Path(f'translations/lil_B{other_block}_contextual_final_review_v1.json')
        matches=[r['id'] for r in load(other)['records'] if english in r.get('english','')]
        assert matches
        evidence_paths.append(other)
        rows.append(dict(item_ID=ident,registered_item_record=row['id'],pointer_field_offset=at,
            source=source,current=target,source_field_hex=clean[at:at+4].hex(),current_field_hex=ctx.arm[at:at+4].hex(),
            scoped_dialogue_ids=speeches,earlier_cross_route_review=str(other),earlier_matching_records=matches))
    save(OUT,dict(runtime=rt,items=rows,read_only=True,inventory_cards_and_acquisition_unvisited=True,new_credit=0,
        evidence={str(p):sha(p.read_bytes()) for p in evidence_paths}))
    print([(r['item_ID'],r['current']['text']) for r in rows])


if __name__=='__main__':
    main()

