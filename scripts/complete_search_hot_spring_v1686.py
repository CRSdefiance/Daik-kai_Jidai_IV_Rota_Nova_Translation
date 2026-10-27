"""Close25 source/native/representative-gameplay entries;keep full goal active."""
from copy import deepcopy
from dataclasses import asdict
from pathlib import Path
from shutil import copy2
import json
import os
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from dk4tool.patch.search_reports_editorial import current_entries
from dk4tool.patch.grand_race_menu_release import sha
from scripts.hot_spring_native_plan_v1615 import compiled as hot_compiled
from scripts.hot_spring_notice_plan_v1632 import compiled as notice_compiled
from scripts.search_reports_native_plan_v1661 import compiled as search_compiled
from scripts.verify_village_wrap_v608 import read, save

ROOT=Path('work/analysis/editorial_completion_v1686')
GUIDE=Path('E:/Rota Nova translations/Guide screenshots/V1676 Search and hot springs verified')
RELEASE=Path('work/analysis/search_reports_release_v1675/registered_release_verification.json')
SEARCH=Path('work/analysis/search_reports_actual_v1683/original_revised_failure_forage_and_loss312_verified.json')
HOT=Path('work/analysis/hot_spring_optional_actual_v1684/original_optional_hot_spring_and_Experience_notice_verified.json')
IDS={310,312,*range(2217,2222),*range(2229,2234),*range(2275,2288)}


def atomic_json(path,value,expected):
    path=Path(path);root=Path.cwd().absolute();target=path.absolute();temporary=target.with_name(target.stem+'_v1686_pending.json')
    target.relative_to(root);temporary.relative_to(root)
    assert target.parent==temporary.parent and not temporary.exists() and target.read_bytes()==expected
    temporary.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    assert read(temporary)==value and target.read_bytes()==expected
    os.replace(temporary,target)


