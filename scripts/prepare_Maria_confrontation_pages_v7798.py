"""Freeze complete guarded native pages againstthe macro-order-correct v2 prose."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
if __name__=='__main__':
    root=Path('work/analysis/maria_confrontation_page_tools_v7798');assert not root.exists()
    d=derive('scripts/prove_Maria_confrontation_pages_v7794.py','scripts/prove_Maria_confrontation_pages_v7798.py',{
        'maria_confrontation_pages_v7794':'maria_confrontation_pages_v7798',
        'translations/maria_B36_editorial_manuscript_v1.json':'translations/maria_B36_editorial_manuscript_v2.json',
        'work/analysis/maria_confrontation_layout_v7793/16_automatic_full_width_plans_all_base_QA_preserved.json':
        'work/analysis/maria_confrontation_intro_v7796/16_complete_automatic_plans_original_macro_order_preserved.json',
    })
    root.mkdir(parents=True);save(root/'provenance.json',dict(derivation=d,
        all_original_native_numbers_glyph_bounds_canaries_consumption_andpage_guards_preserved=True,
        no_failed_7793_plan_overwritten_orwaived=True,new_credit=0,full_goal_complete=False))
