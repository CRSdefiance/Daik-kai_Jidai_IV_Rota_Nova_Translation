"""Approve source/native hot-spring presentation; actual scene remains open."""
from copy import deepcopy
from pathlib import Path
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.patch.grand_race_menu_release import sha
from scripts.hot_spring_native_plan_v1615 import compiled,IDS
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/hot_spring_native_review_v1620')
OLD=Path('translations/hot_spring_editorial_manuscript_v1.json')
NEW=Path('translations/hot_spring_editorial_manuscript_v2.json')
if __name__=='__main__':
    assert not ROOT.exists() and not NEW.exists()
    doc=read(OLD);paths={'native_font_proof':'work/analysis/hot_spring_fonts_v1617/native_font_research.json',
        'native_copy_proof':'work/analysis/hot_spring_copies_v1618/all_native_copies_and_prefix_cache_sequence.json',
        'escape_regression_proof':'work/analysis/hot_spring_escape_v1619/original_direct_escape_regression.json',
        'native_runtime_proof':'work/analysis/hot_spring_runtime_v1616/native_runtime_verification.json'}
    fonts,copies,escape,runtime=[read(p) for p in paths.values()];plan=read('work/analysis/hot_spring_payload_v1615/native_payload_plan.json')
    assert fonts['manuscript_sha256']==sha(OLD.read_bytes()) and len(fonts['cases'])==16 and not fonts['findings']
    assert len(fonts['invalid_compiler_inputs_rejected'])==16 and {c['message_ID'] for c in fonts['cases']}==set(IDS)
    assert sum(len(t['all207_existing_actor_choices']) for t in fonts['all414_existing_actor_table_selections'])==414
    assert sum(c['source_minus1_fallback_to_voice0'] for c in fonts['cases'])==3
    assert copies['complete_native_copies']==7336 and len(copies['sequenced_cache_cases'])==180 and len(escape['all13_original_direct_pipeline_cases'])==13
    assert all(p['ARM9_sha256']==plan['target_ARM9_sha256'] and p['COMMON_sha256']==plan['target_COMMON_sha256'] for p in [fonts,copies,escape])
    assert runtime['native_exact_dispatch_ABI_memory_and_external_reference_proven']
    assert read('work/analysis/hot_spring_runtime_v1616/scope_proof.json')['total_cases']==529481
    assert read('work/analysis/hot_spring_runtime_v1616/runtime_plan.json')['patches']==plan['runtime_plan']['patches']
    for c in fonts['cases']:
        assert not c['findings'] and c['full228x64_native_and_independent_font_exact'] and c['complete_first_final_letters_uniform6px_margins_bounds_and_blank_paper_pass']
        assert sha(Path(c['preview']).read_bytes())==c['preview_sha256']
    for sheet in fonts['sheets_for_visual_review']:assert sha(Path(sheet['path']).read_bytes())==sheet['sha256']
    ROOT.mkdir(parents=True);visual=ROOT/'all16_native_panels_visual_review.json'
    save(visual,{'sheets':fonts['sheets_for_visual_review'],'all16_native_panels_actually_viewed':True,
        'all13_complete_glyph_planes_uniform6px_margins_bounds_blank_paper_and_final_punctuation_pass':True,
        'all414_source_actor_table_selections_and3_minus1_fallbacks_preserved':True,'remaining_layout_findings':0,
        'registered_build_and_original_hot_spring_pending':True,'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    approved=deepcopy(doc);approved.pop('strict_build_validation_rejects_draft_until_formatting_review')
    approved.update(formatting_review_pending=False,status='source-native-approved;registered-release-original-hot-spring-pending',
        source_draft_was_rejected_until_formatting_review=True,reviewed_research_manuscript=str(OLD),reviewed_research_manuscript_sha256=sha(OLD.read_bytes()),
        visual_review=str(visual),visual_review_sha256=sha(visual.read_bytes()))
    for key,path in paths.items():approved[key],approved[key+'_sha256']=path,sha(Path(path).read_bytes())
    for row in approved['records']:
        row['review']['formatting']=True;row['compiled_hex']=compiled(row).hex();row['status']='native-approved;registered-release-original-hot-spring-pending'
    validate_natural_dialogue_batch(approved);save(NEW,approved)
    lp=Path('translations/editorial_review_current_v1.json');ledger=read(lp);before=deepcopy(ledger)
    assert (ledger['records_editorially_completed'],ledger['records_with_source_and_prose_pass'],len(ledger['reviewed_but_incomplete_COMMON_IDs']))==(1350,1507,157)
    save(ROOT/'coverage_before_native_approval.json',before)
    drafts=ledger['active_source_prose_drafts'];drafts['manuscripts'].append(str(NEW));drafts['manuscript_record_subsets_pending'][str(OLD)]=[];drafts['manuscript_record_subsets_pending'][str(NEW)]=list(IDS)
    unit=next(u for u in ledger['coverage_units'] if u['id']=='Shared-hot-spring13-source-prose');unit.update(status=approved['status'],native_approved_manuscript=str(NEW),native_visual_review=str(visual))
    ledger['formatting_watchlist']['hot_spring13'].update(native_approved_manuscript=str(NEW),native_font_proof=paths['native_font_proof'],native_visual_review=str(visual),
        native_font_wrap_release_and_actual_original_hot_spring_pending=False,registered_release_and_actual_original_hot_spring_pending=True)
    summary=('V1620 source/native-approves hot-spring13:12 revisions1 retention,16 original voice/table pipelines including3 source minus1 fallbacks,414 actor-table choices,complete native/independent glyph planes,16 compiler negatives,and viewed16-panel sheet pass without layout findings. '
        '529481 exact native selector/ABI cases,7336 copies180 cache sequences13 prior escape pipelines and historical modal/status checks pass. Two original role1 tables are added to the exact allowlist;encoded selector188/188 and gate168/172 stay within original banks. '
        'Pointer normalization changes896 to873 in one immediate byte;numeric780 and all historical dispatch semantics remain exact.123040 staged bytes,cache/BSS/ITCM/arena and3656 unselected or retained copies stay fixed. '
        'All later screenshot corrections are retained. A newer choice-centering-only profile appeared during work and must also be inherited by integration;it changes SC0 only,not the source hot-spring payload. '
        'No new ROM,patch,startup or actual hot-spring approval yet. Counts1350 complete,1507 source/prose,157 pending COMMON;full editorial goal and separate graphics/all18 plaques remain open.')
    ledger['latest_checkpoint']=summary;ledger['research_checkpoints'].append({'id':'V1620-hot-spring13-native-approved','proof':str(ROOT/'native_approval_receipt.json'),'completed_entries_added':0,'source_prose_reviews_added':0,'full_goal_complete':False})
    for k in ['records_editorially_completed','records_revised_and_integrated','records_with_source_and_prose_pass','reviewed_but_incomplete_COMMON_IDs',
        'current_native_relocation_reference','current_integrated_candidate','source_pins','unresolved_graphics_work','older_record_reaudit_after_full_editorial_goal']:assert ledger[k]==before[k],k
    save(lp,ledger)
    Path('docs/hot_spring_v1620_native_checkpoint.md').write_text('# V1620 hot-spring13 native approval\n\n'+summary+'\n',encoding='utf-8')
    for name in ['translation_progress.md','known_issues.md','todo.md','editorial_review_goal.md']:
        with (Path('docs')/name).open('a',encoding='utf-8') as f:f.write('\n\n## V1620 hot-spring13 native approval\n\n'+summary+'\n')
    save(ROOT/'native_approval_receipt.json',{'manuscript':str(NEW),'manuscript_sha256':sha(NEW.read_bytes()),'proofs':{p:sha(Path(p).read_bytes()) for p in [*paths.values(),str(visual)]},
        'completed':1350,'source_prose':1507,'reviewed_incomplete_COMMON':157,'completed_entries_added':0,'registered_release_and_original_hot_spring_pending':True,
        'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    print('Hot-spring13 source/native approved;1350 complete,1507 reviewed,157 pending. Registered integration and original scene remain open.')
