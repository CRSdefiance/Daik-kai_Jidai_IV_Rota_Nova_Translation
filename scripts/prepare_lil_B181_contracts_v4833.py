"""Prepare exact-current B181 role,dispatch,entry and read-only name contracts."""
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import save

ROOT=Path('work/analysis/lil_B181_contract_tools_v4833')
OLD='lil_B180_source_v4773/all11_clean_current_complete_context'
NEW='lil_B181_source_v4832/all10_clean_current_complete_context'

if __name__=='__main__':
    assert not ROOT.exists()
    tools=[derive('scripts/reconcile_lil_B180_voices_v4775.py','scripts/reconcile_lil_B181_voices_v4833.py',{
        OLD:NEW,'B180':'B181','voices_v4775':'voices_v4833',
        'current207_catalog_eight_voices_and_two_source_selectors':'current207_catalog_eight_voices_and_three_source_selectors',
        "old=read('work/analysis/lil_B180_voices_v4759/current2_static_names_voices_and207_catalog_rebind.json')":
        "old=read('work/analysis/lil_B180_voices_v4775/current207_catalog_eight_voices_and_two_source_selectors.json')",
        'in [166,167]':'in [166,167,168]',
        "for r in old['fresh2_actor_names']['rows']:":"for r in old['catalog']['rows']:\n        if r['actor_ID'] not in fresh:continue",
        "{166:'Lady',167:'Lady'}":"{166:'Lady',167:'Lady',168:'Lady'}",
        'fresh2_actor_names':'fresh3_actor_names','prior_two_source_names':'prior_three_source_names',
        'two source selectors on current V4766 RAM':'three source selectors on current V4821 RAM',
        'Lady166/Lady167 selectors':'Lady166/Lady167/Lady168 selectors'}))]
    tools.append(derive('scripts/prove_lil_B180_dispatches_v4776.py','scripts/prove_lil_B181_dispatches_v4834.py',{
        OLD:NEW,'B180':'B181','dispatches_v4776':'dispatches_v4834','voices_v4775':'voices_v4833',
        'len(cases)==22 and len(leaves)==7':'len(cases)==20 and len(leaves)==3',
        'all11_source_current_dispatches_no_macros_and7_control_leaves':'all10_source_current_dispatches_no_macros_and3_control_leaves',
        'all7_nonrelative':'all3_nonrelative','all2_static_actors':'all3_static_actors',
        'Bind22 source/current speech calls and7':'Bind20 source/current speech calls and3',
        '22 source/current dispatches pass:two static actors':'20 source/current dispatches pass:three static actors',
        'All7 nonrelative leaves':'All3 nonrelative leaves'}))
    tools.append(derive('scripts/prove_lil_B180_entry_v4778.py','scripts/prove_lil_B181_entry_v4835.py',{
        OLD:NEW,'B180':'B181','entry_v4778':'entry_v4835','voices_v4775':'voices_v4833','in [180]':'in [181]'}))
    tools.append(derive('scripts/prove_lil_B180_names_v4779.py','scripts/prove_lil_B181_names_v4837.py',{
        OLD:NEW,'B180':'B181','names_v4779':'names_v4837','voices_v4775':'voices_v4833',
        'for ident in [166,167]:':'for ident in [166,167,168]:','for i in [166,167]':'for i in [166,167,168]',
        'native_four_consumer_cases':'native_six_consumer_cases','four_original_Lady_name_consumers':'six_original_Lady_name_consumers',
        "{'166':'Lady','167':'Lady'}":"{'166':'Lady','167':'Lady','168':'Lady'}",
        'all4MiB_preserved_by_four_readonly_getter_paths':'all4MiB_preserved_by_six_readonly_getter_paths',
        'respectfully_referenced_third_person_has_no_bound_gender_name_rank_or_relation=True':
        'referenced_wearer_is_source_explicit_lady_without_bound_name_rank_relation_or_gift_provenance=True',
        'Four source-owned':'Six source-owned','Four current Lady166/167':'Six current Lady166/167/168'}))
    ROOT.mkdir(parents=True);save(ROOT/'prepared_contracts.json',dict(tools=tools,source_speeches=10,source_commands=13,
        static_selectors=[166,167,168],FE_selector254_not_static_actor=True,new_emulator_runs=0,new_review_credit=0,full_goal_complete=False))
    print('Prepared B181 current role/dispatch/entry/name contracts;no new gameplay or credit.')
