"""Reject damaged caption pixels, foreign backgrounds and malformed cursor bands."""
from pathlib import Path
from PIL import Image
from scripts.audit_story_glyph_consistency import load,save
from scripts.analyze_hodram_B231_B250_menu_v1 import background_band,ROOT
from scripts.check_hodram_B91_B110_actual_pixels import mask,match
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest

OUT=ROOT/'actual_menus_band_v1/model_qualification.json'

def main():
    assert not OUT.exists()
    proof=load(ROOT/'native_objects_v1/menu/B243_C674/menu_provider_and_planes.json')
    imagepath=ROOT/'focused_capture_v1/frame_015360_cold_boot.png';im=Image.open(imagepath).convert('RGB')
    plane=next(r for r in proof['records'] if r['version']=='reviewed-English' and r['option']==0 and r['style']==1)
    ink=mask(plane['path'],plane['sha256'],48);x,y=104,272
    blank={(xx,yy) for yy in range(y-4,y+16) for xx in range(x,x+48)}-{(x+xx,y+yy) for xx,yy in ink}
    assert match(im,ink,(8,8,8),[x],[y])==[x,y] and background_band(im,blank)
    results=[]
    for name,point in [('missing-leading-ink',min(ink)),('missing-final-ink',max(ink))]:
        changed=im.copy();changed.putpixel((x+point[0],y+point[1]),(205,198,180))
        assert not match(changed,ink,(8,8,8),[x],[y]);results.append(dict(case=name,rejected=True))
    for name in ['foreign-background','mixed-row','disjoint-band','interior-band']:
        changed=im.copy()
        for point in blank:changed.putpixel(point,(205,198,180))
        if name=='foreign-background':changed.putpixel(min(blank),(255,0,255))
        elif name=='mixed-row':changed.putpixel(min(blank),(0,165,172))
        else:
            ys=[y-4,y+15] if name=='disjoint-band' else [y+4,y+5]
            for point in blank:
                if point[1] in ys:changed.putpixel(point,(0,165,172))
        try:background_band(changed,blank)
        except AssertionError:results.append(dict(case=name,rejected=True))
        else:raise AssertionError('Accepted malformed background: '+name)
    save(OUT,dict(all6_pixel_andcursor_mutations_rejected=True,cases=results,
        actual_capture=str(imagepath),actual_capture_sha256=digest(imagepath),
        exact_provider_geometry_used_not_positions_selected_from_caption_letters=True,
        native_VM_geometry=[88,64,168,128],caption_width=48,
        no_ROM_orcapture_mutation=True,evidence={str(p):digest(p) for p in [Path(__file__),Path('scripts/analyze_hodram_B231_B250_menu_v1.py')]},new_credit=0))
    print('Six caption/background mutations rejected; original captures and ROM unchanged.')

if __name__=='__main__':main()
