"""Correct only the logical markup/token comparison; preserve the executed first producer."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B213_completion_fix_v6691b')
if __name__=='__main__':
    assert not ROOT.exists() and not Path('work/analysis/lil_B213_completion_v6691').exists() and not Path('translations/lil_B213_contextual_final_review_v1.json').exists()
    proof=derive('scripts/complete_lil_B213_v6691.py','scripts/complete_lil_B213_v6691b.py',{"row['english'].split('}',1)[1]":"row['english'].split('}',1)[1].replace('{MACRO:FI}','FI')"})
    ROOT.mkdir(parents=True);save(ROOT/'source_locked_correction.json',dict(derivation=proof,original_staging_stopped_before_any_shared_ledger_document_or_credit_change=True,only_explicit_source_FI_markup_to_native_token_comparison_corrected=True,ROM_prose_controls_macro_and_release_evidence_unchanged=True,full_goal_complete=False))
