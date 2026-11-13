"""Six complete actual battle holds,ordinary discrimination,and normal returns."""

import struct
from pathlib import Path
from PIL import Image,ImageDraw

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.battle_personal_actual_v898 import actual_view,hold,provenance
from scripts.battle_personal_layout_v892 import layout
from scripts.finish_refit_display_v712 import load
from scripts.verify_personal_gameplay_v841 import get_machine,model_state
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/battle_personal_v898')
ROM=Path('out/all_routes_combined_v893_candidate.nds')
BASE=0x02000000
CAP=Path('E:/Rota Nova translations/Generated/work/emulation_v193')
CASES={'Julio':(1577,14300,(14500,14700),14900,15100),
    'Carlo':(1590,14300,(14500,14700),14900,15100),
    'Joakim':(1572,17100,(17300,17500),17700,17900)}


def rejected(action):
    try:action()
    except AssertionError:return True
    raise AssertionError('Corrupted observed display was accepted')


def main():
    assert not (ROOT/'actual_gameplay_verification.json').exists()
    assert sha(Path('scripts/verify_personal_gameplay_v841.py').read_bytes())=='bee09ebfe59293db935a895ede383a6f0310bd1aa4b1fbb44e5efc328ce628e3'
    helper=read(ROOT/'Julio_two_actual_holds_PRELIMINARY.json')['original_consumer_scope']['successor_sha256']
    assert sha(Path('scripts/battle_personal_actual_v898.py').read_bytes())==helper
    rom=NdsImage.open(ROM);arm=rom.read_file('/__arm9__.bin');digest=sha(ROM.read_bytes())
    assert digest==read(ROM.with_suffix('.manifest.json'))['candidate_sha256']
    doc=read('translations/battle_personal_editorial_manuscript_v2.json');rows={r['message_id']:r for r in doc['records']}
    holds=[];returns=[];receipts=[];fixture_receipts=[];images={};controls=[]
    for label,(number,baseline,frames,first_back,end) in CASES.items():
        folder=CAP/f'battle_personal_v897_893_{label}'
        report,shots,receipt=load(folder,digest,end);receipts.append(receipt);images[label]=shots
        assert report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
        assert report['controlled_battle_personal_adapter']['original_harness_file_unchanged']
        assert report['controlled_battle_personal_adapter']['unchanged_harness_sha256']=='d5bcc9a11b5602bfb44d54e75b02a7a7a0165c9ee819a07cd0cbdac2130b8c6e'
        assert len(report['synthetic_battle_recovery_proximity_fixtures'])==2
        fixture=report['synthetic_battle_personal_Cabin_assignment_fixtures'];assert len(fixture)==1
        fixture=fixture[0];assert fixture['case']==label and fixture['actor_ID']==rows[number]['actor_ID']
        assert len(fixture['changes'])==(2 if label=='Joakim' else 1)
        assert fixture['all_other4MiB_RAM_including_battle_mode_actor_captain_health_money_calendar_RNG_text_code_exact']
        for f in report['synthetic_battle_recovery_proximity_fixtures']:
            assert f['action']=='approach' and len(f['owned_bytes'])==8
            assert f['no_enemy_stats_war_outcome_reward_inventory_or_resource_flags_changed']
            assert f['actual_battle_mode_not_assigned_by_fixture'] and f['source_helpers_unchanged']
            assert all(c['address'] in f['owned_bytes'] for c in f['changes'])
        preservation=read(f'work/analysis/battle_personal_v897/{label}_terminal_source_preservation.json')
        assert preservation['source_and_disposable_donors_unchanged']
        data={n:(folder/f'frame_{n:06d}_arm9_ram.bin').read_bytes() for n in (4800,baseline,*frames,first_back,end)}
        initial_cpu,initial_get=get_machine(arm,data[4800]);mode=initial_get(0x3F0F8)
        assert list(struct.unpack('<2I',initial_cpu.mem_read(mode+8,8)))==[0,0]
        state_before=model_state(arm,data[baseline]);captain_before=None
        for n in frames:
            raw=data[n];cpu,get=get_machine(arm,raw);mode=get(0x3F0F8)
            assert list(struct.unpack('<2I',cpu.mem_read(mode+8,8)))==[0,1] and get(0x7F244)==1
            case=hold(rom,raw,shots[n],rows[number],12)
            assert case['native_image_header_first_word_with_flags_preserved']==0x0E04
            assert model_state(arm,raw)==state_before
            captain=get(0xCB184)+struct.unpack_from('<I',arm,0x1229C)[0]
            current_captain=raw[captain-BASE:captain-BASE+32]
            if captain_before is None:captain_before=current_captain
            assert current_captain==captain_before
            case.update(case=label,frame=n,original_mode_fields8_12=[0,1],
                original_battle_mode_not_assigned_by_any_fixture=True,RAM_sha256=sha(raw),
                actual_screen_sha256=sha((folder/f'frame_{n:06d}_navigation.png').read_bytes()))
            holds.append(case)
        assert model_state(arm,data[first_back])==state_before
        assert rejected(lambda:actual_view(data[end]))
        after=model_state(arm,data[end]);cpu,get=get_machine(arm,data[end]);assert get(0x7F244)==1
        assert after['all31_original_occupant_bytes']==state_before['all31_original_occupant_bytes']
        assert after['funds']==state_before['funds']
        assert after['calendar_tick']>state_before['calendar_tick']
        returns.append({'case':label,'first_back_frame':first_back,'normal_sea_return_frame':end,
            'all_scoped_state_equal_through_first_back':True,'two_holds_actual_captain32_bytes_equal':True,
            'no_active_Cabin_view_after_normal_return':True,'assignments_and_funds_unchanged_on_return':True,
            'ordinary_battle_time_resumes_after_return':True,'state_while_UI_open':state_before,'state_after_resumed_battle':after,
            'no_claim_that_world_ship_or_RNG_state_is_frozen_during_resumed_combat':True})
        fixture_receipts.append({'case':label,'Cabin_fixture':fixture,'coordinate_fixtures':report['synthetic_battle_recovery_proximity_fixtures']})
        # Offline deletion controls only;these bytes are never loaded into a game.
        raw=data[frames[0]];view,parent,resource,h=actual_view(raw)
        bad=bytearray(raw);struct.pack_into('<I',bad,resource-BASE,0x0E05)
        controls.append({'case':label,'negative':'wrong-format-low-byte','rejected':rejected(lambda:actual_view(bytes(bad)))})
        if label in ('Carlo','Julio'):
            x=6 if label=='Carlo' else (len(layout(rows[number]['english'])[1])-1)*6
            bad=bytearray(raw);pixels=((resource+h[4])&0xFFFFFFFF)-BASE
            for y in range(72,83):bad[pixels+y*126+x//2:pixels+y*126+x//2+3]=b'\0'*3
            controls.append({'case':label,'negative':'delete-leading-N-after-odd19-row' if label=='Carlo' else 'delete-final-exclamation',
                'rejected':rejected(lambda:hold(rom,bytes(bad),shots[frames[0]],rows[number],12))})
    ordinary=read(ROOT/'Carlo_ordinary_context_control.json')
    assert ordinary['actual_ordinary_hold']['native_original12104_numeric_selection']==[1380]
    assert ordinary['actual_ordinary_hold']['whole216x36_actual_RGB_ink_and_blank_plane_matches']
    assert len(layout(rows[1590]['english'])[0])==19
    assert layout(rows[1590]['english'])[1]=='(Nods off.) Zzz...'
    sheet=Image.new('RGB',(3*256,2*410),'#263238');draw=ImageDraw.Draw(sheet)
    for i,item in enumerate(holds):
        x,y=(i//2)*256,(i%2)*410;draw.text((x+4,y+4),f"{item['case']} ID{item['message_id']}",fill='white')
        sheet.paste(images[item['case']][item['frame']],(x,y+24))
    path=ROOT/'six_complete_actual_battle_holds.png';sheet.save(path)
    back=Image.new('RGB',(3*256,410),'#263238');draw=ImageDraw.Draw(back)
    for i,(label,spec) in enumerate(CASES.items()):
        draw.text((i*256+4,4),label,fill='white');back.paste(images[label][spec[-1]],(i*256,24))
    back_path=ROOT/'three_normal_battle_returns.png';back.save(back_path)
    save(ROOT/'actual_gameplay_verification.json',{'candidate':str(ROM),'candidate_sha256':digest,
        'terminal_capture_receipts':receipts,'actual_complete_dialogue_holds':holds,'fixture_receipts':fixture_receipts,
        'six_full252x36_native_and216x36_RGB_word_and_blank_planes_pass':True,
        'Carlo_odd19_row_complete_leading_N_and_nodding_direction_pass':True,
        'Julio_generic_drink_and_genuine_captain1_retained_comment_pass':True,
        'original_ordinary1380_versus_battle1590_discriminating_actual_control':ordinary,
        'all_original_donors_and_harness_preserved':True,'scoped_normal_return_controls':returns,
        'offline_deletion_and_bad_header_controls':controls,'original_consumer_scope':provenance(),
        'review_sheet':str(path),'review_sheet_sha256':sha(path.read_bytes()),'return_review_sheet':str(back_path),
        'return_review_sheet_sha256':sha(back_path.read_bytes()),'visual_review_pending':True,
        'scope':'Three independent fresh cold boots of registered V893 with original battle initialization. Two8-byte source-terrain-checked ship-coordinate approaches avoid immediate boarding;one/two original Cabin occupant bytes select the declared actor. No actor/captain identity,health,money,battle-mode,text,code,enemy or outcome replacement. Julio1577 and Carlo1590 revisions plus genuine captain1 retained1572 each have two complete actual/native holds. Ordinary Carlo1380 is a separate actual context control. UI-open state is stable through first Back;normal battle time resumes after leaving the UI. Other22 entries have all clean-source/context/native-font proofs,not individual actual visits. No earned recruitment/travel/full route or hardware claim.',
        'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    print('Six full actual battle holds,ordinary discriminating control,three normal returns and5 negative controls pass;visual review pending.',flush=True)


if __name__=='__main__':main()
