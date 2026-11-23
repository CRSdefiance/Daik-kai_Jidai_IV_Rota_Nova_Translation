"""Archive Rafael's checkpoint and remove checksum-verified duplicates."""

from pathlib import Path
from shutil import copyfile

from scripts import cleanup_hodram_and_lil_followups_20261122 as prior
from scripts import register_rafael_charlotte_and_maria_20261122 as release
from scripts.source_locked_derivation_v5118 import checked_text


base, stage, live = release.base, release.stage, release.live
DRIVE = release.ROOT / "drive_latest_build_receipt.json"
RECEIPT = release.ROOT / "checkpoint_cleanup.json"
QUEUE = stage.BATCH / "current_wrap_queue.json"
CHECKPOINT_DIR = stage.paired.OUTPUT.parent
all_reviews = "(" + ", ".join("current" + ".parent" * n + ".REVIEW" for n in range(18, -1, -1)) + ")"
refresh_source = checked_text(prior.refresh_source, {prior.all_reviews: all_reviews})
queue_scope = prior.queue_scope | dict(current=release, OUTPUT=QUEUE)
exec(compile(refresh_source, __file__ + "::current-wrap-queue", "exec"), queue_scope)

start = prior.cleanup_source.index("    for run in release.RUNS:")
end = prior.cleanup_source.index("    assert all(base.digest(p) == h for p, h in retained.items())")
cleanup_source = checked_text(prior.cleanup_source, {
    "release_stack_with_hodram_and_lil_followups.json": "release_stack_with_rafael_charlotte_and_maria.json",
    prior.cleanup_source[start:end]:'''    fixture = base.load(live.scope["receipt"](0))
    rom = Path(fixture["rom"])
    assert fixture["candidate_sha256"] == candidate and fixture["exact_inverse"] and rom.resolve() in pins
    retained[rom] = fixture["rom_sha256"]
    report = live.report("0")
    retained[report] = focused["report_sha256"]["0"]
    capture_reports.append((report, fixture["rom_sha256"]))
    for hold in [*(row["capture"] for row in focused["observations"]), *focused["return_frames"].values()]:
        retained[Path(hold["path"])] = hold["PNG_sha256"]
''',
    "    discard[earlier_duplicate] = earlier_candidate\n": "",
    'for edition in (stage.BATCH, history, history / "final"):':
        'for edition in (stage.BATCH, history / "staging"):',
})
scope = prior.scope | globals()
exec(compile(cleanup_source, __file__ + "::checksum-bound-cleanup", "exec"), scope)


def handoff(result):
    drive, queue = map(base.load, (DRIVE, QUEUE))
    candidate = base.load(release.RELEASE)["candidate_sha256"]
    assert candidate == drive["sha256"] == queue["candidate_sha256"] == result["candidate_sha256"]
    for evidence in (DRIVE, QUEUE, RECEIPT):
        archived = CHECKPOINT_DIR / evidence.name
        if not archived.exists():
            copyfile(evidence, archived)
        assert base.digest(evidence) == base.digest(archived)
    open_wraps = sum("reviewed" not in row for row in queue["records"])
    queue_ref = (CHECKPOINT_DIR / QUEUE.name).as_posix()
    cleanup_ref = (CHECKPOINT_DIR / RECEIPT.name).as_posix()
    stub = f"# Current editorial checkpoint - 2026-11-22\n\n{release.CHECKPOINT} [Checkpoint]({release.DOC.name})\n\n"
    section = (stub + f"""Four complete exchanges add 134 decisions. Twelve passages changed and 122 have individual reasons for retention. All 12 revised pages passed exact glyph and wrap checks. Focused emulator gameplay verified 17 speech holds, including two default-name substitutions and the return to port. Natural scene activation and handheld display remain unvisited for this batch. [Exact review](../{release.REVIEW.as_posix()})

Ordinary saved gameplay verified twelve shop and tavern panels across Ceuta and Lisbon. The sailor's question tag stays on the first line at both ports. [Town dialogue evidence](../{(release.VERIFY / release.ORDINARY.name).as_posix()})

The sole .nds on Drive matches SHA-256 {candidate}. Startup and 17 targeted tests passed, and the clean-input patch reconstructs the ROM byte for byte. Cleanup removed {len(result['removed'])} redundant files and reclaimed {result['reclaimed_bytes']:,} bytes. [Latest testing build]({drive['url']}) · [Clean-input patch](../{release.PATCH.as_posix()}) · [Cleanup receipt](../{cleanup_ref})

The current scan has {open_wraps} wrap leads awaiting a decision. The next Rafael packet covers six full exchanges in B74, B81, B83, B87, B90 and B97, with 224 texts, twelve wrap leads and four system panels. Continue the other storylines, ordinary town and random scenes, names and remaining player-facing prose. Preserve the 276 shared display leads, 27,700 historical credits, deferred artwork, and later older-record technical re-audit. [Current wrap queue](../{queue_ref}) · [Next Rafael packet](../translations/editorial_checkpoints/rafael_fleet_and_crew_exchanges_20261122/paired_source.json)

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
