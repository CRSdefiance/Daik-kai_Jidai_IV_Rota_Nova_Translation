"""Refresh the wrap queue and remove checksum-verified duplicate build artifacts."""

from pathlib import Path
from shutil import copyfile

from scripts import cleanup_hodram_midroute_followups_20261123 as prior
from scripts import register_hodram_recruitment_and_sails_20261123 as release
from scripts.source_locked_derivation_v5118 import checked_text

base, stage, live = release.base, release.stage, release.live
DRIVE = release.ROOT / "drive_latest_build_receipt.json"
RECEIPT = release.ROOT / "checkpoint_cleanup.json"
QUEUE = stage.BATCH / "current_wrap_queue.json"
CHECKPOINT_DIR = Path("translations/editorial_checkpoints/hodram_recruitment_and_sails_20261123")
all_reviews = "(" + ", ".join("current" + ".parent" * n + ".REVIEW" for n in range(23, -1, -1)) + ")"
refresh = checked_text(prior.refresh_source, {prior.all_reviews: all_reviews})
queue_scope = prior.queue_scope | dict(current=release, OUTPUT=QUEUE)
exec(compile(refresh, __file__ + "::current-wrap-queue", "exec"), queue_scope)

start = prior.cleanup_source.index("    history = stage.BATCH.parent")
end = prior.cleanup_source.index("    roots =", start)
cleanup_source = checked_text(prior.cleanup_source, {
    "release_stack_with_hodram_midroute_followups.json": "release_stack_with_hodram_recruitment_and_sails.json",
    '    choices = [case["capture"] for choice in focused["original_menu_choices"] for case in choice["observations"]]':
        '    ordinary = focused["ordinary_story_evidence"]\n'
        '    report = live.report("istanbul")\n'
        '    retained[report] = ordinary["capture_sha256"]\n'
        '    capture_reports.append((report, candidate))\n'
        '    for hold in [*(row["capture"] for row in focused["ordinary_story_observations"]), ordinary["exit"]]:\n'
        '        retained[Path(hold["path"])] = hold["PNG_sha256"]\n'
        '    choices = [case["capture"] for choice in focused["original_menu_choices"] for case in choice["observations"]]',
    prior.cleanup_source[start:end]:'''    history = stage.BATCH.parent
    for edition in (stage.BATCH, history):
        proof = base.load(edition / "native_preflight.json")
        for picture in proof["sheets"]:
            child = Path(picture["path"])
            if child.resolve().parent == edition.resolve():
                discard[child] = picture["sha256"]
''',
})
scope = prior.scope | globals()
exec(compile(cleanup_source, __file__ + "::checksum-bound-cleanup", "exec"), scope)


def handoff():
    drive, queue, result = map(base.load, (DRIVE, QUEUE, RECEIPT))
    candidate = base.load(release.RELEASE)["candidate_sha256"]
    assert drive["sha256"] == queue["candidate_sha256"] == result["candidate_sha256"] == candidate
    CHECKPOINT_DIR.mkdir(exist_ok=True)
    for proof in (DRIVE, QUEUE, RECEIPT):
        copy = CHECKPOINT_DIR / proof.name
        if not copy.exists():
            copyfile(proof, copy)
        assert base.digest(copy) == base.digest(proof)
    open_wraps = sum("reviewed" not in row for row in queue["records"])
    stub = f"# Current editorial checkpoint - 2026-11-23\n\n{release.CHECKPOINT} [Checkpoint]({release.DOC.name})\n\n"
    section = (stub + f"""Six complete exchanges add 196 contextual decisions. Eighteen revisions address recruitment, the priest's warning and the sail lesson. The ledger records 176 speech and panel retentions, two choice captions and 19 verified names and roles. Native checks covered 19 changed display cases and four original crowd panels. Ordinary Istanbul gameplay verified nine Angelo panels and the return to port. Focused tests verified 18 holds and both sail-lesson choices. Julio's optional line has offline coverage. [Exact review](../{release.REVIEW.as_posix()})

The sole .nds on Drive matches SHA-256 {candidate}. The cold boot, 17 focused tests and exact clean-input reconstruction passed. Cleanup removed {len(result['removed'])} redundant files and reclaimed {result['reclaimed_bytes']:,} bytes. [Latest testing build]({drive["url"]}) · [Clean-input patch](../{release.PATCH.as_posix()}) · [Cleanup receipt](../{(CHECKPOINT_DIR / RECEIPT.name).as_posix()})

The current scan has {open_wraps} open wrap leads. Continue the remaining contextual review and town or random gameplay coverage, including the 276 shared display leads. Preserve the 27,700 historical credits, the separate artwork work and the later older-record technical re-audit. [Current wrap queue](../{(CHECKPOINT_DIR / QUEUE.name).as_posix()})

""").encode("utf-8")
    for name in ("editorial_handoff_current.md", "translation_progress.md"):
        path = release.DOC.with_name(name)
        content = path.read_bytes()
        if not content.startswith(section):
            assert content.startswith(stub.encode())
            base.replace_checked(path, section + content.removeprefix(stub.encode()))


if __name__ == "__main__":
    if not QUEUE.exists():
        queue_scope["main"]()
    if not RECEIPT.exists():
        scope["cleanup"]()
    handoff()
