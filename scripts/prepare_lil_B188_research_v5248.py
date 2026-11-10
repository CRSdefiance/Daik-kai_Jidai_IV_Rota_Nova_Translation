"""Prepare exact-parent reference checks for the measured424-byte B188 target."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B188_research_tools_v5248')
PARENT=Path('out/all_routes_combined_v5219_candidate.nds')
ROM=Path('out/lil_B188_reference_v5249_RESEARCH_ONLY.nds')
PLAN=Path('work/analysis/lil_B188_relocation_v5246/nested_source_relocation_research.json')
if __name__=='__main__':
    assert not ROOT.exists()
    shared={'B187':'B188','prepare_lil_B187_research_v5204':'prepare_lil_B188_research_v5248'}
    rows=[derive('scripts/create_lil_B187_reference_v5205.py','scripts/create_lil_B188_reference_v5249.py',{
        **shared,'research_v5205':'research_v5249','stored_v5203':'stored_v5247','all16_final_stored_targets64':'all11_final_stored_targets44','all16_final_targets':'all11_final_targets',
        'editorial_handoff_verification_v5183':'editorial_handoff_verification_v5225',"stored['current_final_stored_macro_alignment_cases']==64":"stored['current_final_stored_macro_alignment_cases']==44",
        'current_final_stored_macro_alignment_cases=64':'current_final_stored_macro_alignment_cases=44','==[187]':'==[188]','V5177':'V5219'} )]
    rows.append(derive('scripts/verify_lil_B187_loader_v5206.py','scripts/verify_lil_B188_loader_v5250.py',{
        **shared,'loader_v5206':'loader_v5250','research_v5205':'research_v5249',
        'work/analysis/lil_B186_loader_v5162/whole_SC2_and_B186_initial_entry_proof.json':'work/analysis/lil_B187_loader_v5206/whole_SC2_and_B187_initial_entry_proof.json','V5177':'V5219'}))
    rows.append(derive('scripts/verify_lil_B187_references_v5207.py','scripts/verify_lil_B188_references_v5251.py',{
        **shared,'reference_census_v5207':'reference_census_v5251','loader_v5206':'loader_v5250','[187]':'[188]',
        '19-command/no-relative-site':'14-command/no-relative-site',"sum(len(r['mapped_commands'])for r in result)==19":"sum(len(r['mapped_commands'])for r in result)==14",
        'all19':'all14','native_commands_each=19':'native_commands_each=14'}))
    rows.append(derive('scripts/prove_lil_B187_ends_v5208.py','scripts/prove_lil_B188_ends_v5252.py',{
        **shared,'ends_v5208':'ends_v5252','n==187':'n==188'}))
    rows.append(derive('scripts/prove_lil_B187_relocated_controls_v5209.py','scripts/prove_lil_B188_relocated_controls_v5253.py',{
        **shared,'relocated_controls_v5209':'relocated_controls_v5253','blocks[187]':'blocks[188]','block=187':'block=188',
        '00a0ffff014e2fa1':'00a0ffff01293ba1','len(dispatches)==16':'len(dispatches)==11',
        '[(0xA000,8,8),(0xC200,672,708),(0,674,710)]':'[(0xA000,8,8),(0xC200,476,418),(0,478,420)]',
        "len(spec['command_map'])==19":"len(spec['command_map'])==14",'all16_progressive_FE':'all11_progressive_FE','all15_progressive_static_actors1':'all10_progressive_static_actors1',
        'Bind16 relocated dispatches':'Bind11 relocated dispatches','16 relocated dispatches,15 progressive/one impersonal FE':'11 relocated dispatches,10 progressive/one impersonal FE'}))
    ROOT.mkdir(parents=True);save(ROOT/'prepared_tools.json',dict(tools=rows,parent=str(PARENT),research=str(ROM),plan=str(PLAN),
        source_stored_logical=[484,482],target_stored_logical=[424,424],source_tailzeros=2,target_tailzeros=0,
        commands=14,speeches=11,progressive=10,FE=1,relative_sites=0,predicates=0,A000_source8_target8=True,C200_source476_target418=True,end_source478_target420=True,
        parent_loader_reuse_requires_exact_whole_ROM_hash=True,new_emulator_runs=0,new_review_credit=0,full_goal_complete=False))
