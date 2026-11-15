"""Freeze a truthful thread handoff after the existing Stockholm run terminates."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/editorial_thread_checkpoint_v1868')
AUDIT = Path('work/analysis/lil_Stockholm_revised_audit_v1867c/revised_Stockholm36_branch_and_three_fixture_audit.json')
REFERENCE = Path('work/analysis/lil_Stockholm_reference_census_v1866/all102_commands24_relative_sites_and_shipped_entry_census.json')
PROMPT = Path('docs/editorial_next_thread_prompt_v1868.txt')

STATUS = """V1868 thread-switch checkpoint: Stockholm B27 has 51 source/prose/native-font-approved paragraphs (38 proposed revisions, 13 retained). Research relocation preserves all 102 commands and 24 typed relative spans, grows 2692 to 2972 bytes (+280), and passes 120 relocated native skip cases. Both versions pass 336 whole-SC2 loads/cache hits and 672 parent-entry modes each. Revised research gameplay completes 36 speeches with 72 complete native/independent/actual-pixel holds, the original art pause, all 75 original command/result pairs and normal Stockholm town return at frame 62850. Three fixtures alter 16 coordinate bytes each; inputs, captures, full 4 MiB footprints and read-only observer restoration pass. All six contact sheets and the town return were visually reviewed. Command timing differs by at most three frames after prose changes; actual timings are recorded, not asserted identical. Fifteen conditional speeches, including nine Gerhard 0x10 speeches, were not individually activated. All test jobs are terminal. Final relocation-map approval, the guarded production compiler, registered integration, exact patch and startup controls remain pending. No completion credit added: 1529 complete (1158 revised, 371 retained), 1696 source/prose reviewed, 116 incomplete COMMON and 51 incomplete SC2 drafts plus broader untouched prose. Registered V1841 and promoted V1492 remain unchanged. Graphics/all 18 plaques and later older-record re-audit remain separate and unfinished. No new push or promotion."""

NEXT = """/goal Complete the full scene-by-scene editorial review of Translation DS: shared shop/town dialogue, every route, and all remaining player-facing prose. Compare the current English with clean Japanese and surrounding dialogue; use natural, faithful American English while preserving facts, tone, character voice, approved names (Rafael, Hodram, Joakim, Maria and Camille), complete speaker/layout controls and runtime substitutions. Maintain exact source/current coverage and justified retentions. Follow natural-dialogue-v2 and registered release workflows. Verify automatic line breaks, complete leading/trailing letters, bounds, pagination and scene transitions using native rendering and targeted gameplay. Integrate revisions into a registered cumulative ROM with an exactly reconstructable clean-input patch and update progress before crediting completion. Keep the unresolved graphics audit separate and unfinished, and retain the later older-record re-audit.

Continue in the existing dk4-translation-tool worktree. Read docs/editorial_handoff_current.md first, then verify the current files and evidence. The V1868 handoff records the finished Stockholm research test and precise remaining integration gates; no emulator or driver is still running. Resume with Stockholm B27 final reference/presentation-scope approval and production integration, without repeating the completed source/font/gameplay work unless evidence requires it. Preserve ALL generated ROMs; use E:/Rota Nova translations for generated ROMs, evidence and screenshots. Keep V1492 promoted and the canonical baseline unchanged; do not promote or push without a new request. Do not create subagents without authorization. Redirect integrated-builder stdout to a new log and inspect only selected manifest fields to avoid excessive context growth. Keep the full editorial goal intact.
"""

SECTION = """## Current working unit: Stockholm B27, V1868 thread-switch checkpoint

All test processes are terminal. Existing revised runner 1864/session21771 and navigation 1865/session1133 both exited 0 after normal frame62850 return. No test was restarted after compaction. No new test or build should be inferred to be live from old notes.

### Completed evidence, not yet registered editorial completion

