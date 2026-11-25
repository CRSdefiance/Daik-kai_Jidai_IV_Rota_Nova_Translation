"""All25 original battle-personal selections and complete native body ink."""

import struct
from pathlib import Path
from PIL import Image,ImageDraw

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.battle_personal_layout_v892 import layout,compiled
from scripts.prepare_battle_personal_prose_v891 import ROM,MANUSCRIPT,IDS
from scripts.prepare_work_comments_v842 import snapshot,machine_at
from scripts.probe_work_fonts_v843 import prepare_model,execute
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/battle_personal_v892')
BASE=0x02000000


def battle_context(arm,raw):
    cpu,get=machine_at(arm,raw);context=get(0x3F0F8)
    old=list(struct.unpack('<2I',cpu.mem_read(context+8,8)))
    assert old!=[0,1]
    cpu.mem_write(context+8,struct.pack('<2I',0,1))
    after=bytes(cpu.mem_read(BASE,len(raw)))
    owned=list(range(context+8,context+16))
    changes=[{'address':BASE+i,'before':a,'after':b} for i,(a,b) in enumerate(zip(raw,after,strict=True)) if a!=b]
    assert all(c['address'] in owned for c in changes)
    return after,{'original_context_getter':BASE+0x3F0F8,'mode_object':context,'source_fields8_12':old,
        'CPU_only_mode_fields8_12':[0,1],'owned_bytes':owned,'actual_changed_bytes':changes,
        'only_source_mode_fields_changed_after_declared_model_fixture':True,
        'actual_battle_initializer_or_live_gameplay_not_claimed':True}


def main():
    ROOT.mkdir(parents=True,exist_ok=True);assert not (ROOT/'native_font_proof.json').exists()
    rom=NdsImage.open(ROM);arm=rom.read_file('/__arm9__.bin');doc=read(MANUSCRIPT)
    assert sha(ROM.read_bytes())==doc['current_ROM_sha256']
    ui,ui_receipt=snapshot('personal_cabin_v840_838_Charles_after',4600)
    npc,npc_receipt=snapshot('gunnery_deck_v889_888_JoakimDeck',3400)
    heroes={0:('personal_activity_v839_838_Rafael_later',3200),1:('gunnery_deck_v889_888_JoakimDeck',3400),
        2:('ceremony_Lil_approach_v825',23000),3:('ceremony_Maria_approach_v825',26000)}
    cases=[]
    for row in doc['records']:
        actor=row['actor_ID']
        if actor<4:source,receipt=snapshot(*heroes[actor])
        else:source,receipt=npc,npc_receipt
        prepared,fixture=prepare_model(arm,source,actor,12,ui)
        prepared,mode=battle_context(arm,prepared)
        lines=layout(row['english'])
        case,plane=execute(rom,prepared,actor,12,row['message_id'],compiled(row),lines)
        assert case['complete_native_copy_macro_draw_and_ABI'] and case['full252x96_native_and_independent_canvas_equal']
        assert not any(plane[y*252+x] for y in range(60,96) for x in range(216,252))
        assert all(len(line)<=36 for line in lines) and len(lines)<=3
        path=ROOT/f'ID{row["message_id"]}_complete_native_ink.png'
        Image.frombytes('L',(252,96),bytes(0 if v else 255 for v in plane)).save(path)
        case.update(source_snapshot=receipt,isolated_CPU_model_fixture=fixture,isolated_CPU_battle_predicate_fixture=mode,
            all_body_ink_inside_registered216x36_crop=True,all_lines_left_aligned_at_zero=True,
            original_main_selector_working_path_selected_expected_battle_personal_ID=True,
            preview=str(path),preview_sha256=sha(path.read_bytes()),native_ink_only_not_actual_RGB_battle_or_earned_assignment=True)
        cases.append(case);print(row['message_id'],[(len(x),x) for x in lines],flush=True)
    assert tuple(c['message_id'] for c in cases)==IDS
    sheet=Image.new('RGB',(3*442,9*104),'#263238');draw=ImageDraw.Draw(sheet)
    for i,case in enumerate(cases):
        x,y=i%3*442,i//3*104
        draw.text((x+5,y+5),f"ID{case['message_id']}: original native body; battle UI pending",fill='white')
        with Image.open(case['preview']) as im:
            sheet.paste(im.crop((0,60,216,96)).resize((432,72),Image.Resampling.NEAREST),(x+5,y+25))
    path=ROOT/'all25_native_body_ink_masks_2x.png';sheet.save(path)
    save(ROOT/'native_font_proof.json',{'candidate':str(ROM),'candidate_sha256':sha(ROM.read_bytes()),
        'manuscript':str(MANUSCRIPT),'manuscript_sha256':sha(MANUSCRIPT.read_bytes()),'cases':cases,
        'all25_original_battle_numeric_selection_complete_ABI_words_and_visible_ink_pass':True,
        'all25_x0_aligned_words_inside216x36_crop':True,
        'genuine_initialized_body_widget_source':ui_receipt,
        'four_original_actual_captain_states_used_no_captain_ID_substitution':True,
        'role_assignments_UI_clone_and_battle_mode_are_CPU_only_formatting_fixtures':True,
        'review_sheet':str(path),'review_sheet_sha256':sha(path.read_bytes()),'visual_review_pending':True,
        'producer_sha256':sha(Path(__file__).read_bytes()),'layout_producer_sha256':sha(Path('scripts/battle_personal_layout_v892.py').read_bytes()),
        'registered_repack_original_copy_actual_RGB_battle_and_gameplay_pending':True,'full_goal_complete':False})
    print('All25 original battle selectors,native words,left alignment and216x36 bounds pass;actual battle UI pending.',flush=True)


if __name__=='__main__':main()
