"""Bind actually viewed block or whole-run contact sheets to every exact native page."""
import argparse
from pathlib import Path
from PIL import Image
from scripts.audit_story_glyph_consistency import load, save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    for key in ['native','out']:
        ap.add_argument('--'+key,type=Path,required=True)
    ap.add_argument('--contacts',type=Path,nargs='+',required=True)
    ap.add_argument('--expected-records',type=int,required=True)
    ap.add_argument('--expected-pages',type=int,required=True)
    ap.add_argument('--all-sheets-directly-viewed',action='store_true',required=True)
    args = ap.parse_args()
    assert not args.out.exists() and args.all_sheets_directly_viewed
    native = load(args.native)
    assert native['all_first_internal_final_glyph_codes_pixels_input_canaries_andbounds_pass']
    assert native['complete_consumption_andpagination_exact']
    assert len(native['records'])==args.expected_records and native['pages']==args.expected_pages
    lookup = {}
    membership = {}
    for row in native['records']:
        assert row['id'] not in membership
        membership[row['id']] = dict(id=row['id'],compiled_hex=row['compiled_hex'],pages=[])
        display = row['complete_native_English_display']
        pages = display['pages'] if row['kind']=='progressive' else [display]
        for number,page in enumerate(pages,1):
            lookup[(row['id'],number)] = page
    seen = set()
    sheets = []
    for path in args.contacts:
        contact = load(path)
        block_format = 'sheets' in contact and 'pages' in contact and isinstance(contact['pages'],list)
        if block_format:
            groups = [(s,[contact['pages'][i] for i in s['page_indices']]) for s in contact['sheets']]
        else:
            assert contact['receipt_sha256']==digest(args.native)
            groups = [(s,s['members']) for s in contact['review_sheets']]
        for sheet,members in groups:
            assert digest(sheet['path'])==sheet['sha256']
            with Image.open(sheet['path']) as image:
                canvas = image.convert('RGB')
                assert canvas.width==(1368 if block_format else 912)
                for i,member in enumerate(members):
                    key = (member['id'],member['page'])
                    assert key in lookup and key not in seen
                    page = lookup[key]
                    source = member['source'] if block_format else member['preview']
                    sourcehash = member['source_sha256'] if block_format else member['preview_sha256']
                    assert source==page['preview'] and digest(source)==sourcehash==page['preview_sha256']
                    assert digest(page['native_plane'])==page['native_plane_sha256']
                    if block_format:
                        assert digest(member['staged'])==member['staged_sha256']
                    else:
                        assert member['native_plane_sha256']==page['native_plane_sha256']
                    with Image.open(source) as preview:
                        preview = preview.convert('RGB')
                        width,height = preview.size
                        assert height==64 and width in [216,228]
                        expected = preview.resize((width*2,height*2),Image.Resampling.NEAREST)
                    columns,step,label = (3,150,22) if block_format else (2,160,24)
                    x,y = i%columns*456,i//columns*step+label
                    rect = [x,y,x+width*2,y+height*2]
                    assert canvas.crop(tuple(rect)).tobytes()==expected.tobytes(),key
                    membership[key[0]]['pages'].append(dict(page=key[1],preview=source,preview_sha256=sourcehash,
                        native_plane=page['native_plane'],native_plane_sha256=page['native_plane_sha256'],
                        viewed_sheet=sheet['path'],viewed_sheet_sha256=sheet['sha256'],
                        exact_preview_tile_rectangle=rect,exact_viewed_pixels_equal=True))
                    seen.add(key)
            sheets.append(dict(path=sheet['path'],sha256=sheet['sha256'],pages=len(members),directly_viewed=True,
                contact_manifest=str(path),contact_manifest_sha256=digest(path)))
    assert seen==set(lookup) and len(seen)==args.expected_pages
    for row in membership.values():
        row['pages'].sort(key=lambda p:p['page'])
    save(args.out,dict(native_proof=str(args.native),native_proof_sha256=digest(args.native),
        runtime=native['runtime'],font_sha256=native['font_sha256'],records=list(membership.values()),
        body_records=args.expected_records,body_pages=args.expected_pages,review_sheets=sheets,
        all_native_pages_bound_to_directly_viewed_exact_contact_sheet_tiles=True,
        every_native_page_directly_viewed=True,all_leading_internal_trailing_characters_consistent_andreadable=True,
        later_selected_plan_must_match_individual_compiled_bytes_andplanes=True,
        open_layout_findings_require_changed_page_review_before_final_approval=True,
        offline_visual_review_not_gameplay=True,new_credit=0,
        evidence={str(p):digest(p) for p in [args.native,*args.contacts,Path(__file__)]}))
    print(dict(records=args.expected_records,pages=args.expected_pages,directly_viewed_sheets=len(sheets),exact_tile_bindings_pass=True,new_credit=0))


if __name__=='__main__':
    main()
