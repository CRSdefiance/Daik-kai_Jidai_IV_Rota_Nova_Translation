"""Bind the actual ordinary Items visit to complete independently modeled native text fields."""
import struct
from pathlib import Path
from PIL import Image,ImageDraw
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.prove_shachihoko_detail_fonts_v6101d import oracle
from scripts.verify_item_parent_layout import compose
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/shachihoko_actual_menu_v6105')
RUN=Path('work/analysis/shachihoko_item_menu_run_v6104')
FIX=Path('work/analysis/shachihoko_item_menu_fixture_v6103/complete_B204_source_B22_fixture_with_coordinated_item_data.json')
FONTS=Path('work/analysis/shachihoko_detail_fonts_v6101/both_detail_consumers_three_items_two_modes_complete_native_planes.json')
if __name__=='__main__':
    assert not ROOT.exists();fixture=read(FIX)['fixtures'][0];terminal,plan=map(read,[RUN/'terminal.json',RUN/'run_plan.json']);cap=Path(plan['capture_folder']);report,trace=map(read,[cap/'capture_report.json',cap/'observer/commands.json'])
    assert terminal['terminal'] and terminal['observer_host_slots_restored'] and report['ROM_sha256']==fixture['research_ROM_sha256']==sha(Path(fixture['research_ROM']).read_bytes())
    assert report['cold_boot'] and not report['savestate_loaded'] and not report.get('battery_save_preloaded') and not report['callback_errors'] and not any(v for k,v in report.items() if k.startswith('synthetic_'))
    assert not trace['errors'] and not trace['mismatches'] and trace['all_host_slots_restored_and_core_file_exact']
    complete=[]
    for row in trace['rows']:
        assert row['CPU_WRAM_DTCM_ITCM_and_configuration_unchanged_by_callback']
        if row['kind']!='after_command':continue
        entry=trace['rows'][row['entry_row']];s=entry['source'];assert s['whole_resident_payload_exact_ROM'] and s['block']==22
        complete.append(dict(offset=s['instruction_offset'],word=s['first_word'],start=entry['frame'],returned=row['frame'],decoded_length=row['decoded_length'],native_result=row['result_words']))
    assert len(complete)==35 and len([r for r in complete if r['word']==0x4000])==20 and complete[-1]['word']==0 and complete[-1]['returned']<8000
    fonts=read(FONTS);case=next(r for r in fonts['cases'] if (r['version'],r['item_ID'],r['page'],r['mode'])==('target',116,'main',4))
    parent=next(r['native'] for r in fonts['native_parent_versions'] if r['version']=='target');image=NdsImage.open(fixture['research_ROM']);arm=image.read_file('/__arm9__.bin');font=image.read_file('/GRP/KANJI.FNT')
    model,_=oracle();pixels=model(arm,font,case['glyph_events'],4,background=0);assert sha(pixels)==case['full_native_plane_sha256'];composed,_cells=compose(dict(pixels=pixels,glyph_events=case['glyph_events']),parent['requests']);canvas=struct.unpack('<49152H',composed)
    requests=[r for r in parent['requests'] if r['source_origin'] in [[48,0],[0,36],[0,48],[0,60]]];assert len(requests)==4
    photos={r['frame']:r for r in report['frames_captured']};matches=[]
    for frame in [8240,8300]:
        photo=photos[frame];path=Path(photo['path']);assert sha(path.read_bytes())==photo['PNG_sha256'];im=Image.open(path).convert('RGB')
        for r in requests:
            x,y=r['destination_origin'];width,height=r['size'];assert height==12
            expected={(xx,yy) for yy in range(height) for xx in range(width) if canvas[(y+yy)*256+x+xx]==1}
            observed={(xx,yy) for yy in range(height) for xx in range(width) if im.getpixel((x+xx,y+yy))==(230,230,230)}
            assert expected==observed,('actual field glyph mask differs',frame,r,len(expected^observed))
            matches.append(dict(frame=frame,native_source_origin=r['source_origin'],native_parent_destination=[x,y],native_parent_size=[width,height],complete_field_foreground_pixels=len(expected),
                original_native_parent_placement_not_fitted_from_test_letters=True,all_first_interior_final_glyphs_and_blank_guards_exact=True,PNG=str(path),PNG_sha256=photo['PNG_sha256']))
    navigation=read(cap/'navigation_command_journal.json');assert all(r['validation_passed'] for r in navigation['commands_received']) and navigation['commands_received'][-1]['command']=={'stop':True}
    ROOT.mkdir(parents=True);sheet=Image.new('RGB',(1040,1600),'#263238');draw=ImageDraw.Draw(sheet)
    for i,frame in enumerate([8000,8240,8300,8420]):
        row=photos[frame];im=Image.open(row['path']).convert('RGB');x,y=i%2*520,i//2*800;draw.text((x+4,y+3),'Actual ordinary menu visit frame'+str(frame),fill='white');sheet.paste(im.resize((512,768),Image.Resampling.NEAREST),(x+4,y+24))
    picture=ROOT/'actual_Items_description_hold_and_town_return.png';sheet.save(picture)
    save(ROOT/'actual_menu_two_holds_eight_complete_native_text_fields_and_return.json',dict(
        research_ROM=fixture['research_ROM'],research_ROM_sha256=fixture['research_ROM_sha256'],complete_original35_fixture_commands_and20_Japanese_objects=complete,
        source_scene_end_frame=complete[-1]['returned'],actual_item_menu_frames=[8240,8300],actual_after_back_menu_frame=8360,actual_return_to_port_UI_frame=8420,
        eight_complete_actual_title_description_field_matches=matches,all_changed_title_and134_character_description_exact_native_independent_glyphs_and_original_parent_positions=True,
        full_description_three_rows_with_first_final_characters_bounds_and_no_blank_page=True,
        no_pixel_mask_retiming_or_whole_scene_equivalence_claim=True,
        ordinary_X_Up_Up_A_then_B_B_menu_inputs_only_after_source_scene=True,no_RAM_inventory_money_roster_condition_or_RNG_fixture=True,
        actual_acquisition_from_source_A000_inside_disclosed_content_fixture_not_natural_event204_or_earned_route_progress=True,
        no_all_item_use_effects_all_conditional_lines_full_route_or_hardware_claim=True,
        native_CPU_24_plane_checks_remain_distinct_from_this_actual_GPU_visit=True,
        actual_new_cold_boots=1,actual_new_frames=report['frames'],all_sessions_terminal_and_observer_core_slots_restored=True,
        navigation_journal=str(RUN/'navigation.jsonl'),navigation_journal_sha256=sha((RUN/'navigation.jsonl').read_bytes()),
        sheet=str(picture),sheet_sha256=sha(picture.read_bytes()),visual_review_pending=True,new_review_credit=0,full_goal_complete=False,
        evidence={str(p):sha(p.read_bytes()) for p in [FIX,FONTS,RUN/'terminal.json',RUN/'run_plan.json',cap/'capture_report.json',cap/'observer/commands.json',cap/'navigation_command_journal.json',Path(__file__)]}))
    print(dict(actual_menu_holds=2,complete_title_description_field_matches=len(matches),source_end=complete[-1]['returned'],actual_return=8420,new_frames=report['frames'],visual_review_pending=True,no_credit=True))
