"""Contact sheet of the actual original new presentation objects; no approval."""
from pathlib import Path
from PIL import Image,ImageDraw
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_London_control_sheet_v1890b')
NAV=Path('work/analysis/lil_London_context_navigation_v1888/original_presentation_observations_LIVE.json')

if __name__=='__main__':
    assert not ROOT.exists()
    observed=read(NAV)
    rows=[r for r in observed['rows'] if r['prefix_hex'] in ('97','fe','1c')]
    rows=[r for i,r in enumerate(rows) if r['prefix_hex']!='1c' or not any(x['prefix_hex']=='1c' for x in rows[:i])]
    assert len(rows)==4 and [r['prefix_hex'] for r in rows]==['fe','fe','fe','1c']
    sheet=Image.new('RGB',(3*256,2*410),'#263238')
    draw=ImageDraw.Draw(sheet)
    for i,r in enumerate(rows):
        h=r['holds'][1]
        assert sha(Path(h['capture']).read_bytes())==h['capture_sha256']
        im=Image.open(h['capture']).convert('RGB')
        x,y=i%3*256,i//3*410
        draw.text((x+3,y+3),r['id']+' / '+r['prefix_hex'],fill='white')
        sheet.paste(im,(x,y+22))
    ROOT.mkdir(parents=True)
    path=ROOT/'four_actual_new_presentation_objects.png'
    sheet.save(path)
    save(ROOT/'contact_sheet_provenance.json',dict(navigation=str(NAV),navigation_sha256=sha(NAV.read_bytes()),
        sheet=str(path),sheet_sha256=sha(path.read_bytes()),rows=rows,
        actual_old_prose_not_revised_glyph_approval=True,visual_review_pending=True,full_goal_complete=False))
    print(dict(sheet=str(path),objects=4))