- Source packet: `work/analysis/lil_Stockholm_source_v1848b/all51_clean_current_native_source_context.json`; 102 original commands, 51 speeches, five speaker IDs, clean/current references and neighboring context.
- Approved manuscript: `translations/lil_Stockholm_encounter_editorial_manuscript_v2.json`; 38 proposed revisions, 13 justified retentions. Do not shorten the prose to old fixed slots. The fixed encoder/PAD declaration is an allocation probe until the final relocation map is approved.
- Full fonts: `work/analysis/lil_Stockholm_fonts_v1858/all51_native_macros_and_complete_font_planes.json`; 51 native/independent planes and408 macro/alignment calls, all seven sheets viewed. Approval1859b records18 narrow per-record line-break-count waivers and five negative scope/control/review tests.
- Speaker scope: `dk4tool/dialogue/lil_stockholm_profile.py` binds exact ARM9 and original clean/current B27 hashes and adds only leading0x10. Global profiles still reject0x10; scoped profile rejects0x11. `work/analysis/Gerhard_story_control_proof_v1857/original4000_prefix10_Gerhard_live_mapping.json` proves the shared native selector with fixture-free Hodram SC1B42 live Gerhard portrait/name/body and ordinary dismissal. This is not nine B27 visits.
- Relocation1861: `work/analysis/lil_Stockholm_relocation_v1861/nested_source_relocation_research.json`; B27 2692->2972 bytes (+280), 51 whole preambles/parity and102 commands preserved, 24 typed spans/120 target-native cases, exact inverse, 51 parity-space native rasters. Research block SHA256 eb5170c5ff559c68f7b9508f0dc87737d93ef882c717dad40c6b602b4ea00a4f.
- Research1862: `work/analysis/lil_Stockholm_research_v1862/lil_Stockholm_V1841_derived_RESEARCH_ONLY.nds`; SHA256872f4047dd3c9ee335dc7e6dbff5e96af668c67b07e145f29422db71c0871d97. Only SC2B27 changes; every other block/file/component, ARM9, COMMON and staged123040 bytes remain exact. This image is unregistered research, never a production parent or user release.
- Loader1863: `work/analysis/lil_Stockholm_loader_v1863/whole_SC2_and_B27_initial_entry_proof.json`; current/research each336 whole loads/cache hits and672 parent-entry modes, original EV2 block-index selection/payload+8, exact guards/metadata, only original SDK IO bridges.
- Reference census1866: `work/analysis/lil_Stockholm_reference_census_v1866/all102_commands24_relative_sites_and_shipped_entry_census.json`; clean/current/research code/overlay census, only original24070 interpreter entry and no literal aliases, all102 original native command walks/opaque bytes/preambles/ancestors and335 other blocks preserved. Every opcode type has original actual evidence. This is not the final approved release map.
- Revised actual1867c: `work/analysis/lil_Stockholm_revised_audit_v1867c/revised_Stockholm36_branch_and_three_fixture_audit.json`;36 speeches/72 full native-independent-actual ink and exact wrapped-C-string holds,75 original command/result pairs, original2000 art pause, natural event27 completion and normal town return62850. Input journals/capture hashes/full4MiB snapshots/three coordinate-only fixture replays and observer host restoration pass. All six contact sheets and terminal town capture were visually viewed. Changed prose yields command timing deltas up to3 frames; timings are recorded, not required identical.
- Actual capture folder: `E:/Rota Nova translations/Generated/work/emulation_v193/lil_Stockholm_revised_run_v1864_RESEARCH_ONLY`. Runner/source/journal: `scripts/run_lil_Stockholm_revised_v1864.py`, `work/analysis/lil_Stockholm_revised_run_v1864`, driver `scripts/navigate_lil_Stockholm_revised_v1865.py`.
- Three16-byte coordinate-only fixtures at30290 (Bruges1754),42580 (Amsterdam1833c),48810 (Stockholm1850). Native discovery49440 and docking50040; town7 known flag0->2, event27 complete0->1. No save/savestate, RNG, event, outcome, actor or message override. Headless targeted evidence, not a full route playthrough/hardware proof.
- Fifteen conditional IDs not individually activated: R83,87,91,94,97,101,105,108,127,196,200,204,207,233,237 (all DK4_MES_B27_). Native Gerhard condition0x3000FE10 returns0; Fernando0x3000FE14 returns1. Do not report all51 as individually played.
- Failed audit1867 used `.data` on an ILNK bytes block;1867b overrequired equal command frames after prose changes. Both failed before output creation; frozen successors retained.1867c fixes the API and records frame deltas while retaining exact command path/results, per-hold timing and all source/input/glyph checks. No emulator restart.

### Exact next work

1. Review source/native/presentation evidence for all51, explicitly state the 36 actual/15 conditional sampling scope, and approve a final source-bound relocation map. If a specific conditional presentation risk remains, gather targeted original-path evidence; do not substitute structural walking for actual gameplay.
2. Implement a guarded production compiler/release config using the B24 module `dk4tool/patch/lil_trade_routes_editorial.py` and lessons references as templates. Rebuild from approved prose and typed spans, not from a research binary. Preserve all complete six-byte preambles, byte parity/optional trailing space, macros, opaque commands and inverse restoration. Call private `profile_for(arm,original_B27)` before mutation. Bind source/runtime/config/map and add meaningful negative gates.
3. Add an experimental integrated profile after the complete V1841 stack and before final story-percent/art guards. Preserve114 accepted layers and every previous profile. Expected479 manifest batches if one new manuscript is added. Use `scripts/build_integrated_release.py`, redirect its enormous stdout to a NEW log, and inspect narrow manifest keys only. Never use the research ROM as parent.
4. Prove whole registered ROM equals the tested research image, exact clean-input xdelta reconstruction, all335 untouched SC2 blocks/every other component and123040 staged bytes; run required fresh startup/New Game regression controls. No automatic promotion; V1492 remains promoted.
5. Only after all final gates pass, add51 completions (38 revised13 retained), update coverage/progress and save selected finalized guide screenshots. Continue broader shared/routes/player prose afterward; do not redefine the full goal as this one batch.

