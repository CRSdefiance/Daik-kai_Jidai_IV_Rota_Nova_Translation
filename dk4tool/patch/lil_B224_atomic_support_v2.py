"""Individual editorial obligations supplement the preserved exact-byte/palette gates."""
from dk4tool.patch.lil_B224_atomic_support_v1 import audit_sealed_scope as original_scope

def audit_sealed_scope(doc,mapping,seal,load,require):
    for key,count in dict(actual_objects=15,actual_pages=15,actual_complete_body_holds=59,actual_complete_name_holds=59,offline_only_objects=0).items():
        require(doc[key]==count,'manuscript coverage:'+key)
    require(doc['offline_only_object_IDs']==[],'no false offline list')
    for r in doc['records']:
        require(r['speaker']=={26:'Julian Lopes',197:'Safia'}[r['source_selector']],'exact original speaker without invented rank')
        require(all(isinstance(r[k],str) and r[k].strip() for k in ['context','source_meaning','localization_note','editorial_finding']),'individual contextual reasoning')
        require(r['native_profile_maximum_total_rows']==r['original_physical_native_rows_per_page']==4 and r['native_page_count']==1,'original physical geometry')
    font=load(doc['native_font_proof']);stored=load(doc['native_stored_proof']);policy=load(doc['native_policy_validation'])
    require(font['complete_native_pages']==15 and font['logical_compiled_input_alignment_cases']==120 and all(font[k] for k in ['all15_single_pages','all_first_internal_final_visible_glyphs_in_order_unique_cells_and_bounds','each216x64_plane_exact_independent_current_font_and_all_canaries','all_original_current_font_renderer_instructions_verified','original_pair_phase_and_guards_bound_without_new_substitutions','only_original_static_selectors26_197','original_source_current_R11_ellipsis_CP932_glyph_retained_without_punctuation_revision']),'complete font proof')
    require(stored['stored_alignment_cases']==60 and stored['fresh_alignment_cases']==36 and stored['exact_reused_alignment_cases']==24 and stored['zero_ink_parity_tail_count']==9 and stored['complete_native_pages']==15 and stored['all_final_stored_targets_equal_reviewed_complete_native_ink'] and stored['all_bounds_canaries_pair_phase_and_zero_macros_pass'],'complete stored proof')
    require(policy['positive_paragraph_count']==15 and policy['negative_count']==len(policy['negative_cases'])==62 and all(c['rejected'] for c in policy['negative_cases']) and policy['original_R11_ellipsis_compiled_hex']=='1a8163' and policy['original_R11_native_width_px']==12 and policy['three_exact_record_local_weak_waivers_all_base_diagnostics_preserved'],'policy positive/negative obligations')
    original_scope(doc,mapping,seal,load,require)
