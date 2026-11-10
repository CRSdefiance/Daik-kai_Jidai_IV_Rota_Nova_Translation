"""Derive the established full216px Hodram formatter and native glyph checks."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
if __name__=='__main__':
    root=Path('work/analysis/Hodram_B31_B53_layout_tools_v8724');assert not root.exists();tools=[]
    tools.append(derive('scripts/prove_Hodram_B52_logical_v8633.py','scripts/prove_Hodram_B31_B53_logical_v8724.py',{
        'scripts.Hodram_B51_registered_route_context_v8612':'scripts.Hodram_B52_registered_route_context_v8707',
        'Hodram_B52_logical_v8633':'Hodram_B31_B53_logical_v8724','hodram_B52_editorial_manuscript_v1':'hodram_B31_B53_editorial_manuscript_v1',
        'Hodram_B52_source_display_v8626/source_display.json':'Hodram_B31_B53_source_display_v8720/source_display_andbranch_paths.json',
        'current_V8609_Hodram_native_v8612':'current_V8704_Hodram_native_v8707','prefix in [113]':'prefix in [34,113]',
        'B52':'B31/B53','all_five_formatting_gates_remain_false':'all_three_formatting_gates_remain_false',
    }))
    tools.append(derive('scripts/plan_Hodram_B52_v8634.py','scripts/plan_Hodram_B31_B53_v8725.py',{
        'Hodram_B52_layout_v8634':'Hodram_B31_B53_layout_v8725','hodram_B52_editorial_manuscript_v1':'hodram_B31_B53_editorial_manuscript_v1',
        'Hodram_B52_logical_v8633':'Hodram_B31_B53_logical_v8724',"row['source_selector'] in [113]":"row['source_selector'] in [34,113]",
        "|{(\"hayreddin's\",'outfit'),('death','wish')}":"|{(\"hayreddin's\",'outfit'),('death','wish')}|{('will','you?'),('take','you'),('you','on'),('ottoman','empire'),(\"you'd\",'better')}",
        'Hodram B52 plan:':'Hodram B31/B53 plan:','Hodram-B52-RESEARCH-ONLY:':'Hodram-B31-B53-RESEARCH-ONLY:',
    }))
    tools.append(derive('scripts/prove_Hodram_B52_pages_v8635.py','scripts/prove_Hodram_B31_B53_pages_v8726.py',{
        'scripts.Hodram_B51_registered_route_context_v8612':'scripts.Hodram_B52_registered_route_context_v8707',
        'Hodram_B52_pages_v8635':'Hodram_B31_B53_pages_v8726','hodram_B52_editorial_manuscript_v1':'hodram_B31_B53_editorial_manuscript_v1',
        'Hodram_B52_layout_v8634':'Hodram_B31_B53_layout_v8725','Hodram_B52_logical_v8633':'Hodram_B31_B53_logical_v8724',
        'Hodram_B52_source_display_v8626/source_display.json':'Hodram_B31_B53_source_display_v8720/source_display_andbranch_paths.json',
        'current_V8609_Hodram_native_v8612':'current_V8704_Hodram_native_v8707',
        'B52':'B31/B53','; choices uncompiled.':'; no typed choices.',
        'all_five_formatting_gates_still_false':'all_three_formatting_gates_still_false',
    }))
    root.mkdir(parents=True);save(root/'derivations.json',dict(tools=tools,
        all_native_high_integer_constants_andmultiplicity_preserved=True,full216px_original_metrics_guards_pairphase_macrolengths_QA_andfontoracles_preserved=True,
        only_sourceactors34_and113_three_speeches_in_scope=True,no_authored_ordinary_breaks_padding_shortening_QA_weakening_orwaiver=True,
        original_coherent_pair_preference_additions_not_narrowed_viewport=True,
        no_ROM_registry_orcredit_change=True,new_credit=0,new_emulator_runs=0,full_goal_complete=False))
    print('Prepared source-locked logical/fullwidth/native-page successors;all original geometry,QA andnative addresses preserved.')
