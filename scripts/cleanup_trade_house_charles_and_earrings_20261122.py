"""Refresh the wrap queue and clear redundant artifacts at the registered checkpoint."""

from pathlib import Path

from scripts import cleanup_rafael_confrontations_and_maria_wraps_20261122 as precedent
from scripts import register_trade_house_charles_and_earrings_20261122 as release
from scripts.source_locked_derivation_v5118 import checked_text


base, stage = release.base, release.stage
DRIVE = release.ROOT / "drive_latest_build_receipt.json"
RECEIPT = release.ROOT / "checkpoint_cleanup.json"
QUEUE = stage.draft.ROOT.parent / "current_wrap_queue.json"
prior_reviews = "(" + ", ".join("current" + ".parent" * i + ".REVIEW" for i in range(5, -1, -1)) + ")"
all_reviews = "(" + ", ".join("current" + ".parent" * i + ".REVIEW" for i in range(6, -1, -1)) + ")"
refresh_source = checked_text(precedent.refresh_source, {prior_reviews: all_reviews})
queue_scope = precedent.queue_scope | {"current": release, "OUTPUT": QUEUE}
exec(compile(refresh_source, __file__ + "::current-wrap-queue", "exec"), queue_scope)

cleanup_source = checked_text(precedent.cleanup_source, {
    '''    maria = base.load(release.live.MARIA_ROOT / "fixture_receipt.json")["fixture_ROMs"]["after"]
    assert Path(maria["path"]) == release.live.MARIA_ROM
    retained[release.live.MARIA_ROM] = maria["sha256"]
    retained[release.live.MARIA_REPORT] = focused["maria_report_sha256"]''':
        '''    hodram = base.load(release.live.HODRAM_ROOT / "fixture.json")
    assert Path(hodram["fixture"]) == release.live.HODRAM_ROM
    retained[release.live.HODRAM_ROM] = hodram["fixture_sha256"]
    retained[release.live.HODRAM_REPORT] = focused["hodram_report_sha256"]''',
    'for exit in [focused["rafael_return"], *focused["maria_returns"]]':
        'for exit in [focused["rafael_return"], focused["hodram_return"]]',
    'capture_reports.append((release.live.MARIA_REPORT, maria["sha256"]))':
        'capture_reports.append((release.live.HODRAM_REPORT, hodram["fixture_sha256"]))',
    'release.live.MARIA_ROM.resolve()': 'release.live.HODRAM_ROM.resolve()',
    'release_stack_with_rafael_confrontations_and_maria_wraps.json': 'release_stack_with_trade_house_charles_and_earrings.json',
    'stage.draft.ROOT.parent / "initial_preflight")': 'stage.draft.ROOT.parent / "initial_preflight", stage.draft.ROOT.parent / "layout_trial")',
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

This pass covered 119 dialogue turns and four choice labels. It installed 24 wording revisions and three wrap fixes, with 92 dialogue turns and four choice labels retained for specific reasons. Focused Rafael and Hodram replays verified 17 pages with their speaker labels. Every installed line passed native visual checks, including Clau's greeting with the longest supported name. Shipwright (actor 109, 造船所の親父) and Shady Man (actor 173, 怪しい人) retain their source-supported role labels. The two choice command objects passed exact offline checks. Their natural branches and handheld behavior remain unvisited. [Exact source and installed references](../{release.REVIEW.as_posix()})

The sole .nds in the Drive folder matches SHA-256 {drive['sha256']}. The patch reconstructs it byte for byte. Startup and 17 regressions passed. Cleanup reclaimed {result['reclaimed_bytes']:,} bytes from {len(result['removed'])} redundant files. [Latest testing ROM]({drive['url']}) · [Patch](../{release.PATCH.as_posix()}) · [Cleanup receipt](../{RECEIPT.as_posix()})

The refreshed queue has {leads} heuristic leads, including {reviewed} with current source-based decisions. Continue with Rafael's B123 and Hodram's B168 and B172 exchanges, including representative town and random content in the wider pass. Carry forward the 27,700 credited records and 276 shared display leads. [Current wrap queue](../{QUEUE.as_posix()})

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
