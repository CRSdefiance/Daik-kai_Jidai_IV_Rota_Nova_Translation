"""Retain observed later sailing differences as a bounded test limitation."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
if __name__=='__main__':
    p=Path('work/analysis/lil_B201_later_differences_v5943b/unmodified_later_difference_inventory.json');d=read(p);out=p.parent/'all_broad_later_pairs_viewed.json';assert not out.exists()
    assert len(d['prompt_bounded_samples'])==7 and len(d['broad_later_samples'])==14 and len(d['whole_screen_sheets'])==3
    for s in d['whole_screen_sheets']:assert sha(Path(s['path']).read_bytes())==s['sha256']
    save(out,dict(inventory=str(p),inventory_sha256=sha(p.read_bytes()),all_three_sheets_viewed_after_return_at_original_detail=True,
        views=d['whole_screen_sheets'],review='Viewed every14 broad later source/English full-screen pair at identical frames. All are refusal-path later Sea View at12250..13001. The departure log remains readable in both;cloud/bird positions and later wind/readouts differ. Both progress to ordinary sailing without a stuck B201 text/menu. Seven other differences are confined to the advance-prompt bounds. No broad world,weather,calendar,actor,future RNG or pixel equivalence is claimed. Buy final queried groups/actor agree but PRNG differs;refusal queried models,persistent objects,calendar,actor and PRNG differ. State/tasks agree in both. These differences are retained,not masked,retimed or assigned a complete causal explanation. Following B120/SeaView prose gets no new editorial credit.',
        no_open_translation_specific_B201_display_menu_control_or_return_risk=True,later_simulation_differences_remain_explicit=True,no_new_emulator_runs_or_credit=True,evidence=d['evidence'],producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('All14 broad later sailing pairs viewed;seven prompt samples retained. No broad simulation-equivalence claim.')
