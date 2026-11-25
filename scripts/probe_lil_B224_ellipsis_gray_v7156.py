"""Check the retained CP932 glyph's actual black/gray behavior without replay."""
from pathlib import Path
from PIL import Image
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B224_ellipsis_gray_v7156')
ACTUAL=Path('work/analysis/lil_B224_source_actual_v7139/all15_source_speeches_complete_Japanese_name_masks27_commands_C200_and_normal_return.json')
FONT=Path('work/analysis/lil_B224_native_pages_v7143/all15_paragraphs15_complete_native_pages120_alignments.json')
if __name__=='__main__':
    assert not ROOT.exists();a,f=map(read,[ACTUAL,FONT]);native=next(r for r in f['records'] if r['id']=='DK4_MES_B224_R0011');assert native['compiled_hex']=='1a8163' and len(native['pages'])==1
    page=native['pages'][0];pixels=Path(page['native_plane']).read_bytes();assert sha(pixels)==page['native_plane_sha256'];black={(i%216,i//216) for i,b in enumerate(pixels) if b==1};gray={(i%216,i//216) for i,b in enumerate(pixels) if b==15}
    source=next(r for r in a['source_body_masks'] if r['id']==native['id']);assert source['expanded_source_body_hex']=='8163' and Path(source['native_plane']).read_bytes()==pixels
    cases=[]
    for hold in source['complete_body_holds']:
        path=Path(hold['capture']);assert sha(path.read_bytes())==hold['sha256'];im=Image.open(path).convert('RGB');foundblack={(x-16,y-296) for y in range(296,360) for x in range(16,232) if im.getpixel((x,y))==(0,8,0)};foundgray={(x-16,y-296) for y in range(296,360) for x in range(16,232) if im.getpixel((x,y))==(98,97,98)}
        assert foundblack==black and foundgray==gray,(hold['frame'],len(gray-foundgray),len(foundgray-gray));cases.append(dict(frame=hold['frame'],capture=str(path),capture_sha256=hold['sha256'],complete_black_and_gray_masks_equal=True,black_pixels=len(black),gray_pixels=len(gray)))
    assert cases;ROOT.mkdir(parents=True);save(ROOT/'retained_R11_actual_black_gray_and_source_English_native_plane_identity.json',dict(actual_source_proof=str(ACTUAL),actual_source_proof_sha256=sha(ACTUAL.read_bytes()),native_English_proof=str(FONT),native_English_proof_sha256=sha(FONT.read_bytes()),source_and_English_R11_body_hex='8163',all_R11_cases=cases,source_and_English_independent_native_planes_byte_exact=True,sole_CP932_ellipsis_actual_gray_scope_not_all_Japanese_gray=True,no_glyph_replacement_metric_runtime_or_capture_change=True,new_emulator_runs=0,new_credit=0,full_goal_complete=False));print(dict(retained_ellipsis_cases=len(cases),black=len(black),gray=len(gray),all_actual_masks_equal=True,no_replay=True))
