"""Record the published candidate and remove verified duplicate checkpoint storage."""

from json import dumps
from os import link, replace
from pathlib import Path

from scripts import register_pirate_affiliation_20261123 as release
from scripts import probe_pirate_panel_emulator_20261123 as panels
from scripts.observe_legacy_fleet_text_20261123 import ROOT as REGIONAL


base, stage = release.base, release.stage
BOOK = Path("translations/editorial_checkpoints/pirate_affiliation_20261123")
DRIVE = release.ROOT / "drive_latest_build_receipt.json"
OUT = BOOK / "checkpoint_cleanup.json"


def duplicate_save(report_file, scope):
    save = base.load(report_file)["battery_save_preloaded"]
    source, duplicate = Path(save["source"]), Path(save["destination"])
    assert duplicate.resolve().parent == scope.resolve()
    assert source.resolve() != duplicate.resolve()
    assert base.digest(source) == save["source_sha256"]
    if not duplicate.is_file() or base.digest(duplicate) != save["source_sha256"]:
        return None
    receipt = dict(path=str(duplicate), retained=str(source), bytes=duplicate.stat().st_size,
                   sha256=save["source_sha256"], reason="Temporary battery save matches the original donor.")
    duplicate.unlink()
    return receipt


def main():
    registered, drive = map(base.load, (release.RELEASE, DRIVE))
    candidate = registered["candidate_sha256"]
    assert candidate == drive["sha256"] and drive["sole_nds_in_folder"] and drive["readback_verified"]
    assert base.digest(release.ROM) == base.digest(stage.ROM) == candidate
    assert release.ROM.samefile(stage.REBUILT) and not OUT.exists()
    BOOK.mkdir(parents=True, exist_ok=True)
    base.save(BOOK / DRIVE.name, drive)
    staged = stage.ROM.resolve()
    assert staged.parent == stage.ROOT.resolve() and not staged.samefile(release.ROM)
    replacement = staged.with_suffix(".same-verified-rom")
    assert not replacement.exists() and staged.stat().st_nlink == 1
    link(release.ROM, replacement)
    replace(replacement, staged)
    assert staged.samefile(release.ROM)
    removed = [dict(path=str(stage.ROM), retained=str(release.ROM), bytes=staged.stat().st_size,
                    sha256=candidate, reason="Preserved the original pathname with a verified hard link.")]
    captures = [stage.STARTUP_CAPTURE.parent, REGIONAL / "regional/capture",
                *(panels.ROOT / case / "capture" for case in ("installed", "english", "staged"))]
    for folder in captures:
        receipt = duplicate_save(folder / "capture_report.json", folder / "saves")
        if receipt:
            removed.append(receipt)
    base.save(OUT, dict(candidate_sha256=candidate, removed_duplicate_storage=removed,
                       focused_test_scratch=dict(path="work/pytest_pirate_affiliation_20261123", files=9, bytes=13282),
                       all_named_ROM_paths_and_test_evidence_preserved=True))
    size = sum(row["bytes"] for row in removed) + 13282
    text = ("# Current editorial checkpoint - 2026-11-23\n\n"
        "The registered cumulative candidate displays **Pirate** on the alternate-battle nameplate. "
        "All nine visible nameplate holds passed. The staged ROM matched all eleven focused fixture frames using its stored label. "
        "Six startup holds, 24 protected name getter checks, all 17 focused tests and exact clean-input reconstruction passed. "
        "Ordinary activation and exit for this alternate battle remain unvisited. "
        f"[Registered review](../{release.REVIEW.as_posix()})\n\n"
        f"Drive contains one .nds and the readback matches SHA-256 `{candidate}`. "
        f"[Latest testing build]({drive['url']}) · [Clean-input patch](../{release.PATCH.as_posix()})\n\n"
        "Both legacy regional text formatters remain unobserved in ordinary play. "
        "Continue the remaining player-facing text inventory and keep the scoped evidence for their other callers. "
        f"Cleanup reclaimed {size:,} bytes. [Cleanup receipt](../{OUT.as_posix()})\n\n")
    for name in ("editorial_handoff_current.md", "translation_progress.md"):
        path = Path("docs") / name
        base.replace_checked(path, text.encode("utf-8") + path.read_bytes())
    print(f"Preserved all named ROM paths and reclaimed {size:,} duplicate and temporary bytes.")


if __name__ == "__main__":
    main()