if __name__=='__main__':
    finals=[Path('translations/hot_spring_final_review_v1.json'),Path('translations/hot_spring_notice_final_review_v1.json'),Path('translations/search_reports_final_review_v1.json')]
    assert not ROOT.exists() and not GUIDE.exists() and not any(p.exists() for p in finals)
    release,search,hot=[read(p) for p in [RELEASE,SEARCH,HOT]]
    rom_path=Path(release['candidate']);digest=sha(rom_path.read_bytes())
    assert digest==release['candidate_sha256']==search['candidate_sha256']==hot['candidate_sha256']
    assert release['complete_reconstruction_byte_exact'] and release['all473_batches114_accepted_layers_and_prior_profiles_preserved']
    assert release['all11_compiled_paragraphs_and3657_unselected_texts_preserved']
    assert release['actual_changed_message_IDs']==[312,*range(2217,2222),*range(2229,2234)]
    assert sha(Path(release['patch']).read_bytes())==release['patch_sha256']
    assert search['original_Search_failure_forage_and_sailor_loss_callers_and_ordered_arguments_observed']
    assert search['only_individually_activated_message_IDs']==[312,2217,2229]
    assert hot['original_Search_discovery_recovery_optional_relaxation_effect_notice_and_dismissal_observed']
    assert hot['original_optional_branch_passed_without_actor_skill_RNG_or_event_outcome_edits']
    assert hot['individually_activated_hot_spring_IDs']==[2276,2283,310]
    assert hot['unchanged_prior_text_and_font_reference_reconciled_to_V1637_with_fresh_V1676_native_and_actual_RGB']
    preservation=search['preservation_audit'];assert preservation==hot['preservation_audit']
    assert preservation['terminal_frame']==20792 and preservation['all48_location20_supply10_crew_owned_bytes_and_all_other4MiB_audited']
    assert preservation['all_inputs_snapshots_PNG_hashes_and_unchanged_source_disposable_saves_audited']
    assert preservation['source_proven_crew10_fixture_frames']==preservation['source_proven_supply20_fixture_frames']==[]
    startup_path=RELEASE.parent/'ordinary_startup_verification.json';shop_path=RELEASE.parent/'photographed_shop_formatting.json'
    startup,shop=read(startup_path),read(shop_path)
    assert startup['candidate_sha256']==shop['candidate_sha256']==digest
    assert startup['all8_complete_startup_title_NewGame_frames_exact'] and startup['no_battery_save_savestate_or_fixtures']
    assert all(row['no_authored_indent_internal_gap_or_stray_Discover'] for row in shop['entries'])
    ledger_path=Path('translations/editorial_review_current_v1.json');ledger_raw=ledger_path.read_bytes();ledger=read(ledger_path);before=deepcopy(ledger)
    assert (ledger['records_editorially_completed'],ledger['records_with_source_and_prose_pass'],len(ledger['reviewed_but_incomplete_COMMON_IDs']))==(1350,1519,169)
    assert IDS<=set(ledger['reviewed_but_incomplete_COMMON_IDs']) and not any(IDS&set(f.get('native_message_IDs',[])) for f in ledger['completed_editorial_families'])
    rom=NdsImage.open(rom_path);arm,common=rom.read_file('/__arm9__.bin'),rom.read_file('/COMMON/MESFILE.DK4');entries=current_entries(common,arm)
    clean=NdsImage.open('work/clean.nds');jp=common_message_entries(clean.read_file('/COMMON/MESFILE.DK4'),clean.read_file('/__arm9__.bin'))
    assert sha(arm)==release['ARM9_sha256'] and sha(common)==release['COMMON_sha256']
    ROOT.mkdir(parents=True);save(ROOT/'coverage_before_completion.json',before)
    save(ROOT/'startup_visual_review.json',{'candidate_sha256':digest,'review_sheet':startup['review_sheet'],
        'review_sheet_sha256':sha(Path(startup['review_sheet']).read_bytes()),'all8_panels_actually_viewed':True,
        'startup_title_NewGame_existing_story_and_source_portraits_preserved':True,'no_full_route_or_hardware_claim':True})
    actual_by_id={}
    for group in search['spoken_groups']:
        for hold in group['holds']:actual_by_id.setdefault(hold['message_ID'],[]).append(hold)
    actual_by_id[312]=search['loss_holds']
    for group in hot['spoken_groups']:actual_by_id[group['message_ID']]=group['holds']
    actual_by_id[310]=hot['notice310_holds']
    family_specs=[('Shared-hot-spring13','translations/hot_spring_editorial_manuscript_v2.json',finals[0],hot_compiled,HOT,13,12,1),
                  ('Shared-hot-spring-Experience-notice1','translations/hot_spring_notice_editorial_manuscript_v2.json',finals[1],notice_compiled,HOT,1,1,0),
                  ('Shared-Search-reports11','translations/search_reports_editorial_manuscript_v4.json',finals[2],search_compiled,SEARCH,11,11,0)]
    scope=('Original-donor cold boot with declared48-byte shore location fixtures only. No crew or provisions refill was used in this run;all other4MiB,original actors,skills,fatigue,RNG,event outcomes,inputs,captures and source/disposable saves are audited. '
        'Individually activated IDs are2217 failure,2229 forage,312 sailor loss,2276 hot-spring discovery,2283 relaxation and310 Experience notice. Other voice alternatives retain complete native font/selector/source and representative-family coverage,not individual gameplay activation. '
        'Failure7151/7181 returns7621;forage10183/10213 shows two original105-barrel arguments and returns10433;loss20542/20572 shows original10 and returns normal Sea View20792. '
        'Hot discovery8402/8432,-15 recovery8652/8682,relaxation8902/8932 and Experience9152/9182 return normally9402;both9402 and final20792 were viewed. '
        'Full actual/native/independent source-palette ink and shadows match.312 uses count-neutral grammar and original x0;spoken rows have uniform native6px origins. '
        '294 native quantity/font cases,414 Search actor selections,17 compiler negatives,7336 copies180 cache,13 prior direct pipelines and529507 dispatch/ABI cases pass. '
        'Actual source forage quantities are multiples5 with conservative maxima4650 water/3875 food. Impossible numeric stress cases preserve every glyph and bounds;their awkward breaks are disclosed and excluded from claims about original-game layouts. '
        'Exact clean-input patch,all8 fixture-free startup controls and photographed676/677 preservation pass. No new shop visit,full route or hardware claim. V1676 remains experimental,V1492 promoted;broader editorial and separate graphics/all18 plaques remain open.')
    for family,manuscript,final,compiler,actual,count,revised,retained in family_specs:
        doc=read(manuscript);rows=[];proofs={str(p):sha(p.read_bytes()) for p in [Path(manuscript),RELEASE,actual,startup_path,shop_path]}
        assert len(doc['records'])==count and not doc['formatting_review_pending']
        assert sum(r['editorial_decision']=='revise' for r in doc['records'])==revised
        assert sum(r['editorial_decision']=='retain' for r in doc['records'])==retained
        for key in ['native_font_proof','native_copy_proof','escape_regression_proof','native_runtime_proof','visual_review']:
            if key in doc:proofs[doc[key]]=sha(Path(doc[key]).read_bytes())
        for original in doc['records']:
            row=deepcopy(original);n=row['message_id'];assert n in IDS and all(row['review'].values()) and row['source_hex']==jp[n].text.hex()
            assert entries[n].text==compiler(row)
            row.update(previous_current_text_hex=row['current_text_hex'],current_reference={k:v for k,v in asdict(entries[n]).items() if k!='text'},
                current_text_hex=entries[n].text.hex(),current_English=row['english'],manuscript=manuscript,
                decision='revised-and-integrated' if row['editorial_decision']=='revise' else 'retained-after-source-native-review',
                status='complete-source-native-and-representative-original-gameplay-scope-documented',completed_candidate_reference=str(rom_path),completed_candidate_sha256=digest,
                actual_holds=actual_by_id.get(n,[]),actual_proof=str(actual),individually_activated_in_gameplay=n in actual_by_id,
                actual_scope='Individually activated with two complete actual holds.' if n in actual_by_id else 'Native alternative-voice coverage and original representative-family gameplay;not individually activated.',
                family_actual_verification_scope=scope)
            rows.append(row)
        save(final,{'format':'dk4-editorial-family-final-review-v1','native_message_IDs':[r['message_id'] for r in rows],
            'records':rows,'manuscript':manuscript,'candidate':str(rom_path),'candidate_sha256':digest,'proofs':proofs,
            'actual_verification_scope':scope,'completed_entries':count,'revised':revised,'retained':retained,'full_goal_complete':False})
        ledger['completed_editorial_families'].append({'id':family,'native_message_IDs':[r['message_id'] for r in rows],'records':rows,'final_review':str(final),
            'documentation':'docs/search_hot_spring_v1686_completion.md','actual_verification_scope':scope})
        unit=next(u for u in ledger['coverage_units'] if u['id']==family+'-source-prose')
        unit.update(status='superseded-by-complete-family',completed_family=family,final_review=str(final))
        ledger['coverage_units'].append({'id':family,'status':'complete-source-native-and-original-gameplay-scope-documented',
            'native_message_IDs':[r['message_id'] for r in rows],'final_review':str(final),'actual_proofs':[str(actual)],'full_goal_complete':False})
    ledger['records_editorially_completed']+=25;ledger['records_revised_and_integrated']+=24;ledger['retained_wordings_editorially_completed']+=1
    ledger['completed_editorial_record_counts_by_file']['/COMMON/MESFILE.DK4']+=25
    ledger['reviewed_but_incomplete_COMMON_IDs']=[n for n in ledger['reviewed_but_incomplete_COMMON_IDs'] if n not in IDS]
    expected=set(read('work/analysis/search_reports_source_v1653/coverage_before_review.json')['reviewed_but_incomplete_COMMON_IDs'])-{310,*range(2275,2288)}
    assert set(ledger['reviewed_but_incomplete_COMMON_IDs'])==expected and len(expected)==144
    drafts=ledger['active_source_prose_drafts'];drafts['native_message_IDs']=[n for n in drafts['native_message_IDs'] if n not in IDS]
    for key,values in drafts['manuscript_record_subsets_pending'].items():drafts['manuscript_record_subsets_pending'][key]=[n for n in values if n not in IDS]
    drafts.update(status='earlier144-reviewed-COMMON-and-broader-prose-open',note='Hot-spring13,Experience310 andSearch11 are complete with representative original-gameplay scope. Earlier144 reviewed COMMON and broader shared/routes/player-facing prose remain.')
    ledger.setdefault('native_completed_reference_history',[]).append(deepcopy(ledger['current_native_relocation_reference']))
    ledger['current_native_relocation_reference'].update(candidate=str(rom_path),candidate_sha256=digest,COMMON_sha256=sha(common),ARM9_sha256=sha(arm),
        parser='dk4tool.patch.search_reports_editorial.current_entries',release_config='translations/search_reports_editorial_release_v1.json',hot_spring13_Experience310_and_Search11_complete=True)
    ledger['latest_registered_editorial_candidate']={**release,'status':'experimental-source-native-and-representative-original-gameplay-scope-complete',
        'final_reviews':[str(p) for p in finals],'actual_proofs':[str(SEARCH),str(HOT)],'full_goal_complete':False}
    ledger['latest_registered_hot_spring_candidate'].update(status='superseded-by-completed-families-in-V1676',completed_in_candidate=str(rom_path),current_actual_proof=str(HOT),final_reviews=[str(p) for p in finals[:2]])
    ledger['formatting_watchlist']['hot_spring13'].update(status='completed-in-V1676',final_review=str(finals[0]),actual_proof=str(HOT),
        registered_candidate=str(rom_path),registered_release_and_actual_original_hot_spring_pending=False,optional_relaxation_family_actual_pending=False,
        actual_relaxation_ID2283_and_original_Experience_followup_verified=True)
    ledger['formatting_watchlist']['hot_spring_Experience_notice310'].update(status='completed-in-V1676',final_review=str(finals[1]),actual_proof=str(HOT),
        reviewed_source_prose_but_not_completed=False,native_font_release_and_original_optional_notice_pending=False,
        current_authored_leading_spaces_and_LF_require_native_literal_modal_review=False)
    ledger['formatting_watchlist']['Search_reports11'].update(status='completed-in-V1676',final_review=str(finals[2]),actual_proof=str(SEARCH),
        full_native_fonts_compiler_bounds_copies_patch_and_actual_revised_scenes_pending=False,registered_release_and_original_revised_gameplay_pending=False)
    summary='V1686 closes25 entries(24 revised1 retained):1375 complete(1033 revised342 retained),1519 source/prose reviewed,144 reviewed-incomplete COMMON plus broader shared/routes/player-facing prose. '+scope
    ledger['latest_checkpoint']=summary;ledger['research_checkpoints'].append({'id':'V1686-Search11-and-hot-spring14-complete',
        'proof':str(ROOT/'completion_receipt.json'),'completed_entries_added':25,'source_prose_reviews_added':0,'full_goal_complete':False})
    assert ledger['unresolved_graphics_work']==before['unresolved_graphics_work'] and ledger['records_with_source_and_prose_pass']==1519
    assert (ledger['records_editorially_completed'],ledger['records_revised_and_integrated'],ledger['retained_wordings_editorially_completed'])==(1375,1033,342)
    atomic_json(ledger_path,ledger,ledger_raw)
    GUIDE.mkdir(parents=True);report=read('E:/Rota Nova translations/Generated/work/emulation_v193/search_reports_live_v1680_1676/capture_report.json');frames={r['frame']:r for r in report['frames_captured']};pictures=[]
    for frame,name in [(7151,'Search_nothing_found'),(10183,'Search_water_and_food'),(20542,'Sailors_lost'),(8402,'Hot_spring_discovered'),
                       (8652,'Hot_spring_fatigue_recovery'),(8902,'Hot_spring_relaxation'),(9152,'Hot_spring_Experience'),(20792,'Normal_Sea_View_return')]:
        original=Path(frames[frame]['path']);target=GUIDE/(name+'.png');copy2(original,target)
        assert sha(target.read_bytes())==frames[frame]['PNG_sha256'];pictures.append({'frame':frame,'source':str(original),'guide':str(target),'sha256':sha(target.read_bytes())})
    save(GUIDE/'capture_provenance.json',{'candidate':str(rom_path),'candidate_sha256':digest,'captures':pictures,'original256x384_lossless_framebuffer_captures':True,
        'targeted_headless_DeSmuME_cold_boot_not_full_playthrough_or_hardware':True,'artificial_shore_locations_not_earned_travel':True,
        'no_live_actor_skill_RNG_or_event_outcome_injection_and_no_crew_supply_refill_used':True,'verification_proofs':[str(SEARCH),str(HOT)]})
    pins_path=Path('translations/rom_retention_pins.json');pins=read(pins_path);assert isinstance(pins,list)
    for path,reason in [('E:/Rota Nova translations/Generated/out/all_routes_combined_v1637_candidate.nds','Required current-source ancestor and unchanged hot-spring text/font reference for completed V1676 and future reconstruction.'),
                        ('E:/Rota Nova translations/Generated/out/all_routes_combined_v1676_candidate.nds','Current completed-native editorial reference:Search11 andhot-spring14 complete;broader goal and separate graphics remain open.')]:
        if not any(p['path'].replace('\\','/').lower()==path.lower() for p in pins):pins.append({'path':path,'reason':reason})
    save(pins_path,pins)
    handoff='# Current editorial handoff - V1686\n\n'+summary+'\n\n'+'''## Current authoritative evidence

- Ledger:translations/editorial_review_current_v1.json.
- Completion:work/analysis/editorial_completion_v1686/completion_receipt.json.
- Final reviews:translations/hot_spring_final_review_v1.json,hot_spring_notice_final_review_v1.json,search_reports_final_review_v1.json.
- Current parser:dk4tool.patch.search_reports_editorial.current_entries;config translations/search_reports_editorial_release_v1.json.
- Release:work/analysis/search_reports_release_v1675/registered_release_verification.json.
- Actual Search:work/analysis/search_reports_actual_v1683/original_revised_failure_forage_and_loss312_verified.json.
- Actual optional hot spring:work/analysis/hot_spring_optional_actual_v1684/original_optional_hot_spring_and_Experience_notice_verified.json.
- Current manuscript:translations/search_reports_editorial_manuscript_v4.json,source/native-approved. Never edit executed producers or proofs;use successors.

## Current ROM

out/all_routes_combined_v1676_candidate.nds;physical E:/Rota Nova translations/Generated/out/all_routes_combined_v1676_candidate.nds.
ROM SHA256 337edf22ab6ee96536aadb15fb461652149b157e8d9bd1ef60db998f97608510.
Patch SHA256 4609fc580635481203103b4be3eee4690c70bbef98e41121ab679c40484e802f.
Profile all-routes-unified-v1676;all473 prior manifest batches and114 accepted layers preserved. All earlier route/UI/graphics/fonts,SC0 screenshot repairs andYes/No centering remain exact toV1637;only COMMON4/23 and owned native metadata/runtime banks differ.
V1492 remains promoted;immutable construction baseline out/raphael_natural_v2_accepted_base.nds SHA2563cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe remains unchanged. HistoricalV997 preserved. V1676 is experimental,not user-promoted.

## Test state

All current jobs terminal. Emulator97803 ends20792 at directly viewed normal Sea View. Captures E:/Rota Nova translations/Generated/work/emulation_v193/search_reports_live_v1680_1676. Runner scripts/run_search_reports_live_v1680.py;log work/search_reports_live_v1680.log;journal work/analysis/search_reports_live_v1680/navigation.jsonl.
No active process handle. Old58934 terminal53178 and69622 terminal95860 remain historical evidence. Do not resume or restart those from assumptions.
Optional hot-spring branch is NOW VERIFIED and COMPLETE in scoped coverage;do not repeat the random Search campaign. Its13 alternative lines have full prior native fonts and representative discovery/relaxation gameplay;notice310 is individually activated. Actual current-native and paletteRGB proof reconciles unchanged texts/fonts fromV1637. Search independently activates2217,2229,312;other8 alternatives have native and representative family coverage.
Eight verified guide screenshots and provenance are in E:/Rota Nova translations/Guide screenshots/V1676 Search and hot springs verified.

## Continue the full editorial goal

Proceed with the exact earlier144 pending COMMON IDs in the ledger or scene-by-scene unreviewed shared/route prose. Do not redo closed families without a concrete remaining risk. Broader routes and player-facing prose remain unfinished;these counts are not overall project completion. Preserve Rafael,Joakim,Maria,Camille. Older-record re-audit stays queued after the full editorial goal.
Separate graphics/all18 plaques remain unfinished;wood texture/borders were accepted but not the entire audit. Four low-resolution Online bodies stay excluded andtwo brown marks retained. No subagents authorized.
Read AGENTS,build_continuity_protocol,release_stack,relevantknown_issues,natural_dialogue_workflow anddialogue_delegation_protocol before author/build. Sources/ read-only. All new prose usesnatural-dialogue-v2 and original-source controls/arguments. The full goal staysACTIVE;do not mark itcomplete orpaused because this batch is complete.
Use Python C:/Python314/python.exe,PYTHONUTF8=1,PYTHONPATH=.;.deps. out/work-analysis junction toE;archive lexical paths without resolve(). Keep all generatedROMs;retention script remains unsigned/policy-blocked;no bypass or deletion. No new commit/push orpromotion was authorized this turn.
Registration1675 encountered WindowsOSError22 opening the existing13MB registry after writing the optional builder block. Explicit1675b validated original registry bytes and complete block,then atomically added onlyV1676. Provenance is in the release folder;do not rerun1675. The new191 delta/run64 codec fits186/188 bytes,gate168/172 and staged123040 remain fixed;all prior memberships preserved.
'''
    Path('docs/editorial_handoff_current.md').write_text(handoff,encoding='utf-8')
    doc='# V1686 Search and hot-spring editorial completion\n\n'+summary+'\n\n## Registered candidate and patch\n\n'+handoff[handoff.index('out/all_routes_combined_v1676_candidate.nds;'):handoff.index('## Test state')]+\
        '\nClean input work/clean.nds SHA256f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d. The .xdelta rebuild matches every byte. Registered layer search_reports_editorial is experimental after the fullV1637 stack;114 accepted layers remain unchanged.\n\n'+\
        '## Evidence and limits\n\nSee the current handoff and completion receipt for exact source/final reviews,native proofs,actual input schedules and captures. Actual tests are targeted headless DeSmuME cold boots using an unchanged ordinary battery save and isolated shore positions,not saved states. Only six distinct IDs were individually activated;other alternatives have complete native and representative-family coverage. No full route orhardware claim. The prior shop screenshot676/677 corrections are preserved and rechecked without claiming a new shop visit. All25 entries are now closed;the broader goal and separate graphics/all18 plaques remain open.\n'
    Path('docs/search_hot_spring_v1686_completion.md').write_text(doc,encoding='utf-8')
    for name in ['translation_progress.md','known_issues.md','todo.md','editorial_review_goal.md']:
        with (Path('docs')/name).open('a',encoding='utf-8') as f:f.write('\n\n## V1686 Search11 and hot-spring14 complete\n\n'+summary+'\n\nSee [completion](search_hot_spring_v1686_completion.md).\n')
    save(ROOT/'completion_receipt.json',{'candidate':str(rom_path),'candidate_sha256':digest,'patch':release['patch'],'patch_sha256':release['patch_sha256'],
        'completed':1375,'revised':1033,'retained':342,'source_prose':1519,'reviewed_incomplete_COMMON':144,'newly_completed':25,
        'newly_revised':24,'newly_retained':1,'unique_complete_COMMON':1374,'final_reviews':[str(p) for p in finals],
        'proofs':{str(p):sha(p.read_bytes()) for p in [RELEASE,SEARCH,HOT,startup_path,shop_path]},'guide':str(GUIDE),'screenshots':pictures,
        'V1492_promotion_canonical_baseline_historical_V997_and_all_prior_profiles_preserved':True,
        'source_native_complete_and_representative_gameplay_scope_explicit':True,'all_current_jobs_terminal':True,
        'separate_graphics_unchanged':True,'all_generated_ROMs_retained':True,'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    print('Closed25 entries:1375 complete(1033 revised342 retained),1519 source/prose reviewed,144 earlier COMMON pending. V1676 and exact patch verified;8 guide screenshots saved;all jobs terminal. Full editorial goal active,graphics separate.')
