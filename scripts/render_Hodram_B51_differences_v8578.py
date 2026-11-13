"""Render every nonidentical later RGB pair from the completed B51 captures."""
from pathlib import Path
from PIL import Image,ImageDraw
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/Hodram_B51_difference_view_v8578')
COMPARE=Path('work/analysis/Hodram_B51_comparison_v8577/paired_selected_path_comparison.json')
if __name__=='__main__':
    assert not ROOT.exists();proof=read(COMPARE);g=proof['groups'][0]
    differences=[r for r in g['later_RGB_comparisons'] if not r['whole_RGB_equal']]
    assert [r['frame'] for r in differences]==[4870,5650,5830]
    sheet=Image.new('RGB',(512*len(differences),410),'#263238');draw=ImageDraw.Draw(sheet)
    for i,row in enumerate(differences):
        for j,key in enumerate(['clean','revised']):
            ref=row[key];p=Path(ref['path']);assert sha(p.read_bytes())==ref['PNG_sha256']
            x=(i*2+j)*256;draw.text((x+3,3),key+' frame'+str(row['frame']),fill='white')
            pic=Image.open(p).convert('RGB');assert pic.size==(256,384);sheet.paste(pic,(x,24))
    ROOT.mkdir(parents=True);path=ROOT/'all_three_later_RGB_differences.png';sheet.save(path)
    save(ROOT/'sheet.json',dict(sheet=dict(path=str(path),sha256=sha(path.read_bytes())),all_nonidentical_later_pairs=differences,comparison=str(COMPARE),comparison_sha256=sha(COMPARE.read_bytes()),visual_review_pending=True,new_credit=0,full_goal_complete=False,producer_sha256=sha(Path(__file__).read_bytes())))
