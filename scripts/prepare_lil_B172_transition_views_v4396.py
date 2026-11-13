"""Create paired full-screen views; record measured differences before review."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageChops
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_B172_transition_views_v4396')
ACTUAL=Path('work/analysis/lil_B172_actual_v4394/actual_all27_presentations_resources_C200_A000_and_end.json')
BASE=Path('E:/Rota Nova translations/Generated/work/emulation_v193')
if __name__=='__main__':
    assert not ROOT.exists()
    actual=read(ACTUAL)
    assert actual['fresh_actual_unique_speech_panels']==actual['complete_matching_observations']==27
    assert not actual['failures'] and not actual['paired_region_differences']
    versions=['clean_Japanese','reviewed_English']
    reports=[read(BASE/('lil_B172_display_v4390_'+c)/'capture_report.json') for c in versions]
    photos=[{p['frame']:p for p in r['frames_captured']} for r in reports]
    checks=[]
    for frame in sorted(photos[0]):
        pictures=[]
        for group in photos:
            p=group[frame]
            assert sha(Path(p['path']).read_bytes())==p['PNG_sha256']
            pictures.append(Image.open(p['path']).convert('RGB'))
        a,b=pictures
        bbox=ImageChops.difference(a.crop((0,0,256,294)),b.crop((0,0,256,294))).getbbox()
        checks.append(dict(frame=frame,upper_portrait_name_equal=bbox is None,nontext_difference_bbox=bbox,
            whole_RGB_equal=a.tobytes()==b.tobytes(),source=photos[0][frame],English=photos[1][frame]))
    assert next(c for c in checks if c['frame']==9370)['whole_RGB_equal']
    ROOT.mkdir(parents=True)
    sheets=[]
    selected=[3010,2950,6010,6610,6730,6790,9130,9370,14170,19990]
    for start in range(0,len(selected),3):
        frames=selected[start:start+3]
        sheet=Image.new('RGB',(len(frames)*520,824),'#263238');draw=ImageDraw.Draw(sheet)
        for column,frame in enumerate(frames):
            for row,case in enumerate(versions):
                p=photos[row][frame]
                draw.text((column*520+4,row*412+4),f'{case} frame{frame} original full screen',fill='white')
                sheet.paste(Image.open(p['path']).convert('RGB').resize((512,768),Image.Resampling.NEAREST).resize((256,384),Image.Resampling.NEAREST),(column*520+132,row*412+24))
        path=ROOT/f'paired_full_screen_sheet{start//3+1}.png'
        sheet.save(path)
        sheets.append(dict(path=str(path),sha256=sha(path.read_bytes()),frames=frames,viewed=False))
    save(ROOT/'paired_full_screen_and_region_inventory.json',dict(actual=str(ACTUAL),actual_sha256=sha(ACTUAL.read_bytes()),
        all_sampled_region_checks=checks,nontext_region_differences=[c for c in checks if not c['upper_portrait_name_equal']],
        paired_view_sheets=sheets,visual_review_pending=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print(dict(samples=len(checks),nontext_differences=sum(not c['upper_portrait_name_equal'] for c in checks),sheets=len(sheets),whole_RGB_town9370_equal=True))
