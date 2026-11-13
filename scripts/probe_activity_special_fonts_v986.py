"""Full native font proof for14 Deck comments and three distinct Chapel refusal modals."""
import struct
from pathlib import Path
from types import FunctionType
from PIL import Image,ImageDraw
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.activity_special_layout_v986 import ROM,ROM_SHA,ARM_SHA,compiled,visible_lines
from scripts.prepare_activity_special_prose_v985 import MANUSCRIPT,IDS
from scripts.prepare_work_comments_v842 import snapshot,machine_at
from scripts import probe_work_fonts_v843 as original
from scripts.prepare_product_pitches_v747 import native_layout
from scripts.verify_arrival_native_v792 import prepared
from scripts.verify_common_alignment_native_v257 import raster as original_raster
from scripts.verify_shipyard_gameplay_v760 import independent_font
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/activity_special_v986')
BASE=0x02000000

def execute_activity(rom,raw,actor,role,number,text,lines,activity):
    source=Path('scripts/probe_work_fonts_v843.py');before=source.read_bytes()
    def call(cpu,offset,args,**kwargs):
        if offset==0x15334:
            assert args==(original.VIEW,role,0,actor)
            args=(original.VIEW,role,activity,actor)
        return original.call(cpu,offset,args,**kwargs)
    execute=FunctionType(original.execute.__code__,{**original.execute.__globals__,'call':call},argdefs=original.execute.__defaults__)
    result,plane=execute(rom,raw,actor,role,number,text,lines)
    assert source.read_bytes()==before
    result.update(original_renderer_source_sha256=sha(before),scoped_adapter_changes_only_declared_activity_argument=activity,
        original_native_renderer_and_complete_pixel_guards_unchanged=True)
    return result,plane

def prepare_special(arm,raw,mode,flag):
    cpu,get=machine_at(arm,raw);context=get(0x3F0F8);allowed=set(range(context+8,context+16))
    cpu.mem_write(context+8,struct.pack('<2I',*mode))
    if flag is not None:
        root=get(0xCB190);at=root+0x1A5;old=bytes(cpu.mem_read(at,1))[0]
        cpu.mem_write(at,bytes([(old&~4)|flag]));allowed.add(at);assert get(0x4A224,root+0x194)==flag
    after=bytes(cpu.mem_read(BASE,len(raw)))
    changes=[{'address':BASE+i,'before':a,'after':b} for i,(a,b) in enumerate(zip(raw,after,strict=True)) if a!=b]
    assert all(r['address'] in allowed for r in changes)
    return after,{'declared_CPU_mode':list(mode),'declared_CPU_shared_object_bit2_value':flag,'changes':changes,
        'all_actor_records_and_all_other4MiB_RAM_exact':True,'bit2_story_gender_meaning_not_inferred':True}

