"""Prepare source-locked B186 conditional proofs without changing native constants."""
from pathlib import Path
import py_compile

from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save

ROOT=Path('work/analysis/lil_B186_control_preparation_v5138c')

if __name__=='__main__':
    assert not ROOT.exists()
    shared={
        'B182':'B186',
        'source_v4878':'source_v5132',
        'all8_clean_current_complete_context':'all12_clean_current_complete_context',
        'voices_v4879':'voices_v5133',
        '.blocks[182]':'.blocks[186]',
    }
    rows=[]
    rows.append(derive('scripts/prove_lil_B182_predicate500_v4883.py','scripts/prove_lil_B186_predicate700_v5138.py',{
        **shared,
        'Original500 predicate':'Original700 predicate',
        'predicate500_v4883':'predicate700_v5138',
        'probe500':'probe700',
        '0080fffff4010000':'0080ffffbc020000',
        'roll<500':'roll<700',
        'roll==500':'roll==700',
        'threshold=500':'threshold=700',
        'equal500':'equal700',
        'roll>500':'roll>700',
        '[499,500,501]':'[699,700,701]',
        'len(cases)==16':'len(cases)==8',
        "for r in cases)==4":"for r in cases)==2",
        '[512,544]':'[540]',
        'all16_original500':'all8_original700',
        'unforced_cases=4,CPU_only_boundary_fixture_cases=12':'unforced_cases=2,CPU_only_boundary_fixture_cases=6',
        'all16_seed_transitions':'all8_seed_transitions',
        'cases=16,unforced=4,CPU_boundary_fixtures=12':'cases=8,unforced=2,CPU_boundary_fixtures=6',
    }))
    rows.append(derive('scripts/prove_lil_B182_C200_v4883.py','scripts/prove_lil_B186_C200_v5138.py',{
        **shared,'C200_v4883':'C200_v5138',
    }))
    rows.append(derive('scripts/prove_lil_B182_controls_v4883.py','scripts/prove_lil_B186_controls_v5138.py',{
        **shared,'block=182':'block=186',
        'two predicates,ten relative sites':'one predicate,six relative sites',
        'predicate500_v4883':'predicate700_v5138',
        'probe500':'probe700',
        'C200_v4883':'C200_v5138',
        'controls_v4883':'controls_v5138',
        'branches_v4881':'branches_v5134',
        "len(branch['cases'])==100":"len(branch['cases'])==60",
        "len(branch['operands_requiring_adjustment_when_resizing'])==10":"len(branch['operands_requiring_adjustment_when_resizing'])==6",
        'len(commands)==25':'len(commands)==24',
        "        (512,'0080fffff4010000'),(532,'00a0ffff014700a1'),(544,'0080fffff4010000'),\n        (564,'00a0ffff014800a1'),(576,'00a0ffff014600a1'),(630,'00c2'),(632,'00000000')":
        "        (540,'0080ffffbc020000'),(560,'00a0ffff010b19a1'),(572,'00a0ffff011219a1'),\n        (584,'00a0ffff010c19a1'),(644,'00c2'),(646,'00000000')",
        'len(predicates)==4':'len(predicates)==2',
        '[512,544]':'[540]',
        'repeat=2':'repeat=1',
        "p['source_end_offset']==632 and p['C200_offsets']==[630]":"p['source_end_offset']==646 and p['C200_offsets']==[644]",
        '{532,564,576}':'{560,572,584}',
        'two_predicates_three_A000_C200_ten_relative_sites_and_single_end':'one_predicate_three_A000_C200_six_relative_sites_and_single_end',
        'all7_source_current_nonrelative_nonspeech_leaves':'all6_source_current_nonrelative_nonspeech_leaves',
        'both_source_raw_operand_values=500':'source_raw_operand_value=700',
        'exact_source500_threshold':'exact_source700_threshold',
        'all16_original500':'all8_original700',
        'threshold500_uses':'threshold700_uses',
        'source_offset=630':'source_offset=644',
        'all8_speeches':'all12_speeches',
        'source_declared_end_offsets=[632]':'source_declared_end_offsets=[646]',
        'dict(predicates=4':'dict(predicates=2',
    }))
    for r in rows:py_compile.compile(r['successor'],doraise=True)
    ROOT.mkdir(parents=True)
    save(ROOT/'prepared_source_locked_control_producers.json',dict(derivations=rows,new_review_credit=0,full_goal_complete=False))
    print('Prepared three B186 control producers; native high constants and multiplicities unchanged.')
