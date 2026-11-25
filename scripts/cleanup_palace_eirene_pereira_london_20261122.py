"""Refresh the review queue and remove verified duplicate checkpoint artifacts."""

from pathlib import Path

from scripts import cleanup_aziza_shamshir_20261122 as aziza
from scripts import cleanup_mosque_elysion_mikhail_20261122 as precedent
from scripts import register_palace_eirene_pereira_london_20261122 as release
from scripts.source_locked_derivation_v5118 import checked_text


base, stage = release.base, release.stage
DRIVE = release.ROOT / "drive_latest_build_receipt.json"
RECEIPT = release.ROOT / "checkpoint_cleanup.json"
QUEUE = stage.BATCH / "current_wrap_queue.json"
all_reviews = "(" + ", ".join("current" + ".parent" * i + ".REVIEW" for i in range(9, -1, -1)) + ")"
refresh_source = checked_text(aziza.refresh_source, {aziza.all_reviews: all_reviews})
queue_scope = aziza.queue_scope | {"current": release, "OUTPUT": QUEUE}
exec(compile(refresh_source, __file__ + "::current-wrap-queue", "exec"), queue_scope)

cleanup_source = checked_text(precedent.cleanup_source, {
    'release_stack_with_mosque_elysion_mikhail.json': 'release_stack_with_palace_eirene_pereira_london.json',
    '    capture_reports.append((release.live.HODRAM_REPORT, hodram["fixture_sha256"]))':
        '''    capture_reports.append((release.live.HODRAM_REPORT, hodram["fixture_sha256"]))
    town = release.verify_town(candidate)
    retained.update({Path(path): sha for path, sha in town["evidence"].items()})
    visit = release.town.ROOT / release.town.CASE / "capture/capture_report.json"
    retained[visit] = base.digest(visit)
    capture_reports.append((visit, candidate))''',
    'for edition in (stage.BATCH, history, history / "initial_preflight", history / "layout_trial"):':
        'for edition in (stage.BATCH, history, history / "initial_preflight"):',
})
scope = precedent.scope | globals()
scope["workflow"] = release.parent.scope["workflow"]
exec(compile(cleanup_source, __file__ + "::cleanup", "exec"), scope)


def handoff(result):
    drive, queue = map(base.load, (DRIVE, QUEUE))
    assert drive["sha256"] == queue["candidate_sha256"] == result["candidate_sha256"]
    leads = len(queue["records"])
    reviewed = sum("reviewed" in lead for lead in queue["records"])
    section = f"""# Current editorial checkpoint - 2026-11-22

{release.CHECKPOINT} [Checkpoint]({release.DOC.name})

Four complete exchanges add 275 contextual decisions and two retained choice labels. The candidate installs 25 wording revisions and keeps 250 dialogue records for individual reasons. The focused emulator replays verify 23 story panels and their nameplates. All 27 changed-page variants matched exact game-font and contact-sheet pixels offline, including default and maximum-width substitutions. Cristina's harbor line now breaks after her complete sentence. The first word of Rafael's earlier pushy line was present in the saved preview pixels and in emulator playback. The lesson options and seven speakerless commands remain byte-exact. [Coverage and exact source/current references](../{release.REVIEW.as_posix()})

An ordinary saved-game visit to Tripoli reached the original Tavern, verified the greeting, five-coin drink price and randomly selected Algiers lead, then returned to its menu. Natural activation of the four story excerpts, the live lesson choice branches, and handheld checks remain unvisited in this batch. [Tripoli observation](../{release.ORDINARY.as_posix()})

The sole .nds in the Drive folder matches SHA-256 {drive['sha256']}. The patch reconstructs it byte for byte. Startup and 17 focused regressions passed. Cleanup reclaimed {result['reclaimed_bytes']:,} bytes from {len(result['removed'])} redundant files. [Latest testing ROM]({drive['url']}) · [Patch](../{release.PATCH.as_posix()}) · [Cleanup receipt](../{RECEIPT.as_posix()})

The current scan has {leads} heuristic wrap leads, with {reviewed} covered by source-based decisions. Continue Rafael's earlier Proof and tutorial exchanges and the next large Hodram clusters, then the remaining four-route retrospective and shared dialogue, speaker labels, conditional substitutions, and player-facing prose. Continue ordinary town and random coverage where reproducible. Preserve the 27,700 historical credits and the 276-entry shared display worklist, including the 27 legacy dialogue records and eight raw scene labels still awaiting proven consumers. Graphics artwork and the later older-record technical re-audit stay separate. [Current wrap queue](../{QUEUE.as_posix()})

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
