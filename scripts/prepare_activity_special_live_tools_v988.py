"""Prepare nine original-scene pilots with declared UI/room fields and no actor replacement."""
from pathlib import Path
from scripts.prepare_physical_fatigue_native_v961 import rendered
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import save

def main():
    root=Path('work/analysis/activity_special_v988');root.mkdir(parents=True,exist_ok=True)
    alias=Path('scripts/native_activity_special_room_v988.py');assert not alias.exists()
    items=[]
    for name in ('run_mood_comments_adapter_v982','native_mood_comments_standoff_v982','run_mood_comments_live_v982','navigate_mood_comments_v982'):
        source=Path('scripts')/(name+'.py');target=Path('scripts')/(name.replace('mood_comments','activity_special').replace('v982','v988')+'.py')
        assert not target.exists();raw=source.read_bytes();text=source.read_text(encoding='utf-8')
        text=text.replace('mood_comments_v982_975','activity_special_v988_987')
        text=text.replace('mood_comments','activity_special').replace('v982','v988').replace('v981','v987').replace('V982','V988').replace('V981','V987')
        text=text.replace('mood-comments','activity-special').replace('late_mood_only','late_case_only')
        text=text.replace('declared mood0/4/5','declared personnel UI event/selection fields').replace('late_mood0_4_5','late_personnel_UI_event_selection')
        import ast;ast.parse(text);items.append((source,target,raw,text))
    with alias.open('x',encoding='utf-8') as f:f.write('"""Case inventory alias;fixtures preserve actor identities."""\nfrom scripts.native_activity_special_fixture_v988 import CASES\n')
    rows=[]
    for source,target,raw,text in items:
        with target.open('x',encoding='utf-8') as f:f.write(text)
        assert source.read_bytes()==raw
        rows.append({'source':str(source),'source_sha256':sha(raw),'successor':str(target),'successor_sha256':sha(target.read_bytes()),'source_unchanged':True})
    save(root/'live_tools_provenance.json',{'files':rows,'fixture_source_sha256':sha(Path('scripts/native_activity_special_fixture_v988.py').read_bytes()),
        'all_successors_preflighted_before_output':True,'all_actual_scenes_still_pending':True,'producer_sha256':sha(Path(__file__).read_bytes())})
    print('Four historical live tools unchanged;nine declared personnel display pilots prepared.')

if __name__=='__main__':main()
