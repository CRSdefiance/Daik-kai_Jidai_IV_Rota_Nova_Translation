"""Record the verified Drive release and keep one physical copy of the rebuilt ROM."""

from os import link, replace
from pathlib import Path
from json import dumps

from scripts import register_online_card_copy_20261123 as release


base, stage = release.base, release.stage
BOOK = Path("translations/editorial_checkpoints/online_card_copy_20261123")
DRIVE = release.ROOT / "drive_latest_build_receipt.json"
OUT = BOOK / "checkpoint_cleanup.json"


def main():
    registered, drive = map(base.load, (release.RELEASE, DRIVE))
    candidate = registered["candidate_sha256"]
    assert candidate == drive["sha256"] and drive["sole_nds_in_folder"] and drive["readback_verified"]
    assert base.digest(release.ROM) == base.digest(stage.ROM) == candidate
    assert release.ROM.samefile(release.REBUILT) and not OUT.exists()
    BOOK.mkdir(parents=True, exist_ok=True)
    base.save(BOOK / DRIVE.name, drive)
    stage_file = stage.ROM.resolve()
    assert stage_file.is_relative_to(stage.ROOT.resolve())
    replacement = stage_file.with_suffix(".same-verified-rom")
    assert not replacement.exists() and stage_file.stat().st_nlink == 1
    link(release.ROM, replacement)
    replace(replacement, stage_file)
    assert stage_file.samefile(release.ROM)
    receipt = [dict(path=str(stage.ROM), retained=str(release.ROM), bytes=stage_file.stat().st_size,
        sha256=candidate, reason="Replaced duplicate physical ROM bytes with a hard link at the original path.")]
    startup = base.load(release.STARTUP_CAPTURE)
    save = startup["battery_save_preloaded"]
    duplicate, original = Path(save["destination"]), Path(save["source"])
    assert duplicate.resolve().is_relative_to((stage.ROOT / "startup/capture/saves").resolve())
    assert base.digest(original) == save["source_sha256"]
    if duplicate.is_file() and base.digest(duplicate) == save["source_sha256"]:
        receipt.append(dict(path=str(duplicate), retained=str(original), bytes=duplicate.stat().st_size,
            sha256=save["source_sha256"], reason="Temporary battery save matches the original donor."))
        duplicate.unlink()
    first = stage.ROOT.with_name("online_card_copy_20261123")
    earlier = first / "online_card_copy_research.nds"
    earlier_sha = base.load(first / "stored_proof.json")["candidate_sha256"]
    assert base.digest(earlier) == earlier_sha and earlier_sha != candidate
    pinfile = Path("translations/rom_retention_pins.json")
    pins = base.load(pinfile)
    archived_path = str(earlier.resolve())
    if all(row["path"] != archived_path for row in pins):
        pins.append(dict(path=archived_path, reason=f"Preserve the original Online card layout draft {earlier_sha}"))
        base.replace_checked(pinfile, (dumps(pins, ensure_ascii=False, indent=2) + "\n").replace("\n", "\r\n").encode())
    base.save(OUT, dict(candidate_sha256=candidate, removed_duplicate_storage=receipt,
        unique_first_draft=dict(path=str(earlier), sha256=earlier_sha), all_current_verification_artifacts_preserved=True))
    refresh_handoff(registered, drive, receipt)


def refresh_handoff(registered, drive, receipt):
    review = release.PACKAGE.as_posix()
    display = stage.review.OUT.as_posix()
    text = ("# Current editorial checkpoint - 2026-11-23\n\n"
        "The registered Online guide restores ship types, the number of sails, and the Leaning Tower of Pisa. "
        "The five revised holds passed complete text and outline checks. The comparison also verified the previous guide panel, "
        "the title return, and six startup holds. The 17 focused regressions passed. "
        f"[Exact source and display review](../{review}/verification/registered_review.json)\n\n"
        f"Drive contains a single .nds and its readback matches SHA-256 {drive['sha256']}. "
        f"The clean-input patch reconstructs the same ROM byte for byte. Cleanup reclaimed {sum(r['bytes'] for r in receipt):,} "
        f"duplicate bytes. [Latest testing build]({drive['url']}) · [Clean-input patch](../{review}/translation.xdelta) · "
        f"[Cleanup receipt](../{OUT.as_posix()})\n\n"
        f"238 shared entries have scoped dispositions. Continue with the 38 outside those scopes and preserve the direct-caller "
        f"references for all 276. [Display inventory](../{display})\n\n")
    assert registered["clean_input_patch_byte_exact"] and registered["repository_tests"] == 17
    for name in ("editorial_handoff_current.md", "translation_progress.md"):
        path = Path("docs") / name
        base.replace_checked(path, text.encode("utf-8") + path.read_bytes())


if __name__ == "__main__":
    main()
