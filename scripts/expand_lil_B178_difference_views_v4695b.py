"""Retain and expose both remaining measured postscene difference frames in full."""
from pathlib import Path
from PIL import Image,ImageDraw
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_B178_actual_review_v4695')
INPUT=ROOT/'paired_all115_samples25_commands13_planes_and_final_state_analysis.json'
OUTPUT=ROOT/'paired_all115_samples25_commands13_planes_expanded_fullscreens.json'
assert not OUTPUT.exists()
d=read(INPUT);differences=d['sampled_postscene_whole_RGB_differences_unmasked']
assert [(r['frame'],r['whole_frame_difference_bbox']) for r in differences]==[
    (6970,[224,360,240,371]),(7150,[224,360,240,371]),(7930,[224,360,240,376]),(8110,[224,360,240,376])]
frames=[7930,8110];sheet=Image.new('RGB',(1048,1600),'#263238');draw=ImageDraw.Draw(sheet)
for row,frame in enumerate(frames):
    found=next(r for r in differences if r['frame']==frame)
    for col,label in enumerate(['source','English']):
        p=found[label];path=Path(p['path']);assert sha(path.read_bytes())==p['PNG_sha256']
        x,y=col*524,row*800;draw.text((x+4,y+4),label+' / frame '+str(frame),fill='white')
        sheet.paste(Image.open(path).convert('RGB').resize((512,768),Image.Resampling.NEAREST),(x+4,y+24))
        d['evidence'][str(path)]=sha(path.read_bytes())
p=ROOT/'paired_screen_review4.png';assert not p.exists();sheet.save(p)
d['paired_full_screen_sheets'].append(dict(path=str(p),sha256=sha(p.read_bytes()),frames=frames,visual_review_pending=True))
d.update(previous_analysis=str(INPUT),previous_analysis_sha256=sha(INPUT.read_bytes()),
    expansion_producer_sha256=sha(Path(__file__).read_bytes()))
save(OUTPUT,d)
print('Prepared four full-screen comparison sheets;all four postscene difference frames exposed without retiming/masking.')
