"""Nine original-scene samples:18 complete font/RGB holds,returns and corruption controls."""
import struct
from pathlib import Path
from types import FunctionType
from PIL import Image,ImageDraw
from dk4tool.patch import activity_special_editorial_v987b as owned
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.activity_special_layout_v986b import compiled,visible_lines
from scripts.activity_special_flags_v988 import actual_view,hold,provenance
from scripts.native_activity_special_fixture_v988 import SPECS,assign
from scripts.verify_common_alignment_native_v257 import raster as original_raster
from scripts.verify_shipyard_gameplay_v760 import independent_font
from scripts.verify_personal_gameplay_v841 import get_machine,model_state
from scripts.verify_port_gameplay_v762 import cstring
from scripts.finish_refit_display_v712 import load
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/activity_special_v988')
ROM=Path('out/all_routes_combined_v987_candidate.nds')
CAP=Path('E:/Rota Nova translations/Generated/work/emulation_v193')
BASE=0x02000000

def rejected(action):
    try:action()
    except AssertionError:return True
    raise AssertionError('Corrupted observed display accepted')

def modal_hold(rom,raw,image,row):
    arm=rom.read_file('/__arm9__.bin');text=compiled(row);lines=visible_lines(row)
    owner,wrapped=[struct.unpack_from('<I',arm,n)[0] for n in (0x552A0,0x54450)]
    assert cstring(raw,owner+0x2030)==cstring(raw,wrapped)==text
    class CurrentFont:
        @staticmethod
        def open(path):assert path=='out/all_routes_combined_v255_candidate.nds';return rom
    raster=FunctionType(original_raster.__code__,{**original_raster.__globals__,'NdsImage':CurrentFont},argdefs=original_raster.__defaults__)
    plane=raster(arm,text,0x01FFCE40-BASE,size=(228,64),instruction_limit=2000000)
    assert plane==independent_font(arm,rom.read_file('/GRP/KANJI.FNT'),lines)
    rgb=image.convert('RGB')
    expected={(16+i%228,296+i//228) for i,p in enumerate(plane) if p==1}
    actual={(x,y) for y in range(294,366) for x in range(16,244) if rgb.getpixel((x,y))==(0,8,0)}
    assert expected==actual
    return {'message_id':row['message_id'],'actor_ID':row['actor_ID'],'visible_lines':lines,
        'original_actor_speech_dispatcher':0x02053FE4,'source_wrapper_parent':0x02054014,
        'resident_source_and_wrapped_buffers_exact_to_compiled_record':True,
        'all228x64_native_glyphs_and_actual_RGB_ink_and_blank_plane_pass':True,
        'independent_preexisting_text_origin':[16,296],'uniform_native_cell_origin_x6_each_row':True,
        'complete_leading_trailing_letters_words_and_popup_bounds':True}

def main():
    assert not (ROOT/'actual_gameplay_verification.json').exists()
    rom=NdsImage.open(ROM);arm=rom.read_file('/__arm9__.bin');digest=sha(ROM.read_bytes())
    assert digest==read(ROM.with_suffix('.manifest.json'))['candidate_sha256']
    rows={r['message_id']:r for r in read('translations/activity_special_editorial_manuscript_v2.json')['records']}
    entries=owned.current_entries(rom.read_file('/COMMON/MESFILE.DK4'),arm)
    holds=[];returns=[];receipts=[];fixtures=[];controls=[];images={}
    for label,(actor,n,activity,flag) in SPECS.items():
        modal=activity is None;terminal=18100 if modal else 16900
        folder=CAP/f'activity_special_v988_987_{label}';report,shots,receipt=load(folder,digest,terminal)
        receipts.append(receipt);images[label]=shots
        adapter=report['controlled_activity_special_adapter'];assert adapter['original_harness_file_unchanged']
        assert adapter['unchanged_harness_sha256']=='d5bcc9a11b5602bfb44d54e75b02a7a7a0165c9ee819a07cd0cbdac2130b8c6e'
        selected_fixtures=report['synthetic_activity_special_Cabin_assignment_fixtures'];assert len(selected_fixtures)==2
        data={f:(folder/f'frame_{f:06d}_arm9_ram.bin').read_bytes() for f in (15300,16100,16300,16500,16700,16900,terminal)}
        if modal:
            for f in (17100,17300,17500,17700):data[f]=(folder/f'frame_{f:06d}_arm9_ram.bin').read_bytes()
        for f in selected_fixtures:
            frame=f['frame'];request=label if f['phase']=='room' else {'case':label,'late_case_only':True}
            replay,expected=assign(arm,data[frame],request)
            assert f=={**expected,'frame':frame} and sha(replay)==f['after_RAM_sha256']
            assert f['actor_and_genuine_captain32_byte_records_unchanged'] and f['all_other4MiB_RAM_including_health_mood_battle_mode_money_and_native_text_code_exact']
        coordinates=report['synthetic_battle_recovery_proximity_fixtures'];assert len(coordinates)==2
        for f in coordinates:
            assert f['action']=='approach' and len(f['owned_bytes'])==8 and f['actual_battle_mode_not_assigned_by_fixture']
            assert f['no_enemy_stats_war_outcome_reward_inventory_or_resource_flags_changed'] and f['source_helpers_unchanged']
        assert not any(v for k,v in report.items() if k.startswith('synthetic_') and k not in ('synthetic_activity_special_Cabin_assignment_fixtures','synthetic_battle_recovery_proximity_fixtures'))
        assert read(ROOT/f'{label}_terminal_source_preservation.json')['source_and_disposable_donors_unchanged']
        assert read(ROOT/f'{label}_observed_original_combat.json')['native_combat_predicate_observed_before_any_personnel_fixture']
        row=rows[n];assert row['actor_ID']==actor and entries[n].text==compiled(row)
        pre_fixture_state=model_state(arm,data[16100])
        expected_fixture_RAM,_=assign(arm,data[16100],{'case':label,'late_case_only':True})
        before=model_state(arm,expected_fixture_RAM)
        if modal:
            cpu,get=get_machine(arm,data[16100]);source_model=get(0x82E04,get(0xCB1A8)+0x2090)
            for observed_frame in (16900,17100):
                source_bytes=data[16100][source_model-BASE:source_model-BASE+140]
                observed_bytes=data[observed_frame][source_model-BASE:source_model-BASE+140]
                assert [(i,a,b) for i,(a,b) in enumerate(zip(source_bytes,observed_bytes,strict=True)) if a!=b]==[(42,12,18)]
        else:assert before==pre_fixture_state
        frames=(16900,17100) if modal else (16300,16500)
        for frame in frames:
            raw=data[frame];cpu,get=get_machine(arm,raw);actors=get(0xCB184);obj=actors+4+actor*32
            assert get(0x7F244)==1 and get(0x7E100,obj)==0 and get(0x7E0B4,obj) in (1,2,3)
            assert model_state(arm,raw)==before
            if modal:
                case=modal_hold(rom,raw,shots[frame],row)
            else:
                case=hold(rom,raw,shots[frame],row,12)
                assert case['original_parent_activity_state']==activity and case['source_role_type']==2
                if flag is not None:assert get(0x4A224,get(0xCB190)+0x194)==flag
            case.update(case=label,frame=frame,RAM_sha256=sha(raw),actual_screen_sha256=sha((folder/f'frame_{frame:06d}_navigation.png').read_bytes()),
                display_fixtures_declared_no_earned_event_or_unlock=True)
            holds.append(case)
        after=model_state(arm,data[terminal])
        assert before['all31_original_occupant_bytes']==after['all31_original_occupant_bytes'] and before['funds']==after['funds']
        assert after['calendar_tick']>before['calendar_tick']
        assert rejected(lambda:actual_view(data[terminal]))
        returns.append({'case':label,'modal':modal,'return_frame':terminal,'all_scoped_state_equal_during_both_holds':True,
            'assignments_and_funds_preserved_on_return':True,'ordinary_battle_time_resumes':True,
            'no_active_Cabin_view_at_normal_sea_return':True,'state_before':before,'source_pre_late_fixture_state':pre_fixture_state,'state_after':after,'exact_declared_Chapel_type_byte42_12_to18_accounted_for':modal,
            'modal_native_Assign16700_A_dismiss17300_B_cancel17500_B_exit17900_no_extra_page':modal,
            'room_event_or_shared_item_bit_are_display_fixtures_not_earned_progression':True})
        fixtures.append({'case':label,'personnel_fixtures':selected_fixtures,'coordinate_fixtures':coordinates})
        raw=data[frames[0]];image=shots[frames[0]]
        if modal:
            wrapped=struct.unpack_from('<I',arm,0x54450)[0];bad=bytearray(raw);bad[wrapped-BASE+1]^=1
            controls.append({'case':label,'negative':'wrong-resident-leading-letter','rejected':rejected(lambda:modal_hold(rom,bytes(bad),image,row))})
            lines=visible_lines(row)
            for line,column,name in ((0,0,'erase-leading-letter'),(len(lines)-1,len(lines[-1])-1,'erase-final-punctuation')):
                bad_image=image.convert('RGB').copy();x,y=16+6+column*6,296+line*16
                bad_image.paste('white',(x,y,x+6,y+11))
                controls.append({'case':label,'negative':name,'rejected':rejected(lambda:modal_hold(rom,raw,bad_image,row))})
            bad_image=image.convert('RGB').copy();bad_image.paste((0,8,0),(16,296,17,297))
            controls.append({'case':label,'negative':'stray-left-margin-ink','rejected':rejected(lambda:modal_hold(rom,raw,bad_image,row))})
        else:
            view,parent,resource,h=actual_view(raw);bad=bytearray(raw);struct.pack_into('<I',bad,resource-BASE,(h[0]&0xFFFFFF00)|5)
            controls.append({'case':label,'negative':'wrong-native-image-format','rejected':rejected(lambda:actual_view(bytes(bad)))})
            lines=visible_lines(row);last=len(lines)-1
            interior=next((i for i,c in enumerate(lines[-1][1:-1],1) if c.isalpha()),None);assert interior is not None
            for line,column,name in ((0,0,'erase-leading-letter'),(last,len(lines[-1])-1,'erase-final-punctuation'),(last,interior,'erase-interior-word-letter')):
                bad=bytearray(raw);pixels=((resource+h[4])&0xFFFFFFFF)-BASE
                for y in range(60+line*12,71+line*12):
                    at=pixels+y*126+column*3;bad[at:at+3]=bytes(3)
                controls.append({'case':label,'negative':name,'rejected':rejected(lambda:hold(rom,bytes(bad),image,row,12))})
    assert len(holds)==18 and len(returns)==9 and len(controls)==36
    sheet=Image.new('RGB',(9*256,2*410),'#263238');draw=ImageDraw.Draw(sheet)
    for i,case in enumerate(holds):
        x,y=(i//2)*256,(i%2)*410;draw.text((x+4,y+4),f"{case['case']} ID{case['message_id']}",fill='white');sheet.paste(images[case['case']][case['frame']],(x,y+24))
    path=ROOT/'eighteen_complete_actual_holds.png';sheet.save(path)
    back=Image.new('RGB',(9*256,410),'#263238');draw=ImageDraw.Draw(back)
    for i,r in enumerate(returns):draw.text((i*256+4,4),r['case'],fill='white');back.paste(images[r['case']][r['return_frame']],(i*256,24))
    back_path=ROOT/'nine_normal_returns.png';back.save(back_path)
    save(ROOT/'actual_gameplay_verification.json',{'candidate':str(ROM),'candidate_sha256':digest,'terminal_capture_receipts':receipts,
        'actual_complete_dialogue_holds':holds,'scoped_normal_return_controls':returns,'fixture_receipts':fixtures,
        'offline_corruption_controls':controls,'all18_complete_native_and_actual_RGB_word_blank_planes_pass':True,
        'all3_Chapel_refusal_source_and_wrapped_buffers_complete_and_original_Assign_dismissal_return_pass':True,
        'post_event_activity2_Emilio36cell_and_Fernando_two_rows_and_special_Yifa36cell_Julian_retained_Aziza_both_bit_paths_pass':True,
        'original_consumer_scope':provenance(),'all_original_donors_and_harness_preserved':True,
        'review_sheet':str(path),'review_sheet_sha256':sha(path.read_bytes()),'return_review_sheet':str(back_path),
        'return_review_sheet_sha256':sha(back_path.read_bytes()),'visual_review_pending':True,
        'scope':'Nine separate V987 fresh cold boots:six embedded cases (activity2 Emilio1873/Fernando1876,battle personal Yifa1885/Julian1886/Aziza1887 and1888) and three distinct Chapel refusal popup cases Al1878/Yifa1879/Yukihisa1880. Each has two complete native/actual RGB holds and normal return. Actual original combat0/1 precedes declared room/UI event/selection fields;actor and captain32-byte records,health,mood and battle mode are never assigned. The two Aziza alternatives explicitly use a one-bit shared item-object fixture without inferring kinship or story meaning. Two coordinate approaches remain. No savestate,text/code injection,earned recruitment,unlock,event or assignment,full-route or hardware claim. Other8 entries have full source/native-font proof,not individual actual scene visits.',
        'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    print('18 complete native/actual RGB holds,nine returns and36 offline corruption controls pass;visual review pending.')

if __name__=='__main__':main()
