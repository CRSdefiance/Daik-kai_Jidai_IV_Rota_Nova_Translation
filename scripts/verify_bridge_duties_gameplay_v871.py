"""Complete Captain5/FirstMate6/Helm4 native/RGB holds,original selectors,fixture replays and returns."""

from pathlib import Path
from types import FunctionType

from PIL import Image,ImageDraw

from dk4tool.patch.bridge_duties_editorial import current_entries
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.finish_refit_display_v712 import load
from scripts.native_bridge_duties_fixture_v871 import assign,CASES as FIXTURE_CASES
from scripts.verify_personal_gameplay_v841 import hold as prior_hold,model_state,get_machine
from scripts.bridge_duties_layout_v869 import compiled,layout
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/bridge_duties_v871')
ROM=Path('out/all_routes_combined_v870_candidate.nds')
CAP=Path('E:/Rota Nova translations/Generated/work/emulation_v193')
CASES={'JoakimCaptain':1472,'CamilleMate':1477,'JoakimMate':1484,'CamilleHelm':1489}
hold=FunctionType(prior_hold.__code__,{**prior_hold.__globals__,'layout':layout})


def main():
    rom=NdsImage.open(ROM);digest=sha(ROM.read_bytes());arm=rom.read_file('/__arm9__.bin')
    entries=current_entries(rom.read_file('/COMMON/MESFILE.DK4'),arm)
    rows={r['message_id']:r for r in read('translations/bridge_duties_editorial_manuscript_v2.json')['records']}
    holds,controls,receipts,images,fixture_proofs=[],[],{},{},[]
    for label,number in CASES.items():
        folder=CAP/f'bridge_duties_v871_870_{label}'
        report,shots,receipt=load(folder,digest,4800);receipts[label]=receipt;images[label]=shots
        data={}
        for item in report.get('read_only_capture_RAM_snapshots',[])+report.get('read_only_pause_RAM_snapshots',[]):
            raw=Path(item['path']).read_bytes()
            assert item['read_only_export'] and len(raw)==0x400000 and sha(raw)==item['sha256']
            assert item['frame'] not in data or data[item['frame']]==raw
            data[item['frame']]=raw
        donor=report['battery_save_preloaded'];plan=read(ROOT/f'{label}_run_plan.json')
        assert donor['copied_byte_exact_before_cold_boot'] and donor['source']!=donor['destination']
        assert sha(Path(donor['source']).read_bytes())==sha(Path(plan['source_donor']).read_bytes())==donor['source_sha256']
        assert sha(Path(plan['recorded_navigation']).read_bytes())==plan['recorded_navigation_sha256']
        fixtures=report['synthetic_bridge_duties_assignment_fixtures'];assert len(fixtures)==1
        fixture=fixtures[0];assert fixture['frame']==3200 and fixture['case']==label
        after,replay=assign(arm,data[3200],label);assert replay=={k:v for k,v in fixture.items() if k!='frame'}
        assert sha(after)==fixture['after_RAM_sha256']
        assert report['controlled_bridge_duties_adapter']['original_harness_file_unchanged']
        assert not any(v for k,v in report.items() if k.startswith('synthetic_') and k!='synthetic_bridge_duties_assignment_fixtures')
        fixture_proofs.append(fixture)
        row={**rows[number],'actor_ID':FIXTURE_CASES[label][0]};assert entries[number].text==compiled(row)
        for frame in (4200,4400):
            item=hold(rom,data[frame],shots[frame],row,12)
            assert item['source_role_type']==FIXTURE_CASES[label][1] and item['original_parent_activity_state']==0
            item.update(case=label,frame=frame,disclosed_Planning_Finance_fixture=True);holds.append(item)
        a,b=model_state(arm,data[3400]),model_state(arm,data[4800]);assert a==b,(label,a,b)
        cpu,get=get_machine(arm,data[3400]);hero=get(0xCB184)+0x19E4
        assert data[3400][hero-0x2000000:hero-0x2000000+32]==data[4800][hero-0x2000000:hero-0x2000000+32]
        controls.append({'case':label,'before_frame':3400,'normal_return_frame':4800,
            'all_scoped_funds_calendar_assignments_owned_actor_ship_Hull_Crew_equal':True,
            'actual_captain32_byte_object_equal':True,'state':a})
    assert len(layout(rows[1489]['english'])[0])==25 and layout(rows[1489]['english'])[1]=='Hard starboard!'
    assert layout(rows[1477]['english'])==["I'll handle the diplomatic talks!"]
    assert {f['case']:f['actor_owned_in_original_save'] for f in fixture_proofs}=={'JoakimCaptain':True,'CamilleMate':False,'JoakimMate':True,'CamilleHelm':False}
    assert all(f['original_actor_faction']==f['player_company'] for f in fixture_proofs if f['actor_owned_in_original_save'])
    assert all(f['original_actor_faction']!=f['player_company'] for f in fixture_proofs if not f['actor_owned_in_original_save'])
    sheet=Image.new('RGB',(4*256,2*410),'#263238');draw=ImageDraw.Draw(sheet)
    for i,item in enumerate(holds):
        x,y=(i//2)*256,(i%2)*410;draw.text((x+4,y+4),f"{item['case']} ID{item['message_id']}",fill='white')
        sheet.paste(images[item['case']][item['frame']],(x,y+24))
    path=ROOT/'actual8_complete_bridge_duties_holds.png';sheet.save(path)
    returns=Image.new('RGB',(4*256,410),'#263238');draw=ImageDraw.Draw(returns)
    for i,label in enumerate(CASES):
        draw.text((i*256+4,4),label,fill='white');returns.paste(images[label][4800],(i*256,24))
    returns_path=ROOT/'four_normal_town_returns.png';returns.save(returns_path)
    save(ROOT/'actual_gameplay_verification.json',{'candidate':str(ROM),'candidate_sha256':digest,
        'terminal_capture_receipts':receipts,'actual_complete_dialogue_holds':holds,'fixture_replays':fixture_proofs,
        'all_original_donors_and_harness_preserved':True,'scoped_normal_return_state_controls':controls,
        'actual_capital_I1477_and_odd25_first_row_complete_aligned_starboard_continuation_pass':True,
        'all_three_original_roles5_6_4_and_actual_bodies_pass':True,'real_current_captain_strongest_fleet_and_first_mate_joke_pass':True,
        'review_sheet':str(path),'review_sheet_sha256':sha(path.read_bytes()),
        'return_review_sheet':str(returns_path),'return_review_sheet_sha256':sha(returns_path.read_bytes()),'visual_review_pending':True,
        'scope':'Eight complete bitmap/RGB holds sample1472 Joakim strongest-fleet resolve,1477 Camille first-person diplomatic offer,1484 Joakim first-mate joke,and1489 Camille hard-starboard order after odd25-character first row. All three original roles5/6/4 execute. Each disposable Copenhagen run changes only2/3 room/occupant bytes;Joakim remains actual captain and Camille keeps her original foreign faction. Four normal returns preserve scoped funds,calendar,31 assignments,owned actors,actual captain and ship models. Other24 entries have full source/native-font proof,not individual actual visits. No full route,earned assignment/recruitment or hardware claim.',
        'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    print('Eight complete actual bridge duties holds and four normal return state controls pass;visual review pending.',flush=True)


if __name__=='__main__':main()
