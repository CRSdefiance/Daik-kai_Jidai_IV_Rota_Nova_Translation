"""Prepare B202's exact source dispatch,entry,branch and complete-scene fixture tools."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B202_contract_tools_v5963')
if __name__=='__main__':
    assert not ROOT.exists()
    rows=[derive('scripts/prove_lil_B200_dispatches_v5828.py','scripts/prove_lil_B202_dispatches_v5963.py',{
      'B200':'B202','dispatches_v5828':'dispatches_v5963','source_v5826':'source_v5959','voices_v5827':'voices_v5960',
      'len(leaves)==12':'len(leaves)==7',"sum(c['source_selector']==254 for c in cases)==4":"sum(c['source_selector']==254 for c in cases)==0",
      'all19_source_current_dispatches_no_macros_and12_control_leaves':'all19_source_current_dispatches_no_macros_and7_control_leaves',
      'all12_nonrelative':'all7_nonrelative','all2_static_actors':'all4_static_actors','two_distinct_FE_objects_use_original_null_actor_path':'no_FE_system_objects_or_null_actor_paths_in_source',
      '38 source/current dispatches pass:two static actors,two distinct FE/null-actor objects,no FI/FA/FO. All12 nonrelative leaves exact. No native display/gameplay/reviewcredit claim.':
      '38 source/current dispatches pass:four static actors,no FE or FI/FA/FO. All7 nonrelative leaves exact. No native display/gameplay/reviewcredit claim.'})]
    rows.append(derive('scripts/prove_lil_B200_entry_v5829.py','scripts/prove_lil_B202_entry_v5964.py',{
      'B200':'B202','entry_v5829':'entry_v5964','source_v5826':'source_v5959','voices_v5827':'voices_v5960','[200]':'[202]'}))
    rows.append(derive('scripts/prove_lil_B200_branches_v5830.py','scripts/prove_lil_B202_branches_v5965.py',{
      'B200':'B202','branches_v5830':'branches_v5965','source_v5826':'source_v5959'}))
    rows.append(derive('scripts/research_lil_B200_source_fixture_v5835.py','scripts/research_lil_B202_source_fixture_v5967.py',{
      'B200':'B202','fixture_v5835':'fixture_v5967','source_v5835':'source_v5967','source_v5826':'source_v5959',
      'blocks[200]':'blocks[202]','source_block=200':'source_block=202','len(jp)==932 and end==930':'len(jp)==588 and end==586',
      'len(commands)==40':'len(commands)==35','all40_stored_fixture_commands':'all35_stored_fixture_commands',
      'all31_source_commands_plus9_original_initializers_stored':'all26_source_commands_plus9_original_initializers_stored',
      'source_event200_not_naturally_activated':'source_event202_not_naturally_activated','collapse/inn-recovery/thanks-and-Charm':'unsolicited-book-handoff/pursuit/glassmaking-title',
      '31 original+9 initializer commands,19 speeches,no predicates':'26 original+9 initializer commands,19 speeches,no predicates'}))
    rows.append(derive('scripts/run_lil_B200_source_fixture_v5836.py','scripts/run_lil_B202_source_fixture_v5968.py',{
      'B200':'B202','fixture_v5835':'fixture_v5967','run_v5836':'run_v5968','source_v5836':'source_v5968',
      "selected['source_block']==200":"selected['source_block']==202",'source_event200_not_naturally_selected':'source_event202_not_naturally_selected',
      "'displayed_original_source_block':200":"'displayed_original_source_block':202",'all31_source_commands_retained':'all26_source_commands_retained'}))
    ROOT.mkdir(parents=True);save(ROOT/'source_locked_tools.json',dict(tools=rows,no_new_prose_or_controls_inherited=True,no_ROM_registry_ledger_orcompletion_credit_change=True,full_goal_complete=False))
    print('B20238 dispatches/seven leaves,original entry,no-relative-site checks and complete35-command source fixture/run tools prepared.')