def main():
    assert not ROOT.exists();ROOT.mkdir(parents=True)
    rom=NdsImage.open(ROM);arm=rom.read_file('/__arm9__.bin');assert sha(ROM.read_bytes())==ROM_SHA and sha(arm)==ARM_SHA
    doc=read(MANUSCRIPT);assert doc['current_ROM_sha256']==ROM_SHA
    source,receipt=snapshot('mood_comments_v982_975_CaptainSilent',16100)
    ui,ui_receipt=snapshot('personal_cabin_v840_838_Charles_after',4600)
    class CurrentFont:
        @staticmethod
        def open(path):
            assert path=='out/all_routes_combined_v255_candidate.nds'
            return rom
    raster=FunctionType(original_raster.__code__,{**original_raster.__globals__,'NdsImage':CurrentFont},argdefs=original_raster.__defaults__)
    cases=[];body_cases=0;modal_cases=0
    for row in doc['records']:
        n=row['message_id'];actor=row['actor_ID'];text=compiled(row);lines=visible_lines(row);variants=[];planes=[]
        if row['consumer']=='Deck-CabinInfoView':
            model,fixture=original.prepare_model(arm,source,actor,2,ui)
            modes=((0,0),(0,1)) if n<1878 else (tuple(row['original_mode_fields8_12']),)
            flag=0 if n in (1883,1887) else 4 if n in (1884,1888) else None
            for mode in modes:
                raw,selection=prepare_special(arm,model,mode,flag)
                result,plane=execute_activity(rom,raw,actor,2,n,text,lines,row['activity_state'])
                assert not any(plane[y*252+x] for y in range(60,96) for x in range(216,252))
                result.update(selection_fixture=selection,original_numeric_selector_selected_expected_message=True)
                variants.append(result);planes.append(plane);body_cases+=1
            assert all(plane==planes[0] for plane in planes)
            preview=ROOT/f'ID{n}_complete_native_body.png'
            Image.frombytes('L',(252,96),bytes(0 if v else 255 for v in planes[0])).save(preview)
            case={'message_id':n,'actor_ID':actor,'consumer':row['consumer'],'generated_native_lines':lines,
                'source_snapshot':receipt,'CPU_room_and_genuine_widget_clone':fixture,'native_controls':variants,
                'complete_words_and216x36_body_bounds_pass':True,'preview':str(preview),'preview_sha256':sha(preview.read_bytes())}
        else:
            cpu=prepared(arm);formatted,wrapped_lines=native_layout(cpu,text,n,(),parent=0x02054014)
            assert formatted==text and wrapped_lines==lines
            pixels=raster(arm,formatted,0x01FFCE40-BASE,size=(228,64),instruction_limit=2000000)
            assert pixels==independent_font(arm,rom.read_file('/GRP/KANJI.FNT'),lines)
            preview=ROOT/f'ID{n}_complete_native_modal.png'
            Image.frombytes('L',(228,64),bytes(0 if v else 255 for v in pixels)).save(preview);modal_cases+=1
            case={'message_id':n,'actor_ID':actor,'consumer':row['consumer'],'generated_native_lines':lines,
                'compiled_hex':text.hex(),'original_54014_COMMON_dispatch_keeps_compiled_bytes_exact':True,
                'native_balanced_wrapper_generated_all_breaks_no_authored_padding':True,
                'whole228x64_native_and_independent_font_canvas_equal':True,
                'all_leading_trailing_glyphs_and_uniform_visible_left_margin_pass':True,
                'source_context_proof':doc['native_context_proof'],'source_actor_and_assignment_refusal_selection_proven_separately':True,
                'raster_helper_scoped_to_current_ROM_font_no_historical_helper_edit':True,
                'preview':str(preview),'preview_sha256':sha(preview.read_bytes())}
        case.update(native_font_only_not_actual_RGB_UI_or_earned_unlock=True,compiled_hex=text.hex(),visible_widths=list(map(len,lines)))
        cases.append(case);print(n,row['consumer'],[(len(line),line) for line in lines],flush=True)
    assert tuple(c['message_id'] for c in cases)==IDS and body_cases==20 and modal_cases==3
    sheet=Image.new('RGB',(3*466,6*116),'#263238');draw=ImageDraw.Draw(sheet)
    for i,case in enumerate(cases):
        x,y=i%3*466,i//3*116;draw.text((x+5,y+5),f"ID{case['message_id']} {case['consumer']};actual pending",fill='white')
        with Image.open(case['preview']) as im:
            crop=im.crop((0,60,216,96)) if case['consumer']=='Deck-CabinInfoView' else im.crop((0,0,228,36))
            sheet.paste(crop.resize((crop.width*2,crop.height*2),Image.Resampling.NEAREST),(x+5,y+28))
    image=ROOT/'all17_native_body_and_modal_masks_2x.png';sheet.save(image)
    save(ROOT/'native_font_proof.json',{'candidate':str(ROM),'candidate_sha256':ROM_SHA,'ARM9_sha256':ARM_SHA,
        'manuscript':str(MANUSCRIPT),'manuscript_sha256':sha(MANUSCRIPT.read_bytes()),'cases':cases,
        'complete_Deck_native_font_cases':body_cases,'complete_modal_native_font_cases':modal_cases,
        'all17_complete_words_leading_trailing_letters_and_native_bounds_pass':True,
        'modal3_use_existing_native_balanced_formatter_as_offline_compiler_no_runtime_code_or_membership_changes':True,
        'activity2_ordinary_and_battle_both_source_controls_equal':True,
        'special_actor25_26_27_ordinary_and_battle_and_both_actor27_bit2_paths_covered':True,
        'source_snapshot':receipt,'genuine_initialized_body_widget_source':ui_receipt,
        'actual_scenes_modal_geometry_and_dismissal_registered_repack_and_exact_patch_pending':True,
        'review_sheet':str(image),'review_sheet_sha256':sha(image.read_bytes()),'visual_review_pending':True,
        'renderer_source_sha256':sha(Path('scripts/probe_work_fonts_v843.py').read_bytes()),
        'layout_producer_sha256':sha(Path('scripts/activity_special_layout_v986.py').read_bytes()),
        'producer_sha256':sha(Path(__file__).read_bytes()),'completed_entries_added':0,'full_goal_complete':False})
    print('17 entries:20 complete original Deck font cases and3 distinct native modal font cases pass;actual UI and integration remain pending.')

if __name__=='__main__':main()
