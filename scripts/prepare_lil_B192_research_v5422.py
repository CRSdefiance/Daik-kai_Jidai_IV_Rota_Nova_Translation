"""Prepare measured linear B192 reference checks without conditional inheritance."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save

ROOT=Path('work/analysis/lil_B192_research_tools_v5422')
PARENT=Path('out/all_routes_combined_v5396_candidate.nds')
ROM=Path('out/lil_B192_reference_v5423_RESEARCH_ONLY.nds')
PLAN=Path('work/analysis/lil_B192_relocation_v5420/nested_source_relocation_research.json')

if __name__=='__main__':
    assert not ROOT.exists()
    shared={'B188':'B192','prepare_lil_B188_research_v5248':'prepare_lil_B192_research_v5422'}
    rows=[derive('scripts/create_lil_B188_reference_v5249.py','scripts/create_lil_B192_reference_v5423.py',{
        **shared,'research_v5249':'research_v5423','stored_v5247':'stored_v5421',
        'all11_final_stored_targets44':'all8_final_stored_targets32','all11_final_targets':'all8_final_targets',
        'editorial_handoff_verification_v5225':'editorial_handoff_verification_v5402',
        "stored['current_final_stored_macro_alignment_cases']==44":"stored['current_final_stored_macro_alignment_cases']==32",
        'current_final_stored_macro_alignment_cases=44':'current_final_stored_macro_alignment_cases=32','==[188]':'==[192]','V5219':'V5396'})]
    rows.append(derive('scripts/verify_lil_B188_loader_v5250.py','scripts/verify_lil_B192_loader_v5424.py',{
        **shared,'loader_v5250':'loader_v5424','research_v5249':'research_v5423',
        'work/analysis/lil_B187_loader_v5206/whole_SC2_and_B187_initial_entry_proof.json':'work/analysis/lil_B191_loader_v5382/whole_SC2_and_B191_initial_entry_proof.json','V5219':'V5396'}))
    rows.append(derive('scripts/verify_lil_B188_references_v5251.py','scripts/verify_lil_B192_references_v5425.py',{
        **shared,'reference_census_v5251':'reference_census_v5425','loader_v5250':'loader_v5424','[188]':'[192]',
        '14-command/no-relative-site':'11-command/no-relative-site',"sum(len(r['mapped_commands'])for r in result)==14":"sum(len(r['mapped_commands'])for r in result)==11",
        'all14':'all11','native_commands_each=14':'native_commands_each=11'}))
    rows.append(derive('scripts/prove_lil_B188_ends_v5252.py','scripts/prove_lil_B192_ends_v5426.py',{
        **shared,'ends_v5252':'ends_v5426','n==188':'n==192'}))
    rows.append(derive('scripts/prove_lil_B188_relocated_controls_v5253.py','scripts/prove_lil_B192_relocated_controls_v5427.py',{
        **shared,'relocated_controls_v5253':'relocated_controls_v5427','blocks[188]':'blocks[192]','block=188':'block=192',
        '00a0ffff01293ba1':'00a0ffff012116a1','len(dispatches)==11':'len(dispatches)==8',
        '[(0xA000,8,8),(0xC200,476,418),(0,478,420)]':'[(0xA000,8,8),(0xC200,396,370),(0,398,372)]',
        "len(spec['command_map'])==14":"len(spec['command_map'])==11",'all11_progressive_FE':'all8_progressive_FE','all10_progressive_static_actors1':'all7_progressive_static_actors1',
        'Bind11 relocated dispatches':'Bind8 relocated dispatches','11 relocated dispatches,10 progressive/one impersonal FE':'8 relocated dispatches,7 progressive/one impersonal FE'}))
    ROOT.mkdir(parents=True)
    save(ROOT/'prepared_tools.json',dict(tools=rows,parent=str(PARENT),research=str(ROM),plan=str(PLAN),
        source_stored_logical=[404,402],target_stored_logical=[376,376],source_tailzeros=2,target_tailzeros=0,
        commands=11,speeches=8,progressive=7,FE=1,relative_sites=0,predicates=0,A000_source8_target8=True,C200_source396_target370=True,end_source398_target372=True,
        parent_loader_reuse_requires_exact_whole_ROM_hash=True,new_emulator_runs=0,new_review_credit=0,full_goal_complete=False))
