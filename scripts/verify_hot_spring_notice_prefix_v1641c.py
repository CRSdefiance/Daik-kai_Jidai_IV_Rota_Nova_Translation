"""Read-only whole-frame equivalence for the complete old13600-frame prefix."""
from pathlib import Path
from PIL import Image
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/hot_spring_notice_prefix_v1641c')
OLD=Path('E:/Rota Nova translations/Generated/work/emulation_v193/hot_spring_live_v1626_1622')
NEW=Path('E:/Rota Nova translations/Generated/work/emulation_v193/hot_spring_notice_live_v1641_1637')
if __name__=='__main__':
    assert not ROOT.exists()
    report=read(OLD/'capture_report.json');plan=read('work/analysis/hot_spring_notice_live_v1641/run_plan.json')
    assert report['frames']==13600 and report['ROM_sha256']=='cb049635c45b6bc75add4ada18db69ae2ece4aa05b9270a3553ed9ed74a228e4'
    assert plan['candidate_sha256']==sha(Path(plan['candidate']).read_bytes())=='0d81ee2668d2ff535432e2a50a5df44b9c1a4b0f683fca407f5753348038e7b2'
    pairs=[]
    for row in report['frames_captured']:
        old=Path(row['path']);new=NEW/old.name;assert sha(old.read_bytes())==row['PNG_sha256']
        with Image.open(old) as a,Image.open(new) as b:assert a.convert('RGB').tobytes()==b.convert('RGB').tobytes(),row['frame']
        pairs.append({'frame':row['frame'],'prior':str(old),'prior_sha256':row['PNG_sha256'],'current':str(new),'current_sha256':sha(new.read_bytes()),'whole256x384_RGB_exact':True})
    ROOT.mkdir(parents=True);save(ROOT/'all_original_prefix_frames_RGB_exact.json',{'candidate':plan['candidate'],'candidate_sha256':plan['candidate_sha256'],
        'prior_report_sha256':sha((OLD/'capture_report.json').read_bytes()),'frames':pairs,'prefix_through13600_including_discovery_recovery_returns_and_rats_exact':True,
        'new_optional_notice310_was_not_activated_in_this_prefix':True,'current_run_still_live_no_terminal_or_completion_claim':True,
        'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    print(len(pairs),'whole captured frames through13600 match V1622 exactly;notice310/optional relaxation still pending;current run remains live.')
