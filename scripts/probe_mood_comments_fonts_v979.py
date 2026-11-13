"""All39 original mood selectors and complete native words/symbols in78 CPU font cases."""
import struct
from pathlib import Path
from PIL import Image,ImageDraw
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.mood_comments_layout_v979 import layout,compiled
from scripts.prepare_mood_comments_prose_v978 import ROM,MANUSCRIPT,IDS
from scripts.prepare_work_comments_v842 import snapshot,machine_at
from scripts.probe_work_fonts_v843 import prepare_model,execute
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/mood_comments_v979')
BASE=0x02000000


def prepare_mood(arm,raw,actor,mode,mood):
    cpu,get=machine_at(arm,raw);actors=get(0xCB184);hero=get(0x7F244)
    assert arm[0x7E0B4:0x7E0BC]==bytes.fromhex('0700d0e51eff2fe1')
    obj=actors+struct.unpack_from('<I',arm,0x1229C)[0] if actor==hero else actors+4+actor*32
    before_actor=bytes(cpu.mem_read(obj,32));assert get(0x7E100,obj)==before_actor[6]==0
    before_mood=get(0x7E0B4,obj);assert before_mood==before_actor[7] and before_mood in (1,2,3) and mood in (0,4,5)
    context=get(0x3F0F8);old_mode=list(struct.unpack('<2I',cpu.mem_read(context+8,8)))
    cpu.mem_write(obj+7,bytes([mood]));cpu.mem_write(context+8,struct.pack('<2I',*mode))
    assert get(0x7E100,obj)==0 and get(0x7E0B4,obj)==mood
    after_actor=bytes(cpu.mem_read(obj,32));assert after_actor==before_actor[:7]+bytes([mood])+before_actor[8:]
    after=bytes(cpu.mem_read(BASE,len(raw)))
    changes=[{'address':BASE+i,'before':a,'after':b} for i,(a,b) in enumerate(zip(raw,after,strict=True)) if a!=b]
    assert all(r['address']==obj+7 or context+8<=r['address']<context+16 for r in changes)
    return after,{'actor_ID':actor,'actual_captain_ID':hero,'mood_getter_source_hex':arm[0x7E0B4:0x7E0BC].hex(),'actor_object':obj,
        'source_actor_record_hex':before_actor.hex(),'CPU_actor_record_hex':after_actor.hex(),'physical_condition_preserved':0,'source_mood':before_mood,'CPU_mood':mood,
        'source_mode_fields8_12':old_mode,'CPU_mode_fields8_12':list(mode),'changes':changes,
        'only_declared_mood_byte_and_mode_fields_change':True,'other31_actor_bytes_and_all_other_CPU_RAM_exact':True,'no_ROM_or_live_RAM_changes_not_earned_mood':True}


