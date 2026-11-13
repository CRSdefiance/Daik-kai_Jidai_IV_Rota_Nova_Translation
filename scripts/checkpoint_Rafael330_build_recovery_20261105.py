"""Save330 contextual decisions andthe exact live unchanged-source build;add no completion credit."""
import ctypes as ct
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load
from scripts.save_editorial_progress_checkpoint_v5 import checkpoint

ROOT=Path('work/analysis/Rafael_B81_B100_clean_20261105')
COMPARISON=ROOT/'B81_B84_325_whole_exchange_comparisons_v1.json'
CHOICES=ROOT/'B84_five_choice_comparisons_v1.json'
RETRY=Path('work/analysis/Sea22_Fleet66_malloc_retry_20261105')

if __name__=='__main__':
    comp,choices,request=map(load,[COMPARISON,CHOICES,RETRY/'request.json'])
    assert (comp['records_count'],comp['proposed_revisions'],comp['justified_retentions'],comp['first_four_gates_passed'])==(325,170,155,324)
    assert (choices['records_count'],choices['proposed_revisions'],choices['justified_retentions'])==(5,3,2)
    assert not (RETRY/'completion.json').exists()
    kernel=ct.WinDLL('kernel32',use_last_error=True);kernel.OpenProcess.argtypes=[ct.c_ulong,ct.c_int,ct.c_ulong];kernel.OpenProcess.restype=ct.c_void_p
    kernel.GetExitCodeProcess.argtypes=[ct.c_void_p,ct.POINTER(ct.c_ulong)];kernel.GetExitCodeProcess.restype=ct.c_int
    kernel.CloseHandle.argtypes=[ct.c_void_p];kernel.CloseHandle.restype=ct.c_int
    handle=kernel.OpenProcess(0x1000,False,113672);assert handle
    exit_code=ct.c_ulong();assert kernel.GetExitCodeProcess(handle,ct.byref(exit_code));kernel.CloseHandle(handle);assert exit_code.value==259
    summary=('Rafael/tutorial priority continues. All202 Help source topics retain completedfive-gate research;156 awaitregistered integration,no checks repeated. '
        'Original locked core27ce0796 andregistry82a17be4 areexact. New unchanged-source675 retry71768/PID113672 isOS-confirmed live withsystem allocator/tighter collection;all eight stages/114 layers/26 checks preserved. '
        'Next580 clean Rafael speeches havezero completed-ID overlap. Four whole exchanges nowhave325 contextual speech comparisons(170 revisions/155 retentions) plusfive choices(3 revisions/2 retentions). '
        '329 four-prose-gate passes;one bull-throw action ambiguity remains. Four full-width Latin artifacts inthree speeches andspecific name/skill/Quarters mismatches areidentified;all fresh display/stored/actual/release gates remain. '
        '11359 integrated/current9c5/main unchanged;zero newcredit,all scope/ROMs preserved,no guide photos.')
    document='''# Rafael330 and unchanged-source build recovery — November 5, 2026

Rafael's early story and tutorials remain first. Preserve the full all-route/earlier-translation/shared town-shop/random/name/glyph/wrap objective, all ROMs/evidence and existing credit. No guide photographs, promotion, pruning or commit/push. Reuse [the completed202-Help checkpoint](editorial_HELP_active_terms_remaining67_20261105.md); this turn repeats none of its page tests.

## Registered build recovery

The three earlier675 attempts remain terminal failures with preserved work/evidence. Original `dk4tool/rom/nds.py` is still exactly27ce07965815b1c71ce39ce166406507fab621631b2373a96733eccd75dc2963;the rejected optimization remains research only. A read-only Windows job query reports no process/job memory cap. No registry, native dependency guard, canonical builder or final-stage driver was changed.

`scripts/run_registered_build_with_gc_v3.py` runs all original nine registered drivers using `PYTHONMALLOC=malloc`,GC thresholds10/1/1 and0.25-second collection. Request/telemetry: `work/analysis/Sea22_Fleet66_malloc_retry_20261105/`. No other Python/native/emulator job was live at launch. **Session71768/PID113672 is OS-confirmed live**;do not restart a quiet job or mutate its registry/dependencies. Output is `out/all_routes_combined_sea22_fleet66_20261105_malloc_candidate.nds`,work `work/s22f66m`;expected81511dde target,675 entries/114 accepted layers/eight final stages/26 checks. Source/registry pins and target requirements are unchanged. There is no terminal build pass or candidate handoff yet.

On terminal0, prepare/execute the two-layer final verifier,exact clean patch,own startup/RAM and both Fernan getters,then add59 source credits once(37+22,44 revisions/15 retentions;66 amendment adds none). Existing4001-frame planned-identity capture and all Help/native/actual proofs remain reusable with exact bindings. Corrected31 and67 are ready for a **single ordered successor with two reviewed extensions**,subject to registration/qualification;combining them avoids two full rebuilds. Do not credit or promote before required checks/user acceptance.

## Next Rafael source and complete exchanges

`work/analysis/Rafael_B81_B100_clean_20261105/clean_source_packet.json` contains580 speeches across20 complete blocks;five blocks have no speech. `completed_overlap_census_v1.json` checks every relevant credited family with explicit source IDs and finds zero overlap. Clean-name fields and original EV0 event/dependency records are saved;numeric block order is not narrative chronology. Earlier English dialogue was not consulted before the new drafts;current name metadata alone was disclosed.

`B81_B84_325_clean_meanings_andlogical_drafts_v1.json` seals325 meanings/drafts. `B84_five_clean_choice_drafts_v1.json` seals both recruitment answers and all three training choices. `current_name_metadata_andclean_event_context_v1.json` binds exact source/current metadata. `work/analysis/Rafael_B81_B84_current_20261105/current_effective.json` uses the reusable v7 extractor's own verified Rafael/captain0 snapshot and325 original catalogue lookups,preserving every six-byte source preamble/command type. `current_choice_objects_v1.json` binds all five current typed labels;their providers/geometry have not been executed. All physical duplicate tutorial speeches remain separate.

Complete-exchange comparisons: `B81_B84_325_whole_exchange_comparisons_v1.json` has170 proposed revisions/155 justified retentions,324 four-prose-gate passes. `B84_five_choice_comparisons_v1.json` adds3 revisions/2 retentions/all five four-gate passes. Total330 objects:173 revisions/157 retentions,329 four-gate passes. **All fresh formatting/native body/name-plane/stored/representative-gameplay/release gates remain.** Other255 speeches in the580 packet have no completed draft/comparison credit. B85's10-speech Gerhard return is read as neighboring context,not reviewed/credited yet.

Findings include the reversed fear>affection turn before Mivor's resolve,non-source third-person this old man for Gerhard,missing Emilio Ferog surname,Manaus/Manous andGenz/Gentz inconsistencies,Cristina/Christina body inconsistency,non-source Master/Lady titles,andincorrect tutorial Aim/Gun Battery/Swords/Boarding Leader/Quarters wording. Four full-width Latin letters(three I/one F) occur inthree speeches;12 other records have copied punctuation/ellipsis candidates. Proposed normalization is visible-body-only and requires fresh consumer rendering;no controls were normalized. No display fix is claimed tested yet.

Retentions preserve concise reactions,emotional pauses,the mother's courtesy,Claudio's blunt asides andGerhard's natural military brevity. Each record has exact source/current references and a specific source intent/reason. Julio/Cristina grandfather-granddaughter kinship is explicit;the rescued child's familiar sibling-like addresses are localized without inventing kinship. The source father-nameヘラルド retains existing Herald with no independent Latin-source claim.

One concrete source risk remains: **B81 R106**,who throws whom at the bullfight. The independent draft reads Emilio throwing the bull;old English says the bull throws him. The Japanese leaves the object unstated. Its localization gate remains false pending original action/visual evidence;do not ship either reading on the authority of old English alone. Combine that focused check with the later B81 transition sample rather than starting a separate exhaustive playthrough.

Five newly scoped actors79/82/95/162/167 now have fresh clean/current name getters and current voice-selector bindings under `work/analysis/Rafael_B81_B84_new_name_bindings_20261105/names.json`. These confirm Mivor Genz,Shopkeeper,Patron,Boy,Lady in both original current name consumers. Reuse earlier compatible actor proofs where qualified;the complete16-actor scoped name binding/planes and retrospective207-name review remain open. No name fields changed and no global approval is inferred.

Integrated totals remain11359=6601 revisions+4758 retentions(source/prose11362). Editorial current remains Town9c5ca87b;main3cb827e4 remains unchanged. Graphics artwork and the older-record technical re-audit remain separate. Full objective remains active.
'''
    protected={str(p):sha(p.read_bytes()) for p in [COMPARISON,CHOICES,ROOT/'B81_B84_325_clean_meanings_andlogical_drafts_v1.json',ROOT/'B84_five_clean_choice_drafts_v1.json',ROOT/'completed_overlap_census_v1.json',RETRY/'request.json',Path('scripts/run_registered_build_with_gc_v3.py')]}
    protected.update({'translations/release_stack.json':'82a17be4f7610abef225fa39c2059cd4180511af5683f519aec8171de3df5f4e',
        'dk4tool/rom/nds.py':'27ce07965815b1c71ce39ce166406507fab621631b2373a96733eccd75dc2963',
        'out/raphael_natural_v2_accepted_base.nds':'3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe',
        'out/all_routes_combined_town_help23_20261104_candidate.nds':'9c5ca87bce5c4ace721ad4ce33c8409374eb412349acf4098098c927f08e7a9f'})
    live=dict(new_credit=0,build_live=True,registered_build_live=True,registered_cumulative_build_live=True,
        build_session=71768,build_PID=113672,registered_build_session=71768,registered_build_PID=113672,
        retry_request=str(RETRY/'request.json'),retry_request_sha256=sha((RETRY/'request.json').read_bytes()),
        original_locked_ROM_core_restored=True,all_original_registry_driver_andnative_guards_preserved=True,registered_integration_pending=True)
    checkpoint(mutation='work/analysis/Editorial_checkpoint_Rafael330_build_recovery_20261105',batch_key='editorial_execution_priority_20261104',
        batch_updates=dict(**live,current_batch='Rafael_SC0_B81_B100_clean_20261105',next_batch='sea22_fleet66_registered_cumulative_20261105',
            new_Rafael_source_speeches=580,new_Rafael_draft_speeches=325,new_Rafael_draft_choices=5,new_Rafael_comparisons=330,
            new_Rafael_four_gate_passes=329,new_Rafael_proposed_revisions=173,new_Rafael_justified_retentions=157,
            next_focus='Complete675 verification andcombine reviewed31+67 intoone registered successor;resolve B81R106 andformat330 Rafael objects.',guide_photos=False),
        additional_updates={k:live for k in ['sea22_fleet66_registered_cumulative_20261105','shared_HELP_T81_T102_contextual_20261104','shared_HELP66_Command_amendment_20261104']},
        new_entries={'Rafael_SC0_B81_B100_clean_20261105':dict(new_credit=0,source_speeches=580,source_blocks=list(range(81,101)),
            source_packet=str(ROOT/'clean_source_packet.json'),source_packet_sha256=sha((ROOT/'clean_source_packet.json').read_bytes()),
            completed_source_ID_overlap=0,source_draft_speeches=325,source_draft_choices=5,comparisons=str(COMPARISON),
            comparisons_sha256=sha(COMPARISON.read_bytes()),choice_comparisons=str(CHOICES),proposed_revisions=173,justified_retentions=157,
            contextual_comparisons=330,four_gate_passes=329,pending_source_action_IDs=comp['pending_source_action_record_IDs'],
            fullwidth_Latin_letters=4,fullwidth_Latin_records=3,all_fifth_gates_pending=True,all_registered_integration_pending=True,
            remaining_packet_speech_drafts=255,new_gameplay_runs=0,guide_photos=False)},
        summary=summary,document='docs/editorial_Rafael330_build_recovery_20261105.md',document_text=document,completed=11359,protected=protected)
    print('Saved330 contextual comparisons andlive original-source675 retry;11359 integrated unchanged. Full scope remains active.')
