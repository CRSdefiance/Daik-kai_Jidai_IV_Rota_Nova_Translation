"""Prepare B181 reference gates while reusing only exact-current whole-ROM evidence."""
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import save

ROOT=Path('work/analysis/lil_B181_research_tools_v4851')
PARENT=Path('out/all_routes_combined_v4821_candidate.nds')
ROM=Path('out/lil_B181_reference_v4852_RESEARCH_ONLY.nds')
PLAN=Path('work/analysis/lil_B181_relocation_v4846/nested_source_relocation_research.json')

if __name__=='__main__':
    assert not ROOT.exists();tools=[]
    tools.append(derive('scripts/create_lil_B180_reference_v4801.py','scripts/create_lil_B181_reference_v4852.py',{
        'B180':'B181','prepare_lil_B180_research_v4800':'prepare_lil_B181_research_v4851',
        'research_v4801':'research_v4852','stored_v4799':'stored_v4847',
        'all11_final_stored_targets44_macro_cases':'all10_final_stored_targets40_macro_cases',
        'editorial_handoff_verification_v4797':'editorial_handoff_verification_v4850',
        "stored['all11_final_targets":"stored['all10_final_targets",
        "stored['current_final_stored_macro_alignment_cases']==44":"stored['current_final_stored_macro_alignment_cases']==40",
        '==[180]':'==[181]','all11_final_targets':'all10_final_targets','current_final_stored_macro_alignment_cases=44':'current_final_stored_macro_alignment_cases=40',
        'V4766':'V4821','source/RNG/control/gameplay':'source/control/gameplay'}))
    tools.append(derive('scripts/verify_lil_B179_loader_v4735.py','scripts/verify_lil_B181_loader_v4853.py',{
        'B179':'B181','prepare_lil_B179_research_v4733':'prepare_lil_B181_research_v4851','loader_v4735':'loader_v4853','research_v4734':'research_v4852',
        'work/analysis/lil_B178_loader_v4687/whole_SC2_and_B178_initial_entry_proof.json':
        'work/analysis/lil_B180_loader_v4802/whole_SC2_and_B180_initial_entry_proof.json','V4701':'V4821'}))
    tools.append(derive('scripts/verify_lil_B179_references_v4736.py','scripts/verify_lil_B181_references_v4854.py',{
        'B179':'B181','prepare_lil_B179_research_v4733':'prepare_lil_B181_research_v4851',
        'reference_census_v4736':'reference_census_v4854','loader_v4735':'loader_v4853','[179]':'[181]',
        '16-command/no-relative-site':'13-command/no-relative-site',
        "sum(len(r['mapped_commands'])for r in result)==16":"sum(len(r['mapped_commands'])for r in result)==13",
        'all16':'all13','native_commands_each=16':'native_commands_each=13'}))
    tools.append(derive('scripts/prove_lil_B179_ends_v4737.py','scripts/prove_lil_B181_ends_v4855.py',{
        'B179':'B181','prepare_lil_B179_research_v4733':'prepare_lil_B181_research_v4851','ends_v4737':'ends_v4855','n==179':'n==181'}))
    tools.append(derive('scripts/prove_lil_B178_relocated_controls_v4690.py','scripts/prove_lil_B181_relocated_controls_v4856.py',{
        'B178':'B181','relocated_controls_v4690':'relocated_controls_v4856','prepare_lil_B178_research_v4685':'prepare_lil_B181_research_v4851',
        'current_common_native_context_v2677':'current_build_native_context_v4774','prove_lil_B139_C200_v3461e':'prove_lil_B180_C200_v4784',
        'blocks[178]':'blocks[181]','block=178':'block=181','[1,0,13,0,0,0,1]':'[1,2,13,0,0,0,1]',
        '00a0ffff010002a1':'00a0ffff014913a1','len(dispatches)==13':'len(dispatches)==10',
        '[(0xA000,8,8),(0xC200,488,450),(0,490,452)]':'[(0xA000,8,8),(0xC200,390,374),(0,392,376)]',
        "len(spec['command_map'])==16":"len(spec['command_map'])==13",'all13':'all10','all12_progressive':'all9_progressive',
        'thirteen relocated dispatches':'ten relocated dispatches','Thirteen relocated dispatches,twelve progressive':'Ten relocated dispatches,nine progressive'}))
    ROOT.mkdir(parents=True);save(ROOT/'prepared_tools.json',dict(tools=tools,parent=str(PARENT),research=str(ROM),plan=str(PLAN),
        source_commands=13,speeches=10,current_loader_reuse_bound_by_whole_ROM_hash_to4802_research=True,
        target_whole_loader336_parent_modes672_and_three_entry_censuses_fresh=True,new_emulator_runs=0,new_review_credit=0,full_goal_complete=False))
    print('Prepared B181 research image,exact-current loader reuse,fresh target loader/census/end and relocated control gates.')
