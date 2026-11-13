"""Bind final B50 dispatches/item/hide/complete end using preserved source-owned native adapters."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/Hodram_B50_control_tools_v8497')
if __name__=='__main__':
    assert not ROOT.exists();result=derive('scripts/prove_Hodram_B49_controls_v8401d.py','scripts/prove_Hodram_B50_controls_v8497.py',{
        'scripts.Hodram_outcomes_registered_route_context_v8380':'scripts.Hodram_B49_registered_route_context_v8478',
        'Hodram_B49_controls_v8401d':'Hodram_B50_controls_v8497','Hodram_B49_relocation_v8398':'Hodram_B50_relocation_v8495','work/analysis/Hodram_B49_choice_binding_v8387b/current_with_choices.json':'work/analysis/Hodram_B50_current_v8488/current_effective.json',
        'Hodram_B49_source_controls_v8384':'Hodram_B50_source_controls_v8486','Hodram_B49_source_display_v8386b':'Hodram_B50_source_display_v8487','Hodram_B49_stored_v8399':'Hodram_B50_stored_v8496','current_V8377_Hodram_native_v8380':'current_V8475_Hodram_native_v8478',
        "    for before,after,cm in zip(":"    assert not any(c['word'] in [0x100,0x200,0x300,0x400,0x8000,0x8100,0x2100] for c in g['all_target_commands'])\n    for before,after,cm in zip(",
        'len(dispatches)==14':'len(dispatches)==3','len(queries)==1 and len(pictures)==4 and len(controls)==13':'len(queries)==0 and len(pictures)==2 and len(controls)==9',
        '[0x4820,0x4700,0x4800,0x4700]':'[0x4800,0x4700]',
        "len(g['relative_fixups'])==8 and sum(len(r['cases']) for r in g['relocated_skip_cases'])==40":"not g['relative_fixups'] and not queries",
        "relocated_relative_cases=g['relocated_skip_cases']":"relocated_relative_cases=[]",
        'all14_source_actors_voices_full_preambles_stored_bodies_andoriginal_null_FE_exact':'all3_source_actors_voices_full_preambles_stored_bodies_andoriginal_null_FE_exact',
        'original_item148_descriptors_distinct_layouts_andhide_boundaries_exact':'original_item148_layout0_andhide_boundaries_exact','seven_opaque_effects_preserved_without_claiming_gameplay_semantics':'six_opaque_effects_preserved_without_claiming_gameplay_semantics',
        'source_query_raw_result_not_boolean_orinventory_award':'source_has_no_query_orchoice_andno_inventory_award_semantics_claim',
        'all8_relative_sites40_cases_and25_normal_value_carries_pass':'no_relative_orquery_sites_and25_normal_value_carries_pass',
        'actual_scene_resource_effect_bodies_eligibility_menu_selection_andFE_transition_pending':'actual_scene_resource_effect_bodies_eligibility_andFE_transition_pending',
        'B49 stored controls:14 dispatches/one null FE,40 relocated branch cases,one unchanged raw query,four picture/hide boundaries,25 normal value-carry cases pass.No actual effect oractivation claim.':'B50storedcontrols:3dispatches/one nullFE/no relative-query-choice sites/two originalitem148show-hide boundaries/25normalvaluecarryends pass.Exacthide r3pointerdelta preserved.Noactualeffect oractivation claim.',
    })
    ROOT.mkdir(parents=True);save(ROOT/'derivation.json',dict(derivation=result,all_native_addresses_constants_andmultiplicity_preserved=True,all_original_full_dispatch_macro_preamble_picture_descriptor_layout_andhide_pointer_delta_checks_preserved=True,no_new_ROM_registered_stage_orcredit=True,new_credit=0,full_goal_complete=False))
