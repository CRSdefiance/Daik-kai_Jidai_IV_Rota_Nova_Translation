"""Bind the retained glyph's observed lighter shadow; preserve the failed dark-gray probe."""
from pathlib import Path
from PIL import Image
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B224_ellipsis_palette_v7156b')
ACTUAL=Path('work/analysis/lil_B224_source_actual_v7139/all15_source_speeches_complete_Japanese_name_masks27_commands_C200_and_normal_return.json')
FONT=Path('work/analysis/lil_B224_native_pages_v7143/all15_paragraphs15_complete_native_pages120_alignments.json')
if __name__=='__main__':
    assert not ROOT.exists();a,f=map(read,[ACTUAL,FONT]);native=next(r for r in f['records'] if r['id']=='DK4_MES_B224_R0011');assert native['compiled_hex']=='1a8163' and len(native['pages'])==1
    page=native['pages'][0];pixels=Path(page['native_plane']).read_bytes();assert sha(pixels)==page['native_plane_sha256'];black={(i%216,i//216) for i,b in enumerate(pixels) if b==1};gray={(i%216,i//216) for i,b in enumerate(pixels) if b==15};assert len(black)==len(gray)==6
    source=next(r for r in a['source_body_masks'] if r['id']==native['id']);assert source['expanded_source_body_hex']=='8163' and Path(source['native_plane']).read_bytes()==pixels
    cases=[];body_crops=[]
    for hold in source['complete_body_holds']:
        path=Path(hold['capture']);assert sha(path.read_bytes())==hold['sha256'];im=Image.open(path).convert('RGB');crop=im.crop((16,296,232,360));body_crops.append(crop.tobytes())
        actual={color:{(x-16,y-296) for y in range(296,360) for x in range(16,232) if im.getpixel((x,y))==color} for color in [(0,8,0),(197,198,197),(98,97,98)]}
        assert actual[0,8,0]==black and actual[197,198,197]==gray and not actual[98,97,98]
        cases.append(dict(frame=hold['frame'],capture=str(path),capture_sha256=hold['sha256'],body_RGB_sha256=sha(crop.tobytes()),all6_black_and6_lighter_gray_pixels_exact=True))
    assert len(cases)==4 and len(set(body_crops))==1
    ROOT.mkdir(parents=True);save(ROOT/'retained_R11_source_lighter_gray_palette_and_complete_masks.json',dict(actual_source_proof=str(ACTUAL),actual_source_proof_sha256=sha(ACTUAL.read_bytes()),native_English_proof=str(FONT),native_English_proof_sha256=sha(FONT.read_bytes()),record_ID='DK4_MES_B224_R0011',complete_source_current_compiled_hex='1a8163',source_and_English_native_planes_byte_exact=True,black_RGB=[0,8,0],retained_CP932_shadow_RGB=[197,198,197],other_English_ASCII_shadow_RGB=[98,97,98],black_pixels=6,shadow_pixels=6,source_actual_cases=cases,all_four_complete_body_RGB_crops_identical=True,source_body_RGB_sha256=cases[0]['body_RGB_sha256'],sole_existing_ellipsis_palette_scope_not_global_Japanese_renderer_approval=True,failed_probe7156_dark_gray_assumption_preserved=True,no_capture_glyph_font_metric_renderer_guard_or_source_byte_change=True,new_emulator_runs=0,new_credit=0,evidence={str(p):sha(p.read_bytes()) for p in [ACTUAL,FONT,Path('scripts/probe_lil_B224_ellipsis_gray_v7156.py'),Path(__file__)]},full_goal_complete=False));print('Original R11 glyph:all6 black+6 lighter-gray pixels match in4 actual source holds;all RGB body crops identical. Dark-gray-only probe preserved. No font/ROM/prose change.')
