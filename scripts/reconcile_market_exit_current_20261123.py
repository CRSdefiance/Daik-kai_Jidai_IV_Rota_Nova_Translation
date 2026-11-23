"""Bind the current Trade exit flow to the clean source and its archived leads."""

from pathlib import Path
from struct import unpack_from

from PIL import Image, ImageChops, ImageDraw

from dk4tool.dialogue.font_audit import GameAsciiFont
from scripts import checkpoint_market_shared_consumers_20261114 as old
from scripts import observe_market_exit_current_20261123 as live
from scripts.reconcile_ds_save_space_20261123 import OUT as PREVIOUS
from scripts.reconcile_legacy_setup_and_recruitment_20261123 import registered_review
from scripts.reconcile_legacy_fleet_and_quit_paths_20261123 import (
    WORKLIST, base, current, native, common_message_entries, owned_entries, picture, reference, stored_record,
    DIRECTORY_OFFSET, TABLE_OFFSET,
)


OUT = PREVIOUS.with_name("market_exit_current_20261123.json")
SHEET = OUT.with_suffix(".png")
STORY_CHECK = old.OUTPUT.with_name("retail_story_archive_selection_20261121_v1.json")
MARKET_REVIEW = Path("releases/all_routes_editorial_20261120_market_bargaining_candidate")
FINDINGS = {
    750: "The tested direct Back action discards the pending trade. Finish uses a separate agreement question.",
    751: "Declining the DS Finish confirmation returns to the same pending deal without a trader reply.",
    752: "Accepting the pending deal triggers the verified trader farewell. Back and No do not select an irritated reply.",
}


def trace_case(case, ids, release, precedent):
    folder = live.ROOT / case
    terminal_path, trace_path, report_path, contract_path = (folder / name for name in (
        "terminal.json", "requests.json", "capture/capture_report.json", "source_contract.json"))
    terminal, trace, report, contract = map(base.load, (terminal_path, trace_path, report_path, contract_path))
    events, frames, end, _, donor = live.earlier.schedule(case)
    assert report["ROM_sha256"] == terminal["ROM_sha256"] == release["candidate_sha256"]
    assert report["frames"] == terminal["completed_frames"] == end
    assert report["scripted_input_schedule"] == events and report["exact_requested_capture_frames"] == frames
    assert report["cold_boot"] and not report["savestate_loaded"] and not report["callback_errors"]
    assert not any(v for k, v in report.items() if k.startswith("synthetic_"))
    preload = report["battery_save_preloaded"]
    assert preload["copied_byte_exact_before_cold_boot"] and preload["source_sha256"] == donor["source_sha256"]
    assert base.digest(donor["source"]) == donor["source_sha256"]
    assert trace["all_host_slots_restored_and_core_file_exact"] and not trace["errors"] and not trace["mismatches"]
    assert base.digest(contract_path) == trace["source_contract_sha256"] and contract["ARM9_sha256"] == release["target_ARM9_sha256"]
    assert all(base.digest(path) == digest for path, digest in terminal["evidence"].items())
    calls = trace["source_requests"]
    assert calls == terminal["target_COMMON_calls"] and len(calls) == terminal["COMMON_requests"] == 2 * len(ids)
    for key, got, copied in zip(ids, calls[::2], calls[1::2], strict=True):
        assert (got["message_ID"], got["PC"]) == (key, 0x0205528C)
        assert copied == got | {"PC": 0x020534F4}
        assert got["caller_LR"] == (0x02053D10 if key == 14 else 0x02053FF8)
    older = precedent["observation"][case]
    assert [{k: v for k, v in r.items() if k != "frame"} for r in calls] == [
        {k: v for k, v in r.items() if k != "frame"} for r in older]
    holds = {r["frame"]: r for r in report["frames_captured"] if r["path"].endswith("_cold_boot.png")}
    assert set(frames) <= holds.keys()
    return calls, holds, {str(p): base.digest(p) for p in (terminal_path, trace_path, report_path, contract_path)}


def alternate_header(clean, active):
    row = base.load(STORY_CHECK)["alternate_Maria_length_word"]
    path, index = row["file"], row["block"]
    data = [native.IlnkContainer.parse(rom.read_file(path)).blocks[index] for rom in (clean, active)]
    assert data[0] == data[1] and native.digest(data[0]) == row["block_sha256"]
    assert data[0][:4] == b"CS\x01\x01" and unpack_from("<I", data[0], row["offset"])[0] == len(data[0]) - 10 == 750
    return row


