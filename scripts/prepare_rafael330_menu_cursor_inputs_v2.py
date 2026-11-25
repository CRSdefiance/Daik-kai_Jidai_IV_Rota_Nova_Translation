"""Move actual cursors through both menus with ordinary DOWN presses;keep the same fixture ROM."""
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load,save

ROOT=Path('work/analysis/Rafael330_actual_fixtures_20261105')
if __name__=='__main__':
    parent=ROOT/'B84_two_andthree_choice_fixture.json';out=ROOT/'B84_menu_cursor_fixture_v2.json';assert not out.exists()
    doc=deepcopy(load(parent));inputs=ROOT/'B84_menu_cursor_inputs_v2.json';values=load(Path(doc['inputs']))
    assert doc['frames']==10001
    values=[r for r in values if r['start']<5500]
    values+=[dict(start=f,duration=5,buttons=['DOWN']) for f in [4120,4500,4580]];values.sort(key=lambda r:r['start'])
    save(inputs,values)
    doc.update(frames=6001,inputs=str(inputs),inputs_sha256=sha(inputs.read_bytes()),
        original_fixture=str(parent),original_fixture_sha256=sha(parent.read_bytes()),
        only_three_ordinary_DOWN_presses_added_original_acceptance_times_unchanged=True,
        intended_cursor_states={3114:[0,1],5298:[0,1,2]},new_credit=0)
    save(out,doc);print('Prepared ordinary cursor DOWN/accept tests for two/three choices on the exact same research ROM;6001 frames.')
