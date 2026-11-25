"""Show every verified gameplay page at 2x size without repeated upper-screen scenery."""
import argparse
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from scripts.audit_story_glyph_consistency import load, save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--actual', type=Path, required=True)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    assert not args.out.exists()
    actual = load(args.actual)
    assert actual['all_selected_pages_observed_in_exact_fixture_order']
    assert actual['all_complete_native_body_andheader_planes_andblank_guards_match']
    unique = {}
    for page in actual['body_pages']:
        unique.setdefault((page['id'], page['page']), page)
    ordered = [unique[(row['id'],row['page'])] for row in actual['ordered_selected_source_calls']]
    assert len(ordered) == actual['selected_pages'] == len(unique)
    font = ImageFont.truetype('C:/Windows/Fonts/consola.ttf', 18)
    args.out.mkdir(parents=True)
    sheets = []
    for start in range(0,len(ordered),12):
        pages = ordered[start:start+12]
        sheet = Image.new('RGB',(1536,410*((len(pages)+2)//3)),'#eee')
        draw = ImageDraw.Draw(sheet)
        for index,row in enumerate(pages):
            capture = row['capture']; assert digest(capture['path']) == capture['PNG_sha256']
            x,y = index%3*512,index//3*410
            draw.text((x+4,y+3),row['id'].replace('DK4_MES_','')+f" p{row['page']} @{row['frame']}",font=font,fill='black')
            picture = Image.open(capture['path']).convert('RGB')
            assert picture.size == (256,384)
            sheet.paste(picture.crop((0,192,256,384)).resize((512,384),Image.Resampling.NEAREST),(x,y+26))
        path = args.out/f'body_{len(sheets)+1:02d}.png'; sheet.save(path)
        sheets.append(dict(path=str(path),sha256=digest(path),pages=[dict(id=p['id'],page=p['page'],capture=p['capture']) for p in pages]))
    save(args.out/'sheets.json',dict(actual=str(args.actual),actual_sha256=digest(args.actual),
        pages=len(ordered),sheets=sheets,lower_screen_only=True,all_complete_portrait_header_andbody_areas_included=True,
        direct_view_pending=True,new_credit=0,producer=__file__,producer_sha256=digest(__file__)))
    print('Prepared',len(ordered),'complete lower-screen pages in',len(sheets),'readable sheets.')


if __name__=='__main__':
    main()
