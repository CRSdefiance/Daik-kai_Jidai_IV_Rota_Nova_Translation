"""Measure complete current/target labels on the original menu caption renderer and owned backing."""
import inspect
from pathlib import Path
from PIL import Image,ImageDraw
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.source_locked_derivation_v5118 import checked_text
from scripts import native_menu_backing_surface_v4080 as backing
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B212_choice_planes_v6607b');CONTROL=Path('work/analysis/lil_B212_controls_v6603b/two_three_choices21_return_cases_four_paths_two_effect_pairs_and30_guarded_ends.json');DOC=Path('translations/lil_B212_editorial_manuscript_v2.json');ARM9='aa5a7ed159f33fb8ca5dafdfc068ebc69cf9de0469ffe8eba388d3b954e20d05'
if __name__=='__main__':
    assert not ROOT.exists();control,doc=read(CONTROL),read(DOC);image=NdsImage.open(doc['current_ROM']);arm=image.read_file('/__arm9__.bin');assert sha(arm)==ARM9 and control['candidate_sha256']==doc['current_ROM_sha256']
    adapter=checked_text(inspect.getsource(backing.paint),{"'expected[(y+yy)*backing_width+x+index*6+xx]'":"'expected[(y+yy+1)*backing_width+x+index*6+xx]'",'    assert 0<width<=228':'    assert sha(arm)==ARM9\n    assert 0<width<=228'});env={**backing.__dict__,'ARM9':ARM9};exec(compile(adapter,__file__+'::current-one-pixel-ink-original-backing','exec'),env);ROOT.mkdir(parents=True);cases=[];pictures=[]
    for menu in control['menus']:
        for version in menu['versions'][1:]:
            width=version['minimum_width_units']*6;planes=[];assert 0<width<=228
            for index,label in enumerate(version['labels']):
                for style in [1,15]:
                    pixels,proof=env['paint'](arm,label.encode('ascii'),style,width,(0,index*12));assert proof['independent_complete_native_pixels_match'] and proof['storage_padding_all_blank'] and proof['extra_flush_stays_within_physical_backing']
                    if version['version']=='reviewed-research':assert proof['visible_cell_center_twice']==width
                    path=ROOT/f"C{menu['command_offset']}_{version['version']}_O{index}_style{style}.bin";path.write_bytes(pixels);assert proof['style']==style;planes.append(dict(index=index,native_plane=str(path),native_plane_sha256=sha(pixels),**proof))
                    if style==1:
                        im=Image.new('RGB',(width,12));im.putdata([(8,8,8) if p else (239,232,201) for p in pixels]);ip=path.with_suffix('.png');im.save(ip);pictures.append((f"C{menu['command_offset']} {version['version']} option{index}: {label!r}",im))
            assert len(planes)==menu['count']*2;cases.append(dict(command_offset=menu['command_offset'],word=menu['word'],version=version['version'],native_original_menu_rectangle=version['native_menu_rectangle'],native_width_units=version['minimum_width_units'],caption_width_px=width,original_owned_backing_model=[256,36],logical_caption_height=12,planes=planes,all_leading_internal_final_glyphs_complete=True,no_font_metrics_viewport_or_text_abbreviation=True))
    assert sum(len(c['planes']) for c in cases)==20 and len(pictures)==10
    sheet=Image.new('RGB',(1000,400),'#263238');draw=ImageDraw.Draw(sheet)
    for i,(title,im) in enumerate(pictures):
        x,y=i%2*500,i//2*80;draw.text((x+5,y+5),title,fill='white');sheet.paste(im.resize((im.width*3,36),Image.Resampling.NEAREST),(x+5,y+25))
    sp=ROOT/'all5_current_and_full_reviewed_menu_labels.png';sheet.save(sp);save(ROOT/'all5_labels20_style_planes_complete_and_native_widths.json',dict(candidate=doc['current_ROM'],candidate_sha256=doc['current_ROM_sha256'],control_proof=str(CONTROL),control_proof_sha256=sha(CONTROL.read_bytes()),manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),records=cases,complete_current_and_reviewed_label_style_planes=20,all5_target_labels_centered_complete_first_internal_final_glyphs_bounds_and_canaries=True,full_Zhao_Yun_Guan_Yu_Zhuge_Liang_names_not_abbreviated_to_fit=True,original_native_constructor_computes_width_from_full_labels=True,current_one_pixel_ASCII_descent_bound_to_exact_AA5=True,source_owned_painter_adapter=adapter,historical_two_option_backing_proof='work/analysis/lil_B166_menu_owner_trace_v4086/actual_caption_context_view_and_backing.json',historical_backing_proof_sha256=sha(Path('work/analysis/lil_B166_menu_owner_trace_v4086/actual_caption_context_view_and_backing.json').read_bytes()),B212_actual_two_and_three_option_backing_geometry_highlights_selection_and_branch_return_pending=True,offline_owned_surface_checks_not_actual_B212_backing_capture=True,review_sheet=str(sp),review_sheet_sha256=sha(sp.read_bytes()),visual_review_pending=True,no_ROM_registry_ledger_or_completion_change=True,new_emulator_runs=0,new_review_credit=0,evidence={str(p):sha(p.read_bytes()) for p in [DOC,CONTROL,Path(backing.__file__),Path(__file__)]},full_goal_complete=False));print('All5 target labels and current predecessors pass20 complete black/gray native planes. Full names use native width; B212 actual backing/selection still pending.')
