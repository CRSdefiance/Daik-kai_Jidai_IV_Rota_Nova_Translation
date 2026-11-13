"""All24 original sail/boarding selectors and complete independent native font planes."""

from pathlib import Path
from PIL import Image,ImageDraw
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.sails_boarding_layout_v880 import layout,compiled
from scripts.prepare_sails_boarding_prose_v879 import ROM,MANUSCRIPT
from scripts.prepare_work_comments_v842 import snapshot
from scripts.probe_work_fonts_v843 import prepare_model,execute
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/sails_boarding_v880')


def main():
    ROOT.mkdir(parents=True,exist_ok=True);assert not (ROOT/'native_font_proof.json').exists()
    rom=NdsImage.open(ROM);arm=rom.read_file('/__arm9__.bin');doc=read(MANUSCRIPT)
    assert sha(ROM.read_bytes())==doc['current_ROM_sha256']
    ui,ui_receipt=snapshot('personal_cabin_v840_838_Charles_after',4600)
    npc,npc_receipt=snapshot('planning_finance_v864_863_JoakimPlanning',3400)
    reps={0:4,1:16,2:9,3:7,4:5,5:6,6:14,7:23}
    heroes={0:('personal_activity_v839_838_Rafael_later',3200),1:('planning_finance_v864_863_JoakimPlanning',3400),
        2:('ceremony_Lil_approach_v825',23000),3:('ceremony_Maria_approach_v825',26000)}
    cases=[]
    for row in doc['records']:
        if row['protagonist_ID'] is None:actor=reps[row['voice_class']];source,receipt=npc,npc_receipt
        else:actor=row['protagonist_ID'];source,receipt=snapshot(*heroes[actor])
        prepared,fixture=prepare_model(arm,source,actor,row['role_ID'],ui)
        lines=layout(row['english']);case,plane=execute(rom,prepared,actor,row['role_ID'],row['message_id'],compiled(row),lines)
        assert case['complete_native_copy_macro_draw_and_ABI'] and case['full252x96_native_and_independent_canvas_equal']
        assert not any(plane[y*252+x] for y in range(60,96) for x in range(216,252))
        path=ROOT/f'ID{row["message_id"]}_complete_native_ink.png'
        Image.frombytes('L',(252,96),bytes(0 if v else 255 for v in plane)).save(path)
        case.update(source_snapshot=receipt,isolated_CPU_fixture=fixture,all_body_ink_inside_registered216x36_crop=True,
            preview=str(path),preview_sha256=sha(path.read_bytes()),native_ink_only_not_actual_RGB_scene_or_earned_assignment=True)
        cases.append(case);print(row['message_id'],[(len(x),x) for x in lines],flush=True)
    assert len(cases)==24
    sheet=Image.new('RGB',(3*514,8*231),'#263238');draw=ImageDraw.Draw(sheet)
    for i,case in enumerate(cases):
        x,y=i%3*514,i//3*231;draw.text((x+5,y+5),f"ID{case['message_id']} complete native words;actual scene pending",fill='white')
        with Image.open(case['preview']) as im:sheet.paste(im.resize((504,192),Image.Resampling.NEAREST),(x+5,y+24))
    path=ROOT/'all24_native_ink_masks_2x.png';sheet.save(path)
    save(ROOT/'native_font_proof.json',{'candidate':str(ROM),'candidate_sha256':sha(ROM.read_bytes()),
        'manuscript':str(MANUSCRIPT),'manuscript_sha256':sha(MANUSCRIPT.read_bytes()),'cases':cases,
        'all24_source_numeric_selection_complete_ABI_words_and_visible_ink_pass':True,
        'genuine_initialized_body_widget_source':ui_receipt,'four_original_actual_captain_states_used_no_captain_ID_substitution':True,
        'role_assignments_and_UI_clone_are_CPU_only_formatting_fixtures':True,
        'complete_sail_types_dead_calm_and_boarding_words_pass':True,
        'review_sheet':str(path),'review_sheet_sha256':sha(path.read_bytes()),'visual_review_pending':True,
        'producer_sha256':sha(Path(__file__).read_bytes()),'layout_producer_sha256':sha(Path('scripts/sails_boarding_layout_v880.py').read_bytes()),
        'registered_repack_original_copy_actual_RGB_and_gameplay_pending':True,'full_goal_complete':False})
    print('All24 complete original/native fonts and216x36 bounds pass;visual review and actual release pending.',flush=True)


if __name__=='__main__':main()
