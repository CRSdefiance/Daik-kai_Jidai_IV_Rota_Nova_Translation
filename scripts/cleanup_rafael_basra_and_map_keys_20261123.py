"""Refresh the current wrap queue and archive the verified Basra testing checkpoint."""

from pathlib import Path
from shutil import copyfile

from scripts import cleanup_hodram_recruitment_and_sails_20261123 as prior
from scripts import cleanup_rafael_midroute_exchanges_20261122 as fixture_cleanup
from scripts import register_rafael_basra_and_map_keys_20261123 as release
from scripts.source_locked_derivation_v5118 import checked_text

base, stage, live = release.base, release.stage, release.live
DRIVE = release.ROOT / "drive_latest_build_receipt.json"
RECEIPT = release.ROOT / "checkpoint_cleanup.json"
QUEUE = stage.BATCH / "current_wrap_queue.json"
CHECKPOINT_DIR = stage.paired.OUTPUT.parent
all_reviews = "(" + ", ".join("current" + ".parent" * n + ".REVIEW" for n in range(24, -1, -1)) + ")"
refresh = checked_text(prior.refresh, {prior.all_reviews: all_reviews})
queue_scope = prior.queue_scope | dict(current=release, OUTPUT=QUEUE)
exec(compile(refresh, __file__ + "::current-wrap-queue", "exec"), queue_scope)

cleanup_source = checked_text(fixture_cleanup.cleanup_source, {
    "release_stack_with_rafael_midroute_exchanges.json": "release_stack_with_rafael_basra_and_map_keys.json",
    '    history = stage.BATCH.parent': '    history = stage.BATCH',
    'for edition in (stage.BATCH, history / "first_native_preflight", history / "second_native_preflight"):':
        'for edition in (stage.BATCH,):',
    '    assert all(base.digest(p) == h for p, h in retained.items())\n    keep =':
        '    prototype_root = stage.BATCH.parent / "staged"\n'
        '    prototype = prototype_root / stage.ROM.name\n'
        '    old = base.load(prototype_root / stage.PROOF.name)\n'
        '    assert old["whole_parent_inverse"] and prototype.resolve() in pins\n'
        '    retained[prototype] = old["candidate_sha256"]\n'
        '    assert all(base.digest(p) == h for p, h in retained.items())\n    keep =',
    '    discard = {stage.REBUILT: candidate, stage.ROM: candidate, stage.PATCH: patch}':
        '    discard = {stage.REBUILT: candidate, stage.ROM: candidate, stage.PATCH: patch,\n'
        '               prototype_root / stage.REBUILT.name: old["candidate_sha256"]}',
    'history.resolve(), release.WORK.resolve()':
        'history.resolve(), prototype_root.resolve(), release.WORK.resolve()',
})
scope = fixture_cleanup.scope | globals()
exec(compile(cleanup_source, __file__ + "::checksum-bound-cleanup", "exec"), scope)


def handoff():
    drive, queue, result = map(base.load, (DRIVE, QUEUE, RECEIPT))
    candidate = base.load(release.RELEASE)["candidate_sha256"]
    assert drive["sha256"] == queue["candidate_sha256"] == result["candidate_sha256"] == candidate
    for proof in (DRIVE, QUEUE, RECEIPT):
        archive = CHECKPOINT_DIR / proof.name
        if not archive.exists():
            copyfile(proof, archive)
        assert base.digest(archive) == base.digest(proof)
    open_wraps = sum("reviewed" not in row for row in queue["records"])
    stub = f"# Current editorial checkpoint - 2026-11-23\n\n{release.CHECKPOINT} [Checkpoint]({release.DOC.name})\n\n"
    section = (stub + f"""Ten exchanges add 213 contextual decisions. Fifteen revisions address fourteen queued wraps, Escante's incomplete homeland reference and the barkeep's company-name punctuation. The ledger records 192 dialogue and modal panel retentions, six choice captions and twelve names and roles. Native checks covered seventeen revised display cases and two market-share notices. Focused gameplay verified 28 holds and all six original menu outcomes. Ordinary story activation and handheld testing remain open for these scenes. The five original Uddin actor controls have byte-exact references at their new offsets. [Exact review](../{release.REVIEW.as_posix()})

The sole .nds on Drive matches SHA-256 {candidate}. Cold boot, seventeen focused tests, and exact clean-input reconstruction passed. Cleanup removed {len(result['removed'])} redundant files and reclaimed {result['reclaimed_bytes']:,} bytes. [Latest testing build]({drive["url"]}) · [Clean-input patch](../{release.PATCH.as_posix()}) · [Cleanup receipt](../{(CHECKPOINT_DIR / RECEIPT.name).as_posix()})

The scan has {open_wraps} open wrap leads. Continue the contextual review, ordinary town and random gameplay samples, and the 276 shared display leads. Preserve the 27,700 historical credits, separate artwork work and later older-record technical re-audit. [Current wrap queue](../{(CHECKPOINT_DIR / QUEUE.name).as_posix()})

""").encode("utf-8")
    for name in ("editorial_handoff_current.md", "translation_progress.md"):
        path = release.DOC.with_name(name)
        old = path.read_bytes()
        if not old.startswith(section):
            assert old.startswith(stub.encode())
            base.replace_checked(path, section + old.removeprefix(stub.encode()))


if __name__ == "__main__":
    if not QUEUE.exists():
        queue_scope["main"]()
    if not RECEIPT.exists():
        scope["cleanup"]()
    handoff()
