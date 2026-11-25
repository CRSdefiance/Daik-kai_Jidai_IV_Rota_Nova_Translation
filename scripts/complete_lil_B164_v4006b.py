"""Preserve the completion draft;clear inherited typed-choice pending flags after actual selection."""
from pathlib import Path
if __name__=='__main__':
    draft=Path('scripts/complete_lil_B164_v4006.py');text=draft.read_text(encoding='utf-8');needle='actual_advice_choice_result_observed=True if choice else None,';assert text.count(needle)==1;text=text.replace(needle,needle+'actual_choice_selection_still_pending=False,current_native_typed_choice_font_reference_and_outcome_binding_pending=False,');assert text.count('proofpaths=[')==1;text=text.replace('proofpaths=[','proofpaths=[DRAFT,');exec(compile(text,__file__,'exec'),dict(__name__='__main__',__file__=__file__,DRAFT=draft))
