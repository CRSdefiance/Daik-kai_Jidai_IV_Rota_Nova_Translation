"""Bind the31 English modal submissions to settled QA captures and exact FE geometry."""
import math
import struct
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load,save
from scripts.trace_file_ids_v683 import mapped_read

ROOT=Path('work/analysis/Hodram_B156_cinematic_English_actual_20261102')
FIXTURE=Path('work/analysis/Hodram_B156_cinematic_English_fixture_20261102/fixture.json')
TERMINAL=Path('work/analysis/Hodram_B156_cinematic_English_run_20261102/terminal.json')

if __name__=='__main__':
    assert not ROOT.exists();fixture,terminal=load(FIXTURE),load(TERMINAL)
    assert terminal['terminal'] and terminal['frames']==15001
    report_path=Path(terminal['report']);observer_path=Path(terminal['observer'])
    assert sha(report_path.read_bytes())==terminal['report_sha256'] and sha(observer_path.read_bytes())==terminal['observer_sha256']
    report,observer=load(report_path),load(observer_path)
    assert report['cold_boot'] and not report['savestate_loaded'] and not report.get('battery_save_preloaded') and not report['callback_errors']
    assert not observer['errors'] and not observer['mismatches'] and observer['all_host_slots_restored_and_core_file_exact']
    paints=[r for r in observer['rows'] if r['kind']=='modal_paint'];expected=[r for r in fixture['selected_target_commands'] if r['id'] is not None]
    captures=report['frames_captured'];rows=[];start=0
    for wanted in expected:
        hit=next(i for i in range(start,len(paints)) if paints[i]['text_hex']==wanted['expected_expanded_body_hex']);row=paints[hit];start=hit+1
        assert row['CPU_all4MiB_DTCM_ITCM_and_configuration_unchanged_by_callback']
        data={}
        for kind,ref in row['complete_readonly_snapshots'].items():
            raw=Path(ref['path']).read_bytes();assert len(raw)==ref['bytes'] and sha(raw)==ref['sha256'];data[kind]=raw
        read=lambda address,count:mapped_read(data['WRAM'],data['DTCM'],row['DTCM_base'],address,count)
        context=list(struct.unpack('<19I',read(row['context'],76)));view=list(struct.unpack('<25I',read(row['bitmap'],100)))
        font=list(struct.unpack('<6I',read(row['font_metrics_object'],24)))
        assert context[11]==row['bitmap']
        if wanted['source_selector']==254:
            assert context[1:6]==[0,0,228,48,1] and view[10:16]==[228,48,0,0,228,48] and font[1:3]==[6,12]
        end=paints[hit+1]['frame'] if hit+1<len(paints) else report['frames']
        candidates=[c for c in captures if row['frame']+60<=c['frame']<end]
        assert candidates,(wanted['id'],row['frame'],end)
        capture=candidates[0];assert sha(Path(capture['path']).read_bytes())==capture['PNG_sha256']
        rows.append(dict(id=wanted['id'],source_offset=wanted['source_offset'],stored_offset=wanted['stored_offset'],fixture_offset=wanted['fixture_offset'],
            selector=wanted['source_selector'],actual_paint_frame=row['frame'],actual_expanded_body_hex=row['text_hex'],
            exact_stored_English_andnative_macro_expansion_observed=True,context=context,view=view,font=font,capture=capture,
            FE_geometry_original_228x48_6x12_observed=wanted['source_selector']==254,
            modal_submission_not_new_characterization_of_all_progressive_consumers=True,
            actual_callback_readonly_snapshots=row['complete_readonly_snapshots'],visual_approval_pending=True))
    assert len(rows)==31 and sum(r['selector']==254 for r in rows)==23
    ROOT.mkdir(parents=True);sheets=[];font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',12)
    for at in range(0,len(rows),12):
        part=rows[at:at+12];sheet=Image.new('RGB',(768,math.ceil(len(part)/3)*216),'#eeeeee');draw=ImageDraw.Draw(sheet)
        for j,r in enumerate(part):
            x=j%3*256;y=j//3*216;pic=Image.open(r['capture']['path']).convert('RGB');assert pic.size==(256,384)
            sheet.paste(pic.crop((0,192,256,384)),(x,y+24));draw.text((x+3,y+2),r['id'].replace('DK4_MES_','')+' @'+str(r['capture']['frame']),fill='black',font=font)
        path=ROOT/f'English_actual_QA_{at//12+1:02d}.png';sheet.resize((sheet.width*2,sheet.height*2),Image.Resampling.NEAREST).save(path)
        sheets.append(dict(path=str(path),sha256=sha(path.read_bytes()),record_ids=[r['id'] for r in part]))
    save(ROOT/'observed_English_panels.json',dict(fixture=str(FIXTURE),fixture_sha256=sha(FIXTURE.read_bytes()),terminal=str(TERMINAL),
        report=str(report_path),report_sha256=sha(report_path.read_bytes()),observer=str(observer_path),observer_sha256=sha(observer_path.read_bytes()),
        actual_coldboot_frames=15001,English_speech_objects_observed=31,FE_panels_observed=23,selected_records=rows,review_sheets=sheets,
        all31_stored_English_bodies_andmacros_observed_in_original_sequence=True,all23_FE_geometries_match_qualified_source=True,
        later_opening_text_observed_after_fixture=True,later_opening_panels_not_additional_editorial_coverage=True,
        source_condition_wrapper_andother_dialogue_explicitly_excluded=True,natural_endgame_or_earned_plot_progress=False,
        catalogue_UI_city_ship_labels_Rafael0_andmenus_not_tested_by_this_run=True,guide_photos=False,new_credit=0,
        direct_visual_review_pending=True,producer_sha256=sha(Path(__file__).read_bytes())))
    print('Observed31 stored English bodies/all23 cinematic FE panels insequence;15001-frame coldboot,source geometry exact. Three QA sheets need direct review;no natural-ending orfull-route claim.')
