"""Refresh the wrap queue and remove verified duplicate assets for the joint batch."""

from pathlib import Path
from shutil import copyfile

from scripts import cleanup_hodram_sera_nagarpur_and_kuhn_20261122 as prior
from scripts import register_rafael_athens_and_maria_crew_20261122 as release
from scripts.source_locked_derivation_v5118 import checked_text


base, stage = release.base, release.stage
DRIVE = release.ROOT / "drive_latest_build_receipt.json"
RECEIPT = release.ROOT / "checkpoint_cleanup.json"
QUEUE = stage.BATCH / "current_wrap_queue.json"
CHECKPOINT_DIR = Path("translations/editorial_checkpoints/rafael_athens_and_maria_crew_20261122")
all_reviews = "(" + ", ".join("current" + ".parent" * i + ".REVIEW" for i in range(14, -1, -1)) + ")"
refresh_source = checked_text(prior.refresh_source, {prior.all_reviews: all_reviews})
queue_scope = prior.queue_scope | dict(current=release, OUTPUT=QUEUE)
exec(compile(refresh_source, __file__ + "::current-wrap-queue", "exec"), queue_scope)

fixtures_start = prior.cleanup_source.index('    pins = {Path(r["path"]).resolve()')
fixtures_end = prior.cleanup_source.index("    assert all(base.digest(p) == h for p, h in retained.items())")
cleanup_source = checked_text(prior.cleanup_source, {
    "release_stack_with_hodram_sera_nagarpur_and_kuhn.json": "release_stack_with_rafael_athens_and_maria_crew.json",
    prior.cleanup_source[fixtures_start:fixtures_end]:'''    pins = {Path(r["path"]).resolve() for r in base.load(Path("translations/rom_retention_pins.json"))}
    assert stage.ROM.resolve() not in pins
    for route in release.live.SAMPLE:
        fixture = base.load(release.live.receipt(route))
        assert fixture["candidate_sha256"] == candidate and fixture["exact_inverse"]
        rom = Path(fixture["rom"])
        assert rom.resolve() in pins
        retained[rom] = fixture["rom_sha256"]
        path = release.live.report_path(route)
        digest = focused["report_sha256"][str(route)]
        assert base.digest(path) == digest
        retained[path] = digest
        capture_reports.append((path, fixture["rom_sha256"]))
    for hold in [*(o["capture"] for o in focused["observations"]), *focused["return_frames"].values()]:
        retained[Path(hold["path"])] = hold["PNG_sha256"]
''',
    'for edition in (stage.BATCH, history):': '''trial = release.TRIAL.parent / stage.REBUILT.name
    assert base.digest(release.TRIAL) == base.digest(trial)
    discard[trial] = base.digest(release.TRIAL)
    for edition in (stage.BATCH, history, history / "final"):''',
})
scope = prior.scope | globals()
exec(compile(cleanup_source, __file__ + "::checksum-bound-cleanup", "exec"), scope)


def handoff(result):
    drive, queue = map(base.load, (DRIVE, QUEUE))
    candidate = base.load(release.RELEASE)["candidate_sha256"]
    assert drive["sha256"] == queue["candidate_sha256"] == result["candidate_sha256"] == candidate
    CHECKPOINT_DIR.mkdir(parents=True, exist_ok=True)
    for evidence in (DRIVE, QUEUE, RECEIPT):
        archived = CHECKPOINT_DIR / evidence.name
        if not archived.exists():
            copyfile(evidence, archived)
        assert base.digest(evidence) == base.digest(archived)
    open_wraps = sum("reviewed" not in row for row in queue["records"])
    queue_ref = (CHECKPOINT_DIR / QUEUE.name).as_posix()
    cleanup_ref = (CHECKPOINT_DIR / RECEIPT.name).as_posix()
    stub = f"# Current editorial checkpoint - 2026-11-22\n\n{release.CHECKPOINT} [Checkpoint]({release.DOC.name})\n\n"
    section = (stub + f"""Three complete exchanges add 132 contextual decisions, including 18 wording revisions, one wrap-only revision and 113 individual retentions. Revised phrases make fuller use of the line width. All 21 revised layout variants passed exact glyph checks. Focused controller replays verified 29 panels, including ten native modal pages and both of Maria's original two-page sequences. Natural story activation and handheld display remain unvisited for this batch. [Exact current review](../{release.REVIEW.as_posix()})

The sole .nds on Drive matches SHA-256 {candidate}. Its clean-input patch reconstructs it byte for byte. Startup and 17 focused regressions passed. Cleanup removed {len(result['removed'])} redundant files and reclaimed {result['reclaimed_bytes']:,} bytes. [Latest testing build]({drive['url']}) · [Patch](../{release.PATCH.as_posix()}) · [Cleanup receipt](../{cleanup_ref})

The scan has {open_wraps} wrap leads awaiting a current decision. Rafael's complete B41 Proof of Conquest draft has 27 decisions, including six proposals. The next source packet binds both exchanges, including all 115 B44 financing texts, both captions in the original choice object, and four wrap leads. Continue with both exchanges and the remaining four-route, town, shared and random dialogue. Keep the 276 shared display leads, identity and name review, 27,700 historical credits, graphics artwork deferral and later older-record technical re-audit. [Current wrap queue](../{queue_ref}) · [Rafael's briefing draft](../scripts/rafael_proof_briefing_20261122.md) · [Exact source pairs](../translations/editorial_checkpoints/rafael_proof_and_financing_20261122/paired_source.json)

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
