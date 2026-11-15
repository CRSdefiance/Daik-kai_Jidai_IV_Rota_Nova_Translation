"""Prepare one500 predicate,six relative sites and three early alternative effects."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B190_control_preparation_v5318')
if __name__=='__main__':
    assert not ROOT.exists()
    shared={'B186':'B190','source_v5132/all12':'source_v5314/all17','voices_v5133':'voices_v5315','.blocks[186]':'.blocks[190]'}
    rows=[derive('scripts/prove_lil_B186_predicate700_v5138.py','scripts/prove_lil_B190_predicate500_v5318.py',{
        **shared,'Original700 predicate':'Original500 predicate','predicate700_v5138':'predicate500_v5318','probe700':'probe500',
        '0080ffffbc020000':'0080fffff4010000','roll<700':'roll<500','roll==700':'roll==500','threshold=700':'threshold=500','equal700':'equal500','roll>700':'roll>500',
        '[699,700,701]':'[499,500,501]','[540]':'[8]','all8_original700':'all8_original500',
    })]
    rows.append(derive('scripts/prove_lil_B186_C200_v5138.py','scripts/prove_lil_B190_C200_v5318.py',{
        **shared,'C200_v5138':'C200_v5318',
    }))
    rows.append(derive('scripts/prove_lil_B186_controls_v5138.py','scripts/prove_lil_B190_controls_v5318.py',{
        **shared,'block=186':'block=190','predicate700_v5138':'predicate500_v5318','probe700':'probe500','C200_v5138':'C200_v5318',
        'controls_v5138':'controls_v5318','branches_v5134':'branches_v5318','len(commands)==24':'len(commands)==29',
        "        (540,'0080ffffbc020000'),(560,'00a0ffff010b19a1'),(572,'00a0ffff011219a1'),\n        (584,'00a0ffff010c19a1'),(644,'00c2'),(646,'00000000')":
        "        (8,'0080fffff4010000'),(28,'00a0ffff014c41a1'),(40,'00a0ffff014b41a1'),\n        (52,'00a0ffff014d41a1'),(600,'00c2'),(602,'00000000')",
        '[540]':'[8]',"p['source_end_offset']==646 and p['C200_offsets']==[644]":"p['source_end_offset']==602 and p['C200_offsets']==[600]",
        '{560,572,584}':'{28,40,52}','source_raw_operand_value=700':'source_raw_operand_value=500','exact_source700_threshold':'exact_source500_threshold',
        'all8_original700':'all8_original500','threshold700_uses':'threshold500_uses','source_offset=644':'source_offset=600',
        'all12_speeches':'all17_speeches','source_declared_end_offsets=[646]':'source_declared_end_offsets=[602]',
    }))
    ROOT.mkdir(parents=True);save(ROOT/'prepared_source_locked_control_producers.json',dict(derivations=rows,
        original_native_high_integer_constants_and_multiplicities_preserved=True,source500_predicate_at8=True,
        six_original_relative_sites_and_nested_alternative_effects_required=True,new_review_credit=0,full_goal_complete=False))
