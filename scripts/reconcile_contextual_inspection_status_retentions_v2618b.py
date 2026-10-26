"""Normalize the frozen literal-font schema from its explicit per-case guarantees."""
from pathlib import Path
from types import FunctionType
from scripts.reconcile_contextual_inspection_retentions_v2617 import reconcile as original
from scripts.verify_village_wrap_v608 import read as original_read
def read(path):
 value=original_read(path)
 if str(path).replace('\\','/')=='work/analysis/inspection_status_fonts_v2615/native_font_proof.json':
  assert 'findings'not in value and value['native_literal_modal_single_line_no_authored_breaks_or_cursor_patch']and len(value['cases'])==2
  value={**value,'findings':[dict(message_ID=c['message_ID'],finding='literal-font-contract-failed')for c in value['cases']if not(c['literal_modal_origin_x0_native_preserved']and c['complete_first_final_letters_single_line_bounds_and_blank_paper_pass']and c['full228x64_native_and_independent_font_equal'])]}
 return value
reconcile=FunctionType(original.__code__,{**original.__globals__,'read':read,'__file__':__file__},argdefs=original.__defaults__)
