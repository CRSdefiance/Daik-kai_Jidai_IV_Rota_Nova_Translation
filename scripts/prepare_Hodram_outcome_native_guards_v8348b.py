"""Preserve passing v1; add explicit frozen source-adapter identity before any native adapter executes."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
if __name__=='__main__':
    root=Path('work/analysis/Hodram_outcome_native_guard_tools_v8348b');assert not root.exists();tools=[]
    tools.append(derive('dk4tool/patch/hodram_outcomes_native_evidence_v1.py','dk4tool/patch/hodram_outcomes_native_evidence_v2.py',{
        'from scripts.Hodram_FE_font_oracles_v8315 import bind':'from scripts.Hodram_FE_font_oracles_v8315 import bind\nfrom dk4tool.patch.hodram_outcomes_native_guards_v1 import trusted_adapter',
        "page_adapter=data['pages']['source_owned_target_page_adapter'];":"page_adapter=trusted_adapter('pages',data['pages']['source_owned_target_page_adapter']);",
    }))
    tools.append(derive('scripts/validate_Hodram_outcome_actual_evidence_v8349.py','scripts/validate_Hodram_outcome_actual_evidence_v8349b.py',{
        'hodram_outcomes_native_evidence_v1':'hodram_outcomes_native_evidence_v2',
        'Hodram_outcome_actual_evidence_v8349':'Hodram_outcome_actual_evidence_v8349b',
    }))
    root.mkdir(parents=True);save(root/'trusted_adapter_identity_successor.json',dict(tools=tools,
        passing_native_v1_andactual_v1_results_preserved=True,frozen_native_adapter_guard_independent_of_release_dependency_check_bypass=True,
        no_native_address_font_oractual_input_change=True,new_credit=0,full_goal_complete=False))