Original eligibility1846/1847 remains documented: London B26 is an unreviewed111-speech lead; B25 requires event128, not24. Event80 predicate has an original LCG write in a disposable offline copy; never claim every predicate query is pure or alter live RNG.

Current counts stay1529 complete/1696 source-prose reviewed. Registered V1841 unchanged. No new ROM promotion, commit or push requested or performed during this checkpoint. No subagents authorized. The next-thread goal text is saved at `docs/editorial_next_thread_prompt_v1868.txt`.

"""

if __name__ == '__main__':
    assert not ROOT.exists() and not PROMPT.exists()
    audit, reference = read(AUDIT), read(REFERENCE)
    terminal = read('work/analysis/lil_Stockholm_revised_run_v1864/terminal.json')
    assert terminal['terminal'] and terminal['frame'] == 62850
    assert audit['all36_activated_revised_speeches72_holds_complete_native_independent_actual_glyphs']
    assert audit['same75_original_commands_results_and_event_transitions']
    assert audit['all_inputs_capture_hashes4MiB_snapshots_and_three_coordinate_footprints_verified']
    assert audit['all_readonly_observer_boundaries_and_host_restoration_pass']
    assert len(audit['contact_sheets']) == 6 and len(audit['unvisited_original_speech_IDs']) == 15
    assert reference['all102_commands_reexecuted_clean_current_and_target']
    ledger_path = Path('translations/editorial_review_current_v1.json')
    ledger = read(ledger_path)
    assert (ledger['records_editorially_completed'], ledger['records_with_source_and_prose_pass']) == (1529,1696)
    registered = ledger['current_integrated_candidate']
    assert sha(Path(registered['path']).read_bytes()) == registered['sha256'] == '84be5d1e7382fcec09ba0846292dec418cff44533f81f843f10dd541c2cd6a28'
    ROOT.mkdir(parents=True)
    handoff = Path('docs/editorial_handoff_current.md')
    (ROOT/'handoff_before.md').write_bytes(handoff.read_bytes())
    (ROOT/'ledger_before.json').write_bytes(ledger_path.read_bytes())
    ledger['latest_checkpoint'] = STATUS
    ledger['lil_Stockholm_thread_checkpoint_v1868'] = {
        'revised_actual_audit': str(AUDIT), 'revised_actual_audit_sha256': sha(AUDIT.read_bytes()),
        'reference_census': str(REFERENCE), 'reference_census_sha256': sha(REFERENCE.read_bytes()),
        'all_test_jobs_terminal': True, 'actual_revised_speeches': 36, 'complete_actual_holds': 72,
        '15_conditional_records_not_individually_activated': audit['unvisited_original_speech_IDs'],
        'all_six_actual_contact_sheets_and_terminal_town_visually_reviewed': True,
        'registered_integration_final_map_patch_and_startup_pending': True,
        'completed_entries_added': 0, 'full_goal_complete': False}
    save(ledger_path,ledger)
    text=handoff.read_text(encoding='utf-8').replace('# Current editorial handoff - V1859','# Current editorial handoff - V1868')
    start=text.index('## Current working unit:'); end=text.index('## Latest completed scene:',start)
    text=text[:start]+SECTION+text[end:]
    text=text.replace('User askedwhethernewthread advisable;recommendedfreshthread,notauthorizedcreationyet.',
        'User explicitly requested preparation for a new thread; current V1868 checkpoint is the authoritative resume point. Do not create a thread unless separately requested.')
    handoff.write_text(text,encoding='utf-8')
    PROMPT.write_text(NEXT,encoding='utf-8')
    for name in ('editorial_review_goal.md','translation_progress.md','known_issues.md','todo.md'):
        p=Path('docs')/name
        with p.open('a',encoding='utf-8') as f:
            f.write('\n\n## V1868 thread-switch checkpoint\n\n'+STATUS+'\n\nSee [current handoff](editorial_handoff_current.md) and [next-thread goal](editorial_next_thread_prompt_v1868.txt).\n')
    evidence = [AUDIT, REFERENCE, PROMPT, handoff, ledger_path,
        Path('work/analysis/lil_Stockholm_revised_run_v1864/terminal.json')]
    save(ROOT/'checkpoint_receipt.json',{
        'status':STATUS,'all_jobs_terminal':True,'no_new_registered_build_push_or_promotion':True,
        'completion_count_unchanged':1529,'source_prose_reviewed_unchanged':1696,
        'goal_active_full_scope_unchanged':True,'next_thread_prompt':str(PROMPT),
        'evidence':{str(p):sha(p.read_bytes())for p in evidence},
        'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    print({'checkpoint':'V1868','actual_revised_speeches':36,'all_jobs_terminal':True,'completion_credit_added':0},flush=True)
