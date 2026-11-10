"""Derive source-exact whole-loader andcaller bindings before whole-scene fixtures."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/Hodram_B50_reference_tools_v8503')
if __name__=='__main__':
    assert not ROOT.exists();results=[]
    results.append(derive('scripts/verify_Hodram_B49_loaders_v8404.py','scripts/verify_Hodram_B50_loaders_v8503.py',{
        'scripts.create_Hodram_B49_reference_v8403':'scripts.create_Hodram_B50_reference_v8502','Hodram_B49_reference_v8403':'Hodram_B50_reference_v8502','Hodram_B49_loaders_v8404':'Hodram_B50_loaders_v8503',
    }))
    source=Path('scripts/verify_Hodram_B49_references_v8405b.py').read_text('utf8')
    insert='''    manuscript=read('translations/hodram_B50_editorial_manuscript_v3.json')
    for ref in b['text_records']:
        row=next(r for r in manuscript['records'] if r['id']==ref['id'])
        ref.update(source_reference=row['source_reference'],current_reference=row['current_reference'],source_selector=row['source_selector'],source_complete_preamble_hex=row['source_complete_preamble_hex'])
    b['all_source_commands']=a['all_source_commands'];b['relocated_skip_cases']=[]
    qualified={**mapping,'groups':[b],'external_references_complete':True,'source_current_final_references_complete':True}
    qualified_path=ROOT/'source_current_final_map.json';save(qualified_path,qualified)
'''
    results.append(derive('scripts/verify_Hodram_B49_references_v8405b.py','scripts/verify_Hodram_B50_references_v8503.py',{
        'Hodram_B49_references_v8405b':'Hodram_B50_references_v8503','Hodram_B49_reference_v8403':'Hodram_B50_reference_v8502','work/analysis/Hodram_B49_choice_binding_v8387b/current_with_choices.json':'work/analysis/Hodram_B50_current_v8488/current_effective.json','Hodram_B49_relocation_v8398':'Hodram_B50_relocation_v8495','Hodram_B49_loaders_v8404':'Hodram_B50_loaders_v8503','Hodram_B49_controls_v8401d':'Hodram_B50_controls_v8497',
        'block=bank[49]':'block=bank[50]','len(maps)==36':'len(maps)==12',"len(b['relative_fixups'])==8 and sum(len(r['cases']) for r in b['relocated_skip_cases'])==40":"not b['relative_fixups']",
        "r['native_selected_block']==49":"r['native_selected_block']==50",'[(49,49,[48])]':'[(50,50,[49])]',"len(controls['final_dispatches'])==14":"len(controls['final_dispatches'])==3",
        "ROOT.mkdir(parents=True);save(ROOT/'references.json'":"ROOT.mkdir(parents=True)\n"+insert+"    save(ROOT/'references.json'",
        'block=49':'block=50',"relocated_native_skip_cases=b['relocated_skip_cases']":"relocated_native_skip_cases=[]",'all14_text_records':'all3_text_records',"typed_choice_records=b['choice_commands']":"typed_choice_records=[]",
        'all36_commands14_full_preambles8_relatives2_choices_query_picture_hide_effects_andterminal_bound':'all12_commands3_full_preambles_source_FE_item_hide_effects_terminal_andtails_bound',
        'event49_requires48_not_natural_eligibility_location_orfull_chronology_proof':'event50_requires49_not_natural_eligibility_location_orfull_chronology_proof',
        'actual_B49_backing_controller_transitions_policy_atomic_registered_release_pending':'actual_B50_FE_header_palette_item_transition_policy_atomic_registered_release_pending',
        'B49:36 command maps/8 relative sites40cases/14 speeches2choices,originalEV1entry,325load-cache/650modes andfresh shipped-code census pass.Actual UI/policy/release pending.':'B50:12commandmaps/3preambles/zero relative-query-choice sites,originalEV1entry/325load-cache650modes/fresh shippedcodecensus pass. ActualFEheader/itemtransition/policy/release pending.',
    }))
    ROOT.mkdir(parents=True);save(ROOT/'derivations.json',dict(derivations=results,all_original_native_addresses_sizes_limits_andmultiplicity_preserved=True,only_completeB50_sourcequalified_scope_bound=True,no_new_ROM_capture_orcredit_by_preparer=True,new_credit=0,full_goal_complete=False))
