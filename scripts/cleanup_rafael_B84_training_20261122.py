"""Refresh the wrap queue and clear verified duplicate B84 staging files."""

from pathlib import Path

from scripts import cleanup_mosque_elysion_mikhail_20261122 as baseline
from scripts import cleanup_north_sea_and_hodram_reconciliation_20261122 as prior
from scripts import register_rafael_B84_training_20261122 as release
from scripts.source_locked_derivation_v5118 import checked_text


base,stage=release.base,release.stage
DRIVE=release.ROOT/"drive_latest_build_receipt.json"
RECEIPT=release.ROOT/"checkpoint_cleanup.json"
QUEUE=stage.BATCH/"current_wrap_queue.json"
all_reviews="("+", ".join("current"+".parent"*i+".REVIEW" for i in range(11,-1,-1))+")"
refresh_source=checked_text(prior.refresh_source,{prior.all_reviews:all_reviews})
queue_scope=prior.queue_scope|dict(current=release,OUTPUT=QUEUE)
exec(compile(refresh_source,__file__+"::current-wrap-queue","exec"),queue_scope)

old_source=baseline.cleanup_source
fixture_start=old_source.index('    fixture = base.load(')
fixture_end=old_source.index('    assert all(base.digest(p) == h for p, h in retained.items())')
trials_start=old_source.index("    history = stage.BATCH.parent")
trials_end=old_source.index("    removed = []",trials_start)
cleanup_source=checked_text(old_source,{
    "release_stack_with_mosque_elysion_mikhail.json":"release_stack_with_rafael_B84_training.json",
    old_source[fixture_start:fixture_end]:'''    for kind in ("speech","pact_entry","lesson_entry"):
        fixture = base.load(release.replay.ROOT / kind / "fixture.json")
        assert fixture["candidate_sha256"] == candidate and fixture["exact_inverse"]
        retained[Path(fixture["path"])] = fixture["rom_sha256"]
    pins = {Path(r["path"]).resolve() for r in base.load(Path("translations/rom_retention_pins.json"))}
    assert stage.ROM.resolve() not in pins
    fixture_paths = {path.resolve() for path in retained if path.name.endswith("_FOCUSED_ONLY.nds")}
    assert len(fixture_paths)==3 and fixture_paths <= pins
    for entry in [*focused["observations"], *(p for m in focused["original_menu_choices"] for p in m["observations"])]:
        hold = entry["capture"]
        retained[Path(hold["path"])] = hold["PNG_sha256"]
    closing = focused["return_frame"]
    retained[Path(closing["path"])] = closing["PNG_sha256"]
    for site, sha in focused["report_sha256"].items():
        path = Path(site)
        data = base.load(path)
        assert base.digest(path) == sha
        retained[path] = sha
        capture_reports.append((path,data["ROM_sha256"]))
''',
    old_source[trials_start:trials_end]:"    roots = stage.ROOT.resolve(), release.ROOT.resolve()\n",
})
scope=baseline.scope|globals()
scope["workflow"]=release.parent.scope["workflow"]
exec(compile(cleanup_source,__file__+"::cleanup", "exec"),scope)


def handoff(result):
    drive,queue=map(base.load,(DRIVE,QUEUE))
    assert drive["sha256"]==queue["candidate_sha256"]==result["candidate_sha256"]
    open_wraps=sum("reviewed" not in row for row in queue["records"])
    section=f"""# Current editorial checkpoint - 2026-11-22

{release.CHECKPOINT} [Checkpoint]({release.DOC.name})

This complete B84 pass covers 131 texts with eight revised speeches, a corrected choice and 122 individually justified retentions. Rafael can say that they do not have to defeat Vels. Controller input verified both Vels options and the training lesson-only option, including their original responses. Fifteen complete speech or notice panels, both two-page instructional notices, all nine revised native speech variants, and the exact choice pixels passed. Both menu objects and all 20 relative destinations preserve their structure. Natural activation and handheld display remain unvisited here. [Exact review and verification](../{release.REVIEW.as_posix()})

The sole .nds on Drive matches SHA-256 {drive['sha256']}. The patch rebuilds it byte for byte. Startup and 17 focused regressions passed. Cleanup removed {len(result['removed'])} redundant files and reclaimed {result['reclaimed_bytes']:,} bytes. [Latest testing build]({drive['url']}) · [Patch](../{release.PATCH.as_posix()}) · [Cleanup receipt](../{RECEIPT.as_posix()})

The scan has {open_wraps} wrap leads awaiting a current decision. Continue with the 90 outstanding Hodram B61–B70 differences in their original exchanges and other unfinished route and tutorial leads. Keep names, shared dialogue ownership and representative ordinary town and random coverage active across all four routes. Preserve the 27,700 historical credits and 276 shared display leads. Graphics artwork and the later older-record technical re-audit remain separate. [Current wrap queue](../{QUEUE.as_posix()})

""".encode("utf-8")
    for name in ("editorial_handoff_current.md","translation_progress.md"):
        path=release.DOC.with_name(name)
        body=path.read_bytes()
        boundary=body.index(b"# Current editorial checkpoint",1)
        base.replace_checked(path,section+body[boundary:])


if __name__=="__main__":
    if not QUEUE.exists():
        queue_scope["main"]()
    if not RECEIPT.exists():
        scope["cleanup"]()
    handoff(base.load(RECEIPT))
