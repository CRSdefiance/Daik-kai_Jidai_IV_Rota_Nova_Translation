"""Check all three original ellipsis glyphs against fresh actual B234 source holds."""
from pathlib import Path
from PIL import Image
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B234_ellipsis_palette_v7583b')
ACTUAL=Path('work/analysis/lil_B234_source_actual_v7583/all18_source_speeches_complete_Japanese_name_masks29_commands_A000_and_normal_return.json')
FONT=Path('work/analysis/lil_B234_source_pages_v7582/all18_clean_objects_complete_native_CP932_pages_and_exact_consumption.json')
PRIOR=Path('work/analysis/lil_B224_ellipsis_palette_v7156b/retained_R11_source_lighter_gray_palette_and_complete_masks.json')
if __name__=='__main__':
    assert not ROOT.exists();a,f,prior=map(read,[ACTUAL,FONT,PRIOR]);ident='DK4_MES_B234_R0005'
    native=next(r for r in f['records'] if r['id']==ident);source=next(r for r in a['source_body_masks'] if r['id']==ident)
    assert native['source_body_hex']==source['expanded_source_body_hex']=='816381638163' and len(native['pages'])==1
    page=native['pages'][0];pixels=Path(page['native_plane']).read_bytes();assert sha(pixels)==page['native_plane_sha256'] and Path(source['native_plane']).read_bytes()==pixels
    black={(i%216,i//216) for i,b in enumerate(pixels) if b==1};gray={(i%216,i//216) for i,b in enumerate(pixels) if b==15}
    assert len(black)==len(gray)==18 and prior['retained_CP932_shadow_RGB']==[197,198,197]
    cases=[];crops=[]
    for hold in source['complete_body_holds']:
        p=Path(hold['capture']);assert sha(p.read_bytes())==hold['sha256'];im=Image.open(p).convert('RGB');crop=im.crop((16,296,232,360));crops.append(crop.tobytes())
        actual={c:{(x-16,y-296) for y in range(296,360) for x in range(16,232) if im.getpixel((x,y))==c} for c in [(0,8,0),(197,198,197),(98,97,98)]}
        assert actual[0,8,0]==black and actual[197,198,197]==gray and not actual[98,97,98]
        cases.append(dict(frame=hold['frame'],capture=str(p),capture_sha256=hold['sha256'],body_RGB_sha256=sha(crop.tobytes()),all18_black_and18_lighter_gray_pixels_exact=True))
    assert cases and len(set(crops))==1
    ROOT.mkdir(parents=True);save(ROOT/'three_source_ellipsis_glyphs_lighter_gray_palette_and_complete_masks.json',dict(actual_source_proof=str(ACTUAL),actual_source_proof_sha256=sha(ACTUAL.read_bytes()),source_font_proof=str(FONT),source_font_proof_sha256=sha(FONT.read_bytes()),earlier_single_ellipsis_palette_lead=str(PRIOR),earlier_single_ellipsis_palette_lead_sha256=sha(PRIOR.read_bytes()),record_ID=ident,source_body_hex='816381638163',complete_original_three_CP932_ellipsis_glyphs=True,black_RGB=[0,8,0],retained_CP932_shadow_RGB=[197,198,197],English_ASCII_shadow_RGB=[98,97,98],black_pixels=18,shadow_pixels=18,source_actual_cases=cases,all_complete_body_RGB_crops_identical=True,source_body_RGB_sha256=cases[0]['body_RGB_sha256'],focused_B234_R5_source_palette_scope_not_global_Japanese_renderer_approval=True,English_native_and_actual_masks_pending=True,no_capture_glyph_font_metric_renderer_guard_or_source_byte_change=True,new_emulator_runs=0,new_credit=0,evidence={str(p):sha(p.read_bytes()) for p in [ACTUAL,FONT,PRIOR,Path(__file__)]},full_goal_complete=False))
    print(dict(source_ellipsis_glyphs=3,black_pixels=18,light_gray_pixels=18,complete_actual_holds=len(cases),credit=0))
