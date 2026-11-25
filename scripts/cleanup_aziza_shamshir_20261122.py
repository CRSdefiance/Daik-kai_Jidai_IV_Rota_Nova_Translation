"""Refresh the open wrap queue and clear verified duplicate checkpoint artifacts."""

from pathlib import Path

from scripts import cleanup_mosque_elysion_mikhail_20261122 as precedent
from scripts import register_aziza_shamshir_20261122 as release
from scripts.source_locked_derivation_v5118 import checked_text


base, stage = release.base, release.stage
DRIVE = release.ROOT / "drive_latest_build_receipt.json"
RECEIPT = release.ROOT / "checkpoint_cleanup.json"
QUEUE = stage.BATCH / "current_wrap_queue.json"
all_reviews = "(" + ", ".join("current" + ".parent" * i + ".REVIEW" for i in range(8, -1, -1)) + ")"
refresh_source = checked_text(precedent.refresh_source, {precedent.all_reviews: all_reviews})
queue_scope = precedent.queue_scope | {"current": release, "OUTPUT": QUEUE}
exec(compile(refresh_source, __file__ + "::current-wrap-queue", "exec"), queue_scope)
old_source = precedent.cleanup_source
second_fixture = old_source[old_source.index('    hodram = base.load('):old_source.index('    retained.update({Path(r["path"]): r["sha256"] for r in focused["sheets"]})')]
old_trials = old_source[old_source.index('    history = stage.BATCH.parent'):old_source.index('        proof = base.load(edition / "native_preflight.json")')]
cleanup_source = checked_text(old_source, {
    'fixture = base.load(release.live.ROM.with_name("fixture.json"))': 'fixture = base.load(release.live.ROOT / "fixture.json")',
    'focused["rafael_report_sha256"]': 'focused["report_sha256"]',
    second_fixture:'''    town = base.load(release.ORDINARY)
    assert town["candidate_sha256"] == candidate and town["ordinary_saved_gameplay"]
    retained.update({Path(path): sha for path, sha in town["evidence"].items()})
    for case in ("copenhagen", "tripoli_square", "tripoli", "tripoli_docked"):
        report = release.town.ROOT / case / "capture/capture_report.json"
        retained[report] = base.digest(report)
        capture_reports.append((report, candidate))
''',
    'for exit in [focused["rafael_return"], focused["hodram_return"]]':
        'for exit in [focused["return_frame"]]',
    '    capture_reports.append((release.live.HODRAM_REPORT, hodram["fixture_sha256"]))\n': '',
    '{release.live.ROM.resolve(), release.live.HODRAM_ROM.resolve()} <= pins': 'release.live.ROM.resolve() in pins',
    'release_stack_with_mosque_elysion_mikhail.json': 'release_stack_with_aziza_shamshir.json',
    old_trials:'''    review_root = stage.BATCH.resolve()
    for edition in (stage.BATCH, stage.BATCH / "initial_preflight"):
''',
})
scope = precedent.scope | globals()
scope["workflow"] = release.parent.scope["workflow"]
exec(compile(cleanup_source, __file__ + "::cleanup", "exec"), scope)


def handoff(result):
    drive, queue, visits = map(base.load, (DRIVE, QUEUE, release.ORDINARY))
    assert drive["sha256"] == queue["candidate_sha256"] == result["candidate_sha256"] == visits["candidate_sha256"]
    leads = len(queue["records"])
    reviewed = sum("reviewed" in lead for lead in queue["records"])
    observed = sum(len(r["panels"]) for r in visits["visits"].values())
    section = f"""# Current editorial checkpoint - 2026-11-22

{release.CHECKPOINT} [Checkpoint]({release.DOC.name})

All 78 turns of Rafael and Aziza's exchange have exact source and installed references. The release includes 14 wording revisions and 64 justified retentions. Snake's company-name substitution now expands cleanly to Castor Co. The 11 focused story panels and 15 native layout variants passed. Natural story activation and hardware remain unvisited. [Coverage ledger](../{release.REVIEW.as_posix()})

The {observed} ordinary town panels come from preserved saves and original input at Copenhagen's Square and Tavern and Tripoli's Square. They include the four-line Hayreddin rumor and original nameplates. Tripoli's Tavern and unselected local variants remain unvisited. These observations add gameplay evidence for unchanged COMMON records. [Town observations](../{release.ORDINARY.as_posix()})

The sole .nds in the Drive folder matches SHA-256 {drive['sha256']}. The patch reconstructs it byte for byte. Startup and 17 regressions passed. Cleanup reclaimed {result['reclaimed_bytes']:,} bytes from {len(result['removed'])} redundant files. [Latest testing ROM]({drive['url']}) · [Patch](../{release.PATCH.as_posix()}) · [Cleanup receipt](../{RECEIPT.as_posix()})

The refreshed queue has {leads} heuristic leads, including {reviewed} with current source-based decisions. Continue with the remaining Rafael and Hodram clusters and shared town and random dialogue. Carry forward the 27,700 credited records and the full 276-entry shared worklist. [Current wrap queue](../{QUEUE.as_posix()})

""".encode("utf-8")
    for name in ("editorial_handoff_current.md", "translation_progress.md"):
        path = release.DOC.with_name(name)
        body = path.read_bytes()
        boundary = body.index(b"# Current editorial checkpoint", 1)
        base.replace_checked(path, section + body[boundary:])


if __name__ == "__main__":
    if not QUEUE.exists():
        queue_scope["main"]()
    if not RECEIPT.exists():
        scope["cleanup"]()
    handoff(base.load(RECEIPT))