def main():
    ROOT.mkdir(parents=True,exist_ok=True);assert not (ROOT/'native_font_proof.json').exists()
    rom=NdsImage.open(ROM);arm=rom.read_file('/__arm9__.bin');doc=read(MANUSCRIPT);assert sha(ROM.read_bytes())==doc['current_ROM_sha256']
    ui,ui_receipt=snapshot('personal_cabin_v840_838_Charles_after',4600);npc,npc_receipt=snapshot('battle_personal_v897_893_Julio',14700)
    reps={0:4,1:16,2:9,3:7,4:5,5:6,6:14,7:19}
    heroes={0:('personal_activity_v839_838_Rafael_later',3200),1:('battle_gunnery_deck_v955_954_CaptainDeck',16500),
        2:('ceremony_Lil_approach_v825',23000),3:('ceremony_Maria_approach_v825',26000)}
    cases=[]
    for row in doc['records']:
        if row['special_actor_ID'] is not None:actor=row['special_actor_ID'];source,receipt=npc,npc_receipt
        elif row['protagonist_ID'] is None:actor=reps[row['voice_class']];source,receipt=npc,npc_receipt
        else:actor=row['protagonist_ID'];source,receipt=snapshot(*heroes[actor])
        prepared,fixture=prepare_model(arm,source,actor,row['role_ID'],ui);lines=layout(row['english']);variants=[];planes=[]
        for name,mode in (('ordinary',(0,0)),('battle',(0,1))):
            mood_raw,mood_fixture=prepare_mood(arm,prepared,actor,mode,row['mood_ID'])
            case,plane=execute(rom,mood_raw,actor,row['role_ID'],row['message_id'],compiled(row),lines)
            assert case['complete_native_copy_macro_draw_and_ABI'] and case['full252x96_native_and_independent_canvas_equal']
            assert not any(plane[y*252+x] for y in range(60,96) for x in range(216,252))
            case.update(mode=name,mood_fixture=mood_fixture,original_mood_selector_selected_expected_message=True)
            variants.append(case);planes.append(plane)
        assert planes[0]==planes[1]
        path=ROOT/f'ID{row["message_id"]}_complete_native_ink.png'
        Image.frombytes('L',(252,96),bytes(0 if v else 255 for v in planes[0])).save(path)
        cases.append({'message_id':row['message_id'],'actor_ID':actor,'physical_condition_ID':0,'mood_ID':row['mood_ID'],'source_snapshot':receipt,
            'isolated_CPU_role_and_widget_fixture':fixture,'generated_native_lines':lines,'ordinary_and_battle_font_controls':variants,
            'both_original_selectors_full_canvas_and_words_equal':True,'all_body_ink_inside_registered216x36_crop':True,
            'preview':str(path),'preview_sha256':sha(path.read_bytes()),'nonverbal_only':row['nonverbal_only'],'native_ink_only_not_actual_RGB_scene_or_earned_mood':True})
        print(row['message_id'],[(len(x),x) for x in lines],flush=True)
    assert tuple(c['message_id'] for c in cases)==IDS
    sheet=Image.new('RGB',(3*442,13*104),'#263238');draw=ImageDraw.Draw(sheet)
    for i,case in enumerate(cases):
        x,y=i%3*442,i//3*104;draw.text((x+5,y+5),f"ID{case['message_id']} complete native body;actual pending",fill='white')
        with Image.open(case['preview']) as im:sheet.paste(im.crop((0,60,216,96)).resize((432,72),Image.Resampling.NEAREST),(x+5,y+25))
    path=ROOT/'all39_native_body_ink_masks_2x.png';sheet.save(path)
    save(ROOT/'native_font_proof.json',{'candidate':str(ROM),'candidate_sha256':sha(ROM.read_bytes()),'manuscript':str(MANUSCRIPT),'manuscript_sha256':sha(MANUSCRIPT.read_bytes()),'cases':cases,
        'all39_source_numeric_selection_complete_ABI_words_and_visible_ink_pass':True,'complete_native_font_cases':78,
        'ordinary_and_battle_each_mood0_4_5_controls_equal':True,'Sera24_special1845_1858_1871_included':True,
        'genuine_initialized_body_widget_source':ui_receipt,'four_original_actual_captain_states_used_no_captain_ID_substitution':True,
        'role_UI_clone_mood_byte_and_mode_fields_are_CPU_only_formatting_fixtures':True,'physical_condition0_and_other31_actor_bytes_preserved':True,
        'complete_split_repairs_ASCII_I_pure_silence_and_comic_symbols_pass':True,
        'review_sheet':str(path),'review_sheet_sha256':sha(path.read_bytes()),'visual_review_pending':True,'producer_sha256':sha(Path(__file__).read_bytes()),
        'layout_producer_sha256':sha(Path('scripts/mood_comments_layout_v979.py').read_bytes()),'registered_repack_original_copy_actual_RGB_and_gameplay_pending':True,'full_goal_complete':False})
    print('All39 mood messages in78 original selector/font controls pass;actual scenes and registered release remain pending.',flush=True)


if __name__=='__main__':main()
