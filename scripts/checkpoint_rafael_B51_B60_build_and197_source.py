"""Record the qualified live cumulative build andfresh source-only editorial progress."""
import ctypes as ct
from datetime import datetime,timezone
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load,save
from scripts.save_editorial_progress_checkpoint_v3 import checkpoint

ROOT=Path('work/analysis/Rafael_B51_B60_release_registry_v2_20261104')
SOURCE=Path('work/analysis/Rafael_B61_B80_clean_20261104')
RELEASE=Path('work/analysis/Shared_tutorial_name_data_release_verified_20261104/registered_release_verification.json')
PID=24560
SESSION=94922

if __name__=='__main__':
    prepared_path=ROOT/'registered_preparation.json';prepared=load(prepared_path)
    qualified_path=Path('work/analysis/Rafael_B51_B60_release_qualification_v2_20261104/qualification.json');qualified=load(qualified_path)
    startup_path=Path('work/analysis/Rafael_B51_B60_identity_coldboot_20261104/identity_RGB_qualification.json');startup=load(startup_path)
    release=load(RELEASE)
    assert len(qualified['semantic_rejections'])==12 and qualified['direct_andshared_scene_targets_equal']
    assert len(startup['exact_RGB_pairs'])==10 and startup['planned_ROM_sha256']==prepared['target_ROM_sha256']
    packet_path=SOURCE/'clean_source_packet.json';packet=load(packet_path)
    meanings_paths=[SOURCE/'B61_B63_77_clean_meanings_v1.json',SOURCE/'B64_120_clean_meanings_v1.json']
    meanings=[r for p in meanings_paths for r in load(p)['records']]
    assert packet['records']==539 and len(packet['groups'])==20 and len(meanings)==197
    assert len({r['id'] for r in meanings})==197 and all(r['earlier_English_unconsulted'] for r in meanings)
    # Read-only operating-system confirmation, not a stale run-plan assertion.
    kernel=ct.WinDLL('kernel32',use_last_error=True)
    kernel.OpenProcess.argtypes=[ct.c_ulong,ct.c_int,ct.c_ulong];kernel.OpenProcess.restype=ct.c_void_p
    kernel.GetExitCodeProcess.argtypes=[ct.c_void_p,ct.POINTER(ct.c_ulong)];kernel.GetExitCodeProcess.restype=ct.c_int
    kernel.CloseHandle.argtypes=[ct.c_void_p];kernel.CloseHandle.restype=ct.c_int
    handle=kernel.OpenProcess(0x1000,False,PID);assert handle,ct.get_last_error()
    try:
        status=ct.c_ulong();assert kernel.GetExitCodeProcess(handle,ct.byref(status))
        assert status.value==259,('Build is no longer live;poll its existing session before checkpointing.',status.value)
    finally:
        kernel.CloseHandle(handle)
    observed=datetime.now(timezone.utc).isoformat()
    snapshot=ROOT/'live_build_snapshot_v1.json';assert not snapshot.exists()
    save(snapshot,dict(PID=PID,exec_session_id=SESSION,observed_UTC=observed,Windows_process_exit_code=259,process_confirmed_live=True,
        command='C:/Python314/python.exe scripts/build_integrated_release_with_Fernan_field.py --profile '+prepared['profile']+
            ' --out out/all_routes_combined_rafael_b51_b60_Fernan_20261104_candidate.nds --work work/f8',
        expected_final_ROM_sha256=prepared['target_ROM_sha256'],registry_sha256=prepared['registry_sha256'],
        only_a_live_snapshot_repoll_handle_before_any_restart=True,producer_sha256=sha(Path(__file__).read_bytes())))
    summary=('Rafael/tutorial priority:249 reviews are registered andqualified (102 revisions/147 retentions,38 wraps/three I glyphs),witha separate exclusive Fernan F stage. '
        f'Cumulative eight-stage build session{SESSION}/PID{PID} is OS-confirmed live;final manifest/patch/own RAM binding pending. '
        'Exact planned-identity4001-frame startup matches10 reviewed RGB frames. Next Rafael B61–B80 clean intake has539 speeches;197 source-only meanings across B61–B64 aresealed before older English. '
        '10525 integrated completions andverified4b10fd67/main unchanged;all earlier work/ROMs/full scope retained;no guide photos.')
    document=Path('docs/editorial_rafael_B51_B60_build_and197_source_20261104.md')
    text=f'''# Registered Rafael build andnext source progress — 2026-11-04

Rafael early story andall tutorials remain first. Full storyline/shared shop/town/random/player prose scope andevery prior translation,retention,coverage credit,ROM andproof arepreserved. No main promotion,commit/push,pruning orguide photos. Graphics artwork andlater older-record technical re-audit remain separate.

## Build in progress

Previous turn was concrete progress:249 research reviews/representative actual checks were sealed. This turn registers andqualifies the complete cumulative successor andadvances197 new source meanings. Build session `{SESSION}`,PID `{PID}` was confirmed live by Windows GetExitCodeProcess==259 at `{observed}`. Snapshot:`{snapshot}`. Poll that exact session orcheckPID/command before deciding whether it is terminal;do not restart because output is quiet orobservation times out.

Command:`C:/Python314/python.exe scripts/build_integrated_release_with_Fernan_field.py --profile {prepared['profile']} --out out/all_routes_combined_rafael_b51_b60_Fernan_20261104_candidate.nds --work work/f8`.

Expected final SHA256:`{prepared['target_ROM_sha256']}`. Work path is deliberately short;deep canonical manifest path checked219 characters. The existing canonical builder/all guards andall seven earlier final drivers run unchanged;the eighth stage owns only actor35,column0,F-width data. Preserve every intermediate. No final candidate,manifest,clean-input patch orown registered RAM proof is claimed complete yet.

Authoritative preparation:`{prepared_path}`. Registry SHA256:`{prepared['registry_sha256']}`. Scene config:`{prepared['config']}`. Field config:`{prepared['field_config']}`. All114 accepted layers andall prior profiles remain unchanged. The seven earlier stage configs changed only whole-ROM parent/target identities (plus the bounds manifest/new dependency bindings);their tested code,fonts,field spans,pointers,allocations andqualification inputs remain exact.

The source-bound scene planner is `dk4tool/patch/rafael_B51_B60_release_v1.py`,with lowercase registry entry point `dk4tool/patch/rafael_story_b51_b60_release_v1.py`. It imports the existing generic compound-object compiler andcomplete-scene rebuilder. It rechecks all249 individual gates,logical/prose/compiled bindings,exact leading controls,three FE consumers,two complete2100 objects,stored/native/source/current references,complete branch maps,whole-archive andserialized NDS inverses,unowned files/components andexact whole-ROM identities. No renderer/code/font edits are hidden in the SC0 extension.

Separate field planner:`dk4tool/patch/registered_Fernan_name_field_v1.py`;driver:`scripts/build_integrated_release_with_Fernan_field.py`. Both original getters/four native planes/eight negatives are reused on the explicit current-parent disjoint-data qualification. The plan rescans exclusive ownership/references,requires the exact seven-byte/six-difference field plan,all18-name reviewed context andcomplete actual normal-F header,andverifies whole-ROM inverse/unowned preservation. Full catalogue UI remains unvisited. AGENTS/build continuity now require this eighth stage/config/check for `owned_Fernan_name_field` profiles.

The first preparation used an uppercase production adapter module. The shared extension guard rejected that binding before any build. Preserve `work/analysis/Rafael_B51_B60_release_20261104/registered_preparation.json`,its original configs/reference ROMs andthe rejected qualifier. The repaired v2 preparation reuses all seven exact reference ROMs andproves the lowercase shared extension before publication. Only the new experimental profile's last adapter/config andbounds-dependency binding changed;no prior profile/main/ROM was overwritten. Do not rerun the rejected preparation ormodify its frozen producers.

Qualification:`{qualified_path}`. Direct/shared249-record production plans andseparate Fernan final data plan pass;12 invalid release inputs are rejected (failed per-record gates,changed selector/body/choice index,missing actual page,failed name/menu/header/getter proofs,wrong field owner andstale complete parents). All caller objects remain exact. Earlier native compiler/field negative cases are reused,not rerun. All seven prior stage contracts were compared exactly. These are production planner tests,not additional gameplay observations.

## Startup identity evidence already captured

`{startup_path}`. `scripts/capture_rafael_B51_B60_startup.py` cold-booted the exact planned final research identity for4001frames using ordinary title/NewGame/Rafael inputs,no battery/savestate/RAM override. All10 RGB frames arebyte-equal to the previously directly reviewed registered4b10fd67 startup. Exact EV0,openingSC0B44,COMMON/fonts,all unowned files andcode areunchanged;onlyten laterSC0 blocks andthe exclusive Fernan field differ. The matching prior startup visual approval is reused explicitly;no new direct visual inspection is claimed. Capture/dumps areunder `work/analysis/Rafael_B51_B60_identity_coldboot_20261104`.

This remains planned-identity evidence until the registered output hash matches;own RAM/current captain0/route0/getters/payload/actors must still be bound by the final startup verifier. Reuse these completed captures once equality is proven;do not rerun an identical4001-frame capture without a changed dependency orfailed risk.

##249 batch state andremaining release work

Final research manuscript:`translations/rafael_B51_B60_contextual_final_review_v1.json`;all five gates pass,102 revisions/147 retentions. Formatting:253 body pages/four choice captions,38 wrap fixes/three ASCII-I glyphs. Two initialized fixtures observed32 speeches/35 body pages/four captions andall18 scoped headers;213 speeches remain offline-only. Full original conditions/earned chronology/locations/routes/hardware,original menu narrative branches/cancellation andfull catalogue UI remain unvisited. All prior native/visual/stored/catalogue/loaders/actual proofs aresealed;see `docs/editorial_rafael_B51_B60_research_ready_20261104.md`. Do not repeat those checks.

When build is terminal0,verify final manifest/registry/profile/all accepted batches/eight stage configs andinverse checks,exact source-bound scene andFernan bytes/all unowned preservation,clean-input xdelta andwhole-ROM reconstruction. Then bind the exact planned4001-frame capture/own RAM through a Rafael startup verifier that permits the one separately proved field change;never ignore ARM9 differences. Reuse the parent startup10-RGB chain;verify original native current captain0/route0 andprotected names using this candidate's own dump. Only then credit249 exactly once. Expected totals after verified integration:10774 complete,6356 revisions/4418 retentions. Current totals remain10525/6254/4271,source/prose/draft historical10528 unchanged. No credit is granted by this checkpoint.

Verified prior candidate remains `{release['candidate']}`,SHA256 `{release['candidate_sha256']}`,with its exact clean-input patch/own startup. Main remains `out/raphael_natural_v2_accepted_base.nds`,SHA256 `{release['canonical_sha256']}`. Current registry legitimately has the new experimental profile in addition to the historical registry associated with that prior candidate;do not rewrite prior manifests.

## Next Rafael source work:539 speeches,197 meanings finished

Clean-only packet:`{packet_path}`,SHA256 `{sha(packet_path.read_bytes())}`. Original cleanROM `work/clean.nds`,SHA256 `{packet['source_ROM_sha256']}`.20completeSC0 blocks61–80 contain539 speeches;block68has zero speeches andremains control-only,not a missing translation. No2100/4100 objects occur in this source intake. Exact native source commands,preambles,selectors,source references/macros andcomplete block bytes arebound. No existing contextual coverage keys for theseSC0 blocks were present;bare IDs from other routes are not overlap.

Source-only meanings:`{meanings_paths[0]}` (77,B61–B63) and`{meanings_paths[1]}` (120,B64). All197 areread as complete exchanges before consulting old English. They are source glosses,not approved localized drafts orfive-gate completions. No existing English for B61–B80 has been read this turn. Preserve539-record intake andall untouched later groups. Remaining342 speech meanings,B65–B80,still need the same clean source pass;then exact clean name/full/public/private identity andEV0/conditional memberships,English drafts,current comparison,formatting andregistered integration.

B61:Kuhn jar/vessel defeat alternatives,Pereira's source self-title/joke and500000 military funds. Keep the exact amount,sourceconditional short/long replies andthe familiar older-man address without kinship. The vessel's exact named-item binding is still pending;do not invent a treasure name.

B62:unknown actor179 offers an empty sword scabbard;Rafael/Arcadius alternative map-key conclusions andClaudio's explicit NewWorld reference. Proper name/role bindings remain pending;do not invent a blade,giver biography orformal king rank.

B63:Claudio's anger over physical labor,Rafael's defensiveness,private Eirene reassurance anda meal/comic payoff. Source explicitly says the public Arcadius persona is believed male andconceals being a woman. Preserve private sourceエイレネ andpublic speaker controls without globally renaming Arcadius;final English spelling/native fields still need binding. The older-sister phrase is an explicit comparison,not kinship. Rafael's final scholar explanation is comic uncertainty,not permission to invent romance.

B64:120-speech village rescue/argument,patronizing charity offer,woman's difficult apology,Claudio's change of heart,an actual trade andthe migration account. Source identifies her people asジプシー. Preserve the Romani ethnic/cultural identity instead of reducing it to generic nomads orimplying settlement ended their ethnicity. Her theft/disease examples report discriminatory accusations;they are not endorsed generalizations. Her parents/family/village areexplicit. Reported promises of gold/fertile land aredeceptive recruitment,not verified narrator facts. Dates stayapproximate:two orthree years to self-sufficiency,aboutone year since ships/barter. Rafael connects their lack of a homeland with Portugal's threatened annexation. The charity wording andher echoed objection must remain coherent as a full exchange in English. Charlotte is provisional sourceシャルロット transliteration until exact proper-name binding;no romantic relationship is inferred.

Continue useful source/prose work while the canonical build runs. Do not use repetitive status polls as a substitute for editorial progress. All other routes/shared/town/random/tutorial/prose obligations andthe deferred graphics/older-record work remain intact.
'''
    checkpoint(mutation=ROOT/'build_and197_source_checkpoint_mutation_v1',batch_key='Rafael_SC0_B51_B60_contextual_20261104',
        batch_updates=dict(new_credit=0,registered_preparation=str(prepared_path),registered_preparation_sha256=sha(prepared_path.read_bytes()),
            release_qualification=str(qualified_path),release_qualification_sha256=sha(qualified_path.read_bytes()),
            registered_profile=prepared['profile'],registered_integration_pending=True,
            build_exec_session_id=SESSION,build_PID=PID,build_confirmed_live_at_UTC=observed,
            expected_registered_candidate='out/all_routes_combined_rafael_b51_b60_Fernan_20261104_candidate.nds',
            expected_registered_candidate_sha256=prepared['target_ROM_sha256'],planned_identity_startup_RGB=str(startup_path),
            planned_identity_startup_frames=4001,own_registered_RAM_binding_pending=True,
            remaining=['Poll live build94922/PID24560;do not restart on quiet output','Final registered manifest/eight-stage/clean-input patch inverse',
                'Bind exact planned identity capture andown native RAM/getters','Once-only249 credit after verification']),
        additional_updates={'editorial_execution_priority_20261104':dict(new_credit=0,
            current_batch='Rafael_SC0_B51_B60_contextual_20261104',next_batch='Rafael_SC0_B61_B80_clean_20261104',
            Rafael_early_story_andall_tutorials_first=True,registered_cumulative_build_live=True,next_source_meanings=197,
            full_editorial_scope_preserved=True,guide_photos=False)},
        new_entries={'Rafael_SC0_B61_B80_clean_20261104':dict(new_credit=0,source_speeches=539,source_blocks=list(range(61,81)),
            source_packet=str(packet_path),source_packet_sha256=sha(packet_path.read_bytes()),
            source_meanings=197,source_meaning_blocks=[61,62,63,64],source_meaning_files={str(p):sha(p.read_bytes()) for p in meanings_paths},
            earlier_English_unconsulted=True,source_glosses_not_final_localized_English=True,
            exact_source_current_native_names_event_membership_drafts_andall_five_gates_pending=True,
            zero_speech_control_only_blocks=[68],remaining_source_meanings=342,
            full_editorial_scope_preserved=True,actual_gameplay_records=0,guide_photos=False)},
        summary=summary,document=document,document_text=text,completed=10525,
        protected={'translations/release_stack.json':prepared['registry_sha256'],release['candidate']:release['candidate_sha256'],
            release['patch']:release['patch_sha256'],'out/raphael_natural_v2_accepted_base.nds':release['canonical_sha256']})
    print('Saved qualified live8-stage build94922/PID24560 and197 clean-only source meanings;10525 integrated completions/main unchanged;full goal active.',flush=True)
