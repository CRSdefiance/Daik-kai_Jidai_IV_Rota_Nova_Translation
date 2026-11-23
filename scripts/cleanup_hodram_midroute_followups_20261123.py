"""Archive the Hodram checkpoint and remove verified redundant files."""

from pathlib import Path
from shutil import copyfile

from scripts import cleanup_rafael_midroute_exchanges_20261122 as prior
from scripts import register_hodram_midroute_followups_20261123 as release
from scripts.source_locked_derivation_v5118 import checked_text

base, stage, live = release.base, release.stage, release.live
DRIVE = release.ROOT / "drive_latest_build_receipt.json"
RECEIPT = release.ROOT / "checkpoint_cleanup.json"
QUEUE = stage.BATCH / "current_wrap_queue.json"
CHECKPOINT_DIR = stage.paired.OUTPUT.parent
all_reviews = "(" + ", ".join("current" + ".parent" * n + ".REVIEW" for n in range(22, -1, -1)) + ")"
refresh_source = checked_text(prior.refresh_source, {prior.all_reviews: all_reviews})
queue_scope = prior.queue_scope | dict(current=release, OUTPUT=QUEUE)
exec(compile(refresh_source, __file__ + "::current-wrap-queue", "exec"), queue_scope)

start = prior.cleanup_source.index('        if run == "0":')
end = prior.cleanup_source.index('        fixture = base.load(fixture_path)', start)
cleanup_source = checked_text(prior.cleanup_source, {
    'release_stack_with_rafael_midroute_exchanges.json': 'release_stack_with_hodram_midroute_followups.json',
    'for edition in (stage.BATCH, history / "first_native_preflight", history / "second_native_preflight"):':
        'for edition in (stage.BATCH, history / "first_staging", history / "second_preflight"):',
    prior.cleanup_source[start:end]:'''        if run == "route1":
            rom = live.route_rom(1)
            fixture_path = rom.with_name("fixture.json")
            digest_key, inverse_key = "fixture_sha256", "exact_candidate_inverse"
        else:
            _, rom, fixture_path = live.choice_paths(live.RUNS[run][0])
            digest_key, inverse_key = "rom_sha256", "exact_inverse"
''',
})
scope = prior.scope | globals()
exec(compile(cleanup_source, __file__ + "::checksum-bound-cleanup", "exec"), scope)


def handoff(result):
    drive, queue = map(base.load, (DRIVE, QUEUE))
    candidate = base.load(release.RELEASE)["candidate_sha256"]
    assert drive["sha256"] == queue["candidate_sha256"] == result["candidate_sha256"] == candidate
    for proof in (DRIVE, QUEUE, RECEIPT):
        copy = CHECKPOINT_DIR / proof.name
        if not copy.exists():
            copyfile(proof, copy)
        assert base.digest(copy) == base.digest(proof)
    open_wraps = sum("reviewed" not in row for row in queue["records"])
    queue_ref = (CHECKPOINT_DIR / QUEUE.name).as_posix()
    cleanup_ref = (CHECKPOINT_DIR / RECEIPT.name).as_posix()
    stub = f"# Current editorial checkpoint - 2026-11-23\n\n{release.CHECKPOINT} [Checkpoint]({release.DOC.name})\n\n"
    section = (stub + f"""Thirteen exchanges add 306 contextual decisions. Twenty-five revisions address 17 queued wraps and related issues, including the amber conversation and two tutorial panels. The ledger records 268 dialogue and modal retentions, eight choice captions and five style variants. Eighteen names and roles passed native getter checks. Focused gameplay verified 47 displays and eight original choice outcomes. The style variants were verified offline. Ordinary story activation and handheld testing remain open. [Exact review](../{release.REVIEW.as_posix()})

The sole .nds on Drive matches SHA-256 {candidate}. Cold boot and 17 targeted tests passed, and the clean-input patch reconstructs the ROM byte for byte. The registered ROM and manifest are in workspace storage. Cleanup removed {len(result['removed'])} redundant files and reclaimed {result['reclaimed_bytes']:,} bytes. [Latest testing build]({drive['url']}) · [Clean-input patch](../{release.PATCH.as_posix()}) · [Cleanup receipt](../{cleanup_ref})

The current scan has {open_wraps} open wrap leads. The focused footage also showed the existing break after “I tell” in the priest's B110 R0047 warning. Keep that wording in context when reflowing the speaker's warning. Continue the remaining story and shared-text review, including the 276 shared display leads and practical town and random-scene coverage. Keep the 27,700 historical credits, separate artwork work and older-record technical re-audit. [Current wrap queue](../{queue_ref})

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
    handoff(base.load(RECEIPT))
