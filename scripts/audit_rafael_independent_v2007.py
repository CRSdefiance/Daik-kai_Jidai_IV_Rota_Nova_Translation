"""Terminal ordinary opening/choice1: exact captures, glyph samples and return."""
from pathlib import Path
import struct
from PIL import Image,ImageDraw
from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/rafael_independent_actual_v2007')
CAP=Path('E:/Rota Nova translations/Generated/work/emulation_v193/rafael_opening_trace_v2003_RESEARCH_ONLY')
RUN=Path('work/analysis/rafael_opening_trace_v2003')
PLAN=Path('work/analysis/rafael_opening_relocation_v2001b/current_B44_typed_relocation_research.json')
FONT=Path('work/analysis/rafael_opening_fonts_v1998/all114_progressive_native_macros_and_complete_font_planes.json')

def ink(image,width,color,origin=(16,296),height=64):
    return {(x,y)for y in range(height)for x in range(width)if image.getpixel((origin[0]+x,origin[1]+y))==color}

if __name__=='__main__':
    assert not ROOT.exists()
    plan,font=map(read,(PLAN,FONT));report=read(CAP/'capture_report.json');observer=read(CAP/'observer/commands.json')
    terminal=read(RUN/'terminal.json');nav=read(CAP/'navigation_command_journal.json')
    assert terminal['terminal']and terminal['observer_host_slots_restored']
    assert report['ROM_sha256']==plan['research_ROM_sha256']==sha(Path(plan['research_ROM']).read_bytes())
    assert report['frames']==45690 and report['cold_boot']and not report['savestate_loaded']and not report['callback_errors']
    assert not report['hardware_device_verification']and not report['goal_complete']
    assert not any(value for key,value in report.items()if key.startswith('synthetic_'))
    assert 'battery_save_preloaded'not in report
    assert not observer['errors']and not observer['mismatches']and not observer['unreturned_at_capture_end']
    assert observer['all_host_slots_restored_and_core_file_exact']and observer['callbacks']==354
    assert nav['completion_confirmed']and all(r['validation_passed']for r in nav['commands_received'])
    initial=read('work/analysis/cliff_editorial_v829/ordinary_newgame_inputs.json');schedule=list(initial)
    for r in nav['commands_received']:
        command=r['command']
        assert set(command)<=set(('until','buttons','duration','stop'))
        if command.get('buttons'):schedule.append(dict(start=r['frame']+1,duration=command.get('duration',12),buttons=command['buttons']))
    assert report['scripted_input_schedule']==schedule
    images={};captures={}
    for row in report['frames_captured']:
        p=Path(row['path']);assert sha(p.read_bytes())==row['PNG_sha256']
        image=Image.open(p).convert('RGB');assert image.size==(256,384)
        if row['frame']in images:assert images[row['frame']].tobytes()==image.tobytes()
        images[row['frame']]=image;captures[row['frame']]=dict(path=str(p),sha256=row['PNG_sha256'])
    ram_rows=report['read_only_capture_RAM_snapshots']+report['read_only_pause_RAM_snapshots']+[report['read_only_RAM_snapshot']]
    for row in ram_rows:assert len(Path(row['path']).read_bytes())==4194304 and sha(Path(row['path']).read_bytes())==row['sha256']
    rows=observer['rows'];commands={r['new_offset']:r for r in plan['mapped_native_commands']}
    texts={r['new_command_offset']:r for r in plan['text_records']}
    fonts={r['id']:r for r in font['cases']};observations=[];executed=[];pairs=[];partial=[]
    for index,row in enumerate(rows):
        source=row['source']
        assert source['classification']=='original_SC_cache'and source['route']==0 and source['block']==44
        assert source['whole_resident_payload_exact_ROM']and source['actual_sha256']==plan['target_block_sha256']
        assert row['CPU_WRAM_DTCM_ITCM_and_configuration_unchanged_by_callback']
        if row['kind']!='after_command':continue
        before=rows[row['entry_row']];at=before['source']['instruction_offset'];expected=commands[at]
        # Conditional 0200/0300 lengths depend on the actual selection; the
        # structural walk deliberately uses a nonmatching previous-result.
        if expected['word']not in(0x200,0x300):assert row['decoded_length']==expected['new_native_extent']
        pairs.append(dict(offset=at,word=expected['word'],start_frame=before['frame'],return_frame=row['frame'],
            native_length=row['decoded_length'],result_words=row['result_words']))
        if expected['word']!=0x4000:continue
        text=texts[at];ident=text['id'];executed.append(ident)
        if text.get('unchanged_FE_separate_display_pending'):
            mask=Path('work/analysis/rafael_money_FE_v2005/physical_228x64_mask.bin').read_bytes()
            width=228;wanted={(x,y)for y in range(64)for x in range(width)if mask[y*width+x]}
        else:
            preview=Path(fonts[ident]['preview']);assert sha(preview.read_bytes())==fonts[ident]['preview_sha256']
            expected_image=Image.open(preview).convert('RGB');width=216;wanted=ink(expected_image,width,(0,8,0),(0,0))
        holds=[]
        for frame,image in sorted(images.items()):
            if not before['frame']<frame<row['frame']:continue
            actual=ink(image,width,(0,8,0))
            if actual==wanted:
                holds.append(dict(frame=frame,capture=captures[frame]['path'],capture_sha256=captures[frame]['sha256'],
                    complete_native_independent_actual_ink_equal=True))
            else:partial.append(dict(id=ident,frame=frame,missing_ink=len(wanted-actual),extra_ink=len(actual-wanted),
                sampled_before_complete_matching_hold_not_an_editorial_completion=True))
        observations.append(dict(id=ident,word=expected['word'],start_frame=before['frame'],return_frame=row['frame'],
            FE_separate_mode1=text.get('unchanged_FE_separate_display_pending',False),holds=holds))
    assert len(pairs)==177 and len(executed)==len(set(executed))==113
    assert set(text['id']for text in texts.values())-set(executed)=={'DK4_MES_B44_R0464','DK4_MES_B44_R0469'}
    last=next(r for r in observations if r['id']=='DK4_MES_B44_R0479')
    assert {45300,45330}<=set(h['frame']for h in last['holds'])
    money=next(r for r in observations if r['id']=='DK4_MES_B44_R0264');assert any(h['frame']==26160 for h in money['holds'])
    menu=next(r for r in pairs if r['word']==0x2100);assert menu['result_words']==[2,1]and menu['native_length']==32
    jump=next(r for r in pairs if r['offset']==6490);assert jump['native_length']==184 and jump['result_words']==[3,1]
    assert pairs[pairs.index(jump)+1]['offset']==6674
    assert pairs[-1]['offset']==6822 and pairs[-1]['result_words']==[0,1]
    image=NdsImage.open(plan['research_ROM']);arm=image.read_file('/__arm9__.bin');ascii_font=GameAsciiFont.from_arm9(arm)
    menu_holds=[]
    for frame in(44880,44940):
        for index,label,x in((0,'Ask him.',18),(1,'Prepare alone.',0)):
            wanted=set()
            for i,c in enumerate(label):
                glyph=ascii_font.decode(c)
                for y in range(11):
                    for xx in range(6):
                        if glyph.getpixel((xx,y)):wanted.add((x+i*6+xx,4+y))
            actual=ink(images[frame],84,(8,8,8),(86,268+20*index),20)
            assert actual==wanted
            menu_holds.append(dict(frame=frame,option_index=index,label=label,observed_menu_canvas_origin=[86,268+20*index],
                complete_first_last_internal_native_font_ink_and_blank_cells_equal=True,capture=captures[frame]))
    final=Path(report['read_only_RAM_snapshot']['path']).read_bytes();ev=image.read_file('/data/EV0.DK4')
    header=final.find(ev[:96]);assert header>=0 and final.find(ev[:96],header+1)<0
    owner=0x02000000+header-0x34;cpu,get=get_machine(arm,final)
    town=list(struct.unpack('<2I',cpu.mem_read(owner+0x2454,8)));assert town==[0,0]
    assert get(0x7F244)==get(0x2E58C)==0 and get(0x34674,get(0xCB1A8)+4)==0
    ROOT.mkdir(parents=True)
    selected=[]
    for ident in('DK4_MES_B44_R0053','DK4_MES_B44_R0091','DK4_MES_B44_R0140','DK4_MES_B44_R0210','DK4_MES_B44_R0316','DK4_MES_B44_R0327','DK4_MES_B44_R0398','DK4_MES_B44_R0479'):
        row=next(r for r in observations if r['id']==ident)
        if row['holds']:selected.append((ident,row['holds'][-1]['frame']))
    sheets=[]
    for start in range(0,len(selected),4):
        sheet=Image.new('RGB',(512,820),'#263238');draw=ImageDraw.Draw(sheet)
        for k,(ident,frame)in enumerate(selected[start:start+4]):
            x,y=256*(k%2),410*(k//2);draw.text((x+3,y+3),f'{ident} / {frame}',fill='white');sheet.paste(images[frame],(x,y+22))
        path=ROOT/f'representative_actual_{start//4+1:02d}.png';sheet.save(path);sheets.append(str(path))
    save(ROOT/'independent_preparation_and_normal_Lisbon_return.json',dict(research_ROM=plan['research_ROM'],research_ROM_sha256=plan['research_ROM_sha256'],
        plan=str(PLAN),plan_sha256=sha(PLAN.read_bytes()),capture_report=str(CAP/'capture_report.json'),capture_report_sha256=sha((CAP/'capture_report.json').read_bytes()),
        observer_report=str(CAP/'observer/commands.json'),observer_report_sha256=sha((CAP/'observer/commands.json').read_bytes()),
        all113_executed_speeches=executed,observed_speech_panels=observations,
        complete_matching_speech_panels=sum(bool(r['holds'])for r in observations),complete_matching_speech_holds=sum(len(r['holds'])for r in observations),
        other_samples_not_full_matching_holds=partial,all177_actual_command_pairs=pairs,choice_menu_actual_complete_label_holds=menu_holds,
        actual_choice1_result_2_1_and_repaired0300_jump_to6674=True,revised_R0479_two_holds_complete_native_actual_pixels=True,
        unchanged_FE_money_notice_actual_complete_native_mode1_ink=True,normal_Lisbon_town_ID=0,town_state=town,normal_docked_fleet_state=0,
        no_gameplay_save_state_location_RNG_funds_outcome_or_event_fixture=True,
        all_inputs_schedule_PNGs_RAM_hashes_callbacks_host_restoration_verified=True,
        actual_outer0100_skip_and_guided_choice0_still_pending=True,not_full_route_or_hardware_proof=True,
        representative_contact_sheets=sheets,visual_review_pending=True,
        producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print(dict(executed_speeches=113,matching_panels=sum(bool(r['holds'])for r in observations),matching_holds=sum(len(r['holds'])for r in observations),
        partial_samples=len(partial),actual_commands=177,choice=1,Lisbon_return=True))
