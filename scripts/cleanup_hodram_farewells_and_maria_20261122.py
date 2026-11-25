"""Refresh the wrap queue and clear exact duplicate artifacts for the Hodram batch."""

from pathlib import Path
from shutil import copyfile

from scripts import cleanup_mosque_elysion_mikhail_20261122 as baseline
from scripts import cleanup_rafael_B84_training_20261122 as prior
from scripts import register_hodram_farewells_and_maria_20261122 as release
from scripts.source_locked_derivation_v5118 import checked_text


base, stage = release.base, release.stage
DRIVE = release.ROOT / "drive_latest_build_receipt.json"
RECEIPT = release.ROOT / "checkpoint_cleanup.json"
QUEUE = stage.BATCH / "current_wrap_queue.json"
CHECKPOINT_DIR = Path("translations/editorial_checkpoints/hodram_farewells_and_maria_20261122")
all_reviews = "(" + ", ".join("current" + ".parent" * i + ".REVIEW" for i in range(12, -1, -1)) + ")"
refresh_source = checked_text(prior.refresh_source, {prior.all_reviews: all_reviews})
queue_scope = prior.queue_scope | dict(current=release, OUTPUT=QUEUE)
exec(compile(refresh_source, __file__ + "::current-wrap-queue", "exec"), queue_scope)

old_source = baseline.cleanup_source
fixture_start = old_source.index('    fixture = base.load(')
fixture_end = old_source.index('    assert all(base.digest(p) == h for p, h in retained.items())')
trials_start = old_source.index("    history = stage.BATCH.parent")
trials_end = old_source.index("    removed = []", trials_start)
cleanup_source = checked_text(old_source, {
    "release_stack_with_mosque_elysion_mikhail.json": "release_stack_with_hodram_farewells_and_maria.json",
    old_source[fixture_start:fixture_end]:'''    pins = {Path(r["path"]).resolve() for r in base.load(Path("translations/rom_retention_pins.json"))}
    assert release.live.ROM.resolve() in pins and stage.ROM.resolve() not in pins
    native_report = base.load(release.live.REPORT)
    assert base.digest(release.live.REPORT)==focused["report_sha256"]
    retained[release.live.ROM] = native_report["ROM_sha256"]
    retained[release.live.REPORT] = focused["report_sha256"]
    capture_reports.append((release.live.REPORT, native_report["ROM_sha256"]))
    for hold in [*(o["capture"] for o in focused["observations"]),focused["return_frame"]]:
        retained[Path(hold["path"])] = hold["PNG_sha256"]
''',
    old_source[trials_start:trials_end]:'''    history = stage.BATCH.parent
    earlier = release.EARLIER_STAGE
    initial = base.load(earlier / stage.PROOF.name)
    assert base.digest(earlier / stage.ROM.name) == initial["candidate_sha256"]
    discard[earlier / stage.REBUILT.name] = initial["candidate_sha256"]
    for edition in (stage.BATCH, history, history / "corrected"):
        proof = base.load(edition / "native_preflight.json")
        for picture in proof["sheets"]:
            child = edition / Path(picture["path"]).name
            assert child.resolve().parent == edition.resolve()
            discard[child] = picture["sha256"]
    roots = stage.ROOT.resolve(), release.ROOT.resolve(), history.resolve()
''',
})
scope = baseline.scope | globals()
scope["workflow"] = release.parent.scope["workflow"]
exec(compile(cleanup_source, __file__ + "::checksum-bound-cleanup", "exec"), scope)


def handoff(result):
    drive, queue = map(base.load, (DRIVE, QUEUE))
    assert drive["sha256"] == queue["candidate_sha256"] == result["candidate_sha256"]
    CHECKPOINT_DIR.mkdir(parents=True, exist_ok=True)
    for evidence in (DRIVE, QUEUE, RECEIPT):
        archived = CHECKPOINT_DIR / evidence.name
        if not archived.exists():
            copyfile(evidence, archived)
        assert base.digest(evidence) == base.digest(archived)
    open_wraps = sum("reviewed" not in row for row in queue["records"])
    manuscript = Path("scripts/hodram_sera_nagarpur_and_kuhn_20261122.md")
    section = f"""# Current editorial checkpoint - 2026-11-22

{release.CHECKPOINT} [Checkpoint]({release.DOC.name})

The batch records 103 source comparisons with 16 prose revisions and 87 individual retentions. Forty-four of the earlier Hodram differences are now reconciled. Exact checks covered 17 revised layout variants, including the default and maximum display width for Camille's thanks. Focused cold boots verified 19 panels and nameplates and the return to port. Original scene triggers and handheld display remain unvisited in this batch. [Exact coverage ledger](../{release.REVIEW.as_posix()})

The sole .nds on Drive matches SHA-256 {drive['sha256']}. Its patch reconstructs the exact ROM from the clean input. Startup and 17 focused regressions passed. Cleanup removed {len(result['removed'])} redundant files and reclaimed {result['reclaimed_bytes']:,} bytes. [Latest testing build]({drive['url']}) · [Patch](../{release.PATCH.as_posix()}) · [Cleanup receipt](../{(CHECKPOINT_DIR / RECEIPT.name).as_posix()})

The scan has {open_wraps} wrap leads awaiting a current decision. The remaining 46 differences in B61–B70 belong to six scenes. A 108-line contextual manuscript covers all six, with integration still pending. Keep subsequent route, tutorial, shared-dialogue and identity work in scope, with the 276 display leads and 27,700 historical credits preserved. [Next manuscript](../{manuscript.as_posix()}) · [Current wrap queue](../{(CHECKPOINT_DIR / QUEUE.name).as_posix()})

""".encode("utf-8")
    for name in ("editorial_handoff_current.md", "translation_progress.md"):
        path = release.DOC.with_name(name)
        installed = path.read_bytes()
        if not installed.startswith(section):
            base.replace_checked(path, section + installed)


if __name__ == "__main__":
    if not QUEUE.exists():
        queue_scope["main"]()
    if not RECEIPT.exists():
        scope["cleanup"]()
    handoff(base.load(RECEIPT))
