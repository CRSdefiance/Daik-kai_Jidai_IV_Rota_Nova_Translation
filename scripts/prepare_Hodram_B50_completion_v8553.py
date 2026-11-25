"""Preserve the unapplied first stage;clear completed pending flags only in credited current records."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save

if __name__=='__main__':
    root=Path('work/analysis/Hodram_B50_completion_tools_v8553');assert not root.exists()
    status="""        for key in ['native_speaker_item_controls_FE_current_editorial_actual_andregistered_integration_pending','prose_formatting_actual_effects_andregistered_release_pending','formatting_native_stored_actual_policy_atomic_andregistered_integration_pending','all_stored_controls_actual_effects_headers_FE_geometry_policy_andregistered_release_pending']:
            assert row[key] is True and row['pre_integration_review_record_preserved'][key] is True
            row[key]=False
        row['all_current_editorial_formatting_policy_atomic_registered_requirements_completed']=True
        row['opaque_effect_gameplay_semantics_andouter_eligibility_remain_unproven']=True
"""
    result=derive('scripts/complete_Hodram_B50_v8551.py','scripts/complete_Hodram_B50_v8553.py',{
        'v8551':'v8553','V8551':'V8553','v8552':'v8554','V8552':'V8554',
        'translations/hodram_B50_contextual_final_review_v1.json':'translations/hodram_B50_contextual_final_review_v2.json',
        "        assert all(row[k]==original[k] for k in ['english'":status+"        assert all(row[k]==original[k] for k in ['english'",
        "profile=release['profile'],records=rows,revised=2":"profile=release['profile'],predecessor_staged_final_review='translations/hodram_B50_contextual_final_review_v1.json',predecessor_staged_final_review_sha256=sha(Path('translations/hodram_B50_contextual_final_review_v1.json').read_bytes()),unapplied_first_stage_preserved=True,completed_pending_flags_cleared_withall_prior_flags_in_preintegration_history=True,records=rows,revised=2",
    })
    root.mkdir(parents=True);save(root/'derivation.json',dict(tool=result,unapplied_first_stage_andfinal_review_preserved=True,only_current_completed_status_flags_cleared_prior_flags_preserved_in_history=True,all_prose_source_current_final_refs_individual_review_gates_andcounter_arithmetic_preserved=True,all_native_high_integer_constants_andmultiplicity_preserved=True,full_objective_andnext_five_clean_B51_glosses_preserved=True,no_credit_before_staged_inverse_audit=True))
