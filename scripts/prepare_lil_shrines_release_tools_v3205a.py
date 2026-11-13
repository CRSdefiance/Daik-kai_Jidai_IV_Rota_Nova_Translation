"""Prepare successors for cumulative release and fresh headless startup checks."""
import re
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import save

ROOT=Path('work/analysis/lil_Shrines_Temples_release_tools_v3205a')
def replace_all(text,changes):
    for value in changes:assert value in text,value
    return re.sub('|'.join(re.escape(k) for k in sorted(changes,key=len,reverse=True)),lambda m:changes[m.group()],text)

if __name__=='__main__':
    outputs=[
        (Path('scripts/verify_lil_crew_items_release_v3145.py'),Path('scripts/verify_lil_shrines_release_v3205.py')),
        (Path('scripts/run_lil_crew_items_startup_v3146.py'),Path('scripts/run_lil_shrines_startup_v3206.py')),
        (Path('scripts/verify_lil_crew_items_startup_v3147.py'),Path('scripts/verify_lil_shrines_startup_v3207.py'))]
    assert not ROOT.exists() and not any(n.exists() for o,n in outputs)
    old,new=outputs[0]
    text=replace_all(old.read_text(encoding='utf-8'),{
        'lil_crew_items_editorial':'lil_shrines_temples_editorial',
        'lil_Crew_Items_release_v3145':'lil_Shrines_Temples_release_v3205',
        'out/all_routes_combined_v3144_candidate.nds':'out/all_routes_combined_v3204_candidate.nds',
        'out/all_routes_combined_v3103_candidate.nds':'out/all_routes_combined_v3144_candidate.nds',
        'lil_Crew_Items_registration_v3143':'lil_Shrines_Temples_registration_v3203b',
        'all-routes-unified-v3144':'all-routes-unified-v3204',
        'all-routes-unified-v3103':'all-routes-unified-v3144',
        "[normal(conf['manuscript']),normal(conf['choices'])]":"[normal(conf['manuscript']),normal(conf['actor_styles']),normal(conf['choices'])]",
        '512':'515','exact_to_V3103':'exact_to_V3144'})
    new.write_text(text,encoding='utf-8')
    old,new=outputs[1]
    text=replace_all(old.read_text(encoding='utf-8'),{
        'lil_Crew_Items_runs_v3146':'lil_Shrines_Temples_runs_v3206',
        'lil_Crew_Items_v3146_':'lil_Shrines_Temples_v3206_',
        'version=3144':'version=3204',
        'Crew_Items':'Shrines_Temples',
        'Crew-Items':'Shrines-Temples'})
    new.write_text(text,encoding='utf-8')
    old,new=outputs[2]
    text=replace_all(old.read_text(encoding='utf-8'),{
        'lil_Crew_Items_startup_v3147':'lil_Shrines_Temples_startup_v3207',
        'lil_Crew_Items_runs_v3146':'lil_Shrines_Temples_runs_v3206',
        'out/all_routes_combined_v3144_candidate.nds':'out/all_routes_combined_v3204_candidate.nds',
        'out/all_routes_combined_v3103_candidate.nds':'out/all_routes_combined_v3144_candidate.nds',
        'work/analysis/lil_Recruits_Julian_runs_v3105':'work/analysis/lil_Crew_Items_runs_v3146',
        'V3103':'V3144','Current3144':'Current3204',
        'actual_selected_Crew_Items_IDs':'actual_selected_Shrines_Temples_IDs'})
    new.write_text(text,encoding='utf-8')
    for old,new in outputs:compile(new.read_text(encoding='utf-8'),str(new),'exec')
    ROOT.mkdir(parents=True)
    save(ROOT/'release_startup_successor_provenance.json',dict(
        previous={str(o):sha(o.read_bytes()) for o,n in outputs},
        successors={str(n):sha(n.read_bytes()) for o,n in outputs},
        exact_whole_clean_input_patch_and_fresh_current_coldboot_checks_required=True,
        no_prior_producer_ROM_capture_or_input_modified=True,
        producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
