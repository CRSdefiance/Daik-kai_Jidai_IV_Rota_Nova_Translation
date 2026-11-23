"""Refresh the current wrap queue and archive the Hodram reconciliation checkpoint."""

from pathlib import Path
from shutil import copyfile

from scripts import cleanup_hodram_farewells_and_maria_20261122 as prior
from scripts import register_hodram_sera_nagarpur_and_kuhn_20261122 as release
from scripts.source_locked_derivation_v5118 import checked_text


base, stage = release.base, release.stage
DRIVE = release.ROOT / "drive_latest_build_receipt.json"
RECEIPT = release.ROOT / "checkpoint_cleanup.json"
QUEUE = stage.BATCH / "current_wrap_queue.json"
CHECKPOINT_DIR = Path("translations/editorial_checkpoints/hodram_sera_nagarpur_and_kuhn_20261122")
all_reviews = "(" + ", ".join("current" + ".parent" * i + ".REVIEW" for i in range(13, -1, -1)) + ")"
refresh_source = checked_text(prior.refresh_source, {prior.all_reviews: all_reviews})
queue_scope = prior.queue_scope | dict(current=release, OUTPUT=QUEUE)
exec(compile(refresh_source, __file__ + "::current-wrap-queue", "exec"), queue_scope)

trials_start = prior.cleanup_source.index("    history = stage.BATCH.parent")
trials_end = prior.cleanup_source.index("    removed = []", trials_start)
cleanup_source = checked_text(prior.cleanup_source, {
    "release_stack_with_hodram_farewells_and_maria.json": "release_stack_with_hodram_sera_nagarpur_and_kuhn.json",
    prior.cleanup_source[trials_start:trials_end]:'''    history = stage.BATCH.parent
    for edition in (stage.BATCH, history):
        proof = base.load(edition / "native_preflight.json")
        for picture in proof["sheets"]:
            child = edition / Path(picture["path"]).name
            assert child.resolve().parent == edition.resolve()
            discard[child] = picture["sha256"]
    roots = stage.ROOT.resolve(), release.ROOT.resolve(), history.resolve()
''',
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
    section = f"""# Current editorial checkpoint - 2026-11-22

{release.CHECKPOINT} [Checkpoint]({release.DOC.name})

Six complete exchanges add 108 source decisions, eight prose revisions and 100 individually justified retentions. All 96 earlier Hodram B61–B70 differences now have a registered decision across three batches. Nine revised layouts passed exact glyph checks. A focused emulator replay verified 12 panels, their nameplates and the host's return. Natural activation and handheld display remain unvisited for this batch. [Exact review](../{release.REVIEW.as_posix()})

The sole .nds on Drive matches SHA-256 {candidate}. Its patch reconstructs the exact ROM from the clean input. Startup and 17 focused regressions passed. Cleanup removed {len(result['removed'])} redundant files and reclaimed {result['reclaimed_bytes']:,} bytes. [Latest testing build]({drive['url']}) · [Patch](../{release.PATCH.as_posix()}) · [Cleanup receipt](../{cleanup_ref})

The current scan has {open_wraps} wrap leads awaiting a source-based decision. Continue with Rafael's remaining early tutorial and Proof of Conquest dialogue, including the B47 and B48 wrap leads. Maria's B116 crew conversation has 26 source-bound decisions and two byte-verified pairs of system panels. Its eight prose proposals await native formatting and integration. Keep the shared town, random dialogue, speaker names and other player-facing prose in scope alongside the 276 shared display leads and 27,700 historical credits. [Current wrap queue](../{queue_ref}) · [Maria's crew conversation](../translations/editorial_checkpoints/maria_admiral_story_20261122/contextual_draft.json)

""".encode("utf-8")
    stub = f"# Current editorial checkpoint - 2026-11-22\n\n{release.CHECKPOINT} [Checkpoint]({release.DOC.name})\n\n".encode("utf-8")
    for name in ("editorial_handoff_current.md", "translation_progress.md"):
        path = release.DOC.with_name(name)
        body = path.read_bytes()
        if not body.startswith(section):
            base.replace_checked(path, section + body.removeprefix(stub))


if __name__ == "__main__":
    if not QUEUE.exists():
        queue_scope["main"]()
    if not RECEIPT.exists():
        scope["cleanup"]()
    handoff(base.load(RECEIPT))
