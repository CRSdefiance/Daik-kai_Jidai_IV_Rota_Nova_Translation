"""Map actual marker-source arguments without reusing frame-caption identities."""

import contextlib
import io
import json
import struct
from pathlib import Path

from capstone import CS_ARCH_ARM, CS_MODE_ARM, Cs
from ndspy.code import MainCodeFile, loadOverlayTable

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts import trace_frame_crop_arguments_v584 as census

ROOT = Path("work/analysis/marker_consumers_v605")
ROM = Path("out/all_routes_combined_v604_candidate.nds")
OWNER = 0x02313F74
TARGETS = {"Sell": (112, 48, 144, 60), "Buy": (112, 60, 144, 72),
           "Temp Storage": (184, 0, 248, 16), "Issued": (168, 64, 216, 80), "Spoils": (168, 80, 216, 96)}


def main():
    ROOT.mkdir(parents=True, exist_ok=True)
    old = census.ROOT, census.ROM, census.OWNER
    try:
        census.ROOT, census.ROM, census.OWNER = ROOT, ROM, OWNER
        with contextlib.redirect_stdout(io.StringIO()):
            census.main()
    finally:
        census.ROOT, census.ROM, census.OWNER = old
    path = ROOT / "crop_argument_census.json"
    d = json.loads(path.read_text(encoding="utf-8"))
    # The reused abstract interpreter enumerates source arguments, but its old
    # frame caption identities do not apply to the marker atlas.
    for case in d["owner_load_cases"]:
        case.pop("intersecting_caption_cells", None)
        if case.get("geometry_statically_resolved"):
            x, y, width, height = case["source_XYWH"]
            case["target_intersections"] = [label for label, (left, top, right, bottom) in TARGETS.items()
                                            if x < right and y < bottom and x + width > left and y + height > top]
    rom = NdsImage.open(ROM)
    arm = rom.read_file("/__arm9__.bin")
    clean = NdsImage.open("work/clean.nds").read_file("/__arm9__.bin")
    assert arm[0x48098:0x48128] == clean[0x48098:0x48128]
    units = [(s.ramAddress, bytes(s.data)) for s in MainCodeFile(arm, 0x02000000).sections]
    units += [(o.ramAddress, bytes(o.data)) for o in loadOverlayTable(
        rom.rom.arm9OverlayTable, lambda _, f: rom.rom.files[f]).values()]
    calls, stored = [], []
    for base, data in units:
        for at in range(len(data) - 3):
            value = struct.unpack_from("<I", data, at)[0]
            if value == 0x02048098:
                stored.append(base + at)
            if at % 4 == 0 and value & 0x0F000000 == 0x0B000000 and census.branch(value, base + at) == 0x02048098:
                calls.append(base + at)
    assert calls == [0x020C20CC, 0x020C2154, 0x020C21DC] and not stored
    # Bind the two direct immediate selector arguments. The third r4 argument
    # has a dominating MOV r4,#0 with no intervening writer in original code.
    assert arm[0xC20C4:0xC20C8] == clean[0xC20C4:0xC20C8] == bytes.fromhex("0210a0e3")
    assert arm[0xC2150:0xC2154] == clean[0xC2150:0xC2154] == bytes.fromhex("0110a0e3")
    assert arm[0xC219C:0xC21E0] == clean[0xC219C:0xC21E0]
    decoder = Cs(CS_ARCH_ARM, CS_MODE_ARM)
    decoder.detail = True
    for ins in decoder.disasm(arm[0xC21A0:0xC21DC], 0x020C21A0):
        assert "r4" not in [ins.reg_name(reg) for reg in ins.regs_access()[1]]
    selectors = [{"call": call, "selector": index, "source_XYWH": [112, index * 16, 32, 16], "current_caption": label}
                 for call, index, label in ((0x020C20CC, 2, "Cargo"), (0x020C2154, 1, "Local"), (0x020C21DC, 0, "Sold"))]
    d.update(target_boxes=TARGETS, literal_owner=OWNER, source_wrapper=0x02048098,
             source_wrapper_code_exact_clean=True, direct_wrapper_calls=selectors,
             all_loaded_sections_and_overlay_stored_wrapper_pointers=[],
             wrapper_source_rows_are_existing_Sold_Local_Cargo_not_price_words=True,
             old_Sold_Local_Cargo_native_evidence="docs/market_transactions_v598_checkpoint.md",
             no_new_native_parent_credit_from_this_static_census=True,
             computed_or_indirect_code_addresses_not_excluded=True,
             reused_interpreter="scripts/trace_frame_crop_arguments_v584.py",
             reused_interpreter_sha256=sha(Path("scripts/trace_frame_crop_arguments_v584.py").read_bytes()),
             script_sha256=sha(Path(__file__).read_bytes()), full_goal_complete=False)
    path.write_text(json.dumps(d, indent=2) + "\n", encoding="utf-8")
    print(f"V605 marker census:{len(d['owner_load_cases'])} PC loads; source wrapper selectors2/1/0 are Cargo/Local/Sold; five other header contexts stay open.")


if __name__ == "__main__":
    main()
