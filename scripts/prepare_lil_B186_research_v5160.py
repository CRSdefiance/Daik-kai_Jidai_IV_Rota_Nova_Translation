"""Prepare B186 reference gates with exact V5122 parent reuse and measured controls."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save

ROOT=Path('work/analysis/lil_B186_research_tools_v5160')
PARENT=Path('out/all_routes_combined_v5122_candidate.nds')
ROM=Path('out/lil_B186_reference_v5161_RESEARCH_ONLY.nds')
PLAN=Path('work/analysis/lil_B186_relocation_v5157/nested_source_relocation_research.json')
if __name__=='__main__':
    assert not ROOT.exists()
    rows=[derive('scripts/create_lil_B182_reference_v4898.py','scripts/create_lil_B186_reference_v5161.py',{
        'B182':'B186','prepare_lil_B182_research_v4897':'prepare_lil_B186_research_v5160',
        'research_v4898':'research_v5161','stored_v4894':'stored_v5158',
        'all8_final_stored_targets32_macro_cases':'all12_final_stored_targets48_macro_cases',
        'editorial_handoff_verification_v4874':'editorial_handoff_verification_v5128',
        'all8_final_targets':'all12_final_targets',
        "stored['current_final_stored_macro_alignment_cases']==32":"stored['current_final_stored_macro_alignment_cases']==48",
        'current_final_stored_macro_alignment_cases=32':'current_final_stored_macro_alignment_cases=48',
        '==[182]':'==[186]','V4867':'V5122',
    })]
    rows.append(derive('scripts/verify_lil_B185_loader_v5109.py','scripts/verify_lil_B186_loader_v5162.py',{
        'B185':'B186','prepare_lil_B185_research_v5107':'prepare_lil_B186_research_v5160',
        'loader_v5109':'loader_v5162','research_v5108':'research_v5161',
        'work/analysis/lil_B184_loader_v5063/whole_SC2_and_B184_initial_entry_proof.json':'work/analysis/lil_B185_loader_v5109/whole_SC2_and_B185_initial_entry_proof.json',
        'V5076':'V5122',
    }))
    rows.append(derive('scripts/verify_lil_B182_references_v4900.py','scripts/verify_lil_B186_references_v5163.py',{
        'B182':'B186','prepare_lil_B182_research_v4897':'prepare_lil_B186_research_v5160',
        'reference_census_v4900':'reference_census_v5163','loader_v4899':'loader_v5162','[182]':'[186]',
        '25-command/ten-relative-site':'24-command/six-relative-site',
        "sum(len(r['mapped_commands'])for r in result)==25":"sum(len(r['mapped_commands'])for r in result)==24",
        "sum(r['typed_relative_span_count']for r in result)==10":"sum(r['typed_relative_span_count']for r in result)==6",
        "sum(r['target_native_skip_cases']for r in result)==50":"sum(r['target_native_skip_cases']for r in result)==30",
        'all25_commands_ten_relative_sites':'all24_commands_six_relative_sites',
        'all25_clean_current_target_commands_and_ten_relative_sites':'all24_clean_current_target_commands_and_six_relative_sites',
        'native_commands_each=25':'native_commands_each=24',
    }))
    rows.append(derive('scripts/prove_lil_B182_ends_v4901.py','scripts/prove_lil_B186_ends_v5164.py',{
        'B182':'B186','prepare_lil_B182_research_v4897':'prepare_lil_B186_research_v5160',
        'ends_v4901':'ends_v5164','n==182':'n==186','two_declared_tail_end_decodes_ten_relative_sites':'two_declared_tail_end_decodes_six_relative_sites',
    }))
    rows.append(derive('scripts/prove_lil_B182_relocated_controls_v4902.py','scripts/prove_lil_B186_relocated_controls_v5165.py',{
        'B182':'B186','relocated_controls_v4902':'relocated_controls_v5165',
        'prepare_lil_B182_research_v4897':'prepare_lil_B186_research_v5160',
        'predicate500_v4896':'predicate700_v5159','probe500':'probe700','C200_v4883':'C200_v5138',
        'editorial_manuscript_v3':'editorial_manuscript_v5','blocks[182]':'blocks[186]',
        'len(dispatches)==8':'len(dispatches)==12',
        'all7_source_current_nonrelative_nonspeech_leaves':'all6_source_current_nonrelative_nonspeech_leaves',
        'len(leaves)==7 and len(predicates)==2':'len(leaves)==6 and len(predicates)==1',
        '[512,544]':'[540]','repeat=2':'repeat=1',
        "after['C200_offsets']==[630] and after['source_end_offset']==632":"after['C200_offsets']==[644] and after['source_end_offset']==646",
        'len(paths)==25':'len(paths)==5','{532,564,576}':'{560,572,584}',
        'all8_dispatches_two_RNG_predicates_three_effects_C200_and25_mapped_paths':'all12_dispatches_one_RNG_predicate_three_effects_C200_and5_mapped_paths',
        'all7_exact_nonrelative_leaves':'all6_exact_nonrelative_leaves',
        'all25_source_and_relocated_structural_paths_identical':'all5_source_and_relocated_structural_paths_identical',
        'all10_native_relative_sites_and50_skip_cases_bound':'all6_native_relative_sites_and30_skip_cases_bound',
        'whole_exchange_all8_speeches':'whole_exchange_all12_speeches',
        'B182 relocation:8 dispatches,7 exact leaves,2 unforced RNG predicate pairs,3 opaque effect pairs,C200 and25 structural paths pass.':
        'B186 relocation:12 dispatches,6 exact leaves,1 unforced RNG predicate pair,3 opaque effect pairs,C200 and5 structural paths pass.',
    }))
    ROOT.mkdir(parents=True);save(ROOT/'prepared_tools.json',dict(tools=rows,parent=str(PARENT),research=str(ROM),plan=str(PLAN),
        speeches=12,commands=24,relative_sites=6,predicates=1,raw_threshold=700,alternative_effects=3,C200=1,source_end=646,target_end=578,
        source_stored_logical= [652,650],target_stored_logical=[584,582],source_and_target_two_tailzeros=True,
        source_predicate540_aligned_target478_halfword_aligned=True,
        exact_original_helper_scratch_proof='work/analysis/lil_B186_predicate700_v5159/all12_aligned_and_unaligned_original700_ownership_cases.json',
        parent_loader_reuse_requires_exact_whole_ROM_hash=True,new_emulator_runs=0,new_review_credit=0,full_goal_complete=False))
    print('Prepared B186 reference,loader,census,end and mapped conditional/control gates;parent reuse requires exact V5122 equality.')
