"""Prepare all mixed-predicate structural paths without flattening no-effect branches."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B191_control_tools_v5363')
if __name__=='__main__':
    assert not ROOT.exists()
    rows=[derive('scripts/prove_lil_B190_C200_v5318.py','scripts/prove_lil_B191_C200_v5363.py',{
        'B190':'B191','C200_v5318':'C200_v5363','source_v5314/all17':'source_v5356/all13','voices_v5315':'voices_v5357','blocks[190]':'blocks[191]',
    })]
    rows.append(derive('scripts/prove_lil_B190_controls_v5318.py','scripts/prove_lil_B191_controls_v5363.py',{
        'B190':'B191','controls_v5318':'controls_v5363','source_v5314/all17':'source_v5356/all13','branches_v5318':'branches_v5360','voices_v5315':'voices_v5357',
        'from scripts.prove_lil_B190_predicate500_v5318 import probe500 as probe':'from scripts.prove_lil_B191_predicates_v5362 import probe_mixed as probe',
        'C200_v5318':'C200_v5363',"len(branch['cases'])==60":"len(branch['cases'])==160","len(branch['operands_requiring_adjustment_when_resizing'])==6":"len(branch['operands_requiring_adjustment_when_resizing'])==16",
        'blocks[190]':'blocks[191]','len(commands)==29':'len(commands)==38','block=190':'block=191',
        "(8,'0080fffff4010000'),(28,'00a0ffff014c41a1'),(40,'00a0ffff014b41a1'),\n        (52,'00a0ffff014d41a1'),(600,'00c2'),(602,'00000000')":
        "(8,'0080fffff4010000'),(28,'0080ffffbc020000'),(48,'00a0ffff01512aa1'),(60,'00a0ffff01522aa1'),\n        (76,'0080fffff4010000'),(96,'00a0ffff01542aa1'),(108,'00a0ffff01552aa1'),(728,'00c2'),(730,'00000000')",
        'len(predicates)==2':'len(predicates)==6','for offset in [8]':'for offset in [8,28,76]',
        'values[[8].index(cursor)]':'values[[8,28,76].index(cursor)]','repeat=1':'repeat=3',
        "p['source_end_offset']==602 and p['C200_offsets']==[600]":"p['source_end_offset']==730 and p['C200_offsets']==[728]",
        '=={28,40,52}':'=={48,60,96,108}',"all(len(p['A000_offsets'])==1 for p in paths)":"all(len(p['A000_offsets']) in [0,1] for p in paths) and any(not p['A000_offsets'] for p in paths) and len(paths)==125",
        'one_predicate_three_A000_C200_six_relative_sites_and_single_end':'three_predicates_four_A000_C200_sixteen_relative_sites_and_single_end',
        'all6_source_current_nonrelative':'all9_source_current_nonrelative','source_raw_operand_value=500':"source_raw_operand_values={'8':500,'28':700,'76':500}",
        "exact_source500_threshold_and_original_RNG_ownership_proof='work/analysis/lil_B190_predicate500_v5318/all8_original500_predicate_RNG_ownership_cases.json'":"exact_mixed_threshold_and_original_RNG_ownership_proof='work/analysis/lil_B191_predicates_v5362/all24_original_mixed_predicate_RNG_ownership_cases.json'",
        'threshold500_uses_original':'thresholds500_700_use_original','source_offset=600':'source_offset=728','all17_speeches_all_three_alternative_effects':'all13_speeches_all_four_alternative_effects_and_no_effect_paths',
        'source_declared_end_offsets=[602]':'source_declared_end_offsets=[730]',
        'Bind one predicate,six relative sites,three opaque effects':'Bind three predicates,16relative sites,four opaque effects and no-effect paths',
        'predicates=2,A000_source_current_pairs=3':'predicates=6,A000_source_current_pairs=4',
    }))
    ROOT.mkdir(parents=True);save(ROOT/'prepared_exact_conditional_contracts.json',dict(tools=rows,
        source38_commands13_speeches_three_predicates16_relative_sites_four_effect_alternatives=True,
        source_no_effect_paths_must_remain_possible=True,expected_structural_paths=125,no_credit=True,full_goal_complete=False))
