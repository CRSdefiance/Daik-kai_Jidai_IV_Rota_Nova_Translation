"""Bind actual227 fixture/plan while preserving copied226 disclaimer metadata as history."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B227_atomic_tools_v7320b')
if __name__=='__main__':
    assert not ROOT.exists()
    rows=[derive('dk4tool/patch/lil_B227_atomic_support_v1.py','dk4tool/patch/lil_B227_atomic_support_v2.py',{
        "'initialized_B22_not_natural_event227_original_location_earned_progress_full_effects_route_orhardware',":"'initialized_B22_not_natural_event226_original_location_earned_progress_full_effects_route_orhardware',",
        "    for p in a['actual_page_panels']:":"    plan=load(next(p for p in a['evidence'] if p.endswith('/run_plan.json')));fixture=load(a['fixture'])\n    require(plan['source_event227_not_naturally_selected'] and plan['displayed_original_source_block']==227 and fixture['fixtures'][0]['source_block']==227 and fixture['initialized_Amsterdam_B22_not_natural_event227_location_or_earned_progress'],'actual B227 entry scope independently bound;copied226 disclaimer label preserved for later metadata audit')\n    for p in a['actual_page_panels']:"}),
        derive('dk4tool/patch/lil_B227_editorial_v1.py','dk4tool/patch/lil_B227_editorial_v2.py',{'lil_B227_atomic_support_v1':'lil_B227_atomic_support_v2'}),
        derive('scripts/validate_lil_B227_atomic_v7321.py','scripts/validate_lil_B227_atomic_v7321b.py',{'lil_B227_editorial_v1':'lil_B227_editorial_v2','lil_B227_atomic_support_v1':'lil_B227_atomic_support_v2','lil_B227_atomic_v7321':'lil_B227_atomic_v7321b','lil_B227_atomic_tools_v7320':'lil_B227_atomic_tools_v7320b','prepare_lil_B227_atomic_v7320.py':'repair_lil_B227_atomic_scope_v7320b.py'})]
    ROOT.mkdir(parents=True);save(ROOT/'source_locked_atomic_compiler.json',dict(derivations=rows,original_positive_failure_before_archive_write_preserved=True,actual_B227_fixture_andrun_plan_scope_flags_now_independently_required=True,original_source_andEnglish_actual_copied_event226_disclaimer_metadata_preserved_for_later_older_record_technical_reaudit=True,no_dialogue_runtime_capture_orapproved_record_changed=True))
