"""Pack complete native previews into legible, hash-bound review sheets."""
import argparse
from pathlib import Path

from PIL import Image, ImageDraw

from scripts.audit_story_glyph_consistency import load, save
from scripts.plan_rafael_B201_B220_v1 import ROOT, digest


PAPER = (239,232,201)
COLORS = {0:PAPER,1:(0,8,0),15:(98,97,98)}


def read_image(path, expected):
    assert digest(path) == expected
    with Image.open(path) as picture:
        return picture.convert('RGB')


def sheet_batch(out, items, *, columns, columns_width, row_height, max_rows, scale):
    out.mkdir()
    receipts = []
    chunk = columns * max_rows
    for start in range(0,len(items),chunk):
        group = items[start:start+chunk]
        height = ((len(group)+columns-1)//columns) * row_height
        sheet = Image.new('RGB',(columns * columns_width,height),'#263238')
        pen = ImageDraw.Draw(sheet)
        for index, (label, picture, proof) in enumerate(group):
            x,y = index%columns*columns_width, index//columns*row_height
            width,height = picture.width*scale,picture.height*scale
            assert width+8 <= columns_width and height+20 <= row_height
            pen.text((x+4,y+2),label,fill='white')
            sheet.paste(picture.resize((width,height),Image.Resampling.NEAREST),(x+4,y+18))
        path = out/f'review_{start//chunk+1:02d}.png'
        sheet.save(path)
        receipts.append(dict(path=str(path),sha256=digest(path),included=[proof for _,_,proof in group]))
    return receipts


def body(out, receipt):
    doc = load(receipt)
    items = []
    for row in doc['records']:
        display = row['complete_native_English_display']
        pages = [display] if row['kind']=='system-FE' else display['pages']
        for index,page in enumerate(pages,1):
            pic = read_image(page['preview'],page['preview_sha256'])
            assert pic.size == ((228,64) if row['kind']=='system-FE' else (216,64))
            items.append((f"{row['id']} {'FE' if row['kind']=='system-FE' else 'page '+str(index)}",
                pic,dict(id=row['id'],page=index,preview=page['preview'],preview_sha256=page['preview_sha256'])))
    assert len(items)==doc['pages']
    sheets = sheet_batch(out,items,columns=3,columns_width=468,row_height=148,max_rows=8,scale=2)
    save(out/'sheet_index.json',dict(native_receipt=str(receipt),native_receipt_sha256=digest(receipt),
        sheets=sheets,pages=len(items),complete_source_planes_without_crop=True,direct_review_pending=True))


def support(out):
    two = ROOT/'two_choice_native_v1/complete_choice_objects.json'
    menus = [(f"B{o['block']}_C{o['source_command_offset']}",Path(o['receipt']))
             for o in load(two)['objects']]
    menus.append(('B209_C230',ROOT/'three_choice_native_v1/menu_provider_and_planes.json'))
    items = []
    for stem, receipt in menus:
        for row in load(receipt)['records']:
            if row['version'] != 'reviewed-English':
                continue
            path = Path(row['path'])
            assert digest(path) == row['sha256']
            pixels = path.read_bytes()
            size = row['logical_width_px'],row['logical_height_px']
            assert len(pixels) == size[0]*size[1]
            picture = Image.new('RGB',size)
            palette = {**COLORS,row['style']:(0,8,0) if row['style']==1 else (78,77,78)}
            picture.putdata([palette[v] for v in pixels])
            label = f"{stem} choice {row['option']+1} / style {row['style']} | {row['text']}"
            items.append((label,picture,dict(source_object=stem,option=row['option'],style=row['style'],
                plane=row['path'],plane_sha256=row['sha256'])))
    assert len(items)==42
    sheets=sheet_batch(out,items,columns=3,columns_width=380,row_height=62,max_rows=8,scale=3)
    save(out/'sheet_index.json',dict(sheets=sheets,caption_style_planes=len(items),
        direct_review_pending=True,evidence={str(path):digest(path) for _,path in menus}))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out',required=True,type=Path)
    parser.add_argument('--body',type=Path)
    args = parser.parse_args()
    if args.body:
        body(args.out,args.body)
    else:
        support(args.out)

