"""Prepare exact-parent reference,whole loaders and twenty relocated native dispatches."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save

ROOT=Path('work/analysis/lil_B195_research_tools_v5563')
PARENT=Path('out/all_routes_combined_v5531_candidate.nds')
ROM=Path('out/lil_B195_reference_v5564_RESEARCH_ONLY.nds')
PLAN=Path('work/analysis/lil_B195_relocation_v5561/nested_source_relocation_research.json')
if __name__=='__main__':
    assert not ROOT.exists()
    shared={'B193':'B195','prepare_lil_B193_research_v5463':'prepare_lil_B195_research_v5563'}
    rows=[derive('scripts/create_lil_B193_reference_v5464.py','scripts/create_lil_B195_reference_v5564.py',{
        **shared,'research_v5464':'research_v5564','stored_v5462':'stored_v5562','all15':'all20','targets60':'targets80',
        'verification_v5443':'verification_v5560',"stored['current_final_stored_macro_alignment_cases']==60":"stored['current_final_stored_macro_alignment_cases']==80",
        'current_final_stored_macro_alignment_cases=60':'current_final_stored_macro_alignment_cases=80','==[193]':'==[195]','V5437':'V5531'} )]
    rows.append(derive('scripts/verify_lil_B193_loader_v5465.py','scripts/verify_lil_B195_loader_v5565.py',{
        **shared,'loader_v5465':'loader_v5565','research_v5464':'research_v5564',
        'work/analysis/lil_B192_loader_v5424/whole_SC2_and_B192_initial_entry_proof.json':
        'work/analysis/lil_B194_loader_v5510/whole_SC2_and_B194_initial_entry_proof.json','V5437':'V5531'}))
    rows.append(derive('scripts/verify_lil_B193_references_v5466.py','scripts/verify_lil_B195_references_v5566.py',{
        **shared,'reference_census_v5466':'reference_census_v5566','loader_v5465':'loader_v5565','[193]':'[195]',
        '18-command/no-relative-site':'23-command/no-relative-site',"sum(len(r['mapped_commands'])for r in result)==18":"sum(len(r['mapped_commands'])for r in result)==23",
        'all18':'all23','native_commands_each=18':'native_commands_each=23'}))
    rows.append(derive('scripts/prove_lil_B193_ends_v5467.py','scripts/prove_lil_B195_ends_v5567.py',{
        **shared,'ends_v5467':'ends_v5567','n==193':'n==195'}))
    rows.append(derive('scripts/prove_lil_B193_relocated_controls_v5468.py','scripts/prove_lil_B195_relocated_controls_v5568.py',{
        **shared,'relocated_controls_v5468':'relocated_controls_v5568','blocks[193]':'blocks[195]','block=193':'block=195',
        'from scripts.prove_lil_B180_C200_v4784 import':'from scripts.prove_lil_B190_C200_v5318 import','00a0ffff011d39a1':'00a0ffff010841a1',
        'len(dispatches)==15':'len(dispatches)==20','[(0xA000,8,8),(0xC200,660,670),(0,662,672)]':'[(0xA000,8,8),(0xC200,704,610),(0,706,612)]',
        "len(spec['command_map'])==18":"len(spec['command_map'])==23",'all15_progressive_FE':'all20_progressive_FE',
        'all14_progressive_static_actors1':'all19_progressive_static_actors1','Bind15 relocated dispatches':'Bind20 relocated dispatches',
        '15 relocated dispatches,14 progressive/one impersonal FE':'20 relocated dispatches,19 progressive/one impersonal FE'}))
    ROOT.mkdir(parents=True);save(ROOT/'prepared_tools.json',dict(tools=rows,parent=str(PARENT),research=str(ROM),plan=str(PLAN),
        source_stored_logical=[712,710],target_stored_logical=[616,616],source_tailzeros=2,target_tailzeros=0,
        commands=23,speeches=20,progressive=19,FE=1,relative_sites=0,predicates=0,
        A000_source8_target8=True,C200_source704_target610=True,end_source706_target612=True,
        source_owned_fleet_descriptor_C200_adapter_used=True,parent_loader_reuse_requires_exact_whole_ROM_hash=True,
        new_emulator_runs=0,new_review_credit=0,full_goal_complete=False))
