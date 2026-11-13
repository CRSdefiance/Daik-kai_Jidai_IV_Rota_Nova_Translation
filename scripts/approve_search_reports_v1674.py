"""Source/native approval only;registered ROM and original changed scenes pending."""
from copy import deepcopy
from pathlib import Path
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.patch.grand_race_menu_release import sha
from scripts.search_reports_native_plan_v1661 import compiled, IDS
from scripts.verify_village_wrap_v608 import read, save

ROOT=Path('work/analysis/search_reports_native_review_v1674')
SOURCE=Path('translations/search_reports_editorial_manuscript_v3.json')
OUT=Path('translations/search_reports_editorial_manuscript_v4.json')
if __name__=='__main__':
    assert not ROOT.exists() and not OUT.exists()
    doc=deepcopy(read(SOURCE))
    paths={k:Path(v) for k,v in {
        'native_font_proof':'work/analysis/search_reports_fonts_v1671/native_font_research.json',
        'native_copy_proof':'work/analysis/search_reports_copies_v1672/all_native_copies_and_prefix_cache_sequence.json',
        'escape_regression_proof':'work/analysis/search_reports_escape_v1673/original_direct_escape_regression.json',
        'native_runtime_proof':'work/analysis/search_reports_runtime_v1660/native_runtime_verification.json'}.items()}
    fonts,copies,escape,runtime=[read(paths[k]) for k in paths]
    assert fonts['manuscript_sha256']==sha(SOURCE.read_bytes()) and len(fonts['cases'])==294 and not fonts['findings']
    assert len(fonts['invalid_compiler_inputs_rejected'])==17 and len(fonts['all414_existing_actor_selections'])==414
    assert fonts['all_original_one_to_four_digit_quantity_width_pairs_tested']
    assert len(fonts['sheets_for_visual_review'])==3 and sum(s['panels'] for s in fonts['sheets_for_visual_review'])==38
    for sheet in fonts['sheets_for_visual_review']:assert sha(Path(sheet['path']).read_bytes())==sheet['sha256']
    assert copies['complete_native_copies']==7336 and len(copies['sequenced_cache_cases'])==180
    assert len(escape['all13_original_direct_pipeline_cases'])==13 and runtime['native_exact_dispatch_ABI_memory_and_external_reference_proven']
    assert all(p['ARM9_sha256']==fonts['ARM9_sha256'] and p['COMMON_sha256']==fonts['COMMON_sha256'] for p in [copies,escape])
    rows={r['message_id']:r for r in doc['records']}
    assert {c['message_ID'] for c in fonts['cases']}==set(IDS)
    for case in fonts['cases']:
        assert case['compiled_hex']==compiled(rows[case['message_ID']]).hex()
        assert case['full228x64_native_and_independent_ink_shadow_planes_equal']
        assert case['complete_leading_trailing_letters_source_quantities_margins_bounds_and_blank_paper_verified']
    ROOT.mkdir(parents=True);visual=ROOT/'complete_native_panels_visual_review.json'
    save(visual,{'sheets':fonts['sheets_for_visual_review'],'all3_sheets38_panels_actually_viewed':True,
        'all11_distinct_wordings_and_original_voice_fallbacks_reviewed':True,
        '2218_orphan_resolved_with_natural_unwrapped_prose':True,'312_singular_plural_grammar_fixed_with_count_neutral_label':True,
        'source_reachable_quantity_layout_findings':0,'remaining_layout_findings':0,
        'outside_source_domain_numeric_stress_weak_breaks_disclosed_not_real_gameplay_claims':fonts['outside_source_domain_stress_findings'],
        'native_literal_x0_and_spoken6px_uniform_line_origins_preserved':True,'no_release_gameplay_or_completion_credit':True})
    doc.update(formatting_review_pending=False,status='source-native-approved;registered-release-and-original-gameplay-pending',
               reviewed_research_manuscript=str(SOURCE),reviewed_research_manuscript_sha256=sha(SOURCE.read_bytes()),
               visual_review=str(visual),**{k:str(p) for k,p in paths.items()})
    for row in doc['records']:
        row['review']['formatting']=True;row['compiled_hex']=compiled(row).hex();row['status']='source-native-approved;release-actual-pending'
    validate_natural_dialogue_batch(doc);save(OUT,doc)
    lp=Path('translations/editorial_review_current_v1.json');ledger=read(lp);before=deepcopy(ledger)
    unit=next(u for u in ledger['coverage_units'] if u['id']=='Shared-Search-reports11-source-prose');unit.update(status=doc['status'],native_approved_manuscript=str(OUT))
    drafts=ledger['active_source_prose_drafts'];drafts['manuscripts'].extend([str(SOURCE),str(OUT)])
    drafts['manuscript_record_subsets_pending']['translations/search_reports_editorial_manuscript_v1.json']=[]
    drafts['manuscript_record_subsets_pending'][str(SOURCE)]=[];drafts['manuscript_record_subsets_pending'][str(OUT)]=list(IDS)
    ledger['formatting_watchlist']['Search_reports11'].update(status=doc['status'],native_approved_manuscript=str(OUT),
        native_font_proof=str(paths['native_font_proof']),native_copy_proof=str(paths['native_copy_proof']),native_visual_review=str(visual),
        source_reachable_wrap_and_count_grammar_findings_resolved=True,registered_release_and_original_revised_gameplay_pending=True)
    ledger['research_checkpoints'].append({'id':'V1674-Search-reports11-native-approved','proof':str(ROOT/'native_approval_receipt.json'),
                                           'source_prose_reviews_added':0,'completed_entries_added':0,'full_goal_complete':False})
    for key in ['records_editorially_completed','records_with_source_and_prose_pass','reviewed_but_incomplete_COMMON_IDs','unresolved_graphics_work']:assert ledger[key]==before[key]
    save(lp,ledger);save(ROOT/'native_approval_receipt.json',{'manuscript':str(OUT),'manuscript_sha256':sha(OUT.read_bytes()),
        'proofs':{str(p):sha(p.read_bytes()) for p in [*paths.values(),visual]},'completed':1350,'source_prose':1519,'reviewed_incomplete_COMMON':169,
        'completed_entries_added':0,'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    print('Eleven reports native-approved:294 complete font cases,414 actor selections,17 negatives,7336 copies180 cache,13 prior pipelines,529507 dispatch/ABI cases. Registered ROM and actual changed scenes pending.')
