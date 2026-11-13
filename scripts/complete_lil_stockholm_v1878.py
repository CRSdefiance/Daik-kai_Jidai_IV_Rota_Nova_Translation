"""Credit Stockholm after source, native, representative actual and release gates."""
from copy import deepcopy
import os
from pathlib import Path
from shutil import copy2
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.approve_lil_stockholm_v1873 import NEW, MAP, ACTUAL
from scripts.register_lil_stockholm_v1874b import ROOT as REL, PROFILE
from scripts.verify_lil_stockholm_release_v1876 import ROM
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/lil_Stockholm_completion_v1878')
FINAL = Path('translations/lil_stockholm_final_review_v1.json')
LEDGER = Path('translations/editorial_review_current_v1.json')
HANDOFF = Path('docs/editorial_handoff_current.md')
GUIDE = Path('E:/Rota Nova translations/Guide screenshots/V1875 Lil Stockholm verified')
NAV = Path('work/analysis/lil_Stockholm_revised_navigation_v1865/closed_revised_B27_unit_and_next_context.json')

if __name__ == '__main__':
    assert not ROOT.exists() and not FINAL.exists() and not GUIDE.exists()
    doc, mapping, release, startup, actual, nav = map(read, (NEW, MAP,
        REL/'registered_release_verification.json', REL/'ordinary_startup_verification.json', ACTUAL, NAV))
    digest = sha(ROM.read_bytes())
    assert digest == release['candidate_sha256'] == startup['candidate_sha256'] == actual['candidate_sha256']
    assert release['complete_reconstruction_byte_exact']
    assert release['registered_ROM_whole_file_byte_exact_to_actual_scene_research_ROM']
    assert startup['all8_complete_startup_title_NewGame_frames_exact'] and startup['no_battery_save_savestate_or_fixtures']
    assert actual['all36_activated_revised_speeches72_holds_complete_native_independent_actual_glyphs']
    assert actual['same75_original_commands_results_and_event_transitions']
    assert actual['all_inputs_capture_hashes4MiB_snapshots_and_three_coordinate_footprints_verified']
    assert actual['all_readonly_observer_boundaries_and_host_restoration_pass']
    assert sha(ROM.with_suffix('.manifest.json').read_bytes()) == release['manifest_sha256']
    assert sha(Path(release['patch']).read_bytes()) == release['patch_sha256']
    assert mapping['external_references_complete']
    block = IlnkContainer.parse(NdsImage.open(ROM).read_file('/data/SC2.DK4')).blocks[27]
    clean = IlnkContainer.parse(NdsImage.open('work/clean.nds').read_file('/data/SC2.DK4')).blocks[27]
    refs = {r['id']:r for r in mapping['records']}
    observed = {r['id']:r for r in actual['revised_speech_observations']}
    rows = []
    for draft in doc['records']:
        row = deepcopy(draft)
        ref = refs[row['id']]
        at = ref['new_offset']
        raw = bytes.fromhex(ref['target_hex'])
        ja = row['source_reference']['offset']
        old = bytes.fromhex(row['source_hex'])
        assert block[at:at+len(raw)] == raw and block[at+len(raw)] == 0
        assert clean[ja:ja+len(old)] == old and all(row['review'].values())
        assert row['contextual_review_v1873']['source_and_entire_exchange_reread']
        individual = row['id'] in observed
        row.update(previous_current_reference=row['current_reference'], previous_current_text_hex=row['current_text_hex'],
            current_reference=dict(offset=at, bytes=len(raw), header_offset=at-5, record_index=block[:at].count(b'\0')),
            current_text_hex=raw.hex(), current_English=row['english'],
            completed_candidate_reference=str(ROM), completed_candidate_sha256=digest,
            reference_map=MAP, actual_proof=ACTUAL, individually_activated_in_current_build=individual,
            actual_holds=observed[row['id']]['holds'] if individual else [],
            decision='revised-and-integrated' if row['editorial_decision']=='revise' else 'retained-with-justification',
            status='complete-source-native-registered-and-representative-original-gameplay',
            offline_scope='Exact full source/preamble/macro/native plane,typed relocation,registered target and bounds/pagination checks.')
        if row['editorial_decision']=='retain-wording':
            row['retained_wording_justification'] = row['localization_note']
        rows.append(row)
    assert len(rows) == 51 and sum(r['editorial_decision']=='revise' for r in rows) == 38
    assert sum(r['individually_activated_in_current_build'] for r in rows) == 36
    ids = {r['id'] for r in rows}
    raw_ledger = LEDGER.read_bytes()
    ledger = read(LEDGER)
    before = deepcopy(ledger)
    assert (ledger['records_editorially_completed'], ledger['records_revised_and_integrated'],
        ledger['retained_wordings_editorially_completed'], ledger['records_with_source_and_prose_pass']) == (1529,1158,371,1696)
    assert ids == set(ledger['reviewed_but_incomplete_route_record_IDs']['/data/SC2.DK4'])
    ROOT.mkdir(parents=True)
    (ROOT/'ledger_before.json').write_bytes(raw_ledger)
    (ROOT/'handoff_before.md').write_bytes(HANDOFF.read_bytes())
    scope = ('Stockholm SC2 B27: all 51 speeches reread against clean Japanese as a complete exchange;38 revisions and13 justified retentions. '
        'Lil\'s confrontation,Camille\'s apology,Hodram\'s restrained reassurance andGerhard\'s conditional conversation retain meaning,voice andrelationships. '
        'All51 native-independent font planes and408 macro/alignment calls,102 original commands,24 typed spans120 relocated cases,inverse restoration,and336 loads672 parent modes pass. '
        'Representative actual gameplay covers36 revised speeches72 full matching holds,75 original command/results,original art pause andnormalStockholm return62850. '
        'Fifteen conditional speeches were not individually activated;nine Gerhard0x10 objects inherit the exact source/runtime selector mapped through original Hodram gameplay. '
        'Three disclosed fixtures own16 coordinate bytes each;all4MiB footprints,inputs,captures andreadonly observer restoration pass. '
        'RegisteredV1875 equals the complete tested research ROM. OnlySC2B27 grows280bytes fromV1841;335 other blocks,every other file/component,ARM9,COMMON,fonts,graphics and123040 staged bytes remain exact. '
        'All479 manifest batches114 accepted layers,12 invalid-release controls,exact clean-input patch andeight fresh fixture-free startup frames pass. '
        'No full-route,earned-travel orhardware claim. Full fresh editorial goal remains active;116 incompleteCOMMON,broader all-routes/player prose,graphics/all18 plaques andlater older-record technical re-audit remain open. V1492 stays promoted.')
    visual = ROOT/'registered_gameplay_and_visual_reconciliation.json'
    save(visual, dict(registered_ROM_equals_entire_actual_research_ROM=True,
        prior_seven_native_and_six_actual_sheet_reviews_inherited_with_exact_hashes=True,
        all8_fresh_startup_title_NewGame_controls_actually_viewed=True,
        no_new_individual_visit_claim_for15_conditional_speeches=True,
        proofs={str(p):sha(Path(p).read_bytes()) for p in (NEW,MAP,ACTUAL,NAV,
            REL/'registered_release_verification.json',REL/'ordinary_startup_verification.json')}, full_goal_complete=False))
    family = 'Lil-Stockholm-Hodram51'
    save(FINAL, dict(format='dk4-editorial-final-family-review-v1', family=family,
        file_path='/data/SC2.DK4', blocks=[27], record_IDs=sorted(ids), records=rows,
        revised_count=38, retained_count=13, candidate=str(ROM), candidate_sha256=digest,
        actual_scope=scope, reference_map=MAP, final_proof=str(visual),
        source_native_registered_and_representative_actual_gates_passed=True, full_goal_complete=False))
    ledger['completed_editorial_families'].append(dict(id=family,file_path='/data/SC2.DK4',blocks=[27],
        record_IDs=sorted(ids),final_review=str(FINAL),revised_count=38,retained_count=13,
        actual_verification_scope=scope,records=rows))
    unit = next(u for u in ledger['coverage_units'] if u['id']=='Lil-Stockholm-Hodram51-source-prose')
    assert set(unit['record_IDs']) == ids
    unit.update(status='superseded-by-complete-family',completed_family=family,final_review=str(FINAL))
    ledger['coverage_units'].append(dict(id=family,file_path='/data/SC2.DK4',blocks=[27],record_IDs=sorted(ids),
        status='complete-source-native-registered-and-representative-original-gameplay',final_review=str(FINAL),
        actual_proofs=[ACTUAL,str(visual)],individually_observed_record_count=36,offline_only_record_count=15,
        completed_entries_added=51,full_goal_complete=False))
    for u in ledger['coverage_units']:
        if u['id']=='all-route-scenes':
            u.update(reviewed_route_records=178,completed_route_records=178,
                next='Continue fresh contextual source review through LondonB26,all other storylines andshared/player-facing prose;prior translations not automatically complete forV1871.')
    ledger['records_editorially_completed'] += 51
    ledger['records_revised_and_integrated'] += 38
    ledger['retained_wordings_editorially_completed'] += 13
    ledger['completed_editorial_record_counts_by_file']['/data/SC2.DK4'] += 51
    for file, pending_ids in ledger['reviewed_but_incomplete_route_record_IDs'].items():
        ledger['reviewed_but_incomplete_route_record_IDs'][file] = [i for i in pending_ids if i not in ids]
    drafts = ledger['active_source_prose_drafts']
    for name, pending_ids in drafts['route_record_subsets_pending'].items():
        drafts['route_record_subsets_pending'][name] = [i for i in pending_ids if i not in ids]
    drafts['manuscripts'].append(NEW)
    drafts.update(status='116-reviewed-COMMON-and-broader-fresh-contextual-prose-open',
        note='Stockholm51 complete inV1875. Every remaining storyline,earlier translation,shared/random scene andplayer-facing prose remains in full contextual scope.')
    ledger.setdefault('integrated_candidate_reference_history',[]).append(deepcopy(ledger['current_integrated_candidate']))
    ledger['current_integrated_candidate'] = dict(path=str(ROM),sha256=digest,profile=PROFILE,
        MESFILE_sha256=release['COMMON_sha256'],ARM9_sha256=release['ARM9_sha256'],SC2_sha256=release['SC2_sha256'],
        patch=release['patch'],patch_sha256=release['patch_sha256'],manifest=str(ROM.with_suffix('.manifest.json')),
        status='experimental-verified-editorial-checkpoint-not-promoted',details=scope,full_goal_complete=False)
    ledger.setdefault('native_completed_reference_history',[]).append(deepcopy(ledger['current_native_relocation_reference']))
    ledger['current_native_relocation_reference'].update(candidate=str(ROM),candidate_sha256=digest,
        COMMON_sha256=release['COMMON_sha256'],ARM9_sha256=release['ARM9_sha256'])
    ledger['latest_registered_editorial_candidate'] = dict(**release,status='experimental-verified-Stockholm51',
        final_review=str(FINAL),actual_proof=str(visual))
    ledger['formatting_watchlist']['Lil_Stockholm_Hodram51'].update(status='complete-in-V1875',
        final_review=str(FINAL),revised_displays_not_yet_verified=False,
        all51_source_native_registered_and_representative_actual_gates_passed=True,
        unmapped_control_hex=None,affected_IDs=[],conditional_individual_visits_not_claimed=15)
    ledger['next_route_scene_editorial_packet'] = dict(file_path='/data/SC2.DK4',candidate=str(ROM),
        prior_reviewed_blocks=[22,120,23,24,27],prior_blocks_editorially_complete=True,
        next_source_scene_selection_pending=True,next_source_lead='LondonB26 original111-speech eligible lead;B25 requires128,not24.',
        next='Source-first contextual review ofLondonB26 orpendingCOMMON;broader all-routes/player-prose objective unchanged.')
    fresh = ledger['contextual_story_natural_dialogue_pass_v1871']
    fresh.update(first_reconciled_contextual_family=family,record_IDs=sorted(ids),
        fresh_pass_records_explicitly_reread=51,fresh_pass_records_integrated=51,final_review=str(FINAL),
        historical_completed_records_outside_this_family_need_evidence_reconciliation=1529,
        prior_counts_are_historical_not_total_fresh_pass_completion=True,
        coverage_note='Stockholm51 explicitly reread afterV1871. Other existing reviews retain their evidence but are not automatically recredited to the fresh full-context pass.')
    summary = 'V1878 Stockholm51 complete:1580 historical editorial completions(1196 revised384 retained),1696 source/prose reviewed. FreshV1871 contextual pass explicitly reconciled51;other prior reviews require reconciliation. '+scope
    ledger['latest_checkpoint'] = summary
    ledger['research_checkpoints'].append(dict(id='V1878-Stockholm51-complete',proof=str(ROOT/'completion_receipt.json'),
        completed_entries_added=51,source_prose_reviews_added=0,full_goal_complete=False))
    for key in ('unresolved_graphics_work','reviewed_but_incomplete_COMMON_IDs','source_prose_reviewed_counts_by_file',
                'records_with_source_and_prose_pass','older_record_reaudit_after_full_editorial_goal'):
        assert ledger[key] == before[key],key
    assert ledger['records_editorially_completed'] == sum(ledger['completed_editorial_record_counts_by_file'].values()) == 1580
    assert ledger['records_revised_and_integrated']+ledger['retained_wordings_editorially_completed'] == 1580
    assert ledger['goal_status']=='active' and not ledger['full_goal_complete']
    assert not any(ledger['reviewed_but_incomplete_route_record_IDs'].values())
    GUIDE.mkdir(parents=True)
    photos = []
    for row in rows:
        if not row['actual_holds']:
            continue
        hold = row['actual_holds'][1]
        src = Path(hold['capture'])
        assert sha(src.read_bytes()) == hold['capture_sha256']
        dst = GUIDE/(row['id']+'.png')
        copy2(src,dst)
        photos.append(dict(id=row['id'],path=str(dst),sha256=sha(dst.read_bytes()),source_capture=str(src)))
    extra = [('Stockholm_normal_return',nav['terminal_capture'],nav['terminal_capture_sha256']),
        ('Original_art_pause',actual['original_art2000_interstitial']['holds'][1]['capture'],
         actual['original_art2000_interstitial']['holds'][1]['capture_sha256'])]
    for label, src, expected in extra:
        assert sha(Path(src).read_bytes()) == expected
        dst = GUIDE/(label+'.png')
        copy2(src,dst)
        photos.append(dict(id=label,path=str(dst),sha256=sha(dst.read_bytes()),source_capture=src))
    save(GUIDE/'provenance.json',dict(candidate=str(ROM),candidate_sha256=digest,captures=photos,
        source_proof=ACTUAL,proof_sha256=sha(Path(ACTUAL).read_bytes()),
        actual_speeches=36,conditional_speeches_not_individually_activated=15,
        three_each16_coordinate_byte_fixtures=True,targeted_headless_emulator_not_full_route_or_hardware=True))
    pending = LEDGER.with_name('editorial_review_current_v1878_pending.json')
    assert not pending.exists() and LEDGER.read_bytes() == raw_ledger
    save(pending,ledger)
    os.replace(pending,LEDGER)
    Path('docs/lil_stockholm_v1878_completion.md').write_text('# V1878 Stockholm editorial integration\n\n'+summary+
        f'\n\nCandidate: {ROM.as_posix()}\n\nSHA256: {digest}\n\nPatch SHA256: {release["patch_sha256"]}\n\nFinal review: {FINAL.as_posix()}\n',encoding='utf-8')
    for name in ('translation_progress.md','known_issues.md','todo.md','editorial_review_goal.md'):
        with (Path('docs')/name).open('a',encoding='utf-8') as f:
            f.write('\n\n## V1878 Stockholm51 complete\n\n'+summary+'\n\nSee [completion](lil_stockholm_v1878_completion.md).\n')
    text = HANDOFF.read_text(encoding='utf-8')
    text = text.replace('# Current editorial handoff - V1868','# Current editorial handoff - V1878',1)
    start = text.index('## Current coverage and registered release')
    end = text.index('## Latest completed scene: Lil trade routes and officers, SC2 B24')
    current = f'''## Current coverage and registered release

- Ledger: translations/editorial_review_current_v1.json. **1580 historical completions =1196 revised+384 retained;1696 source/prose reviewed.**
- Fresh V1871 contextual pass explicitly reread/reconciled: Stockholm51. Prior1529 completions retain historical evidence and require reconciliation;do not automatically count them asfresh full-context completion.
- Completed perfile1402COMMON+178SC2;reviewed1518COMMON+178SC2. Noactive reviewed-incomplete route drafts;116 incompleteCOMMON andbroader shared/routes/player prose remain.
- Latest registered experimental: {ROM.as_posix()},profile {PROFILE};479manifest batches/114accepted layers.
- Candidate SHA256: {digest}.
- Clean-input patch: {release['patch']};SHA256 {release['patch_sha256']};whole-ROM reconstruction exact.
- Canonical baseline unchanged: out/raphael_natural_v2_accepted_base.nds SHA2563cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe.
- Clean work/clean.nds SHA256f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d.
- V1492 remains promoted. No new promotion,commit orpush. AllROMs andearlier translations preserved.
- ARM9 {release['ARM9_sha256']};COMMON {release['COMMON_sha256']};SC2 {release['SC2_sha256']}. Staged123040bytes unchanged.

## Stockholm B27 complete - V1878

{scope}

- Final review: {FINAL.as_posix()};approved manuscript: {NEW};map: {MAP}.
- Compiler: dk4tool/patch/lil_stockholm_editorial.py;registered config: translations/lil_stockholm_editorial_release_v2.json.
- Release proof: {REL.as_posix()}/registered_release_verification.json;startup proof: {REL.as_posix()}/ordinary_startup_verification.json. All8 frames viewed.
- Approval: work/analysis/lil_Stockholm_approval_v1873/source_context_and_final_map_approval.json. Existing7 native and6 actual sheet reviews inherited withhash verification;no repeated scene run.
- Actual proof: {ACTUAL};normal return62850. 36observed/15conditional-offline;not51individual visits.
- Completion receipt: {ROOT.as_posix()}/completion_receipt.json. Guide screenshots: {GUIDE.as_posix()} (36speeches,art pause,town return).
- Failed1874 registration stopped on anincorrect expected negative-test count(13 versus12) afterall12 rejected,before registry/builder changes. Frozen successor1874b corrected the count;oldproducer/config/proofs preserved.
- Allnewjobs terminal:builder1875(session43992),newgame1877(session70534),title1877 completed0. Noactive emulator inferred fromoldnotes.

### Exact next work

Continue thefull fresh contextual pass fromcleanJapanese. LondonB26 is anunreviewed111-speech lead. Inspect itscomplete source/current exchange andoriginal context;do notinferB25 eligibility(itrequires128,not24). Alternatively advance116pendingCOMMON wherecontextavailable. Prioritize broad town/random-scene capture andrepresentative risks;noexhaustive conditional-story playthrough required. Reconcile earlier reviewed storyline evidence explicitly before fresh-pass credit.

AllStockholm native/branch/control/gameplay/release checks arecomplete;do notrepeat them absent aconcrete newrisk. Full objective,graphics/all18plaques andlater older-record technical re-audit remainopen.

'''
    HANDOFF.write_text(text[:start]+current+text[end:],encoding='utf-8')
    save(ROOT/'completion_receipt.json',dict(candidate=str(ROM),candidate_sha256=digest,patch=release['patch'],
        patch_sha256=release['patch_sha256'],final_review=str(FINAL),completed_before_after=[1529,1580],
        source_prose_reviewed_unchanged=1696,revised_added=38,retained_added=13,
        fresh_contextual_records_explicitly_reread=51,guide_captures=photos,
        ledger_sha256=sha(LEDGER.read_bytes()),handoff_sha256=sha(HANDOFF.read_bytes()),
        all_required_source_native_representative_actual_registered_patch_startup_visual_gates_passed=True,
        full_goal_remains_active=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print(dict(historical_complete=1580,revised=1196,retained=384,source_prose_reviewed=1696,
               fresh_contextual_reconciled=51,actual_speeches=36,conditional_offline=15,guide_captures=len(photos),full_goal_remains_active=True))
