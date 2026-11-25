"""Bind the next linear source exchange to exact V5177 RAM without exposing old prose."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save

ROOT=Path('work/analysis/lil_B187_source_tools_v5188')
if __name__=='__main__':
    assert not ROOT.exists()
    rows=[derive('scripts/map_lil_B186_source_v5132.py','scripts/map_lil_B187_source_v5188.py',{
        'B186':'B187','source_v5132':'source_v5188','editorial_handoff_verification_v5128':'editorial_handoff_verification_v5183',
        'clean_context_v5131/all12':'clean_context_v5187/all16','len(known)==6015':'len(known)==6027','blocks[186]':'blocks[187]',
        'len(old)==24 and len(spoken)==12':'len(old)==19 and len(spoken)==16',
        '[174,175,254]':'[87,155,254]','block=186':'block=187',
        "[0x8000,0xA000,0xA000,0xA000,0xC200,0]":"[0xA000,0xC200,0]",
        'lil_B185_runs_v5124':'lil_B186_runs_v5179',
        'physical_speeches=12':'physical_speeches=16','relative_sites=6':'relative_sites=0',
        'all12_clean_current_complete_context':'all16_clean_current_complete_context',
        'total_editorial_objects=12,speech_objects=12,ordinary_source_speeches=11':'total_editorial_objects=16,speech_objects=16,ordinary_source_speeches=15',
        'source_static_actor_selectors=[174,175],source_native_commands=24':'source_static_actor_selectors=[87,155],source_native_commands=19',
        'source_A000=3':'source_A000=1','source_predicates=1':'source_predicates=0',
        'all12_clean_first_glosses':'all16_clean_first_glosses',
        'B186 bound:12 complete speeches,24 commands,1 predicate,6 relative sites,3 A000/C200/end;two source actors and current V5122 opening snapshot.':
        'B187 bound:16 complete speeches,19 linear commands,A000/C200/end;two source actors and current V5177 opening snapshot.',
    })]
    rows.append(derive('scripts/reconcile_lil_B186_voices_v5133.py','scripts/reconcile_lil_B187_voices_v5189.py',{
        'B186':'B187','voices_v5133':'voices_v5189','source_v5132/all12':'source_v5188/all16',
        '[174,175]':'[87,155]','V5122':'V5177',
        'no_rank_profession_ownership_or_kinship_inferred_from_polished_speech_or_laugh':'no_rank_profession_medical_role_or_relationship_inferred_from_concern_or_remedy_hearsay',
    }))
    shared={'B185':'B187','source_v5087/all8':'source_v5188/all16','voices_v5088':'voices_v5189'}
    rows.append(derive('scripts/prove_lil_B185_dispatches_v5089.py','scripts/prove_lil_B187_dispatches_v5190.py',{
        **shared,'dispatches_v5089':'dispatches_v5190','Bind16 source/current':'Bind32 source/current',
        'len(cases)==16':'len(cases)==32','all8_source_current':'all16_source_current',
        '16 source/current dispatches pass':'32 source/current dispatches pass',
    }))
    rows.append(derive('scripts/prove_lil_B185_entry_v5090.py','scripts/prove_lil_B187_entry_v5191.py',{
        **shared,'entry_v5090':'entry_v5191','in [185]':'in [187]',
    }))
    rows.append(derive('scripts/prove_lil_B185_controls_v5091.py','scripts/prove_lil_B187_controls_v5192.py',{
        **shared,'controls_v5091':'controls_v5192','blocks[185]':'blocks[187]','block=185':'block=187',
        "[(8,'00a0ffff013807a1'),(382,'00c2'),(384,'00000000')]":"[(8,'00a0ffff014e2fa1'),(672,'00c2'),(674,'00000000')]",
        'len(commands)==11 and len(blocks[0])==len(blocks[1])==388':'len(commands)==19 and len(blocks[0])==len(blocks[1])==680',
        'source_offset=382':'source_offset=672','source_declared_end_offsets=[384]':'source_declared_end_offsets=[674]',
    }))
    rows.append(derive('scripts/prove_lil_B185_names_v5092.py','scripts/prove_lil_B187_names_v5193.py',{
        **shared,'names_v5092':'names_v5193','[164,165]':'[87,155]',
    }))
    ROOT.mkdir(parents=True);save(ROOT/'prepared_current_source_native_contracts.json',dict(tools=rows,
        previous_goal_turn_classification='progress',previous_goal_turn_evidence='work/analysis/editorial_handoff_verification_v5183/verified_handoff.json',
        current_candidate='out/all_routes_combined_v5177_candidate.nds',clean_only_glosses_already_complete=16,
        expected_linear_commands=19,expected_control_leaves=3,source_stored_bytes=680,source_logical_end=678,source_tailzeros=2,
        original_actor_getter_CB184_and_all_existing_native_high_constants_and_multiplicities_preserved=True,
        no_predecessor_English_or_ROM_or_ledger_change=True,new_review_credit=0,full_goal_complete=False))
    print('Prepared B187 source mapping,207-name/voice binding,32 dispatches,event/C200 controls and four name consumers;no prose comparison or credit.')
