"""Prepare all reference gates for the mixed-predicate and possible no-effect scene."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B191_research_tools_v5380')
PARENT=Path('out/all_routes_combined_v5346_candidate.nds')
ROM=Path('out/lil_B191_reference_v5381_RESEARCH_ONLY.nds')
PLAN=Path('work/analysis/lil_B191_relocation_v5377b/nested_source_relocation_research.json')
if __name__=='__main__':
    assert not ROOT.exists()
    rows=[derive('scripts/create_lil_B190_reference_v5332.py','scripts/create_lil_B191_reference_v5381.py',{
        'B190':'B191','prepare_lil_B190_research_v5331':'prepare_lil_B191_research_v5380','research_v5332':'research_v5381','stored_v5329':'stored_v5378b',
        'all17_final':'all13_final','targets68_macro':'targets52_macro','editorial_handoff_verification_v5310':'editorial_handoff_verification_v5352',
        "stored['current_final_stored_macro_alignment_cases']==68":"stored['current_final_stored_macro_alignment_cases']==52",'current_final_stored_macro_alignment_cases=68':'current_final_stored_macro_alignment_cases=52','==[190]':'==[191]','V5304':'V5346',
    })]
    rows.append(derive('scripts/verify_lil_B190_loader_v5333.py','scripts/verify_lil_B191_loader_v5382.py',{
        'B190':'B191','prepare_lil_B190_research_v5331':'prepare_lil_B191_research_v5380','loader_v5333':'loader_v5382','research_v5332':'research_v5381',
        'work/analysis/lil_B189_loader_v5291/whole_SC2_and_B189_initial_entry_proof.json':'work/analysis/lil_B190_loader_v5333/whole_SC2_and_B190_initial_entry_proof.json','V5304':'V5346',
    }))
    rows.append(derive('scripts/verify_lil_B190_references_v5334.py','scripts/verify_lil_B191_references_v5383.py',{
        'B190':'B191','prepare_lil_B190_research_v5331':'prepare_lil_B191_research_v5380','reference_census_v5334':'reference_census_v5383','loader_v5333':'loader_v5382',
        '[190]':'[191]','29-command/six-relative-site':'38-command/16-relative-site',"sum(len(r['mapped_commands'])for r in result)==29":"sum(len(r['mapped_commands'])for r in result)==38",
        "sum(r['typed_relative_span_count']for r in result)==6":"sum(r['typed_relative_span_count']for r in result)==16","sum(r['target_native_skip_cases']for r in result)==30":"sum(r['target_native_skip_cases']for r in result)==80",
        'all29_commands_six_relative_sites':'all38_commands_sixteen_relative_sites','all29_clean_current_target_commands_and_six_relative_sites':'all38_clean_current_target_commands_and_sixteen_relative_sites',
        'native_commands_each=29,relative_sites=6,target_native_skip_cases=30':'native_commands_each=38,relative_sites=16,target_native_skip_cases=80',
    }))
    rows.append(derive('scripts/prove_lil_B190_ends_v5335.py','scripts/prove_lil_B191_ends_v5384.py',{
        'B190':'B191','prepare_lil_B190_research_v5331':'prepare_lil_B191_research_v5380','ends_v5335':'ends_v5384','n==190':'n==191','six_relative_sites':'sixteen_relative_sites',
    }))
    rows.append(derive('scripts/prove_lil_B190_relocated_controls_v5336.py','scripts/prove_lil_B191_relocated_controls_v5385.py',{
        'B190':'B191','relocated_controls_v5336':'relocated_controls_v5385','prepare_lil_B190_research_v5331':'prepare_lil_B191_research_v5380',
        'from scripts.prove_lil_B190_predicate500_v5330 import probe500':'from scripts.prove_lil_B191_predicates_v5362 import probe_mixed',
        'probe500':'probe_mixed','C200_v5318':'C200_v5363','editorial_manuscript_v3':'editorial_manuscript_v4','blocks[190]':'blocks[191]',
        'len(dispatches)==17':'len(dispatches)==13','all6_source_current_nonrelative':'all9_source_current_nonrelative','all6_exact_nonrelative_leaves':'all9_exact_nonrelative_leaves',
        'len(leaves)==6 and len(predicates)==1':'len(leaves)==9 and len(predicates)==3','len(effects)==3':'len(effects)==4',
        'values[[8].index(source_at)]':'values[[8,28,76].index(source_at)]','repeat=1':'repeat=3',
        "assert len(after['A000_offsets'])==1 and after['C200_offsets']==[600] and after['source_end_offset']==602":"assert len(after['A000_offsets']) in [0,1] and after['C200_offsets']==[728] and after['source_end_offset']==730",
        'len(paths)==5':'len(paths)==125','=={28,40,52}':'=={48,60,96,108}',
        'all17_dispatches_one_RNG_predicate_three_effects_C200_and5_mapped_paths':'all13_dispatches_three_RNG_predicates_four_effects_C200_and125_mapped_paths',
        'all5_source_and_relocated_structural_paths_identical':'all125_source_and_relocated_structural_paths_identical',
        'all6_native_relative_sites_and30_skip_cases':'all16_native_relative_sites_and80_skip_cases',
        'whole_exchange_all17_speeches_and_three_alternative_effects':'whole_exchange_all13_speeches_four_alternative_effects_and_no_effect_paths',
        'B190 relocation:17 dispatches,6 exact leaves,1 unforced RNG predicate pair,3 opaque effect pairs,C200 and5 structural paths pass.':'B191 relocation:13 dispatches,9 exact leaves,3 unforced mixed-predicate pairs,4 opaque effect pairs,C200 and125 structural paths pass,including no-effect paths.',
    }))
    ROOT.mkdir(parents=True);save(ROOT/'prepared_all_conditional_reference_gates.json',dict(tools=rows,parent=str(PARENT),research=str(ROM),plan=str(PLAN),
        expected38_commands13_speeches_three_predicates16_sites80_skip_cases_and125_paths=True,
        no_effect_paths_and_all_four_source_effect_alternatives_preserved=True,no_ROM_registry_or_credit_mutation_by_preparation=True,full_goal_complete=False))
