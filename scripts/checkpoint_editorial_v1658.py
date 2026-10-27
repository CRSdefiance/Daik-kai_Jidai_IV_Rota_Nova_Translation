"""Checkpoint completed review work and terminal tests;full goal remains active."""
from pathlib import Path
from shutil import copy2
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/editorial_checkpoint_v1658')
ARCHIVE = Path('E:/Rota Nova translations/Editorial review/V1658 Search prose and hot spring test checkpoint')

if __name__ == '__main__':
    assert not ROOT.exists() and not ARCHIVE.exists()
    ledger = read('translations/editorial_review_current_v1.json')
    assert (ledger['records_editorially_completed'], ledger['records_revised_and_integrated'],
            ledger['retained_wordings_editorially_completed'], ledger['records_with_source_and_prose_pass'],
            len(ledger['reviewed_but_incomplete_COMMON_IDs'])) == (1350, 1009, 341, 1519, 169)
    terminal = Path('work/analysis/hot_spring_crew_terminal_v1657/terminal95860_preservation.json')
    preservation = read(terminal)
    assert preservation['terminal_frame'] == 95860
    assert preservation['all48_location20_supply10_crew_owned_bytes_and_all_other4MiB_audited']
    assert preservation['all_inputs_snapshots_PNG_hashes_and_unchanged_source_disposable_saves_audited']
    cap = Path('E:/Rota Nova translations/Generated/work/emulation_v193')
    old, new = [read(cap / folder / 'capture_report.json') for folder in
                ['hot_spring_notice_resilient_v1645_1637', 'hot_spring_crew_v1651_1637']]
    assert old['frames'] == 53178 and new['frames'] == 95860
    p, q = [{r['frame']: r for r in report['frames_captured'] if r['frame'] <= 42673} for report in [old, new]]
    assert p.keys() == q.keys() and len(p) == 296
    assert all(p[n]['PNG_sha256'] == q[n]['PNG_sha256'] for n in p)
    release = read('work/analysis/hot_spring_notice_release_v1636/registered_release_verification.json')
    assert release['candidate_sha256'] == new['ROM_sha256'] == preservation['candidate_sha256']
    assert sha(Path(release['candidate']).read_bytes()) == release['candidate_sha256']
    assert sha(Path(release['patch']).read_bytes()) == release['patch_sha256']
    ROOT.mkdir(parents=True)
    save(ROOT / 'all296_replayed_prefix_PNGs_byte_exact.json', {
        'candidate_sha256': release['candidate_sha256'], 'prefix_through_frame': 42673,
        'all296_complete_PNG_files_byte_exact': True,
        'frames': [{'frame': n, 'previous': p[n]['path'], 'current': q[n]['path'], 'PNG_sha256': p[n]['PNG_sha256']} for n in p],
        'native_glyph_completion_or_optional_branch_credit': False})
    note = '''# Current editorial handoff - V1658

## Goal and counts

The full scene-by-scene natural-English editorial goal remains ACTIVE. Coverage:
1350 complete =1009 revised +341 retained;1519 source/prose reviewed;169 reviewed
but incomplete COMMON (earlier144 +hot-spring13 +notice310 +new Search reports11).
Broader shared/town/shop,all routes and remaining player-facing prose remain.
Separate graphics/all18 plaques remain unfinished. Accepted wood textures/borders
do not close those entries. Keep the four low-resolution Online bodies excluded
and the two brown marks preserved. Revisit older record-based checks after the
editorial goal. Preserve Rafael,Joakim,Maria,Camille.

## Integrated release

Latest experimental cumulative ROM:out/all_routes_combined_v1637_candidate.nds.
SHA256 0d81ee2668d2ff535432e2a50a5df44b9c1a4b0f683fca407f5753348038e7b2.
Exact patch SHA256 922fdf497eaabea655e3b9529ce309386f8ee129d5ba5c07885de5eddf658856.
Profile all-routes-unified-v1637,473 batches114 accepted layers;release proof
work/analysis/hot_spring_notice_release_v1636/registered_release_verification.json.
V1492 remains promoted;immutable construction base and historical V997 unchanged.
Completed-native reference stays V1594 until hot-spring14 closes. Preserve the
later screenshot-text-repairs-centered-20261022 stage in every successor.
No new ROM was built in V1650-V1658;the eleven new drafts are not integrated.

## New source/prose review11

translations/search_reports_editorial_manuscript_v1.json reviews COMMON312,
2217-2221 and2229-2233 against clean Japanese and original consumers. Restore
the expedition's return,tentative findings/hearsay and complete foraging reports.
Use two original quantities in water-food order,barrels for each.312 retains one
original loss amount without asserting death. All prose is unwrapped and unpadded.
Formatting gates remain FALSE:source/prose only,no completion credit.
Source/callers/neighbors/coverage receipt:work/analysis/search_reports_source_v1653.
Failure role1/table02116EC0 and forage role7/table02116E80 need independent native
argument/formatter contracts.312 is a separate modal. Preserve their distinctions.
Next useful implementation work is a source-locked native plan for these11;
then complete fonts,bounds,negative compiler cases,copies,registered release,
exact patch,startup and revised original-gameplay samples. Do not call drafts done.

## Hot-spring14 remains pending

hot_spring_editorial_manuscript_v2.json has13 source/native-approved lines inV1622
and inherited byV1637;hot_spring_notice_editorial_manuscript_v2.json adds310 inV1637.
New310 is The hot spring boosted Experience. All14 remain reviewed-incomplete.
Source/native font/selector/ABI/copy proofs and startup/patch/shop preservation
exist;the original optional relaxation/table02116D60 and notice310 still have NOT
been activated in gameplay. Discovery2276 and recovery309 have actual coverage.
The optional branch reads original captain stat5;do not infer it from ordinary
discovery or dispatch a numeric message as proof. Preserve original event choices.

## All current jobs terminal

Old emulator58934 terminal53178 at Assign Sailors,not normal Sea View. Audited:
work/analysis/hot_spring_resilient_terminal_v1650a/terminal53178_preservation.json.
Navigator1649 mistook stale339 for live dialogue there and sent repeated A.
This was a test-navigation error,not a ROM formatting defect. Inputs are retained.
Successor1652 requires visible paper before acknowledging loaded dialogue.
1655 failed before input due a Python local binding;1655b fixes it explicitly.
Navigation masks/paper checks do NOT count as complete-glyph verification.

Successor emulator69622 is terminal95860,normal Sea View directly viewed before
stop. Captures:E:/Rota Nova translations/Generated/work/emulation_v193/hot_spring_crew_v1651_1637.
Runner:scripts/run_hot_spring_crew_v1651.py;log:work/hot_spring_crew_v1651.log;
journal:work/analysis/hot_spring_crew_v1651/navigation.jsonl. No active handle.
Its original input prefix through42673 matches all296 previous PNG files exactly.
At57475/57505 original2276 discovery,57725/57755 original309 requested-15 recovery;
57755 viewed;A returned to viewed normal Sea View57975 without optional branch.
Routine attempts continued through95860;no relaxation/310 observed.
Full audit:work/analysis/hot_spring_crew_terminal_v1657/terminal95860_preservation.json.
It reproduces all48-byte location,20-byte supply and10-byte live-crew fixtures,
all other4MiB bytes,every input/capture/RAM hash,and unchanged source/disposable
battery saves. No savestate. No direct actor/skill/fatigue/RNG/event-result writes.

User-authorized crew fixture native_hot_spring_crew_v1650.py restores only ten
live ushort bytes at mobile+1A to original persisted49/19/19/19/19. Hull and all
persisted models stay exact;not earned recruitment. Repeated supply refills use
the source-bound original60518 method and own20 model water/food bytes only.
These are isolated testing support,not route/travel/resupply progress.
New actual verifier verify_hot_spring_crew_actual_v1656.py is AUTHORED,NOT RUN;
requires real relaxation2283/310 cases and normal return,using audit1654. No
predeclared cases JSON exists. Prior1646 is tied to old run;use1656 for1651.

## Resume rules

Read AGENTS,build_continuity_protocol,release_stack,relevant known_issues,
natural_dialogue_workflow and dialogue_delegation_protocol before author/build.
Do not spawn agents. sources/ is read-only. Executed producers/proofs frozen;
correct with explicit successors. Mutable ledger/docs/registry may be updated.
Python C:/Python314/python.exe;PYTHONUTF8=1;PYTHONPATH=.;.deps.
out and work/analysis junction to E;archive lexical paths,never resolve junctions.
Retain all generated ROMs;unsigned retention script remains policy-blocked;do not
bypass execution policy. No commit/push or promotion newly authorized this turn.
Before a new hot-spring run,verify all jobs above are terminal. A new runner may
cold-boot an ordinary battery save and replay a documented prefix;never restore a
savestate or restart merely because an observation timed out. The current runner
has a100000-frame ceiling;plan any longer successor explicitly. Do not repeat
random attempts indefinitely at the expense of the pending11's native/release work.
The broad goal remains active;this checkpoint neither completes nor pauses it.
'''
    Path('docs/editorial_handoff_current.md').write_text(note, encoding='utf-8')
    receipt = ROOT / 'checkpoint_receipt.json'
    ledger['research_checkpoints'].append({'id': 'V1658-source-review-and-terminal-test-checkpoint', 'proof': str(receipt),
                                           'source_prose_reviews_added': 0, 'completed_entries_added': 0, 'full_goal_complete': False})
    save('translations/editorial_review_current_v1.json', ledger)
    save(receipt, {'previous_goal_turn_classification': 'no editorial deliverable progress;answered user thread question',
                   'this_goal_turn_classification': 'progress:eleven clean-source prose reviews,new original event evidence and fully audited terminal tests',
                   'completed': 1350, 'revised': 1009, 'retained': 341, 'source_prose_reviewed': 1519, 'reviewed_incomplete_COMMON': 169,
                   'candidate': release['candidate'], 'candidate_sha256': release['candidate_sha256'], 'patch': release['patch'], 'patch_sha256': release['patch_sha256'],
                   'new11_not_integrated': True, 'hot_spring_optional_relaxation_and310_still_pending': True,
                   'terminal95860_normal_Sea_View_actually_viewed': True, 'terminal_proof': str(terminal), 'terminal_proof_sha256': sha(terminal.read_bytes()),
                   'all_current_processes_terminal': True, 'no_full_route_or_hardware_verification': True,
                   'full_goal_active_not_complete_or_paused': True, 'producer_sha256': sha(Path(__file__).read_bytes())})
    selected = [Path('docs/editorial_handoff_current.md'), Path('docs/search_reports_v1653_source_review.md'),
                Path('translations/editorial_review_current_v1.json'), Path('translations/search_reports_editorial_manuscript_v1.json'),
                terminal, Path('work/analysis/hot_spring_resilient_terminal_v1650a/terminal53178_preservation.json'),
                Path('work/analysis/hot_spring_crew_fixture_v1650/ten_byte_crew_refill_preflight.json'),
                Path('work/analysis/hot_spring_notice_release_v1636/registered_release_verification.json')]
    selected += list(Path('work/analysis/search_reports_source_v1653').glob('*.json')) + list(ROOT.glob('*.json'))
    ARCHIVE.mkdir(parents=True)
    copied = []
    for path in selected:
        relative = path.absolute().relative_to(Path.cwd().absolute())
        target = ARCHIVE / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        copy2(path, target)
        assert sha(path.read_bytes()) == sha(target.read_bytes())
        copied.append({'source': str(path), 'archived': str(target), 'sha256': sha(path.read_bytes())})
    save(ARCHIVE / 'archive_receipt.json', {'files': copied, 'ROM_patch_and_all_captures_retained_at_original_E_paths': True,
                                          'no_ROMS_deleted': True, 'full_goal_complete': False})
    print(f'V1658 checkpoint:11 new prose reviews,1350 complete/1519 reviewed/169 pending;296 replay PNGs exact;terminal95860 fully audited. Handoff updated;{len(copied)} records archived on E;full goal remains active.')
