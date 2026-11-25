"""Read-only comparison of actual name, menu and page glyphs against native planes."""
from pathlib import Path
from PIL import Image
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load,save

ROOT=Path('work/analysis/Hodram_B81_B89_actual_pixels_20261101')
NAME=Path('work/analysis/Emilio_name_glyph_native_20261101/native_name_glyph_verification_reviewed.json')
MENU=Path('work/analysis/Hodram_B87_menu_20261101/menu_provider_and_planes_reviewed.json')
NATIVE=Path('work/analysis/Hodram_B81_B89_native_20261101c/compiled_native_pages.json')
FOLDERS={84:'Hodram_B81_B89_B84_20261101',85:'Hodram_B81_B89_B85_20261101',87:'Hodram_B81_B89_B87_20261101','decline':'Hodram_B87_decline_20261101'}

def capture(key,frame):
    folder=Path('work/emulation_v193')/FOLDERS[key];path=folder/'capture_report.json';report=load(path)
    assert report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
    assert sha(Path(report['ROM']).read_bytes())==report['ROM_sha256']
    row=next(r for r in report['frames_captured'] if r['frame']==frame)
    pic=Path(row['path']);assert sha(pic.read_bytes())==row['PNG_sha256']
    return Image.open(pic).convert('RGB'),dict(frame=frame,capture_report=str(path),capture_report_sha256=sha(path.read_bytes()),capture=row)

def plane_mask(path,digest,width):
    raw=Path(path).read_bytes();assert sha(raw)==digest
    return {(i%width,i//width) for i,v in enumerate(raw) if v}

if __name__=='__main__':
    assert not ROOT.exists();ROOT.mkdir(parents=True)
    name,menu,native=map(load,[NAME,MENU,NATIVE]);names=[];menus=[];bodies=[]
    target=next(p for p in name['planes'] if p['version']=='proposed')
    ink=plane_mask(target['plane'],target['plane_sha256'],216)
    for frame in [6720,7200,11520,12240,12720,13200,13680,13920]:
        im,ref=capture(84,frame);origin=(16,276);xx,yy=origin
        found={(x-xx,y-yy) for y in range(yy,yy+13) for x in range(xx-4,xx+80) if im.getpixel((x,y))==(98,97,98)}
        assert found==ink,('name',frame,len(ink-found),len(found-ink))
        names.append(dict(**ref,caption_origin=list(origin),label='Emilio Ferog',complete_name_ink_andblank_guards_exact=True))
    vm=menu['versions'][-1]['cases'][0]['native_VM'];width=vm['minimum_width_units']*6
    rect=vm['native_menu_rectangle'];x=rect[0]+16;assert x==(256-width)//2
    masks=[plane_mask(p['path'],p['sha256'],width) for p in menu['records'] if p['version']=='reviewed-English' and p['style']==1]
    assert len(masks)==2
    for key,frame in [(87,5520),('decline',5500),('decline',5520),('decline',5540),('decline',5580),('decline',5620),('decline',5660)]:
        im,ref=capture(key,frame);selected=[];captions=[]
        for option,ink in enumerate(masks):
            y=192+rect[1]+16+20*option
            found={(xx-x,yy-y) for yy in range(y-1,y+13) for xx in range(x-2,x+width+2) if im.getpixel((xx,yy))==(8,8,8)}
            assert found==ink,('menu',key,frame,option,len(ink-found),len(found-ink))
            positions={(xx,yy) for yy in range(y-4,y+16) for xx in range(x,x+width)}-{(x+xx,y+yy) for xx,yy in ink}
            cyan={p for p in positions if im.getpixel(p)==(0,165,172)}
            assert not cyan or cyan==positions
            background=(0,165,172) if cyan else (205,198,180)
            assert all(im.getpixel(p)==background for p in positions)
            if cyan:selected.append(option)
            captions.append(dict(option=option,label=vm['labels'][option],complete_caption_glyphs_andblank_guards_exact=True,
                background_andhighlight_exact=True,highlight_visible=bool(cyan)))
        assert len(selected)<=1
        if key=='decline' and frame==5500:assert selected==[0]
        if key=='decline' and frame==5620:assert selected==[1]
        menus.append(dict(**ref,labels=captions,visible_selected_option=selected[0] if selected else None,
            no_actual_VM_register_orbacking_owner_identity_claim=True))
    record=next(r for r in native['records'] if r['id']=='DK4_MES_B85_R0018')
    for number,frame in [(0,4800),(1,5040)]:
        page=record['complete_native_English_display']['pages'][number]
        ink=plane_mask(page['native_plane'],page['native_plane_sha256'],216)
        im,ref=capture(85,frame);matches=[];best=[]
        for x in range(12,21):
            for y in range(298,307):
                right=max(xx for xx,yy in ink)+4;bottom=max(yy for xx,yy in ink)+2
                found={(xx-x,yy-y) for yy in range(y,y+bottom) for xx in range(x-2,x+right) if im.getpixel((xx,yy))==(8,8,8)}
                difference=len(ink-found)+len(found-ink)
                best.append((difference,x,y))
                if not difference:matches.append((x,y))
        assert len(matches)==1,('page',number,sorted(best)[:3])
        bodies.append(dict(**ref,id=record['id'],page=number+1,actual_origin=list(matches[0]),
            bounded_image_alignment_search_only_not_renderer_research=True,
            complete_visible_glyph_plane_andblank_guards_equal=True))
    save(ROOT/'focused_actual_pixels.json',dict(name_headers=names,menu_samples=menus,rejection_pages=bodies,
        complete_normal_F_first_internal_final_name_characters=True,
        complete_both_caption_labels_highlights_andordinary_DOWN_selection=True,
        complete_two_page_rejection_continuation=True,readonly_framebuffer_checks_no_RAM_orstate_modification=True,
        no_actual_backing_owner_RAM_VRAM_palette_orVM_register_identity_claim=True,
        actual_gameplay=True,disclosed_initialized_fixtures=True,natural_activation=False,hardware_verification=False,new_credit=0,
        evidence={str(p):sha(p.read_bytes()) for p in [NAME,MENU,NATIVE,Path(__file__)]}))
    print(dict(actual_name_headers=len(names),menu_samples=len(menus),caption_checks=2*len(menus),rejection_pages=len(bodies),all_complete_native_pixels_match=True))
