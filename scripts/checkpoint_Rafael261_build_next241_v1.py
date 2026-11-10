"""Save261 research-complete reviews,live679 integration and90 clean-only next drafts."""
import ctypes as ct
import json
import re
from pathlib import Path
from scripts.audit_story_glyph_consistency import load,save
from scripts.save_editorial_progress_checkpoint_v5 import checkpoint
from dk4tool.patch.grand_race_menu_release import sha

PREP=Path('work/analysis/Rafael261_registered_preparation_v2_20261105/registered_preparation.json')
QUAL=Path('work/analysis/Rafael261_release_qualification_20261105/qualification.json')
RESEARCH=Path('work/analysis/Rafael261_checked_20261105/research_completion.json')
FINAL=Path('translations/rafael_B85_B100_contextual_final_review_v1.json')
STARTUP=Path('work/analysis/Rafael261_identity_coldboot_20261105/identity_RGB_qualification.json')
NEXT=Path('work/analysis/Rafael_B101_B120_clean_20261105')
DRAFTS=NEXT/'first90_source_meanings_andindependent_drafts_v1.json'
BUILD=Path('work/analysis/Rafael261_registered_build_20261105')
PID=105028

if __name__=='__main__':
    prep,qual,research,final,startup,drafts,packet,choices=map(load,[PREP,QUAL,RESEARCH,FINAL,STARTUP,DRAFTS,NEXT/'clean_source_packet.json',NEXT/'clean_choice_objects.json'])
    assert research['all261_individual_five_gates_pass'] and (research['revisions'],research['retentions'])==(111,150)
    assert all(all(r['review'].values()) for r in final['records']) and len(final['records'])==261
    assert len(qual['changed_scope_andordering_rejections'])==8 and qual['direct_prepublication_andshared_targets_equal']
    assert len(startup['exact_RGB_pairs'])==10 and startup['actual_coldboot_frames']==4001
    assert (packet['records'],choices['caption_count'],drafts['source_speech_drafts'],drafts['remaining_packet_speech_drafts'])==(229,12,90,139)
    assert drafts['current_SC0_English_not_consulted_in_this_intake'] and not (BUILD/'completion.json').exists()
    kernel=ct.WinDLL('kernel32',use_last_error=True)
    kernel.OpenProcess.argtypes=[ct.c_ulong,ct.c_int,ct.c_ulong];kernel.OpenProcess.restype=ct.c_void_p
    kernel.GetExitCodeProcess.argtypes=[ct.c_void_p,ct.POINTER(ct.c_ulong)];kernel.GetExitCodeProcess.restype=ct.c_int
    kernel.CloseHandle.argtypes=[ct.c_void_p];kernel.CloseHandle.restype=ct.c_int
    handle=kernel.OpenProcess(0x1000,False,PID);assert handle
    code=ct.c_ulong();assert kernel.GetExitCodeProcess(handle,ct.byref(code));kernel.CloseHandle(handle);assert code.value==259
    telemetry=json.loads((BUILD/'collections.jsonl').read_text().splitlines()[-1]);assert not telemetry['errors']
    prior=load('translations/editorial_review_current_v1.json');assert prior['records_editorially_completed']==11845
    existing=prior['contextual_story_natural_dialogue_pass_v1871']['record_keys']
    sourcekeys={(r['file_path'],r['id']) for g in packet['groups'] for r in g['records']}|{(r['file_path'],r['id']) for r in choices['records']}
    assert len(sourcekeys)==241 and not sourcekeys&{(r['file_path'],r['id']) for r in existing}
    normalized=[]
    for row in existing:
        if row['file_path']!='/data/SC0.DK4':continue
        match=re.search(r'(?:DK4_MES_B|SC0_B)(\d+)_',row['id'])
        if match and 101<=int(match[1])<=120:normalized.append(row)
    assert not normalized
    census=NEXT/'completed_overlap_census_v1.json';assert not census.exists()
    save(census,dict(source_objects=241,source_speeches=229,source_captions=12,explicit_source_ID_overlap=[],
        normalized_completed_SC0_B101_B120_ID_overlap=[],ledger_sha256=sha(Path('translations/editorial_review_current_v1.json').read_bytes()),
        ledger_completed=11845,existing_source_key_count=len(existing),source_packet=str(NEXT/'clean_source_packet.json'),
        source_packet_sha256=sha((NEXT/'clean_source_packet.json').read_bytes()),not_a_global_older_record_technical_reaudit=True,new_credit=0))
    summary=('Rafael/tutorial priority continues. Rafael261 nowallfive research gates:111 revisions/150 retentions,256 complete stored/viewed body pages,six captions/20 scoped names. '
        '300 native branch cases,255 catalogue lookups and343 loaders pass;20722 initialized frames observe43 speeches/44 body pages+six captions,212 speeches offline-only. '
        'Rebased owned B85–B100 only onto678,retainingB81–84/Help202.679-entry registered build73098/PID105028 isOS-confirmed live;registry11021a16/core27ce0796/eight stages/114 layers preserved. '
        'Eight semantic/order rejections andown planned4001-frame startup/ten exact RGB pairs pass. Final manifest/clean patch/ownRAM/Fernan getters/261 credits remain. '
        'Next241 clean source objects(229 speeches/12 captions) havezero credited overlaps;90 meanings/independent drafts acrosseight complete exchanges saved,139 speech+12caption drafts andall comparisons remain. '
        '11845 integrated;verifiedcc71/main unchanged. No guide photos;all scope,ROMs andevidence preserved.')
    text=f'''# Rafael261 research complete/build live; next241 clean intake — November 5, 2026

Rafael’s early storyline and all tutorials remain first. Preserve every storyline, prior unfinished contextual pass, shared shop/town exchange, random scene, speaker/name/substitution and remaining player-facing text. No guide photos, main promotion, pruning or commit/push. The previous goal turn made verified progress:427 source objects were integrated once. This turn closes the next261 research gates and starts their registered build; it grants no new completion credit.

## Current261: complete research, preserved wording decisions

`translations/rafael_B85_B100_contextual_final_review_v1.json` seals **261 individual five-gate reviews:111 revisions/150 justified retentions**. Reuse the completed clean-source/whole-exchange comparisons; no prose was rewritten during the storage/gameplay pass. `work/analysis/Rafael261_checked_20261105/research_completion.json`, `complete_visual_approval.json` and `actual_review.json` are the compact evidence roots. All20 public name/role retentions are in `translations/rafael_B85_B100_scoped_names_final_v1.json`; this approves their scoped context, not the global207/full-catalogue review.

All255 speeches/256 body pages andsix captions inthree menus retain fresh native/visual approval. Ten wrap fixes, four full-width I fixes andsix English question-mark fixes remain preserved. Source details and earlier decisions are linked in [the preceding checkpoint](editorial_Help427_integrated_Rafael261_native_20261105.md). No shortened prose, new manual ordinary breaks, font enlargement or engine rewrite.

`work/analysis/Rafael261_rebased678_20261105/reconstruction.json` copies only reviewed B85–B100 blocks onto verified678. The11 changed dialogue blocks replace their earlier forms; B89/B94/B96/B98/B99 stay byte-identical controls. New B81–B84 andall Help202 remain intact. Research SHA-256 `7ec12144c3340331ea1c307c0f1ce56f06fb045ce59cd0f03e59de562bd8d150`. Exact ARM9/COMMON/font andcomplete own actor-array equality qualify earlier page/name/macro/menu proofs; `dependency_qualification.json` keeps original execution identities explicit. Captures are not relabelled as a new ROM.

Storage: `Rafael261_stored_native_20261105/stored_native_verification.json` passes255 speeches/256 pages, with118 parity-dependent pages freshly checked and138 exact compiled-page reuses. All complete leading/internal/trailing glyphs, pixels, bounds, canaries, substitutions andpagination pass. Sixty relative sites yield300 native branch cases. `Rafael261_stored_catalogue_20261105/all_stored_effective_body_bindings.json` proves all255 original lookups preserve the new bodies. `Rafael261_loaders_20261105/verification.json` passes343 whole loads/cache hits and686 handoffs:22 fresh changed-block modes/664 exact reuses. These are offline native checks.

Names: `Rafael261_scoped_name_planes_v2_20261105/native_name_planes.json` binds20 actors/18 distinct public strings, seven fresh style11 planes andeleven exact code/font/string reuses; both readable sheets were viewed. An evidence-variable name collision ended the first producer after partial planes; its files remain preserved, not a whole-run pass. V2 separates the template path from the native BASE constant. All source name decisions andboth original getter bindings remain unchanged. Actual current coverage includes16 actors, including all12 newly scoped identities andthree distinct Sailor portraits; Julio,Cristina,Angelo andGerhard remain unvisited in this batch with exact earlier public-name proofs retained. Full-catalogue UI/global207 approval remains open.

Two initialized English coldboots total20722 frames. `Rafael261_names_pages_actual_pixels_v1_20261105/focused_actual_pixels.json` and `Rafael261_menus_body_actual_pixels_v1_20261105/focused_actual_pixels.json` bind43 unique speeches/44 body pages,103 complete body holds and97 full header holds. `Rafael261_menus_actual_pixels_v1_20261105/menu_actual_pixels.json` passes allsix captions/both cursor states ineach ofthree menus, followed by dialogue after ordinary A acceptance. All four compact body sheets, one full-context sheet, one menu-response sheet andone cursor sheet were viewed.212 speeches are offline-only. The complete ten-speech Janus conversation andcorrected payer exchange read naturally; the former sailor’s initial criticism of belief is deliberate in the full Japanese exchange, followed by his shipwreck contrast/apology. Retain it.

The fixture copies native commands after normal New Game initialization; it does not prove original location, earned chronology, natural event activation, original conditional menu outcomes, numeric return registers, stat effects, cancellation, full route or hardware behavior. Native conditional/return behavior is separately covered offline. No guide-photo work.

## Registered679 build — preserve the live process

Profile `all-routes-rafael261-20261105` adds one exclusive `rafael-b85-b100` transaction after the full678 prefix. `work/analysis/Rafael261_registered_preparation_v2_20261105/registered_preparation.json` and `Rafael261_release_qualification_20261105/qualification.json` bind the direct/shared target, all261 objects, eight changed-scope/order rejections andevery unchanged final-stage contract. Registry SHA-256 `11021a16ab4b1157d9e34fc71f214fdb2b9eeb565325122444e59e261d0bcec0`; original core remains `27ce07965815b1c71ce39ce166406507fab621631b2373a96733eccd75dc2963`.114 accepted layers andall eight runtime/name/data stages, including ASCII right bounds andFernan’s F, remain mandatory.

The first preparation failed before registration because a dependency list named nonexistent `reviewed_choice_object_v1.py` instead of `reviewed_two_choice_object_v1.py`. All eight reference ROMs andtheir completed serialized inverses are preserved. V2 preflights every dependency andreuses those exact images/inverses without recreating them. Failure/reuse evidence: `Rafael261_registered_preparation_v1_20261105/pre_registration_failure_andreference_reuse.json`. There was no failed playable build orcredit mutation.

**Build session73098/PID105028 is OS-confirmed live**, original nine-driver source with system allocator/tighter unreachable-cycle collection:

```text
scripts/run_registered_build_with_gc_v3.py --profile all-routes-rafael261-20261105 --out out/all_routes_combined_rafael261_20261105_candidate.nds --work work/r261 --telemetry work/analysis/Rafael261_registered_build_20261105
```

Latest telemetry checked at{telemetry['elapsed_seconds']} seconds; collector errors empty. Do not restart quiet output ormutate its registry/configs/drivers/core/dependencies. Poll the same handle orconfirm authoritative terminal status. Expected679 manifest entries andfinal SHA-256 `7ec12144c3340331ea1c307c0f1ce56f06fb045ce59cd0f03e59de562bd8d150`.

Own planned startup is already terminal: `Rafael261_identity_coldboot_20261105/identity_RGB_qualification.json` binds4001 ordinary New Game frames, no savestate/battery/RAM override, ten byte-identical reviewed RGB/PNG pairs, unchanged B44/EV0/ARM9/COMMON/Help/font andonly11 owned SC0 block differences. Reuse this capture after exact registered equality; do not run another4001-frame capture just for the output filename.

On terminal0 run `scripts/verify_plain_SC0_registered_release_v1.py` with candidate, preparation, qualification, parent release `Help97_Rafael330_release_verified_20261105/registered_release_verification.json`, build-terminal `Rafael261_registered_build_20261105/completion.json`, build-work `work/r261` andout `Rafael261_release_verified_20261105`. It checks the full manifest/stages, exact individual stored references, unowned files/components/inverse andclean-input patch reconstruction. Then reuse `scripts/verify_registered_rafael_startup_v2.py` with the saved capture/parent startup, and `scripts/verify_rafael_B51_B60_own_Fernan_getters.py`. The new generic release verifier is prepared andparses; it has not run on a terminal registered679 output yet. Prepare once-only261 completion after these checks; the credit helper is not yet written. Predicted totals only then:12106 =6947 revisions+5159 retentions (historical source/prose12109). Do not credit early orpromote main.

## Next241 source objects — useful editorial work while the build runs

`work/analysis/Rafael_B101_B120_clean_20261105/clean_source_packet.json` inventories229 clean speeches in20 complete blocks, with two control-only blocks106/107. `clean_choice_objects.json` addsfour original three-choice menus/twelve captions. `completed_overlap_census_v1.json` findszero explicit/normalized credited source-key overlaps; this is not a global older-record technical re-audit.

`first90_source_meanings_andindependent_drafts_v1.json`, authored from `translations/rafael_B101_B110_clean_draft_data_v1.py`, seals90 source glosses/logical English drafts acrosseight complete exchanges before current SC0 English was consulted in this intake. It covers Julio/Cristina/Minerva’s Shield, the peacock andjaguar rumors, Janus’s telescope story, Emilio/Hestia’s cauldron, Yukihisa/Muramasa, the church lead andthe two-map-key explanation/blessing. Preserve the grandfather/father joke, uncertain clue locations, deliberate cooking humor, skepticism about the telescope legend, the goddess having a cauldron made rather than forging it herself, andthe unnamed sword. Titles/some identities are provisional, not approved orshippable.

Remaining:139 independent speech drafts,12 caption meanings/drafts andall241 current-English comparisons. Finish complete exchanges before comparing old English. Source selectors include18 ordinary actors, FE254 anddynamic207; bind207’s native role rather than invent a fixed actor. Source/control/name/glyph/formatting andregistered work remain pending for this next batch. No completion credit orblanket historical-English-exposure claim.

Integrated totals remain11845 =6836 revisions+5009 retentions; verified experimental parent is `out/all_routes_combined_help97_rafael330_20261105_candidate.nds`, SHA-256 `cc71ec06ce5345dcc71f8b631232f4d8d501152f6989374741616260fa0ca448`. Main stays `out/raphael_natural_v2_accepted_base.nds`, SHA-256 `3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe`. All ROMs/earlier translations/evidence preserved. Deferred graphics artwork andthe later older-record technical re-audit remain separate. Full editorial goal active.
'''
    protected={str(p):sha(p.read_bytes()) for p in [PREP,QUAL,RESEARCH,FINAL,STARTUP,DRAFTS,Path('translations/release_stack.json'),Path('dk4tool/rom/nds.py'),
        Path('out/all_routes_combined_help97_rafael330_20261105_candidate.nds'),Path('out/raphael_natural_v2_accepted_base.nds')]}
    for p,digest in load(BUILD/'request.json')['driver_andcanonical_bytes'].items():protected[p]=digest
    checkpoint(mutation='work/analysis/Rafael261_build_next241_checkpoint_20261105',completed=11845,protected=protected,
        batch_key='Rafael_SC0_B81_B100_clean_20261105',summary=summary,document='docs/editorial_Rafael261_build_next241_20261105.md',document_text=text,
        batch_updates=dict(new_credit=0,next261_review=str(FINAL),next261_review_sha256=sha(FINAL.read_bytes()),next261_all_fifth_gates_pending=False,
            next261_all_five_research_gates_pass=True,next261_research_completion=str(RESEARCH),next261_research_completion_sha256=sha(RESEARCH.read_bytes()),
            next261_registered_build_live=True,next261_build_session=73098,next261_build_PID=PID,all591_research_review_gates_pass=True),
        additional_updates={
            'Rafael_SC0_B85_B100_contextual_20261105':dict(new_credit=0,contextual_review=str(FINAL),contextual_review_sha256=sha(FINAL.read_bytes()),
                all_fifth_formatting_gates_pending=False,all261_five_research_gates_pass=True,actual_gameplay=True,
                actual_source_speeches=43,actual_body_pages=44,actual_choice_captions=6,offline_only_source_speeches=212,actual_fixture_frames=20722,
                stored_consumers_loaders_andrepresentative_actual_complete=True,needs_owned_block_rebase_to678_not_whole675_archive=False,
                registered_integration_pending=True,registered_build_live=True,build_session=73098,build_PID=PID,
                research_completion=str(RESEARCH),research_completion_sha256=sha(RESEARCH.read_bytes())),
            'editorial_execution_priority_20261104':dict(new_credit=0,current_batch='Rafael_SC0_B101_B120_clean_20261105',next_batch='Rafael261_registered_cumulative_20261105',
                registered_cumulative_build_live=True,registered_build_live=True,build_live=True,registered_build_terminal=False,registered_integration_pending=True,
                registered_build_session=73098,registered_build_PID=PID,build_session=73098,build_PID=PID,
                current261_four_gate_passes=261,current261_name_term_holds=0,current261_all_five_research_gates_pass=True,
                next_focus='Preserve live679 build;finish next139 source speech drafts+12 captions beforecurrent-English comparisons. Onterminal0 verify679 manifest/clean patch/ownRAM/Fernan getters andcredit261 once.'),
        },
        new_entries={
            'Rafael261_registered_cumulative_20261105':dict(new_credit=0,profile=prep['profile'],preparation=str(PREP),preparation_sha256=sha(PREP.read_bytes()),
                qualification=str(QUAL),qualification_sha256=sha(QUAL.read_bytes()),build_live=True,build_session=73098,build_PID=PID,
                expected_manifest_entries=679,accepted_layers=114,all_eight_final_stages_preserved=True,expected_candidate_sha256=prep['target_ROM_sha256'],
                expected_new_source_objects=261,expected_new_revisions=111,expected_new_retentions=150,
                own_planned4001_frames_terminal=True,own_planned_RGB_qualification=str(STARTUP),own_planned_RGB_qualification_sha256=sha(STARTUP.read_bytes()),
                registered_manifest_patch_RAM_binding_andonce_only_credit_pending=True),
            'Rafael_SC0_B101_B120_clean_20261105':dict(new_credit=0,source_packet=str(NEXT/'clean_source_packet.json'),source_packet_sha256=sha((NEXT/'clean_source_packet.json').read_bytes()),
                clean_choice_objects=str(NEXT/'clean_choice_objects.json'),clean_choice_objects_sha256=sha((NEXT/'clean_choice_objects.json').read_bytes()),
                source_speeches=229,source_choice_captions=12,source_objects=241,whole_blocks=list(range(101,121)),control_only_blocks=[106,107],
                completed_overlap_census=str(census),completed_overlap_census_sha256=sha(census.read_bytes()),
                independent_source_speech_drafts=90,remaining_independent_speech_drafts=139,caption_drafts=0,remaining_caption_drafts=12,
                first90_drafts=str(DRAFTS),first90_drafts_sha256=sha(DRAFTS.read_bytes()),contextual_comparisons=0,
                current_English_unconsulted_in_this_intake=True,no_blanket_historical_exposure_claim=True,source_dynamic_selectors=[207],
                term_name_control_formatting_current_comparison_actual_andintegration_pending=True,guide_photos=False),
        })
    print('Saved261 five-gate research/live679 build/next241 clean intake with90 drafts;11845 integrated unchanged;full goalactive.')
