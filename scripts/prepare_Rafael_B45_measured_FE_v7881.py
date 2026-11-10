"""Preserve the failed bitmap-width assumption; bind measured216px usable FE text width."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
if __name__=='__main__':
    root=Path('work/analysis/Rafael_B45_measured_FE_tools_v7881');assert not root.exists()
    results=[]
    results.append(derive('scripts/plan_Rafael_B45_layout_v7877.py','scripts/plan_Rafael_B45_layout_v7881.py',{
        'work/analysis/Rafael_B45_layout_v7877':'work/analysis/Rafael_B45_layout_v7881',
        "ADAPTER=checked_text(previous.ADAPTER,{":"""MEASUREMENT=Path('work/analysis/Rafael_B45_FE_boundary_v7880/32_FE_terminal_andbreak_pair_boundary_measurements.json')
measured=read(MEASUREMENT)
assert len(measured['cases'])==32 and measured['ARM9_sha256']==bound_ARM9 if False else True
final36=next(r for r in measured['cases'] if r['ascii_count']==36 and r['kind']=='final')
final37=next(r for r in measured['cases'] if r['ascii_count']==37 and r['kind']=='final')
phase36=next(r for r in measured['cases'] if r['ascii_count']==36 and r['kind']=='phase-space-guarded-LF')
assert [r['y'] for r in final36['rendered_rows']]==[0] and [r['y'] for r in final37['rendered_rows']]==[0,12]
assert phase36['rendered_rows'][1]==dict(y=12,text='  ')
def get_profile(row):
    return previous.replace(previous.get_profile(row),window_width_px=216)
base_qa=previous.FunctionType(previous.base_qa.__code__,{**previous.base_qa.__globals__,'get_profile':get_profile},argdefs=previous.base_qa.__defaults__)
ADAPTER=checked_text(checked_text(previous.ADAPTER,{"cells=38 if row['kind']=='system-FE' else 36":"cells=36"}),{""",
        "ENV={**previous.ENV,'BOUND_ZERO_SOURCE_BODIES':BOUND_ZERO_SOURCE_BODIES}":
        "assert len(measured['cases'])==32 and measured['ARM9_sha256']==bound['current_ARM9_sha256']\nENV={**previous.ENV,'BOUND_ZERO_SOURCE_BODIES':BOUND_ZERO_SOURCE_BODIES,'get_profile':get_profile}",
        "base_QA=previous.base_qa(planning,p),original_consumer_width_px=228 if row['kind']=='system-FE' else 216,":
        "base_QA=base_qa(planning,p),original_consumer_usable_text_width_px=216,original_consumer_bitmap_width_px=228 if row['kind']=='system-FE' else 216,",
        "source_owned_measured_profile=inspect.getsource(previous.get_profile),":
        "source_owned_base_measured_profile=inspect.getsource(previous.get_profile),source_owned_measured_usable_width_profile=inspect.getsource(get_profile),",
        "full_original_consumer_widths_no_global_font_profile_guard_orweak_rule_change=True,":
        "measured_FE_usable_text216_inside_original228_bitmap=True,boundary_measurement=str(MEASUREMENT),boundary_measurement_sha256=sha(MEASUREMENT.read_bytes()),no_global_font_profile_guard_orweak_rule_change=True,",
        "[MANUSCRIPT,LOGICAL,CURRENT,Path(previous.__file__),Path(__file__)]":
        "[MANUSCRIPT,LOGICAL,CURRENT,MEASUREMENT,Path(previous.__file__),Path(__file__)]",
    }))
    results.append(derive('scripts/prove_Rafael_B45_pages_v7878.py','scripts/prove_Rafael_B45_pages_v7882.py',{
        'work/analysis/Rafael_B45_pages_v7878':'work/analysis/Rafael_B45_pages_v7882',
        'work/analysis/Rafael_B45_layout_v7877/12_automatic_plans_full_native_width_zero_preamble_separate_body.json':
        'work/analysis/Rafael_B45_layout_v7881/12_automatic_plans_full_native_width_zero_preamble_separate_body.json',
    }))
    root.mkdir(parents=True);save(root/'provenance.json',dict(derivations=results,
        failed_page_producer='scripts/prove_Rafael_B45_pages_v7878.py',
        failed_painter_partial_planes_preserved='work/analysis/Rafael_B45_pages_v7878',
        forensic_failure='work/analysis/Rafael_B45_FE_diagnostic_v7879/FE_native_return_andcomplete_glyph_forensic_failure.json',
        measured_FE_terminal_limit36_cells_andpair_phase_extra_blank_row_at36=True,
        FE_bitmap228_not_usable_text_width=True,no_prose_command_viewport_orfont_change=True,
        original_all_glyph_canary_complete_return_code_andmacro_guards_preserved=True,new_credit=0,full_goal_complete=False))
