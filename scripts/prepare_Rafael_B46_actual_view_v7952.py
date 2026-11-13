"""Make eight unique-page sheets; preserve all58 measured occurrences and four transition sheets."""
from pathlib import Path
from PIL import Image,ImageDraw
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/Rafael_B46_actual_view_v7952')
ACTUAL=Path('work/analysis/Rafael_B46_actual_v7948/four_runs24_unique_speeches58_occurrences_two_choices_actual_body_name_FE_return_audit.json')
MENU=Path('work/analysis/Rafael_B46_menu_actual_v7950c/four_actual_menus12_full_owned_backing_andhighlight_samples.json')
COMPARE=Path('work/analysis/Rafael_B46_actual_comparison_v7949/both_choices29_scene_pairs_full_measured_timing_RNG_components_RGB_limits.json')
if __name__=='__main__':
    assert not ROOT.exists();actual,menu,compare=map(read,[ACTUAL,MENU,COMPARE])
    assert not actual['unresolved'] and not menu['unresolved'];ROOT.mkdir(parents=True);sheets=[];refs=[]
    for version in ['clean_Japanese','English']:
        same=[g for g in actual['groups'] if g['version']==version];unique={}
        for g in same:
            for speech in g['speech_observations']:
                if speech['id'] not in unique:unique[speech['id']]=dict(choice=g['choice'],speech=speech)
        ordered=sorted(unique.values(),key=lambda r:r['speech']['source_record_index']);assert len(ordered)==24
        for start in range(0,24,6):
            sheet=Image.new('RGB',(1560,832),'#263238');draw=ImageDraw.Draw(sheet);ids=[]
            for i,item in enumerate(ordered[start:start+6]):
                s=item['speech'];hold=s['complete_body_holds'][-1];photo=Path(hold['capture']);assert sha(photo.read_bytes())==hold['sha256']
                x,y=i%3*520,i//3*416
                draw.text((x+4,y+3),f"{version} {item['choice']} {s['id']} frame{hold['frame']}",fill='white')
                sheet.paste(Image.open(photo).convert('RGB').crop((0,192,256,384)).resize((512,384),Image.Resampling.NEAREST),(x+4,y+24))
                ids.append(s['id']);refs.append(dict(version=version,choice=item['choice'],id=s['id'],capture=hold))
            path=ROOT/f'{version}_24_unique_pages_sheet{start//6+1:02d}.png';sheet.save(path)
            sheets.append(dict(kind='unique-complete-actual-pages',version=version,IDs=ids,path=str(path),sha256=sha(path.read_bytes())))
    for g in actual['groups']:
        t=g['transition_sheet'];assert sha(Path(t['path']).read_bytes())==t['sha256']
        sheets.append(dict(kind='full-actual-transitions',version=g['version'],choice=g['choice'],**t))
    for kind,s in [('actual-menu-owned-backing-andhighlights',menu['review_sheet']),
        ('unmasked-later-comparison',dict(path=compare['review_sheet'],sha256=compare['review_sheet_sha256']))]:
        assert sha(Path(s['path']).read_bytes())==s['sha256'];sheets.append(dict(kind=kind,**s))
    assert len(sheets)==14 and len(refs)==48
    save(ROOT/'48_unique_actual_panes14_review_sheets_58_occurrences_preserved.json',dict(
        actual_proof=str(ACTUAL),actual_proof_sha256=sha(ACTUAL.read_bytes()),sheets=sheets,unique_actual_page_references=refs,
        full_actual_occurrences=58,complete_holds=214,duplicate_occurrences_not_removed_from_actual_audit=True,
        two_additional_decline_only_IDs=['DK4_MES_B46_R0105','DK4_MES_B46_R0109'],
        visual_review_pending=True,new_credit=0,new_emulator_runs=0,
        evidence={str(p):sha(p.read_bytes()) for p in [ACTUAL,MENU,COMPARE,Path(__file__)]},full_goal_complete=False))
    print('Prepared14 sheets:48 unique source/English pages,four transitions,actual menus andunmasked later comparison. All58 actual occurrences remain audited.')
