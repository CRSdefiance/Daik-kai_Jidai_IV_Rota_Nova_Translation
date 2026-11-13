"""Bind all fifteen clean cooking turns and original three-actor controls."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B193_source_tools_v5447')
if __name__=='__main__':
    assert not ROOT.exists()
    rows=[derive('scripts/map_lil_B192_source_v5406.py','scripts/map_lil_B193_source_v5447.py',{
        'B192':'B193','source_v5406':'source_v5447','verification_v5402':'verification_v5443','clean_context_v5405/all8':'clean_context_v5446/all15',
        'len(known)==6101':'len(known)==6109','blocks[192]':'blocks[193]','len(old)==11 and len(spoken)==8':'len(old)==18 and len(spoken)==15',
        '[115,153,254]':'[166,167,168,254]','[115,153]':'[166,167,168]','block=192':'block=193','lil_B191_runs_v5398':'lil_B192_runs_v5439',
        'physical_speeches=8':'physical_speeches=15','all8':'all15','total_editorial_objects=8,speech_objects=8,ordinary_source_speeches=7':'total_editorial_objects=15,speech_objects=15,ordinary_source_speeches=14',
        'source_native_commands=11':'source_native_commands=18','B192 bound:8 complete speeches,11 linear commands,A000/C200/end;two source actors and current V5396 opening snapshot.':
        'B193 bound:15 complete speeches,18 linear commands,A000/C200/end;three source actors and current V5437 opening snapshot.'})]
    rows.append(derive('scripts/reconcile_lil_B189_voices_v5274b.py','scripts/reconcile_lil_B193_voices_v5448.py',{
        'B189':'B193','voices_v5274b':'voices_v5448','source_v5273b/all17':'source_v5447/all15','[82,104,113,147]':'[166,167,168]',
        'len(fresh)==4':'len(fresh)==3','fresh4_actor_names':'fresh3_actor_names','four_source_selectors':'three_source_selectors','four B189 actors':'three B193 actors','V5263':'V5437',
        'no_rank_kinship_profession_or_relationship_inferred_from_collecting_or_sales_register':'no_rank_class_marriage_or_kinship_inferred_from_genteel_cooking_register'}))
    rows.append(derive('scripts/prove_lil_B192_dispatches_v5408.py','scripts/prove_lil_B193_dispatches_v5449.py',{
        'B192':'B193','source_v5406/all8':'source_v5447/all15','voices_v5407':'voices_v5448','dispatches_v5408':'dispatches_v5449',
        'Bind16':'Bind30','len(cases)==16':'len(cases)==30','all8_source_current':'all15_source_current','16 source/current dispatches':'30 source/current dispatches',
        'all2_static_actors':'all3_static_actors','two static actors':'three static actors'}))
    rows.append(derive('scripts/prove_lil_B192_entry_v5409.py','scripts/prove_lil_B193_entry_v5450.py',{
        'B192':'B193','source_v5406/all8':'source_v5447/all15','voices_v5407':'voices_v5448','entry_v5409':'entry_v5450','in [192]':'in [193]'}))
    rows.append(derive('scripts/prove_lil_B192_controls_v5410.py','scripts/prove_lil_B193_controls_v5451.py',{
        'B192':'B193','source_v5406/all8':'source_v5447/all15','voices_v5407':'voices_v5448','controls_v5410':'controls_v5451','blocks[192]':'blocks[193]','block=192':'block=193',
        "[(8,'00a0ffff012116a1'),(396,'00c2'),(398,'00000000')]":"[(8,'00a0ffff011d39a1'),(660,'00c2'),(662,'00000000')]",
        'len(commands)==11 and len(blocks[0])==len(blocks[1])==404':'len(commands)==18 and len(blocks[0])==len(blocks[1])==668',
        'source_offset=396':'source_offset=660','source_declared_end_offsets=[398]':'source_declared_end_offsets=[662]'}))
    rows.append(derive('scripts/prove_lil_B189_names_v5278b.py','scripts/prove_lil_B193_names_v5452.py',{
        'B189':'B193','source_v5273b/all17':'source_v5447/all15','voices_v5274b':'voices_v5448','names_v5278b':'names_v5452','[82,104,113,147]':'[166,167,168]',
        'four_source_selectors':'three_source_selectors','source-four-name-consumers':'source-three-name-consumers',"len(native['rows'])==8":"len(native['rows'])==6",
        'fresh4_actor_names':'fresh3_actor_names','eight_original':'six_original','native_eight_consumer_cases':'native_six_consumer_cases','Eight source-owned':'Six source-owned'}))
    ROOT.mkdir(parents=True);save(ROOT/'prepared_current_source_native_contracts.json',dict(tools=rows,previous_goal_turn_classification='progress',
        previous_goal_turn_evidence='work/analysis/editorial_handoff_verification_v5443/verified_handoff.json',current_candidate='out/all_routes_combined_v5437_candidate.nds',
        source_commands=18,speeches=15,source_stored=668,source_logical=666,source_tailzeros=2,selectors_hex=['A6','A7','A8'],selectors_decimal=[166,167,168],
        linear_no_predicate_or_relative_contract=True,no_predecessor_English_ROM_registry_or_credit_change=True,full_goal_complete=False))
