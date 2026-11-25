"""All13 fatigue selectors and full native words in both ordinary and battle CPU controls."""
import struct
from pathlib import Path
from PIL import Image,ImageDraw

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.illness_critical_layout_v974 import layout,compiled
ROM=Path('out/all_routes_combined_v2284_candidate.nds')
MANUSCRIPT=Path('translations/illness_critical_contextual_editorial_manuscript_v1.json')
IDS=tuple(range(1807,1833))
from scripts.prepare_work_comments_v842 import snapshot,machine_at
from scripts.probe_work_fonts_v843 import prepare_model as original_prepare,execute as original_execute
from types import FunctionType
from scripts.verify_personal_gameplay_v841 import actual_view,projected
from scripts.probe_common_single_cache_v862 import Loader
from dk4tool.patch.refit_contextual_spritsail_v1 import current_entries
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/illness_critical_fonts_v2472')
BASE=0x02000000


def prepare_condition(arm,raw,actor,mode,status):
    cpu,get=machine_at(arm,raw);actors=get(0xCB184);hero=get(0x7F244)
    assert arm[0x7E100:0x7E108]==bytes.fromhex('0600d0e51eff2fe1')
    obj=actors+struct.unpack_from('<I',arm,0x1229C)[0] if actor==hero else actors+4+actor*32
    before_actor=bytes(cpu.mem_read(obj,32));assert get(0x7E100,obj)==before_actor[6]==0
    context=get(0x3F0F8);old_mode=list(struct.unpack('<2I',cpu.mem_read(context+8,8)))
    cpu.mem_write(obj+6,bytes([status]));cpu.mem_write(context+8,struct.pack('<2I',*mode))
    assert get(0x7E100,obj)==status
    after_actor=bytes(cpu.mem_read(obj,32));assert after_actor==before_actor[:6]+bytes([status])+before_actor[7:]
    after=bytes(cpu.mem_read(BASE,len(raw)))
    changes=[{'address':BASE+i,'before':a,'after':b} for i,(a,b) in enumerate(zip(raw,after,strict=True)) if a!=b]
    assert all(r['address']==obj+6 or context+8<=r['address']<context+16 for r in changes)
    return after,{'actor_ID':actor,'actual_captain_ID':hero,'physical_condition_getter_source_hex':arm[0x7E100:0x7E108].hex(),
        'actor_object':obj,'source_actor_record_hex':before_actor.hex(),'CPU_actor_record_hex':after_actor.hex(),
        'original_condition':0,'CPU_condition':status,'source_mode_fields8_12':old_mode,'CPU_mode_fields8_12':list(mode),'changes':changes,
        'only_declared_condition_byte_and_mode_fields_change':True,'other31_actor_bytes_and_all_other_CPU_RAM_exact':True,
        'no_ROM_or_live_RAM_changes_not_actual_injury_acquisition':True}


