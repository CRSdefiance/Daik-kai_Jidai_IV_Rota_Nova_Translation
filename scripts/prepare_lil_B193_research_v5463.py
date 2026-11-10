"""Prepare exact-parent one-block research for measured676-byte cooking target."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B193_research_tools_v5463')
PARENT=Path('out/all_routes_combined_v5437_candidate.nds')
ROM=Path('out/lil_B193_reference_v5464_RESEARCH_ONLY.nds')
PLAN=Path('work/analysis/lil_B193_relocation_v5461/nested_source_relocation_research.json')
if __name__=='__main__':
    assert not ROOT.exists()
    shared={'B192':'B193','prepare_lil_B192_research_v5422':'prepare_lil_B193_research_v5463'}
    rows=[derive('scripts/create_lil_B192_reference_v5423.py','scripts/create_lil_B193_reference_v5464.py',{
        **shared,'research_v5423':'research_v5464','stored_v5421':'stored_v5462','all8_final_stored_targets32':'all15_final_stored_targets60','all8_final_targets':'all15_final_targets',
        'verification_v5402':'verification_v5443',"stored['current_final_stored_macro_alignment_cases']==32":"stored['current_final_stored_macro_alignment_cases']==60",
        'current_final_stored_macro_alignment_cases=32':'current_final_stored_macro_alignment_cases=60','==[192]':'==[193]','V5396':'V5437'})]
    rows.append(derive('scripts/verify_lil_B192_loader_v5424.py','scripts/verify_lil_B193_loader_v5465.py',{
        **shared,'loader_v5424':'loader_v5465','research_v5423':'research_v5464','work/analysis/lil_B191_loader_v5382/whole_SC2_and_B191_initial_entry_proof.json':
        'work/analysis/lil_B192_loader_v5424/whole_SC2_and_B192_initial_entry_proof.json','V5396':'V5437'}))
    rows.append(derive('scripts/verify_lil_B192_references_v5425.py','scripts/verify_lil_B193_references_v5466.py',{
        **shared,'reference_census_v5425':'reference_census_v5466','loader_v5424':'loader_v5465','[192]':'[193]','11-command/no-relative-site':'18-command/no-relative-site',
        "sum(len(r['mapped_commands'])for r in result)==11":"sum(len(r['mapped_commands'])for r in result)==18",'all11':'all18','native_commands_each=11':'native_commands_each=18'}))
    rows.append(derive('scripts/prove_lil_B192_ends_v5426.py','scripts/prove_lil_B193_ends_v5467.py',{
        **shared,'ends_v5426':'ends_v5467','n==192':'n==193'}))
    rows.append(derive('scripts/prove_lil_B192_relocated_controls_v5427.py','scripts/prove_lil_B193_relocated_controls_v5468.py',{
        **shared,'relocated_controls_v5427':'relocated_controls_v5468','blocks[192]':'blocks[193]','block=192':'block=193','00a0ffff012116a1':'00a0ffff011d39a1',
        'len(dispatches)==8':'len(dispatches)==15','[(0xA000,8,8),(0xC200,396,370),(0,398,372)]':'[(0xA000,8,8),(0xC200,660,670),(0,662,672)]',
        "len(spec['command_map'])==11":"len(spec['command_map'])==18",'all8_progressive_FE':'all15_progressive_FE','all7_progressive_static_actors1':'all14_progressive_static_actors1',
        'Bind8 relocated dispatches':'Bind15 relocated dispatches','8 relocated dispatches,7 progressive/one impersonal FE':'15 relocated dispatches,14 progressive/one impersonal FE'}))
    ROOT.mkdir(parents=True);save(ROOT/'prepared_tools.json',dict(tools=rows,parent=str(PARENT),research=str(ROM),plan=str(PLAN),
        source_stored_logical=[668,666],target_stored_logical=[676,676],source_tailzeros=2,target_tailzeros=0,commands=18,speeches=15,progressive=14,FE=1,relative_sites=0,predicates=0,
        A000_source8_target8=True,C200_source660_target670=True,end_source662_target672=True,parent_loader_reuse_requires_exact_whole_ROM_hash=True,new_emulator_runs=0,new_review_credit=0,full_goal_complete=False))
