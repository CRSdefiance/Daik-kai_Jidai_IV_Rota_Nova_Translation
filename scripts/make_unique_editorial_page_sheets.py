"""Review every page while reusing only byte-identical, compatible native planes."""
import argparse
from pathlib import Path
from PIL import Image,ImageDraw
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load,save

def pages(report):
    for record in report['records']:
        rendered=record['complete_native_English_display']
        for number,page in enumerate(rendered['pages'] if record['kind']=='progressive' else [rendered],1):
            plane=Path(page['native_plane']);assert sha(plane.read_bytes())==page['native_plane_sha256']
            preview=Path(page['preview']);assert sha(preview.read_bytes())==page['preview_sha256']
            width=216 if record['kind']=='progressive' else 228
            assert len(plane.read_bytes())==width*64
            yield record,number,page,(record['kind'],width,page['native_plane_sha256'])

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    for arg in ('native','reuse-native','reuse-visual','out'):
        parser.add_argument('--'+arg,type=Path,required=True)
    args=parser.parse_args();assert not args.out.exists()
    current,old,visual=map(load,[args.native,args.reuse_native,args.reuse_visual])
    assert visual['native_sha256']==sha(args.reuse_native.read_bytes())
    assert visual['all_final_pages_directly_viewed_or_exact_plane_reuse']
    assert current['runtime']['ARM9_sha256']==old['runtime']['ARM9_sha256']
    assert current['font_sha256']==old['font_sha256']
    known={}
    for record,number,page,key in pages(old):
        known[key]=dict(id=record['id'],page=number,preview=page['preview'],
            preview_sha256=page['preview_sha256'],prior_visual=str(args.reuse_visual))
    fresh,coverage=[],[];old_count=duplicate_count=0
    for record,number,page,key in pages(current):
        entry=dict(id=record['id'],block=record['block'],page=number,kind=record['kind'],
            native_plane=page['native_plane'],native_plane_sha256=key[-1],
            own_preview=page['preview'],own_preview_sha256=page['preview_sha256'])
        if key in known:
            match=known[key]
            assert Path(match['preview']).read_bytes()==Path(page['preview']).read_bytes()
            entry.update(exact_visual_reuse=match)
            if 'prior_visual' in match:old_count+=1
            else:duplicate_count+=1
        else:
            match=dict(id=record['id'],page=number,preview=page['preview'],preview_sha256=page['preview_sha256'],fresh_unique_index=len(fresh))
            known[key]=match;fresh.append((entry,Image.open(page['preview']).convert('RGB')))
            entry.update(fresh_unique_index=match['fresh_unique_index'])
        coverage.append(entry)
    args.out.mkdir(parents=True);sheets=[]
    for start in range(0,len(fresh),12):
        part=fresh[start:start+12];sheet=Image.new('RGB',(912,((len(part)+1)//2)*160),'#263238');draw=ImageDraw.Draw(sheet)
        for index,(entry,picture) in enumerate(part):
            x,y=index%2*456,index//2*160
            draw.text((x+3,y+3),entry['id']+f' p{entry["page"]} offline QA',fill='white')
            sheet.paste(picture.resize((picture.width*2,128),Image.Resampling.NEAREST),(x,y+24))
        filename=args.out/f'unique_part{start//12+1:02d}.png';sheet.save(filename)
        sheets.append(dict(path=str(filename),sha256=sha(filename.read_bytes()),fresh_unique_indices=list(range(start,start+len(part)))))
    assert len(coverage)==current['pages'] and old_count+duplicate_count+len(fresh)==len(coverage)
    save(args.out/'visual_coverage_pending.json',dict(native=str(args.native),native_sha256=sha(args.native.read_bytes()),
        previous_native=str(args.reuse_native),previous_native_sha256=sha(args.reuse_native.read_bytes()),
        previous_visual=str(args.reuse_visual),previous_visual_sha256=sha(args.reuse_visual.read_bytes()),
        records=coverage,review_sheets=sheets,pages=len(coverage),fresh_unique_pages=len(fresh),
        previously_reviewed_exact_planes=old_count,duplicate_new_planes=duplicate_count,
        only_pixel_identical_same_consumer_size_runtime_andfont_reuse=True,
        changed_text_already_received_fresh_native_checks=True,direct_view_of_fresh_sheets_pending=True,
        actual_gameplay=False,new_credit=0,producer_sha256=sha(Path(__file__).read_bytes())))
    print(dict(pages=len(coverage),fresh_unique_pages=len(fresh),old_exact_reuse=old_count,new_duplicates=duplicate_count,sheets=len(sheets)))

if __name__=='__main__':main()
