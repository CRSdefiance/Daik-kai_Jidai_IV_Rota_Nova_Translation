"""Credit59 Speyer entries only after native, representative actual and release gates."""
from copy import deepcopy
import os
from pathlib import Path
from shutil import copy2
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.approve_lil_speyer_references_v1942 import DOC,CHOICES,MAP,ACTUAL
from scripts.register_lil_speyer_v1944 import ROOT as RELEASE,PROFILE
from scripts.verify_lil_speyer_release_v1946 import ROM
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_Speyer_completion_v1948')
FINAL=Path('translations/lil_speyer_final_review_v1.json')
LEDGER=Path('translations/editorial_review_current_v1.json')
HANDOFF=Path('docs/editorial_handoff_current.md')
GUIDE=Path('E:/Rota Nova translations/Guide screenshots/V1945 Lil Speyer verified')
TOWN_GUIDE=Path('E:/Rota Nova translations/Guide screenshots/V1909 Hamburg recruitment original context unreviewed')
TOWN=Path('work/analysis/lil_Hamburg_arrival_navigation_v1933/closed_original_scene_context.json')
TOWN_SOURCE=Path('work/analysis/lil_Hamburg_arrival_navigation_v1933/full_source_context_uncredited.json')

if __name__=='__main__':
    assert not ROOT.exists()and not FINAL.exists()and not GUIDE.exists()and not TOWN_GUIDE.exists()
    doc,choices,mapping,actual,release,startup,town,town_source=map(read,(DOC,CHOICES,MAP,ACTUAL,
        RELEASE/'registered_release_verification.json',RELEASE/'ordinary_startup_verification.json',TOWN,TOWN_SOURCE))
    digest=sha(ROM.read_bytes())
    assert digest==release['candidate_sha256']==startup['candidate_sha256']==actual['candidate_sha256']
    assert release['complete_reconstruction_byte_exact']and release['registered_ROM_whole_file_byte_exact_to_actual_scene_research_ROM']
    assert release['all482_batches114_accepted_layers_and_prior_profiles_preserved']
    assert startup['all8_complete_startup_title_NewGame_frames_exact']and startup['no_battery_save_savestate_or_fixtures']
    assert actual['all51_activated_revised_speeches102_holds_complete_native_independent_actual_glyphs']
    assert actual['both_revised_choice_labels_two_actual_holds_complete_native_ink_and_bounds']
    assert actual['same107_original_B128_commands_results_and_event_transitions']
    assert actual['all_inputs_capture_hashes4MiB_snapshots_and_three_access_footprints_verified']
    assert actual['all_readonly_observer_boundaries_and_host_restoration_pass']
    assert mapping['external_references_complete']
    assert sha(ROM.with_suffix('.manifest.json').read_bytes())==release['manifest_sha256']
    assert sha(Path(release['patch']).read_bytes())==release['patch_sha256']
    lint=read(RELEASE/'frozen_input_style_findings.json')
    assert len(lint)==2 and {r['code']for r in lint}=={'I001','RUF007'}
    blocks=IlnkContainer.parse(NdsImage.open(ROM).read_file('/data/SC2.DK4')).blocks
    jp=IlnkContainer.parse(NdsImage.open('work/clean.nds').read_file('/data/SC2.DK4')).blocks
    changes={r['id']:r for r in release['stage']['changed_records']}
    observed={r['id']:r for r in actual['revised_speech_observations']}
    rows=[]
    for draft in doc['records']+choices['records']:
        row=deepcopy(draft)
        change=changes[row['id']]
        at=change['new_offset']
        value=blocks[row['block']][at:at+change['new_bytes']]
        source=bytes.fromhex(row['source_hex'])
        ja=row['source_reference']['offset']
        assert jp[row['block']][ja:ja+len(source)]==source and jp[row['block']][ja+len(source)]==0
        assert blocks[row['block']][at+len(value)]==0 and all(row['review'].values())
        is_choice=row['id'].startswith('DK4_CHOICE_')
        if is_choice:
            assert value.decode('ascii')==row['english']
            current_reference=dict(offset=at,bytes=len(value),hex=value.hex(),text=value.decode('ascii'),
                command_offset=next(b for b in mapping['blocks']if b['block']==128)['choice_commands'][0]['new_offset'],
                option_index=row['option_index'])
            individual=True
            holds=actual['revised_choice']['holds']
        else:
            ref=next(r for b in mapping['blocks']for r in b['text_records']if r['id']==row['id'])
            assert value.hex()==ref['target_hex']and value[:1]==source[:1]
            current_reference=dict(offset=at,bytes=len(value),header_offset=at-5,record_index=blocks[row['block']][:at].count(b'\0'))
            individual=row['id']in observed
            holds=observed[row['id']]['holds']if individual else[]
        row.update(previous_current_reference=row['current_reference'],previous_current_text_hex=row['current_text_hex'],
            current_reference=current_reference,current_text_hex=value.hex(),current_English=row['english'],
            completed_candidate_reference=str(ROM),completed_candidate_sha256=digest,
            reference_map=str(MAP),actual_proof=str(ACTUAL),individually_activated_in_current_build=individual,
            actual_holds=holds,decision='revised-and-integrated'if row['editorial_decision']=='revise'else'retained-with-justification',
            status='complete-source-native-registered-and-representative-original-gameplay')
        if is_choice:row['individually_selected_in_current_build']=row['option_index']==0
        else:
            row['previous_current_stored_English']=row.get('current_stored_English')
            row['current_stored_English']=value[1:].decode('cp932')
        row['context']=row['context'].replace('registered integration remains pending','registered V1945 integration and exact clean-input patch now pass')
        if row['editorial_decision']=='retain-wording':row['retained_wording_justification']=row['localization_note']
        rows.append(row)
    assert len(rows)==59 and sum(r['editorial_decision']=='revise'for r in rows)==39
    assert len(observed)==51 and sum(r['individually_activated_in_current_build']for r in rows)==53
    ids={r['id']for r in rows}
    raw=LEDGER.read_bytes()
    ledger=read(LEDGER)
    before=deepcopy(ledger)
    assert(ledger['records_editorially_completed'],ledger['records_revised_and_integrated'],ledger['retained_wordings_editorially_completed'],
        ledger['records_with_source_and_prose_pass'])==(1691,1277,414,1866)
    assert ids==set(ledger['reviewed_but_incomplete_route_record_IDs']['/data/SC2.DK4'])
    ROOT.mkdir(parents=True)
    (ROOT/'ledger_before.json').write_bytes(raw)
    (ROOT/'handoff_before.md').write_bytes(HANDOFF.read_bytes())
    scope=('Speyer B128/B25:57 speeches and two choice labels received clean-Japanese full-exchange review;39 revisions and20 justified retentions. '
        'All57 native/independent font planes,456 macro/alignment cases,two native labels/eight style planes/six selection-cancel cases,137 commands,48 typed spans,240 relocated native cases and inverse restoration pass. '
        'Representative revised gameplay covers51 B128 speeches with102 complete matching glyph holds,both menu labels in two full matching holds,the original choice0 explanatory path,107 original command/results and normal Hamburg town return at93780. '
        'The97 fallback,two alternate-choice replies and all three B25 aftermath speeches have source/native coverage without individual activation;choice1 was not selected. '
        'Two inherited fixtures own16 coordinate bytes each;the Hamburg fixture owns16 coordinate bytes and one four-byte company-funds field,set to60000 against the original50000 threshold. '
        'Every other4MiB byte,inputs,capture hashes and read-only observer restoration pass. No earned-travel,earned-funds,full-route or hardware claim. '
        'Registered V1945 equals the entire tested research ROM. Only SC2 B25(+28) and B128(+80) change from V1909;334 other blocks,all other files/components,ARM9,COMMON,fonts,graphics and123040 staged bytes remain exact. '
        'All482 manifest batches,114 accepted layers,prior profiles,18 invalid-release controls,exact clean-input patch and eight fresh fixture-free startup frames pass. '
        'The same original run also captured Hamburg B74:79 speeches,the join panel and tutorial choice0;that source inventory is not editorial completion. '
        'The full fresh editorial objective remains active,including116 incomplete COMMON entries,other storylines/shared/town/random/player prose,separate graphics/all18 plaques and the later older-record technical re-audit. V1492 stays promoted.')
    visual=ROOT/'registered_gameplay_and_visual_reconciliation.json'
    save(visual,dict(registered_ROM_equals_entire_actual_research_ROM=True,
        all57_native_previews_and12_selected_revised_actual_panels_viewed=True,
        revised_two_label_menu_and_normal_Hamburg_return_viewed=True,
        automated102_actual_speech_holds_and_two_menu_holds_distinct_from12_visual_samples=True,
        all8_fresh_startup_title_NewGame_controls_actually_viewed=True,
        six_speeches_not_individually_activated_and_choice1_not_selected=True,
        frozen_production_input_style_only_lint_exclusions={'dk4tool/dialogue/lil_speyer_profile.py':['I001'],
            'dk4tool/patch/lil_speyer_editorial.py':['RUF007']},
        style_exclusion_reason='Preserve frozen validated inputs: one import-group blank line and the inherited adjacent-pair zip loop. Remaining focused Ruff checks pass with these exact per-file exclusions.',
        evidence={str(p):sha(p.read_bytes())for p in(DOC,CHOICES,MAP,ACTUAL,RELEASE/'registered_release_verification.json',
            RELEASE/'ordinary_startup_verification.json',RELEASE/'frozen_input_style_findings.json')},full_goal_complete=False))
    family='Lil-Speyer59'
    save(FINAL,dict(format='dk4-editorial-final-family-review-v1',family=family,file_path='/data/SC2.DK4',blocks=[25,128],
        record_IDs=sorted(ids),records=rows,revised_count=39,retained_count=20,candidate=str(ROM),candidate_sha256=digest,
        actual_scope=scope,reference_map=str(MAP),final_proof=str(visual),
        source_native_registered_and_representative_actual_gates_passed=True,full_goal_complete=False))
    ledger['completed_editorial_families'].append(dict(id=family,file_path='/data/SC2.DK4',blocks=[25,128],
        record_IDs=sorted(ids),final_review=str(FINAL),revised_count=39,retained_count=20,actual_verification_scope=scope,records=rows))
    unit=next(u for u in ledger['coverage_units']if u['id']=='Lil-Speyer59-source-prose')
    unit.update(status='superseded-by-complete-family',completed_family=family,final_review=str(FINAL))
    ledger['coverage_units'].append(dict(id=family,file_path='/data/SC2.DK4',blocks=[25,128],record_IDs=sorted(ids),
        status='complete-source-native-registered-and-representative-original-gameplay',final_review=str(FINAL),
        actual_proofs=[str(ACTUAL),str(visual)],individually_observed_speech_count=51,offline_only_speech_count=6,
        visible_choice_label_count=2,individually_selected_choice_index=0,completed_entries_added=59,full_goal_complete=False))
    town_ids=[r['id']for r in town_source['records']]
    assert len(town_ids)==79 and not set(town_ids)&ids
    ledger['coverage_units'].append(dict(id='Lil-Hamburg-B74-actual-context-unreviewed',file_path='/data/SC2.DK4',blocks=[74],
        record_IDs=town_ids,status='original-gameplay-captured;editorial-source-prose-review-pending',
        source_context=str(TOWN_SOURCE),actual_proof=str(TOWN),actual_speech_count=79,original_join_panel_count=1,
        original_tutorial_choice0_observed=True,completed_entries_added=0,source_prose_reviews_added=0,full_goal_complete=False))
    for u in ledger['coverage_units']:
        if u['id']=='all-route-scenes':u.update(reviewed_route_records=348,completed_route_records=348,
            next='Review the complete captured Hamburg B74 recruitment/tutorial exchange,then continue every remaining storyline and shared/town/random/player prose. Reconcile prior reviews explicitly.')
    ledger['records_editorially_completed']+=59
    ledger['records_revised_and_integrated']+=39
    ledger['retained_wordings_editorially_completed']+=20
    ledger['completed_editorial_record_counts_by_file']['/data/SC2.DK4']+=59
    for path,pending_ids in ledger['reviewed_but_incomplete_route_record_IDs'].items():
        ledger['reviewed_but_incomplete_route_record_IDs'][path]=[i for i in pending_ids if i not in ids]
    drafts=ledger['active_source_prose_drafts']
    for name,pending_ids in drafts['route_record_subsets_pending'].items():drafts['route_record_subsets_pending'][name]=[i for i in pending_ids if i not in ids]
    drafts['manuscripts']+=list(map(str,(DOC,CHOICES)))
    drafts.update(status='116-reviewed-COMMON-and-broader-fresh-contextual-prose-open',
        note='Stockholm51,London111 andSpeyer59 are integrated in V1945. B74original79 speeches/two labels are captured but not source/prose reviewed. All other storylines/shared/random/player prose remain in full contextual scope.')
    ledger.setdefault('integrated_candidate_reference_history',[]).append(deepcopy(ledger['current_integrated_candidate']))
    ledger['current_integrated_candidate']=dict(path=str(ROM),sha256=digest,profile=PROFILE,MESFILE_sha256=release['COMMON_sha256'],
        ARM9_sha256=release['ARM9_sha256'],SC2_sha256=release['SC2_sha256'],patch=release['patch'],patch_sha256=release['patch_sha256'],
        manifest=str(ROM.with_suffix('.manifest.json')),status='experimental-verified-editorial-checkpoint-not-promoted',details=scope,full_goal_complete=False)
    ledger.setdefault('native_completed_reference_history',[]).append(deepcopy(ledger['current_native_relocation_reference']))
    ledger['current_native_relocation_reference'].update(candidate=str(ROM),candidate_sha256=digest,
        COMMON_sha256=release['COMMON_sha256'],ARM9_sha256=release['ARM9_sha256'],SC2_sha256=release['SC2_sha256'])
    ledger['latest_registered_editorial_candidate']={**release,'status':'experimental-verified-Speyer59',final_review if False else'final_review':str(FINAL),
        'actual_proof':str(visual),'startup_controls_and_editorial_completion_pending':False}
    watch=ledger['formatting_watchlist']['Lil_Speyer59']
    watch['resolved_scene_presentation_prefixes_and_record_IDs']=watch.pop('pending_scene_presentation_prefixes_and_record_IDs')
    watch.update(status='complete-in-V1945',final_review=str(FINAL),all57_speeches_two_labels_native_and_representative_actual_pass=True,
        six_speeches_and_choice1_not_individually_activated=True)
    ledger['next_route_scene_editorial_packet']=dict(file_path='/data/SC2.DK4',block=74,source_context=str(TOWN_SOURCE),
        actual_original_context=str(TOWN),source_prose_review_complete=False,editorial_review_complete=False,
        original79_speeches_join_panel_and_two_choice_labels_captured=True,
        note='Source-first full-exchange review remains pending. Native controls includeGerhard10 andthreeFE system/tutorial panels. Preserve the original79 capture evidence;do not repeat equivalent original gameplay without a concrete risk.')
    fresh=ledger['contextual_story_natural_dialogue_pass_v1871']
    assert fresh['fresh_pass_records_explicitly_reread']==221 and fresh['fresh_pass_records_integrated']==162
    assert ids<=set(fresh['record_IDs'])
    fresh.update(fresh_pass_records_integrated=221,fresh_pass_records_pending_native_actual_release=0,
        latest_completed_family=family,latest_final_review=str(FINAL),historical_completed_records_outside_reconciled_fresh_pass=1529,
        coverage_note='Stockholm51,London111 andSpeyer59 explicitly reread and integrated after V1871. Prior historical reviews require explicit reconciliation;B74capture alone gives no editorial credit.')
    fresh['reconciled_families'].append(dict(id=family,records=59,final_review=str(FINAL)))
    summary=('V1948 Speyer59 complete:1750 historical editorial completions(1316 revised434 retained),1866 source/prose reviewed. '
        'Fresh V1871 contextual pass:221 explicitly reread and integrated;other prior reviews require reconciliation. '+scope)
    ledger['latest_checkpoint']=summary
    ledger['research_checkpoints'].append(dict(id='V1948-Speyer59-complete',proof=str(ROOT/'completion_receipt.json'),
        completed_entries_added=59,source_prose_reviews_added=0,full_goal_complete=False))
    for key in('unresolved_graphics_work','reviewed_but_incomplete_COMMON_IDs','source_prose_reviewed_counts_by_file',
        'records_with_source_and_prose_pass','older_record_reaudit_after_full_editorial_goal'):
        assert ledger[key]==before[key],key
    assert ledger['records_editorially_completed']==sum(ledger['completed_editorial_record_counts_by_file'].values())==1750
    assert ledger['records_revised_and_integrated']+ledger['retained_wordings_editorially_completed']==1750
    assert not any(ledger['reviewed_but_incomplete_route_record_IDs'].values())
    assert ledger['goal_status']=='active'and not ledger['full_goal_complete']
    GUIDE.mkdir(parents=True)
    TOWN_GUIDE.mkdir(parents=True)
    copied=[]
    for group in actual['revised_speech_observations']:
        source=Path(group['holds'][1]['capture']);target=GUIDE/(group['id']+'.png');copy2(source,target)
        assert target.read_bytes()==source.read_bytes();copied.append(str(target))
    for label,source in(('choice',Path(actual['revised_choice']['holds'][0]['capture'])),
        ('Hamburg_return',Path('E:/Rota Nova translations/Generated/work/emulation_v193/lil_Speyer_revised_run_v1938_RESEARCH_ONLY/frame_093780_navigation.png'))):
        target=GUIDE/(label+'.png');copy2(source,target);assert target.read_bytes()==source.read_bytes();copied.append(str(target))
    town_copied=[]
    for index,group in enumerate(town['old_text_observations']+town['original_art_pauses']+town['choices']):
        source=Path(group['holds'][1]['capture']);target=TOWN_GUIDE/(group.get('id',f'interstitial_{index:02d}')+'.png')
        copy2(source,target);assert target.read_bytes()==source.read_bytes();town_copied.append(str(target))
    target=TOWN_GUIDE/'Hamburg_return.png';copy2(Path(town['terminal_capture']),target);town_copied.append(str(target))
    assert len(copied)==53 and len(town_copied)==82
    pending=LEDGER.with_name('editorial_review_current_v1948_pending.json')
    assert not pending.exists()and LEDGER.read_bytes()==raw
    save(pending,ledger);os.replace(pending,LEDGER)
    details=(f'# V1948 Speyer completion\n\n{summary}\n\nCandidate: {ROM.as_posix()}\n\nSHA256: {digest}\n\nProfile: {PROFILE}\n\n'
        f'Clean-input patch: {release["patch"]}\n\nPatch SHA256: {release["patch_sha256"]}\n\nFinal review: {FINAL.as_posix()}\n\n'
        f'Source map: {MAP.as_posix()}\n\nActual proof: {ACTUAL.as_posix()}\n\nGuide: {GUIDE}\n\nOriginal unreviewed B74 context: {TOWN_GUIDE}\n\n'
        'Focused Ruff passes with two documented per-file style exclusions to preserve frozen inputs: I001(import-group spacing) for the private profile,and RUF007(inherited adjacent-pair zip) for the compiler. No behavioral checks are waived.\n')
    Path('docs/lil_speyer_v1948_completion.md').write_text(details,encoding='utf-8')
    for name in('translation_progress.md','known_issues.md','todo.md','editorial_review_goal.md'):
        with(Path('docs')/name).open('a',encoding='utf-8')as stream:stream.write('\n\n## V1948 Speyer59 complete\n\n'+summary+'\n\nSee [completion](lil_speyer_v1948_completion.md).\n')
    text=HANDOFF.read_text(encoding='utf-8')
    text=text.replace('# Current editorial handoff - V1917','# Current editorial handoff - V1948',1)
    start=text.index('## Current coverage and registered release')
    end=text.index('## London B26 complete - V1912')
    coverage=f'''## Current coverage and registered release

- Ledger: translations/editorial_review_current_v1.json. **1750 historical completions =1316 revised +434 retained;1866 source/prose reviewed.**
- Fresh V1871 contextual pass:221 explicitly reread and integrated(Stockholm51 +London111 +Speyer59). Prior1529 completions remain historical and require evidence reconciliation.
- Completed:1402 COMMON +348 SC2;reviewed:1518 COMMON +348 SC2. No active reviewed-incomplete route drafts.116 COMMON entries and broader shared/routes/player prose remain.
- Latest registered experimental: {ROM.as_posix()},profile {PROFILE};482 manifest batches /114 accepted layers.
- Candidate SHA256: {digest}.
- Clean-input patch: {release['patch']};SHA256 {release['patch_sha256']};whole-ROM reconstruction exact.
- Canonical baseline unchanged: out/raphael_natural_v2_accepted_base.nds SHA2563cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe.
- Clean work/clean.nds SHA256f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d.
- ARM9 {release['ARM9_sha256']};COMMON {release['COMMON_sha256']};SC2 {release['SC2_sha256']}. Staged123040bytes unchanged.
- V1492 remains promoted. No new promotion,commit orpush. All ROMs and earlier translations preserved.

## Speyer B128/B25 complete - V1948

{scope}

- Final review: {FINAL.as_posix()};approved prose: {DOC.as_posix()};choices: {CHOICES.as_posix()};map: {MAP.as_posix()}.
- Compiler: dk4tool/patch/lil_speyer_editorial.py;config:translations/lil_speyer_editorial_release_v1.json. Source compilation equals the entire tested research ROM;18 invalid-release gates pass before mutation.
- Source/control proof1936 binds original B25/B128 and exact runtime only. Speyer1d maps29;98 maps152 and actually displays Sailor,while its catalog full name says Retainer. Do not substitute catalog identity for actual nameplates. Global profiles stay unchanged.
- Native proof1937b:57 complete planes/456 macro cases;all8 sheets viewed. Only23 physical-source line-count warnings narrowly waived. Six invalid source/control cases reject. Two labels pass8 complete style planes and6 VM selection/cancel cases.
- Revised proof1941:51 speeches/102 full matching holds,two full matching choice holds,107 original B128 results and116 replayed unowned B74 results. Twelve representative revised panels,choice andtown return actually viewed. Six speeches andchoice1 have no individual gameplay claim.
- Original audit1935b:79 B74 speeches,one join panel andone tutorial choice,plus51 B128 speeches andits choice0.1935 failed before outputs by assuming two art pauses;1935b correctly records the B74join panel plus tutorial choice. Navigator1932 paused safely on A000;1933 continued the same process after viewing Gerhard's full join panel.
- Native event128 requires company1 funds >=50000;copied-state boundaries49999 reject,50000/50001 accept. Disclosed Hamburg access owns20bytes(16 coordinates +4 synthetic funds set60000);two inherited coordinate fixtures own16bytes each. No event/RNG/message/branch/outcome ownership. Native subtype3 isPort,verified getter020B8220 and actual[7,5,3] scheduling. Normal Hamburg return93780;events74/128 complete,B25 incomplete.
- Guide: {GUIDE}. Separate original B74 context: {TOWN_GUIDE};79 speeches andtwo labels are captured but not editorially reviewed.
- All test/build jobs terminal: auxiliary1920/session70666,original1924/session10009,navigators70197/55980/93578,revised1938/session16360,navigator1940/session14989,builder1945/session73739,and startup controls. No live emulator is implied by old notes.
- Frozen approval1937 rejected missing batch-level formatting-gate metadata before outputs;1937b declares all five batch/individual gates. Two style-only Ruff exclusions preserve frozen validated inputs;see completion doc. Full editorial goal remains active.

'''
    text=text[:start]+coverage+text[end:]
    start=text.index('## Current working unit: Speyer B128 and B25 - V1917')
    end=text.index('## Latest completed scene: Lil trade routes and officers, SC2 B24')
    next_work=f'''### Exact next work

Review the complete captured Hamburg B74 Gerhard recruitment/tutorial exchange from clean Japanese. Source/current packet: {TOWN_SOURCE.as_posix()};79 speeches. Original full context: {TOWN.as_posix()},including the join panel and default Yes,please tutorial choice. Both stored choice labels still need source/prose review. No fresh editorial credit has been given for this capture. Controls includeGerhard10 andthreeFE tutorial/system panels;preserve their separate native modal consumer. Do not repeat completed original gameplay without a concrete display/context risk.

The current post-Speyer snapshot is E:/Rota Nova translations/Generated/work/emulation_v193/lil_Speyer_revised_run_v1938_RESEARCH_ONLY/frame_093780_arm9_ram.bin. Its entire ROM equals registered V1945. Native events74 and128 complete;B25aftermath remains incomplete. Do not force its defeat condition or assume a numbered next chapter. The Amsterdam dye lead from London and native catalog Pedro デ Valdes remain separate unresolved player-facing leads.

Continue the full fresh contextual pass through every storyline,earlier translation,shared town/shop/random scene andremaining player-facing prose.116 COMMON entries remain incomplete. Graphics/all18plaques and the later older-record technical re-audit remain separate/open. Preserve all ROMs andearlier translations;V1492 stays promoted.

'''
    HANDOFF.write_text(text[:start]+next_work+text[end:],encoding='utf-8')
    save(ROOT/'completion_receipt.json',dict(final_review=str(FINAL),final_review_sha256=sha(FINAL.read_bytes()),
        candidate=str(ROM),candidate_sha256=digest,profile=PROFILE,patch=release['patch'],patch_sha256=release['patch_sha256'],
        completed_entries_added=59,revised_added=39,retained_added=20,historical_completed_after=1750,source_prose_reviewed_after=1866,
        fresh_contextual_reread_and_integrated=221,source_prose_reviews_added=0,
        actual_revised_speeches=51,actual_complete_speech_holds=102,actual_menu_holds=2,offline_only_speeches=6,
        guide_captures=copied,unreviewed_original_B74_guide_captures=town_copied,
        ledger_sha256=sha(LEDGER.read_bytes()),handoff_sha256=sha(HANDOFF.read_bytes()),
        all_ROMs_and_earlier_translations_preserved=True,full_goal_remains_active=True,
        producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print(dict(historical_completed=1750,revised=1316,retained=434,source_prose_reviewed=1866,
        fresh_contextual_integrated=221,guide_captures=53,B74_unreviewed_context_captures=82,full_goal_remains_active=True))
