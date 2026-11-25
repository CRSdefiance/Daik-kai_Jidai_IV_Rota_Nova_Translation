"""Bind the conditional remedy scene to verified V5304 without old English."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B190_source_tools_v5314')
if __name__=='__main__':
    assert not ROOT.exists()
    rows=[derive('scripts/map_lil_B186_source_v5132.py','scripts/map_lil_B190_source_v5314.py',{
        'B186':'B190','source_v5132':'source_v5314','editorial_handoff_verification_v5128':'editorial_handoff_verification_v5310',
        'clean_context_v5131/all12':'clean_context_v5313/all17','len(known)==6015':'len(known)==6071','blocks[186]':'blocks[190]',
        'len(old)==24 and len(spoken)==12':'len(old)==29 and len(spoken)==17','[174,175,254]':'[119,159,254]','block=186':'block=190',
        'lil_B185_runs_v5124':'lil_B189_runs_v5306','physical_speeches=12':'physical_speeches=17','all12_clean_current_complete_context':'all17_clean_current_complete_context',
        'total_editorial_objects=12,speech_objects=12,ordinary_source_speeches=11':'total_editorial_objects=17,speech_objects=17,ordinary_source_speeches=16',
        'source_static_actor_selectors=[174,175],source_native_commands=24':'source_static_actor_selectors=[119,159],source_native_commands=29',
        'all12_clean_first_glosses':'all17_clean_first_glosses',
        'B186 bound:12 complete speeches,24 commands,1 predicate,6 relative sites,3 A000/C200/end;two source actors and current V5122 opening snapshot.':
        'B190 bound:17 complete speeches,29 commands,one500 predicate,six relative sites,three A000/C200/end;two source actors and current V5304 opening snapshot.',
    })]
    rows.append(derive('scripts/reconcile_lil_B188_voices_v5233.py','scripts/reconcile_lil_B190_voices_v5315.py',{
        'B188':'B190','voices_v5233':'voices_v5315','source_v5232/all11':'source_v5314/all17','[130,150]':'[119,159]','V5219':'V5304',
        'no_rank_age_profession_or_relationship_inferred_from_archaic_or_deferential_register':'no_rank_kinship_medical_role_or_relationship_inferred_from_remedy_rumor_or_danna',
    }))
    shared={'B186':'B190','source_v5132/all12':'source_v5314/all17','voices_v5133':'voices_v5315'}
    rows.append(derive('scripts/prove_lil_B186_dispatches_v5135.py','scripts/prove_lil_B190_dispatches_v5316.py',{
        **shared,'dispatches_v5135':'dispatches_v5316','Bind24 source/current':'Bind34 source/current','len(cases)==24':'len(cases)==34',
        'all12_source_current_dispatches_no_macros_and3_control_leaves':'all17_source_current_dispatches_no_macros_and6_control_leaves',
        '24 source/current dispatches pass':'34 source/current dispatches pass',
    }))
    rows.append(derive('scripts/prove_lil_B186_entry_v5136.py','scripts/prove_lil_B190_entry_v5317.py',{
        **shared,'entry_v5136':'entry_v5317','in [186]':'in [190]',
    }))
    rows.append(derive('scripts/prove_lil_B188_names_v5237.py','scripts/prove_lil_B190_names_v5319.py',{
        'B188':'B190','source_v5232/all11':'source_v5314/all17','voices_v5233':'voices_v5315','names_v5237':'names_v5319','[130,150]':'[119,159]',
    }))
    rows.append(derive('scripts/prove_lil_B186_branches_v5134.py','scripts/prove_lil_B190_branches_v5318.py',{
        **shared,'branches_v5134':'branches_v5318',
    }))
    ROOT.mkdir(parents=True);save(ROOT/'prepared_current_source_native_contracts.json',dict(tools=rows,
        previous_goal_turn_classification='progress',previous_goal_turn_evidence='work/analysis/editorial_handoff_verification_v5310/verified_handoff.json',
        current_candidate='out/all_routes_combined_v5304_candidate.nds',clean_only_glosses_already_complete=17,
        expected_commands=29,expected_nonrelative_control_leaves=6,source_stored_bytes=608,source_logical_end=606,source_tailzeros=2,
        exact_hex77_9F_equal_decimal119_159_guarded=True,conditional500_predicate_and_six_nested_relative_sites_require_distinct_checks=True,
        original_actor_getter_CB184_and_all_existing_native_high_constants_and_multiplicities_preserved=True,
        no_predecessor_English_or_ROM_or_ledger_change=True,new_review_credit=0,full_goal_complete=False))
