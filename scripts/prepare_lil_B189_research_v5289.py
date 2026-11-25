"""Prepare exact-parent reference gates for the measured848-byte two-pair scene."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B189_research_tools_v5289')
PARENT=Path('out/all_routes_combined_v5263_candidate.nds')
ROM=Path('out/lil_B189_reference_v5290_RESEARCH_ONLY.nds')
PLAN=Path('work/analysis/lil_B189_relocation_v5287/nested_source_relocation_research.json')
if __name__=='__main__':
    assert not ROOT.exists()
    shared={'B188':'B189','prepare_lil_B188_research_v5248':'prepare_lil_B189_research_v5289'}
    rows=[derive('scripts/create_lil_B188_reference_v5249.py','scripts/create_lil_B189_reference_v5290.py',{
        **shared,'research_v5249':'research_v5290','stored_v5247':'stored_v5288','all11_final_stored_targets44':'all17_final_stored_targets68','all11_final_targets':'all17_final_targets',
        'editorial_handoff_verification_v5225':'editorial_handoff_verification_v5269',"stored['current_final_stored_macro_alignment_cases']==44":"stored['current_final_stored_macro_alignment_cases']==68",
        'current_final_stored_macro_alignment_cases=44':'current_final_stored_macro_alignment_cases=68','==[188]':'==[189]','V5219':'V5263'} )]
    rows.append(derive('scripts/verify_lil_B188_loader_v5250.py','scripts/verify_lil_B189_loader_v5291.py',{
        **shared,'loader_v5250':'loader_v5291','research_v5249':'research_v5290',
        'work/analysis/lil_B187_loader_v5206/whole_SC2_and_B187_initial_entry_proof.json':'work/analysis/lil_B188_loader_v5250/whole_SC2_and_B188_initial_entry_proof.json','V5219':'V5263'}))
    rows.append(derive('scripts/verify_lil_B188_references_v5251.py','scripts/verify_lil_B189_references_v5292.py',{
        **shared,'reference_census_v5251':'reference_census_v5292','loader_v5250':'loader_v5291','[188]':'[189]',
        '14-command/no-relative-site':'20-command/no-relative-site',"sum(len(r['mapped_commands'])for r in result)==14":"sum(len(r['mapped_commands'])for r in result)==20",
        'all14':'all20','native_commands_each=14':'native_commands_each=20'}))
    rows.append(derive('scripts/prove_lil_B188_ends_v5252.py','scripts/prove_lil_B189_ends_v5293.py',{
        **shared,'ends_v5252':'ends_v5293','n==188':'n==189'}))
    rows.append(derive('scripts/prove_lil_B188_relocated_controls_v5253.py','scripts/prove_lil_B189_relocated_controls_v5294.py',{
        **shared,'relocated_controls_v5253':'relocated_controls_v5294','blocks[188]':'blocks[189]','block=188':'block=189',
        '00a0ffff01293ba1':'00a0ffff012a05a1','len(dispatches)==11':'len(dispatches)==17',
        '[(0xA000,8,8),(0xC200,476,418),(0,478,420)]':'[(0xA000,8,8),(0xC200,764,842),(0,766,844)]',
        "len(spec['command_map'])==14":"len(spec['command_map'])==20",'all11_progressive_FE':'all17_progressive_FE','all10_progressive_static_actors1':'all16_progressive_static_actors1',
        'Bind11 relocated dispatches':'Bind17 relocated dispatches','11 relocated dispatches,10 progressive/one impersonal FE':'17 relocated dispatches,16 progressive/one impersonal FE'}))
    ROOT.mkdir(parents=True);save(ROOT/'prepared_tools.json',dict(tools=rows,parent=str(PARENT),research=str(ROM),plan=str(PLAN),
        source_stored_logical=[772,770],target_stored_logical=[848,848],source_tailzeros=2,target_tailzeros=0,
        commands=20,speeches=17,progressive=16,FE=1,relative_sites=0,predicates=0,A000_source8_target8=True,C200_source764_target842=True,end_source766_target844=True,
        parent_loader_reuse_requires_exact_whole_ROM_hash=True,new_emulator_runs=0,new_review_credit=0,full_goal_complete=False))
