"""Refresh the wrap queue and remove verified duplicates from this checkpoint."""

from pathlib import Path
from shutil import copyfile

from scripts import cleanup_rafael_six_followup_exchanges_20261122 as prior
from scripts import register_hodram_and_lil_followups_20261122 as release
from scripts.source_locked_derivation_v5118 import checked_text


base, stage, live = release.base, release.stage, release.live
DRIVE = release.ROOT / "drive_latest_build_receipt.json"
RECEIPT = release.ROOT / "checkpoint_cleanup.json"
QUEUE = stage.BATCH / "current_wrap_queue.json"
CHECKPOINT_DIR = stage.paired.OUTPUT.parent
all_reviews = "(" + ", ".join("current" + ".parent" * n + ".REVIEW" for n in range(17, -1, -1)) + ")"
refresh_source = checked_text(prior.refresh_source, {prior.all_reviews: all_reviews})
queue_scope = prior.queue_scope | dict(current=release, OUTPUT=QUEUE)
exec(compile(refresh_source, __file__ + "::current-wrap-queue", "exec"), queue_scope)

start = prior.cleanup_source.index('    fixture = base.load(release.live.scope["receipt"](0))')
end = prior.cleanup_source.index("    assert all(base.digest(p) == h for p, h in retained.items())")
cleanup_source = checked_text(prior.cleanup_source, {
    "release_stack_with_rafael_six_followup_exchanges.json": "release_stack_with_hodram_and_lil_followups.json",
    "discard[release.ROOT / filename]": "discard[release.WORK / filename]",
    "roots = stage.ROOT.resolve(), release.ROOT.resolve(), history.resolve()":
        "roots = stage.ROOT.resolve(), release.ROOT.resolve(), history.resolve(), release.WORK.resolve()",
    prior.cleanup_source[start:end]:'''    for run in release.RUNS:
        if run in live.BRANCHES:
            rom, fixture_path = live.CHOICE_ROM, live.CHOICE_RECEIPT
            digest_field, inverse_field = "rom_sha256", "exact_inverse"
        else:
            rom = live.route_rom(int(run[-1]))
            fixture_path = rom.with_name("fixture.json")
            digest_field, inverse_field = "fixture_sha256", "exact_candidate_inverse"
        fixture = base.load(fixture_path)
        assert fixture["candidate_sha256"] == candidate and fixture[inverse_field] and rom.resolve() in pins
        retained[rom] = fixture[digest_field]
        report = live.report(run)
        retained[report] = focused["report_sha256"][run]
        capture_reports.append((report, fixture[digest_field]))
    menu_holds = (item["capture"] for branch in focused["original_menu_choices"] for item in branch["observations"])
    for hold in [*(row["capture"] for row in focused["observations"]), *focused["return_frames"].values(), *menu_holds]:
        retained[Path(hold["path"])] = hold["PNG_sha256"]
    earlier = stage.BATCH.parent / "staged"
    earlier_rom = earlier / stage.ROM.name
    earlier_duplicate = earlier / stage.REBUILT.name
    earlier_candidate = base.load(earlier / stage.PROOF.name)["candidate_sha256"]
    assert earlier_rom.resolve() in pins
    retained[earlier_rom] = earlier_candidate
''',
    "    history = stage.BATCH.parent\n    for edition in (stage.BATCH, history):":
        "    history = stage.BATCH.parent\n"
        "    discard[earlier_duplicate] = earlier_candidate\n"
        '    for edition in (stage.BATCH, history, history / "final"):',
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
    section = (stub + f"""Four complete exchanges add 288 speech and notice decisions and two choice decisions. Eighteen passages changed and 270 texts and both captions have individual retention reasons. All 18 revised pages passed complete glyph and layout checks. Focused emulator gameplay verified 30 holds, four original notices, both choice responses, and the host exits. The natural story triggers and handheld display remain unvisited. [Exact review](../{release.REVIEW.as_posix()})

The sole .nds on Drive matches SHA-256 {candidate}. Startup and 17 targeted tests passed, and the clean-input patch reconstructs the ROM byte for byte. Cleanup removed {len(result['removed'])} redundant files and reclaimed {result['reclaimed_bytes']:,} bytes. [Latest testing build]({drive['url']}) · [Clean-input patch](../{release.PATCH.as_posix()}) · [Cleanup receipt](../{cleanup_ref})

The current scan has {open_wraps} wrap leads awaiting a decision. The next Rafael packet binds 134 texts and eight wrap leads across the Charlotte exchange and his first East Asia scenes with Maria. Continue the other storylines, ordinary town and random scenes, and remaining player-facing prose. Preserve the 276 shared display leads, name and identity review, 27,700 historical credits, deferred artwork, and later older-record technical re-audit. [Current wrap queue](../{queue_ref}) · [Rafael paired source](../translations/editorial_checkpoints/rafael_charlotte_and_maria_20261122/paired_source.json)

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
