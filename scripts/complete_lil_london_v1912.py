"""Credit London after source, native, representative actual and release gates."""
from copy import deepcopy
import os
from pathlib import Path
from shutil import copy2
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.approve_lil_london_references_v1907 import DOC as DOC_PATH, MAP as MAP_PATH, ACTUAL as ACTUAL_PATH
NEW, MAP, ACTUAL = map(str,(DOC_PATH, MAP_PATH, ACTUAL_PATH))
from scripts.register_lil_london_v1908b import ROOT as REL, PROFILE
from scripts.verify_lil_london_release_v1910 import ROM
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/lil_London_completion_v1912')
FINAL = Path('translations/lil_london_final_review_v1.json')
LEDGER = Path('translations/editorial_review_current_v1.json')
HANDOFF = Path('docs/editorial_handoff_current.md')
GUIDE = Path('E:/Rota Nova translations/Guide screenshots/V1909 Lil London verified')
NAV = Path('work/analysis/lil_London_revised_navigation_v1904/closed_revised_B26_unit_and_next_context.json')

if __name__ == '__main__':
    assert not ROOT.exists() and not FINAL.exists() and not GUIDE.exists()
    doc, mapping, release, startup, actual, nav = map(read, (NEW, MAP,
        REL/'registered_release_verification.json', REL/'ordinary_startup_verification.json', ACTUAL, NAV))
    digest = sha(ROM.read_bytes())
    assert digest == release['candidate_sha256'] == startup['candidate_sha256'] == actual['candidate_sha256']
    assert release['complete_reconstruction_byte_exact']
    assert release['registered_ROM_whole_file_byte_exact_to_actual_scene_research_ROM']
    assert startup['all8_complete_startup_title_NewGame_frames_exact'] and startup['no_battery_save_savestate_or_fixtures']
    assert actual['all105_activated_revised_speeches210_holds_complete_native_independent_actual_glyphs']
    assert actual['same228_original_commands_results_and_event_transitions']
    assert actual['all_inputs_capture_hashes4MiB_snapshots_and_three_coordinate_footprints_verified']
    assert actual['all_readonly_observer_boundaries_and_host_restoration_pass']
    assert sha(ROM.with_suffix('.manifest.json').read_bytes()) == release['manifest_sha256']
    assert sha(Path(release['patch']).read_bytes()) == release['patch_sha256']
    assert mapping['external_references_complete']
    block = IlnkContainer.parse(NdsImage.open(ROM).read_file('/data/SC2.DK4')).blocks[26]
    clean = IlnkContainer.parse(NdsImage.open('work/clean.nds').read_file('/data/SC2.DK4')).blocks[26]
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
        assert row['contextual_review_sequence_index'] in range(111)
        assert row['source_meaning'] and row['localization_note']
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
    assert len(rows) == 111 and sum(r['editorial_decision']=='revise' for r in rows) == 81
    assert sum(r['individually_activated_in_current_build'] for r in rows) == 105
    ids = {r['id'] for r in rows}
    raw_ledger = LEDGER.read_bytes()
    ledger = read(LEDGER)
    before = deepcopy(ledger)
    assert (ledger['records_editorially_completed'], ledger['records_revised_and_integrated'],
        ledger['retained_wordings_editorially_completed'], ledger['records_with_source_and_prose_pass']) == (1580,1196,384,1807)
    assert ids == set(ledger['reviewed_but_incomplete_route_record_IDs']['/data/SC2.DK4'])
    ROOT.mkdir(parents=True)
    (ROOT/'ledger_before.json').write_bytes(raw_ledger)
    (ROOT/'handoff_before.md').write_bytes(HANDOFF.read_bytes())
    scope = ('London SC2 B26: all 111 speeches received a clean-Japanese, full-exchange contextual review; 81 revisions and 30 justified retentions. '
        'The recognition, monster rumor, Clifford reveal, clothing joke, dinner, wary alliance proposal and Amsterdam dye direction preserve facts, humor and character voices. '
        'All 111 native/independent font planes, 888 macro/alignment cases, 262 commands, 92 typed spans, 460 relocated native cases, exact inverse restoration, 336 loads and 672 parent modes per ROM pass. '
        'The revised original path covers 105 speeches and 210 full matching actual/native holds, all 228 original command results, four art pauses, the timed outfit pan and normal London return at frame 86310. '
        'Five Gerhard speeches and one Retainer97 fallback were not individually activated; their source-bound shared presenters and complete native checks pass. FE anonymous dialogue uses its separate 228x48 mode1 paper consumer. '
        'Three disclosed fixtures own 16 coordinate bytes each. Full 4 MiB footprints, inputs, captures and read-only observer restoration pass. '
        'Registered V1909 equals the complete tested research ROM. Only SC2 B26 grows 864 bytes from V1875; all 335 other blocks, other files/components, ARM9, COMMON, fonts, graphics and 123040 staged bytes remain exact. '
        'All 480 manifest batches, 114 accepted layers, prior profiles, 13 invalid-release controls, exact clean-input patch and eight fresh fixture-free startup frames pass. '
        'This is targeted headless gameplay, not a full route or hardware test. The full fresh editorial goal remains active, including 116 incomplete COMMON entries and broader story/shared/random/player prose. Graphics, all18 plaques and the later older-record technical re-audit remain separate and unfinished. V1492 stays promoted.')
    visual = ROOT/'registered_gameplay_and_visual_reconciliation.json'
    save(visual, dict(registered_ROM_equals_entire_actual_research_ROM=True,
        all111_native_previews_and16_selected_revised_actual_panels_viewed=True,
        automated210_actual_glyph_holds_distinct_from16_visual_samples=True,
        all8_fresh_startup_title_NewGame_controls_actually_viewed=True,
        no_new_individual_visit_claim_for6_conditional_speeches=True,
        proofs={str(p):sha(Path(p).read_bytes()) for p in (NEW,MAP,ACTUAL,NAV,
            REL/'registered_release_verification.json',REL/'ordinary_startup_verification.json')}, full_goal_complete=False))
    family = 'Lil-London-Clifford111'
    save(FINAL, dict(format='dk4-editorial-final-family-review-v1', family=family,
        file_path='/data/SC2.DK4', blocks=[26], record_IDs=sorted(ids), records=rows,
        revised_count=81, retained_count=30, candidate=str(ROM), candidate_sha256=digest,
        actual_scope=scope, reference_map=MAP, final_proof=str(visual),
        source_native_registered_and_representative_actual_gates_passed=True, full_goal_complete=False))
    ledger['completed_editorial_families'].append(dict(id=family,file_path='/data/SC2.DK4',blocks=[26],
        record_IDs=sorted(ids),final_review=str(FINAL),revised_count=81,retained_count=30,
        actual_verification_scope=scope,records=rows))
    unit = next(u for u in ledger['coverage_units'] if u['id']=='Lil-London-Clifford111-source-prose')
    assert set(unit['record_IDs']) == ids
    unit.update(status='superseded-by-complete-family',completed_family=family,final_review=str(FINAL))
    ledger['coverage_units'].append(dict(id=family,file_path='/data/SC2.DK4',blocks=[26],record_IDs=sorted(ids),
        status='complete-source-native-registered-and-representative-original-gameplay',final_review=str(FINAL),
        actual_proofs=[ACTUAL,str(visual)],individually_observed_record_count=105,offline_only_record_count=6,
        completed_entries_added=111,full_goal_complete=False))
    for u in ledger['coverage_units']:
        if u['id']=='all-route-scenes':
            u.update(reviewed_route_records=289,completed_route_records=289,
                next='Continue the full fresh contextual pass through all remaining storylines and shared/random/player prose; reconcile prior reviews explicitly before fresh-pass credit.')
    ledger['records_editorially_completed'] += 111
    ledger['records_revised_and_integrated'] += 81
    ledger['retained_wordings_editorially_completed'] += 30
    ledger['completed_editorial_record_counts_by_file']['/data/SC2.DK4'] += 111
    for file, pending_ids in ledger['reviewed_but_incomplete_route_record_IDs'].items():
        ledger['reviewed_but_incomplete_route_record_IDs'][file] = [i for i in pending_ids if i not in ids]
    drafts = ledger['active_source_prose_drafts']
    for name, pending_ids in drafts['route_record_subsets_pending'].items():
        drafts['route_record_subsets_pending'][name] = [i for i in pending_ids if i not in ids]
    drafts['manuscripts'].append(NEW)
    drafts.update(status='116-reviewed-COMMON-and-broader-fresh-contextual-prose-open',
        note='Stockholm51 and London111 complete in V1909. Every remaining storyline, earlier translation, shared/random scene and player-facing prose remains in full contextual scope.')
    ledger.setdefault('integrated_candidate_reference_history',[]).append(deepcopy(ledger['current_integrated_candidate']))
    ledger['current_integrated_candidate'] = dict(path=str(ROM),sha256=digest,profile=PROFILE,
        MESFILE_sha256=release['COMMON_sha256'],ARM9_sha256=release['ARM9_sha256'],SC2_sha256=release['SC2_sha256'],
        patch=release['patch'],patch_sha256=release['patch_sha256'],manifest=str(ROM.with_suffix('.manifest.json')),
        status='experimental-verified-editorial-checkpoint-not-promoted',details=scope,full_goal_complete=False)
    ledger.setdefault('native_completed_reference_history',[]).append(deepcopy(ledger['current_native_relocation_reference']))
    ledger['current_native_relocation_reference'].update(candidate=str(ROM),candidate_sha256=digest,
        COMMON_sha256=release['COMMON_sha256'],ARM9_sha256=release['ARM9_sha256'],SC2_sha256=release['SC2_sha256'])
    ledger['latest_registered_editorial_candidate'] = {**release,'status':'experimental-verified-London111',
        'final_review':str(FINAL),'actual_proof':str(visual),'startup_controls_and_editorial_completion_pending':False}
    watch=ledger['formatting_watchlist']['Lil_London_Clifford111']
    watch['resolved_scene_presentation_prefixes_and_record_IDs']=watch.pop('pending_scene_presentation_prefixes_and_record_IDs')
    watch.update(status='complete-in-V1909',final_review=str(FINAL),
        all111_source_native_registered_and_representative_actual_gates_passed=True,
        six_conditional_speeches_not_individually_activated=True)
    ledger['next_route_scene_editorial_packet'] = dict(file_path='/data/SC2.DK4',candidate=str(ROM),
        prior_reviewed_blocks=[22,120,23,24,27,26],prior_blocks_editorially_complete=True,
        next_source_scene_selection_pending=True,
        next='Inventory original EV2 dependencies after actual London return86310. Verify event128 before assuming B25. Continue the full contextual pass or pending COMMON with original context.')
    fresh = ledger['contextual_story_natural_dialogue_pass_v1871']
    assert fresh['fresh_pass_records_explicitly_reread']==162 and fresh['fresh_pass_records_integrated']==51
    assert len(set(fresh['record_IDs']))==162 and ids<=set(fresh['record_IDs'])
    fresh['previous_outside_family_count_snapshot']=fresh.pop('historical_completed_records_outside_this_family_need_evidence_reconciliation')
    fresh.update(fresh_pass_records_integrated=162,fresh_pass_records_pending_native_actual_release=0,
        latest_completed_family=family,latest_final_review=str(FINAL),
        historical_completed_records_outside_reconciled_fresh_pass=1529,
        prior_counts_are_historical_not_total_fresh_pass_completion=True,
        coverage_note='Stockholm51 and London111 explicitly reread and integrated after V1871. Other existing reviews require evidence reconciliation and are not automatically fresh-pass completions.')
    fresh['reconciled_families']=[dict(id='Lil-Stockholm-Hodram51',records=51,final_review='translations/lil_stockholm_final_review_v1.json'),
        dict(id=family,records=111,final_review=str(FINAL))]
    summary = 'V1912 London111 complete: 1691 historical editorial completions (1277 revised, 414 retained), 1807 source/prose reviewed. The fresh V1871 contextual pass has 162 explicitly reread and integrated records; other prior reviews require reconciliation. '+scope
    ledger['latest_checkpoint'] = summary
    ledger['research_checkpoints'].append(dict(id='V1912-London111-complete',proof=str(ROOT/'completion_receipt.json'),
        completed_entries_added=111,source_prose_reviews_added=0,full_goal_complete=False))
    for key in ('unresolved_graphics_work','reviewed_but_incomplete_COMMON_IDs','source_prose_reviewed_counts_by_file',
                'records_with_source_and_prose_pass','older_record_reaudit_after_full_editorial_goal'):
        assert ledger[key] == before[key],key
    assert ledger['records_editorially_completed'] == sum(ledger['completed_editorial_record_counts_by_file'].values()) == 1691
    assert ledger['records_revised_and_integrated']+ledger['retained_wordings_editorially_completed'] == 1691
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
    extra = [('London_normal_return',nav['terminal_capture'],nav['terminal_capture_sha256'])]
    for i,art in enumerate(actual['original_art2000_interstitials']):
        hold=art['holds'][1]
        extra.append((f'Original_art_pause_{i+1}',hold['capture'],hold['capture_sha256']))
    for label,hold in actual['original4905_art_pan'].items():
        if label in ('before','after'):
            extra.append(('Outfit_pan_'+label,hold['capture'],hold['capture_sha256']))
    for label, src, expected in extra:
        assert sha(Path(src).read_bytes()) == expected
        dst = GUIDE/(label+'.png')
        copy2(src,dst)
        photos.append(dict(id=label,path=str(dst),sha256=sha(dst.read_bytes()),source_capture=src))
    save(GUIDE/'provenance.json',dict(candidate=str(ROM),candidate_sha256=digest,captures=photos,
        source_proof=ACTUAL,proof_sha256=sha(Path(ACTUAL).read_bytes()),
        actual_speeches=105,conditional_speeches_not_individually_activated=6,
        three_each16_coordinate_byte_fixtures=True,targeted_headless_emulator_not_full_route_or_hardware=True))
    pending = LEDGER.with_name('editorial_review_current_v1912_pending.json')
    assert not pending.exists() and LEDGER.read_bytes() == raw_ledger
    save(pending,ledger)
    os.replace(pending,LEDGER)
    Path('docs/lil_london_v1912_completion.md').write_text('# V1912 London editorial integration\n\n'+summary+
        f'\n\nCandidate: {ROM.as_posix()}\n\nSHA256: {digest}\n\nPatch SHA256: {release["patch_sha256"]}\n\nFinal review: {FINAL.as_posix()}\n',encoding='utf-8')
    for name in ('translation_progress.md','known_issues.md','todo.md','editorial_review_goal.md'):
        with (Path('docs')/name).open('a',encoding='utf-8') as f:
            f.write('\n\n## V1912 London111 complete\n\n'+summary+'\n\nSee [completion](lil_london_v1912_completion.md).\n')
    text = HANDOFF.read_text(encoding='utf-8')
    text = text.replace('# Current editorial handoff - V1882','# Current editorial handoff - V1912',1)
    start = text.index('## Current coverage and registered release')
    end = text.index('## Latest completed scene: Lil trade routes and officers, SC2 B24')
    current = f'''## Current coverage and registered release

- Ledger: translations/editorial_review_current_v1.json. **1691 historical completions = 1277 revised + 414 retained; 1807 source/prose reviewed.**
- Fresh V1871 contextual pass: 162 explicitly reread and integrated (Stockholm51 + London111). Prior1529 completions retain historical evidence and require reconciliation; do not automatically count them as fresh full-context completion.
- Completed per file: 1402 COMMON + 289 SC2; reviewed: 1518 COMMON + 289 SC2. No active reviewed-incomplete route drafts.116 incomplete COMMON and broader shared/routes/player prose remain.
- Latest registered experimental: {ROM.as_posix()}, profile {PROFILE}; 480 manifest batches /114 accepted layers.
- Candidate SHA256: {digest}.
- Clean-input patch: {release['patch']};SHA256 {release['patch_sha256']};whole-ROM reconstruction exact.
- Canonical baseline unchanged: out/raphael_natural_v2_accepted_base.nds SHA2563cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe.
- Clean work/clean.nds SHA256f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d.
- V1492 remains promoted. No new promotion,commit orpush. AllROMs andearlier translations preserved.
- ARM9 {release['ARM9_sha256']};COMMON {release['COMMON_sha256']};SC2 {release['SC2_sha256']}. Staged123040bytes unchanged.

## London B26 complete - V1912

{scope}

- Final review: {FINAL.as_posix()};approved manuscript: {NEW};map: {MAP}.
- Compiler: dk4tool/patch/lil_london_editorial.py; registered config: translations/lil_london_editorial_release_v1.json.
- Release proof: {REL.as_posix()}/registered_release_verification.json;startup proof: {REL.as_posix()}/ordinary_startup_verification.json. All8 frames viewed.
- Approval: work/analysis/lil_London_approval_v1907/final_source_reference_approval.json. All111 native panels and16 selected actual panels viewed; all210 actual glyph holds pass automated complete-pixel checks.
- Actual proof: {ACTUAL}; normal return86310.105 observed /6 conditional offline; not111 individual visits.
- Relocation: work/analysis/lil_London_relocation_v1899/nested_source_relocation_research.json. B26 grows6256 to7120 bytes (+864), preserving262 commands,92 typed spans and exact inverse restoration.460 target native span cases pass.
- Native fonts: work/analysis/lil_London_font_approval_v1898/all111_complete_native_font_and_macro_reconciliation.json.888 macro/alignment cases; only24 physical line-count warnings narrowly waived. FE uses separate mode1 geometry228x48, with all6 original FE holds matched and all3 final parity targets rechecked.
- Controls: dk4tool/dialogue/lil_london_profile.py binds original B26/runtime only. Gerhard10,Clifford1c andRetainer97 use the original shared progressive presenter; FE has a separate private profile. Global profiles unchanged.5Gerhard+1Retainer conditional speeches have no individual visit claim.
- Entry census: work/analysis/lil_London_reference_census_v1905/all262_commands92_relative_sites_and_shipped_entry_census.json. Clean/current/research each preserve original24070 entry; no literal aliases. Both versions pass336 whole loads/cache hits and672 parent modes.
- Completion receipt: {ROOT.as_posix()}/completion_receipt.json. Guide screenshots: {GUIDE.as_posix()} (105speeches,4art pauses,outfit pan,town return).
- Frozen failed producers1890/1893/1908 are preserved.1890 assumed the unvisited fallback appeared;1890b records only four actual controls.1893's clean-code span included one registered macro call and miscopied two branch words;1893b binds the original controls around the three registered macro calls.1908 stopped before writes on mixed Path/string sorting;1908b normalizes metadata and passes13 invalid-release gates.
- All test/build jobs are terminal: original1884/session54400, revised1903/session84654, navigator1904/session1687, builder1909/session73488 and fresh startup controls. No active emulator should be inferred from old notes.

## Previously completed Stockholm checkpoint

Stockholm51 remains complete and inherited byte-for-byte. See docs/lil_stockholm_v1878_completion.md and translations/lil_stockholm_final_review_v1.json. Its36 actual/15 conditional-offline scope is unchanged. Do not repeat its completed checks without a concrete new risk.

### Exact next work

Inventory original EV2 dependencies in the actual London return snapshot: E:/Rota Nova translations/Generated/work/emulation_v193/lil_London_revised_run_v1903_RESEARCH_ONLY/frame_086310_arm9_ram.bin. Registered V1909 is whole-ROM identical to that test image. Verify event128 before assuming B25 or a follow-up Amsterdam dye scene. Continue source-first full-exchange review of the next relevant storyline or the116 pending COMMON entries. Prioritize broad town/random capture and distinct display risks; individual visits to all conditional lines are not required.

Reconcile earlier translated storylines explicitly before fresh-pass credit. The full objective, graphics/all18 plaques and later older-record technical re-audit remain open. Preserve all ROMs and earlier translations. V1492 remains promoted; no new promotion or push.

'''
    tail=text[end:].replace('### Process state and next action','### Historical B24 process note (superseded by V1912)',1)
    HANDOFF.write_text(text[:start]+current+tail,encoding='utf-8')
    save(ROOT/'completion_receipt.json',dict(candidate=str(ROM),candidate_sha256=digest,patch=release['patch'],
        patch_sha256=release['patch_sha256'],final_review=str(FINAL),completed_before_after=[1580,1691],
        source_prose_reviewed_unchanged=1807,revised_added=81,retained_added=30,
        fresh_contextual_records_explicitly_reread=162,guide_captures=photos,
        ledger_sha256=sha(LEDGER.read_bytes()),handoff_sha256=sha(HANDOFF.read_bytes()),
        all_required_source_native_representative_actual_registered_patch_startup_visual_gates_passed=True,
        full_goal_remains_active=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print(dict(historical_complete=1691,revised=1277,retained=414,source_prose_reviewed=1807,
               fresh_contextual_reconciled=162,actual_speeches=105,conditional_offline=6,guide_captures=len(photos),full_goal_remains_active=True))

