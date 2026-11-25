"""Correct only compiler API binding and source-locked compatibility imports;preserve v1 failure."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/Hodram_B49_atomic_fix_v8450')
if __name__=='__main__':
    assert not ROOT.exists();result=derive('dk4tool/patch/hodram_B49_editorial_v1.py','dk4tool/patch/hodram_B49_editorial_v2.py',{
        "encode_relocatable_dialogue(raw,row['english'],profile);qa=audit_relocatable_dialogue_record(raw,row['english'],profile)":"encode_relocatable_dialogue(raw,row['planned_English_markup'],profile);qa=audit_relocatable_dialogue_record(raw,row['planned_English_markup'],profile)",
        'hodram_outcomes_builder_guard_v4':'hodram_outcomes_builder_guard_v5',
        'Hodram_B49_release_paths_v8447':'Hodram_B49_release_paths_v8450',
    })
    ROOT.mkdir(parents=True);save(ROOT/'source_equivalence.json',dict(derivation=result,only_existing_validated_compiler_API_field_andexplicit_namespace_bindings_changed=True,approved_prose_all_source_current_final_refs_native_geometry_runtime_values_QA_andall_independent_evidence_checks_unchanged=True,failed_v1_andconfig1_andproducer8449_preserved=True,no_ROM_commit_registration_orcredit=True,new_credit=0,full_goal_complete=False))
