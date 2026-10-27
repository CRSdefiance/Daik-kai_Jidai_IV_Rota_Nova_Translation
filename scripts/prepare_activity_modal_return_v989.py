"""Repeat only three modal cold boots to include the final command-menu Back."""
from pathlib import Path
from scripts.prepare_physical_fatigue_native_v961 import rendered
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import save

def main():
    root=Path('work/analysis/activity_special_v989');assert not root.exists();root.mkdir(parents=True)
    items=[]
    items.append(rendered('scripts/run_activity_special_live_v988.py','scripts/run_activity_special_live_v989.py',[
        ('activity_special_v988_987','activity_special_v989_987'),("ROOT=Path('work/analysis/activity_special_v988')","ROOT=Path('work/analysis/activity_special_v989')"),
        ("print('V988'","print('V989'")]))
    items.append(rendered('scripts/navigate_activity_special_v988.py','scripts/navigate_activity_special_v989.py',[
        ('activity_special_v988_987','activity_special_v989_987'),("ROOT=Path('work/analysis/activity_special_v988')","ROOT=Path('work/analysis/activity_special_v989')")]))
    items.append(rendered('scripts/navigate_activity_special_body_v988.py','scripts/navigate_activity_special_body_v989.py',[
        ("ROOT=Path('work/analysis/activity_special_v988')","ROOT=Path('work/analysis/activity_special_v989')")]))
    items.append(rendered('scripts/navigate_activity_special_modal_v988.py','scripts/navigate_activity_special_modal_v989.py',[
        ("ROOT=Path('work/analysis/activity_special_v988')","ROOT=Path('work/analysis/activity_special_v989')"),
        ("else:extra=[{'until':17900,'buttons':['B'],'duration':8},{'until':18100,'duration':1},{'stop':True}]",
         "else:extra=[{'until':17900,'buttons':['B'],'duration':8},{'until':18100,'duration':1},{'until':18300,'buttons':['B'],'duration':8},{'until':18500,'duration':1},{'stop':True}]")]))
    rows=[]
    for s,t,raw,text in items:
        with t.open('x',encoding='utf-8') as f:f.write(text)
        assert s.read_bytes()==raw
        rows.append({'source':str(s),'source_sha256':sha(raw),'successor':str(t),'successor_sha256':sha(t.read_bytes()),'source_unchanged':True})
    save(root/'modal_return_tools_provenance.json',{'files':rows,'same_V987_ROM_fixture_and_pre_popup_inputs':True,
        'reason':'V988 modal pilots pass full text and A dismissal,but18100 is the original command menu. Include one more native Back at18300 and observe actual sea return18500. The six body runs remain valid;no ROM change or reused savestate.',
        'producer_sha256':sha(Path(__file__).read_bytes())})
    print('Three fresh popup cold-boot repeats prepared;only final native command-menu Back added;historical tools/captures exact.')

if __name__=='__main__':main()
