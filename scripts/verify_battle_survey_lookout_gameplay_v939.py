"""Full actual Survey/Lookout words and RGB,normal returns and glyph controls."""

import struct
from pathlib import Path
from PIL import Image,ImageDraw
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.battle_survey_lookout_flags_v939 import actual_view,hold,provenance
from scripts.battle_survey_lookout_layout_v936 import layout
from scripts.finish_refit_display_v712 import load
from scripts.verify_personal_gameplay_v841 import get_machine,model_state
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/battle_survey_lookout_v939')
ROM=Path('out/all_routes_combined_v938_candidate.nds')
CAP=Path('E:/Rota Nova translations/Generated/work/emulation_v193')
BASE=0x02000000
SPECS={'CaptainSurvey':(1718,1,3,True),'ClaudioSurvey':(1713,5,3,False),'YukihisaLookout':(1722,12,1,False),'CarloLookout':(1728,19,1,False)}


def rejected(action):
    try:action()
    except AssertionError:return True
    raise AssertionError('Corrupted observed display was accepted')


def main():
    assert not (ROOT/'actual_gameplay_verification.json').exists()
    selected=read(ROOT/'actual_sample_frame_plan.json');assert set(selected['cases'])==set(SPECS)
    rom=NdsImage.open(ROM);arm=rom.read_file('/__arm9__.bin');digest=sha(ROM.read_bytes())
    assert digest==read(ROM.with_suffix('.manifest.json'))['candidate_sha256']
    rows={r['message_id']:r for r in read('translations/battle_survey_lookout_editorial_manuscript_v2.json')['records']}
    holds=[];returns=[];receipts=[];fixture_receipts=[];images={};controls=[]
    for label,(number,actor,role,owned) in SPECS.items():
        spec=selected['cases'][label];baseline,frames,first_back,end=spec['baseline'],spec['holds'],spec['first_back'],spec['end']
        assert len(frames)==2 and baseline<frames[0]<frames[1]<first_back<end
        row={**rows[number],'actor_ID':actor};folder=CAP/f'battle_survey_lookout_v939_938_{label}'
        report,shots,receipt=load(folder,digest,end);receipts.append(receipt);images[label]=shots
        assert report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
        assert report['controlled_battle_survey_lookout_adapter']['original_harness_file_unchanged']
        assert report['controlled_battle_survey_lookout_adapter']['unchanged_harness_sha256']=='d5bcc9a11b5602bfb44d54e75b02a7a7a0165c9ee819a07cd0cbdac2130b8c6e'
        fixtures=report['synthetic_battle_survey_lookout_Cabin_assignment_fixtures'];assert len(fixtures)==1
        fixture=fixtures[0];assert fixture['case']==label and fixture['actor_ID']==actor and fixture['role_type']==role
        assert len(fixture['changes'])==(3 if owned else 2) and fixture['actor_owned_in_source_save']==owned
        assert fixture['all_other4MiB_RAM_including_battle_mode_actor_captain_health_money_calendar_RNG_text_code_exact']
        if owned:assert fixture['source_actual_battle_fields8_12']==[0,1]
        coordinates=report['synthetic_battle_recovery_proximity_fixtures'];assert len(coordinates)==2
        for f in coordinates:
            assert f['action']=='approach' and len(f['owned_bytes'])==8
            assert f['no_enemy_stats_war_outcome_reward_inventory_or_resource_flags_changed']
            assert f['actual_battle_mode_not_assigned_by_fixture'] and f['source_helpers_unchanged']
            assert all(c['address'] in f['owned_bytes'] for c in f['changes'])
        assert not any(v for k,v in report.items() if k.startswith('synthetic_') and k not in (
            'synthetic_battle_survey_lookout_Cabin_assignment_fixtures','synthetic_battle_recovery_proximity_fixtures'))
        assert read(ROOT/f'{label}_terminal_source_preservation.json')['source_and_disposable_donors_unchanged']
        data={n:(folder/f'frame_{n:06d}_arm9_ram.bin').read_bytes() for n in (4800,baseline,*frames,first_back,end)}
        cpu,get=get_machine(arm,data[4800]);mode=get(0x3F0F8)
        assert list(struct.unpack('<2I',cpu.mem_read(mode+8,8)))==[0,0]
        before=model_state(arm,data[baseline]);captain_before=None
        for n in frames:
            raw=data[n];cpu,get=get_machine(arm,raw);mode=get(0x3F0F8)
            assert list(struct.unpack('<2I',cpu.mem_read(mode+8,8)))==[0,1] and get(0x7F244)==1
            case=hold(rom,raw,shots[n],row,12);assert case['source_role_type']==role
            assert model_state(arm,raw)==before
            captain=get(0xCB184)+struct.unpack_from('<I',arm,0x1229C)[0]
            current=raw[captain-BASE:captain-BASE+32]
            if captain_before is None:captain_before=current
            assert current==captain_before
            case.update(case=label,frame=n,original_mode_fields8_12=[0,1],original_battle_mode_not_assigned_by_any_fixture=True,
                RAM_sha256=sha(raw),actual_screen_sha256=sha((folder/f'frame_{n:06d}_navigation.png').read_bytes()))
            holds.append(case)
        assert model_state(arm,data[first_back])==before and rejected(lambda:actual_view(data[end]))
        after=model_state(arm,data[end]);cpu,get=get_machine(arm,data[end]);assert get(0x7F244)==1
        assert before['all31_original_occupant_bytes']==after['all31_original_occupant_bytes']
        assert before['funds']==after['funds'] and after['calendar_tick']>before['calendar_tick']
        returns.append({'case':label,'first_back_frame':first_back,'normal_sea_return_frame':end,
            'all_scoped_state_equal_through_first_back':True,'two_holds_actual_captain32_bytes_equal':True,
            'no_active_Cabin_view_after_normal_return':True,'assignments_and_funds_unchanged_on_return':True,
            'ordinary_battle_time_resumes_after_return':True,'state_while_UI_open':before,'state_after_resumed_battle':after,
            'no_claim_that_world_ship_or_RNG_state_is_frozen_during_resumed_combat':True})
        fixture_receipts.append({'case':label,'room_fixture':fixture,'coordinate_fixtures':coordinates})
        raw=data[frames[0]];view,parent,resource,h=actual_view(raw);bad=bytearray(raw)
        struct.pack_into('<I',bad,resource-BASE,(h[0]&0xFFFFFF00)|5)
        controls.append({'case':label,'negative':'wrong-format-low-byte','rejected':rejected(lambda:actual_view(bytes(bad)))})
        lines=layout(row['english']);cells=[(0,0,'delete-initial-glyph'),(len(lines)-1,len(lines[-1])-1,'delete-final-punctuation')]
        if label=='CaptainSurvey':cells.extend([(1,0,'delete-second-row-t'),(2,0,'delete-third-row-m')])
        for line,column,name in cells:
            bad=bytearray(raw);pixels=((resource+h[4])&0xFFFFFFFF)-BASE
            for y in range(60+line*12,71+line*12):
                at=pixels+y*126+column*3;bad[at:at+3]=b'\0'*3
            controls.append({'case':label,'negative':name,'rejected':rejected(lambda:hold(rom,bytes(bad),shots[frames[0]],row,12))})
    assert layout(rows[1718]['english'])==["Even if I'm not fighting,",'taking these measurements','matters, too...']
    assert len(layout(rows[1713]['english'])[0])==36
    assert layout(rows[1722]['english'])==["Let's try to snipe their admiral",'during the boarding action.']
    assert layout(rows[1728]['english'])[0].startswith("I'm")
    sheet=Image.new('RGB',(4*256,2*410),'#263238');draw=ImageDraw.Draw(sheet)
    for i,item in enumerate(holds):
        x,y=(i//2)*256,(i%2)*410;draw.text((x+4,y+4),f"{item['case']} ID{item['message_id']}",fill='white')
        sheet.paste(images[item['case']][item['frame']],(x,y+24))
    path=ROOT/'eight_complete_actual_battle_holds.png';sheet.save(path)
    back=Image.new('RGB',(4*256,410),'#263238');draw=ImageDraw.Draw(back)
    for i,label in enumerate(SPECS):
        draw.text((i*256+4,4),label,fill='white');back.paste(images[label][selected['cases'][label]['end']],(i*256,24))
    back_path=ROOT/'four_normal_battle_returns.png';back.save(back_path)
    save(ROOT/'actual_gameplay_verification.json',{'candidate':str(ROM),'candidate_sha256':digest,
        'terminal_capture_receipts':receipts,'actual_complete_dialogue_holds':holds,'fixture_receipts':fixture_receipts,
        'eight_full252x36_native_and216x36_RGB_word_and_blank_planes_pass':True,
        'complete_three_row1718_full36cell1713_boarding1722_initial_I1728_pass':True,
        'original_battle_Survey3_Lookout1_and_genuine_captain1_pass':True,
        'all_original_donors_and_harness_preserved':True,'scoped_normal_return_controls':returns,
        'offline_deletion_and_bad_header_controls':controls,'original_consumer_scope':provenance(),
        'review_sheet':str(path),'review_sheet_sha256':sha(path.read_bytes()),'return_review_sheet':str(back_path),
        'return_review_sheet_sha256':sha(back_path.read_bytes()),'visual_review_pending':True,
        'scope':"Four separate V938 fresh cold boots verify genuine captain1 Survey3 also-matters1718 across three full rows,Claudio5 Survey3 full36cell1713,Yukihisa12 Lookout1 boarding-action sniping1722 and Carlo19 Lookout1 full initial I1728. Each has two complete active-widget252x36 native/216x36 RGB holds and normal returns. Two declared coordinate approaches and two/three room/occupant bytes are isolated fixtures. Captain assignment follows actual observed original combat0/1;original travel assignments are preserved until then. No savestate,actor/captain replacement,battle-mode,outcome,health,money or text injection. Other20 entries,including the four retained wordings and subject-neutral Maria1720,have full source/native-font proof rather than individual actual visits. No earned recruitment,refit,travel,complete-route or hardware claim.",
        'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    print('Eight actual Survey/Lookout holds,four returns and14 negative controls pass;visual review pending.',flush=True)


if __name__=='__main__':main()
