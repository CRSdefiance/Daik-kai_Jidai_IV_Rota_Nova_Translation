"""Reconcile all literal frame-owner paths without claiming global non-use."""

import json
import struct
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.probe_button_prompt_native import call, machine

ROOT = Path("work/analysis/frame_callers_v584")
OWNER = 0x02313F60
CELLS = [(208, 32, 256, 40), (208, 40, 240, 48), (240, 40, 256, 48),
         (184, 48, 208, 56), (208, 48, 256, 56)]


def read(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def main():
    rom, clean = (NdsImage.open(p) for p in ("out/all_routes_combined_v581_candidate.nds", "work/clean.nds"))
    digest = sha(rom.source.read_bytes())
    u, original = (machine(r.read_file("/__arm9__.bin")) for r in (rom, clean))
    census = read(ROOT / "crop_argument_census.json")
    rows = read(ROOT / "original_source_row_proof.json")
    styles = read(ROOT / "native_all_style_tiles_proof.json")
    pixels = read(ROOT / "native_blitter_contract_proof.json")
    assert all(digest == p["candidate_sha256"] for p in (census, rows, styles, pixels))
    cases = census["owner_load_cases"]
    assert len(cases) == 48
    views = [c for c in cases if c["kind"] in ("view_setter", "view_constructor")]
    assert len(views) == 38
    source_rows = {r["constructor_call"]: r for r in rows["six_original_row_definitions"]}
    for view in views:
        if view["geometry_statically_resolved"]:
            assert not view["intersecting_caption_cells"]
        else:
            y = view["source_XYWH"][1]
            if y is None:
                y = source_rows[view["call"]]["source_row"]
            assert 56 <= y < 256
    assert len(styles["native_style_cases"]) == 84
    assert sum(len(r["native_cases"]) for r in styles["native_style_cases"]) == 168
    tile_calls = [d for r in styles["native_style_cases"] for c in r["native_cases"] for d in c["native_source_tile_calls"]]
    assert len(tile_calls) == 852 and not any(d["intersecting_caption_cells"] for d in tile_calls)
    assert len(pixels["cases"]) == 18 and len(pixels["non_tiled_corner_cases"]) == 4
    fixed = []

    def fixed_case(owner_load, region, pointers):
        lo, hi = region
        code = bytes(u.mem_read(lo, hi - lo))
        assert code == bytes(original.mem_read(lo, hi - lo))
        tiles = []
        for address, count in pointers:
            data = bytes(u.mem_read(address, count * 4))
            assert data == bytes(original.mem_read(address, count * 4))
            values = struct.unpack(f"<{count}I", data)
            if count == 5:
                values = values[1:]
            x, y, width, height = values
            assert width and height and x + width <= 256 and y + height <= 256
            assert not any(x < r and y < b and x + width > l and y + height > t for l, t, r, b in CELLS)
            tiles.append({"address": address, "source_XYWH": list(values), "exact_clean": True})
        fixed.append({"owner_load": owner_load, "region": region, "region_sha256": sha(code),
                      "code_and_source_constants_exact_clean": True, "source_tiles": tiles,
                      "static_source_binding_not_ordinary_live_parent": True})

    fixed_case(0x020D2E20, (0x020D2DB0, 0x020D2E70), [(0x021278E0, 4)])
    fixed_case(0x020FAE08, (0x020FADE4, 0x020FAED0),
               [(0x0212EED8, 4), (0x0212EE4C, 4), (0x0212EEF0, 4)])
    pointers = struct.unpack("<4I", u.mem_read(0x0216B19C, 16))
    assert bytes(u.mem_read(0x0216B19C, 16)) == bytes(original.mem_read(0x0216B19C, 16))
    fixed_case(0x020FB160, (0x020FB124, 0x020FB198), [(p, 5) for p in pointers])
    # The remaining text-field helper copies source XY from three pairs, with
    # the separately declared 8x20 source dimensions (not following pair words).
    lo, hi = 0x020FB324, 0x020FB4B8
    assert bytes(u.mem_read(lo, hi - lo)) == bytes(original.mem_read(lo, hi - lo))
    size = struct.unpack("<2I", u.mem_read(0x0212EC6C, 8))
    assert size == (8, 20) and bytes(u.mem_read(0x0212EC6C, 8)) == bytes(original.mem_read(0x0212EC6C, 8))
    xy = [struct.unpack("<2I", u.mem_read(p, 8)) for p in (0x0212EEC0, 0x0212EEC8, 0x0212EED0)]
    assert xy == [(104, 56), (112, 56), (184, 56)]
    assert all(y >= 56 for _, y in xy)
    fixed.append({"owner_load": 0x020FB348, "region": [lo, hi], "code_exact_clean": True,
                  "source_XY_pairs": xy, "separate_source_size": size,
                  "source_rows_outside_caption_band": True, "static_not_ordinary_live_parent": True})
    getters = [c["owner_load"] for c in cases if c["kind"] == "resource_getter"]
    assert set(getters) == {0x020D0AD0, 0x020D0E70, 0x020D1208, 0x020D1370,
                            *(r["owner_load"] for r in fixed)}
    initialization = [c["owner_load"] for c in cases if c["kind"] == "initialization_or_unresolved_control_transfer"]
    assert initialization == [0x0210E1AC, 0x0210E1C4]
    call(u, 0x10E190, ())
    filename_pointer = int.from_bytes(u.mem_read(OWNER + 12, 4), "little")
    assert bytes(u.mem_read(filename_pointer, 64)).split(b"\0")[0] == b"_pxl/__frame.pxl"
    assert sha(rom.source.read_bytes()) == digest
    snapshot = read("work/analysis/confirm_material_v572/audit_scope_before.json")
    for filename, saved in snapshot.items():
        d = read(Path("translations") / filename)
        assert d.get("historical_pending_items_retained") == saved["historical_pending_items_retained"]
        assert d.get("plaque_style_v247", {}).get("ongoing_plaque_inventory") == saved["ongoing_plaque_inventory"]
    proof_files = ["crop_argument_census.json", "original_source_row_proof.json", "literal_style_callers.json",
                   "native_all_style_tiles_proof.json", "native_blitter_contract_proof.json"]
    result = {"candidate": str(rom.source), "candidate_sha256": digest,
              "owner": OWNER, "original_initializer_filename_verified": "_pxl/__frame.pxl",
              "literal_owner_loads_reconciled": 48, "view_sites_outside_five_caption_cells": 38,
              "view_row_alias_and_call_ABI_assumptions_retained": True,
              "fixed_style_call_sites": 84, "native_style_wrapper_cases": 168,
              "native_source_tile_calls": 852, "all_literal_style_tiles_outside_five_cells": True,
              "fixed_other_resource_getter_bindings": fixed, "initializer_load_sites": initialization,
              "native_pixel_contract_cases": 22,
              "proofs": {name: sha((ROOT / name).read_bytes()) for name in proof_files},
              "corrected_contract": "Tiled: r3 source XYWH; stack0 destination LTRB. Corner: r3 source XY, stack0 size, stack4 destination XY.",
              "zero_dimension_tiled_fill_is_a_source_pixel_not_an_unused_record": True,
              "ordinary_five_caption_and_Confirm_contexts_remain_open": True,
              "computed_owner_aliases_indirect_calls_and_embedded_copy_consumers_not_excluded": True,
              "no_new_ordinary_UI_or_DeSmuME_display_credit": True,
              "all18_plaques_incomplete_and22_historical_objects_exact": True,
              "ROM_and_patch_changed": False, "full_goal_complete": False}
    (ROOT / "frame_caller_reconciliation.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print("V584:48 owner loads reconciled;38 view sites,84 style sites/852 native tile calls and4 fixed getter bindings outside the miniature cells;22 pixel-contract cases pass.")


if __name__ == "__main__":
    main()
