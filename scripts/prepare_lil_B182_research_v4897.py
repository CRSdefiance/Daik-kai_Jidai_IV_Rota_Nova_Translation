"""Prepare B182 reference gates with exact-parent loader reuse and scoped scratch proof."""
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import save

ROOT=Path('work/analysis/lil_B182_research_tools_v4897')
PARENT=Path('out/all_routes_combined_v4867_candidate.nds')
ROM=Path('out/lil_B182_reference_v4898_RESEARCH_ONLY.nds')
PLAN=Path('work/analysis/lil_B182_relocation_v4893/nested_source_relocation_research.json')
if __name__=='__main__':
    assert not ROOT.exists();tools=[]
    tools.append(derive('scripts/create_lil_B181_reference_v4852.py','scripts/create_lil_B182_reference_v4898.py',{
        'B181':'B182','prepare_lil_B181_research_v4851':'prepare_lil_B182_research_v4897',
        'research_v4852':'research_v4898','stored_v4847':'stored_v4894',
        'all10_final_stored_targets40_macro_cases':'all8_final_stored_targets32_macro_cases',
        'editorial_handoff_verification_v4850':'editorial_handoff_verification_v4874',
        'all10_final_targets':'all8_final_targets',"stored['current_final_stored_macro_alignment_cases']==40":"stored['current_final_stored_macro_alignment_cases']==32",
        'current_final_stored_macro_alignment_cases=40':'current_final_stored_macro_alignment_cases=32',
        '==[181]':'==[182]','V4821':'V4867'}))
    tools.append(derive('scripts/verify_lil_B181_loader_v4853.py','scripts/verify_lil_B182_loader_v4899.py',{
        'B181':'B182','prepare_lil_B181_research_v4851':'prepare_lil_B182_research_v4897',
        'loader_v4853':'loader_v4899','research_v4852':'research_v4898',
        'work/analysis/lil_B180_loader_v4802/whole_SC2_and_B180_initial_entry_proof.json':
        'work/analysis/lil_B181_loader_v4853/whole_SC2_and_B181_initial_entry_proof.json',
        'V4821':'V4867'}))
    tools.append(derive('scripts/verify_lil_B180_references_v4803.py','scripts/verify_lil_B182_references_v4900.py',{
        'B180':'B182','prepare_lil_B180_research_v4800':'prepare_lil_B182_research_v4897',
        'reference_census_v4803':'reference_census_v4900','loader_v4802':'loader_v4899','[180]':'[182]',
        '28-command':'25-command',"sum(len(r['mapped_commands'])for r in result)==28":"sum(len(r['mapped_commands'])for r in result)==25",
        'all28':'all25','native_commands_each=28':'native_commands_each=25'}))
    tools.append(derive('scripts/prove_lil_B180_ends_v4804.py','scripts/prove_lil_B182_ends_v4901.py',{
        'B180':'B182','prepare_lil_B180_research_v4800':'prepare_lil_B182_research_v4897','ends_v4804':'ends_v4901','n==180':'n==182'}))
    tools.append(derive('scripts/prove_lil_B180_relocated_controls_v4805.py','scripts/prove_lil_B182_relocated_controls_v4902.py',{
        'B180':'B182','relocated_controls_v4805':'relocated_controls_v4902',
        'prepare_lil_B180_research_v4800':'prepare_lil_B182_research_v4897',
        'predicate500_v4782':'predicate500_v4896','C200_v4784':'C200_v4883',
        'blocks[180]':'blocks[182]','len(dispatches)==11':'len(dispatches)==8',
        'assert a%4==b%4==0':'assert a%4==0 and b%4==2',
        'full4MiB_difference_exactly_one_original_owned_RNG_word':'full4MiB_difference_exactly_original_owned_RNG_and_optional_operand_scratch',
        '[452,484]':'[512,544]',"after['C200_offsets']==[570] and after['source_end_offset']==572":"after['C200_offsets']==[630] and after['source_end_offset']==632",
        '{472,504,516}':'{532,564,576}','all11':'all8','relocation:11 dispatches':'relocation:8 dispatches'}))
    ROOT.mkdir(parents=True);save(ROOT/'prepared_tools.json',dict(tools=tools,parent=str(PARENT),research=str(ROM),plan=str(PLAN),
        speeches=8,commands=25,relative_sites=10,predicates=2,alternative_effects=3,C200=1,end=632,
        source_operand_offsets_aligned_target_offsets_halfword_aligned=True,
        exact_original_helper_scratch_proved_by24_cases='work/analysis/lil_B182_predicate500_v4896/all24_aligned_and_unaligned_original500_ownership_cases.json',
        parent_loader_reuse_requires_exact_whole_ROM_hash=True,new_emulator_runs=0,new_review_credit=0,full_goal_complete=False))
    print('Prepared B182 reference,loader,census,end and relocated conditional/control gates.')
