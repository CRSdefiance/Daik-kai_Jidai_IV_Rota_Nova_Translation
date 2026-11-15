"""Reuse the strict native money adapter for the one exact source8500 debit."""
from pathlib import Path
from collections import Counter
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.source_locked_derivation_v5118 import native_numbers
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B197_funds_tools_v5660')
if __name__=='__main__':
    assert not ROOT.exists();source=Path('scripts/prove_lil_B196_funds_v5601b.py');text=source.read_text(encoding='utf8')
    a=text.index('AMOUNTS=');b=text.index('BASE=',a)
    r=derive(source,'scripts/prove_lil_B197_funds_v5660.py',{
        text[a:b]:"AMOUNTS={'00a0ffff5afd0191':8500}\n",'B196':'B197','funds_v5601b':'funds_v5660',
        'source_v5590/all36_clean_current_complete_context_with_twelve_choice_labels':'source_v5647/all24_clean_current_complete_context_with_three_choice_labels',
        "list(AMOUNTS.values())==gloss['source_asking_price_ladder']":"list(AMOUNTS.values())==[gloss['source_asking_amount']]",
        'blocks[196]':'blocks[197]','voices_v5591':'voices_v5648','len(cases)==36':'len(cases)==6',
        'six_exact_source_prices_six_unforced_and_thirty_offline_payment_boundaries':'one_exact8500_source_price_one_unforced_and_five_offline_payment_boundaries',
        'six_source_prices_match_six_exact_native_payment_amounts':'source8500_price_matches_exact_native_payment_amount',
        'six_unchanged_context_cases_and_thirty_disclosed_CPU_only_funds_inputs':'one_unchanged_context_case_and_five_disclosed_CPU_only_funds_inputs',
        'six source payments':'one source payment',
        'Six source asking prices match six native payments:36 cases(6 unchanged snapshot/30 disclosed CPU funds inputs).':'Source8500 price matches one native payment:six cases(one unchanged snapshot/five disclosed CPU funds inputs).',
        'native_payment_saturates_at_zero_not_a_proof_of_purchase_affordability_or_outer_eligibility':'native_payment_saturates_at_zero_not_a_proof_of_purchase_affordability_delegation_or_outer_eligibility'})
    old,new=native_numbers(text),native_numbers(Path(r['successor']).read_text());assert old-new==Counter({200000:1}) and not new-old
    ROOT.mkdir(parents=True);save(ROOT/'prepared8500_money_probe.json',dict(tool=r,only_removed_high_numeric_constant_is_prior200000_price_data=True,
        native_instruction_addresses_and_multiplicities_original_snapshot_argument_and_CForce_setter_guard_preserved=True,
        original_other_four_A000_bodies_and_gift_delegation_conditions_not_inferred=True,new_ROMs=0,new_emulator_runs=0,new_credit=0,full_goal_complete=False))
