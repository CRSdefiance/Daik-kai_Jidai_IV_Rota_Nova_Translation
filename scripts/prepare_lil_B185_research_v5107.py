"""Prepare B185 reference paths;reuse only the byte-identical V5076 parent proof."""
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B185_research_tools_v5107')
PARENT=Path('out/all_routes_combined_v5076_candidate.nds')
ROM=Path('out/lil_B185_reference_v5108_RESEARCH_ONLY.nds')
PLAN=Path('work/analysis/lil_B185_relocation_v5105/nested_source_relocation_research.json')
if __name__=='__main__':
    assert not ROOT.exists();tools=[]
    tools.append(derive('scripts/create_lil_B184_reference_v5062.py','scripts/create_lil_B185_reference_v5108.py',{
        'B184':'B185','prepare_lil_B184_research_v5061':'prepare_lil_B185_research_v5107','research_v5062':'research_v5108','stored_v5060':'stored_v5106',
        'all9_final_stored_targets36':'all8_final_stored_targets32','all9_final_targets':'all8_final_targets',
        'editorial_handoff_verification_v5058':'editorial_handoff_verification_v5082',
        "stored['current_final_stored_macro_alignment_cases']==36":"stored['current_final_stored_macro_alignment_cases']==32",
        'current_final_stored_macro_alignment_cases=36':'current_final_stored_macro_alignment_cases=32','==[184]':'==[185]','V5030':'V5076'}))
    tools.append(derive('scripts/verify_lil_B183_loader_v4951.py','scripts/verify_lil_B185_loader_v5109.py',{
        'B183':'B185','prepare_lil_B183_research_v4949':'prepare_lil_B185_research_v5107','loader_v4951':'loader_v5109','research_v4950':'research_v5108',
        'work/analysis/lil_B182_loader_v4899/whole_SC2_and_B182_initial_entry_proof.json':'work/analysis/lil_B184_loader_v5063/whole_SC2_and_B184_initial_entry_proof.json',
        'V4914':'V5076'}))
    tools.append(derive('scripts/verify_lil_B184_references_v5064.py','scripts/verify_lil_B185_references_v5110.py',{
        'B184':'B185','prepare_lil_B184_research_v5061':'prepare_lil_B185_research_v5107','reference_census_v5064':'reference_census_v5110',
        'loader_v5063':'loader_v5109','[184]':'[185]','12-command/no-relative-site':'11-command/no-relative-site',
        "sum(len(r['mapped_commands'])for r in result)==12":"sum(len(r['mapped_commands'])for r in result)==11",'all12':'all11','native_commands_each=12':'native_commands_each=11'}))
    tools.append(derive('scripts/prove_lil_B184_ends_v5065.py','scripts/prove_lil_B185_ends_v5111.py',{
        'B184':'B185','prepare_lil_B184_research_v5061':'prepare_lil_B185_research_v5107','ends_v5065':'ends_v5111','n==184':'n==185'}))
    tools.append(derive('scripts/prove_lil_B184_relocated_controls_v5066.py','scripts/prove_lil_B185_relocated_controls_v5112.py',{
        'B184':'B185','prepare_lil_B184_research_v5061':'prepare_lil_B185_research_v5107','relocated_controls_v5066':'relocated_controls_v5112',
        'blocks[184]':'blocks[185]','block=184':'block=185','00a0ffff011f22a1':'00a0ffff013807a1','len(dispatches)==9':'len(dispatches)==8',
        '[(0xA000,8,8),(0xC200,426,410),(0,428,412)]':'[(0xA000,8,8),(0xC200,382,370),(0,384,372)]',
        "len(spec['command_map'])==12":"len(spec['command_map'])==11",'all9':'all8','all8_progressive_static_actors1':'all7_progressive_static_actors1',
        '9 relocated dispatches':'8 relocated dispatches','8 progressive/one impersonal FE':'7 progressive/one impersonal FE'}))
    ROOT.mkdir(parents=True);save(ROOT/'prepared_tools.json',dict(tools=tools,parent=str(PARENT),research=str(ROM),plan=str(PLAN),
        source388_target376_stored_and_logical=True,source_commands=11,speeches=8,progressive=7,FE=1,source_C200382_maps370_end384_maps372=True,
        exact_whole_ROM_parent_hash_required_before_reusing_previous_research_loader=True,new_emulator_runs=0,new_review_credit=0,full_goal_complete=False))
