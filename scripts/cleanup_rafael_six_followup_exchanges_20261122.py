"""Refresh the wrap queue and retain the evidence for Rafael's six exchanges."""

from pathlib import Path
from shutil import copyfile

from scripts import cleanup_rafael_proof_and_financing_20261122 as prior
from scripts import register_rafael_six_followup_exchanges_20261122 as release
from scripts.source_locked_derivation_v5118 import checked_text


base, stage = release.base, release.stage
DRIVE = release.ROOT / "drive_latest_build_receipt.json"
RECEIPT = release.ROOT / "checkpoint_cleanup.json"
QUEUE = stage.BATCH / "current_wrap_queue.json"
CHECKPOINT_DIR = Path("translations/editorial_checkpoints/rafael_six_followup_exchanges_20261122")
all_reviews = "(" + ", ".join("current" + ".parent" * i + ".REVIEW" for i in range(16, -1, -1)) + ")"
refresh_source = checked_text(prior.refresh_source, {prior.all_reviews: all_reviews})
queue_scope = prior.queue_scope | dict(current=release, OUTPUT=QUEUE)
exec(compile(refresh_source, __file__ + "::current-wrap-queue", "exec"), queue_scope)

start = prior.cleanup_source.index('    pins = {Path(r["path"]).resolve()')
end = prior.cleanup_source.index("    assert all(base.digest(p) == h for p, h in retained.items())")
attempt_start = prior.cleanup_source.index('    attempt = history / "registration_attempt_1"')
attempt_end = prior.cleanup_source.index("    for edition in (stage.BATCH, history):", attempt_start)
cleanup_source = checked_text(prior.cleanup_source, {
    "release_stack_with_rafael_proof_and_financing.json": "release_stack_with_rafael_six_followup_exchanges.json",
    prior.cleanup_source[start:end]:'''    pins = {Path(r["path"]).resolve() for r in base.load(Path("translations/rom_retention_pins.json"))}
    assert stage.ROM.resolve() not in pins
    fixture = base.load(release.live.scope["receipt"](0))
    rom = Path(fixture["rom"])
    assert fixture["candidate_sha256"] == candidate and fixture["exact_inverse"] and rom.resolve() in pins
    assert base.digest(release.REPORT) == focused["report_sha256"]["0"]
    retained[rom] = fixture["rom_sha256"]
    retained[release.REPORT] = focused["report_sha256"]["0"]
    capture_reports.append((release.REPORT, fixture["rom_sha256"]))
    for hold in [*(row["capture"] for row in focused["observations"]), *focused["return_frames"].values()]:
        retained[Path(hold["path"])] = hold["PNG_sha256"]
''',
    prior.cleanup_source[attempt_start:attempt_end]: '',
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
    section = (stub + f"""Six complete exchanges add 129 decisions, 16 wording revisions and 113 individual retentions. All 17 revised layouts passed exact font checks, including both supported surname cases. Focused controller gameplay verified 19 panels, including three original notices and the return to port. Natural scene triggers and handheld display remain unvisited on this build. [Exact review](../{release.REVIEW.as_posix()})

The sole .nds on Drive matches SHA-256 {candidate}. The clean-input patch reconstructs it byte for byte. Startup and 17 targeted repository tests passed. Cleanup removed {len(result['removed'])} redundant files and reclaimed {result['reclaimed_bytes']:,} bytes. [Latest testing build]({drive['url']}) · [Clean-input patch](../{release.PATCH.as_posix()}) · [Cleanup receipt](../{cleanup_ref})

The current scan has {open_wraps} wrap leads awaiting a decision. The next source packet binds 290 texts across Hodram B17 and B85 and Lil B26 and B133. Continue these four exchanges and the remaining Rafael tutorial and story leads. Keep the practical town and random sampling, 276 shared display leads, identities and names, 27,700 historical credits, deferred artwork, and later older-record technical re-audit active. [Current wrap queue](../{queue_ref}) · [Hodram and Lil paired source](../translations/editorial_checkpoints/hodram_and_lil_followups_20261122/paired_source.json)

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
