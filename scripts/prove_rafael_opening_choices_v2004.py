"""One unchanged two-option object: three VM cases and four complete style planes."""
from pathlib import Path
import inspect
from PIL import Image,ImageDraw
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts import verify_ship_advice_choice_centering_20261022 as prior
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/rafael_opening_choices_v2004')
PLAN=Path('work/analysis/rafael_opening_relocation_v2001b/current_B44_typed_relocation_research.json')
DOC=Path('translations/rafael_opening_contextual_choices_editorial_draft_v1.json')

if __name__=='__main__':
    assert not ROOT.exists()
    plan=read(PLAN);current=read('work/analysis/native_storyline_census_v1995/SC0_block044_current_native.json')
    a=next(r for r in current['commands']if r['word']==0x2100)
    b=next(r for r in plan['mapped_native_commands']if r['word']==0x2100)
    assert b['old_offset']==a['offset']==6410
    from dk4tool.formats.ilnk import IlnkContainer
    image=NdsImage.open(plan['research_ROM']);arm=image.read_file('/__arm9__.bin')
    block=IlnkContainer.parse(image.read_file('/data/SC0.DK4')).blocks[44]
    value=bytes.fromhex(a['whole_command_hex'])
    assert block[b['new_offset']:b['new_offset']+b['new_native_extent']]==value
    vm=prior.choice_vm(arm,value)
    assert vm['labels']==['Ask him.','Prepare alone.']
    width=vm['minimum_width_units']*6;assert 0<width<=228
    painter=inspect.getsource(prior.paint).replace('    width, height = 48, 20','    width, height = LABEL_WIDTH, 20')
    env={**prior.__dict__,'LABEL_WIDTH':width};exec(compile(painter,__file__,'exec'),env)
    ROOT.mkdir(parents=True);planes=[];sheet=Image.new('RGB',(520,150),'#263238');draw=ImageDraw.Draw(sheet)
    for i,label in enumerate(vm['labels']):
        for style in (1,15):
            pixels,proof=env['paint'](arm,label.encode(),style)
            assert proof['visible_cell_center_twice']==width and proof['native_origin'][0]>=0
            planes.append(dict(option_index=i,**proof,whole_native_plane_sha256=sha(pixels)))
            if style==1:
                im=Image.new('RGB',(width,20));im.putdata([(8,8,8)if p else(239,232,201)for p in pixels])
                draw.text((8,8+66*i),f'Option{i}: '+label,fill='white');sheet.paste(im.resize((width*2,40)),(8,28+66*i))
    target=ROOT/'unchanged_native_choice_labels.png';sheet.save(target)
    save(ROOT/'typed_choice_VM_geometry_and_complete_native_pixels.json',dict(
        research_ROM=plan['research_ROM'],research_ROM_sha256=plan['research_ROM_sha256'],ARM9_sha256=sha(arm),
        plan=str(PLAN),plan_sha256=sha(PLAN.read_bytes()),manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),
        current_and_target_object_identical=True,object_hex=value.hex(),native_VM=vm,
        three_native_selection_cancel_cases_pass=True,four_complete_native_style_label_planes=planes,
        current_command_offset=a['offset'],target_command_offset=b['new_offset'],source_derived_canvas_width=width,
        exact_8_and14_byte_labels_and_original_option_return_values_preserved=True,
        first_last_internal_glyphs_bounds_centering_and_guards_verified=True,
        repeated_identical_target_plane_tests_not_needed=True,input_loop_bridged_not_actual_branch_visit=True,
        preview=str(target),preview_sha256=sha(target.read_bytes()),visual_review_pending=True,
        actual_visible_choice_and_both_relocated_transitions_pending=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print(dict(native_VM_cases=3,native_style_planes=4,labels=vm['labels'],width=width))
