"""Prepare exact clean-patch and fresh current cold-boot successors."""
import re
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import save

ROOT=Path('work/analysis/lil_B111_B119_release_tools_v3252')
def replace_all(text,changes):
    for value in changes:assert value in text,value
    return re.sub('|'.join(re.escape(k) for k in sorted(changes,key=len,reverse=True)),lambda m:changes[m.group()],text)

if __name__=='__main__':
    outputs=[(Path('scripts/verify_lil_shrines_release_v3205.py'),Path('scripts/verify_lil_B111_B119_release_v3252b.py')),(Path('scripts/run_lil_shrines_startup_v3206.py'),Path('scripts/run_lil_B111_B119_startup_v3253.py')),(Path('scripts/verify_lil_shrines_startup_v3207.py'),Path('scripts/verify_lil_B111_B119_startup_v3254.py'))]
    assert not ROOT.exists() and not any(n.exists() for o,n in outputs)
    old,new=outputs[0]
    t=replace_all(old.read_text(encoding='utf-8'),{
        'lil_shrines_temples_editorial':'lil_B111_B119_editorial',
        'lil_Shrines_Temples_release_v3205':'lil_B111_B119_release_v3252b',
        'out/all_routes_combined_v3204_candidate.nds':'out/all_routes_combined_v3251_candidate.nds',
        'out/all_routes_combined_v3144_candidate.nds':'out/all_routes_combined_v3204_candidate.nds',
        'lil_Shrines_Temples_registration_v3203b':'lil_B111_B119_registration_v3250',
        'all-routes-unified-v3204':'all-routes-unified-v3251',
        'all-routes-unified-v3144':'all-routes-unified-v3204',
        "[normal(conf['manuscript']),normal(conf['actor_styles']),normal(conf['choices'])]":"[normal(conf['manuscript']),normal(conf['actor_styles'])]",
        '515':'517','exact_to_V3144':'exact_to_V3204'})
    new.write_text(t,encoding='utf-8')
    old,new=outputs[1]
    t=replace_all(old.read_text(encoding='utf-8'),{'lil_Shrines_Temples_runs_v3206':'lil_B111_B119_runs_v3253','lil_Shrines_Temples_v3206_':'lil_B111_B119_v3253_','version=3204':'version=3251','not_a_selected_Shrines_Temples_activation':'not_a_selected_B111_B119_activation','selectedShrines-Temples':'selectedB111-B119'})
    new.write_text(t,encoding='utf-8')
    old,new=outputs[2]
    t=replace_all(old.read_text(encoding='utf-8'),{'lil_Shrines_Temples_startup_v3207':'lil_B111_B119_startup_v3254','lil_Shrines_Temples_runs_v3206':'lil_B111_B119_runs_v3253','out/all_routes_combined_v3204_candidate.nds':'out/all_routes_combined_v3251_candidate.nds','out/all_routes_combined_v3144_candidate.nds':'out/all_routes_combined_v3204_candidate.nds','work/analysis/lil_Crew_Items_runs_v3146':'work/analysis/lil_Shrines_Temples_runs_v3206','V3144':'V3204','Current3204':'Current3251','actual_selected_Shrines_Temples_IDs':'actual_selected_B111_B119_IDs','match3103':'matchV3204'})
    new.write_text(t,encoding='utf-8')
    for o,n in outputs:compile(n.read_text(encoding='utf-8'),str(n),'exec')
    ROOT.mkdir(parents=True)
    save(ROOT/'release_startup_successor_provenance.json',dict(previous={str(o):sha(o.read_bytes()) for o,n in outputs},successors={str(n):sha(n.read_bytes()) for o,n in outputs},exact_whole_clean_input_patch_and_fresh_current_coldboot_checks_required=True,no_prior_producer_ROM_capture_or_input_modified=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
