"""Read-only native-plane comparisons for focused name, FE, menu and page captures."""
from pathlib import Path
from PIL import Image
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load,save

ROOT=Path('work/analysis/Hodram_B91_B110_actual_pixels_20261101')
BASE=Path('work/emulation_v193')
FOLDERS={91:'Hodram_B91_B110_20261101_B91',104:'Hodram_B91_B110_20261101_B104','decline':'Hodram_B91_B110_20261101_B91_decline'}
NATIVE=Path('work/analysis/Hodram_B91_B110_native_20261101e/compiled_native_pages.json')
NAME=Path('work/analysis/Hodram_B91_B110_name_native_20261101/native_name_fields_verification_reviewed.json')
MENU=Path('work/analysis/Hodram_B91_B110_menu_20261101/menu_provider_and_planes_reviewed.json')

def capture(key,frame):
    path=BASE/FOLDERS[key]/'capture_report.json';report=load(path)
    assert report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
    assert sha(Path(report['ROM']).read_bytes())==report['ROM_sha256']
    row=next(r for r in report['frames_captured'] if r['frame']==frame)
    image=Path(row['path']);assert sha(image.read_bytes())==row['PNG_sha256']
    return Image.open(image).convert('RGB'),dict(frame=frame,capture_report=str(path),capture_report_sha256=sha(path.read_bytes()),capture=row)

def mask(path,digest,width):
    data=Path(path).read_bytes();assert sha(data)==digest
    return {(i%width,i//width) for i,v in enumerate(data) if v}

def match(im,ink,color,xs,ys):
    assert ink
    right=max(x for x,y in ink)+4;bottom=max(y for x,y in ink)+2
    matches=[];best=[]
    for x in xs:
        for y in ys:
            found={(xx-x,yy-y) for yy in range(y,y+bottom) for xx in range(x-2,x+right) if im.getpixel((xx,yy))==color}
            difference=len(ink-found)+len(found-ink);best.append((difference,x,y))
            if not difference:matches.append((x,y))
    assert len(matches)==1,sorted(best)[:3]
    return list(matches[0])

if __name__=='__main__':
    assert not ROOT.exists();ROOT.mkdir(parents=True)
    native,name,menu=map(load,[NATIVE,NAME,MENU]);headers=[];bodies=[];captions=[]
    plane=next(p for p in name['planes'] if p['version']=='proposed' and p['text']=='Fernando Dias' and p['style']==11)
    ink=mask(plane['plane'],plane['plane_sha256'],216)
    for key,frame in [(91,5040),(91,5520),(91,6000),(91,6480),(91,7200),('decline',4800)]:
        im,ref=capture(key,frame);origin=match(im,ink,(98,97,98),[16],[276])
        headers.append(dict(**ref,label='Fernando Dias',origin=origin,normal_F_andall_name_glyphs_andblank_guards_exact=True))
    for key,frame,ident,number in [
        (104,4320,'DK4_MES_B104_R0013',1),(104,4560,'DK4_MES_B104_R0013',2),
        (91,8400,'DK4_MES_B91_R0084',1),(91,8640,'DK4_MES_B91_R0087',1),
        ('decline',5280,'DK4_MES_B91_R0103',1),('decline',5520,'DK4_MES_B91_R0106',1)]:
        row=next(r for r in native['records'] if r['id']==ident)
        rendered=row['complete_native_English_display'];is_FE=row['kind']=='system-FE'
        page=rendered if is_FE else rendered['pages'][number-1]
        ink=mask(page['native_plane'],page['native_plane_sha256'],228 if is_FE else 216)
        im,ref=capture(key,frame);origin=match(im,ink,(8,8,8),range(12,21),range(298,307))
        bodies.append(dict(**ref,id=ident,page=number,origin=origin,kind=row['kind'],complete_native_glyph_plane_andblank_guards_equal=True,
            bounded_framebuffer_alignment_only_no_backing_owner_claim=True))
    vm=menu['versions'][-1]['cases'][0]['native_VM'];width=vm['minimum_width_units']*6;rect=vm['native_menu_rectangle'];x=rect[0]+16
    masks=[mask(p['path'],p['sha256'],width) for p in menu['records'] if p['version']=='reviewed-English' and p['style']==1]
    assert len(masks)==2
    for key,frame,wanted in [(91,4560,0),('decline',4560,0),('decline',4680,1)]:
        im,ref=capture(key,frame);selected=[]
        for i,ink in enumerate(masks):
            y=192+rect[1]+16+20*i
            assert match(im,ink,(8,8,8),[x],[y])==[x,y]
            positions={(xx,yy) for yy in range(y-4,y+16) for xx in range(x,x+width)}-{(x+xx,y+yy) for xx,yy in ink}
            cyan={p for p in positions if im.getpixel(p)==(0,165,172)}
            assert not cyan or cyan==positions
            if cyan:selected.append(i)
            else:assert all(im.getpixel(p)==(205,198,180) for p in positions)
        assert selected==[wanted]
        captions.append(dict(**ref,labels=vm['labels'],selected_option=wanted,both_complete_caption_glyphs_blank_guards_andhighlight_exact=True))
    save(ROOT/'focused_actual_pixels.json',dict(name_headers=headers,body_pages=bodies,menu_samples=captions,
        actual_gameplay=True,disclosed_initialized_fixtures=True,natural_activation=False,hardware_verification=False,
        read_only_framebuffer_comparisons=True,whole_live_RAM_VRAM_backing_palette_orregister_ownership_not_claimed=True,
        Samwell_full_catalogue_UI_unvisited=True,new_credit=0,evidence={str(p):sha(p.read_bytes()) for p in [NATIVE,NAME,MENU,Path(__file__)]}))
    print(dict(name_headers=len(headers),body_pages=len(bodies),menu_samples=len(captions),all_native_pixels_equal=True))
