"""Bind the glass-collection scene to verified V5219 before reading old English."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B188_source_tools_v5232')
if __name__=='__main__':
    assert not ROOT.exists()
    rows=[derive('scripts/map_lil_B187_source_v5188.py','scripts/map_lil_B188_source_v5232.py',{
        'B187':'B188','source_v5188':'source_v5232','editorial_handoff_verification_v5183':'editorial_handoff_verification_v5225',
        'clean_context_v5187/all16':'clean_context_v5231/all11','len(known)==6027':'len(known)==6043','blocks[187]':'blocks[188]',
        'len(old)==19 and len(spoken)==16':'len(old)==14 and len(spoken)==11','[87,155,254]':'[130,150,254]','block=187':'block=188',
        'lil_B186_runs_v5179':'lil_B187_runs_v5221','physical_speeches=16':'physical_speeches=11',
        'all16_clean_current_complete_context':'all11_clean_current_complete_context',
        'total_editorial_objects=16,speech_objects=16,ordinary_source_speeches=15':'total_editorial_objects=11,speech_objects=11,ordinary_source_speeches=10',
        'source_static_actor_selectors=[87,155],source_native_commands=19':'source_static_actor_selectors=[130,150],source_native_commands=14',
        'all16_clean_first_glosses':'all11_clean_first_glosses',
        'B187 bound:16 complete speeches,19 linear commands,A000/C200/end;two source actors and current V5177 opening snapshot.':
        'B188 bound:11 complete speeches,14 linear commands,A000/C200/end;two source actors and current V5219 opening snapshot.',
    })]
    rows.append(derive('scripts/reconcile_lil_B187_voices_v5189.py','scripts/reconcile_lil_B188_voices_v5233.py',{
        'B187':'B188','voices_v5189':'voices_v5233','source_v5188/all16':'source_v5232/all11','[87,155]':'[130,150]','V5177':'V5219',
        'no_rank_profession_medical_role_or_relationship_inferred_from_concern_or_remedy_hearsay':
        'no_rank_age_profession_or_relationship_inferred_from_archaic_or_deferential_register',
    }))
    shared={'B187':'B188','source_v5188/all16':'source_v5232/all11','voices_v5189':'voices_v5233'}
    rows.append(derive('scripts/prove_lil_B187_dispatches_v5190.py','scripts/prove_lil_B188_dispatches_v5234.py',{
        **shared,'dispatches_v5190':'dispatches_v5234','Bind32 source/current':'Bind22 source/current','len(cases)==32':'len(cases)==22',
        'all16_source_current':'all11_source_current','32 source/current dispatches pass':'22 source/current dispatches pass',
    }))
    rows.append(derive('scripts/prove_lil_B187_entry_v5191.py','scripts/prove_lil_B188_entry_v5235.py',{
        **shared,'entry_v5191':'entry_v5235','in [187]':'in [188]',
    }))
    rows.append(derive('scripts/prove_lil_B187_controls_v5192.py','scripts/prove_lil_B188_controls_v5236.py',{
        **shared,'controls_v5192':'controls_v5236','blocks[187]':'blocks[188]','block=187':'block=188',
        "[(8,'00a0ffff014e2fa1'),(672,'00c2'),(674,'00000000')]":"[(8,'00a0ffff01293ba1'),(476,'00c2'),(478,'00000000')]",
        'len(commands)==19 and len(blocks[0])==len(blocks[1])==680':'len(commands)==14 and len(blocks[0])==len(blocks[1])==484',
        'source_offset=672':'source_offset=476','source_declared_end_offsets=[674]':'source_declared_end_offsets=[478]',
    }))
    rows.append(derive('scripts/prove_lil_B187_names_v5193.py','scripts/prove_lil_B188_names_v5237.py',{
        **shared,'names_v5193':'names_v5237','[87,155]':'[130,150]',
    }))
    ROOT.mkdir(parents=True);save(ROOT/'prepared_current_source_native_contracts.json',dict(tools=rows,
        previous_goal_turn_classification='progress',previous_goal_turn_evidence='work/analysis/editorial_handoff_verification_v5225/verified_handoff.json',
        current_candidate='out/all_routes_combined_v5219_candidate.nds',clean_only_glosses_already_complete=11,
        expected_linear_commands=14,expected_control_leaves=3,source_stored_bytes=484,source_logical_end=482,source_tailzeros=2,
        original_actor_getter_CB184_and_all_existing_native_high_constants_and_multiplicities_preserved=True,
        no_predecessor_English_or_ROM_or_ledger_change=True,new_review_credit=0,full_goal_complete=False))
