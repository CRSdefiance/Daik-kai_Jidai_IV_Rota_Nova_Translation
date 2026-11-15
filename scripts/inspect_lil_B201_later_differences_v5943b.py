"""Expose every broad later framebuffer difference without masking or retiming."""
from pathlib import Path
from PIL import Image,ImageDraw
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B201_later_differences_v5943b')
INPUT=Path('work/analysis/lil_B201_actual_v5942/two_paths_all24_complete_panels_two_options_and_source_comparisons.json')
if __name__=='__main__':
    assert not ROOT.exists();d=read(INPUT);photos={}
    for v in d['versions']:photos[v['path'],v['case']]={r['frame']:r for r in read(v['capture_report'])['frames_captured']}
    prompt=[];broad=[]
    for diff in d['later_whole_RGB_differences']:
        x0,y0,x1,y1=diff['whole_RGB_bbox']
        (prompt if 224<=x0<x1<=240 and 360<=y0<y1<=376 else broad).append(diff)
    ROOT.mkdir(parents=True);sheets=[];evidence={str(INPUT):sha(INPUT.read_bytes()),str(Path(__file__)):sha(Path(__file__).read_bytes())}
    for start in range(0,len(broad),6):
        sheet=Image.new('RGB',(1536,820),'#263238');draw=ImageDraw.Draw(sheet)
        for i,r in enumerate(broad[start:start+6]):
            xx,yy=i%3*512,i//3*410
            for j,case in enumerate(['clean_Japanese','reviewed_English']):
                p=photos[r['path'],case][r['frame']];assert sha(Path(p['path']).read_bytes())==p['PNG_sha256'];evidence[p['path']]=p['PNG_sha256']
                draw.text((xx+256*j+3,yy+3),r['path']+' '+case+' '+str(r['frame']),fill='white');sheet.paste(Image.open(p['path']).convert('RGB'),(xx+256*j,yy+24))
        p=ROOT/f'every_broad_later_difference_sheet{start//6+1}.png';sheet.save(p);sheets.append(dict(path=str(p),sha256=sha(p.read_bytes())))
    save(ROOT/'unmodified_later_difference_inventory.json',dict(actual_proof=str(INPUT),actual_proof_sha256=sha(INPUT.read_bytes()),prompt_bounded_samples=prompt,broad_later_samples=broad,whole_screen_sheets=sheets,no_mask_retiming_or_pixel_edit=True,visual_review_pending=True,evidence=evidence,new_emulator_runs=0,new_review_credit=0,full_goal_complete=False))
    print(dict(prompt=len(prompt),broad=len(broad),sheets=len(sheets)))
