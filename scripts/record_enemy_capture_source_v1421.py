"""Record eight source/prose reviews and the unapproved native repair evidence."""
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save

ROOT = Path('work/analysis/enemy_capture_source_v1421')
MANUSCRIPT = Path('translations/enemy_capture_editorial_manuscript_v1.json')
FONTS = Path('work/analysis/enemy_capture_fonts_v1420/native_font_research.json')
LAYOUT = Path('work/analysis/enemy_capture_layout_v1416/native_layout_research.json')
RUNTIME = Path('work/analysis/enemy_capture_runtime_v1418/native_runtime_verification.json')
IDS = list(range(2082,2090))

if __name__=='__main__':
    assert not ROOT.exists()
    doc,fonts,layout,runtime = [read(p) for p in [MANUSCRIPT,FONTS,LAYOUT,RUNTIME]]
    assert [r['message_id'] for r in doc['records']]==IDS
    assert (doc['revised'],doc['retained'])==(3,5)
    assert sha(Path(doc['source_context']).read_bytes())==doc['source_context_sha256']
    assert all(all(r['review'][g] for g in ['source','context','localization','naturalness'])
        and not r['review']['formatting'] for r in doc['records'])
    assert len(layout['cases'])==208 and len(layout['findings'])==170
    assert len(fonts['cases'])==208 and len(fonts['invalid_compiler_inputs_rejected'])==15
    assert len(fonts['findings'])==53 and fonts['manuscript_sha256']==sha(MANUSCRIPT.read_bytes())
    assert all(r['full228x64_native_and_independent_font_exact'] for r in fonts['cases'])
    scope = read('work/analysis/enemy_capture_runtime_v1418/scope_proof.json')
    assert scope['total_cases']==529325 and runtime['native_exact_dispatch_ABI_memory_and_external_reference_proven']
    for row in fonts['sheets_for_visual_review']:
        assert sha(Path(row['path']).read_bytes())==row['sha256']
    ledger_path = Path('translations/editorial_review_current_v1.json')
    ledger = read(ledger_path);before = deepcopy(ledger)
    assert (ledger['records_editorially_completed'],ledger['records_with_source_and_prose_pass'])==(1315,1403)
    completed = [n for f in ledger['completed_editorial_families'] for n in f.get('native_message_IDs',[])]
    pending = ledger['reviewed_but_incomplete_COMMON_IDs']
    assert len(completed)==len(set(completed))==1314 and len(pending)==len(set(pending))==88
    assert not set(IDS)&(set(completed)|set(pending))
    ROOT.mkdir(parents=True)
    save(ROOT/'coverage_before_source_review.json',before)
    ledger['records_with_source_and_prose_pass'] += 8
    ledger['records_with_source_prose_drafts'] = ledger['records_with_source_and_prose_pass']
    ledger['source_prose_reviewed_counts_by_file']['/COMMON/MESFILE.DK4'] += 8
    ledger['reviewed_but_incomplete_COMMON_IDs'] = sorted(pending+IDS)
    drafts = ledger['active_source_prose_drafts']
    drafts['native_message_IDs'] = sorted(drafts['native_message_IDs']+IDS)
    assert str(MANUSCRIPT) not in drafts['manuscripts']
    drafts['manuscripts'].append(str(MANUSCRIPT))
    drafts['manuscript_record_subsets_pending'][str(MANUSCRIPT)] = IDS
    drafts['status'] = '8-individual-capture16-sinking34-aftermath38-older-reviewed-entries-open'
    drafts['note'] = ('Capture8 has source/context/prose review and research-only literal-name/wrap repair. '
        '53 long-name wrap findings remain;native layout approval,registered ROM/exact patch and original '
        'visible capture/dismissal/transition gates remain pending. Existing88 other incomplete entries stay open.')
    unit = 'Shared-individual-enemy-ship-capture8-source-prose'
    assert unit not in {r['id'] for r in ledger['coverage_units']}
    ledger['coverage_units'].append({'id':unit,'status':'source-context-prose-reviewed-layout-refinement-release-gameplay-pending',
        'native_message_IDs':IDS,'manuscript':str(MANUSCRIPT),'source_context':doc['source_context'],
        'completed_entries_added':0,'full_goal_complete':False})
    summary = ('V1421 source/context/prose-reviews eight individual enemy capture reports2082-2089:three proposed '
        'revisions and five justified retentions.2083 restores enemy;2086 becomes We took the enemy ship%s!;'
        '2088 restores enemy and faithfully expresses took over. Each preserves one original ship-name%s '
        'argument,with no authored breaks/alignment or invented casualty/sinking/fleet-wide result. '
        'Original74050/74058 selects53F0C/table02117B00 and the attacker officer from55DC4(attacker,8). '
        'All206 existing actor choices and earlier actual V1404 Charles18/2082 at10700,Hanse Cog,Hull30/Crew0 '
        'are source/context evidence only;10600 is still visible duel-defeat dialogue,not a capture hold. '
        'V1416 exposes original unscoped capture-path defects:FA/IC/FI/FO/FU sequences inside ship names are '
        'misread as commands and long reports exceed the view.160 of208 cases alter/split names and94 have '
        'width findings(170 unique cases). A research-only exact caller membership activates the existing '
        'literal-name formatter. Numeric selector bias512 replaces384,pointer bias remains896,all historical '
        'numeric dispatch thresholds are adjusted by128. The selector stays188 bytes and gate172 bytes;'
        'all sections/BSS/cache/ITCM/arena and123040 staged bytes remain exact. V1417 stopped before output '
        'at an186-byte estimate;V1417b proves188 after even-row padding. V1418 passes529325 native selector/'
        'ABI/guard cases,3668 old modal outputs238 wrong-parent5 edge controls and140 whole-memory status '
        'cases. V1420 passes208 full228x64 native/independent font planes,literal names,uniform6px visible '
        'margins,complete first/final letters,bounds and15 compiler rejection cases. All8 sheets/64 native '
        'preview panels were visually inspected;53 long-name single-word final rows remain unresolved '
        'layout findings. No formatting approval,registered ROM,new emulator activation or completion '
        'credit is granted. Counts1315 complete(977 revised338 retained),1411 source/prose;96 reviewed-'
        'incomplete COMMON(8 capture16 sinking34 aftermath38 older),plus broader shared/routes/raw prose. '
        'Playable V1404 still lacks this research repair. Canonical,V997,graphics/all18 plaques and later '
        'older-record re-audit remain unchanged/open;goal active.')
    ledger['latest_checkpoint'] = summary
    ledger['research_checkpoints'].append({'id':'V1421-enemy-capture8-source-prose-and-native-research',
        'manuscript':str(MANUSCRIPT),'source_context':doc['source_context'],
        'native_fonts':str(FONTS),'native_runtime':str(RUNTIME),'completed_entries_added':0,
        'source_prose_reviews_added':8,'native_layout_findings_remaining':53,'full_goal_complete':False})
    ledger['formatting_watchlist']['individual_enemy_capture_research'] = {
        'native_IDs':IDS,'source_prose_manuscript':str(MANUSCRIPT),'unfixed_path_evidence':str(LAYOUT),
        'research_font_evidence':str(FONTS),'research_runtime_evidence':str(RUNTIME),
        'literal_names_uniform_margins_and_bounds_research_verified':True,
        'long_name_wrap_findings_remaining':53,'registered_ROM_repair_and_actual_capture_transition_pending':True,
        'global_formatting_audit_complete':False}
    assert len(ledger['reviewed_but_incomplete_COMMON_IDs'])==len(drafts['native_message_IDs'])==96
    assert len(set(completed)|set(ledger['reviewed_but_incomplete_COMMON_IDs']))==1410
    assert sum(ledger['source_prose_reviewed_counts_by_file'].values())==1411
    for key in ['records_editorially_completed','records_revised_and_integrated','retained_wordings_editorially_completed',
        'completed_editorial_record_counts_by_file','current_integrated_candidate','current_native_relocation_reference',
        'source_pins','unresolved_graphics_work','older_record_reaudit_after_full_editorial_goal','raw_source_coverage_revisit']:
        assert ledger[key]==before[key],key
    save(ledger_path,ledger)
    visual = {'native_font_research':str(FONTS),'native_font_research_sha256':sha(FONTS.read_bytes()),
        'all8_sheets_and64_native_preview_panels_actually_viewed':True,
        'literal_FALCON_ICARUS_FIFOFOFU_names_and_all_native_letters_uniform_margins_bounds_pass':True,
        'long_names_create_awkward_single_word_final_rows':True,'layout_findings_remaining':53,
        'no_formatting_release_GPU_gameplay_or_completion_approval':True,'sheets':fonts['sheets_for_visual_review']}
    save(ROOT/'visual_research_review.json',visual)
    document = Path('docs/enemy_capture_v1421_source_checkpoint.md')
    assert not document.exists()
    document.write_text('# V1421 individual enemy ship capture review\n\n'+summary+
        '\n\n## Next required work\n\nRefine the actual formatter\'s complete-word layout for long runtime names '
        'without shortening source-faithful prose merely to pass a fit check. Distinguish an atomic long ship '
        'name on its own row from an avoidable orphan predicate such as captured!. Preserve the exact '
        'source-owned188-byte table and172-byte gate,all earlier logical memberships and123040 staged bytes. '
        'The gate currently uses every owned byte;do not add code or move literal/status data without a '
        'source-bound ownership/reference/callee-state proof. Final native copy/cache/escape/shop regressions, '
        'registered full-stack integration,clean-input exact patch,ordinary cold boots and representative '
        'original capture/dismissal/reward/return verification are still required. Do not promote canonical '
        'or mark the eight records complete from CPU research.\n',encoding='utf-8')
    for name in ['translation_progress.md','known_issues.md','todo.md','editorial_review_goal.md']:
        with (Path('docs')/name).open('a',encoding='utf-8',newline='\n') as handle:
            handle.write('\n\n## V1421 individual enemy capture source and formatting research\n\n'+summary+
                '\n\nSee [checkpoint](enemy_capture_v1421_source_checkpoint.md).\n')
    save(ROOT/'source_review_receipt.json',{'manuscript':str(MANUSCRIPT),'manuscript_sha256':sha(MANUSCRIPT.read_bytes()),
        'completed':1315,'source_prose':1411,'source_prose_reviews_added':8,'completed_entries_added':0,
        'draft_revisions':3,'draft_retained':5,'reviewed_incomplete_COMMON':96,
        'native_layout_findings_remaining':53,'native_font_cases':208,'native_dispatch_ABI_cases':529325,
        'visual_review':str(ROOT/'visual_research_review.json'),
        'registered_release_and_original_visible_gameplay_still_pending':True,
        'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    print('1411 source/prose reviewed;1315 complete unchanged. Capture8 remains open for53 layout findings,integration and gameplay.',flush=True)
