"""Add thirteen source/prose reviews without any completion or formatting credit."""
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/hot_spring_review_v1612')
MANUSCRIPT=Path('translations/hot_spring_editorial_manuscript_v1.json')
CONTEXT=Path('work/analysis/hot_spring_source_v1610/original_hot_spring13_source_context.json')

if __name__=='__main__':
    assert not ROOT.exists()
    doc,context=read(MANUSCRIPT),read(CONTEXT);assert doc['source_context_sha256']==sha(CONTEXT.read_bytes())
    assert doc['translation_policy']=='natural-dialogue-v2' and doc['formatting_review_pending']
    ids=[r['message_id'] for r in doc['records']];assert ids==list(range(2275,2288))
    for row in doc['records']:
        source=next(r for r in context['records_and_neighbors'] if r['message_id']==row['message_id'])
        for k in ['source_reference','source_hex','source_Japanese','current_reference','current_text_hex','current_English']:assert row[k]==source[k]
        assert all(row['review'][k] for k in ['source','context','localization','naturalness']) and not row['review']['formatting']
    path=Path('translations/editorial_review_current_v1.json');ledger=read(path);before=deepcopy(ledger)
    assert (ledger['records_editorially_completed'],ledger['records_with_source_and_prose_pass'],len(ledger['reviewed_but_incomplete_COMMON_IDs']))==(1350,1494,144)
    assert not set(ids)&(set(ledger['reviewed_but_incomplete_COMMON_IDs'])|{n for f in ledger['completed_editorial_families'] for n in f.get('native_message_IDs',[])})
    ROOT.mkdir(parents=True);save(ROOT/'coverage_before_review.json',before)
    ledger['records_with_source_and_prose_pass']+=13;ledger['records_with_source_prose_drafts']+=13
    ledger['source_prose_reviewed_counts_by_file']['/COMMON/MESFILE.DK4']+=13
    ledger['reviewed_but_incomplete_COMMON_IDs']=sorted(ledger['reviewed_but_incomplete_COMMON_IDs']+ids)
    drafts=ledger['active_source_prose_drafts'];drafts['native_message_IDs']=sorted(drafts['native_message_IDs']+ids)
    drafts['manuscripts'].append(str(MANUSCRIPT));drafts['manuscript_record_subsets_pending'][str(MANUSCRIPT)]=ids
    drafts.update(status='157-reviewed-COMMON-and-broader-prose-open',note='Hot-spring13 source/prose reviewed after completed fatigue2. Earlier144 and these13 require remaining gates;broader shared/routes/raw prose and separate graphics remain open.')
    ledger['coverage_units'].append({'id':'Shared-hot-spring13-source-prose','native_message_IDs':ids,'status':'source-context-prose-reviewed;native-release-original-gameplay-pending',
        'manuscript':str(MANUSCRIPT),'source_context':str(CONTEXT),'completed_entries_added':0})
    ledger['formatting_watchlist']['hot_spring13']={'native_message_IDs':ids,'manuscript':str(MANUSCRIPT),'source_context':str(CONTEXT),
        'full_ASCII_I2275_2277_2278_and2285_post_expansion_required':True,'no_authored_breaks_or_indent':True,
        'native_font_wrap_release_and_actual_original_hot_spring_pending':True,'original_role1_tables':[0x02116D80,0x02116D60],
        'original_minus1_voice_fallbacks_must_remain_intact':True,'source_requested_minus15_and_optional_followup310_context_preserved':True}
    summary=('V1612 adds13 hot-spring source/prose reviews(12 proposed revisions1 justified retention),with no completion credit. '
        '1350 complete(1009 revised341 retained),1507 source/prose reviewed,157 reviewed-incomplete COMMON(earlier144 plus hot-spring13),plus broader shared/routes/raw prose. '
        'Current packet uses the later screenshot-text-repairs-20261022 candidate and verifies all13 texts unchanged from V1594 while preserving all later corrections. '
        'Original role1 discovery table2116D80 and optional relaxation2116D60,all414 existing actor selections and minus1 fallback to voice0 are mapped. '
        'Discovery speech precedes original fatigue-15/status309;optional relaxation/experience follows a separate native skill/RNG branch. '
        'Drafts restore hearsay,explicit expedition/admiral context,relaxed voices and the taste joke,and replace absolute fatigue claims with the source personal feeling where stated. '
        '2275 full-width leading I is a formatting lead;ASCII literal-I safety,post-expansion wrapping,full fonts,bounds,registered integration and actual hot-spring scene remain pending. '
        'Do not mark these13 complete or treat the friendly-village snapshot/CPU probes as a hot-spring event. V1492 promoted;graphics/all18 plaques and older-record re-audit remain separate unfinished work;full goal active.')
    ledger['latest_checkpoint']=summary;ledger['research_checkpoints'].append({'id':'V1612-hot-spring13-source-prose','proof':str(ROOT/'source_review_receipt.json'),
        'source_prose_reviews_added':13,'completed_entries_added':0,'full_goal_complete':False})
    assert len(ledger['reviewed_but_incomplete_COMMON_IDs'])==len(set(ledger['reviewed_but_incomplete_COMMON_IDs']))==157
    assert set(drafts['native_message_IDs'])==set(ledger['reviewed_but_incomplete_COMMON_IDs'])
    for k in ['records_editorially_completed','records_revised_and_integrated','retained_wordings_editorially_completed','completed_editorial_families',
        'completed_editorial_record_counts_by_file','current_integrated_candidate','current_native_relocation_reference',
        'source_pins','unresolved_graphics_work','older_record_reaudit_after_full_editorial_goal']:assert ledger[k]==before[k],k
    save(path,ledger)
    document=Path('docs/hot_spring_v1612_source_review.md');assert not document.exists()
    document.write_text('# V1612 hot-spring13 source and prose review\n\n'+summary+'\n\n'
        'Source context: `'+str(CONTEXT)+'`. Manuscript: `'+str(MANUSCRIPT)+'`. No new ROM built and no native formatting or actual hot-spring approval. '
        'Next:source-locked postmacro compiler/selector-membership audit,complete native fonts and pagination,registered integration preserving the later screenshot repairs,then original hot-spring discovery/recovery/follow-up and normal return.\n',encoding='utf-8')
    for name in ['translation_progress.md','known_issues.md','todo.md','editorial_review_goal.md']:
        with (Path('docs')/name).open('a',encoding='utf-8') as f:f.write('\n\n## V1612 hot-spring13 source/prose\n\n'+summary+'\n\nSee [review](hot_spring_v1612_source_review.md).\n')
    with Path('docs/editorial_handoff_current.md').open('a',encoding='utf-8') as f:f.write('\n\n## Latest continuation - V1612\n\n'+summary+'\n\n'
        'Resume from `translations/hot_spring_editorial_manuscript_v1.json` and `work/analysis/hot_spring_source_v1610/original_hot_spring13_source_context.json`. '
        'Build upon and preserve the later screenshot repair profile. V1594 remains the completed native reference;fatigue testing is complete. All current emulator jobs terminal.\n')
    save(ROOT/'source_review_receipt.json',{'manuscript':str(MANUSCRIPT),'manuscript_sha256':sha(MANUSCRIPT.read_bytes()),'source_context':str(CONTEXT),'source_context_sha256':sha(CONTEXT.read_bytes()),
        'completed':1350,'source_prose':1507,'reviewed_incomplete_COMMON':157,'proposed_revised':12,'justified_retained':1,
        'source_prose_reviews_added':13,'completed_entries_added':0,'all_remaining_native_release_original_scene_gates_open':True,
        'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    print('Hot-spring13 source/prose recorded:1350 complete,1507 reviewed,157 pending COMMON;no new ROM or completion claim.')
