"""Retain the failed y277 bitmap comparison; bind the actual native style11 origin y276."""
from pathlib import Path
from PIL import Image
from dk4tool.patch.grand_race_menu_release import sha
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/square_shopkeeper_origin_v7024b')
if __name__=='__main__':
    assert not ROOT.exists()
    image=Path('E:/Rota Nova translations/Generated/work/emulation_v193/square_shopkeeper_static_parent_v7023/frame_002950_cold_boot.png')
    plane=Path('work/analysis/square_shopkeeper_actual_v7024/name00.bin');raw=plane.read_bytes();expected={(i%216,i//216) for i,v in enumerate(raw) if v}
    im=Image.open(image).convert('RGB');cases=[]
    for origin in [275,276,277,278]:
        actual={(x-4,y) for y in range(13) for x in range(110) if im.getpixel((12+x,origin+y))==(98,97,98)}
        cases.append(dict(native_origin=[16,origin],missing=len(expected-actual),extra=len(actual-expected),exact=actual==expected))
    assert [c['native_origin'] for c in cases if c['exact']]==[[16,276]] and len(expected)==140
    source=Path('scripts/audit_lil_B221_English_paths_v7004.py');assert "actualname={(x-16,y-276)" in source.read_text('utf8')
    row=derive('scripts/audit_square_shopkeeper_scenes_v7024.py','scripts/audit_square_shopkeeper_scenes_v7024b.py',{
        'actual_v7024':'actual_v7024b','(x-4,y-1)':'(x-4,y)'})
    ROOT.mkdir(parents=True);save(ROOT/'exact_native_origin_and_source_locked_successor.json',dict(cases=cases,
        capture=str(image),capture_sha256=sha(image.read_bytes()),native_plane=str(plane),native_plane_sha256=sha(raw),
        prior_actual_native_origin_source=str(source),prior_actual_native_origin_source_sha256=sha(source.read_bytes()),successor=row,
        one_row_audit_coordinate_error_not_game_display_defect=True,no_glyph_mask_color_bounds_guard_or_ROM_change=True,
        failed_producer_and_all_partial_artifacts_preserved=True,new_review_credit=0,full_goal_complete=False))
