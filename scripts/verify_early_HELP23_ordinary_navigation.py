"""Bind complete actual Help ink, all original child targets andnative continuation/history returns."""
import struct
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
from dk4tool.rom.nds import NdsImage
from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load,save

ROOT=Path('work/analysis/Shared_HELP_early23_formatting_20261104')
CAPTURE=ROOT/'ordinary_navigation_v1'
OUT=ROOT/'ordinary_navigation_checked_v1'
COLORS={(123,246,123),(213,214,213),(106,157,246)}

if __name__=='__main__':
    assert not OUT.exists()
    schedule_path=ROOT/'ordinary_navigation_plan_v1/navigation_plan.json';schedule=load(schedule_path)
    plan_path=ROOT/'automatic_plans_v1.json';plan=load(plan_path)
    qualification=load(ROOT/'preview_qualification_v1/qualification.json')
    report_path=CAPTURE/'capture_report.json';report=load(report_path)
    assert report['ROM_sha256']==qualification['research_ROM_sha256']
    assert report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
    assert report['frames']==schedule['terminal_frame'] and report['hardware_device_verification'] is False
    assert report['scripted_input_schedule']==load(ROOT/'ordinary_navigation_plan_v1/inputs.json')
    assert not report.get('fixture_mutations') and not report.get('battery_save')
    image=NdsImage.open(qualification['research_ROM']);arm=image.read_file('/__arm9__.bin');font=GameAsciiFont.from_arm9(arm)
    assert sha(Path(qualification['research_ROM']).read_bytes())==report['ROM_sha256']
    vtable=struct.unpack_from('<I',arm,0x7D40C)[0];child=struct.unpack_from('<I',arm,0x7D488)[0]
    frames={r['frame']:r for r in report['frames_captured']}
    snapshots={r['frame']:r for r in report['read_only_capture_RAM_snapshots']}
    for row in frames.values():assert sha(Path(row['path']).read_bytes())==row['PNG_sha256']
    for row in snapshots.values():assert sha(Path(row['path']).read_bytes())==row['sha256']
    cases=[];pictures=[]
    for page in plan['pages']:
        topic=page['topic_id'];frame=schedule['page_frames'][str(topic)];capture=frames[frame]
        picture=Image.open(capture['path']).convert('RGB');expected=set();glyphs=0
        for row,text in enumerate(page['visible_lines']):
            y=192 if row==0 else 216+(row-1)*16
            for col,char in enumerate(text):
                bitmap=font.decode(char);glyphs+=char!=' '
                expected.update((col*6+x,y+yy+1) for yy in range(11) for x in range(6) if bitmap.getpixel((x,yy)))
        actual={(x,y) for y in range(192,356) for x in range(252) if picture.getpixel((x,y)) in COLORS}
        assert actual==expected,(topic,frame,'missing',sorted(expected-actual)[:8],'extra',sorted(actual-expected)[:8])
        ram=Path(snapshots[frame]['path']).read_bytes();assert len(ram)==4194304
        parents=[]
        for offset in range(0,len(ram)-0x6B0,4):
            if struct.unpack_from('<I',ram,offset)[0]!=vtable:continue
            count,depth=[struct.unpack_from('<I',ram,offset+field)[0] for field in [0x660,0x6A8]]
            if depth>15 or count!=len(page['links']):continue
            history=struct.unpack_from('<16I',ram,offset+0x668)
            if history[depth]!=topic:continue
            targets=[]
            for n in range(count):
                at=offset+0xA0+n*0x5C
                assert struct.unpack_from('<I',ram,at)[0]==child
                targets.append(struct.unpack_from('<I',ram,at+8)[0])
            assert targets==[l['id'] for l in page['links']],(topic,targets)
            parents.append(dict(address=offset+0x02000000,history_depth=depth,history=list(history),constructed_link_targets=targets))
        assert len(parents)==1,(topic,parents)
        cases.append(dict(topic_id=topic,source_article_id=page['source_article_id'],frame=frame,capture=capture['path'],
            capture_sha256=capture['PNG_sha256'],RAM=snapshots[frame],actual_HELP_parent=parents[0],
            complete_visible_glyphs=glyphs,complete_expected_ink_pixels=len(expected),all_first_internal_final_glyphs_andblank_gaps_exact=True,
            full252x164_actual_text_mask_equals_current_independent_font_model=True,complete_ASCII_ink_offset_y=1))
        pictures.append((page,picture))
    returns=[]
    for pair in schedule['return_pairs']:
        a,b=[Image.open(frames[f]['path']).convert('RGB') for f in pair['frames']]
        assert a.crop((0,192,252,356)).tobytes()==b.crop((0,192,252,356)).tobytes(),pair
        returns.append({**pair,'complete_title_andbody_RGB_equal':True,'history_dependent_footer_excluded':True})
    assert len(cases)==25 and len({c['source_article_id'] for c in cases})==23
    OUT.mkdir();sheets=[];label=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',18)
    for first in range(0,len(pictures),4):
        group=pictures[first:first+4];sheet=Image.new('RGB',(1536,1080),'#263238');draw=ImageDraw.Draw(sheet)
        for i,(page,picture) in enumerate(group):
            x,y=(i%2)*768,(i//2)*540
            draw.text((x+6,y+4),f"Actual Help{page['source_article_id']} topic{page['topic_id']} p{page['page_number']}/{page['page_count']}",font=label,fill='white')
            sheet.paste(picture.crop((0,192,256,356)).resize((768,492),Image.Resampling.NEAREST),(x,y+30))
        path=OUT/('readable_actual_sheet_'+str(len(sheets)+1)+'.png');sheet.save(path)
        sheets.append(dict(path=str(path),sha256=sha(path.read_bytes()),pages=len(group)))
    save(OUT/'ordinary_gameplay_verification.json',dict(research_ROM=qualification['research_ROM'],research_ROM_sha256=report['ROM_sha256'],
        actual_pages=25,actual_articles=23,cold_boot_frames=report['frames'],all25_complete_actual_pages_andnative_child_targets_pass=True,
        all_source_preserved_links_andcontinuation_targets_constructed=True,original_forward_back_andL_R_history_returns=returns,
        actual_HELP_cases=cases,readable_actual_sheets=sheets,actual_ordinary_controls_no_state_injection=True,
        full_story_playthrough=False,hardware=False,guide_photos=False,new_credit=0,direct_actual_visual_review_pending=True,
        archive_load_andnative_widgets_observed=True,registered_release_pending=True,
        evidence={str(p):sha(p.read_bytes()) for p in [schedule_path,plan_path,report_path,ROOT/'preview_qualification_v1/qualification.json',Path(__file__)]}))
    print('All25 actual Help pages/23 articles:complete text masks/native child targets andthree continuation/history return pairs pass. Seven actual sheets await direct review.')
