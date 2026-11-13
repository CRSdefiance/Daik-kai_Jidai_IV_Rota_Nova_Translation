"""Original two-choice VM, native rectangle and centered full label painting."""
import inspect
from pathlib import Path
from PIL import Image,ImageDraw
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts import verify_ship_advice_choice_centering_20261022 as prior
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_lesson_choice_ui_v1735')


if __name__=='__main__':
    assert not ROOT.exists()
    research=read('work/analysis/lil_lesson_relocation_v1731/nested_source_relocation_research.json')
    packet=read('work/analysis/lil_lessons_source_v1717/complete_lesson_source_context.json')
    arm=NdsImage.open(research['candidate']).read_file('/__arm9__.bin')
    painter=inspect.getsource(prior.paint);old='    width, height = 48, 20';assert painter.count(old)==1
    painter=painter.replace(old,'    width, height = LABEL_WIDTH, 20',1)
    ROOT.mkdir(parents=True);(ROOT/'native_painter_adapter.txt').write_text(painter,encoding='utf-8')
    cases=[];pictures=[]
    for block in research['blocks']:
        number=block['block'];target=block['choice_commands'][0]
        source=next(b['choices'][0] for b in packet['blocks'] if b['block']==number)
        for version,value in [('current',bytes.fromhex(source['current_hex'])),('reviewed_research',bytes.fromhex(target['target_hex']))]:
            vm=prior.choice_vm(arm,value)
            if version=='reviewed_research':assert vm['labels']==target['labels']
            env={**prior.__dict__,'LABEL_WIDTH':vm['minimum_width_units']*6}
            exec(compile(painter,'source_derived_choice_painter_v1735','exec'),env)
            labels=[]
            for row,label in enumerate(vm['labels']):
                for style in (1,15):
                    pixels,proof=env['paint'](arm,label.encode('ascii'),style)
                    assert proof['native_origin'][0]>=0 and proof['independent_complete_native_pixels_match']
                    labels.append(proof)
                    if style==1:
                        im=Image.new('RGB',(env['LABEL_WIDTH'],20));background=(0,168,176) if row==0 else (204,198,180)
                        im.putdata([(8,8,8) if p else background for p in pixels]);pictures.append((f'B{number} {version} option{row}',im))
            if version=='reviewed_research':
                assert all(p['visible_cell_center_twice']==env['LABEL_WIDTH'] for p in labels)
            cases.append({'block':number,'version':version,'object_hex':value.hex(),'original_VM_getters_geometry_and_selection':vm,
                'source_derived_text_canvas_width':env['LABEL_WIDTH'],'all_four_style_label_planes':labels,
                'native_bounds_complete_first_last_letters_and_reviewed_visible_centering_verified':True})
    sheet=Image.new('RGB',(1000,1200),(28,36,40));draw=ImageDraw.Draw(sheet)
    for i,(title,im) in enumerate(pictures):
        x,y=12+496*(i%2),10+290*(i//2);draw.text((x,y),title,fill='white')
        sheet.paste(im.resize((im.width*2,40),Image.Resampling.NEAREST),(x,y+24))
    path=ROOT/'native_current_and_reviewed_choices.png';sheet.save(path)
    save(ROOT/'original_choice_VM_geometry_and_native_pixels.json',{'candidate':research['candidate'],'candidate_sha256':research['candidate_sha256'],
        'cases':cases,'four_complete_reviewed_labels_two_styles_each':True,
        'all12_original_selection_cancel_VM_cases_and_source_extents_verified':True,
        'menus_remain_two_options_with_original_branch_indices':True,
        'native_auto_sizing_may_shrink_menu_when_unused_trailing_English_spaces_are_removed':True,
        'no_manual_geometry_font_palette_or_UI_code_change':True,
        'input_loop_is_bridged_not_actual_revised_branch_gameplay':True,
        'source_harness':str(Path(prior.__file__)),'source_harness_sha256':sha(Path(prior.__file__).read_bytes()),
        'visual_review_sheet':str(path),'visual_review_sheet_sha256':sha(path.read_bytes()),'visual_review_pending':True,
        'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    print([(r['block'],r['version'],r['source_derived_text_canvas_width'],r['original_VM_getters_geometry_and_selection']['native_menu_rectangle']) for r in cases],flush=True)
