"""Frozen successor of the full registered verifier,with explicit partial gameplay coverage."""
import inspect
from pathlib import Path
from scripts import verify_early_HELP23_registered_release as previous
from scripts.source_locked_derivation_v5118 import checked_text
from dk4tool.dialogue.reviewed_help_pages_v3 import plan_articles

source=checked_text(inspect.getsource(previous.main),{
 "len(manifest['batches'])==671":"len(manifest['batches'])==672",
 "len(qualification['semantic_rejections'])==10":"len(qualification['changed_partial_coverage_rejections'])==4",
 "len(compiled['pages'])==25":"len(compiled['pages'])==28",
 "len(blocks)==212":"len(blocks)==216",
 "    assert actual['all25_complete_actual_pages_andnative_child_targets_pass'] and visual['all25_complete_pages_approved']":
 """    assert actual['all_selected_complete_actual_pages_andnative_child_targets_pass'] and visual['all15_observed_pages_approved']
    assert actual['actual_pages']==15 and actual['actual_articles']==10 and actual['offline_only_pages']==13
    assert len(actual['offline_only_article_IDs'])==13 and len(actual['original_forward_back_andL_R_history_returns'])==6
    native=load(conf['native']);native_visual=load(conf['visual'])
    assert native['native_pages']==28 and len(native['records'])==28
    assert native['all_complete_glyph_codes_font_pixels_link_requests_row_coordinates_input_header_andpixel_guards_pass']
    assert native['all_executed_current_instruction_bytes_exact']
    assert native['current_ARM9_sha256']==sha(candidate.read_file('/__arm9__.bin'))
    assert native_visual['all28_complete_pages_approved'] and native_visual['all_seven_refined_sheets_directly_viewed']
    assert native_visual['native_proof_sha256']==sha(Path(conf['native']).read_bytes())
    previous_qualification=load(qualification['previous_unchanged_source_gates_andruntime_name_stage_proofs'])
    assert len(previous_qualification['semantic_rejections'])==10
    assert sha(Path(qualification['previous_unchanged_source_gates_andruntime_name_stage_proofs']).read_bytes())==qualification['previous_unchanged_proofs_sha256']""",
 "(16,7)":"(19,4)",
 "            case=next(r for r in actual['actual_HELP_cases'] if r['topic_id']==block)\n            assert case['frame']==page['actual_frame'] and case['all_first_internal_final_glyphs_andblank_gaps_exact']":
 """            native_case=next(r for r in native['records'] if r['topic_id']==block)
            assert native_case['encoded_hex']==raw.hex() and native_case['all_visible_lines_coordinates_complete_pixels_and_first_final_glyphs_exact']
            assert native_case['input_header_pixel_guards_pass'] and native_case['all_executed_current_instruction_bytes_exact']
            cases=[r for r in actual['actual_HELP_cases'] if r['topic_id']==block]
            if 'actual_frame' in page:
                assert len(cases)==1 and cases[0]['frame']==page['actual_frame']
                assert cases[0]['all_first_internal_final_glyphs_andblank_gaps_exact'] and not row['offline_only']
            else:
                assert not cases and row['offline_only'] and row['topic_id'] in actual['offline_only_article_IDs']
                assert 'actual_capture' not in page""",
 'complete_stack_entries=671':'complete_stack_entries=672',
 'prose_revisions=16,justified_retentions=7':'prose_revisions=19,justified_retentions=4',
 'native_andactual_pages=25,actual_ordinary_Help_frames=32761':
 'native_andvisually_reviewed_pages=28,observed_actual_pages=15,observed_actual_articles=10,offline_only_pages=13,offline_only_articles=13,actual_ordinary_Help_frames=31641',
 "*Path('work/h23').rglob('*.nds')":"*Path('work/t23').rglob('*.nds')",
 "rom_retention_pins.HELP23_verified.pending.json":"rom_retention_pins.TownHELP23_verified.pending.json",
 "671 entries/114 accepted layers/eight stages/23 exact articles andclean-input patch pass;own registered startup binding pending.":
 "672 entries/114 accepted layers/eight stages/23 exact articles andclean-input patch pass;28 native,15 observed,13 offline-only pages;own startup binding pending.",
})
env={**previous.main.__globals__,'__file__':__file__,'plan_articles':plan_articles,
 'PARENT_PROOF':Path('work/analysis/Early_HELP23_release_verified_20261104/registered_release_verification.json'),
 'QUAL':Path('work/analysis/Town_HELP23_release_qualification_20261104/qualification.json')}
exec(compile(source,__file__+'::same-complete-registry-inverse-clean-patch-with-individual-native-andactual-membership','exec'),env)
main=env['main']
if __name__=='__main__':main()
