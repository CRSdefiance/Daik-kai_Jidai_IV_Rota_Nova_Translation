"""Show the complete observed R347 source page,English pages andfollowing original dialogue."""
from pathlib import Path
from PIL import Image,ImageDraw
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/Rafael_B48_actual_focus_v8055')
ACTUAL=Path('work/analysis/Rafael_B48_actual_v8053/paired_source_English_observed_path_complete_pages_names_andR347_transition.json')
if __name__=='__main__':
    assert not ROOT.exists();d=read(ACTUAL);assert not d['unresolved']
    source,english=[next(g for g in d['groups'] if g['version']==v) for v in ['clean_Japanese','English']]
    a=next(s for s in source['speech_observations'] if s['source_record_index']==347)
    b=next(s for s in english['speech_observations'] if s['source_record_index']==347)
    following=english['speech_observations'][english['speech_observations'].index(b)+1]
    assert a['native_page_count']==1 and b['native_page_count']==2 and len(b['ordinary_page_transitions'])==1
    entries=[('JP original R347',a['actual_complete_page_holds'][0][-1]),
        ('EN R347 page1',b['actual_complete_page_holds'][0][-1]),('EN R347 page2',b['actual_complete_page_holds'][1][0]),
        ('EN following R351',following['complete_body_holds'][0])]
    ROOT.mkdir(parents=True);sheet=Image.new('RGB',(1024,410),'#263238');draw=ImageDraw.Draw(sheet)
    for i,(label,h) in enumerate(entries):
        p=Path(h['capture']);assert sha(p.read_bytes())==h['sha256']
        draw.text((i*256+3,3),f"{label} frame{h['frame']}",fill='white');sheet.paste(Image.open(p).convert('RGB'),(i*256,24))
    path=ROOT/'R347_complete_source_English_two_pages_andfollowing_dialogue.png';sheet.save(path)
    save(ROOT/'focused_actual_page_turn_sheet.json',dict(actual_proof=str(ACTUAL),actual_proof_sha256=sha(ACTUAL.read_bytes()),
        entries=[dict(label=label,hold=h) for label,h in entries],ordinary_page_transition=b['ordinary_page_transitions'][0],
        sheet=str(path),sheet_sha256=sha(path.read_bytes()),visual_review_pending=True,
        R347_complete_masks_names_andfollowing_command_already_audited=True,no_new_emulator_run_orstate_change=True,new_credit=0,full_goal_complete=False))
    print(dict(sheet=str(path),page_turn=b['ordinary_page_transitions'][0]))
