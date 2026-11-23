"""Refresh the exact wrap queue and clear this checkpoint's redundant files."""

from pathlib import Path

from scripts import cleanup_camille_and_maria_reveals_20261122 as precedent
from scripts import register_rafael_confrontations_and_maria_wraps_20261122 as release
from scripts.source_locked_derivation_v5118 import checked_text


base, stage = release.base, release.stage
DRIVE = release.ROOT / "drive_latest_build_receipt.json"
RECEIPT = release.ROOT / "checkpoint_cleanup.json"
QUEUE = stage.draft.ROOT.parent / "current_wrap_queue.json"
refresh_source = checked_text(precedent.refresh_source, {
    '(current.parent.parent.parent.parent.REVIEW, current.parent.parent.parent.REVIEW, current.parent.parent.REVIEW, current.parent.REVIEW, current.REVIEW)':
        '(current.parent.parent.parent.parent.parent.REVIEW, current.parent.parent.parent.parent.REVIEW, current.parent.parent.parent.REVIEW, current.parent.parent.REVIEW, current.parent.REVIEW, current.REVIEW)',
})
queue_scope = precedent.queue_scope | {"current": release, "OUTPUT": QUEUE}
exec(compile(refresh_source, __file__ + "::current-wrap-queue", "exec"), queue_scope)

cleanup_source = checked_text(precedent.cleanup_source, {
    '    assert Path(fixture["fixture"]) == release.live.ROM\n    retained[release.live.ROM] = fixture["fixture_sha256"]':
        '    assert Path(fixture["fixture_ROM"]) == release.live.ROM\n    retained[release.live.ROM] = fixture["fixture_ROM_sha256"]',
    '    capture_reports.append((release.live.REPORT, fixture["fixture_sha256"]))':
        '    capture_reports.append((release.live.REPORT, fixture["fixture_ROM_sha256"]))',
    'focused["lil_report_sha256"]': 'focused["rafael_report_sha256"]',
    'focused["lil_return"]': 'focused["rafael_return"]',
    'release_stack_with_camille_and_maria_reveals.json': 'release_stack_with_rafael_confrontations_and_maria_wraps.json',
    '    roots = stage.ROOT.resolve(), release.ROOT.resolve()':
        '''    review_root = stage.draft.ROOT.parent.resolve()
    for edition in (stage.draft.ROOT, stage.draft.ROOT.parent / "initial_preflight"):
        proof = base.load(edition / "native_preflight.json")
        for picture in proof["sheets"]:
            child = edition / Path(picture["path"]).name
            assert child.resolve().parent == edition.resolve()
            discard[child] = picture["sha256"]
    roots = stage.ROOT.resolve(), release.ROOT.resolve(), review_root''',
})
scope = precedent.scope | globals()
scope["workflow"] = release.parent.scope["workflow"]
exec(compile(cleanup_source, __file__ + "::cleanup", "exec"), scope)


def handoff(result):
    drive = base.load(DRIVE)
    queue = base.load(QUEUE)
    assert queue["candidate_sha256"] == drive["sha256"] == result["candidate_sha256"]
    leads = len(queue["records"])
    reviewed = sum("reviewed" in lead for lead in queue["records"])
    section = f"""# Current editorial checkpoint - 2026-11-22

{release.CHECKPOINT} [Checkpoint]({release.DOC.name})

The batch compared 207 records in four complete exchanges against the clean source. It contains 25 wording revisions, seven wrap corrections and 175 justified retentions. Focused Rafael and Maria cold-boot replays verified 18 pages and their nameplates, including both reported Maria phrase breaks. Both hosts returned to port. Native and visual checks covered every installed change. Natural story triggers and hardware remain unvisited for this batch. [Exact source and installed references](../{release.REVIEW.as_posix()})

The sole .nds in the Drive folder matches SHA-256 {drive['sha256']}. The patch reconstructs it byte for byte. Startup and 17 regressions passed. Cleanup reclaimed {result['reclaimed_bytes']:,} bytes from {len(result['removed'])} redundant files. [Latest testing ROM]({drive['url']}) · [Patch](../{release.PATCH.as_posix()}) · [Cleanup receipt](../{RECEIPT.as_posix()})

The refreshed queue has {leads} heuristic leads, including {reviewed} with current source-based decisions. Continue with the next Rafael and Hodram clusters and practical town and random scenes. Carry forward the 27,700 credited records and 276 shared display leads. Charlotte's FI-prefaced thanks in SC0 B69 R0143 preserves the dramatic beat and exact substitution. Its opening can be reassessed alongside other runtime-name variants. [Current wrap queue](../{QUEUE.as_posix()})

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
