"""Prepare B182 source-owned roles, conditionals, UI and name proofs."""
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import save

ROOT=Path('work/analysis/lil_B182_contract_tools_v4879')
OLD='lil_B180_source_v4773/all11_clean_current_complete_context'
NEW='lil_B182_source_v4878/all8_clean_current_complete_context'

if __name__=='__main__':
    assert not ROOT.exists()
    tools=[]
    tools.append(derive('scripts/reconcile_lil_B180_voices_v4775.py','scripts/reconcile_lil_B182_voices_v4879.py',{
        OLD:NEW,'B180':'B182','voices_v4775':'voices_v4879',
        "old=read('work/analysis/lil_B180_voices_v4759/current2_static_names_voices_and207_catalog_rebind.json')":
        "old=read('work/analysis/lil_B181_voices_v4833/current207_catalog_eight_voices_and_three_source_selectors.json')",
        "for r in old['fresh2_actor_names']['rows']:":"for r in old['catalog']['rows']:\n        if r['actor_ID'] not in fresh:continue",
        'current V4766 RAM':'current V4867 RAM'}))
    tools.append(derive('scripts/prove_lil_B180_dispatches_v4776.py','scripts/prove_lil_B182_dispatches_v4880.py',{
        OLD:NEW,'B180':'B182','dispatches_v4776':'dispatches_v4880','voices_v4775':'voices_v4879',
        'len(cases)==22 and len(leaves)==7':'len(cases)==16 and len(leaves)==7',
        'all11_source_current_dispatches':'all8_source_current_dispatches','Bind22':'Bind16','22 source/current':'16 source/current'}))
    tools.append(derive('scripts/prove_lil_B180_branches_v4777.py','scripts/prove_lil_B182_branches_v4881.py',{
        OLD:NEW,'B180':'B182','branches_v4777':'branches_v4881'}))
    tools.append(derive('scripts/prove_lil_B180_entry_v4778.py','scripts/prove_lil_B182_entry_v4882.py',{
        OLD:NEW,'B180':'B182','entry_v4778':'entry_v4882','voices_v4775':'voices_v4879','in [180]':'in [182]'}))
    tools.append(derive('scripts/prove_lil_B180_predicate500_v4782.py','scripts/prove_lil_B182_predicate500_v4883.py',{
        OLD:NEW,'B180':'B182','predicate500_v4782':'predicate500_v4883','voices_v4775':'voices_v4879',
        'blocks[180]':'blocks[182]','[452,484]':'[512,544]',
        'prior_readonly_failure_and_diagnostic_preserved=True':'B180_predecessor_diagnostics_preserved_without_claiming_a_new_failure=True'}))
    tools.append(derive('scripts/prove_lil_B180_C200_v4784.py','scripts/prove_lil_B182_C200_v4883.py',{
        OLD:NEW,'B180':'B182','C200_v4784':'C200_v4883','voices_v4775':'voices_v4879','blocks[180]':'blocks[182]'}))
    tools.append(derive('scripts/prove_lil_B180_controls_v4780c.py','scripts/prove_lil_B182_controls_v4883.py',{
        OLD:NEW,'B180':'B182','controls_v4780c':'controls_v4883','voices_v4775':'voices_v4879',
        'branches_v4777':'branches_v4881','predicate500_v4782':'predicate500_v4883','C200_v4784':'C200_v4883',
        'blocks[180]':'blocks[182]','block=180':'block=182','len(commands)==28':'len(commands)==25',
        "(452,'0080fffff4010000'),(472,'00a0ffff013d0ba1'),(484,'0080fffff4010000'),\n        (504,'00a0ffff013b0ba1'),(516,'00a0ffff013c0ba1'),(570,'00c2'),(572,'00000000')":
        "(512,'0080fffff4010000'),(532,'00a0ffff014700a1'),(544,'0080fffff4010000'),\n        (564,'00a0ffff014800a1'),(576,'00a0ffff014600a1'),(630,'00c2'),(632,'00000000')",
        '[452,484]':'[512,544]',"p['source_end_offset']==572 and p['C200_offsets']==[570]":"p['source_end_offset']==632 and p['C200_offsets']==[630]",
        '{472,504,516}':'{532,564,576}','source_offset=570':'source_offset=630',
        'all11_speeches':'all8_speeches','source_declared_end_offsets=[572]':'source_declared_end_offsets=[632]'}))
    tools.append(derive('scripts/prove_lil_B180_names_v4779.py','scripts/prove_lil_B182_names_v4884.py',{
        OLD:NEW,'B180':'B182','names_v4779':'names_v4884','voices_v4775':'voices_v4879',
        'respectfully_referenced_third_person_has_no_bound_gender_name_rank_or_relation=True':
        'referenced_princess_duke_and_dukes_son_are_explicit_in_source_but_have_no_bound_personal_names=True'}))
    ROOT.mkdir(parents=True)
    save(ROOT/'prepared_contracts.json',dict(tools=tools,source_speeches=8,source_commands=25,
        source_relative_sites=10,source_predicates=2,source_effect_alternatives=3,
        static_selectors=[166,167],new_emulator_runs=0,new_review_credit=0,full_goal_complete=False))
    print('Prepared eight B182 native contract producers; no prose or gameplay approval.')
