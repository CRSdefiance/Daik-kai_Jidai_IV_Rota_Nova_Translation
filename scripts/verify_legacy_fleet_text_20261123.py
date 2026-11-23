"""Bind the legacy fleet text calls to a current ordinary regional replay."""

import json
from pathlib import Path
from struct import unpack_from

from PIL import Image, ImageDraw

from dk4tool.rom.nds import NdsImage
from scripts.observe_legacy_fleet_text_20261123 import RELEASE, ROOT, TARGETS
from scripts.reconcile_editorial_acceptance_20261123 import ARM, BASE, OUT, digest, read, reference


PREVIOUS = ROOT.with_name("regional_orders") / "regional/capture/capture_report.json"
REPORT = OUT.with_name("legacy_fleet_text_current_20261123.json")
SHEET = REPORT.with_suffix(".png")
SAMPLES = (7000, 15400, 20200)


def main():
    assert not REPORT.exists() and not SHEET.exists()
    folder = ROOT / "regional"
    capture_file = folder / "capture/capture_report.json"
    trace_file = folder / "requests.json"
    contract_file = folder / "source_contract.json"
    release, capture, trace, contract, previous = map(read, (RELEASE, capture_file, trace_file, contract_file, PREVIOUS))
    assert capture["ROM_sha256"] == digest(release["candidate"]) == release["candidate_sha256"]
    assert capture["cold_boot"] and not capture["savestate_loaded"] and not capture["callback_errors"]
    assert not any(value for k, value in capture.items() if k.startswith("synthetic_"))
    assert capture["frames"] == previous["frames"] == 36600
    assert capture["scripted_input_schedule"] == previous["scripted_input_schedule"]
    donor = capture["battery_save_preloaded"]
    assert donor["copied_byte_exact_before_cold_boot"] and digest(donor["source"]) == donor["source_sha256"]

    assert trace["source_contract_sha256"] == digest(contract_file)
    assert contract["ARM9_sha256"] == release["target_ARM9_sha256"]
    assert {row["PC"] for row in contract["targets"]} == TARGETS.keys()
    assert trace["all_host_slots_restored_and_core_file_exact"] and not trace["errors"] and not trace["mismatches"]
    assert trace["callbacks"] == 6
    orders = trace["rows"]
    assert len(orders) == 6 and all(row["owner"] == "regional_order_selection" for row in orders)

    def frames(report):
        return {row["frame"]: row for row in report["frames_captured"] if not row["path"].endswith("_final.png")}

    actual, earlier = map(frames, (capture, previous))
    assert actual.keys() == earlier.keys() and len(actual) == 20
    for frame, row in actual.items():
        assert digest(row["path"]) == row["PNG_sha256"]
        assert row["framebuffer_sha256"] == earlier[frame]["framebuffer_sha256"]

    arm = NdsImage.open(release["candidate"]).read_file(ARM)
    source = NdsImage.open("work/clean.nds").read_file(ARM)
    lo, hi = 0x136824, 0x136860
    assert arm[lo:hi] == source[lo:hi]
    assert unpack_from("<4I", arm, 0x136850) == (0x02036D84, 0x0203707C, 0x02037568, 0x02038358)
    info_record, = unpack_from("<I", arm, 0x136828)
    name, = unpack_from("<I", arm, info_record - BASE + 4)
    class_bytes = b"21CControlableFleetView\0"
    assert arm[name - BASE:name - BASE + len(class_bytes)] == class_bytes
    prior_fields = read(OUT)["native_text_followups"]["open_original_callers"][1:]
    assert [row["source_Japanese"] for row in prior_fields] == ["目標街：%s", "収入額%8lu支出額%8lu投資額%8lu"]
    findings = []
    for row in prior_fields:
        at = row["ARM9_offset"]
        stored = bytes.fromhex(row["clean_and_current_hex"])
        assert arm[at:at + len(stored)] == source[at:at + len(stored)] == stored
        assert TARGETS[BASE + row["call_offset"]].endswith("_format")
        findings.append(row | {"current_replay_calls": 0, "confirmed_in_other_DS_paths": False})

    sheet = Image.new("RGB", (3 * 256 + 40, 427), "#242a34")
    labels = ImageDraw.Draw(sheet)
    for i, number in enumerate(SAMPLES):
        x = 10 + 266 * i
        labels.text((x, 12), f"Regional fleet replay · Frame {number}", fill="white")
        with Image.open(actual[number]["path"]) as screen:
            assert screen.size == (256, 384)
            sheet.paste(screen, (x, 32))
    sheet.save(SHEET)
    evidence = {"candidate_sha256": release["candidate_sha256"], "cold_boot_ordinary_controller_replay": True,
                "copied_save": {"sha256": donor["source_sha256"], "original": donor["source"]},
                "matching_full_frames": sorted(actual), "regional_order_selector_calls": orders,
                "legacy_owner": "CControlableFleetView", "legacy_vtable_span": [lo, hi],
                "legacy_text_records": findings, "sheet": reference(SHEET),
                "evidence": [reference(path) for path in (capture_file, trace_file, contract_file, PREVIOUS)],
                "ordinary_scope": "The reproduced regional controls and six selection dispatches. Other original callers remain open.",
                "registered_ROM_changed": False, "new_editorial_credit": 0}
    REPORT.write_text(json.dumps(evidence, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    print("Ordinary regional replay matches 20 earlier full frames. Both legacy field call counts were zero.")


if __name__ == "__main__":
    main()
