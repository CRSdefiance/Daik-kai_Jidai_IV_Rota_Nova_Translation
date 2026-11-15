"""Select the final native pages and render only changed pages for fresh visual review."""
from pathlib import Path

from scripts.audit_story_glyph_consistency import load, save
from scripts.pack_rafael_B201_B220_review_sheets_v1 import read_image, sheet_batch
from scripts.plan_rafael_B201_B220_v1 import ROOT, digest
from scripts.source_locked_derivation_v5118 import checked_text


PARENT = Path(__file__).with_name('assemble_rafael_B201_B220_offline_v1.py')
BEFORE = ROOT/'offline_display_package_v1/compiled_native_pages.json'
AFTER = ROOT/'offline_display_package_v2/compiled_native_pages.json'
OUT_DIFF = ROOT/'body_visual_final_delta_v1'
source = checked_text(PARENT.read_text(encoding='utf-8'), {
    'from scripts.refine_rafael_B201_B220_wraps_v2 import OUT as MANUSCRIPT':
        'from scripts.refine_rafael_B201_B220_wraps_v6 import MANUSCRIPT',
    "OUT = ROOT/'offline_display_package_v1'": "OUT = ROOT/'offline_display_package_v2'",
    "PLAN = ROOT/'ordinary_plans_v4/automatic_plans.json'": "PLAN = ROOT/'ordinary_plans_v7/automatic_plans.json'",
    "'ordinary_native_v1','ordinary_native_delta_v1','ordinary_native_delta_v2')":
        "'ordinary_native_v1','ordinary_native_delta_v1','ordinary_native_delta_v2',\n    'ordinary_native_delta_v3','ordinary_native_delta_v4','ordinary_native_delta_v5')",
    '==[(381,382),(11,13),(2,2)]':'==[(381,382),(11,13),(2,2),(14,14),(2,2),(1,1)]',
    '(381+11+2+2)*4':'(381+11+2+14+2+1+2)*4',
    "if __name__ == '__main__':\n    main()":'',
})
scope={**globals(),'__file__':__file__}
exec(compile(source,__file__+'::select-final-revised-and-staged-body-pages', 'exec'),scope)


def pages(native):
    result={}
    for r in load(native)['records']:
        display=r['complete_native_English_display']
        group=[display] if r['kind']=='system-FE' else display['pages']
        for i,p in enumerate(group,1):
            result[(r['id'],i)]=p
    return result


def pack_delta():
    before,after=map(pages,(BEFORE,AFTER))
    assert list(before)==list(after) and len(after)==383
    items=[]
    reused=[]
    for key,page in after.items():
        old=before[key]
        ident,index=key
        path=Path(page['preview'])
        assert digest(path)==page['preview_sha256']
        assert digest(Path(old['preview']))==old['preview_sha256']
        if old['preview_sha256']==page['preview_sha256']:
            reused.append(dict(id=ident,page=index,preview_sha256=page['preview_sha256']))
            continue
        image=read_image(path,page['preview_sha256'])
        items.append((f'{ident} page {index}',image,
            dict(id=ident,page=index,preview=str(path),preview_sha256=page['preview_sha256'])))
    assert len(items)==14 and len(reused)==369
    sheets=sheet_batch(OUT_DIFF,items,columns=3,columns_width=468,row_height=148,max_rows=8,scale=2)
    save(OUT_DIFF/'sheet_index.json',dict(sheets=sheets,pages=len(items),unchanged_pages=reused,
        before=str(BEFORE),before_sha256=digest(BEFORE),after=str(AFTER),after_sha256=digest(AFTER),
        direct_review_pending=True))


if __name__=='__main__':
    scope['main']()
    pack_delta()

