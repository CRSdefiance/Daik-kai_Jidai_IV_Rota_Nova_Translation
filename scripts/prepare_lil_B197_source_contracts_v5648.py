"""Prepare source-owned actor, dispatch, event-entry, branch and name consumers."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B197_source_tools_v5648')
if __name__=='__main__':
    assert not ROOT.exists();shared={'B196':'B197','source_v5590':'source_v5647',
        'all36_clean_current_complete_context_with_twelve_choice_labels':'all24_clean_current_complete_context_with_three_choice_labels'}
    rows=[derive('scripts/reconcile_lil_B196_voices_v5591.py','scripts/reconcile_lil_B197_voices_v5648.py',{
        **shared,'voices_v5591':'voices_v5648','[2,6,19,20,25,173]':'[21,169]','len(fresh)==6':'len(fresh)==2',
        'fresh6_actor_names':'fresh2_actor_names','current207_catalog_eight_voices_and_six_source_selectors':'current207_catalog_eight_voices_and_two_source_selectors',
        'six B196 actors':'two B197 actors','V5580':'V5637'})]
    rows.append(derive('scripts/prove_lil_B196_dispatches_v5592.py','scripts/prove_lil_B197_dispatches_v5649.py',{
        **shared,'dispatches_v5592':'dispatches_v5649','voices_v5591':'voices_v5648',
        'Bind48 source/current speech calls and37 exact':'Bind42 source/current speech calls and11 exact',
        '0x2100]':'0x2200]','len(cases)==48':'len(cases)==42','len(leaves)==37':'len(leaves)==11',
        'all24_source_current_dispatches_FI1_and37_control_leaves':'all21_source_current_dispatches_no_macros_and11_control_leaves',
        'all37_nonrelative':'all11_nonrelative','all6_static_actors':'all2_static_actors',
        '48 source/current dispatches':'42 source/current dispatches','six static actors':'two static actors','FI1. All37':'no FI/FA/FO. All11'}))
    rows.append(derive('scripts/prove_lil_B196_entry_v5593.py','scripts/prove_lil_B197_entry_v5650.py',{
        **shared,'entry_v5593':'entry_v5650','voices_v5591':'voices_v5648','[196]':'[197]'}))
    rows.append(derive('scripts/prove_lil_B196_branches_v5595.py','scripts/prove_lil_B197_branches_v5651.py',{
        **shared,'branches_v5595':'branches_v5651','len(edges)==52':'len(edges)==6','len(cases)==520':'len(cases)==60'}))
    rows.append(derive('scripts/prove_lil_B196_names_v5594.py','scripts/prove_lil_B197_names_v5652.py',{
        **shared,'names_v5594':'names_v5652','voices_v5591':'voices_v5648',
        'current207_catalog_eight_voices_and_six_source_selectors':'current207_catalog_eight_voices_and_two_source_selectors',
        '[2,6,19,20,25,173]':'[21,169]','len(native[\'rows\'])==12':"len(native['rows'])==4",'fresh6_actor_names':'fresh2_actor_names',
        'source-six-name-consumers':'source-two-name-consumers','twelve_original_progressive_and_catalogue_name_consumers':'four_original_progressive_and_catalogue_name_consumers',
        'native_twelve_consumer_cases':'native_four_consumer_cases','Twelve source-owned':'Four source-owned'}))
    ROOT.mkdir(parents=True);save(ROOT/'prepared_source_tools.json',dict(tools=rows,objects=24,speeches=21,choice_labels=3,static_actors=2,FE=1,macros=0,
        commands=39,relative_sites=6,opaque_nonrelative_leaves=11,source_2200_selection_effects_4720_4735_and_cultural_prose_pending=True,
        new_emulator_runs=0,new_review_credit=0,full_goal_complete=False))
