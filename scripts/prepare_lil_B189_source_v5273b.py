"""Bind the complete two-pair ceramics scene to verified V5263 before old prose."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B189_source_tools_v5273b')
if __name__=='__main__':
    assert not ROOT.exists()
    rows=[derive('scripts/map_lil_B188_source_v5232.py','scripts/map_lil_B189_source_v5273b.py',{
        'B188':'B189','source_v5232':'source_v5273b','editorial_handoff_verification_v5225':'editorial_handoff_verification_v5269',
        'clean_context_v5231/all11':'clean_context_v5272b/all17','len(known)==6043':'len(known)==6054','blocks[188]':'blocks[189]',
        'len(old)==14 and len(spoken)==11':'len(old)==20 and len(spoken)==17','[130,150,254]':'[82,104,113,147,254]','block=188':'block=189',
        'lil_B187_runs_v5221':'lil_B188_runs_v5265','physical_speeches=11':'physical_speeches=17','all11_clean_current_complete_context':'all17_clean_current_complete_context',
        'total_editorial_objects=11,speech_objects=11,ordinary_source_speeches=10':'total_editorial_objects=17,speech_objects=17,ordinary_source_speeches=16',
        'source_static_actor_selectors=[130,150],source_native_commands=14':'source_static_actor_selectors=[82,104,113,147],source_native_commands=20',
        'all11_clean_first_glosses':'all17_clean_first_glosses',
        'B188 bound:11 complete speeches,14 linear commands,A000/C200/end;two source actors and current V5219 opening snapshot.':
        'B189 bound:17 complete speeches,20 linear commands,A000/C200/end;four source actors and current V5263 opening snapshot.',
    })]
    rows.append(derive('scripts/reconcile_lil_B188_voices_v5233.py','scripts/reconcile_lil_B189_voices_v5274b.py',{
        'B188':'B189','voices_v5233':'voices_v5274b','source_v5232/all11':'source_v5273b/all17','[130,150]':'[82,104,113,147]','len(fresh)==2':'len(fresh)==4',
        'the two B188 actors':'the four B189 actors','V5219':'V5263','fresh2_actor_names':'fresh4_actor_names','two_source_selectors':'four_source_selectors',
        'no_rank_age_profession_or_relationship_inferred_from_archaic_or_deferential_register':'no_rank_kinship_profession_or_relationship_inferred_from_collecting_or_sales_register',
    }))
    shared={'B188':'B189','source_v5232/all11':'source_v5273b/all17','voices_v5233':'voices_v5274b'}
    rows.append(derive('scripts/prove_lil_B188_dispatches_v5234.py','scripts/prove_lil_B189_dispatches_v5275b.py',{
        **shared,'dispatches_v5234':'dispatches_v5275b','Bind22 source/current':'Bind34 source/current','len(cases)==22':'len(cases)==34',
        'all11_source_current':'all17_source_current','all2_static_actors':'all4_static_actors','22 source/current dispatches pass:two static actors':'34 source/current dispatches pass:four static actors',
    }))
    rows.append(derive('scripts/prove_lil_B188_entry_v5235.py','scripts/prove_lil_B189_entry_v5276b.py',{
        **shared,'entry_v5235':'entry_v5276b','in [188]':'in [189]',
    }))
    rows.append(derive('scripts/prove_lil_B188_controls_v5236.py','scripts/prove_lil_B189_controls_v5277b.py',{
        **shared,'controls_v5236':'controls_v5277b','blocks[188]':'blocks[189]','block=188':'block=189',
        "[(8,'00a0ffff01293ba1'),(476,'00c2'),(478,'00000000')]":"[(8,'00a0ffff012a05a1'),(764,'00c2'),(766,'00000000')]",
        'len(commands)==14 and len(blocks[0])==len(blocks[1])==484':'len(commands)==20 and len(blocks[0])==len(blocks[1])==772',
        'source_offset=476':'source_offset=764','source_declared_end_offsets=[478]':'source_declared_end_offsets=[766]',
    }))
    rows.append(derive('scripts/prove_lil_B188_names_v5237.py','scripts/prove_lil_B189_names_v5278b.py',{
        **shared,'names_v5237':'names_v5278b','[130,150]':'[82,104,113,147]','two_source_selectors':'four_source_selectors','fresh2_actor_names':'fresh4_actor_names',
        'source-two-name-consumers':'source-four-name-consumers',"len(native['rows'])==4":"len(native['rows'])==8",'native_four_consumer_cases':'native_eight_consumer_cases',
        'four_original_progressive_and_catalogue_name_consumers':'eight_original_progressive_and_catalogue_name_consumers','Four source-owned name consumers':'Eight source-owned name consumers',
    }))
    ROOT.mkdir(parents=True);save(ROOT/'prepared_current_source_native_contracts.json',dict(tools=rows,
        previous_goal_turn_classification='progress',previous_goal_turn_evidence='work/analysis/editorial_handoff_verification_v5269/verified_handoff.json',
        current_candidate='out/all_routes_combined_v5263_candidate.nds',clean_only_glosses_already_complete=17,
        expected_linear_commands=20,expected_control_leaves=3,source_stored_bytes=772,source_logical_end=770,source_tailzeros=2,
        four_source_actors_eight_name_consumers_and_original_voices_required=True,
        original_actor_getter_CB184_and_all_existing_native_high_constants_and_multiplicities_preserved=True,
        no_predecessor_English_or_ROM_or_ledger_change=True,new_review_credit=0,full_goal_complete=False))
