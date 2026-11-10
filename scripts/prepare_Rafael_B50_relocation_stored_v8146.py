"""Prepare branch-free B50 research reconstruction and complete stored-body native checks."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/Rafael_B50_relocation_tools_v8146')
RELOC='Rafael_B50_relocation_v8146/one_block28_speeches_zero_relative_cases_exact_full_inverse.json'
NATIVE='Rafael_B50_pages_refined_v8143/28_final_native_pages20_fresh92_reused_alignments.json'
REVIEW='Rafael_B50_native_review_v8145/28_native_pages3_names_two_scoped_warnings18_infos_wrap_review.json'
LOGICAL='Rafael_B50_logical_v8139/28_logical_paragraphs112_original_native_alignments_no_FE.json'
if __name__=='__main__':
    assert not ROOT.exists()
    a=derive('scripts/relocate_Rafael_B49_v8096.py','scripts/relocate_Rafael_B50_v8146.py',{
        'Rafael_B49_relocation_v8096':'Rafael_B50_relocation_v8146',
        'Rafael_B49_current_v8086/all61_complete_source_current_refs':'Rafael_B50_current_v8136/all28_complete_source_current_refs',
        'Rafael_next_clean_v8073/complete_clean_SC0_B49_EV0_andcoverage_before_current_English.json':'Rafael_next_clean_v8129/complete_clean_SC0_B50_EV0_andcoverage_before_current_English.json',
        'Rafael_B49_layout_v8090c/61_automatic_plans_full_native_width_exact_source00_02_09_no_FE.json':'Rafael_B50_layout_v8140b/28_automatic_plans_full_native_width_exact_source00_02_09_FA2_FI1.json',
        'Rafael_B49_native_review_v8095/61_native_pages7_names_three_scoped_warnings22_infos_wrap_review.json':REVIEW,
        'Rafael_B49_archive_tools_v8096/56_exact_source_current_relative_operands_bound_to280_native_cases.json':'Rafael_B50_archive_tools_v8146/zero_source_current_relative_operands37_commands_nine_nontext_pairs.json',
        'current_V8066_Rafael_native_v8069':'current_V8122_Rafael_native_v8125','B49':'B50','[213,244,405]':'[61,114]',
        "for g in groups)==61":"for g in groups)==28", "for g in groups)==56":"for g in groups)==0",'==[49]':'==[50]',
        'one_block61_speeches56_relative_fixups280_cases_exact_full_inverse':'one_block28_speeches_zero_relative_cases_exact_full_inverse',
        'source_relative_sites=56,relocated_native_skip_cases=280':'source_relative_sites=0,relocated_native_skip_cases=0',
        'all61_six_byte_preambles_twoFI_macros_selectors_complete_terminal_andseparate_tails_preserved':'all28_six_byte_preambles_FA2_FI1_selectors_complete_terminal_andseparate_tails_preserved',
        'source_UI_effects_waits_seven_A000_C281_wholecontrols_stored_fonts_census_actual_policy_production_andrelease_pending':'source_UI_4821_4720_4681_oneA000_nine_wholecontrols_stored_fonts_census_actual_policy_production_andrelease_pending',
        'Research-only B49 reconstruction:56nested fixups,61complete preambles,61reviewed pages andfull inverses.':'Research-only B50 reconstruction:zero fixups,28complete preambles,28reviewed pages andfull inverses.',
        'Research archive:61speeches/56relative sites/280guarded cases;onlyB49 changes,342others exact;full predecessor archive andclean block inverses pass.No ROM orcredit.':'Research archive:28speeches/zero relative sites orcases;onlyB50 changes,342others exact;full predecessor archive andclean block inverses pass.No ROM orcredit.',
    })
    b=derive('scripts/prove_Rafael_B49_stored_v8097.py','scripts/prove_Rafael_B50_stored_v8147.py',{
        'Rafael_B49_stored_v8097':'Rafael_B50_stored_v8147',
        'Rafael_B49_relocation_v8096/one_block61_speeches56_relative_fixups280_cases_exact_full_inverse.json':RELOC,
        'Rafael_B49_pages_refined_v8092/61_final_native_pages20_fresh224_reused_alignments.json':NATIVE,
        'Rafael_B49_native_review_v8095/61_native_pages7_names_three_scoped_warnings22_infos_wrap_review.json':REVIEW,
        'Rafael_B49_logical_v8089/61_logical_paragraphs244_original_native_alignments_no_FE.json':LOGICAL,
        'B49':'B50','block=49':'block=50','blocks[49]':'blocks[50]',
        "len(view['directly_viewed_sheets'])==12":"len(view['directly_viewed_sheets'])==6",
        "len(target)==3792 and group['target_logical_end']==3792":"len(target)==group['target_bytes'] and group['target_logical_end']+group['target_tail_bytes']==len(target)",
        "body=raw[1:];assert all(t not in body for t in [b'FA',b'FO',b'%'])\n        assert body.count(b'FI')==int(row['source_record_index'] in [311,388])\n        expected=body.replace(b'FI',b'Rafael')":"body=raw[1:];assert b'%' not in body\n        for token in [b'FI',b'FA',b'FO']:assert body.count(token)==bytes.fromhex(row['source_hex'])[1:].count(token)\n        expected=body.replace(b'FI',b'Rafael').replace(b'FA',b'Castor').replace(b'FO',b'Castor Co.')",
        'len(rows)==61 and len(fresh)==31 and len(reused)==30':'len(rows)==28 and len(fresh)==sum(r[\'parity_space_added\'] for r in group[\'text_records\']) and len(fresh)+len(reused)==28',
        "for r in rows)==61":"for r in rows)==28",
        'all61_stored_bodies124_fresh120_reused_alignments61_exact_viewed_pages':'all28_stored_bodies_full_native_alignment_and28_exact_viewed_pages',
        'fresh_native_alignment_cases=124,exact_reused_native_alignment_cases=120,total_bound_alignment_cases=244':'fresh_native_alignment_cases=4*len(fresh),exact_reused_native_alignment_cases=4*len(reused),total_bound_alignment_cases=112',
        'all61_complete_native_paragraphs61_pages_full_first_internal_final_glyphs_bounds_consumption_pass':'all28_complete_native_paragraphs28_pages_full_first_internal_final_glyphs_bounds_consumption_pass',
        'all61_native_ink_planes_exact_to_already_viewed':'all28_native_ink_planes_exact_to_already_viewed',
        'all31_parity_tails_create_no_blank_oradditional_page':'all_parity_tails_create_no_blank_oradditional_page',
        'all61_complete_stored_single_pages_exact_to_viewed':'all28_complete_stored_single_pages_exact_to_viewed',
        'all61_complete_sixbyte_preambles_source00_02_09_andtwo_FI_preserved':'all28_complete_sixbyte_preambles_source00_02_09_FA2_FI1_preserved',
        'three_exact_QA_warnings22_infos_andnarrow_documented_exceptions_unchanged':'two_exact_QA_warnings18_infos_andnarrow_documented_exceptions_unchanged',
        'final_dispatch_predicates_fullreference_callers_loaders_actual_C281_transition_policy_atomic_andrelease_pending':'final_dispatch_controls_fullreference_callers_loaders_actual_4821_4720_4681_transition_policy_atomic_andrelease_pending',
        'Fresh native checks for eight zero-ink parity tails;reuse seven byte-exact reviewed bodies.':'Fresh native checks only for B50 parity tails;reuse exact reviewed bodies without invented branch cases.',
        "print('61stored paragraphs/61exactviewed pages:31tails124fresh/30bodies120reused alignments;noextra/blank pages. ActualC281transition/control/reference/release pending.')":"print('28stored paragraphs/28exact viewed pages:',len(fresh),'tails/',len(fresh)*4,'fresh and',len(reused),'bodies/',len(reused)*4,'reused alignments;noextra/blank pages.Actual picture/control/reference/release pending.')",
    })
    ROOT.mkdir(parents=True);save(ROOT/'source_locked_derivations.json',[a,b])
    print('Prepared B50 zero-relative research relocation andexact stored parity/native proofs;no ROM orcredit.')
