"""Credit Hamburg81 after source/native/revised/registered/patch/startup gates."""
from copy import deepcopy
import os
from pathlib import Path
from shutil import copy2
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.approve_lil_hamburg_references_v1968 import DOC, CHOICES, MAP, ACTUAL
from scripts.lil_hamburg_release_paths_v1972 import ROOT as RELEASE, PROFILE, ROM
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/lil_Hamburg_completion_v1974')
FINAL = Path('translations/lil_hamburg_final_review_v1.json')
LEDGER = Path('translations/editorial_review_current_v1.json')
HANDOFF = Path('docs/editorial_handoff_current.md')
GUIDE = Path('E:/Rota Nova translations/Guide screenshots/V1971 Lil Hamburg recruitment verified')

if __name__ == '__main__':
    assert not ROOT.exists() and not FINAL.exists() and not GUIDE.exists()
    doc, choices, mapping, actual, release, startup = map(read,(DOC,CHOICES,MAP,ACTUAL,
        RELEASE/'registered_release_verification.json',RELEASE/'ordinary_startup_verification.json'))
    digest = sha(ROM.read_bytes())
    assert digest == release['candidate_sha256'] == startup['candidate_sha256'] == actual['candidate_sha256']
    assert release['complete_reconstruction_byte_exact'] and release['registered_ROM_whole_file_byte_exact_to_actual_scene_research_ROM']
    assert release['all484_batches114_accepted_layers_and_prior_profiles_preserved']
    assert startup['all8_complete_startup_title_NewGame_frames_exact'] and startup['no_battery_save_savestate_or_fixtures']
    for flag in ('all79_activated_revised_speeches158_holds_complete_native_independent_actual_glyphs',
        'both_revised_choice_labels_two_actual_holds_complete_native_ink_and_bounds',
        'all3_FE_panels_six_actual_holds_match_separate_paper_planes',
        'original_join_command_and_complete_bottom_screen_ink_preserved',
        'same116_original_B74_commands_results_and_event_transitions',
        'all_inputs_capture_hashes4MiB_snapshots_and_three_access_footprints_verified',
        'all_readonly_observer_boundaries_and_host_restoration_pass'):
        assert actual[flag]
    assert mapping['external_references_complete']
    assert sha(ROM.with_suffix('.manifest.json').read_bytes()) == release['manifest_sha256']
    assert sha(Path(release['patch']).read_bytes()) == release['patch_sha256']
    lint = read(RELEASE/'frozen_input_style_findings.json')
    assert len(lint) <= 1 and all(r['code'] == 'I001' for r in lint)
    blocks = IlnkContainer.parse(NdsImage.open(ROM).read_file('/data/SC2.DK4')).blocks
    jp = IlnkContainer.parse(NdsImage.open('work/clean.nds').read_file('/data/SC2.DK4')).blocks
    changes = {r['id']:r for r in release['stage']['changed_records']}
    observed = {r['id']:r for r in actual['revised_speech_observations']}
    refs = {r['id']:r for r in mapping['blocks'][0]['text_records']}
    rows = []
    for draft in doc['records']+choices['records']:
        row = deepcopy(draft)
        change = changes[row['id']]
        at = change['new_offset']
        value = blocks[74][at:at+change['new_bytes']]
        source = bytes.fromhex(row['source_hex'])
        ja = row['source_reference']['offset']
        assert jp[74][ja:ja+len(source)] == source and jp[74][ja+len(source)] == 0
        assert blocks[74][at+len(value)] == 0 and all(row['review'].values())
        is_choice = row['id'].startswith('DK4_CHOICE_')
        if is_choice:
            assert value.decode('ascii') == row['english']
            current_reference = dict(offset=at,bytes=len(value),hex=value.hex(),text=value.decode('ascii'),
                command_offset=mapping['blocks'][0]['choice_commands'][0]['new_offset'],option_index=row['option_index'])
            holds = actual['revised_choice']['holds']
        else:
            ref = refs[row['id']]
            assert value.hex() == ref['target_hex'] and value[:1] == source[:1]
            assert blocks[74][at-5:at+1].hex() == row['source_complete_preamble_hex']
            current_reference = dict(offset=at,bytes=len(value),header_offset=at-5,record_index=blocks[74][:at].count(b'\0'))
            holds = observed[row['id']]['holds']
        row.update(previous_current_reference=row['current_reference'],previous_current_text_hex=row['current_text_hex'],
            current_reference=current_reference,current_text_hex=value.hex(),current_English=row['english'],
            completed_candidate_reference=str(ROM),completed_candidate_sha256=digest,reference_map=str(MAP),actual_proof=str(ACTUAL),
            individually_activated_in_current_build=True,actual_holds=holds,
            decision='revised-and-integrated' if row['editorial_decision'] == 'revise' else 'retained-with-justification',
            status='complete-source-native-registered-and-representative-original-gameplay')
        if is_choice:
            row['individually_selected_in_current_build'] = row['option_index'] == 0
            row['individually_visible_in_current_build'] = True
        else:
            row['previous_current_stored_English'] = row.get('current_stored_English')
            row['current_stored_English'] = value[1:].decode('cp932')
        row['context'] = row['context'].replace('registered integration remains pending','registered V1971 integration and exact clean-input patch pass')
        if row['editorial_decision'] == 'retain-wording': row['retained_wording_justification'] = row['localization_note']
        rows.append(row)
    assert len(rows) == 81 and sum(r['editorial_decision'] == 'revise' for r in rows) == 46
    assert len(observed) == 79 and all(len(r['actual_holds']) == 2 for r in rows)
    ids = {r['id'] for r in rows}
    raw = LEDGER.read_bytes()
    ledger = read(LEDGER)
    before = deepcopy(ledger)
    assert (ledger['records_editorially_completed'],ledger['records_revised_and_integrated'],ledger['retained_wordings_editorially_completed'],
        ledger['records_with_source_and_prose_pass']) == (1750,1316,434,1947)
    assert ids == set(ledger['reviewed_but_incomplete_route_record_IDs']['/data/SC2.DK4'])
    fresh = ledger['contextual_story_natural_dialogue_pass_v1871']
    assert fresh['fresh_pass_records_explicitly_reread'] == 302 and fresh['fresh_pass_records_integrated'] == 221
    assert ids <= set(fresh['record_IDs']) and fresh['fresh_pass_records_pending_native_actual_release'] == 81
    scope = (
        'Hamburg B74: 79 speeches and two tutorial choice labels reviewed from clean Japanese as a complete exchange; '
        '46 revisions and 35 justified retentions preserve the wife misunderstanding, manners clash, Lil\'s defense of Camille, '
        'Gerhard\'s limited apology, naval-admiral/private-fleet history, reluctant recruitment and title/name joke. '
        'Current Battery, Quarters and Boarding Leader terms are source-bound. All 79 native/independent planes and 632 macro/alignment cases, '
        'two labels/eight style planes/six VM cases, 123 command mappings, 20 relative spans/100 relocated native cases and inverse restoration pass. '
        'Revised actual gameplay covers all 79 speeches in 158 complete matching holds, including three FE panels/six holds, '
        'the original join panel/two holds, both menu labels/two holds, original choice0 lesson, all 116 original command results and normal Hamburg return at76170. '
        'Choice1 has source/native-VM coverage without individual selection. Nineteen representative revised panels, join/menu/return and all eight fresh fixture-free startup frames were viewed. '
        'Two inherited fixtures own16 coordinate bytes each; Hamburg access owns16 coordinate bytes and four synthetic company-funds bytes set60000. '
        'All other4MiB bytes, input/capture hashes and read-only observer restoration pass. No earned travel/funds, full-route or hardware claim. '
        'Registered V1971 equals the entire tested research ROM. Only SC2 B74 grows168bytes from V1945; 335 other blocks, every other file/component, ARM9, COMMON, fonts, graphics and123040 staged bytes remain exact. '
        'All484 manifest batches/114 accepted layers, prior profiles, 20 invalid-release controls, exact clean-input patch reconstruction and eight ordinary startup controls pass. '
        'Full fresh editorial goal remains active: 116 incomplete COMMON entries, every remaining storyline/earlier translation/shared shop/town/random/player-facing text, '
        '1529 historical completions requiring reconciliation, separate graphics/all18 plaques and the later older-record technical re-audit. V1492 stays promoted.')
    ROOT.mkdir(parents=True)
    (ROOT/'ledger_before.json').write_bytes(raw)
    (ROOT/'handoff_before.md').write_bytes(HANDOFF.read_bytes())
    visual = ROOT/'registered_gameplay_and_visual_reconciliation.json'
    save(visual,dict(registered_ROM_equals_entire_actual_research_ROM=True,
        all79_native_previews_and19_selected_revised_actual_panels_viewed=True,
        revised_three_FE_panels_join_two_label_menu_and_normal_Hamburg_return_viewed=True,
        automated158_actual_speech_holds_separate_from19_visual_samples=True,
        all8_fresh_startup_title_NewGame_controls_actually_viewed=True,choice1_not_individually_selected=True,
        frozen_private_profile_style_only_I001_exclusion_preserves_validated_inputs=True,
        failed_control1953_expected_host_closed_but1933_was_scene_checkpoint_corrected_by_later_terminal_receipt=True,
        failed_navigator1966_capture_wait_expired_before49440_same_process_continued_in1966b=True,
        failed_audit1967_assumed_later_Port_context_corrected_to_exact_original_arrival_context_in1967b=True,
        no_equivalent_original_gameplay_rerun=True,
        evidence={str(p):sha(p.read_bytes()) for p in (DOC,CHOICES,MAP,ACTUAL,RELEASE/'registered_release_verification.json',
            RELEASE/'ordinary_startup_verification.json',RELEASE/'frozen_input_style_findings.json')},full_goal_complete=False))
    family = 'Lil-Hamburg-recruitment81'
    save(FINAL,dict(format='dk4-editorial-final-family-review-v1',family=family,file_path='/data/SC2.DK4',blocks=[74],
        record_IDs=sorted(ids),records=rows,revised_count=46,retained_count=35,candidate=str(ROM),candidate_sha256=digest,
        actual_scope=scope,reference_map=str(MAP),final_proof=str(visual),
        source_native_registered_and_representative_actual_gates_passed=True,full_goal_complete=False))
    ledger['completed_editorial_families'].append(dict(id=family,file_path='/data/SC2.DK4',blocks=[74],record_IDs=sorted(ids),
        final_review=str(FINAL),revised_count=46,retained_count=35,actual_verification_scope=scope,records=rows))
    unit = next(u for u in ledger['coverage_units'] if u['id'] == 'Lil-Hamburg-recruitment81-source-prose')
    unit.update(status='superseded-by-complete-family',completed_family=family,final_review=str(FINAL))
    context_unit = next(u for u in ledger['coverage_units'] if u['id'] == 'Lil-Hamburg-B74-actual-context-unreviewed')
    context_unit.update(status='original-context-reconciled-to-complete-family',completed_family=family,final_review=str(FINAL))
    ledger['coverage_units'].append(dict(id=family,file_path='/data/SC2.DK4',blocks=[74],record_IDs=sorted(ids),
        status='complete-source-native-registered-and-representative-original-gameplay',final_review=str(FINAL),
        actual_proofs=[str(ACTUAL),str(visual)],individually_observed_speech_count=79,offline_only_speech_count=0,
        FE_panel_count=3,visible_choice_label_count=2,individually_selected_choice_index=0,original_join_panel_count=1,
        completed_entries_added=81,full_goal_complete=False))
    for u in ledger['coverage_units']:
        if u['id'] == 'all-route-scenes':
            u.update(reviewed_route_records=429,completed_route_records=429,
                next='Continue full source/scene inventory from verified Hamburg town context; review remaining Lil story/shared town/random prose, then all other routes and explicitly reconcile earlier translations.')
    ledger['records_editorially_completed'] += 81
    ledger['records_revised_and_integrated'] += 46
    ledger['retained_wordings_editorially_completed'] += 35
    ledger['completed_editorial_record_counts_by_file']['/data/SC2.DK4'] += 81
    for path,pending_ids in ledger['reviewed_but_incomplete_route_record_IDs'].items():
        ledger['reviewed_but_incomplete_route_record_IDs'][path] = [i for i in pending_ids if i not in ids]
    drafts = ledger['active_source_prose_drafts']
    for name,pending_ids in drafts['route_record_subsets_pending'].items():
        drafts['route_record_subsets_pending'][name] = [i for i in pending_ids if i not in ids]
    drafts['manuscripts'] += list(map(str,(DOC,CHOICES)))
    drafts.update(status='116-reviewed-COMMON-and-broader-fresh-contextual-prose-open',
        note='Stockholm51,London111,Speyer59 andHamburg81 are integrated inV1971. Continue every remaining storyline,earlier translation,shared shop/town/randomscene andplayer-facing prose. Historical reviews require explicit reconciliation.')
    ledger.setdefault('integrated_candidate_reference_history',[]).append(deepcopy(ledger['current_integrated_candidate']))
    ledger['current_integrated_candidate'] = dict(path=str(ROM),sha256=digest,profile=PROFILE,MESFILE_sha256=release['COMMON_sha256'],
        ARM9_sha256=release['ARM9_sha256'],SC2_sha256=release['SC2_sha256'],patch=release['patch'],patch_sha256=release['patch_sha256'],
        manifest=str(ROM.with_suffix('.manifest.json')),status='experimental-verified-editorial-checkpoint-not-promoted',details=scope,full_goal_complete=False)
    ledger.setdefault('native_completed_reference_history',[]).append(deepcopy(ledger['current_native_relocation_reference']))
    ledger['current_native_relocation_reference'].update(candidate=str(ROM),candidate_sha256=digest,
        COMMON_sha256=release['COMMON_sha256'],ARM9_sha256=release['ARM9_sha256'],SC2_sha256=release['SC2_sha256'])
    ledger['latest_registered_editorial_candidate'] = {**release,'status':'experimental-verified-Hamburg81',
        'final_review':str(FINAL),'actual_proof':str(visual),'startup_controls_and_editorial_completion_pending':False}
    watch = ledger['formatting_watchlist']['Lil_Hamburg_recruitment81']
    watch['resolved_scene_presentation_prefixes_and_record_IDs'] = watch.pop('pending_scene_presentation_prefixes_and_record_IDs')
    watch.update(status='complete-in-V1971',final_review=str(FINAL),all79_speeches_two_labels_native_and_actual_pass=True,
        complete_native_glyphs_bounds_pagination_private_scope_and_revised_transitions_pending=False,choice1_not_individually_selected=True)
    ledger['next_route_scene_editorial_packet'] = dict(file_path='/data/SC2.DK4',
        current_verified_town_context=str(ACTUAL),current_verified_snapshot='E:/Rota Nova translations/Generated/work/emulation_v193/lil_Hamburg_revised_run_v1965_RESEARCH_ONLY/frame_076170_arm9_ram.bin',
        next='Inventory original town/event/shared dialogue from the verified Hamburg checkpoint; select complete source-bound conversations without assuming a numbered next chapter.',
        source_prose_review_complete=False,editorial_review_complete=False,
        note='Preserve completed Stockholm/London/Speyer/Hamburg checks. The Amsterdam dye lead, B25aftermath andnativecatalog Pedro デ Valdes remain separate unresolved leads. Full editorial scope continues.')
    fresh.update(fresh_pass_records_integrated=302,fresh_pass_records_pending_native_actual_release=0,
        latest_contextual_manuscript=str(DOC),latest_contextual_choice_draft=str(CHOICES),latest_completed_family=family,
        latest_final_review=str(FINAL),historical_completed_records_outside_reconciled_fresh_pass=1529,
        coverage_note='Stockholm51,London111,Speyer59 andHamburg81 explicitly reread andintegrated afterV1871. Other1529 historical completions require explicit contextual evidence reconciliation.')
    fresh['reconciled_families'].append(dict(id=family,records=81,final_review=str(FINAL)))
    summary = ('V1974 Hamburg81 complete:1831 historical editorial completions(1362 revised469 retained),1947 source/prose reviewed. '
        'Fresh V1871 contextual pass:302 explicitly reread andintegrated;1529 other historical completions need reconciliation. '+scope)
    ledger['latest_checkpoint'] = summary
    ledger['research_checkpoints'].append(dict(id='V1974-Hamburg81-complete',proof=str(ROOT/'completion_receipt.json'),
        completed_entries_added=81,source_prose_reviews_added=0,full_goal_complete=False))
    for key in ('unresolved_graphics_work','reviewed_but_incomplete_COMMON_IDs','source_prose_reviewed_counts_by_file',
        'records_with_source_and_prose_pass','older_record_reaudit_after_full_editorial_goal'):
        assert ledger[key] == before[key],key
    assert ledger['records_editorially_completed'] == sum(ledger['completed_editorial_record_counts_by_file'].values()) == 1831
    assert ledger['records_revised_and_integrated']+ledger['retained_wordings_editorially_completed'] == 1831
    assert not any(ledger['reviewed_but_incomplete_route_record_IDs'].values())
    assert ledger['goal_status'] == 'active' and not ledger['full_goal_complete']
    GUIDE.mkdir(parents=True)
    copied = []
    for group in actual['revised_speech_observations']:
        source = Path(group['holds'][1]['capture'])
        target = GUIDE/(group['id']+'.png')
        copy2(source,target)
        assert target.read_bytes() == source.read_bytes()
        copied.append(str(target))
    for label,source in (('choice',Path(actual['revised_choice']['holds'][0]['capture'])),
        ('Gerhard_join',Path(actual['revised_join']['holds'][1]['capture'])),
        ('Hamburg_return',Path('E:/Rota Nova translations/Generated/work/emulation_v193/lil_Hamburg_revised_run_v1965_RESEARCH_ONLY/frame_076170_navigation.png'))):
        target = GUIDE/(label+'.png')
        copy2(source,target)
        assert target.read_bytes() == source.read_bytes()
        copied.append(str(target))
    assert len(copied) == 82
    pending = LEDGER.with_name('editorial_review_current_v1974_pending.json')
    assert not pending.exists() and LEDGER.read_bytes() == raw
    save(pending,ledger)
    os.replace(pending,LEDGER)
    details = (f'# V1974 Hamburg completion\n\n{summary}\n\nCandidate: {ROM.as_posix()}\n\nSHA256: {digest}\n\nProfile: {PROFILE}\n\n'
        f'Clean-input patch: {release["patch"]}\n\nPatch SHA256: {release["patch_sha256"]}\n\nFinal review: {FINAL.as_posix()}\n\n'
        f'Source map: {MAP.as_posix()}\n\nActual proof: {ACTUAL.as_posix()}\n\nGuide: {GUIDE}\n\n'
        'Frozen failed predecessors are preserved. V1953 mistook the closed B74 unit for its continuing host; V1953b binds the later terminal receipt. '
        'V1966 safely timed out waiting for the cold boot to reach49440; V1966b continued the same process. '
        'V1967 assumed the later Speyer Port event context; V1967b compares exact original B74arrival context instead. No game/event state was changed to satisfy those assertions. '
        'Focused Ruff passes with the one I001 import-spacing exclusion for the frozen private profile; the new guarded compiler passes without exclusions.\n')
    Path('docs/lil_hamburg_v1974_completion.md').write_text(details,encoding='utf-8')
    for name in ('translation_progress.md','known_issues.md','todo.md','editorial_review_goal.md'):
        with (Path('docs')/name).open('a',encoding='utf-8') as stream:
            stream.write('\n\n## V1974 Hamburg81 complete\n\n'+summary+'\n\nSee [completion](lil_hamburg_v1974_completion.md).\n')
    text = HANDOFF.read_text(encoding='utf-8').replace('# Current editorial handoff - V1952','# Current editorial handoff - V1974',1)
    start = text.index('## Current coverage and registered release')
    end = text.index('## Speyer B128/B25 complete - V1948')
    coverage = f'''## Current coverage and registered release

- Ledger: translations/editorial_review_current_v1.json. **1831 historical completions =1362 revised +469 retained;1947 source/prose reviewed.**
- Fresh V1871 contextual pass:302 explicitly reread andintegrated(Stockholm51 +London111 +Speyer59 +Hamburg81). Prior1529 completions require explicit reconciliation.
- Completed:1402 COMMON +429 SC2;reviewed:1518 COMMON +429 SC2. No active reviewed-incomplete route drafts.116 COMMON andall broader story/shared/town/random/player prose remain.
- Latest registered experimental: {ROM.as_posix()},profile {PROFILE};484 manifest batches /114 accepted layers.
- Candidate SHA256: {digest}.
- Exact clean-input patch: {release['patch']};SHA256 {release['patch_sha256']};whole-ROM reconstruction exact.
- Canonical baseline andclean Japanese ROM unchanged;all ROMs andearlier translations preserved. V1492 stays promoted. No new promotion,commit orpush.
- ARM9 {release['ARM9_sha256']};COMMON {release['COMMON_sha256']};SC2 {release['SC2_sha256']}. Staged123040bytes unchanged.

## Hamburg B74 complete - V1974

{scope}

- Final review: {FINAL.as_posix()};approved prose: {DOC.as_posix()};choices: {CHOICES.as_posix()};map: {MAP.as_posix()}.
- Compiler: dk4tool/patch/lil_hamburg_editorial.py;config:translations/lil_hamburg_editorial_release_v1.json. Source compiler equals the entire tested research ROM;20 invalid-release controls reject before mutation,including FE-as-progressive andmissing FE actual approval.
- Source/control1953b binds every79 complete preamble toclean/current B74 andexact runtime. Original capture V1909 hasexact B74 andARM9 matchingV1945;whole original capture ROM isnot claimed equalV1945. Gerhard10 native selector/name andactual display areproven. FE staysseparate fromprogressive/fallback actor resolution. Globalprofiles unchanged.
- Native1959:76progressive planes+3FE mode1 planes,632 macro/alignment calls;all11 sheets viewed. FE logical228x48,physical row16,onepage;all6oldactual holds reconcile. Only27 physical-source line-count warnings narrowly waived.11 invalid scope/format controls reject. Two choice labels pass8style planes/6VM cases.
- Relocation1960/reference1963:123commands,20typed spans,100relocated native cases,inverse restoration,336loads/cache hits and672parent modes perROM;fresh clean/current/research census contains onlyoriginal24070 entry,no literal aliases.
- Revised audit1967b:79speeches/158complete holds,threeFE/sixholds,join/twoholds,bothlabels/twoholds,originalchoice0,116original results andnormal Hamburgreturn76170.19representative revised panels,join/menu/return and8startup frames viewed. Choice1 notselected.
- Access reusesoriginal two16-byte coordinate fixtures andHamburg20-byte fixture(16coordinates+4synthetic funds60000). Allother4MiB bytes andread-only callbacks/restoration pass;no event/RNG/message/outcome ownership or earnedtravel/funds claim. Arrival event context iscompared withits exact original capture ratherthan assumed tobe thelaterSpeyer Port context.
- Release proof:work/analysis/lil_Hamburg_release_v1970/registered_release_verification.json;startup:ordinary_startup_verification.json. Guide:{GUIDE} (82captures).
- Failed frozen1953/1966/1967 producers arepreserved withsuccessors;see completion doc. Same coldboot continued after firstcapture wait expired;no restart. Alljobs terminal:revised1965/session37264,failednavigator1966/session21005,successor1966b/session42120,builder1971/session50686,andstartup jobs. No liveemulator is implied byold notes.

'''
    text = text[:start]+coverage+text[end:]
    start = text.index('## Current working unit: Hamburg B74 - V1952')
    end = text.index('## Latest completed scene: Lil trade routes and officers, SC2 B24')
    next_work = f'''## Exact next work after Hamburg

Continue the full fresh contextual review ofevery remaining storyline,earlier translation,shared shop/town/randomscene andplayer-facing prose.116 COMMON entries remain incomplete;1529 historical completions needexplicit reconciliation. Capture town/random scenes broadly aspractical withrepresentative story gameplay andfocused tests onlyforconcrete unresolved display/transition risks. Do not repeat completed Stockholm/London/Speyer/Hamburg checks without a newrisk.

Current verified snapshot:E:/Rota Nova translations/Generated/work/emulation_v193/lil_Hamburg_revised_run_v1965_RESEARCH_ONLY/frame_076170_arm9_ram.bin;wholeROM exactregisteredV1971. Nativeevent74 complete;128 and25 incomplete. Inventory original event/shared-town dialogue fromthis Hamburgreturn;do not force aftermath conditions orassume anumbered nextchapter. Amsterdamdye lead andnativecatalog Pedro デ Valdes remainseparate unresolved player-facing leads.

Preserve allROMs andearlier translations. Graphics/all18plaques remainseparate/open. Retain thelaterolder-record technical re-audit afterthefull editorial objective. Fullgoalactive;V1492promoted.

'''
    HANDOFF.write_text(text[:start]+next_work+text[end:],encoding='utf-8')
    save(ROOT/'completion_receipt.json',dict(final_review=str(FINAL),final_review_sha256=sha(FINAL.read_bytes()),
        candidate=str(ROM),candidate_sha256=digest,profile=PROFILE,patch=release['patch'],patch_sha256=release['patch_sha256'],
        completed_entries_added=81,revised_added=46,retained_added=35,historical_completed_after=1831,source_prose_reviewed_after=1947,
        fresh_contextual_reread_and_integrated=302,source_prose_reviews_added=0,actual_revised_speeches=79,actual_complete_speech_holds=158,
        actual_FE_holds=6,actual_menu_holds=2,actual_join_holds=2,guide_captures=copied,
        ledger_sha256=sha(LEDGER.read_bytes()),handoff_sha256=sha(HANDOFF.read_bytes()),
        all_ROMs_and_earlier_translations_preserved=True,full_goal_remains_active=True,
        producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print(dict(historical_completed=1831,revised=1362,retained=469,source_prose_reviewed=1947,
        fresh_contextual_integrated=302,guide_captures=82,full_goal_remains_active=True))
