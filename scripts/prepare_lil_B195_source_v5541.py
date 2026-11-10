"""Bind all20 clean cheese-specialty turns and source-owned native consumers."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save

ROOT=Path('work/analysis/lil_B195_source_tools_v5541')
if __name__=='__main__':
    assert not ROOT.exists()
    rows=[derive('scripts/map_lil_B193_source_v5447.py','scripts/map_lil_B195_source_v5541.py',{
        'B193':'B195','source_v5447':'source_v5541','verification_v5443':'verification_v5537','clean_context_v5446/all15':'clean_context_v5540/all20',
        'len(known)==6109':'len(known)==6135','blocks[193]':'blocks[195]','len(old)==18 and len(spoken)==15':'len(old)==23 and len(spoken)==20',
        '[166,167,168,254]':'[92,103,119,254]','[166,167,168]':'[92,103,119]','block=193':'block=195','lil_B192_runs_v5439':'lil_B194_runs_v5533',
        'physical_speeches=15':'physical_speeches=20','all15':'all20','total_editorial_objects=15,speech_objects=15,ordinary_source_speeches=14':
        'total_editorial_objects=20,speech_objects=20,ordinary_source_speeches=19','source_native_commands=18':'source_native_commands=23',
        'B193 bound:15 complete speeches,18 linear commands,A000/C200/end;three source actors and current V5437 opening snapshot.':
        'B195 bound:20 complete speeches,23 linear commands,A000/C200/end;three source actors and current V5531 opening snapshot.'})]
    rows.append(derive('scripts/reconcile_lil_B193_voices_v5448.py','scripts/reconcile_lil_B195_voices_v5542.py',{
        'B193':'B195','voices_v5448':'voices_v5542','source_v5447/all15':'source_v5541/all20','[166,167,168]':'[92,103,119]','V5437':'V5531',
        'no_rank_class_marriage_or_kinship_inferred_from_genteel_cooking_register':'no_kinship_rank_employment_or_named_dish_inferred_from_familiar_food_banter'}))
    rows.append(derive('scripts/prove_lil_B193_dispatches_v5449.py','scripts/prove_lil_B195_dispatches_v5543.py',{
        'B193':'B195','source_v5447/all15':'source_v5541/all20','voices_v5448':'voices_v5542','dispatches_v5449':'dispatches_v5543',
        'Bind30':'Bind40','len(cases)==30':'len(cases)==40','all15_source_current':'all20_source_current','30 source/current dispatches':'40 source/current dispatches'}))
    rows.append(derive('scripts/prove_lil_B193_entry_v5450.py','scripts/prove_lil_B195_entry_v5544.py',{
        'B193':'B195','source_v5447/all15':'source_v5541/all20','voices_v5448':'voices_v5542','entry_v5450':'entry_v5544','in [193]':'in [195]'}))
    rows.append(derive('scripts/prove_lil_B193_controls_v5451.py','scripts/prove_lil_B195_controls_v5545.py',{
        'B193':'B195','source_v5447/all15':'source_v5541/all20','voices_v5448':'voices_v5542','controls_v5451':'controls_v5545','blocks[193]':'blocks[195]','block=193':'block=195',
        'from scripts.prove_lil_B180_C200_v4784 import':'from scripts.prove_lil_B190_C200_v5318 import',
        "[(8,'00a0ffff011d39a1'),(660,'00c2'),(662,'00000000')]":"[(8,'00a0ffff010841a1'),(704,'00c2'),(706,'00000000')]",
        'len(commands)==18 and len(blocks[0])==len(blocks[1])==668':'len(commands)==23 and len(blocks[0])==len(blocks[1])==712',
        'source_offset=660':'source_offset=704','source_declared_end_offsets=[662]':'source_declared_end_offsets=[706]'}))
    rows.append(derive('scripts/prove_lil_B193_names_v5452.py','scripts/prove_lil_B195_names_v5546.py',{
        'B193':'B195','source_v5447/all15':'source_v5541/all20','voices_v5448':'voices_v5542','names_v5452':'names_v5546','[166,167,168]':'[92,103,119]'}))
    ROOT.mkdir(parents=True);save(ROOT/'prepared_current_source_native_contracts.json',dict(tools=rows,
        previous_goal_turn_classification='progress',previous_goal_turn_evidence='work/analysis/editorial_handoff_verification_v5537/verified_handoff.json',
        current_candidate='out/all_routes_combined_v5531_candidate.nds',source_commands=23,speeches=20,
        source_stored=712,source_logical=710,source_tailzeros=2,selectors_hex=['5C','67','77'],selectors_decimal=[92,103,119],
        linear_no_predicate_relative_or_macro_contract=True,source_owned_fleet_descriptor_C200_adapter_used=True,
        no_predecessor_English_ROM_registry_or_credit_change=True,full_goal_complete=False))
