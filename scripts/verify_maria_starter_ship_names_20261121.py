"""Check Maria's active fleet and stock names using the original getters."""

from hashlib import sha256
from pathlib import Path
from types import FunctionType

from dk4tool.dialogue.font_audit import GameAsciiFont
from scripts import stage_maria_starter_ship_names_20261121 as stage
from scripts.stage_special_target_labels_20261115 import c_string
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_specialized_ship_labels_20261115 import get_catalogue, native_sheet


base = stage.base
ROOT = stage.ROOT
PROOF = ROOT / "catalogue_verification.json"
FONT_SHEET = ROOT / "maria_starter_names_native.png"
FRAME = 31000


def snapshot(label, rom, expected_sha, report_path=None):
    path = report_path or ROOT / f"{label}_shipyard/capture_report.json"
    report = base.load(path)
    assert report["ROM_sha256"] == base.digest(rom) == expected_sha
    assert report["cold_boot"] and not report["savestate_loaded"] and not report["callback_errors"]
    assert not any(v for k, v in report.items() if k.startswith("synthetic_"))
    donor = report["battery_save_preloaded"]
    assert donor["copied_byte_exact_before_cold_boot"]
    assert base.digest(donor["source"]) == donor["source_sha256"]
    rows = [r for r in report.get("read_only_capture_RAM_snapshots", []) if r["frame"] == FRAME]
    snap = rows[0] if rows else report["read_only_RAM_snapshot"]
    assert rows or report["frames"] == FRAME
    data = Path(snap["path"]).read_bytes()
    assert snap["read_only_export"] and len(data) == 0x400000
    assert sha256(data).hexdigest() == snap["sha256"]
    arm = base.NdsImage.open(rom).read_file(stage.ARM)
    return arm, get_machine(arm, data), report, {str(path): base.digest(path), snap["path"]: snap["sha256"]}


def check_fleet(machine, models, expected):
    cpu, get = machine
    assert get(0x2E58C) == 3
    fleet = get(0xCB1A8) + 4 + 132 * 3
    root = models[2]
    rows = []
    for i, (model, text) in enumerate(expected.items()):
        slot = fleet + 12 + i * 8
        live = get(0x36C94, slot)
        stock = root + 4 + 140 * model
        assert live == root + 4 + 140 * (0, 4)[i]
        assert get(0x11DB0, live) == get(0x11DB0, stock) == 28
        for address in (live, stock):
            assert c_string(cpu, address + 8, "ascii")["text"] == text
        rows.append(dict(slot=i, stock_model_ID=model, stock_address=stock, active_model_address=live,
                         text=text, class_ID=28, original_slot_hex=bytes(cpu.mem_read(slot, 8)).hex()))
    assert all(get(0x36C94, fleet + 12 + slot * 8) == 0 for slot in range(2, 5))
    return rows


def main():
    assert not PROOF.exists()
    draft = base.load(stage.PROOF)
    roms = (stage.parent.ROM, stage.ROM)
    prior_report = ROOT / "current_opening/capture_report.json"
    staged_report = ROOT / "startup/capture/capture_report.json"
    before, after = [snapshot(label, rom, draft[key], path)
                     for label, rom, key, path in zip(("current", "staged"), roms,
                         ("parent_sha256", "candidate_sha256"), (prior_report, staged_report), strict=True)]
    assert before[2]["battery_save_preloaded"]["source_sha256"] == after[2]["battery_save_preloaded"]["source_sha256"]
    old, new = [get_catalogue(machine, arm) for arm, machine, _, _ in (before, after)]
    assert old[0] == new[0] and old[2] == new[2]
    old_fleet, new_fleet = [check_fleet(run[1], models, {
        r["model_ID"]: r[key] for r in draft["records"]})
        for run, models, key in zip((before, after), (old, new), ("previous_English", "english"), strict=True)]
    assert old_fleet == [b | {"text": a["text"]} for a, b in zip(old_fleet, new_fleet, strict=True)]
    changed = [i for i, (a, b) in enumerate(zip(old[1], new[1], strict=True)) if a != b]
    assert changed == [0, 4, 147, 148]
    expected_names = {}
    for model_slot, row in zip((0, 4), new_fleet, strict=True):
        expected_names[model_slot] = row['text']
        expected_names[row['stock_model_ID']] = row['text']
    for i in changed:
        a, b = old[1][i], new[1][i]
        assert a[:8] == b[:8] and a[27:] == b[27:]
        expected = expected_names[i]
        assert b[8:27] == expected.encode("ascii").ljust(19, b"\0")
    formatter = GameAsciiFont.from_arm9(after[0])
    assert all(formatter.decode(c).getbbox() for row in new_fleet for c in row["text"])
    render = FunctionType(native_sheet.__code__, native_sheet.__globals__ | {"SHEET": FONT_SHEET})
    previews = render(after[0], draft["records"])
    base.save(PROOF, dict(
        candidate_sha256=draft["candidate_sha256"], parent_sha256=draft["parent_sha256"],
        catalogue_classes=39, initialized_models=155, changed_model_name_fields=changed,
        previous_fleet=old_fleet, staged_fleet=new_fleet, previews=previews,
        evidence=before[3] | after[3], sheets={str(FONT_SHEET): base.digest(FONT_SHEET)},
        ordinary_opening=True, prepared_system_unlock=True, natural_unlock=False, hardware=False,
    ))
    print("Verified both starter ship names through the original getters and all 155 initialized model records.")


if __name__ == "__main__":
    main()
