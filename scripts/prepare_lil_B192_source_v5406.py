"""Bind linear tobacco-curiosity scene to verified V5396 before older English."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B192_source_tools_v5406')
if __name__=='__main__':
    assert not ROOT.exists()
    rows=[derive('scripts/map_lil_B188_source_v5232.py','scripts/map_lil_B192_source_v5406.py',{
        'B188':'B192','source_v5232':'source_v5406','editorial_handoff_verification_v5225':'editorial_handoff_verification_v5402','clean_context_v5231/all11':'clean_context_v5405/all8',
        'len(known)==6043':'len(known)==6101','blocks[188]':'blocks[192]','len(old)==14 and len(spoken)==11':'len(old)==11 and len(spoken)==8','[130,150,254]':'[115,153,254]','block=188':'block=192',
        'lil_B187_runs_v5221':'lil_B191_runs_v5398','physical_speeches=11':'physical_speeches=8','all11_clean_current_complete_context':'all8_clean_current_complete_context',
        'total_editorial_objects=11,speech_objects=11,ordinary_source_speeches=10':'total_editorial_objects=8,speech_objects=8,ordinary_source_speeches=7',
        'source_static_actor_selectors=[130,150],source_native_commands=14':'source_static_actor_selectors=[115,153],source_native_commands=11','all11_clean_first_glosses':'all8_clean_first_glosses',
        'B188 bound:11 complete speeches,14 linear commands,A000/C200/end;two source actors and current V5219 opening snapshot.':'B192 bound:8 complete speeches,11 linear commands,A000/C200/end;two source actors and current V5396 opening snapshot.',
    })]
    rows.append(derive('scripts/reconcile_lil_B191_voices_v5357.py','scripts/reconcile_lil_B192_voices_v5407.py',{
        'B191':'B192','voices_v5357':'voices_v5407','source_v5356/all13':'source_v5406/all8','[86,154]':'[115,153]','V5346':'V5396',
        'no_rank_kinship_employment_or_relationship_inferred_from_dye_pitch_or_oyajisan':'no_rank_kinship_age_or_relationship_inferred_from_stammering_or_tobacco_curiosity',
    }))
    rows.append(derive('scripts/prove_lil_B188_dispatches_v5234.py','scripts/prove_lil_B192_dispatches_v5408.py',{
        'B188':'B192','source_v5232/all11':'source_v5406/all8','voices_v5233':'voices_v5407','dispatches_v5234':'dispatches_v5408',
        'Bind22':'Bind16','len(cases)==22':'len(cases)==16','all11_source_current':'all8_source_current','22 source/current dispatches':'16 source/current dispatches',
    }))
    rows.append(derive('scripts/prove_lil_B191_entry_v5359.py','scripts/prove_lil_B192_entry_v5409.py',{
        'B191':'B192','source_v5356/all13':'source_v5406/all8','voices_v5357':'voices_v5407','entry_v5359':'entry_v5409','in [191]':'in [192]',
    }))
    rows.append(derive('scripts/prove_lil_B188_controls_v5236.py','scripts/prove_lil_B192_controls_v5410.py',{
        'B188':'B192','source_v5232/all11':'source_v5406/all8','voices_v5233':'voices_v5407','controls_v5236':'controls_v5410','blocks[188]':'blocks[192]','block=188':'block=192',
        "[(8,'00a0ffff01293ba1'),(476,'00c2'),(478,'00000000')]":"[(8,'00a0ffff012116a1'),(396,'00c2'),(398,'00000000')]",
        'len(commands)==14 and len(blocks[0])==len(blocks[1])==484':'len(commands)==11 and len(blocks[0])==len(blocks[1])==404',
        'source_offset=476':'source_offset=396','source_declared_end_offsets=[478]':'source_declared_end_offsets=[398]',
    }))
    rows.append(derive('scripts/prove_lil_B191_names_v5361.py','scripts/prove_lil_B192_names_v5411.py',{
        'B191':'B192','source_v5356/all13':'source_v5406/all8','voices_v5357':'voices_v5407','names_v5361':'names_v5411','[86,154]':'[115,153]',
    }))
    ROOT.mkdir(parents=True);save(ROOT/'prepared_current_source_native_contracts.json',dict(tools=rows,previous_goal_turn_classification='progress',
        previous_goal_turn_evidence='work/analysis/editorial_handoff_verification_v5402/verified_handoff.json',current_candidate='out/all_routes_combined_v5396_candidate.nds',
        source_commands=11,speeches=8,source_stored=404,source_logical=402,source_tailzeros=2,selectors_hex=['73','99'],selectors_decimal=[115,153],
        linear_no_predicate_or_relative_contract=True,no_predecessor_English_ROM_registry_or_credit_change=True,full_goal_complete=False))
