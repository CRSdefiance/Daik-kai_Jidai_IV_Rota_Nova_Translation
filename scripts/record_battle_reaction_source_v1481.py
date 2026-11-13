"""Record32 new source/prose reviews without native/release/gameplay completion."""
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/battle_reactions_source_review_v1481')
MANUSCRIPT=Path('translations/battle_reactions_editorial_manuscript_v1.json')
IDS=list(range(2147,2179))

if __name__=='__main__':
    assert not ROOT.exists()
    doc=read(MANUSCRIPT);context_path=Path(doc['source_context']);context=read(context_path)
    assert sha(context_path.read_bytes())==doc['source_context_sha256']
    assert [r['message_id'] for r in doc['records']]==IDS and (doc['revised'],doc['retained'])==(16,16)
    assert all(all(r['review'][k] for k in ['source','context','localization','naturalness']) and not r['review']['formatting'] for r in doc['records'])
    assert context['all32_current_original_actor_selection_file_copy_printf_macro_entry_contracts_executed']
    assert context['native_actor_selections']==824
    ledger_path=Path('translations/editorial_review_current_v1.json');ledger=read(ledger_path);before=deepcopy(ledger)
    assert (ledger['records_editorially_completed'],ledger['records_with_source_and_prose_pass'])==(1323,1435)
    complete={n for f in ledger['completed_editorial_families'] for n in f.get('native_message_IDs',[])}
    pending=ledger['reviewed_but_incomplete_COMMON_IDs']
    assert len(complete)==1322 and len(pending)==112 and not set(IDS)&(complete|set(pending))
    ROOT.mkdir(parents=True);save(ROOT/'coverage_before_source_review.json',before)
    ledger['records_with_source_and_prose_pass']+=32
    ledger['records_with_source_prose_drafts']=ledger['records_with_source_and_prose_pass']
    ledger['source_prose_reviewed_counts_by_file']['/COMMON/MESFILE.DK4']+=32
    ledger['reviewed_but_incomplete_COMMON_IDs']=sorted(pending+IDS)
    drafts=ledger['active_source_prose_drafts'];drafts['native_message_IDs']=sorted(drafts['native_message_IDs']+IDS)
    assert str(MANUSCRIPT) not in drafts['manuscripts']
    drafts['manuscripts'].append(str(MANUSCRIPT));drafts['manuscript_record_subsets_pending'][str(MANUSCRIPT)]=IDS
    drafts['status']='32-battle-reactions24-loss-surrender16-sinking34-aftermath38-older-reviewed-entries-open'
    drafts['note']='32 battle reactions are source/context/prose-reviewed;native layout/integration/original scenes remain pending. V1456 integrates24 source/native-approved loss/surrender reports with original new events pending.16 sinking,34 aftermath38 older and broader shared/routes/raw prose remain open.'
    unit='Shared-battle-reactions32-source-prose';assert unit not in {u['id'] for u in ledger['coverage_units']}
    ledger['coverage_units'].append({'id':unit,'status':'source-context-prose-reviewed-native-release-gameplay-pending',
        'native_message_IDs':IDS,'manuscript':str(MANUSCRIPT),'source_context':str(context_path),
        'completed_entries_added':0,'full_goal_complete':False})
    ledger['formatting_watchlist']['battle_reactions32']={'native_IDs':IDS,'source_prose_manuscript':str(MANUSCRIPT),
        'source_context':str(context_path),'original_entry':0x02053F0C,'original_parent':0x02053F40,'selector_stack_offset':0x274,
        'one_logical_paragraph_no_authored_alignment_or_breaks':True,
        'ordinary_ASCII_I_postmacro_wrap_native_font_and_margin_checks_pending':True,
        'all_native_font_visual_copy_cache_registered_release_and_original_scene_gates_open':True,
        'global_formatting_audit_complete':False}
    summary=('V1481 source/context/prose-reviews32 new shared reactions2147-2178:16 proposed revisions and16 '
        'justified retentions. Four clean tables and824 existing-actor voice selections are mapped.32 original '
        '53F0C/53F40/274 table/speech/loader/printf/macro contracts execute on current V1456 RAM in CPU research. '
        'Battle-setup callback65968 is registered through71020/71024;its original RNG and voice branches are '
        'preserved. Only voice2/3 reach the first table and4/6 the second through that mapped callback;stored '
        'alternatives are not declared individually reachable or unused across the game. Original own-ship '
        'projectile-hit7564C invokes74094,whose separate surprise and persistent-injury branches explain the '
        'remaining two tables. No RNG,HP,health-state,actor,eligibility or result is changed to map this context. '
        'New English uses logical ASCII paragraphs,retains distinctive exclamations and bleeding,localizes '
        'asameshi-mae as piece of cake,and renders2175 as frustrated injury speech rather than claiming '
        'tactical failure. Full-width Latin I is normalized in otherwise retained prose only where recorded. '
        'Native formatting/glyphs/margins/bounds/visual review,copy/cache regressions,registered integration '
        'and original scene/dismissal/transition gates remain open. The first authoring probe correctly '
        'stopped at the clean-only parser guard;1480b uses existing clean=False canonical mode without '
        'weakening any guard. Counts1467 source/prose reviewed,1323 complete(985 revised338 retained),144 '
        'reviewed-incomplete COMMON(32 reactions24 loss/surrender16 sinking34 aftermath38 older),plus broader '
        'shared/routes/raw prose. V1456 remains experimental integration,V1430 completed-native reference; '
        'canonical,V997,graphics/all18 plaques and later older-record re-audit unchanged/open. A separate '
        'early-mode survey1475 ended with confirmed20-minute navigation timeout/exit1;its partial evidence '
        'and unchanged donors are retained1477 without terminal-input audit or original event credit. Goal active.')
    ledger['latest_checkpoint']=summary
    ledger['research_checkpoints'].append({'id':'V1481-battle-reactions32-source-prose','manuscript':str(MANUSCRIPT),
        'source_context':str(context_path),'source_prose_reviews_added':32,'completed_entries_added':0,'full_goal_complete':False})
    assert len(ledger['reviewed_but_incomplete_COMMON_IDs'])==len(drafts['native_message_IDs'])==144
    assert len(complete|set(ledger['reviewed_but_incomplete_COMMON_IDs']))==1466
    assert sum(ledger['source_prose_reviewed_counts_by_file'].values())==1467
    for key in ['records_editorially_completed','records_revised_and_integrated','retained_wordings_editorially_completed',
        'completed_editorial_record_counts_by_file','current_integrated_candidate','current_native_relocation_reference',
        'source_pins','unresolved_graphics_work','older_record_reaudit_after_full_editorial_goal','raw_source_coverage_revisit']:
        assert ledger[key]==before[key],key
    save(ledger_path,ledger)
    document=Path('docs/battle_reactions_v1481_source_checkpoint.md');assert not document.exists()
    document.write_text('# V1481 battle reaction source and prose review\n\n'+summary+'\n\n'
        '## Next required gates\n\nDetermine whether all four actor-table scopes fit within the existing '
        '188-byte selector and172-byte gate without growth. Preserve every prior parent/stack/high-word '
        'contract and all staged allocations. Compile one paragraph before original macro expansion,then '
        'verify native post-expansion wrapping,complete glyph planes,visible margins,all leading/trailing '
        'characters and page bounds. Resolve layout findings by natural source-faithful wording or a '
        'proven formatter change;never insert alignment padding or abbreviate facts to fit. '
        'Complete native copies/cache regressions,registered full-stack ROM/exact patch,startup and '
        'representative original reactions/dismissal/transition before granting family completion. '
        'Do not force RNG,injuries,actor IDs or combat outcomes.\n',encoding='utf-8')
    for name in ['translation_progress.md','known_issues.md','todo.md','editorial_review_goal.md']:
        with (Path('docs')/name).open('a',encoding='utf-8',newline='\n') as f:
            f.write('\n\n## V1481 battle reactions32 source/prose review\n\n'+summary+'\n\nSee [checkpoint](battle_reactions_v1481_source_checkpoint.md).\n')
    save(ROOT/'source_review_receipt.json',{'manuscript':str(MANUSCRIPT),'manuscript_sha256':sha(MANUSCRIPT.read_bytes()),
        'source_context':str(context_path),'source_context_sha256':sha(context_path.read_bytes()),
        'completed':1323,'source_prose':1467,'reviewed_incomplete_COMMON':144,'source_prose_reviews_added':32,
        'completed_entries_added':0,'proposed_revised':16,'proposed_retained':16,
        'native_release_and_original_events_pending':True,'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    print('1467 source/prose reviewed;1323 complete unchanged.32 new reactions added to144 reviewed-incomplete COMMON entries.')
