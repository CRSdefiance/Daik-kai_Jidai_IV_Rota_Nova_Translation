"""Bind the relocated halfword-aligned700 operand to its original optional scratch writer."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save

ROOT=Path('work/analysis/lil_B186_predicate_ownership_preparation_v5159')
if __name__=='__main__':
    assert not ROOT.exists()
    row=derive('scripts/prove_lil_B182_predicate500_v4896.py','scripts/prove_lil_B186_predicate700_v5159.py',{
        'B182':'B186','Original500':'Original700','predicate500_v4896':'predicate700_v5159',
        'source_v4878':'source_v5132','all8_clean_current_complete_context':'all12_clean_current_complete_context','voices_v4879':'voices_v5133',
        'relocation_v4893':'relocation_v5157','.blocks[182]':'.blocks[186]',
        'probe500':'probe700','0080fffff4010000':'0080ffffbc020000',
        'roll<500':'roll<700','roll==500':'roll==700','threshold=500':'threshold=700','equal500':'equal700','roll>500':'roll>700',
        'value=500':'value=700','scratch_address-BASE,500':'scratch_address-BASE,700',
        '[499,500,501]':'[699,700,701]','[512,544]':'[540]',
        'len(cases)==24':'len(cases)==12',"for r in cases)==6":"for r in cases)==3",
        'all24_aligned_and_unaligned_original500':'all12_aligned_and_unaligned_original700',
        'unforced_cases=6,CPU_only_boundary_fixture_cases=18':'unforced_cases=3,CPU_only_boundary_fixture_cases=9',
        'all24_seed_and_operand':'all12_seed_and_operand','cases=24,unforced=6,CPU_boundary_fixtures=18':'cases=12,unforced=3,CPU_boundary_fixtures=9',
    })
    ROOT.mkdir(parents=True);save(ROOT/'prepared_original_optional_scratch_proof.json',dict(derivation=row,
        measured_source_predicate_offset=540,measured_relocated_predicate_offset=478,source_aligned_relocated_halfword_aligned=True,
        source_and_target_original_RNG_and_optional_operand_scratch_writers_preserved=True,
        no_emulator_seed_outcome_or_native_code_forcing=True,new_review_credit=0,full_goal_complete=False))
    print('Prepared12 exact700 predicate cases:source/current aligned and relocated halfword-aligned;no native constant changes.')
