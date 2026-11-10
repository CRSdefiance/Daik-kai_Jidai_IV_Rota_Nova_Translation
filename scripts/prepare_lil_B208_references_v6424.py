"""Prepare one-block B208 reference and original whole-loader/entry/end consumers."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B208_reference_tools_v6424')
if __name__=='__main__':
    assert not ROOT.exists();rows=[]
    rows.append(derive('scripts/create_lil_B207_reference_v6367.py','scripts/create_lil_B208_reference_v6424.py',{
        'B207':'B208','V6327':'V6380','research_lil_B207_relocation_v6365':'research_lil_B208_relocation_v6422b','reference_v6367':'reference_v6424','research_v6367':'research_v6424',
        'stored_v6366':'stored_v6423b','all13_final_stored_targets52_alignment_cases_and_complete_planes':'all24_final_stored_targets96_macro_cases_and_complete_planes','verification_v6364':'verification_v6404','all13_final_targets':'all24_final_targets','==52':'==96','macro_alignment_cases=52':'macro_alignment_cases=96','==[207]':'==[208]'}))
    shared={'B207':'B208','create_lil_B207_reference_v6367':'create_lil_B208_reference_v6424'}
    rows.append(derive('scripts/verify_lil_B207_loader_v6368.py','scripts/verify_lil_B208_loader_v6425.py',{**shared,'V6327':'V6380','loader_v6368':'loader_v6425','research_v6367':'research_v6424'}))
    rows.append(derive('scripts/verify_lil_B207_references_v6369.py','scripts/verify_lil_B208_references_v6426.py',{**shared,'reference_census_v6369':'reference_census_v6426','loader_v6368':'loader_v6425','[207]':'[208]','15-command':'29-command',"sum(len(r['mapped_commands'])for r in result)==15":"sum(len(r['mapped_commands'])for r in result)==29",'all15':'all29','native_commands_each=15':'native_commands_each=29'}))
    rows.append(derive('scripts/prove_lil_B207_ends_v6370.py','scripts/prove_lil_B208_ends_v6427.py',{**shared,'ends_v6370':'ends_v6427','n==207':'n==208'}))
    ROOT.mkdir(parents=True);save(ROOT/'source_locked_reference_loader_census_end_tools.json',dict(tools=rows,source_commands=29,source_panels=24,source_progressive=23,source_FE=1,source_choices_relative_macros=0,all_native_addresses_and_ABI_guards_preserved=True,new_review_credit=0,full_goal_complete=False));print('B208 reference/whole loaders/29-command entry census/guarded ends prepared;all native addresses unchanged.')
