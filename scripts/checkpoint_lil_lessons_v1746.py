"""Current handoff after FE resolution, native layout approval and revised wind test."""
from copy import deepcopy
from pathlib import Path
import os
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/lil_lessons_checkpoint_v1746')
LEDGER = Path('translations/editorial_review_current_v1.json')
HANDOFF = Path('docs/editorial_handoff_current.md')
DOC = Path('translations/lil_lessons_editorial_manuscript_v3.json')
MENU = Path('translations/lil_lesson_choices_editorial_draft_v2.json')
WIND = Path('work/analysis/lil_revised_wind_v1744/actual_revised_wind_branch_proof.json')
APPROVAL = Path('work/analysis/lil_lesson_layout_approval_v1742/approval_receipt.json')
LOADER = Path('work/analysis/lil_lessons_loader_v1740/whole_SC2_and_lesson_initial_entry_proof.json')

if __name__ == '__main__':
    assert not ROOT.exists()
    wind, approval, loader = map(read, (WIND, APPROVAL, LOADER))
    doc, menu = map(read, (DOC, MENU))
    assert len(wind['all41_original_command_pairs_mapped_and_same_path_results']) == 41
    assert len(wind['all22_executed_speeches44_holds_complete_native_independent_actual_pixels']) == 22
    assert wind['all6_revised_FE_panels_actual_full_ink_matches_prior_composition_contract']
    assert approval['all64_native_formatting_approved_actual_revised_gameplay_still_pending']
    assert sha(DOC.read_bytes()) == approval['manuscript_sha256']
    assert sha(MENU.read_bytes()) == approval['choices_sha256']
    assert loader['all336_whole_blocks_and672_modes_each_pass']
    registry = Path('translations/release_stack.json')
    registry_sha = sha(registry.read_bytes())
    raw = LEDGER.read_bytes(); ledger = read(LEDGER); before = deepcopy(ledger)
    assert (ledger['records_editorially_completed'], ledger['records_with_source_and_prose_pass']) == (1424,1632)
    ROOT.mkdir(parents=True)
    (ROOT/'coverage_before.json').write_bytes(raw)
    (ROOT/'handoff_before.md').write_bytes(HANDOFF.read_bytes())
    visual = ROOT/'actual_wind_visual_review.json'
    save(visual, {'all3_actual_revised_wind_sheets_actually_viewed': True,
        'actual_choice1_menu_and_terminal_Sea_View_captures_actually_viewed': True,
        'complete_source_speakers_nameplates_letters_uniform_left_origins_and_pages_acceptable': True,
        'terminal_is_Sea_View_with_departure_log_not_unobstructed_sailing_or_Bruges_arrival': True,
        'actual_proof': str(WIND), 'actual_proof_sha256': sha(WIND.read_bytes()),
        'revised_B23_other_alternatives_and_registered_release_still_pending': True, 'full_goal_complete': False})
    drafts = ledger['active_source_prose_drafts']
    pending = drafts['route_record_subsets_pending']
    old_doc = next(k for k in pending if k.replace('\\','/') == 'translations/lil_lessons_editorial_manuscript_v2.json')
    old_menu = next(k for k in pending if k.replace('\\','/') == 'translations/lil_lesson_choices_editorial_draft_v1.json')
    assert len(pending[old_doc]) == 60 and len(pending[old_menu]) == 4
    pending[old_doc] = []; pending[old_menu] = []
    pending[str(DOC)] = [r['id'] for r in doc['records']]
    pending[str(MENU)] = [r['id'] for r in menu['records']]
    drafts['manuscripts'].extend([str(DOC), str(MENU)])
    unit = next(u for u in ledger['coverage_units'] if u['id']=='Lil-sailing-lessons64-source-prose')
    unit.update(manuscripts=[str(DOC),str(MENU)],
        status='all64-native-layout-approved;revised-B120-wind22-verified;other-paths-map-and-release-pending',
        native_layout_approval=str(APPROVAL), revised_wind_actual_proof=str(WIND),
        complete_SC2_loader_proof=str(LOADER), FE_actual_multiline_geometry_pending=False)
    ledger['lil_lessons_editorial_v1720'].update(speech_manuscript=str(DOC), choice_manuscript=str(MENU),
        FE_actual_multiline_geometry_pending=False, all64_native_formatting_approved=True,
        revised_B120_wind22_actual_verified=True, revised_wind_actual_proof=str(WIND),
        actual_other_paths_external_reference_approval_and_registered_release_pending=True)
    ledger['formatting_watchlist']['Lil_sailing_lessons64'].update(
        status='all64-open;native-layout-approved;wind22-actual-passed;other-paths-map-release-pending',
        manuscripts=[str(DOC),str(MENU)], FE_actual_context_metric_and_choice_layout_pending=False,
        prior_FE_model12_vs_display16_finding_resolved_by_independent_V365_paper_contract=True,
        all6_revised_FE_full_actual_ink_planes_verified=True, native_layout_approval=str(APPROVAL),
        revised_wind_actual_proof=str(WIND))
    ledger['next_route_scene_editorial_packet'].update(manuscripts=[str(DOC),str(MENU)],
        note='Continue ordinary travel to source-bound B23 crew lesson;verify revised alternatives/choices and transitions. Then approve complete scoped references,register cumulative post-layer,build exact patch and regression controls. B120 wind22 already actual verified;do not repeat its completed tests without a concrete risk.')
    summary = ('V1746 resolves the FE layout-model discrepancy using the independently documented V365 paper contract: '
        'native12-pixel rows compose to16-pixel displayed rows without stretching glyphs. All6 current actual panels '
        'match full ink/blank cells;all9 revised FE panels consume one228x48 native page. All60 speech/system layouts '
        'and4 choice labels are now approved offline/native,with25 specific automatic Japanese/English line-count decisions. '
        'Scoped FE profile only;global profiles and runtime unchanged. Research V1739 is a full V1711 copy changing '
        'only SC2 B1202076-to2316 and B232308-to2584;all334 other blocks and every other file/component exact. '
        'Both original whole-SC2 loaders/cache hits336 and parent modes672 pass per ROM. Revised ordinary no-save '
        'wind replay V1741 ends29930:41 mapped command pairs,22 speeches44 complete pixel-exact holds,6 actual FE '
        'panels,choice1 and original type0 end pass. All3 actual sheets,choice and Sea View departure-log captures '
        'were visually inspected. No B23/Bruges or whole-route claim. Other paths,complete reference approval,registered '
        'integration and exact patch remain pending;all64 entries remain incomplete. Counts1424 complete(1076 revised348 '
        'retained),1632 source/prose,144 pending COMMON plus64 route drafts and broader prose. Registered V1711 and '
        'promoted V1492 unchanged;full goal active,separate graphics/all18 plaques and later older-record re-audit open.')
    ledger['latest_checkpoint'] = summary
    ledger['research_checkpoints'].append({'id':'V1746-Lil-lessons-native-and-revised-wind',
        'proof':str(ROOT/'checkpoint_receipt.json'),'completed_entries_added':0,'source_prose_reviews_added':0,'full_goal_complete':False})
    for key in ['records_editorially_completed','records_revised_and_integrated','retained_wordings_editorially_completed',
        'records_with_source_and_prose_pass','completed_editorial_record_counts_by_file','source_prose_reviewed_counts_by_file',
        'reviewed_but_incomplete_COMMON_IDs','unresolved_graphics_work','current_integrated_candidate']:
        assert ledger[key] == before[key], key
    assert sum(map(len,pending.values())) == 64 and ledger['goal_status']=='active' and not ledger['full_goal_complete']
    temporary = LEDGER.with_name('editorial_review_current_v1746_pending.json')
    assert not temporary.exists() and LEDGER.read_bytes()==raw
    save(temporary,ledger); assert read(temporary)==ledger and LEDGER.read_bytes()==raw
    os.replace(temporary,LEDGER)
    handoff = '''# Current editorial handoff - V1746

## Goal and rules

The full scene-by-scene editorial goal is ACTIVE: natural faithful en-US against clean Japanese, all shared shops/town dialogue, all routes and remaining player prose. Approved names: Rafael, Joakim, Maria, Camille. Do not shrink or mark this goal complete at a batch boundary. No subagents authorized. Sources/ is read-only. Preserve ALL generated ROMs; no pruning. Separate graphics/all18 plaque audit remains unfinished. Wood/borders are accepted; four low-resolution Online bodies excluded; two brown marks retained. Older-record re-audit follows the full editorial goal.

## Verified accounting

1424 complete =1076 revised +348 retained;1632 source/prose reviewed. Completed:1374 COMMON +50 SC2, including Lil opening49. Pending reviewed:144 COMMON +64 Lil lesson entries, plus broader untouched prose. Ledger translations/editorial_review_current_v1.json is authoritative. All64 lesson entries are still incomplete until their remaining gameplay/map/integration/patch gates pass.

## Registered candidate and promotion

- Latest verified registered cumulative candidate: out/all_routes_combined_v1711_candidate.nds, SHA256 251594f89f950f1deb68d6359b6861d6f4a96eb8e9a9045c148d6d6cb64b1201. Physical E:/Rota Nova translations/Generated/out/.
- Profile all-routes-unified-v1711:474 manifest batches,114 accepted layers; experimental. Exact patch out/all_routes_combined_v1711_candidate.xdelta, SHA256 a2d9092b28b26cf213ca874d8c10f8a80ed379509dbfa0aaff9cdce6eceb0528.
- Release proof work/analysis/lil_opening_release_v1710/registered_release_verification.json;successful producer scripts/verify_lil_opening_release_v1712.py.
- Canonical construction parent out/raphael_natural_v2_accepted_base.nds, SHA256 3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe.
- Clean patch input work/clean.nds, SHA256 f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d.
- V1492 remains promoted, tag promoted-v1492. Last pushed commit53c0b58c4be456731024a1e594c3121360395296,branch codex/combined-routes-v89. No fresh commit/push/promotion authorization in this continuation.

## Do not repeat completed Lil opening

SC2 B22 opening49 is complete:43 revisions6 retentions;49 speeches98 actual full-font holds,90 original commands,three crew joins and normal Amsterdam return. Registered V1711 is byte-identical to the tested research ROM. All8 startup controls and inherited shop676/677 fixes pass. Source terminal proved next scene B120,not guessed B23 or Bruges. See translations/lil_opening_final_review_v1.json and work/analysis/lil_opening_completion_v1715b/completion_receipt.json. Eight finalized guide images are in E:/Rota Nova translations/Guide screenshots/V1711 Lil Amsterdam opening verified.

## Current lesson work: native approved, revised wind path verified

Current manuscripts: translations/lil_lessons_editorial_manuscript_v3.json (60 speech/system records) and translations/lil_lesson_choices_editorial_draft_v2.json (4 labels). Prior versions are frozen.45 proposed revisions19 retentions. Use established Sail Handler and Half Open/Full Open. B23R44 restores Camille offering to become admiral;B23R9 restores surprise lessons are not finished. B23R69 states the complete Half Open automatic Sail Handler rule in two lines. No source facts shortened for allocation.

- Full source inventory:work/analysis/lil_lessons_source_v1717/complete_lesson_source_context.json. B12027 speeches,B2333;124 recursively nested commands. Top-level walking alone misses branches.
- Original36 relative skip sites:work/analysis/lil_lesson_branches_v1722/original_relative_skip_operand_proof.json;360 source/current cases.0100 always skips;0200 skips on previous0;0300 on previous1;destination=command+4+u16span. Type2 updates prior choice;type3 preserves it.
- Native60 planes:work/analysis/lil_lesson_layout_v1725/all60_native_font_reconciliation.json. All8 sheets andrefined05 viewed. Full4MiB/ABI/guards and native/independent glyph planes pass.
- FE resolution:work/analysis/lil_FE_display_v1737/actual_paper_contract_and_all9_reviewed_FE_panels.json. Exact captured mode1 geometry228x48,font6x12;prior independent V365 paper contract maps logical12 to displayed16 row origins. All6 current actual full ink/blank cells match;all9 reviewed FE targets fit one real page and complete native planes. Not an independent whole-GPU trace. New9 preview sheet actually viewed.
- Choices:work/analysis/lil_lesson_choice_ui_v1735/original_choice_VM_geometry_and_native_pixels.json. Original count/getters,width/geometry,12 selected0/1/cancel cases and4 labels2styles pass. Actual native auto-sizing shrinks after removing unused old padding. Current/reviewed comparison sheet viewed;no geometry/font/palette change.
- Native/visual approval:work/analysis/lil_lesson_layout_approval_v1742/approval_receipt.json (successful producer1742c).25 exact per-record line-break-count decisions;all64 native formatting gates approved. Generic global profile unchanged;FE only scoped to exact runtime-bound post-layer.
- Research resizing:work/analysis/lil_lesson_relocation_v1731/nested_source_relocation_research.json. B1202076->2316(+240),B232308->2584(+276);60 texts4 labels36 relative operands;180 relocated native branch cases;inverse restores every original logical byte.32 parity spaces repaint exactly. External-reference approval still incomplete.
- Research ROM:work/analysis/lil_lessons_research_v1739/lil_lessons_V1711_derived_RESEARCH_ONLY.nds,SHA256 ee95dc2b9415c0438147b0c29e631bf8e882e26dfdf5876d9e6b9651cb8b8b14. Only SC2 B23/B120 differ from V1711;334 other blocks and every other file/component exact. It is NOT a registered release,parent or user handoff.
- Whole-loader proof:work/analysis/lil_lessons_loader_v1740/whole_SC2_and_lesson_initial_entry_proof.json.336 original EV2-selected whole block loads/cache hits and672 original parent modes pass per ROM;entry+8,0x2400 capacity,payload/cache/tail guards preserved. SDK IO only bridged. Later paths/reference approval still pending.
- Revised actual wind proof:work/analysis/lil_revised_wind_v1744/actual_revised_wind_branch_proof.json. Cold boot V1741,no preloaded save/savestate/cheats/fixtures,terminal29930.41 original command pairs match exact relocated offsets/results;22 speeches44 complete pixel-exact holds,including all6 FE panels. Choice1 result[2,1],mapped0300 skip180,finaltype0[0,1]. Prior choice1 survives in unused secondword;do not demand[0,0].262 read-only callbacks,zero errors/mismatches,host restored. All3 sheets,menu andterminal visually viewed. Terminal is Sea View with departure log,not unobstructed sailing or Bruges. Other B120 alternatives and B23 still pending.

## Live process and exact next action

Fresh ordinary navigation runner scripts/run_lil_lesson_navigation_v1745.py has been launched as exec session35207;check the SAME handle/current authoritative process before resuming. It cold-boots/replays the verified wind input to pause29930,then consumes append-only work/analysis/lil_lesson_navigation_v1745/navigation.jsonl. Captures E:/Rota Nova translations/Generated/work/emulation_v193/lil_lesson_navigation_v1745_RESEARCH_ONLY. Live observer work/analysis/lil_lesson_navigation_v1745/live_observer_progress.json. No gameplay fixtures enabled. V1741 andall preceding runs are terminal. Never restart solely because an observation times out.

Next:advance original sailing/normal event handling to locate B23;use captured native source identity,not scene guesses. Verify both revised choice branches and later crew lesson/pages/transitions. Authorized isolated location/health/inventory/route cheats may help testing if needed;own exact fields and document all4MiB preservation. Do not inject event choices/outcomes/flags to manufacture completion. Finish source-bound interpreter caller/reference census plus all36 branch maps,then approve a scoped lesson relocation contract. Add a registered cumulative post-layer after lil_opening_editorial,build exact clean patch,verify unchanged components/startup/shops and reconcile actual research bytes to registered release. Only then close64. Full editorial goal remains much broader.

## Earlier COMMON and process safeguards

Pending COMMON:614-628;750-752;1911-1930;1994-2010;2022-2037;2058-2081;2090-2105;2147-2178;2192.750-752 context-unmapped:production matches are CS lengths;alternate testdata SC3B164CS0101word750 unclassified. Close-sighting V1693 stopped at Syracuse Dock;unloaded null enemy mobile is not inactivity proof. Use actual open-water context;never force seen flags. Vicinity/Armed Latina actual UI pending. Do not repeat completed hot-spring RNG campaign.

Read AGENTS.md,build_continuity_protocol,release_stack and relevant known_issues before ROM changes;natural_dialogue_workflow/dialogue_delegation_protocol before prose. Executed producers/proofs frozen;use explicit successors. Approval1742 used nonexistent diagnostic.as_dict;1742b compared optionalNone fields to compact schema;1742c normalizes absent optional fields and passes. No output was written by failed approvals. Older1724c alignment metadata equals3 due loop variable overwrite;actual adapter captured correct0239B104. Derive from ITCM01FFCF24 tail andverify188 original helper bytes. Do not mutate old proof.

V1710 release config locks global profiles.py/layout.py/encoder.py. Do not change them for FE;use local source/runtime-bound profile. Existing default literal policy remains forbid;no global guard relaxation. Preserve123040 staged bytes. Python C:/Python314/python.exe,PYTHONUTF8=1,PYTHONPATH=.;.deps. Sandbox launcher fails P-drive credentials;scoped escalation is needed. out andwork/analysis junction to E;archive lexical absolute paths without resolve(). No fresh final guide screenshots from unregistered lesson research.
'''
    HANDOFF.write_text(handoff,encoding='utf-8')
    Path('docs/lil_lessons_v1746_checkpoint.md').write_text('# V1746 Lil lesson checkpoint\n\n'+summary+'\n\nSee the current handoff and work/analysis/lil_lessons_checkpoint_v1746/checkpoint_receipt.json for exact references.\n',encoding='utf-8')
    for name in ('translation_progress.md','known_issues.md','todo.md','editorial_review_goal.md'):
        with (Path('docs')/name).open('a',encoding='utf-8') as f:
            f.write('\n\n## V1746 Lil native layout and revised wind verification\n\n'+summary+'\n\nSee [checkpoint](lil_lessons_v1746_checkpoint.md).\n')
    assert sha(registry.read_bytes())==registry_sha
    save(ROOT/'checkpoint_receipt.json', {'completed':1424,'source_prose_reviewed':1632,
        'new_completed':0,'all64_lesson_entries_remain_incomplete':True,'native_layout_approved':64,
        'actual_revised_wind_speeches_verified':22,'actual_revised_full_font_holds':44,
        'proofs':{str(p):sha(p.read_bytes()) for p in (WIND,APPROVAL,LOADER,DOC,MENU,visual)},
        'registered_candidate_and_registry_unchanged':True,'ledger_sha256':sha(LEDGER.read_bytes()),
        'handoff_sha256':sha(HANDOFF.read_bytes()),'producer_sha256':sha(Path(__file__).read_bytes()),
        'next_live_runner':'scripts/run_lil_lesson_navigation_v1745.py','last_known_exec_session':35207,
        'full_goal_complete':False})
    print('Handoff/ledger V1746 saved:FE resolved,64 native layouts approved,wind22 actual verified;all64 still incomplete,full goal active.')
