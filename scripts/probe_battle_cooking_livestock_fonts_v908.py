"""All25 original battle cooking/livestock numeric selections and full native words."""

import struct
from pathlib import Path
from PIL import Image,ImageDraw

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.battle_cooking_livestock_layout_v908 import layout,compiled
from scripts.prepare_battle_cooking_livestock_prose_v907 import ROM,MANUSCRIPT,IDS
from scripts.prepare_work_comments_v842 import snapshot,machine_at
from scripts.probe_work_fonts_v843 import prepare_model,execute
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/battle_cooking_livestock_v908')
BASE=0x02000000


def prepare_mode(arm,raw):
    cpu,get=machine_at(arm,raw);context=get(0x3F0F8)
    original=list(struct.unpack('<2I',cpu.mem_read(context+8,8)))
    if original==[0,1]:
        return raw,{'original_mode_fields8_12':original,'CPU_fields_changed':False,'genuine_source_battle_mode_preserved':True}
    cpu.mem_write(context+8,struct.pack('<2I',0,1));after=bytes(cpu.mem_read(BASE,len(raw)))
    changes=[{'address':BASE+i,'before':a,'after':b} for i,(a,b) in enumerate(zip(raw,after,strict=True)) if a!=b]
    assert all(context+8<=r['address']<context+16 for r in changes)
    return after,{'original_mode_fields8_12':original,'CPU_mode_fields8_12':[0,1],'CPU_fields_changed':True,
        'only_declared_CPU_mode_fields_changed':True,'changes':changes,'not_actual_battle_initialization':True}


def main():
    ROOT.mkdir(parents=True,exist_ok=True);assert not (ROOT/'native_font_proof.json').exists()
    rom=NdsImage.open(ROM);arm=rom.read_file('/__arm9__.bin');doc=read(MANUSCRIPT)
    assert sha(ROM.read_bytes())==doc['current_ROM_sha256']
    ui,ui_receipt=snapshot('personal_cabin_v840_838_Charles_after',4600)
    npc,npc_receipt=snapshot('battle_personal_v897_893_Julio',14700)
    reps={0:4,1:16,2:9,3:7,4:5,5:6,6:14,7:23}
    heroes={0:('personal_activity_v839_838_Rafael_later',3200),1:('battle_repair_medical_v905_904_CaptainRepair',14700),
        2:('ceremony_Lil_approach_v825',23000),3:('ceremony_Maria_approach_v825',26000)}
    cases=[]
    for row in doc['records']:
        if row.get('special_actor_ID') is not None:actor=row['special_actor_ID'];source,receipt=npc,npc_receipt
        elif row['protagonist_ID'] is None:actor=reps[row['voice_class']];source,receipt=npc,npc_receipt
        else:actor=row['protagonist_ID'];source,receipt=snapshot(*heroes[actor])
        prepared,fixture=prepare_model(arm,source,actor,row['role_ID'],ui)
        prepared,mode=prepare_mode(arm,prepared)
        lines=layout(row['english'])
        case,plane=execute(rom,prepared,actor,row['role_ID'],row['message_id'],compiled(row),lines)
        assert case['complete_native_copy_macro_draw_and_ABI'] and case['full252x96_native_and_independent_canvas_equal']
        assert not any(plane[y*252+x] for y in range(60,96) for x in range(216,252))
        path=ROOT/f'ID{row["message_id"]}_complete_native_ink.png'
        Image.frombytes('L',(252,96),bytes(0 if v else 255 for v in plane)).save(path)
        case.update(source_snapshot=receipt,isolated_CPU_fixture=fixture,source_or_CPU_battle_mode=mode,
            all_body_ink_inside_registered216x36_crop=True,original_working_selector_selected_battle_message=True,
            preview=str(path),preview_sha256=sha(path.read_bytes()),native_ink_only_not_actual_RGB_battle_or_earned_assignment=True)
        cases.append(case);print(row['message_id'],[(len(x),x) for x in lines],flush=True)
    assert tuple(c['message_id'] for c in cases)==IDS
    sheet=Image.new('RGB',(3*442,9*104),'#263238');draw=ImageDraw.Draw(sheet)
    for i,case in enumerate(cases):
        x,y=i%3*442,i//3*104;draw.text((x+5,y+5),f"ID{case['message_id']} complete native body;actual pending",fill='white')
        with Image.open(case['preview']) as im:sheet.paste(im.crop((0,60,216,96)).resize((432,72),Image.Resampling.NEAREST),(x+5,y+25))
    path=ROOT/'all25_native_body_ink_masks_2x.png';sheet.save(path)
    save(ROOT/'native_font_proof.json',{'candidate':str(ROM),'candidate_sha256':sha(ROM.read_bytes()),
        'manuscript':str(MANUSCRIPT),'manuscript_sha256':sha(MANUSCRIPT.read_bytes()),'cases':cases,
        'all25_source_numeric_selection_complete_ABI_words_and_visible_ink_pass':True,
        'genuine_initialized_body_widget_source':ui_receipt,'four_original_actual_captain_states_used_no_captain_ID_substitution':True,
        'role_assignments_UI_clone_and_declared_mode_fields_are_CPU_only_formatting_fixtures':True,
        'complete_ASCII_initial_I1639_Sera1632_and_all_source_words_pass':True,
        'review_sheet':str(path),'review_sheet_sha256':sha(path.read_bytes()),'visual_review_pending':True,
        'producer_sha256':sha(Path(__file__).read_bytes()),'layout_producer_sha256':sha(Path('scripts/battle_cooking_livestock_layout_v908.py').read_bytes()),
        'registered_repack_original_copy_actual_RGB_and_gameplay_pending':True,'full_goal_complete':False})
    print('All25 original battle selectors,complete fonts and216x36 bounds pass;actual scenes still pending.',flush=True)


if __name__=='__main__':main()
