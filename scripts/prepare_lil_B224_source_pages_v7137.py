"""Measure native Japanese pages without assuming the letter scene's pagination."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text,derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B224_source_page_tools_v7137')
if __name__=='__main__':
    assert not ROOT.exists()
    a='scripts/prove_lil_B223_source_pages_v7087.py';b='scripts/prove_lil_B224_source_pages_v7137.py'
    c={'B223':'B224','source_pages_v7087':'source_pages_v7137','source_v7078/all17_clean_current_letter_notices_reactions_full1316_inverse':'source_v7130/fifteen_clean_current_Medusa_flirtation_exchange_source_references',
      "assert len(rows)==17 and sum(r['id']=='DK4_MES_B223_R0040' and len(r['pages'])==2 for r in rows)==1":"assert len(rows)==15 and all(r['pages'] for r in rows)",
      'all17_clean_objects_complete_native_CP932_pages_and_R40_two_page_sequence':'all15_clean_objects_complete_native_CP932_pages_and_exact_consumption',
      'complete_objects=17':'complete_objects=15',
      'source_R40_five_rows_on_two_original_pages=True':'source_original_page_counts={r[\'id\']:len(r[\'pages\']) for r in rows}',
      'source_signature_fullwidth_indentation_preserved_as_source_evidence_not_English_authoring=True':'all_original_Japanese_spacing_preserved_as_source_evidence_not_English_authoring=True',
      "source_objects=17,native_pages=len(pictures),R40_pages=len(next(r for r in rows if r['id']=='DK4_MES_B223_R0040')['pages'])":"source_objects=15,native_pages=len(pictures),page_counts=[len(r['pages']) for r in rows]",
      'Measure all complete clean letter/notice pages,including the five-row source paragraph.':'Measure every complete original Medusa-flirtation page and its exact native glyph sequence.'}
    assert not Path(b).exists();checked_text(Path(a).read_text('utf8'),c);row=derive(a,b,c)
    ROOT.mkdir(parents=True);save(ROOT/'source_locked_CP932_page_tool.json',dict(tool=row,strict2b6_independent_font_oracles_and_all_glyph_bounds_unchanged=True,no_source_pagination_assumption=True,new_credit=0,full_goal_complete=False))
