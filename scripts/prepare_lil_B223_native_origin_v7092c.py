"""Distinguish the first page from an exact compiler-guard continuation; preserve all glyph tests."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save,read
from dk4tool.patch.grand_race_menu_release import sha
ROOT=Path('work/analysis/lil_B223_native_origin_tools_v7092c')
PROOF=Path('work/analysis/lil_B223_continuation_origin_v7092b/R31_page2_source_guard_space_and_complete_first_f_at6.json')
if __name__=='__main__':
    assert not ROOT.exists();proof=read(PROOF);assert proof['both_original_failed_plane_files_pixel_equal_to_independent_research'] and proof['no_runtime_font_guard_geometry_prose_or_QA_change']
    old="assert page['first_visible_origin']==[0,0]"
    new="leading=len(body[page['start']:page['end']])-len(body[page['start']:page['end']].lstrip(b' '));assert leading==(0 if page['page']==1 else 1) and page['first_visible_origin']==[leading*6,0] and (page['page']==1 or body[page['start']-1:page['start']+1]==b'\\n ');page.update(compiler_owned_page_continuation_guard_bytes=leading,exact_first_visible_origin_verified_without_font_or_bounds_change=True)"
    tool=derive('scripts/verify_lil_B223_native_pages_v7092.py','scripts/verify_lil_B223_native_pages_v7092c.py',{'native_pages_v7092':'native_pages_v7092c',old:new})
    ROOT.mkdir(parents=True);save(ROOT/'source_locked_first_page_and_guarded_continuation_assertions.json',dict(tool=tool,focused_origin_proof=str(PROOF),focused_origin_proof_sha256=sha(PROOF.read_bytes()),all_native_numeric_addresses_geometry_font_metrics_guards_and_independent_masks_preserved=True,all17_paragraphs19_pages136_alignment_cases_still_required=True,failed_original_producer_and_partial_planes_preserved=True,no_global_QA_or_renderer_change=True,new_credit=0,full_goal_complete=False))
