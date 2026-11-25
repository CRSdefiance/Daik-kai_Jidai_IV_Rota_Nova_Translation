"""Archive the Hodram checkpoint and clear only verified duplicate artifacts."""

from pathlib import Path
from shutil import copyfile

from scripts import cleanup_rafael_fleet_and_crew_exchanges_20261122 as prior
from scripts import register_hodram_early_and_midroute_wraps_20261122 as release
from scripts.source_locked_derivation_v5118 import checked_text


base, stage, live = release.base, release.stage, release.live
DRIVE = release.ROOT / "drive_latest_build_receipt.json"
RECEIPT = release.ROOT / "checkpoint_cleanup.json"
QUEUE = stage.BATCH / "current_wrap_queue.json"
CHECKPOINT_DIR = stage.paired.OUTPUT.parent
all_reviews = "(" + ", ".join("current" + ".parent" * n + ".REVIEW" for n in range(20, -1, -1)) + ")"
refresh_source = checked_text(prior.refresh_source, {prior.all_reviews: all_reviews})
queue_scope = prior.queue_scope | dict(current=release, OUTPUT=QUEUE)
exec(compile(refresh_source, __file__ + "::current-wrap-queue", "exec"), queue_scope)

start = prior.cleanup_source.index('    fixture = base.load(live.scope["receipt"](0))')
end = prior.cleanup_source.index("    assert all(base.digest(p) == h for p, h in retained.items())")
cleanup_source = checked_text(prior.cleanup_source, {
    "release_stack_with_rafael_fleet_and_crew_exchanges.json": "release_stack_with_hodram_early_and_midroute_wraps.json",
    'for edition in (stage.BATCH, history / "preflight"):':
        'for edition in (stage.BATCH, history / "preflight", history / "release"):',
    '    roots = stage.ROOT.resolve(), release.ROOT.resolve(), history.resolve(), release.WORK.resolve()':
        '    draft_root = history / "release" / "staged"\n'
        '    draft_candidate = base.load(draft_root / stage.PROOF.name)["candidate_sha256"]\n'
        '    draft_rom = draft_root / stage.ROM.name\n'
        '    assert draft_rom.resolve() in pins and base.digest(draft_rom) == draft_candidate\n'
        '    discard[draft_root / stage.REBUILT.name] = draft_candidate\n'
        '    roots = stage.ROOT.resolve(), release.ROOT.resolve(), history.resolve(), release.WORK.resolve()',
    prior.cleanup_source[start:end]:'''    for run in release.RUNS:
        if run == "route1":
            rom = live.route_rom(1)
            fixture_path = rom.with_name("fixture.json")
            digest_key, inverse_key = "fixture_sha256", "exact_candidate_inverse"
        else:
            _, rom, fixture_path = live.choice_paths(live.run_block(run))
            digest_key, inverse_key = "rom_sha256", "exact_inverse"
        fixture = base.load(fixture_path)
        assert fixture["candidate_sha256"] == candidate and fixture[inverse_key] and rom.resolve() in pins
        retained[rom] = fixture[digest_key]
        report = live.report(run)
        retained[report] = focused["report_sha256"][run]
        capture_reports.append((report, fixture[digest_key]))
    choices = [case["capture"] for choice in focused["original_menu_choices"] for case in choice["observations"]]
    for hold in [*(row["capture"] for row in focused["observations"]), *focused["return_frames"].values(), *choices]:
        retained[Path(hold["path"])] = hold["PNG_sha256"]
''',
})
scope = prior.scope | globals()
exec(compile(cleanup_source, __file__ + "::checksum-bound-cleanup", "exec"), scope)


def handoff(result):
    drive, queue = map(base.load, (DRIVE, QUEUE))
    candidate = base.load(release.RELEASE)["candidate_sha256"]
    assert drive["sha256"] == queue["candidate_sha256"] == result["candidate_sha256"] == candidate
    for evidence in (DRIVE, QUEUE, RECEIPT):
        archived = CHECKPOINT_DIR / evidence.name
        if not archived.exists():
            copyfile(evidence, archived)
        assert base.digest(evidence) == base.digest(archived)
    open_wraps = sum("reviewed" not in row for row in queue["records"])
    queue_ref = (CHECKPOINT_DIR / QUEUE.name).as_posix()
    cleanup_ref = (CHECKPOINT_DIR / RECEIPT.name).as_posix()
    stub = f"# Current editorial checkpoint - 2026-11-22\n\n{release.CHECKPOINT} [Checkpoint]({release.DOC.name})\n\n"
    section = (stub + f"""Eighteen complete exchanges add 282 decisions. Twenty-four passages changed to address all flagged wraps, and 258 texts have individual retention reasons, including four choice labels. All 24 revised pages and 20 retained system panels passed native checks, with two extra maximum-name cases. Focused gameplay verified 36 holds, both original outcomes in each menu and the return to port. Natural story activation and handheld verification remain open for this batch. [Exact review](../{release.REVIEW.as_posix()})

The sole .nds on Drive matches SHA-256 {candidate}. Startup and 17 targeted tests passed, and the clean-input patch reconstructs the ROM byte for byte. Cleanup removed {len(result['removed'])} redundant files and reclaimed {result['reclaimed_bytes']:,} bytes. [Latest testing build]({drive['url']}) · [Clean-input patch](../{release.PATCH.as_posix()}) · [Cleanup receipt](../{cleanup_ref})

The current scan has {open_wraps} wrap leads awaiting a decision. Continue the remaining Hodram and Rafael scenes, the other storylines, ordinary town and random scenes, names, and remaining player-facing prose. Preserve the 276 shared display leads, 27,700 historical credits, deferred artwork, and later older-record technical re-audit. [Current wrap queue](../{queue_ref}) · [Next Rafael packet, 280 texts and 21 wrap leads](../translations/editorial_checkpoints/rafael_midroute_exchanges_20261122/paired_source.json) · [Working review of the first six exchanges](../translations/editorial_checkpoints/rafael_midroute_exchanges_20261122/working_review.md)

""").encode("utf-8")
    for name in ("editorial_handoff_current.md", "translation_progress.md"):
        path = release.DOC.with_name(name)
        body = path.read_bytes()
        if not body.startswith(section):
            base.replace_checked(path, section + body.removeprefix(stub.encode("utf-8")))


if __name__ == "__main__":
    if not QUEUE.exists():
        queue_scope["main"]()
    if not RECEIPT.exists():
        scope["cleanup"]()
    handoff(base.load(RECEIPT))
