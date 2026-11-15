"""Readable bottom-screen QA sheets from completed cold boots; no guide captures."""
import argparse
from pathlib import Path
from PIL import Image,ImageDraw
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load,save

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--captures',type=Path,nargs='+',required=True)
    parser.add_argument('--out',type=Path,required=True)
    parser.add_argument('--first-frame',type=int,default=3120)
    args=parser.parse_args();assert not args.out.exists();args.out.mkdir(parents=True)
    runs=[]
    for folder in args.captures:
        report_path=folder/'capture_report.json';report=load(report_path)
        assert report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
        assert sha(Path(report['ROM']).read_bytes())==report['ROM_sha256']
        pictures=[]
        for filename in sorted(folder.glob('frame_*.png')):
            frame=int(filename.name.split('_')[1])
            if frame<args.first_frame:continue
            picture=Image.open(filename).convert('RGB');assert picture.size==(256,384)
            pictures.append((frame,filename,picture))
        sheets=[]
        for start in range(0,len(pictures),6):
            part=pictures[start:start+6]
            sheet=Image.new('RGB',(1024,((len(part)+1)//2)*410),'#263238');draw=ImageDraw.Draw(sheet)
            for index,(frame,filename,picture) in enumerate(part):
                x,y=index%2*512,index//2*410
                draw.text((x+3,y+3),f'{folder.name} frame{frame} bottom-screen QA',fill='white')
                sheet.paste(picture.crop((0,192,256,384)).resize((512,384),Image.Resampling.NEAREST),(x,y+22))
            target=args.out/(folder.name+f'_part{start//6+1}.png');sheet.save(target)
            sheets.append(dict(path=str(target),sha256=sha(target.read_bytes()),
                frames=[frame for frame,_,_ in part]))
        runs.append(dict(capture_report=str(report_path),capture_report_sha256=sha(report_path.read_bytes()),
            ROM=report['ROM'],ROM_sha256=report['ROM_sha256'],frames=report['frames'],
            selected_images=[dict(frame=frame,path=str(filename),sha256=sha(filename.read_bytes()))
                for frame,filename,_ in pictures],review_sheets=sheets,
            cold_boot=True,savestate=False,hardware_verification=False,
            disclosed_initialized_scene_ROM_fixture=True,natural_optional_activation=False))
    save(args.out/'capture_sheets.json',dict(runs=runs,
        lower_screen_crop_only_for_readable_sheet_full_original_captures_preserved=True,
        direct_review_pending=True,new_credit=0,producer_sha256=sha(Path(__file__).read_bytes())))
    print([(Path(r['capture_report']).parent.name,len(r['selected_images']),len(r['review_sheets'])) for r in runs])

if __name__=='__main__':
    main()
