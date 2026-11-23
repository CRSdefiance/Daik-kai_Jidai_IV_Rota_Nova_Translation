"""Remove verified redundant Osaka checkpoint artifacts and record the coverage."""

from gzip import open as gzip_open
from hashlib import file_digest
from pathlib import Path

from scripts import register_osaka_glass_20261122 as release


base, stage = release.base, release.stage
DRIVE = release.ROOT / "drive_latest_build_receipt.json"
RECEIPT = release.ROOT / "checkpoint_cleanup.json"


def cleanup():
    assert not RECEIPT.exists()
    meta, plan, drive, focused, boot, visual = map(base.load, (
        release.RELEASE, release.VERIFY / "registration_mutation_plan.json", DRIVE, stage.LIVE,
        release.VERIFY / release.STARTUP.name, release.VISUAL))
    candidate, patch = meta["candidate_sha256"], meta["patch_sha256"]
    assert candidate == drive["sha256"] == focused["candidate_sha256"] == boot["candidate_sha256"]
    assert drive["sole_nds_in_folder"] and drive["readback_verified"]
    assert base.digest(base.REGISTRY) == plan["registry_after"] == meta["registry_sha256"]
    assert base.digest(base.LEDGER) == plan["ledger_after"]
    assert base.digest(base.PROMOTED) == plan["main_sha256"]
    assert base.load(release.PACKAGE / "checksums.json") == release.workflow.package_checksums(release.PACKAGE)
    retained = {release.ROM: candidate, stage.ROM: candidate, release.PATCH: patch,
        release.MANIFEST: meta["manifest_sha256"], Path(meta["own_registered_startup"]): meta["own_registered_startup_sha256"]}
    retained.update({Path(p): h for p, h in visual["sheets"].items()})
    capture_reports = [(stage.STARTUP_CAPTURE, candidate)]
    for row in [*boot["exact_matching_frames"], boot["read_only_snapshot"]]:
        retained[Path(row["path"])] = row.get("PNG_sha256", row.get("sha256"))
    for route, case in focused["cases"].items():
        folder = stage.ROOT / f"route{route}"
        fixture = base.load(folder / "fixture.json")
        retained[Path(fixture["rom"])] = fixture["sha256"]
        capture = Path(case["capture"])
        retained[capture] = case["capture_sha256"]
        capture_reports.append((capture, fixture["sha256"]))
        for row in [*(s["capture"] for s in case["sightings"]), case["end_capture"]]:
            retained[Path(row["path"])] = row["PNG_sha256"]
    assert all(base.digest(p) == h for p, h in retained.items())
    keep = {p.resolve() for p in retained}

    discard = {stage.REBUILT: candidate, stage.PATCH: patch}
    for archive, key in ((release.ROOT / "editorial_ledger_before.json.gz", "ledger_before"),
                         (release.PACKAGE / "build_release_stack.json.gz", "registry_after")):
        with gzip_open(archive, "rb") as source:
            assert file_digest(source, "sha256").hexdigest() == plan[key]
    for filename, key in (("ledger_before.json", "ledger_before"), ("ledger_after.json", "ledger_after"),
                          ("release_stack_with_osaka_glass.json", "registry_after")):
        discard[release.ROOT / filename] = plan[key]
    for path, sha in capture_reports:
        report = base.load(path)
        assert report["ROM_sha256"] == sha and report["cold_boot"] and not report["savestate_loaded"]
        for row in report["frames_captured"]:
            child = Path(row["path"])
            assert child.resolve().parent == path.parent.resolve()
            if child.resolve() not in keep:
                discard[child] = row["PNG_sha256"]
        battery = report.get("battery_save_preloaded")
        if battery:
            copy = Path(battery["destination"])
            assert copy.resolve().parent == (path.parent / "saves").resolve()
            assert base.digest(battery["source"]) == battery["source_sha256"]
            if copy.exists() and base.digest(copy) == battery["source_sha256"]:
                discard[copy] = battery["source_sha256"]

    roots = stage.ROOT.resolve(), release.ROOT.resolve()
    removed = []
    for path, sha in discard.items():
        resolved = path.resolve()
        assert any(resolved.is_relative_to(d) for d in roots)
        assert resolved not in keep and not path.is_symlink() and not path.is_junction()
        assert path.suffix in {".nds", ".xdelta", ".json", ".png", ".dsv"} and base.digest(path) == sha
        removed.append(dict(path=str(path), sha256=sha, bytes=path.stat().st_size))
    for path in discard:
        path.unlink()
    assert all(base.digest(path) == sha for path, sha in retained.items())
    result = dict(candidate_sha256=candidate, removed=removed,
        reclaimed_bytes=sum(row["bytes"] for row in removed), retained_verified_files=len(retained))
    base.save(RECEIPT, result)
    print(f"Removed {len(removed)} redundant files and reclaimed {result['reclaimed_bytes']:,} bytes.", flush=True)
    return result


def handoff(result):
    drive = base.load(DRIVE)
    assert drive["sha256"] == result["candidate_sha256"]
    section = f"""# Current editorial checkpoint - 2026-11-22

{release.CHECKPOINT} [Checkpoint]({release.DOC.name})

The sole .nds in the Rota Nova Translation Drive folder matches SHA-256 {drive['sha256']}. The clean-input patch reconstructed it byte for byte. The candidate preserves all 114 accepted layers and the ASCII right-bound correction. Startup and 17 focused tests passed. Cleanup removed {len(result['removed'])} redundant files and reclaimed {result['reclaimed_bytes']:,} bytes. [Latest testing build]({drive['url']}) | [Clean-input patch](../{release.PATCH.as_posix()}) | [Cleanup receipt](../{RECEIPT.as_posix()})

The source review covers 44 dialogue turns with two revisions and 42 individual retentions. Focused emulator replays displayed all 22 Hodram and Maria pages, including both speakerless forecasts, 20 complete nameplates, and the exit into the calling context. Rafael and Lil retained their earlier display evidence. The Nagasaki voyage has no ordinary Osaka activation. [Exact decisions and coverage](../{release.REVIEW.as_posix()}) | [Display evidence](../{release.VERIFY.as_posix()})

Continue with other practical ordinary town and random scenes, using verified port saves where available, then follow the remaining player-facing prose and 276 alternate display leads. Keep earlier contextual credit, conditional and custom name review, unresolved artwork, and the later older-record technical re-audit in their documented scopes.

""".encode("utf-8")
    for name in ("editorial_handoff_current.md", "translation_progress.md"):
        path = release.DOC.with_name(name)
        body = path.read_bytes()
        second = body.index(b"# Current editorial checkpoint", 1)
        base.replace_checked(path, section + body[second:])


if __name__ == "__main__":
    handoff(cleanup())

