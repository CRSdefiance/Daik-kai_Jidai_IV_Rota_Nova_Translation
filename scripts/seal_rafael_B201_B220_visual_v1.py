"""Seal every directly inspected final preview and the exact mixed-object rebuild inputs."""
from pathlib import Path

from scripts.assemble_rafael_B201_B220_offline_v2 import AFTER, BEFORE, OUT_DIFF, pages
from scripts.audit_story_glyph_consistency import load, save
from scripts.plan_rafael_B201_B220_v1 import ROOT, digest


OUT=AFTER.parent
NAMES=ROOT/'scoped_name_planes_v1/native_name_planes.json'
BODY=ROOT/'body_visual_final_v1/sheet_index.json'
CAPTIONS=ROOT/'caption_visual_sheets_v1/sheet_index.json'
DELTA=OUT_DIFF/'sheet_index.json'


def checked_sheets(doc, field, count):
    sheets=doc[field]
    assert len(sheets)==count
    assert all(digest(Path(sheet['path']))==sheet['sha256'] for sheet in sheets)
    return sheets


def main():
    assert not (OUT/'visual_review.json').exists() and not (OUT/'menu.json').exists()
    body,delta,captions,names,native,menu=map(load,(BODY,DELTA,CAPTIONS,NAMES,AFTER,OUT/'menu_before_visual.json'))
    assert body['native_receipt_sha256']==delta['before_sha256']==digest(BEFORE)
    assert delta['after_sha256']==digest(AFTER)
    body_sheets=checked_sheets(body,'sheets',16)
    delta_sheets=checked_sheets(delta,'sheets',1)
    caption_sheets=checked_sheets(captions,'sheets',2)
    name_sheets=checked_sheets(names,'review_sheets',3)
    by_key=lambda rows:{(r['id'],r['page']):r['preview_sha256'] for r in rows}
    viewed=by_key(r for sheet in body_sheets for r in sheet['included'])
    changed=by_key(r for sheet in delta_sheets for r in sheet['included'])
    unchanged=by_key(delta['unchanged_pages'])
    final={key:p['preview_sha256'] for key,p in pages(AFTER).items()}
    assert len(viewed)==len(final)==383 and len(changed)==14 and len(unchanged)==369
    assert viewed.keys()==final.keys() and changed.keys().isdisjoint(unchanged)
    assert {key:viewed[key] for key in unchanged}==unchanged
    assert changed | unchanged == final
    assert sum(len(s['included']) for s in caption_sheets)==42 and sum(s['strings'] for s in name_sheets)==29
    assert native['pages']==383 and len(native['records'])==382 and len(menu['menus'])==10
    assert (names['scoped_actors'],names['fresh_name_planes'],names['exact_reused_name_planes'])==(41,18,11)
    assert names['all_scoped_progressive_names_ASCII_complete_andfit_native216px']
    for entry in menu['menus']:
        native_receipt=Path(entry['native_receipt'])
        assert digest(native_receipt)==entry['native_receipt_sha256']
        if 'versions' not in entry:
            receipt=load(native_receipt)
            assert receipt['native_choice_object_hex']==entry['target_object_hex']
            entry['versions']=receipt['versions']
    save(OUT/'menu.json',{**menu,'offline_visual_approved':True,'direct_view_pending':False,
        'caption_visual_sheets':str(CAPTIONS),'caption_visual_sheets_sha256':digest(CAPTIONS)})
    shared={key:native[key] for key in ('manuscript','manuscript_sha256','plan','plan_sha256','runtime','new_credit')}
    save(OUT/'visual_review.json',{**shared,'native':str(AFTER),'native_sha256':digest(AFTER),'body_pages':383,
        'fresh_final_body_pages':14,'exact_prior_page_images_reused':369,'source_staged_FE_pages':2,
        'source_FE_pages':34,'scoped_name_count':41,'distinct_scoped_name_strings':29,
        'typed_choice_captions':21,'reviewed_caption_style_planes':42,'all_body_and_name_sheets_directly_viewed':True,
        'all_final_body_caption_and_name_sheets_directly_viewed':True,'all_final_direct_visual_findings_resolved':True,
        'actual_gameplay':False,'stored_branch_loader_and_gameplay_checks_pending':True,
        'sheets':body_sheets+delta_sheets+caption_sheets+name_sheets,'names':str(NAMES),'names_sha256':digest(NAMES),
        'evidence':{str(p):digest(p) for p in (BODY,DELTA,CAPTIONS,NAMES,BEFORE,AFTER,OUT/'menu.json',Path(__file__))}})
    print('Sealed 383 directly inspected final dialogue pages, 42 caption style planes, and 29 distinct name strings.')


if __name__=='__main__':
    main()