def main():
    ROOT.mkdir(parents=True,exist_ok=True);assert not (ROOT/'native_font_proof.json').exists()
    rom=NdsImage.open(ROM);arm=rom.read_file('/__arm9__.bin');doc=read(MANUSCRIPT)
    assert sha(ROM.read_bytes())==doc['current_ROM_sha256']
    report=read('E:/Rota Nova translations/Generated/work/emulation_v193/gunnery_current_v2375_V2284/capture_report.json');assert report['ROM_sha256']==sha(ROM.read_bytes());ui_receipt=next(r for r in report['read_only_capture_RAM_snapshots']if r['frame']==4600);ui=Path(ui_receipt['path']).read_bytes();assert sha(ui)==ui_receipt['sha256'];view,parent,resource,header=actual_view(ui);projection=projected(rom,ui,view);assert projection[-1]['size']==[216,36]and projection[-1]['source_origin']==[0,60]and projection[-1]['destination']==[16,112];prepare_model=FunctionType(original_prepare.__code__,{**original_prepare.__globals__,'VIEW':view});execute=FunctionType(original_execute.__code__,{**original_execute.__globals__,'VIEW':view});common=rom.read_file('/COMMON/MESFILE.DK4');entries=current_entries(common,arm)
    npc,npc_receipt=snapshot('battle_personal_v897_893_Julio',14700)
    reps={0:4,1:16,2:9,3:7,4:5,5:6,6:14,7:19}
    heroes={0:('personal_activity_v839_838_Rafael_later',3200),1:('battle_gunnery_deck_v955_954_CaptainDeck',16500),
        2:('ceremony_Lil_approach_v825',23000),3:('ceremony_Maria_approach_v825',26000)}
    cases=[]
    for row in doc['records']:
        if row['special_actor_ID'] is not None:actor=row['special_actor_ID'];source,receipt=npc,npc_receipt
        elif row['protagonist_ID'] is None:actor=reps[row['voice_class']];source,receipt=npc,npc_receipt
        else:actor=row['protagonist_ID'];source,receipt=snapshot(*heroes[actor])
        prepared,fixture=prepare_model(arm,source,actor,row['role_ID'],ui)
        lines=layout(row['english']);assert compiled(row)==entries[row['message_id']].text==bytes.fromhex(row['current_hex']);variants=[];planes=[]
        for name,mode,status in (('ordinary',(0,0),row['physical_condition_ID']),('battle',(0,1),row['physical_condition_ID'])):
            condition_raw,condition=prepare_condition(arm,prepared,actor,mode,status)
            case,plane=execute(rom,condition_raw,actor,row['role_ID'],row['message_id'],compiled(row),lines)
            assert case['complete_native_copy_macro_draw_and_ABI'] and case['full252x96_native_and_independent_canvas_equal']
            assert not any(plane[y*252+x] for y in range(60,96) for x in range(216,252))
            case.update(mode=name,physical_condition_fixture=condition,original_physical_selector_selected_condition4_5_message=True)
            variants.append(case);planes.append(plane)
        assert all(p==planes[0]for p in planes)
        path=ROOT/f'ID{row["message_id"]}_complete_native_ink.png'
        Image.frombytes('L',(252,96),bytes(0 if v else 255 for v in planes[0])).save(path)
        cases.append({'message_id':row['message_id'],'actor_ID':actor,'physical_condition_ID':row['physical_condition_ID'],'source_snapshot':receipt,
            'isolated_CPU_role_and_widget_fixture':fixture,'generated_native_lines':lines,'ordinary_and_battle_font_controls':variants,
            'both_original_selectors_full_canvas_and_words_equal':True,'all_body_ink_inside_registered216x36_crop':True,
            'preview':str(path),'preview_sha256':sha(path.read_bytes()),'native_ink_only_not_actual_RGB_scene_or_earned_condition':True})
        print(row['message_id'],[(len(x),x) for x in lines],flush=True)
    assert tuple(c['message_id'] for c in cases)==IDS
    sheet=Image.new('RGB',(3*442,9*104),'#263238');draw=ImageDraw.Draw(sheet)
    for i,case in enumerate(cases):
        x,y=i%3*442,i//3*104;draw.text((x+5,y+5),f"ID{case['message_id']} complete native body;actual pending",fill='white')
        with Image.open(case['preview']) as im:sheet.paste(im.crop((0,60,216,96)).resize((432,72),Image.Resampling.NEAREST),(x+5,y+25))
    path=ROOT/'all26_native_body_ink_masks_2x.png';sheet.save(path)
    loader=Loader(arm,common);copies=[loader.copy(n,entries[n].text,mode)for mode in('cold','warm')for n in IDS];assert len(copies)==52
    save(ROOT/'native_font_proof.json',{'ARM9_sha256':sha(arm),'COMMON_sha256':sha(common),'all52_native_cold_warm_copies':copies,'native_file_IO_explicit_host_contract':True,'all26_complete_native_cases':[dict(message_ID=c['message_id'],**c)for c in cases],'current_parent_projection_controls':1,'current_parent_projection_is_shared_ordinary_control_not_current_battle_GPU':True,'current_parent_draw_commands':projection,'candidate':str(ROM),'candidate_sha256':sha(ROM.read_bytes()),
        'manuscript':str(MANUSCRIPT),'manuscript_sha256':sha(MANUSCRIPT.read_bytes()),'cases':cases,
        'all26_source_numeric_selection_complete_ABI_words_and_visible_ink_pass':True,'complete_native_font_cases':52,
        'ordinary_and_battle_each_condition4_5_controls_equal':True,'Sera24_special1819_1832_included':True,
        'genuine_initialized_body_widget_source':ui_receipt,'four_original_actual_captain_states_used_no_captain_ID_substitution':True,
        'role_UI_clone_condition_byte_and_mode_fields_are_CPU_only_formatting_fixtures':True,
        'complete_independent1821_1822_ASCII_I_Camille_and_Sera_words_pass':True,
        'review_sheet':str(path),'review_sheet_sha256':sha(path.read_bytes()),'review_sheets':[dict(path=str(path),sha256=sha(path.read_bytes()))],'visual_review_pending':True,
        'producer_sha256':sha(Path(__file__).read_bytes()),'layout_producer_sha256':sha(Path('scripts/illness_critical_layout_v974.py').read_bytes()),
        'registered_repack_original_copy_actual_RGB_and_gameplay_pending':True,'full_goal_complete':False})
    print('All26 illness/critical messages in52 original selector/font controls pass;actual scenes and registered release still pending.',flush=True)


if __name__=='__main__':main()
