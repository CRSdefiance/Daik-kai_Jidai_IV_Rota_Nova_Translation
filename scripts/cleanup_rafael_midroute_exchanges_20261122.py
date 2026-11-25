"""Archive Rafael's testing checkpoint and clear verified redundant files."""

from pathlib import Path
from shutil import copyfile

from scripts import cleanup_hodram_early_and_midroute_wraps_20261122 as prior
from scripts import register_rafael_midroute_exchanges_20261122 as release
from scripts.source_locked_derivation_v5118 import checked_text

base, stage, live = release.base, release.stage, release.live
DRIVE = release.ROOT / "drive_latest_build_receipt.json"
RECEIPT = release.ROOT / "checkpoint_cleanup.json"
QUEUE = stage.BATCH / "current_wrap_queue.json"
CHECKPOINT_DIR = stage.paired.OUTPUT.parent
all_reviews = "(" + ", ".join("current" + ".parent" * n + ".REVIEW" for n in range(21, -1, -1)) + ")"
refresh_source = checked_text(prior.refresh_source, {prior.all_reviews: all_reviews})
queue_scope = prior.queue_scope | dict(current=release, OUTPUT=QUEUE)
exec(compile(refresh_source, __file__ + "::current-wrap-queue", "exec"), queue_scope)

fixture_start = prior.cleanup_source.index("        if run == \"route1\":")
fixture_end = prior.cleanup_source.index("        fixture = base.load(fixture_path)", fixture_start)
draft_start = prior.cleanup_source.index("    draft_root = history / \"release\" / \"staged\"")
draft_end = prior.cleanup_source.index("    roots =", draft_start)
cleanup_source = checked_text(prior.cleanup_source, {
    'release_stack_with_hodram_early_and_midroute_wraps.json':
        'release_stack_with_rafael_midroute_exchanges.json',
    prior.cleanup_source[fixture_start:fixture_end]:'''        if run == "0":
            fixture_path = live.excerpt_scope["receipt"](0)
            rom = Path(base.load(fixture_path)["rom"])
        else:
            _, rom, fixture_path = live.choice_paths(live.RUNS[run][0])
        digest_key, inverse_key = "rom_sha256", "exact_inverse"
''',
    'for edition in (stage.BATCH, history / "preflight", history / "release"):':
        'for edition in (stage.BATCH, history / "first_native_preflight", history / "second_native_preflight"):',
    prior.cleanup_source[draft_start:draft_end]: "",
})
scope = prior.scope | globals()
exec(compile(cleanup_source, __file__ + "::checksum-bound-cleanup", "exec"), scope)


def handoff(result):
    drive, queue = map(base.load, (DRIVE, QUEUE))
    candidate = base.load(release.RELEASE)["candidate_sha256"]
    assert drive["sha256"] == queue["candidate_sha256"] == result["candidate_sha256"] == candidate
    for proof in (DRIVE, QUEUE, RECEIPT):
        archive = CHECKPOINT_DIR / proof.name
        if not archive.exists():
            copyfile(proof, archive)
        assert base.digest(archive) == base.digest(proof)
    open_wraps = sum("reviewed" not in row for row in queue["records"])
    queue_ref = (CHECKPOINT_DIR / QUEUE.name).as_posix()
    cleanup_ref = (CHECKPOINT_DIR / RECEIPT.name).as_posix()
    next_packet = CHECKPOINT_DIR.with_name("hodram_midroute_followups_20261123") / "paired_source.json"
    followup = ""
    if next_packet.exists():
        assert base.load(next_packet)["candidate_sha256"] == candidate
        followup = (
            f" · [Next Hodram packet, 306 texts and 17 wrap leads](../{next_packet.as_posix()})"
            "\n\nThe release output drive has about 81 MB free. Use workspace storage for the next "
            "registered ROM and manifest if the existing output location still lacks room. "
            "Keep earlier registered paths and unique ROMs available."
        )
    old_stub = f"# Current editorial checkpoint - 2026-11-22\n\n{release.CHECKPOINT} [Checkpoint]({release.DOC.name})\n\n"
    stub = old_stub.replace("2026-11-22", "2026-11-23")
    section = (stub + f"""Fourteen complete exchanges add 280 decisions. Thirty passages changed, and one Colosseum award panel was reflowed with its wording intact. The batch addresses 21 flagged wraps. The ledger records 244 prose and panel retentions, five choice labels, and 15 reviewed names and roles. Native checks passed for 32 progressive display cases and all 17 modal panels. Focused gameplay verified 50 displays and all five original menu outcomes. Ordinary activation of these story scenes and handheld verification remain open. [Exact review](../{release.REVIEW.as_posix()})

The sole .nds on Drive matches SHA-256 {candidate}. Cold boot and 17 targeted tests passed, and the clean-input patch reconstructs the ROM byte for byte. Cleanup removed {len(result['removed'])} redundant files and reclaimed {result['reclaimed_bytes']:,} bytes. [Latest testing build]({drive['url']}) · [Clean-input patch](../{release.PATCH.as_posix()}) · [Cleanup receipt](../{cleanup_ref})

The current scan has {open_wraps} wrap leads awaiting decisions. Continue the remaining Hodram and Rafael exchanges, the other storylines, ordinary town and random scenes, and shared labels and prose. Preserve the 276 shared display leads, 27,700 historical credits, the separate artwork work, and the later older-record technical re-audit. [Current wrap queue](../{queue_ref}){followup}

""").encode("utf-8")
    for name in ("editorial_handoff_current.md", "translation_progress.md"):
        path = release.DOC.with_name(name)
        old = path.read_bytes()
        if not old.startswith(section):
            if old.startswith(old_stub.encode()):
                remainder = old.removeprefix(old_stub.encode())
            else:
                prefix = section.split(b"\n\n", 5)[:5]
                former = b"\n\n".join(prefix)
                assert old.startswith(former)
                section_end = old.index(b"\n\n", len(former))
                remainder = old[section_end + 2:]
            base.replace_checked(path, section + remainder)


if __name__ == "__main__":
    if not QUEUE.exists():
        queue_scope["main"]()
    if not RECEIPT.exists():
        scope["cleanup"]()
    handoff(base.load(RECEIPT))
