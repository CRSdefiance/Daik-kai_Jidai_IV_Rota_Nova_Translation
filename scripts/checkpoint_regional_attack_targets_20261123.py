"""Record the current Syracuse rejection and clear duplicate replay saves."""

from pathlib import Path
from shutil import copyfile

from scripts import observe_regional_attack_targets_20261123 as play
from scripts import verify_current_regional_orders_20261123 as shared


base = shared.base
ROOT = shared.OUTPUT.parent
OUT = ROOT / "regional_attack_syracuse_20261123.json"
CAPTURE = OUT.with_suffix(".png")
CLEANUP = OUT.with_name("regional_order_cleanup_20261123.json")


def remaining_selector_sites(clean_arm, active_arm):
    book = ROOT.parent / "SharedText_20261110_v1"
    fields = {
        "shared_table_callers_20261115_v2.json": "remaining_prior_site_inventory",
        "shared_message_producers_20261115_v1.json": "resolved_call_sites",
        "shared_selector_ranges_20261115_v1.json": "known_stock_inputs_resolved",
    }
    evidence = {str(book / name): base.digest(book / name) for name in fields}
    table, producers, selectors = [set(base.load(book / name)[field]) for name, field in fields.items()]
    remaining = sorted(table - producers - selectors)
    assert len(remaining) == 43
    current = []
    for site in remaining:
        offset = site - shared.BASE
        old, new = [arm[offset-12:offset+4].hex() for arm in (clean_arm, active_arm)]
        current.append(dict(address=site, clean_local_hex=old, current_local_hex=new, local_code_exact=old == new))
    return dict(sites=current, evidence=evidence, scope="Remaining addresses in the earlier bounded call inventory.")


def read_scope():
    release = base.load(shared.current.RELEASE)
    report = base.load(shared.OUTPUT)
    assert base.digest(shared.current.ROM) == report["candidate_sha256"] == release["candidate_sha256"]
    assert base.digest(base.REGISTRY) == release["registry_sha256"]
    terminal, trace, frames = shared.playback.verify_report(play, "targets", release)
    assert terminal["COMMON_requests"] == len(trace) == 6
    for key, a, b in zip((131, 133, 131), trace[::2], trace[1::2], strict=True):
        assert a["message_ID"] == key and a["PC"] == 0x0205528C and b == a | {"PC": 0x020534F4}
    assert trace[2]["frame"] == 10213 < 10600
    row, = [row for row in report["records"] if row["message_ID"] == 133]
    current_rom = base.NdsImage.open(shared.current.ROM)
    current_arm = current_rom.read_file(shared.current.ARM)
    clean_arm = base.NdsImage.open(shared.current.stage.CLEAN).read_file(shared.current.ARM)
    font = shared.playback.GameAsciiFont.from_arm9(current_arm)
    shot = frames[10600]
    ink = shared.full_dialog(shared.playback.screen(shot), font, [line.strip() for line in row["native_layout"]])
    if not CAPTURE.exists():
        copyfile(shot["path"], CAPTURE)
    assert base.digest(CAPTURE) == shot["PNG_sha256"]
    base.save(OUT, dict(candidate_sha256=release["candidate_sha256"], source_text_reference=row["source_reference"],
        installed_text_reference=row["installed_reference"], source_hex=row["source_hex"], current_hex=row["current_hex"],
        clean_Japanese=row["clean_Japanese"], english=row["english"], decision=row["decision"], review=row["review"],
        context="Regional Attack Town on the area map. Syracuse has existing contracts with other factions.",
        localization_note=row["localization_note"], city_from_visible_header="Syracuse", complete_ink=ink,
        original_paired_requests=trace, screenshot=dict(path=str(CAPTURE), sha256=shot["PNG_sha256"]),
        original_inputs=True, earlier_formed_regional_fleet_save=True, current_RAM_fixture=False, hardware=False,
        prior_bounded_selector_worklist=remaining_selector_sites(clean_arm, current_arm),
        evidence=terminal["evidence"] | {str(shared.OUTPUT): base.digest(shared.OUTPUT)}))


def cleanup():
    current = base.load(OUT)
    archive = Path(shared.play.ROOT).parent
    first = archive / "regional_attack_targets/targets"
    folders = (shared.play.ROOT / "regional", first, play.ROOT / "targets")
    entries, previews = [], []
    for folder in folders:
        report = folder / "capture/capture_report.json"
        item = base.load(report)
        assert item["ROM_sha256"] == current["candidate_sha256"]
        donor = item["battery_save_preloaded"]
        source, duplicate = (Path(donor[key]) for key in ("source", "destination"))
        target_folder = (folder / "capture/saves").resolve()
        assert duplicate.resolve().parent == target_folder and not duplicate.is_symlink()
        assert source.resolve() != duplicate.resolve() and base.digest(source) == donor["source_sha256"]
        if duplicate.is_file() and base.digest(duplicate) == donor["source_sha256"]:
            assert duplicate.stat().st_size == source.stat().st_size
            duplicate.unlink()
            entries.append(dict(path=str(duplicate), retained=str(source), sha256=donor["source_sha256"], bytes=donor["bytes"]))
        for name in ("inspection.png", "inspection_0.png", "inspection_1.png"):
            preview = folder / name
            if not preview.is_file():
                continue
            assert preview.resolve().parent == folder.resolve() and not preview.is_symlink()
            assert all(base.digest(shot["path"]) == shot["PNG_sha256"] for shot in item["frames_captured"])
            previews.append(dict(path=str(preview), sha256=base.digest(preview), bytes=preview.stat().st_size))
            preview.unlink()
    base.save(CLEANUP, dict(candidate_sha256=current["candidate_sha256"], exact_duplicate_saves_removed=entries,
        temporary_contact_sheets=previews, bytes_removed=sum(entry["bytes"] for entry in entries + previews)))


if __name__ == "__main__":
    if not OUT.exists():
        read_scope()
    if not CLEANUP.exists():
        cleanup()
