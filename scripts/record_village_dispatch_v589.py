"""Record expanded village-card source evidence without closing display gates."""

import json
import shutil
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha

ROOT = Path("work/analysis/village_dispatch_v589")
ARCHIVE = Path("E:/Rota Nova translations/Screenshots/Test fixtures/V589 Village dispatch")
SCRIPT = Path("scripts/trace_village_dispatch_v589.py")
DOC = Path("docs/village_dispatch_v589_checkpoint.md")


def read(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def main():
    proof = ROOT / "dispatch_proof.json"
    p = read(proof)
    assert p["script_sha256"] == sha(SCRIPT.read_bytes())
    assert p["native_operand_decoders"]["current"] == p["native_operand_decoders"]["clean"]
    assert p["native_operand_decoders"]["current"]["all65536_operands"] == {"town": 32768, "event_still": 32768}
    assert sum(len(rows) for rows in p["container_scans"].values()) == 40
    assert p["village_card_indices"] == [168, 169, 170, 171, 206, 207, 208, 209]
    candidate = Path(p["candidate"])
    assert sha(candidate.read_bytes()) == p["candidate_sha256"]
    assert sha(candidate.with_suffix(".xdelta").read_bytes()) == "e411c4f24e4669309f262493320b08708c9f376da2b9bd80631a002d2f34e415"
    ARCHIVE.mkdir(parents=True, exist_ok=True)
    for path in (proof, SCRIPT, Path(__file__), DOC):
        target = ARCHIVE / path.name
        shutil.copyfile(path, target)
        assert sha(path.read_bytes()) == sha(target.read_bytes())
    receipts = {path.name: sha(path.read_bytes()) for path in ARCHIVE.iterdir()
                if path.is_file() and path.name != "provenance.json"}
    (ARCHIVE / "provenance.json").write_text(json.dumps({
        "candidate_sha256": p["candidate_sha256"], "files": receipts,
        "original_code_replay_and_source_census_not_new_emulator_screenshots": True,
        "new_screenshots": 0, "guide_or_publication_approval": False,
        "ordinary_village_trigger_and_global_nonuse_not_proven": True}, indent=2) + "\n", encoding="utf-8")
    entry = {"documentation": str(DOC), "proof": str(proof), "proof_sha256": sha(proof.read_bytes()),
             "script_sha256": p["script_sha256"], "candidate": str(candidate),
             "candidate_sha256": p["candidate_sha256"], "native_operand_cases": 131072,
             "clean_current_container_scans": 40, "village_card_indices": p["village_card_indices"],
             "all_main_overlay_three_target_census": True,
             "alternate_image_command_uses_towngrp_not_evstill": True,
             "no_direct_village_encoding_in_shared_route_event_or_testdata_containers": True,
             "source_exact_worldmap_has16_byte_candidates_not_decoded_as_instructions": True,
             "ordinary_village_and_computed_reader_paths_remain_open": True,
             "no_new_GPU_or_global_unused_claim": True, "archive": str(ARCHIVE),
             "production_ROM_and_patch_changed": False, "new_screenshots": 0,
             "all18_plaques_remain_incomplete": True, "all22_historical_objects_retained": True,
             "full_goal_complete": False}
    snapshot = read("work/analysis/confirm_material_v572/audit_scope_before.json")
    for filename, old in snapshot.items():
        target = Path("translations") / filename
        d = read(target)
        assert d.get("historical_pending_items_retained") == old["historical_pending_items_retained"]
        assert d.get("plaque_style_v247", {}).get("ongoing_plaque_inventory") == old["ongoing_plaque_inventory"]
        d["expanded_village_dispatch_and_container_census_v589"] = entry
        d["current_goal_turn_classification"] = "progress-exhaustive-original-event-operand-decoder-and-omitted-shared-event-testdata-census"
        target.write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        reread = read(target)
        assert reread.get("historical_pending_items_retained") == old["historical_pending_items_retained"]
        assert reread.get("plaque_style_v247", {}).get("ongoing_plaque_inventory") == old["ongoing_plaque_inventory"]
    paragraph = """

## V589: original village-card decoder and omitted containers

131,072 native clean/current operand cases distinguish the event-still index
from the alternate town-image pair; the latter formats towngrp, not evstill.
All-main/overlay ARM/Thumb/pointer census binds the three original parent/loader
targets. Forty source/current container searches add shared, VE and historical
test-data coverage to V427: no village-card command there. Sixteen source-exact
WORLDMAP byte candidates are retained without treating them as decoded triggers.
Correct card IDs are168-171/206-209. This closes a source-search gap, not ordinary
village display, indirect readers or global unused art. Proofs/provenance are on
E under Test fixtures/V589 Village dispatch; no new screenshots or ROM. V581 and
its patch remain unchanged. All18 plaques remain incomplete and all22 historical
objects remain exact. The graphics goal stays active. See
[V589 dispatch checkpoint](village_dispatch_v589_checkpoint.md).
"""
    for filename in ("translation_progress.md", "todo.md", "known_issues.md", "release_build.md"):
        target = Path("docs") / filename
        text = target.read_text(encoding="utf-8-sig")
        if "## V589: original village-card decoder and omitted containers" not in text:
            target.write_text(text + paragraph, encoding="utf-8")
    print("Recorded V589 in3 audits/4 progress docs and E evidence archive;18/22 scope exact;V581 unchanged.")


if __name__ == "__main__":
    main()
