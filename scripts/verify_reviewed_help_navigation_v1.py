"""Reusable complete current Help pixel/widget/return checks with explicit observed-versus-offline scope."""
import argparse,struct
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
from dk4tool.rom.nds import NdsImage
from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load,save

COLORS={(123,246,123),(213,214,213),(106,157,246)}
def main():
    parser=argparse.ArgumentParser(description=__doc__)
    for key in ['capture','navigation','plan','out']:parser.add_argument('--'+key,type=Path,required=True)
    args=parser.parse_args();assert not args.out.exists()
    report_path=args.capture/'capture_report.json';report,nav,plan=map(load,[report_path,args.navigation,args.plan])
    assert sha(args.plan.read_bytes())==nav['plan_sha256'] and report['ROM_sha256']==nav['research_ROM_sha256']
    assert report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors'] and not report.get('battery_save_preloaded')
    assert report['frames']==nav['terminal_frame'] and report['scripted_input_schedule']==load(args.navigation.parent/'inputs.json')
    assert not any(v for k,v in report.items() if k.startswith('synthetic_'))
    image=NdsImage.open(nav['research_ROM']);assert sha(Path(nav['research_ROM']).read_bytes())==report['ROM_sha256']
    arm=image.read_file('/__arm9__.bin');font=GameAsciiFont.from_arm9(arm)
    assert sha(image.read_file('/COMMON/HELP.DK4'))==plan['target_HELP_sha256']
    frames={r['frame']:r for r in report['frames_captured']};snapshots={r['frame']:r for r in report['read_only_capture_RAM_snapshots']}
    for r in frames.values():assert sha(Path(r['path']).read_bytes())==r['PNG_sha256']
    for r in snapshots.values():assert sha(Path(r['path']).read_bytes())==r['sha256']
    selected=[p for p in plan['pages'] if p['topic_id'] in nav['observed_reviewed_topics']]
    assert len(selected)==len(nav['observed_reviewed_topics'])
    vtable,child=[struct.unpack_from('<I',arm,a)[0] for a in [0x7D40C,0x7D488]]
    cases=[];pictures=[]
    for page in selected:
        t=page['topic_id'];frame=nav['page_frames'][str(t)];capture=frames[frame];picture=Image.open(capture['path']).convert('RGB');expected=set()
        for row,text in enumerate(page['visible_lines']):
            y=192 if row==0 else 216+(row-1)*16
            for col,char in enumerate(text):
                bitmap=font.decode(char);expected.update((col*6+x,y+yy+1) for yy in range(11) for x in range(6) if bitmap.getpixel((x,yy)))
        actual={(x,y) for y in range(192,356) for x in range(252) if picture.getpixel((x,y)) in COLORS}
        assert actual==expected,(t,frame,'missing',sorted(expected-actual)[:8],'extra',sorted(actual-expected)[:8])
        ram=Path(snapshots[frame]['path']).read_bytes();assert len(ram)==4194304;parents=[]
        for offset in range(0,len(ram)-0x6B0,4):
            if struct.unpack_from('<I',ram,offset)[0]!=vtable:continue
            count,depth=[struct.unpack_from('<I',ram,offset+f)[0] for f in [0x660,0x6A8]]
            if count!=len(page['links']) or depth>15:continue
            history=struct.unpack_from('<16I',ram,offset+0x668)
            if history[depth]!=t:continue
            targets=[]
            for n in range(count):
                a=offset+0xA0+n*0x5C;assert struct.unpack_from('<I',ram,a)[0]==child
                targets.append(struct.unpack_from('<I',ram,a+8)[0])
            assert targets==[r['id'] for r in page['links']]
            parents.append(dict(address=offset+0x02000000,history_depth=depth,history=list(history),constructed_link_targets=targets))
        assert len(parents)==1,(t,parents)
        cases.append(dict(topic_id=t,source_article_id=page['source_article_id'],frame=frame,capture=capture['path'],capture_sha256=capture['PNG_sha256'],
            RAM=snapshots[frame],actual_HELP_parent=parents[0],complete_ink_pixels=len(expected),
            all_first_internal_final_glyphs_andblank_gaps_exact=True,full252x164_actual_text_mask_equals_current_independent_font_model=True))
        pictures.append((page,picture))
    returns=[]
    for pair in nav['return_pairs']:
        a,b=[Image.open(frames[f]['path']).convert('RGB') for f in pair['frames']]
        assert a.crop((0,192,252,356)).tobytes()==b.crop((0,192,252,356)).tobytes(),pair
        returns.append({**pair,'complete_title_andbody_RGB_equal':True,'history_dependent_footer_excluded':True})
    args.out.mkdir();sheets=[];font_label=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',18)
    for first in range(0,len(pictures),4):
        group=pictures[first:first+4];sheet=Image.new('RGB',(1536,1080),'#263238');draw=ImageDraw.Draw(sheet)
        for i,(page,picture) in enumerate(group):
            x,y=(i%2)*768,(i//2)*540
            draw.text((x+6,y+4),f"Actual Help{page['source_article_id']} topic{page['topic_id']} p{page['page_number']}/{page['page_count']}",font=font_label,fill='white')
            sheet.paste(picture.crop((0,192,256,356)).resize((768,492),Image.Resampling.NEAREST),(x,y+30))
        path=args.out/('readable_actual_sheet_'+str(len(sheets)+1)+'.png');sheet.save(path);sheets.append(dict(path=str(path),sha256=sha(path.read_bytes()),pages=len(group)))
    all_articles={p['source_article_id'] for p in plan['pages']};observed_articles={p['source_article_id'] for p in selected}
    save(args.out/'ordinary_gameplay_verification.json',dict(research_ROM=nav['research_ROM'],research_ROM_sha256=report['ROM_sha256'],
        actual_pages=len(cases),actual_articles=len(observed_articles),offline_only_pages=len(plan['pages'])-len(cases),
        offline_only_article_IDs=sorted(all_articles-observed_articles),cold_boot_frames=report['frames'],
        all_selected_complete_actual_pages_andnative_child_targets_pass=True,actual_HELP_cases=cases,
        original_forward_back_andL_R_history_returns=returns,readable_actual_sheets=sheets,actual_ordinary_controls_no_state_injection=True,
        archive_load_andnative_widgets_observed=True,direct_actual_visual_review_pending=True,registered_release_pending=True,
        full_story_playthrough=False,hardware=False,guide_photos=False,new_credit=0,
        evidence={str(p):sha(p.read_bytes()) for p in [report_path,args.navigation,args.plan,Path(__file__)]}))
    print(dict(actual_complete_pages=len(cases),actual_articles=len(observed_articles),offline_only_pages=len(plan['pages'])-len(cases),return_pairs=len(returns),sheets=len(sheets),direct_visual_review_pending=True))

if __name__=='__main__':main()
