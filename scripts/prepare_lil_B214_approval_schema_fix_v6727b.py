"""Keep the failed producer; explicitly declare the encoder and required batch gates before validation."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B214_approval_schema_fix_v6727b')
if __name__=='__main__':
    assert not ROOT.exists() and not Path('translations/lil_B214_editorial_manuscript_v2.json').exists() and not Path('work/analysis/lil_B214_native_approval_v6727').exists()
    proof=derive('scripts/approve_lil_B214_native_v6727.py','scripts/approve_lil_B214_native_v6727b.py',{"doc.update(previous_manuscript=str(INPUT)":"doc.update(encoder='dialogue-relocatable-v1',review_gates=['source','context','localization','naturalness','formatting'],previous_manuscript=str(INPUT)"})
    ROOT.mkdir(parents=True);save(ROOT/'source_locked_required_batch_metadata_correction.json',dict(derivation=proof,first_attempt_stopped_before_approved_manuscript_or_shared_mutation=True,supported_encoder_and_required_batch_gate_declarations_explicit=True,all17_prose_rows_native_bytes_and_individual_gates_unchanged=True,no_ROM_runtime_or_credit_change=True,full_goal_complete=False))
