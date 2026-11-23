"""Refresh wrap leads and remove verified duplicate staging artifacts."""

from pathlib import Path

from scripts import cleanup_trade_house_charles_and_earrings_20261122 as precedent
from scripts import register_mosque_elysion_mikhail_20261122 as release
from scripts.source_locked_derivation_v5118 import checked_text


base, stage = release.base, release.stage
DRIVE = release.ROOT / "drive_latest_build_receipt.json"
RECEIPT = release.ROOT / "checkpoint_cleanup.json"
QUEUE = stage.BATCH / "current_wrap_queue.json"
FOLLOWUP = stage.BATCH / "company_period_followup.json"
prior_reviews = precedent.all_reviews
all_reviews = "(" + ", ".join("current" + ".parent" * i + ".REVIEW" for i in range(7, -1, -1)) + ")"
refresh_source = checked_text(precedent.refresh_source, {prior_reviews: all_reviews})
queue_scope = precedent.queue_scope | {"current": release, "OUTPUT": QUEUE}
exec(compile(refresh_source, __file__ + "::current-wrap-queue", "exec"), queue_scope)

cleanup_source = checked_text(precedent.cleanup_source, {
    'release_stack_with_trade_house_charles_and_earrings.json': 'release_stack_with_mosque_elysion_mikhail.json',
    '    review_root = stage.draft.ROOT.parent.resolve()':
        '''    history = stage.BATCH.parent
    review_root = history.resolve()
    trial_root = history / "staged"
    trial_rom = trial_root / stage.ROM.name
    trial = base.load(trial_root / stage.PROOF.name)
    assert base.digest(trial_rom) == trial["candidate_sha256"] and trial["candidate_sha256"] != candidate
    discard[trial_root / stage.REBUILT.name] = trial["candidate_sha256"]''',
    'for edition in (stage.draft.ROOT, stage.draft.ROOT.parent / "initial_preflight", stage.draft.ROOT.parent / "layout_trial"):':
        'for edition in (stage.BATCH, history, history / "initial_preflight", history / "layout_trial"):',
})
scope = precedent.scope | globals()
scope["workflow"] = release.parent.scope["workflow"]
exec(compile(cleanup_source, __file__ + "::cleanup", "exec"), scope)


def handoff(result):
    drive, queue = map(base.load, (DRIVE, QUEUE))
    lead = base.load(FOLLOWUP)
    assert drive["sha256"] == queue["candidate_sha256"] == result["candidate_sha256"] == lead["candidate_sha256"]
    leads = len(queue["records"])
    reviewed = sum("reviewed" in lead for lead in queue["records"])
    section = f"""# Current editorial checkpoint - 2026-11-22

{release.CHECKPOINT} [Checkpoint]({release.DOC.name})

The review covers 180 dialogue and tutorial records across three complete scenes. It contains 24 wording revisions, three wrap fixes and 153 justified retentions. Focused cold-boot replays verified 19 pages and their speaker labels, including direct visual review of Cesare's original symbols. Both revised runtime name layouts passed at the default and maximum supported widths offline. The seven original speakerless records are byte-exact. Natural story activation and handheld behavior remain unvisited for this batch. [Exact source and installed references](../{release.REVIEW.as_posix()})

The sole .nds in the Drive folder matches SHA-256 {drive['sha256']}. The patch reconstructs it byte for byte. Startup and 17 regressions passed. Cleanup reclaimed {result['reclaimed_bytes']:,} bytes from {len(result['removed'])} redundant files. [Latest testing ROM]({drive['url']}) · [Patch](../{release.PATCH.as_posix()}) · [Cleanup receipt](../{RECEIPT.as_posix()})

The refreshed queue has {leads} heuristic leads, including {reviewed} with current source-based decisions. The new Maria line avoids a duplicate period when the company is Castor Co. The older Rafael and Aziza exchange has a confirmed offline instance of the same defect. Its 78-turn contextual manuscript is drafted. Installation and display checks are pending. [Exact older instance](../{FOLLOWUP.as_posix()}) · [Aziza manuscript](../scripts/rafael_aziza_shamshir_pending_20261122.md) Continue with the remaining Rafael and Hodram clusters and the shared town and random pass. Prioritize representative natural town encounters and the 27 legacy dialogue records in the shared display worklist for source and display triage. Carry forward the 27,700 credited records and the full 276-entry worklist. [Current wrap queue](../{QUEUE.as_posix()})

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
