"""Calibrate original native menu margins before observing revised menu pixels."""
import inspect
from pathlib import Path
from PIL import Image
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts import verify_ship_advice_choice_centering_20261022 as prior
from scripts.verify_village_wrap_v608 import read,save

ROOT = Path('work/analysis/lil_Speyer_choice_calibration_v1939')
UI = Path('work/analysis/lil_Speyer_choice_v1927/original_choice_decoder_VM_geometry_and_native_pixels.json')
NAV = Path('work/analysis/lil_Speyer_original_navigation_v1934/closed_original_scene_context.json')
MARGIN_X,MARGIN_Y,ROW_HEIGHT = 16,12,20
INK = (8,8,8)

def planes(arm,case):
    painter=inspect.getsource(prior.paint)
    anchor='    width, height = 48, 20'
    assert painter.count(anchor)==1
    painter=painter.replace(anchor,'    width, height = LABEL_WIDTH, 20')
    env={**prior.__dict__,'LABEL_WIDTH':case['source_derived_text_canvas_width']}
    exec(compile(painter,'native_menu_margin_calibration_v1939','exec'),env)
    values=[]
    for label in case['native_VM_getters_geometry_and_selection']['labels']:
        pixels,proof=env['paint'](arm,label.encode('ascii'),1)
        assert proof['independent_complete_native_pixels_match']
        values.append(pixels)
    return values

def expected(case,values):
    rect=case['native_VM_getters_geometry_and_selection']['native_menu_rectangle']
    width=case['source_derived_text_canvas_width']
    origin=[rect[0]+MARGIN_X,192+rect[1]+MARGIN_Y]
    ink={(origin[0]+x,origin[1]+index*ROW_HEIGHT+y)for index,pixels in enumerate(values)
        for y in range(ROW_HEIGHT)for x in range(width)if pixels[y*width+x]}
    bounds=[rect[0],192+rect[1],rect[2],192+rect[3]]
    assert all(bounds[0]<=x<bounds[2]and bounds[1]<=y<bounds[3]for x,y in ink)
    return ink,bounds,origin

def verify(im,case,values):
    wanted,bounds,origin=expected(case,values)
    actual={(x,y)for y in range(bounds[1],bounds[3])for x in range(bounds[0],bounds[2])if im.getpixel((x,y))==INK}
    assert wanted==actual,('native menu font mismatch',len(wanted-actual),len(actual-wanted))
    return dict(native_menu_rectangle=bounds,text_canvas_origin=origin,row_height=ROW_HEIGHT,
        complete_native_independent_actual_menu_ink_equal=True,complete_ink_pixels=len(wanted))

if __name__=='__main__':
    assert not ROOT.exists()
    ui,nav=map(read,(UI,NAV))
    case=next(r for r in ui['current_and_reviewed_VM_and_font_cases']if r['version']=='current')
    arm=NdsImage.open(ui['candidate']).read_file('/__arm9__.bin')
    values=planes(arm,case)
    rows=[]
    for hold in nav['choices'][0]['holds']:
        assert sha(Path(hold['capture']).read_bytes())==hold['capture_sha256']
        proof=verify(Image.open(hold['capture']).convert('RGB'),case,values)
        rows.append(dict(**proof,frame=hold['frame'],capture=hold['capture'],capture_sha256=hold['capture_sha256']))
    ROOT.mkdir(parents=True)
    save(ROOT/'original_current_menu_fixed_margin_calibration.json',dict(source_UI=str(UI),source_UI_sha256=sha(UI.read_bytes()),
        original_navigation=str(NAV),original_navigation_sha256=sha(NAV.read_bytes()),
        margin_x=MARGIN_X,margin_y=MARGIN_Y,row_height=ROW_HEIGHT,actual_ink_RGB=list(INK),
        source_original_menu_cases=rows,calibrated_only_from_original_menu_before_revised_pixels=True,
        revised_menu_must_use_native_derived_rectangle_and_same_fixed_margins=True,
        no_revised_image_was_fitted_or_recorded=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print(dict(original_menu_complete_holds=len(rows),fixed_margins=[MARGIN_X,MARGIN_Y],row_height=ROW_HEIGHT,
        ink_pixels_each=rows[0]['complete_ink_pixels'],revised_prediction_not_yet_tested=True))
