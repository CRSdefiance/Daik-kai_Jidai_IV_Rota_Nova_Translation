"""Record all directly viewed English pages, scoped wrap findings and limits."""
from pathlib import Path
from collections import Counter
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/Hodram_B61_B70_native_view_v8896')
DOC=Path('translations/hodram_B61_B70_editorial_manuscript_v1.json')
PAGES=Path('work/analysis/Hodram_B61_B70_pages_v8894/compiled_native_pages.json')
PLANS=Path('work/analysis/Hodram_B61_B70_layout_v8893/automatic_plans.json')
LOGICAL=Path('work/analysis/Hodram_B61_B70_logical_v8891/logical_paragraphs.json')
DELTA=Path('work/analysis/Hodram_B61_B70_boundary_review_v8895/actual_boundary_findings_andprose_preserving_corrections.json')

if __name__=='__main__':
    assert not ROOT.exists();doc,pages,plans,logical,delta=map(read,[DOC,PAGES,PLANS,LOGICAL,DELTA])
    assert pages['manuscript_sha256']==plans['manuscript_sha256']==logical['manuscript_sha256']==sha(DOC.read_bytes())
    assert len(doc['records'])==len(pages['records'])==len(plans['records'])==224 and pages['complete_native_English_pages']==229
    assert pages['total_bound_compiled_alignment_cases']==logical['fresh_native_alignment_cases']==896
    assert pages['fresh_compiled_alignment_cases']==896 and pages['reused_compiled_alignment_cases']==0 and pages['FE_panels']==0
    expected=['B61_English_part1.png',*[f'B62_English_part{i}.png' for i in range(1,4)],
        *[f'B63_English_part{i}.png' for i in range(1,4)],*[f'B64_English_part{i}.png' for i in range(1,3)],
        *[f'B65_English_part{i}.png' for i in range(1,5)],*[f'B66_English_part{i}.png' for i in range(1,3)],
        *[f'B67_English_part{i}.png' for i in range(1,6)],'B68_English_part1.png','B69_English_part1.png','B70_English_part1.png']
    assert len(expected)==23 and expected==[Path(s['path']).name for s in pages['review_sheets']]
    assert sum(s['pages'] for s in pages['review_sheets'])==229
    for s in pages['review_sheets']:assert sha(Path(s['path']).read_bytes())==s['sha256']
    records={r['id']:r for r in doc['records']};planmap={r['id']:r for r in plans['records']}
    two_page=[];allpages=0
    for r in pages['records']:
        source=records[r['id']];p=planmap[r['id']];rendered=r['complete_native_English_display']
        assert r['logical_English']==source['english'] and r['compiled_hex']==p['encoded_hex']
        assert r['source_reference']==source['source_reference'] and r['current_reference']==source['current_reference']
        assert len(rendered['pages'])==p['expected_native_pages'] and rendered['complete_consumed_bytes']==len(bytes.fromhex(r['expanded_native_hex']))
        if len(rendered['pages'])==2:two_page.append(r['id'])
        for page in rendered['pages']:
            assert sha(Path(page['native_plane']).read_bytes())==page['native_plane_sha256']
            assert sha(Path(page['preview']).read_bytes())==page['preview_sha256']
            assert page['complete_first_internal_final_codes_bounds_consumption_andindependent_ink_exact']
            assert page['first_visible_origin']==([6,0] if page['native_continuation_guard_at_zero_andfirst_visible_at_six'] else [0,0])
            allpages+=1
        assert source['review']==dict(source=True,context=True,localization=True,naturalness=True,formatting=False)
    assert allpages==229 and two_page==pages['two_page_record_IDs'] and len(two_page)==5
    assert doc['revised']==132 and doc['retained']==92 and delta['changed_record_count']==16
    assert delta['all224_words_punctuation_names_macros_andprose_values_unchanged']
    QA=Counter(i['severity'] for p in plans['records'] for i in p['base_QA']['issues']);assert QA=={'info':68}
    for ident in doc['six_deliberately_opaque_B65_utterances_retained_exactly']:
        r=records[ident];assert bytes.fromhex(planmap[ident]['encoded_hex'])[1:]==bytes.fromhex(r['source_hex'])[1:]
    ROOT.mkdir(parents=True)
    save(ROOT/'all224_English_native229_pages_direct_view_andboundary_review.json',dict(
        manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),candidate=pages['candidate'],candidate_sha256=pages['candidate_sha256'],
        all23_sheets229_English_native_pages_directly_viewed=True,review_sheets=pages['review_sheets'],
        individual_prose_decisions=224,revised=132,retained=92,complete_native_pages=229,two_page_record_IDs=two_page,
        complete_logical_alignments=896,complete_compiled_alignments=896,source_FE_panels=0,source_macro_counts=dict(FI=15,FA=3,FO=0),
        all_complete_leading_internal_final_glyphs_bounds_independent_pixels_consumption_andpagination_pass_offline=True,
        continuation_guard_space_at_zero_first_visible_six_is_original_native_behavior=True,
        reviewed_ordinary_boundaries=[
            'B64R11 now starts with the complete predicate You truly are the king, then the Indian Ocean complement. The incomplete nine-character opening is removed without changing prose or216px width.',
            'B63R22 keeps the complete don\'t you? tag together. B62R39 keeps the question together after the complete opening Tell me... pause.',
            'B67R238 keeps the complete final sentence on page2, rather than ending page1 with He won\'t. All five two-page speeches have complete continuation pages.',
            'B64R63 iron/ship is an ordinary complete-word soft wrap inside the four native rows. Both words and their relationship remain clear; no missing glyph, word split, narrowed viewport, new manual break or fit-driven prose omission is introduced.',
            'B67R66 and the longer strategic descriptions continue across native pages. Those are automatic logical-paragraph continuations, with every word present; actual paging behavior still needs representative gameplay.',
            'B65R46 uses after all for realization and after all this time for elapsed separation. The distinct idioms retain the captain\'s reflective reunion observation without inventing an exact duration.',
            'The six circle/cross utterances remain source-exact unknown-language speech. They are deliberately opaque prose, not diagnostic placeholders.',
            'Maria\'s full introduction and Lil\'s apology retain their source-bound current full-width I glyphs. Complete native glyph checks pass; no global glyph-storage policy or full-name catalogue approval follows.'],
        original_QA_infos=68,original_QA_warnings=0,original_QA_errors=0,waivers=0,
        actual_findings_separate_from_passing_validation=dict(editorial_revisions=132,justified_retentions=92,
            first_plan_readability_findings=4,plans_refined=16,new_source_native_control_or_glyph_failures=0,new_logical_macro_failures=0,new_compiled_native_page_failures=0),
        no_actual_gameplay_natural_event_activation_header_portrait_transition_orhardware_claim=True,
        all224_formatting_gates_still_false_pending_stored_actual_andrelease_validation=True,
        stored_reconstruction_relative_offsets_complete_refs_inverses_loader_gameplay_production_atomic_andregistered_release_pending=True,
        no_ROM_registry_ledger_credit_orprior_artifact_change=True,new_credit=0,new_emulator_runs=0,full_goal_complete=False,
        evidence={str(p):sha(p.read_bytes()) for p in [DOC,PAGES,PLANS,LOGICAL,DELTA,Path(__file__)]}))
    print('All23 English sheets/229 native pages/224 utterances directly viewed;132 revisions92 retentions;4actual wrap findings corrected. No new glyph/control failure;stored/actual/release pending;zero credit.')
