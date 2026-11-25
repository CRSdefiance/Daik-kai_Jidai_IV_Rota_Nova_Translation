"""Refresh the wrap queue and archive the verified Lisbon checkpoint."""

from pathlib import Path
from shutil import copyfile

from scripts import cleanup_rafael_athens_and_maria_crew_20261122 as prior
from scripts import register_rafael_proof_and_financing_20261122 as release
from scripts.source_locked_derivation_v5118 import checked_text


base, stage = release.base, release.stage
DRIVE = release.ROOT / "drive_latest_build_receipt.json"
RECEIPT = release.ROOT / "checkpoint_cleanup.json"
QUEUE = stage.BATCH / "current_wrap_queue.json"
CHECKPOINT_DIR = Path("translations/editorial_checkpoints/rafael_lisbon_financing_20261122")
all_reviews = "(" + ", ".join("current" + ".parent" * i + ".REVIEW" for i in range(15, -1, -1)) + ")"
refresh_source = checked_text(prior.refresh_source, {prior.all_reviews: all_reviews})
queue_scope = prior.queue_scope | dict(current=release, OUTPUT=QUEUE)
exec(compile(refresh_source, __file__ + "::current-wrap-queue", "exec"), queue_scope)

start = prior.cleanup_source.index('    pins = {Path(r["path"]).resolve()')
end = prior.cleanup_source.index("    assert all(base.digest(p) == h for p, h in retained.items())")
trials_start = prior.cleanup_source.index("    history = stage.BATCH.parent")
trials_end = prior.cleanup_source.index("    removed = []", trials_start)
cleanup_source = checked_text(prior.cleanup_source, {
    "release_stack_with_rafael_athens_and_maria_crew.json": "release_stack_with_rafael_proof_and_financing.json",
    prior.cleanup_source[start:end]:'''    pins = {Path(r["path"]).resolve() for r in base.load(Path("translations/rom_retention_pins.json"))}
    assert stage.ROM.resolve() not in pins
    for run in release.live.RUNS:
        key = "speech" if run == "speech" else "choice"
        fixture = base.load(release.live.ROOT / key / "fixture.json")
        assert fixture["candidate_sha256"] == candidate and fixture["exact_inverse"]
        rom = Path(fixture["rom"])
        assert rom.resolve() in pins
        retained[rom] = fixture["rom_sha256"]
        path = release.live.report(run)
        digest = focused["report_sha256"][run]
        assert base.digest(path) == digest
        retained[path] = digest
        capture_reports.append((path, fixture["rom_sha256"]))
    opening = release.ordinary_opening(candidate)
    retained[release.ordinary.REPORT] = opening["report_sha256"]
    capture_reports.append((release.ordinary.REPORT, candidate))
    menu = [item for choice in focused["original_menu_choices"] for item in choice["observations"]]
    for hold in [*(o["capture"] for o in [*focused["observations"], *menu, *opening["observations"]]),
                 focused["return_frame"]]:
        retained[Path(hold["path"])] = hold["PNG_sha256"]
''',
    prior.cleanup_source[trials_start:trials_end]:'''    history = stage.BATCH.parent
    attempt = history / "registration_attempt_1"
    if attempt.exists():
        discard[attempt / "registry_work" / release.ROM.name] = candidate
        discard[attempt / "partial_package" / release.PATCH.name] = base.digest(release.PATCH)
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
    opening = release.ordinary_opening(candidate)
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
    section = (stub + f"""Both complete exchanges add 142 text decisions and two retained preparation labels. Sixteen passages changed and 126 spoken or system texts have individual retention reasons. The startup loan keeps its amount and terms. Focused controller input verified both preparation selections and Julio's corresponding replies. Seventeen revised native layouts, the original gold notice, and 21 focused holds passed. Ordinary New Game reached {len(opening['observations'])} exact revised Lisbon panels. Focused gameplay covers the other revised panels. Natural activation of the Proof briefing and preparation choice and handheld display remain unvisited. [Exact review](../{release.REVIEW.as_posix()})

The sole .nds on Drive matches SHA-256 {candidate}. The clean-input patch reconstructs it byte for byte. Startup and 17 targeted repository tests passed. Cleanup removed {len(result['removed'])} redundant files and reclaimed {result['reclaimed_bytes']:,} bytes. [Latest testing build]({drive['url']}) · [Clean-input patch](../{release.PATCH.as_posix()}) · [Cleanup receipt](../{cleanup_ref})

The current scan has {open_wraps} wrap leads awaiting a decision. The next manuscript covers 129 records in Rafael B50, B52, B55, B57, B61 and B62. Continue the other storylines, town and random scenes, shared dialogue ownership, speaker names and remaining prose. Preserve the 276 shared display leads, 27,700 historical credits, deferred graphics artwork and later older-record technical re-audit. [Current wrap queue](../{queue_ref}) · [Lil and Lisbon manuscript](../scripts/rafael_lil_farewell_and_lisbon_summons_20261122.md) · [Sofala and following exchanges](../scripts/rafael_sofala_arcadius_pereira_and_scabbard_20261122.md)

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
