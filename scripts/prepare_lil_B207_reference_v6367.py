"""Prepare one-block reference plus current loader/census/end tools without changing native addresses."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B207_reference_tools_v6367')
if __name__=='__main__':
    assert not ROOT.exists();rows=[]
    rows.append(derive('scripts/create_lil_B205_reference_v6203.py','scripts/create_lil_B207_reference_v6367.py',{
      'B205':'B207','V6160':'V6327','research_v6203':'research_v6367',
      'from scripts.prepare_lil_B205_references_v6200 import PARENT,ROM,PLAN':"from scripts.research_lil_B207_relocation_v6365 import PARENT,PLAN\nROM=Path('out/lil_B207_reference_v6367_RESEARCH_ONLY.nds')",
      'stored_v6202':'stored_v6366','all17_final_stored_targets68_macro_cases_and_complete_planes':'all13_final_stored_targets52_alignment_cases_and_complete_planes',
      'verification_v6198':'verification_v6364','all17_final_targets':'all13_final_targets','==68':'==52','macro_alignment_cases=68':'macro_alignment_cases=52','==[205]':'==[207]'}))
    shared={'B205':'B207','from scripts.prepare_lil_B205_references_v6200 import':'from scripts.create_lil_B207_reference_v6367 import'}
    rows.append(derive('scripts/verify_lil_B205_loader_v6205.py','scripts/verify_lil_B207_loader_v6368.py',{**shared,'V6160':'V6327','loader_v6205':'loader_v6368','research_v6203':'research_v6367'}))
    rows.append(derive('scripts/verify_lil_B205_references_v6206.py','scripts/verify_lil_B207_references_v6369.py',{**shared,'reference_census_v6206':'reference_census_v6369','loader_v6205':'loader_v6368','[205]':'[207]','25-command':'15-command',"sum(len(r['mapped_commands'])for r in result)==25":"sum(len(r['mapped_commands'])for r in result)==15",'all25':'all15','native_commands_each=25':'native_commands_each=15'}))
    rows.append(derive('scripts/prove_lil_B205_ends_v6207.py','scripts/prove_lil_B207_ends_v6370.py',{**shared,'ends_v6207':'ends_v6370','n==205':'n==207'}))
    ROOT.mkdir(parents=True);save(ROOT/'source_locked_reference_loader_census_end_tools.json',dict(tools=rows,source_commands=15,source_speeches=13,source_choices_relative_FE_macros=0,all_native_addresses_and_ABI_guards_preserved=True,new_review_credit=0,full_goal_complete=False));print('B207 reference/loaders15-command census/guarded ends prepared with unchanged original native addresses.')
