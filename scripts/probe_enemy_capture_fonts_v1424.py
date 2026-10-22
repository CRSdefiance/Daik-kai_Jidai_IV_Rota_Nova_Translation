"""Refined prose:distinguish a complete runtime name from an orphan predicate."""
import inspect
from pathlib import Path
from scripts import probe_enemy_capture_fonts_v1420 as previous

if __name__=='__main__':
    source = Path(previous.__file__).read_text(encoding='utf-8')
    old = """            if len(lines)>1 and len(lines[-1].split())==1:
                issues.append('single-word-final-line-needs-editorial-layout-decision')"""
    new = """            atomic_name_row = len(lines)>1 and lines[-1]==name.decode('cp932')+'!' and len(name)>=8
            if len(lines)>1 and len(lines[-1].split())==1 and not atomic_name_row:
                issues.append('isolated-non-name-final-word')"""
    assert source.count(old)==1
    source = source.replace(old,new)
    old = "'weak_line_end_indices':weak,'full228x64_native_and_independent_font_exact':True,"
    new = """'weak_line_end_indices':weak,'full228x64_native_and_independent_font_exact':True,
                'complete_atomic_runtime_ship_name_on_final_row':atomic_name_row,
                'atomic_name_review_reason':'A complete runtime proper name is the grammatical object of the preceding complete report;all name bytes and punctuation remain together. It is not an orphan predicate,fragment or missing text.' if atomic_name_row else None,"""
    assert source.count(old)==1
    source = source.replace(old,new)
    for old,new in [
        ("'work/analysis/enemy_capture_fonts_v1420'","'work/analysis/enemy_capture_fonts_v1424'"),
        ("'work/analysis/enemy_capture_payload_v1419/native_payload_plan.json'","'work/analysis/enemy_capture_payload_v1423/native_payload_plan.json'"),
        ("'translations/enemy_capture_editorial_manuscript_v1.json'","'translations/enemy_capture_editorial_manuscript_v2.json'"),
        ("'visual_review_layout_refinement_registered_release_and_original_gameplay_still_pending':True,",
         "'visual_review_registered_release_and_original_gameplay_still_pending':True,'atomic_runtime_name_rows_separately_classified':True,")]:
        assert source.count(old)==1,old
        source = source.replace(old,new)
    exec(compile(source,__file__,'exec'),{**globals(),'__name__':'__main__'})