def reviewed_holds(cases, rows, arm):
    samples = (("back", 11881, "Back returns to Market"), ("finish", 11881, "Finish asks for agreement"),
               ("finish", 12281, "No returns to the pending deal"), ("confirm", 11600, "Trade Goods Info and price"),
               ("confirm", 12281, "Yes completes the deal"), ("confirm", 12681, "Market after the purchase"))
    captures = {(case, frame): cases[case][frame] for case, frame, _ in samples}
    images = {key: picture(value) for key, value in captures.items()}
    font = GameAsciiFont.from_arm9(arm)
    bodies = []
    for case, frame, key in (("finish", 11881, 14), ("confirm", 12281, 9)):
        n = old.font_mask(images[case, frame], font, rows[key]["current_English"], 22, 297,
            (16, 296, 232, 348), (0, 8, 0))
        assert n > 0
        bodies.append(dict(message_ID=key, complete_glyph_mask_pixels=n, capture=captures[case, frame]))
    before = picture(cases["back"][9600]).crop((86, 345, 130, 356))
    cancelled = images["back", 11881].crop((86, 345, 130, 356))
    purchased = images["confirm", 12681].crop((86, 345, 130, 356))
    assert before.tobytes() == cancelled.tobytes() and before.tobytes() != purchased.tobytes()
    no_diff = ImageChops.difference(picture(cases["finish"][11600]), images["finish", 12281]).getbbox()
    assert no_diff == (82, 230, 110, 258)
    sheet = Image.new("RGB", (768, 808), "#142530")
    draw = ImageDraw.Draw(sheet)
    for i, (case, frame, label) in enumerate(samples):
        x, y = i % 3 * 256, i // 3 * 404
        draw.text((x + 5, y + 3), label, fill="white")
        sheet.paste(images[case, frame], (x, y + 19))
    sheet.save(SHEET)
    return bodies, {f"{k[0]}_{k[1]}": v for k, v in captures.items()}, no_diff


def main():
    release, review, previous, inventory, precedent = map(base.load, (current.RELEASE, current.REVIEW, PREVIOUS, WORKLIST, old.OUTPUT))
    ours = release["candidate_sha256"]
    assert base.digest(current.ROM) == ours == review["candidate_sha256"] == previous["candidate_sha256"]
    assert base.digest(native.CLEAN) == release["clean_input_sha256"] == precedent["clean_sha256"]
    assert base.digest(base.REGISTRY) == release["registry_sha256"]
    clean, active = map(base.NdsImage.open, (native.CLEAN, current.ROM))
    ja, en = (rom.read_file(current.ARM) for rom in (clean, active))
    common = active.read_file(current.COMMON)
    assert native.digest(en) == release["target_ARM9_sha256"] and native.digest(common) == release["target_COMMON_sha256"]
    source = common_message_entries(clean.read_file(current.COMMON), ja)
    installed = owned_entries(common, en, native.digest(en[DIRECTORY_OFFSET:TABLE_OFFSET]))
    worklist = {r["message_ID"]: r for r in inventory["records"]}
    binding = {r["message_ID"]: r for r in review["shared_consumer_binding"]["records"]}
    reviewed, market_review_path = registered_review(MARKET_REVIEW)
    decisions = {r["message_ID"]: r for r in reviewed["records"]}
    rows, roots, calls, evidence = {}, {}, {}, {}
    for prior in precedent["retained"]:
        key = prior["message_ID"]
        assert prior["clean_reference"] == reference(source[key]) and prior["clean_hex"] == source[key].text.hex()
        decision = decisions[key]
        assert decision["source_reference"] == prior["clean_reference"] and all(decision["review"].values())
        assert decision["source_hex"] == prior["clean_hex"] and decision["english"].encode("ascii") == installed[key].text
        rows[key] = {name: value for name, value in prior.items() if name != "display"} | dict(
            previous_observed_English=prior["current_English"], previous_display_observation=prior["display"],
            previous_observed_hex=prior["current_hex"], current_English=decision["english"],
            current_hex=installed[key].text.hex(), current_reference=reference(installed[key]),
            installed_reference=reference(installed[key]), decision="justified retention",
            rationale=decision["localization_note"], review=decision["review"])
    for case, ids in old.PATHS.items():
        calls[case], roots[case], files = trace_case(case, ids, release, precedent)
        evidence.update(files)
    legacy = [stored_record(key, source, installed, worklist, binding) | {"verified_scoped_path": note}
              for key, note in FINDINGS.items()]
    for row, former in zip(legacy, precedent["pending"], strict=True):
        assert row["message_ID"] == former["message_ID"]
        assert row["source_hex"] == former["clean_hex"] and row["installed_hex"] == former["current_hex"]
    remaining = set(previous["remaining_without_scoped_disposition"])
    assert len(remaining) == 7 and FINDINGS.keys() <= remaining
    holds, captures, no_diff = reviewed_holds(roots, rows, en)
    base.save(OUT, dict(candidate_sha256=ours, reviewed_entries=legacy, retained_active_copy=list(rows.values()),
        remaining_without_scoped_disposition=sorted(remaining - FINDINGS.keys()), actual_ordinary_replays=calls,
        exact_installed_alternate_archive_length=alternate_header(clean, active), full_glyph_masks=holds,
        state_and_panel_captures=captures, declined_deal_frame_difference=no_diff, hardware=False, new_ROM=False,
        sheet=dict(path=str(SHEET), sha256=base.digest(SHEET)), evidence=evidence | {str(p): base.digest(p) for p in (
            PREVIOUS, old.OUTPUT, WORKLIST, STORY_CHECK, market_review_path, current.RELEASE, current.REVIEW,
            Path(live.__file__), Path(__file__))}))
    print(f"Verified three ordinary Trade exits, two complete dialogue masks, and {len(remaining) - len(FINDINGS)} remaining entries.")


if __name__ == "__main__":
    main()
