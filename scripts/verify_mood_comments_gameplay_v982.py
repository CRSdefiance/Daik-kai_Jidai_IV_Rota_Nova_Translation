"""Six targeted mood0/4/5 scenes:complete words,native/RGB bounds and normal returns."""
import struct
from pathlib import Path
from PIL import Image,ImageDraw
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.mood_comments_flags_v982 import actual_view,hold,provenance
from scripts.mood_comments_layout_v980 import layout
from scripts.finish_refit_display_v712 import load
from scripts.verify_personal_gameplay_v841 import get_machine,model_state
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/mood_comments_v982')
ROM=Path('out/all_routes_combined_v981_candidate.nds')
CAP=Path('E:/Rota Nova translations/Generated/work/emulation_v193')
BASE=0x02000000
SPECS={'CamillePositive': (1835, 9, False, 0), 'SeraPositive': (1845, 24, False, 0), 'CarloDejected': (1853, 19, False, 4), 'CaptainSilent': (1855, 1, True, 4), 'CaptainPanic': (1868, 1, True, 5), 'SeraPanic': (1871, 24, False, 5)}


def rejected(action):
    try:action()
    except AssertionError:return True
    raise AssertionError('Corrupted observed display accepted')


def main():
    assert not (ROOT/'actual_gameplay_verification.json').exists()
    rom=NdsImage.open(ROM);arm=rom.read_file('/__arm9__.bin');digest=sha(ROM.read_bytes())
    assert digest==read(ROM.with_suffix('.manifest.json'))['candidate_sha256']
    rows={r['message_id']:r for r in read('translations/mood_comments_editorial_manuscript_v2.json')['records']}
    holds=[];returns=[];receipts=[];fixtures=[];images={};controls=[]
    for label,(number,actor,owned,status) in SPECS.items():
        folder=CAP/f'mood_comments_v982_975_{label}';report,shots,receipt=load(folder,digest,16900);receipts.append(receipt);images[label]=shots
        assert report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
        adapter=report['controlled_mood_comments_adapter'];assert adapter['original_harness_file_unchanged']
        assert adapter['unchanged_harness_sha256']=='d5bcc9a11b5602bfb44d54e75b02a7a7a0165c9ee819a07cd0cbdac2130b8c6e'
        all_fixtures=report['synthetic_mood_comments_Cabin_assignment_fixtures'];assert len(all_fixtures)==2
        room=[f for f in all_fixtures if not f.get('synthetic_mood_comments_late_mood_fixture')];late=[f for f in all_fixtures if f.get('synthetic_mood_comments_late_mood_fixture')]
        assert len(room)==len(late)==1;room,late=room[0],late[0]
        assert room['case']==late['case']==label and room['actor_ID']==late['actor_ID']==actor
        assert room['role_type']==2 and room['source_condition']==0 and room['actor_owned_in_source_save']==owned
        assert len(room['changes'])==(3 if owned else 2) and room['all_other4MiB_RAM_including_battle_mode_actor_captain_health_money_calendar_RNG_text_code_exact']
        assert late['fixture_mood']==status and late['source_mood'] in (1,2,3) and len(late['changes'])==1
        assert late['only_mood_byte7_changes_all_other4MiB_including_physical_condition_exact'] and late['other31_actor_bytes_and_actor_captain_identity_exact']
        assert room['source_actual_battle_fields8_12']==[0,1] and read(ROOT/f'{label}_observed_original_combat.json')['native_combat_predicate_observed_before_any_room_or_mood_fixture']
        coordinates=report['synthetic_battle_recovery_proximity_fixtures'];assert len(coordinates)==2
        for f in coordinates:
            assert f['action']=='approach' and len(f['owned_bytes'])==8 and all(c['address'] in f['owned_bytes'] for c in f['changes'])
            assert f['no_enemy_stats_war_outcome_reward_inventory_or_resource_flags_changed'] and f['actual_battle_mode_not_assigned_by_fixture'] and f['source_helpers_unchanged']
        assert not any(v for k,v in report.items() if k.startswith('synthetic_') and k not in ('synthetic_mood_comments_Cabin_assignment_fixtures','synthetic_battle_recovery_proximity_fixtures'))
        assert read(ROOT/f'{label}_terminal_source_preservation.json')['source_and_disposable_donors_unchanged']
        data={n:(folder/f'frame_{n:06d}_arm9_ram.bin').read_bytes() for n in (4800,16100,16300,16500,16700,16900)}
        cpu,get=get_machine(arm,data[4800]);context=get(0x3F0F8);assert list(struct.unpack('<2I',cpu.mem_read(context+8,8)))==[0,0]
        before=model_state(arm,data[16100]);actor_record=None;captain_record=None;row={**rows[number],'actor_ID':actor}
        for n in (16300,16500):
            raw=data[n];cpu,get=get_machine(arm,raw);context=get(0x3F0F8)
            assert list(struct.unpack('<2I',cpu.mem_read(context+8,8)))==[0,1] and get(0x7F244)==1
            actors=get(0xCB184);captain=actors+struct.unpack_from('<I',arm,0x1229C)[0];obj=captain if actor==1 else actors+4+actor*32
            assert get(0x7E0B4,obj)==status and get(0x7E100,obj)==0
            body=raw[obj-BASE:obj-BASE+32];hero=raw[captain-BASE:captain-BASE+32]
            if actor_record is None:actor_record,captain_record=body,hero
            assert body==actor_record and hero==captain_record
            case=hold(rom,raw,shots[n],row,12);assert case['source_role_type']==2 and model_state(arm,raw)==before
            case.update(case=label,frame=n,actual_physical_condition_ID=0,actual_mood_ID=status,original_mode_fields8_12=[0,1],
                mood_is_disclosed_fixture_not_earned_acquisition=True,RAM_sha256=sha(raw),actual_screen_sha256=sha((folder/f'frame_{n:06d}_navigation.png').read_bytes()))
            holds.append(case)
        assert model_state(arm,data[16700])==before and rejected(lambda:actual_view(data[16900]))
        after=model_state(arm,data[16900]);assert before['all31_original_occupant_bytes']==after['all31_original_occupant_bytes']
        assert before['funds']==after['funds'] and after['calendar_tick']>before['calendar_tick']
        returns.append({'case':label,'baseline_frame':16100,'first_back_frame':16700,'normal_sea_return_frame':16900,
            'all_scoped_state_equal_through_first_back':True,'two_holds_selected_actor_and_captain32_bytes_exact':True,
            'no_active_Cabin_view_after_normal_return':True,'assignments_and_funds_unchanged_on_return':True,'ordinary_battle_time_resumes':True,
            'state_while_UI_open':before,'state_after_resumed_battle':after,'resumed_world_ship_and_RNG_not_claimed_frozen':True})
        fixtures.append({'case':label,'room_assignment_fixture':room,'late_mood_fixture':late,'coordinate_fixtures':coordinates})
        raw=data[16300];view,parent,resource,h=actual_view(raw);bad=bytearray(raw);struct.pack_into('<I',bad,resource-BASE,(h[0]&0xFFFFFF00)|5)
        controls.append({'case':label,'negative':'wrong-format-low-byte','rejected':rejected(lambda:actual_view(bytes(bad)))})
        lines=layout(row['english']);cells=[(0,0,'delete-initial-glyph'),(len(lines)-1,len(lines[-1])-1,'delete-final-punctuation')]
        extras={'CamillePositive': [(1, 0, 'delete-complete-I-continuation')], 'SeraPositive': [(0, 24, 'delete-now-final-w')], 'CarloDejected': [(1, 0, 'delete-aligned-Oh-after19cell-row'), (1, 30, 'delete-myself-final-f')], 'CaptainSilent': [(0, 1, 'delete-middle-silence-dot')], 'CaptainPanic': [(1, 0, 'delete-complete-at-continuation')], 'SeraPanic': [(0, 2, 'delete-comic-dollar'), (0, 3, 'delete-comic-star')]}
        for line,column,name in [*cells,*extras[label]]:
            bad=bytearray(raw);pixels=((resource+h[4])&0xFFFFFFFF)-BASE
            for y in range(60+line*12,71+line*12):
                at=pixels+y*126+column*3;bad[at:at+3]=b'\0'*3
            controls.append({'case':label,'negative':name,'rejected':rejected(lambda:hold(rom,bytes(bad),shots[16300],row,12))})
    assert len(holds)==12 and len(returns)==6 and len(controls)==26
    assert layout(rows[1835]['english'])==["I'm in top form!","I feel like I can do anything!"]
    assert layout(rows[1845]['english'])==['I feel fantastic right now!']
    assert layout(rows[1853]['english'])==['"Mutter, mutter..."','Oh, I was just talking to myself...']
    assert list(map(len,layout(rows[1853]['english'])))==[19,35]
    assert layout(rows[1855]['english'])==['...'] and rows[1855]['nonverbal_only']
    assert layout(rows[1868]['english'])==['No! I have to stay calm','at a time like this!']
    assert layout(rows[1871]['english'])==['@#$*!!'] and rows[1871]['nonverbal_only']
    sheet=Image.new('RGB',(6*256,2*410),'#263238');draw=ImageDraw.Draw(sheet)
    for i,item in enumerate(holds):
        x,y=(i//2)*256,(i%2)*410;draw.text((x+4,y+4),f"{item['case']} ID{item['message_id']}",fill='white');sheet.paste(images[item['case']][item['frame']],(x,y+24))
    path=ROOT/'twelve_complete_actual_mood_comments_holds.png';sheet.save(path)
    back=Image.new('RGB',(6*256,410),'#263238');draw=ImageDraw.Draw(back)
    for i,label in enumerate(SPECS):draw.text((i*256+4,4),label,fill='white');back.paste(images[label][16900],(i*256,24))
    back_path=ROOT/'six_normal_returns.png';back.save(back_path)
    save(ROOT/'actual_gameplay_verification.json',{'candidate':str(ROM),'candidate_sha256':digest,'terminal_capture_receipts':receipts,
        'actual_complete_dialogue_holds':holds,'fixture_receipts':fixtures,'twelve_full252x36_native_and216x36_RGB_word_and_blank_planes_pass':True,
        'complete_I1835_ASCII_I1845_quoted19_and35cell1853_pure_silence1855_self_calming1868_comic1871_pass':True,
        'all_original_donors_and_harness_preserved':True,'scoped_normal_return_controls':returns,'offline_deletion_and_bad_header_controls':controls,'original_consumer_scope':provenance(),
        'review_sheet':str(path),'review_sheet_sha256':sha(path.read_bytes()),'return_review_sheet':str(back_path),'return_review_sheet_sha256':sha(back_path.read_bytes()),'visual_review_pending':True,
        'scope':'Six separate V981 fresh cold boots:mood0 Camille9 ID1835 and Sera24 ASCII-I1845;mood4 Carlo19 quoted self-talk1853 (19cell quote,35cell aligned reply) and genuine captain1 pure silence1855;mood5 genuine captain1 personal self-calming1868 and Sera24 six comic symbols1871. Two complete native bitmap/actual RGB holds and normal return per case. Disclosed room assignment follows observed original combat0/1;one mood byte7 is inserted after Deck opens with physical health0 and all other RAM exact. Two coordinate approaches remain. No savestate,actor/captain identity or battle-mode/outcome/text/code injection,earned mood/recruitment/refit,full-route or hardware claim. Other33 entries have complete source/native font evidence,not individual actual visits.',
        'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    print('Twelve complete mood/panic holds,six returns and26 offline negative controls pass;visual review pending.',flush=True)


if __name__=='__main__':main()
