"""Complete work-comment bitmap/RGB holds, declared fixtures and ordinary returns."""

from pathlib import Path
from types import FunctionType

from PIL import Image,ImageDraw

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.work_comments_editorial import current_entries
from dk4tool.rom.nds import NdsImage
from scripts.finish_refit_display_v712 import load
from scripts.native_work_room_fixture_v846 import assign,CASES as FIXTURE_CASES
from scripts.verify_personal_gameplay_v841 import hold as previous_hold,model_state,get_machine
from scripts.work_comments_layout_v843 import compiled,layout
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/work_comments_v846')
ROM=Path('out/all_routes_combined_v845_candidate.nds')
CAP=Path('E:/Rota Nova translations/Generated/work/emulation_v193')
CASES={'GerhardShipwright':1387,'ManuelDoctor':1405,'HodramShipwright':1395,'JanusDoctor':1398}
hold=FunctionType(previous_hold.__code__,{**previous_hold.__globals__,'layout':layout})


def main():
    rom=NdsImage.open(ROM);digest=sha(ROM.read_bytes());arm=rom.read_file('/__arm9__.bin')
    entries=current_entries(rom.read_file('/COMMON/MESFILE.DK4'),arm)
    rows={r['message_id']:r for r in read('translations/work_comments_editorial_manuscript_v3.json')['records']}
    holds,controls,receipts,images,fixture_proofs=[],[],{},{},[]
    for label,number in CASES.items():
        folder=CAP/f'work_comments_v846_845_{label}_scheduled'
        report,shots,receipt=load(folder,digest,4800)
        receipts[label]=receipt;images[label]=shots
        data={}
        for s in report.get('read_only_capture_RAM_snapshots',[])+report.get('read_only_pause_RAM_snapshots',[]):
            raw=Path(s['path']).read_bytes()
            assert s['read_only_export'] and len(raw)==0x400000 and sha(raw)==s['sha256']
            assert s['frame'] not in data or data[s['frame']]==raw
            data[s['frame']]=raw
        donor=report['battery_save_preloaded'];plan=read(ROOT/f'845_{label}_scheduled_run_plan.json')
        assert donor['copied_byte_exact_before_cold_boot'] and donor['source']!=donor['destination']
        assert sha(Path(donor['source']).read_bytes())==sha(Path(plan['source_donor']).read_bytes())==donor['source_sha256']
        fs=report['synthetic_work_room_occupant_fixtures'];assert len(fs)==1
        fixture=fs[0];assert fixture['frame']==3200 and fixture['case']==label
        after,replay=assign(arm,data[3200],label)
        assert replay=={k:v for k,v in fixture.items() if k!='frame'}
        assert sha(after)==fixture['after_RAM_sha256']
        assert report['controlled_work_room_adapter']['original_harness_file_unchanged']
        assert not any(v for k,v in report.items() if k.startswith('synthetic_') and k!='synthetic_work_room_occupant_fixtures')
        fixture_proofs.append(fixture)
        row={**rows[number],'actor_ID':FIXTURE_CASES[label][0]}
        assert entries[number].text==compiled(row)
        for frame in (4200,4400):
            item=hold(rom,data[frame],shots[frame],row,12)
            assert item['source_role_type']==FIXTURE_CASES[label][1] and item['original_parent_activity_state']==0
            item.update(case=label,frame=frame,disclosed_room_fixture=True)
            holds.append(item)
        a,b=model_state(arm,data[3400]),model_state(arm,data[4800])
        assert a==b,(label,a,b)
        cpu,get=get_machine(arm,data[3400]);hero=get(0xCB184)+0x19E4
        assert data[3400][hero-0x2000000:hero-0x2000000+32]==data[4800][hero-0x2000000:hero-0x2000000+32]
        controls.append({'case':label,'before_frame':3400,'normal_return_frame':4800,
            'all_scoped_funds_calendar_assignments_owned_actor_ship_Hull_Crew_equal':True,
            'actual_captain32_byte_object_equal':True,'state':a})
    assert len(layout(rows[1398]['english'])[0])==19
    assert len(layout(rows[1405]['english'])[0])==36
    sheet=Image.new('RGB',(4*256,2*410),'#263238');draw=ImageDraw.Draw(sheet)
    for i,item in enumerate(holds):
        x,y=(i//2)*256,(i%2)*410
        draw.text((x+4,y+4),f"{item['case']} ID{item['message_id']}",fill='white')
        sheet.paste(images[item['case']][item['frame']],(x,y+24))
    path=ROOT/'actual8_complete_work_comment_holds.png';sheet.save(path)
    save(ROOT/'actual_gameplay_verification.json',{'candidate':str(ROM),'candidate_sha256':digest,
        'terminal_capture_receipts':receipts,'actual_complete_dialogue_holds':holds,
        'fixture_replays':fixture_proofs,'all_original_donors_and_harness_preserved':True,
        'scoped_normal_return_state_controls':controls,'odd19_character_first_row_and_complete_continuation_pass':True,
        'full36_cell_single_row_trailing_period_pass':True,'actual_original_captain_work_variant_pass':True,
        'review_sheet':str(path),'review_sheet_sha256':sha(path.read_bytes()),'visual_review_pending':True,
        'scope':'Eight complete native bitmap and framebuffer holds for four revised IDs,including NPC voices0,1,7 and real Hodram protagonist. Only2/3 declared room-type/occupant fixture bytes change;Janus remains faction21 and is not earned recruitment. Original selectors and text loading execute in actual cold-boot playback. Four normal cancels/returns preserve scoped funds,calendar,occupants,owned actors,actual captain and ship models. Other20 entries have complete source/native-font proof,not individual actual visits. No full-playthrough or hardware verification claim.',
        'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    print('Eight complete actual work-comment holds and four normal return state controls pass;visual review pending.',flush=True)


if __name__=='__main__':main()
