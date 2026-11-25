"""Use the final plan and latest exact-reuse selection for remaining whole exchanges."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(Path('scripts/stage_maria328_review_sheets_v1.py').read_text(encoding='utf-8'),{
    "plan_visual_v4/automatic_plans.json":"plan_visual_v6/automatic_plans.json",
    "native_final_selection_v1.json":"native_final_selection_v2.json",
    "selected_review_sheets_v1":"selected_review_sheets_v2",
    "freshpath=ROOT/f'native_final_v1/B{block}_checked.json'":"freshpath=ROOT/f'native_final_v2/B{block}_checked.json'",
    "journal=ROOT/('native_final_v1/complete_'+row['id']+'.json')":"journal=ROOT/('native_final_v2/complete_'+row['id']+'.json')",
})
if __name__=='__main__':exec(compile(source,__file__+'::same-source-bound-staging-latest-inputs','exec'),globals())
