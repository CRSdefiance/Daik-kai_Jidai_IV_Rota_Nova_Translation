"""Register24 new source/prose reviews;native integration/gameplay remain open."""
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save

ROOT = Path('work/analysis/ship_loss_surrender_source_v1449')
MANUSCRIPT = Path('translations/ship_loss_surrender_editorial_manuscript_v2.json')
FONTS = Path('work/analysis/ship_loss_surrender_fonts_v1448/native_font_research.json')
RUNTIME = Path('work/analysis/ship_loss_surrender_runtime_v1443b/native_runtime_verification.json')
IDS = [*range(2074,2082),*range(2090,2106)]

if __name__=='__main__':
    assert not ROOT.exists()
    doc,fonts,runtime = [read(p) for p in [MANUSCRIPT,FONTS,RUNTIME]]
    assert [r['message_id'] for r in doc['records']]==IDS and (doc['revised'],doc['retained'])==(24,0)
    assert sha(Path(doc['source_context']).read_bytes())==doc['source_context_sha256']
    assert all(all(r['review'][g] for g in ['source','context','localization','naturalness'])
        and not r['review']['formatting'] for r in doc['records'])
    assert len(fonts['cases'])==624 and len(fonts['all618_source_existing_actor_choices'])==618
    assert fonts['manuscript_sha256']==sha(MANUSCRIPT.read_bytes()) and len(fonts['invalid_compiler_inputs_rejected'])==15
    assert all(r['full228x64_native_and_independent_font_exact'] for r in fonts['cases'])
    scope = read('work/analysis/ship_loss_surrender_runtime_v1443b/scope_proof.json')
    assert scope['total_cases']==529364 and runtime['native_exact_dispatch_ABI_memory_and_external_reference_proven']
    ledger_path = Path('translations/editorial_review_current_v1.json');ledger = read(ledger_path);before = deepcopy(ledger)
    assert (ledger['records_editorially_completed'],ledger['records_with_source_and_prose_pass'])==(1323,1411)
    completed = [n for f in ledger['completed_editorial_families'] for n in f.get('native_message_IDs',[])]
    pending = ledger['reviewed_but_incomplete_COMMON_IDs']
    assert len(completed)==len(set(completed))==1322 and len(pending)==len(set(pending))==88
    assert not set(IDS)&(set(completed)|set(pending))
    ROOT.mkdir(parents=True);save(ROOT/'coverage_before_source_review.json',before)
    ledger['records_with_source_and_prose_pass'] += 24
    ledger['records_with_source_prose_drafts'] = ledger['records_with_source_and_prose_pass']
    ledger['source_prose_reviewed_counts_by_file']['/COMMON/MESFILE.DK4'] += 24
    ledger['reviewed_but_incomplete_COMMON_IDs'] = sorted(pending+IDS)
    drafts = ledger['active_source_prose_drafts']
    drafts['native_message_IDs'] = sorted(drafts['native_message_IDs']+IDS)
    assert str(MANUSCRIPT) not in drafts['manuscripts']
    drafts['manuscripts'].append(str(MANUSCRIPT));drafts['manuscript_record_subsets_pending'][str(MANUSCRIPT)] = IDS
    drafts['status'] = '24-loss-surrender16-sinking34-aftermath38-older-reviewed-entries-open'
    drafts['note'] = ('24 loss/surrender alternatives have source/context/prose review and research native name/font proofs. '
        'They remain incomplete for final visual/native-copy/cache/escape approval,registered integration and original '
        'event/dismissal/transition verification.16 sinking,34 aftermath and38 older reviewed entries remain open,plus broader shared/routes/raw prose.')
    unit = 'Shared-ship-loss-surrender24-source-prose'
    assert unit not in {r['id'] for r in ledger['coverage_units']}
    ledger['coverage_units'].append({'id':unit,'status':'source-context-prose-reviewed-native-release-gameplay-pending',
        'native_message_IDs':IDS,'manuscript':str(MANUSCRIPT),'source_context':doc['source_context'],
        'completed_entries_added':0,'full_goal_complete':False})
    findings = len(fonts['findings'])
    summary = ('V1449 reviews24 new ship-loss/surrender alternatives:own capture2074-2081,own surrender2090-2097 '
        'and enemy surrender2098-2105. All24 current proposed wordings are revised;the earlier2100 retention '
        'becomes a same-length natural direct-address reorder. Restore Admiral where omitted,the white-flag '
        'observation,apparent-surrender qualifiers2091/2103/2105 and reportative2104. No invented casualty,'
        'sinking,treachery or whole-fleet result. Original72990/72B3C/72B7C use role1/53D44,tables02117AC0/'
        '02117B80/02117C60,and one original affected-ship name.618 existing actor voice selections pass. '
        'Source72484 surrender probability and party/slot/state branches remain untouched. V1439 current '
        'CPU probes show FA/IC/FI/FO/FU-like names are still misinterpreted in these3 unscoped paths. '
        'Research adds only those3 role-table memberships in180 of188 owned table bytes and168 of172 '
        'gate bytes,numeric bias780 and pointer bias896;all historical keys/parent/stack/high-word scopes '
        'preserved. V1442 rejected bias768 because role8120/8140 collided with special numeric status '
        'dispatch;no output was written. V1443b passes529364 native original-entry dispatch/ABI/guard '
        'cases,3668 modal-ID routing controls with one fixed synthetic paragraph,238 wrong-parent5 '
        'edge controls and140 whole-memory status cases. V1444 stopped before output at an incorrect '
        'single-block assumption;the source boundary places2100-2105 in COMMON23 and the other18 '
        'selected entries in22. V1444b/1447 preserve3644 unselected texts/copy spans,39 other blocks,'
        'all earlier formatter/status code,sections/BSS/cache/arena/ITCM and123040 staged bytes. '
        'First624 native font cases V1445 preserve literal names/all letters/uniform margins/bounds '
        'but find233 isolated-predicate wraps. V1446 moves20 direct addresses naturally to the end '
        'without removing words or changing any of those paragraph byte lengths. V1448 rechecks624 '
        'original role/printf/macro/wrap/full228x64 independent font planes,26 names per record,and15 '
        'invalid compiler cases;remaining layout findings='+str(findings)+'. Seven one-byte physical-role '
        'CPU counterfactuals are fully4MiB-audited;voice1 uses original logical Gerhard16 with the '
        'physical First Mate slot empty. No actual own-capture/surrender event,registered ROM or '
        'completion credit is claimed. Counts1323 complete(985 revised338 retained),1435 source/prose;'
        '112 reviewed-incomplete COMMON(24 loss/surrender16 sinking34 aftermath38 older),plus broader '
        'shared/routes/raw prose. Current playable/native parent V1430 does not include this new '
        'research repair. Canonical,V997,separate graphics/all18 plaques and later older-record '
        're-audit remain unchanged/open;goal active.')
    ledger['latest_checkpoint'] = summary
    ledger['research_checkpoints'].append({'id':'V1449-ship-loss-surrender24-source-prose-and-native-research',
        'manuscript':str(MANUSCRIPT),'source_context':doc['source_context'],'native_fonts':str(FONTS),
        'native_runtime':str(RUNTIME),'completed_entries_added':0,'source_prose_reviews_added':24,
        'native_layout_findings_remaining':findings,'full_goal_complete':False})
    ledger['formatting_watchlist']['ship_loss_surrender_research'] = {'native_IDs':IDS,'source_prose_manuscript':str(MANUSCRIPT),
        'source_context':doc['source_context'],'native_font_evidence':str(FONTS),'native_runtime_evidence':str(RUNTIME),
        'literal_names_uniform_margins_and_bounds_research_verified':True,'layout_findings_remaining':findings,
        'registered_ROM_repair_and_original_events_still_pending':True,'global_formatting_audit_complete':False}
    assert len(ledger['reviewed_but_incomplete_COMMON_IDs'])==len(drafts['native_message_IDs'])==112
    assert len(set(completed)|set(ledger['reviewed_but_incomplete_COMMON_IDs']))==1434
    assert sum(ledger['source_prose_reviewed_counts_by_file'].values())==1435
    for key in ['records_editorially_completed','records_revised_and_integrated','retained_wordings_editorially_completed',
        'completed_editorial_record_counts_by_file','current_integrated_candidate','current_native_relocation_reference',
        'source_pins','unresolved_graphics_work','older_record_reaudit_after_full_editorial_goal','raw_source_coverage_revisit']:
        assert ledger[key]==before[key],key
    save(ledger_path,ledger)
    document = Path('docs/ship_loss_surrender_v1449_source_checkpoint.md');assert not document.exists()
    document.write_text('# V1449 ship loss and surrender source/native review\n\n'+summary+
        '\n\n## Required next gates\n\nInspect every generated preview and resolve any remaining word/phrase '
        'boundary findings. Then verify complete native copies/cache transitions and prior escape/shop '
        'formats,approve the exact v2 manuscript through the natural-dialogue-v2 gates,and register a '
        'complete V1430 successor with exact clean-input reconstruction. Finish ordinary cold boots and '
        'representative original own-capture/own-surrender/enemy-surrender events,visible text,dismissals '
        'and transitions before closing the three families. Do not inject numeric messages,lower Hull or '
        'crew,force RNG/results,or infer an original event from CPU counterfactuals. Preserve the original '
        'ship status,surrender probability and flagship/result branches. Current V1430 remains unchanged '
        'and retains the already completed enemy-capture8 family.\n',encoding='utf-8')
    for name in ['translation_progress.md','known_issues.md','todo.md','editorial_review_goal.md']:
        with (Path('docs')/name).open('a',encoding='utf-8',newline='\n') as handle:
            handle.write('\n\n## V1449 loss/surrender24 source and native research\n\n'+summary+
                '\n\nSee [checkpoint](ship_loss_surrender_v1449_source_checkpoint.md).\n')
    save(ROOT/'source_review_receipt.json',{'manuscript':str(MANUSCRIPT),'manuscript_sha256':sha(MANUSCRIPT.read_bytes()),
        'completed':1323,'source_prose':1435,'source_prose_reviews_added':24,'completed_entries_added':0,
        'draft_revisions':24,'draft_retained':0,'reviewed_incomplete_COMMON':112,
        'native_layout_findings_remaining':findings,'native_font_cases':624,'native_dispatch_ABI_cases':529364,
        'registered_release_and_original_events_still_pending':True,
        'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    print('1435 source/prose reviewed;1323 complete unchanged.24 new reports remain open for native finalization,integration and original events.',flush=True)
