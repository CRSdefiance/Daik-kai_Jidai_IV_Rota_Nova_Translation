"""Close sea8 and two inspection statuses after full original scene verification."""
from copy import deepcopy
from dataclasses import asdict
from pathlib import Path
from shutil import copy2
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from dk4tool.patch.inspection_status_editorial import current_entries
from dk4tool.patch.grand_race_menu_release import sha
from scripts.sea_responses_native_plan_v1556 import compiled as sea_compiled
from scripts.inspection_status_native_plan_v1573 import compiled as status_compiled
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/sea_inspection_completion_v1584')
ROM=Path('out/all_routes_combined_v1578_candidate.nds')
RELEASE=Path('work/analysis/inspection_status_release_v1577/registered_release_verification.json')
ACTUAL=Path('work/analysis/inspection_status_actual_verified_v1583/both_original_status_paths_native_RGB_and_transitions.json')
GUIDE=Path('E:/Rota Nova translations/Guide screenshots/V1578 corrected creature inspection')
SEA_FINAL=Path('translations/sea_responses_final_review_v1.json')
STATUS_FINAL=Path('translations/inspection_status_final_review_v1.json')

if __name__=='__main__':
    assert not ROOT.exists() and not GUIDE.exists() and not SEA_FINAL.exists() and not STATUS_FINAL.exists()
    release,actual=read(RELEASE),read(ACTUAL);digest=sha(ROM.read_bytes())
    assert digest==release['candidate_sha256']==actual['candidate_sha256']
    assert release['actual_changed_message_IDs']==[306,307] and release['complete_reconstruction_byte_exact']
    assert release['all471_batches114_accepted_layers_and_prior_profiles_preserved']
    assert release['all2_modal_statuses_and3666_unselected_texts_preserved'] and release['only_COMMON4_and_original_native_metadata_changed']
    assert actual['both_source_original_statuses_observed_without_message_injection'] and actual['both_normal_Inspect_returns_proven']
    assert actual['entire4MiB_fixtures_input_primary_RAM_PNG_and_unchanged_donor_audits_pass']
    by_id={p['message_ID']:p for p in actual['paths']}
    assert set(by_id)=={306,307} and all(len(p['holds'])==2 for p in actual['paths'])
    assert [h['changed_pixels'] for h in by_id[306]['holds']]==[392,392]
    assert [h['changed_pixels'] for h in by_id[307]['holds']]==[233,233]
    assert sum(len(p['whole_other_RGB_controls']) for p in actual['paths'])==46
    assert {5800,5830,5900,5930}<={r['frame'] for r in by_id[306]['whole_other_RGB_controls']}
    startup_path=RELEASE.parent/'ordinary_startup_verification.json';shop_path=RELEASE.parent/'photographed_shop_formatting.json'
    startup,shop=read(startup_path),read(shop_path)
    assert startup['candidate_sha256']==shop['candidate_sha256']==digest
    assert startup['all8_complete_startup_title_NewGame_frames_exact'] and startup['no_battery_save_savestate_or_fixtures']
    assert all(r['no_authored_indent_internal_gap_or_stray_Discover'] for r in shop['entries'])
    rom,clean,prior=NdsImage.open(ROM),NdsImage.open('work/clean.nds'),NdsImage.open('out/all_routes_combined_v1563_candidate.nds')
    arm,common=rom.read_file('/__arm9__.bin'),rom.read_file('/COMMON/MESFILE.DK4')
    entries=current_entries(common,arm);jp=common_message_entries(clean.read_file('/COMMON/MESFILE.DK4'),clean.read_file('/__arm9__.bin'))
    assert rom.read_file('/GRP/KANJI.FNT')==prior.read_file('/GRP/KANJI.FNT')
    ledger_path=Path('translations/editorial_review_current_v1.json');ledger=read(ledger_path);before=deepcopy(ledger)
    assert (ledger['records_editorially_completed'],ledger['records_with_source_and_prose_pass'],ledger['records_with_source_prose_drafts'],len(ledger['reviewed_but_incomplete_COMMON_IDs']))==(1338,1492,1492,154)
    IDS=[306,307,*range(2209,2217)]
    assert not any(set(IDS)&set(f.get('native_message_IDs',[])) for f in ledger['completed_editorial_families'])
    ROOT.mkdir(parents=True);save(ROOT/'coverage_before_completion.json',before)
    visual=ROOT/'startup_both_statuses_creature_response_and_returns_visual_review.json'
    save(visual,{'all8_fixture_free_startup_panels_actually_viewed':True,
        'actual306_6100_and307_6630_full_boxes_actually_viewed':True,
        'actual2209_5830_and_Inspect_returns6300_6850_actually_viewed':True,
        'both_status_native_panels_actually_viewed':'work/analysis/inspection_status_native_review_v1576/both_native_panels_visual_review.json',
        'all8_sea_native_panels_prior_review':'work/analysis/sea_responses_native_review_v1561/all8_native_panels_visual_review.json',
        'actual_proof':str(ACTUAL),'actual_proof_sha256':sha(ACTUAL.read_bytes()),'full_goal_complete':False})
    scope=('Source/context/native review closes eight alternative creature/ghost inspection responses2209-2216(5 revised3 justified retentions) and two revised system statuses306/307. '
        'The unsupported war reference is removed;complete astonishment,first-sighting,sea disbelief and personal fear are expressed in natural faithful American English. '
        '306 now says You cannot view that information;307 states the missing lookout assignment. Actual shipped wording preserves the source exclamation and natural contractions. '
        'Source6F4D4/6F674 role7/table021186E0 and independent546B8 status paths are mapped. An actor returned by82478 can be fallback speech and does not prove an occupied lookout;'
        '705F8/8205C identify the empty station. All8 full sea native/independent glyph planes,207 existing actor choices,7 CPU-only role alternatives,14 compiler negatives and viewed sheet are retained. '
        'The V1578 layer preserves every sea text/copy span,all native code,dispatch tables,fonts and the previous native behavior.7336 new complete loader copies180 cache sequences pass. '
        'Both new status texts execute the original loader/varargs/native macro path with the three inherited registered hooks intact;both full native/independent planes and12 compiler negatives pass. '
        'Literal status boxes retain their original x0 cursor;spoken sea responses retain their proven6px margin. No authored line breaks,alignment,layout hook or selector membership is added. '
        'Exact full-stack release preserves471 batches114 accepted layers,3666 other text/copy spans,40 blocks,the opaque duel prefix,all earlier routes/graphics/fonts/helpers,188 selector bytes,172 gate bytes and123040 staged bytes. '
        'Only COMMON4 and original native offset/directory metadata differ from V1563. Clean-input xdelta reconstructs every ROM byte. All8 ordinary startup/title/New Game frames are identical to V1105 and visually reviewed. '
        'Photographed shop676/677 repaired bytes/wrapping/full native planes pass without claiming a fresh shop visit. Two original cold-boot replays use the prior exact inputs and isolated existing Monster Fish registration/location. '
        'One original RNG initialization executes naturally;no RNG value or combat outcome is forced.46 owned bytes cover the no-lookout fixture,48 include moving existing Charles18 from station9 to empty lookout3. '
        'All unowned4MiB bytes,own five ship objects,actor identities/stats and source/disposable saves are preserved. No numeric message,renderer or target-type injection. '
        'Original306 has complete6040/6100 native/independent/reference/RGB holds;all392 changed pixels per hold equal the exact old/new letter XOR. Original307 has complete6600/6630 holds,each233 exact letter pixels. '
        'All46 other full-screen comparisons are exact,including four latest2209 holds5800/5830/5900/5930 matching the prior fully native/independent/RGB-verified scene. '
        'Normal A dismissal returns to Info Mode/Inspect at6300 and6850;this is not a Sea View UI claim. Actual status boxes,Charles response,returns and startup are viewed. '
        'Only2209 is individually activated among the8 voice alternatives;other7 have full native and representative-family coverage. Both status IDs are individually observed. '
        'Targeted headless evidence is not earned travel/discovery/acquisition,a complete route playthrough or hardware verification. Initial1572 clean-code guard correctly detected inherited hooks;1572b verifies provenance and retains them. '
        '1572c reconciles the omitted legacy coverage alias/subset without duplicate reviews.306/307 wrong-text leads are resolved;308 remains a separate unreviewed fatigue-context lead. '
        'V1578 stays experimental,V1492 promoted;the full editorial goal,earlier144 pending entries,broader shared/routes/raw prose,separate graphics/all18 plaques and later older-record re-audit remain open.')
    families=[]
    for family,manuscript,final,numbers,revision_count,retained_count,unit_id,compiler in [
        ('Shared-sea-inspection-fear-awe8',Path('translations/sea_responses_editorial_manuscript_v2.json'),SEA_FINAL,list(range(2209,2217)),5,3,'Shared-sea-inspection-fear-awe8-source-prose',sea_compiled),
        ('Shared-inspection-status2',Path('translations/inspection_status_editorial_manuscript_v2.json'),STATUS_FINAL,[306,307],2,0,'Shared-inspection-status2-source-prose',status_compiled)]:
        doc=read(manuscript);fonts_path=Path(doc['native_font_proof']);fonts=read(fonts_path)
        assert len(fonts['cases'])==len(numbers)
        if numbers[0]==2209:
            assert fonts['ARM9_sha256']==sha(prior.read_file('/__arm9__.bin')) and fonts['COMMON_sha256']==sha(prior.read_file('/COMMON/MESFILE.DK4'))
            assert len(fonts['all207_existing_actor_choices'])==207 and len(fonts['invalid_compiler_inputs_rejected'])==14 and not fonts['findings']
        else:assert fonts['ARM9_sha256']==sha(arm) and fonts['COMMON_sha256']==sha(common)
        rows=[]
        for record in doc['records']:
            row=deepcopy(record);n=row['message_id'];assert n in numbers and row['source_hex']==jp[n].text.hex() and all(row['review'].values())
            assert entries[n].text==compiler(row)
            case=next(c for c in fonts['cases'] if c['message_ID']==n)
            assert case['compiled_hex']==entries[n].text.hex()
            holds=by_id[n]['holds'] if n in by_id else []
            if n==2209:
                holds=[{'frame':frame,'latest_whole_RGB_exact_to_prior_fully_native_verified2209':True,
                    'prior_complete_font_proof':'work/analysis/sea_inspection_verified_v1568b/original_inspection_complete_pixels_and_transition.json',
                    'latest_preservation_proof':str(ACTUAL)} for frame in [5800,5830,5900,5930]]
            row.update(manuscript=str(manuscript),previous_current_text_hex=row['current_text_hex'],
                current_reference={k:v for k,v in asdict(entries[n]).items() if k!='text'},current_text_hex=entries[n].text.hex(),current_English=row['english'],
                decision='revised-and-integrated' if row['editorial_decision']=='revise' else 'retained-with-source-context-justification',
                status='complete-source-native-and-original-system-or-representative-family-gameplay',completed_candidate_reference=str(ROM),completed_candidate_sha256=digest,
                complete_native_font_proof=str(fonts_path),complete_native_font_proof_sha256=sha(fonts_path.read_bytes()),
                complete_native_formatted_lines=case.get('lines',[row['english']]),actual_holds=holds,
                individual_actual_activation_not_claimed_when_actual_holds_empty=True)
            rows.append(row)
        assert sum(r['editorial_decision']=='revise' for r in rows)==revision_count
        save(final,{'format':'dk4-editorial-family-final-review-v1','native_message_IDs':numbers,'records':rows,'manuscript':str(manuscript),
            'candidate':str(ROM),'candidate_sha256':digest,'actual_gameplay':str(ACTUAL),'actual_gameplay_sha256':sha(ACTUAL.read_bytes()),
            'registered_release':str(RELEASE),'registered_release_sha256':sha(RELEASE.read_bytes()),'actual_verification_scope':scope,
            'completed_entries':len(rows),'revised':revision_count,'retained':retained_count,'full_goal_complete':False})
        ledger['completed_editorial_families'].append({'id':family,'native_message_IDs':numbers,'records':rows,'final_review':str(final),
            'documentation':'docs/sea_inspection_v1584_completion.md','actual_verification_scope':scope})
        unit=next(u for u in ledger['coverage_units'] if u['id']==unit_id);unit.update(status='superseded-by-complete-family',completed_family=family,final_review=str(final))
        ledger['coverage_units'].append({'id':family,'status':'complete-source-native-and-original-gameplay-scope-documented','native_message_IDs':numbers,
            'final_review':str(final),'actual_proof':str(ACTUAL),'full_goal_complete':False})
        families.append({'id':family,'final_review':str(final),'completed':len(rows),'revised':revision_count,'retained':retained_count})
    ledger['records_editorially_completed']+=10;ledger['records_revised_and_integrated']+=7;ledger['retained_wordings_editorially_completed']+=3
    ledger['completed_editorial_record_counts_by_file']['/COMMON/MESFILE.DK4']+=10
    ledger['reviewed_but_incomplete_COMMON_IDs']=[n for n in ledger['reviewed_but_incomplete_COMMON_IDs'] if n not in IDS]
    drafts=ledger['active_source_prose_drafts'];drafts['native_message_IDs']=[n for n in drafts['native_message_IDs'] if n not in IDS]
    for name in drafts['manuscript_record_subsets_pending']:
        if any(f in name for f in ['sea_responses_editorial_manuscript','inspection_status_editorial_manuscript']):drafts['manuscript_record_subsets_pending'][name]=[]
    drafts.update(status='earlier144-reviewed-COMMON-and-broader-prose-open',note='Sea8 and two inspection statuses complete in V1578. Earlier144 reviewed COMMON entries,broader shared/routes/raw prose and graphics remain open;fatigue308 is next source/context lead.')
    ledger['current_native_relocation_reference'].update(candidate=str(ROM),candidate_sha256=digest,COMMON_sha256=release['COMMON_sha256'],ARM9_sha256=release['ARM9_sha256'],
        parser='dk4tool.patch.inspection_status_editorial.current_entries',release_config='translations/inspection_status_editorial_release_v1.json',sea8_and_inspection_status2_complete=True)
    for key,final in [('latest_registered_sea_responses_candidate',SEA_FINAL),('latest_registered_inspection_status_candidate',STATUS_FINAL)]:
        ledger[key]={**release,'status':'experimental-source-native-and-original-gameplay-scope-complete','final_review':str(final),'actual_proof':str(ACTUAL),'full_goal_complete':False}
    ledger['formatting_watchlist']['sea_inspection_fear_awe8'].update(status='completed-in-V1578',final_review=str(SEA_FINAL),original_scene_followup_text_gate_open=False,
        native_font_family_verified_but_editorial_completion_pending=False,actual_proof=str(ACTUAL),individually_activated_original_ID=2209)
    ledger['formatting_watchlist']['inspection_status2'].update(status='completed-in-V1578',final_review=str(STATUS_FINAL),
        native_font_release_actual_followup_and_no_lookout_pending=False,actual_proof=str(ACTUAL),individually_activated_original_IDs=[306,307])
    ledger['newly_observed_sea_inspection_modal_defects'].update(status='306307-corrected-complete-in-V1578;308-separate-context-open',resolved_IDs=[306,307],open_IDs=[308],final_review=str(STATUS_FINAL))
    ledger['formatting_watchlist']['latest_reference_proof']=str(shop_path)
    summary=('V1584 completes10 entries in registered V1578:sea inspection8(5 revised3 retained) and original status306/307(2 revised). Counts1348 complete(1007 revised341 retained),1492 source/prose;144 reviewed-incomplete COMMON(32 reactions24 loss/surrender16 sinking34 aftermath38 older),plus broader shared/routes/raw prose. '
        'Both source-faithful statuses replace unrelated old fragments and pass full original loader/varargs/macro/native-independent font planes,12 compiler negatives and visual review. No new native code,layout,selector or authored breaks. All8 sea native planes/207 actor choices and prior full-scene proof are preserved by exact text/copy/code/font retention and four latest whole2209 frames. '
        '7336 complete native copies180 cache sequences,471 batches114 accepted layers,40 other COMMON blocks,3666 other copies,188 selector172 gate123040 staged bytes and all earlier routes/graphics/fonts/helpers are preserved. Exact clean-input patch and all8 viewed fixture-free startup controls pass;shop676/677 retained. '
        'Two original cold-boot exact-input replays audit full4MiB,48/46-owned-byte prebattle fixtures,original natural RNG initialization,unchanged donors and actor/own-ship data.306 holds6040/6100 differ only392 exact letter pixels each;307 holds6600/6630 only233 each.46 other full-screen comparisons match,including latest2209 at5800/5830/5900/5930. Normal A closes return to Info Mode/Inspect6300/6850,both viewed. '
        'Only2209 individually activated among8 voices;other7 native/family coverage,both statuses individually observed. No earned travel/discovery or full-route/hardware claim.1572 inherited-hook guard and1572c alias omission are documented without weakening native guards or duplicate counts.308 fatigue remains an independent context lead. V1578 experimental,V1492 promoted,canonical/V997 unchanged;separate graphics/all18 plaques and later older-record re-audit stay open;goal active.')
    ledger['latest_checkpoint']=summary;ledger['research_checkpoints'].append({'id':'V1584-sea8-status2-complete','proof':str(ROOT/'completion_receipt.json'),
        'final_reviews':[str(SEA_FINAL),str(STATUS_FINAL)],'completed_entries_added':10,'source_prose_reviews_added':0,'full_goal_complete':False})
    complete=[n for f in ledger['completed_editorial_families'] for n in f.get('native_message_IDs',[])];pending=ledger['reviewed_but_incomplete_COMMON_IDs']
    assert len(complete)==len(set(complete))==1347 and len(pending)==len(set(pending))==len(drafts['native_message_IDs'])==144
    assert not set(complete)&set(pending) and len(set(complete)|set(pending))==1491
    assert ledger['records_editorially_completed']==ledger['records_revised_and_integrated']+ledger['retained_wordings_editorially_completed']==1348
    assert sum(ledger['completed_editorial_record_counts_by_file'].values())==1348
    for k in ['records_with_source_and_prose_pass','records_with_source_prose_drafts','source_prose_reviewed_counts_by_file','current_integrated_candidate',
        'source_pins','unresolved_graphics_work','older_record_reaudit_after_full_editorial_goal','raw_source_coverage_revisit']:assert ledger[k]==before[k],k
    save(ledger_path,ledger)
    pins_path=Path('translations/rom_retention_pins.json');pins=read(pins_path);pin='E:/Rota Nova translations/Generated/out/all_routes_combined_v1578_candidate.nds'
    assert not any(p['path']==pin for p in pins);pins.append({'path':pin,'reason':'Completed sea8 and status306/307;current native COMMON parent for remaining editorial review.'});save(pins_path,pins)
    GUIDE.mkdir(parents=True);screenshots=[]
    for label,folder,frame in [('Charles_creature_response','inspection_status_lookout_v1582_1578',5830),('Information_unavailable','inspection_status_lookout_v1582_1578',6100),
        ('No_lookout_assigned','inspection_status_no_lookout_v1582b_1578',6630),('Inspect_Monster_Fish','inspection_status_lookout_v1582_1578',6300)]:
        source=Path('E:/Rota Nova translations/Generated/work/emulation_v193')/folder/f'frame_{frame:06d}_navigation.png';target=GUIDE/(label+'.png')
        copy2(source,target);assert sha(source.read_bytes())==sha(target.read_bytes());screenshots.append({'path':str(target),'source':str(source),'frame':frame,'sha256':sha(target.read_bytes())})
    save(GUIDE/'provenance.json',{'candidate_sha256':digest,'screenshots':screenshots,'actual_proof':str(ACTUAL),
        'artificial_original_creature_registration_location_and_optional_lookout_assignment':True,'one_original_RNG_initialization_not_forced':True,
        'not_earned_travel_discovery_acquisition_or_full_playthrough':True,'full_goal_complete':False})
    document=Path('docs/sea_inspection_v1584_completion.md')
    document.write_text('# V1584 sea inspection8 and system statuses2 complete\n\n'+summary+'\n\n## Exact experimental release\n\n'
        '- Candidate: `E:/Rota Nova translations/Generated/out/all_routes_combined_v1578_candidate.nds`;SHA-256 `'+digest+'`.\n'
        '- Canonical construction base: `out/raphael_natural_v2_accepted_base.nds`;SHA-256 `'+release['canonical_sha256']+'`.\n'
        '- Profile: `all-routes-unified-v1578`;471 batches114 accepted layers. V1492 remains promoted.\n'
        '- Changed files versus V1563: `/COMMON/MESFILE.DK4` and `/__arm9__.bin`;COMMON4 and original metadata only. All code and188/172/123040 banks unchanged.\n'
        '- Exact patch: `'+release['patch']+'`;SHA-256 `'+release['patch_sha256']+'`;clean input `'+release['clean_input_sha256']+'`.\n'
        '- Checks: source1572b/plan1573/fonts1574/copies1575/visual1576/release1579/startup1580/shop1580b/original actual1583.\n'
        '- Experimental user testing can cover title/New Game,Info Mode with and without an assigned lookout,the creature response,following information-unavailable box,and normal return to Inspect.\n\n'
        '## Verification scope\n\n'+scope+'\n',encoding='utf-8')
    for name in ['translation_progress.md','known_issues.md','todo.md','editorial_review_goal.md']:
        with (Path('docs')/name).open('a',encoding='utf-8',newline='\n') as f:f.write('\n\n## V1584 sea8 and inspection status2 complete\n\n'+summary+'\n\nSee [completion](sea_inspection_v1584_completion.md).\n')
    Path('docs/editorial_handoff_current.md').write_text('# Current editorial handoff - V1584\n\n'+summary+'\n\n'
        'Read AGENTS.md,build_continuity_protocol.md,release_stack.json,relevant known_issues.md,natural_dialogue_workflow.md and dialogue_delegation_protocol.md. Sources are read-only;executed producers/manuscripts/proofs receive successors. No subagents authorized. All current build/emulator jobs terminal.\n\n'
        '## Resume from authoritative files\n\n- Ledger: translations/editorial_review_current_v1.json.\n- Completion: work/analysis/sea_inspection_completion_v1584/completion_receipt.json.\n'
        '- Release: work/analysis/inspection_status_release_v1577/registered_release_verification.json.\n- Actual paths: work/analysis/inspection_status_actual_verified_v1583/both_original_status_paths_native_RGB_and_transitions.json.\n'
        '- Current parser: dk4tool.patch.inspection_status_editorial.current_entries.\n- Final reviews: translations/sea_responses_final_review_v1.json and translations/inspection_status_final_review_v1.json.\n\n'
        '## Next work\n\nReview the source/context and original consumers of fatigue308/309.308 is currently the unrelated suffix in, and value followed by a real source %s. Do not drop that runtime argument or edit fatigue/RNG/outcomes merely to force a message. Earlier144 reviewed COMMON and broad shared/routes/raw prose remain unfinished. Preserve separate graphics/all18 plaque audit and later older-record re-audit.\n\n'
        'Python C:/Python314/python.exe with PYTHONUTF8=1 and PYTHONPATH=.;.deps. Normal launcher may fail P drive authentication;task-specific escalation works. Builder logs are huge;redirect and print bounded tails. out/work-analysis are E-drive junctions;archive lexical relative paths without resolve(). ROMs and screenshots stay under E:/Rota Nova translations. Retention preview only. Preserve selector188/gate172/staged123040 and all prior layers. V1492 promoted checkpoint and immutable construction baseline stay unchanged.\n',encoding='utf-8')
    save(ROOT/'completion_receipt.json',{'candidate':str(ROM),'candidate_sha256':digest,'completed':1348,'revised':1007,'retained':341,'source_prose':1492,
        'newly_completed':10,'unique_complete_COMMON':1347,'reviewed_incomplete_COMMON':144,'families':families,
        'actual_proof':str(ACTUAL),'visual_review':str(visual),'guide':str(GUIDE),'guide_screenshots':screenshots,
        'V1492_promoted_canonical_and_V997_unchanged_global_goal_active':True,'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    print('Sea8 and status2 complete:1348 complete(1007 revised341 retained),1492 reviewed,144 reviewed COMMON pending;broader editorial and graphics remain open.')
