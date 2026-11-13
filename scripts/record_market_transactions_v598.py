"""Archive ordinary Market guide candidates and retain all pending graphics scope."""

import json
import shutil
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha

ROOT = Path("work/analysis/trade_consumers_v598")
DOC = Path("docs/market_transactions_v598_checkpoint.md")
GUIDE = Path("E:/Rota Nova translations/Screenshots/Guide candidates/V598 Market transactions")
ARCHIVE = Path("E:/Rota Nova translations/Screenshots/Audit comparisons/V598 Market headings")
KEY = "ordinary_Market_transactions_and_native_three_heading_crops_v598"


def read(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def save(path, value):
    Path(path).write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def copy_checked(source, target):
    shutil.copyfile(source, target)
    assert sha(Path(source).read_bytes()) == sha(Path(target).read_bytes())


def main():
    proof = ROOT / "ordinary_trade_proof.json"
    p = read(proof)
    scripts = [Path("scripts/verify_market_transactions_v598.py"), Path(__file__)]
    assert p["script_sha256"] == sha(scripts[0].read_bytes())
    assert sha(Path(p["candidate"]).read_bytes()) == p["candidate_sha256"]
    assert sha(Path(p["candidate"]).with_suffix(".xdelta").read_bytes()) == "e6e1097e9caa7577a4c51d9bcc175274eb68e4f8041d86acd05d8ba1f4ad52c7"
    assert sha(Path(p["report"]).read_bytes()) == p["report_sha256"]
    r = read(p["report"])
    shots = {s["frame"]: s for s in r["frames_captured"] if "navigation" in Path(s["path"]).name}
    GUIDE.mkdir(parents=True, exist_ok=True)
    ARCHIVE.mkdir(parents=True, exist_ok=True)
    selected = ((19700, "two_purchases_staged"), (20900, "one_purchase_removed"),
                (21200, "purchase_confirmation"), (21700, "purchase_completed_Market_return"),
                (22000, "purchase_committed"), (22300, "sale_staged"), (22600, "sale_confirmation"),
                (22900, "No_returns_to_Deal"), (23800, "sale_completed_Market_return"), (24100, "sale_committed"))
    screenshots = []
    for frame, label in selected:
        s = shots[frame]
        dest = GUIDE / f"V593_{frame:06d}_{label}.png"
        copy_checked(s["path"], dest)
        screenshots.append({"path": str(dest), "sha256": s["PNG_sha256"], "frame": frame,
                            "context": label, "ordinary_cold_boot_controls_no_synthetic_fixtures": True,
                            "publication_approved": False})
    for target in (GUIDE, ARCHIVE):
        for source in (proof, DOC, Path(p["report"]), Path(p["actual_recorded_inputs"]), *scripts):
            copy_checked(source, target / source.name)
    copy_checked(ROOT / "trade_heading_source_current_review.png", ARCHIVE / "trade_heading_source_current_review.png")
    for target in (GUIDE, ARCHIVE):
        save(target / "provenance.json", {"candidate": p["candidate"], "candidate_sha256": p["candidate_sha256"],
            "ordinary_gameplay_no_save_state_or_synthetic_setup": True, "publication_approved": False,
            "screenshots": screenshots if target == GUIDE else [],
            "files": {path.name: sha(path.read_bytes()) for path in target.iterdir()
                      if path.is_file() and path.name != "provenance.json"}})
    entry = {"documentation": str(DOC), "proof": str(proof), "proof_sha256": sha(proof.read_bytes()),
             "candidate": p["candidate"], "candidate_sha256": p["candidate_sha256"],
             "ordinary_cold_boot_no_save_or_synthetic_fixture": True, "completed_purchase_and_sale": True,
             "displayed_purchase_cost": 572, "displayed_sale_income": 288, "final_reopened_funds": 29716,
             "nine_actual_Deal_states": True, "three_complete_heading_words": ["Sold", "Local", "Cargo"],
             "complete_independent_word_ink_points": 188, "whole_native_heading_crops": 27,
             "whole_heading_pixels": 13824, "complete_HUD_word_number_masks": 72,
             "original_resource_getter_and_actual_stock_getters_from_live_objects": True,
             "No_confirmation_returns_entire98304_pixel_Deal_frame": True,
             "original_texture_not_assumed_recoverable_from_other_lettered_cells": True,
             "separate_Buy_Sell_cells_and_global_material_audit_remain_open": True,
             "guide_candidates": str(GUIDE), "full_unmodified_screenshots": len(screenshots),
             "audit_archive": str(ARCHIVE), "publication_approved": False,
             "production_ROM_or_patch_changed": False, "all18_plaques_remain_incomplete": True,
             "all22_historical_objects_retained": True, "full_goal_complete": False}
    scope = read("work/analysis/confirm_material_v572/audit_scope_before.json")
    for filename, old in scope.items():
        target = Path("translations") / filename
        d = read(target)
        assert d.get("historical_pending_items_retained") == old["historical_pending_items_retained"]
        assert d.get("plaque_style_v247", {}).get("ongoing_plaque_inventory") == old["ongoing_plaque_inventory"]
        d[KEY] = entry
        d["current_goal_turn_classification"] = "progress-ordinary-Market-purchase-sale-confirmations-and-complete-native-three-heading-crops"
        save(target, d)
        v = read(target)
        assert v.get("historical_pending_items_retained") == old["historical_pending_items_retained"]
        assert v.get("plaque_style_v247", {}).get("ongoing_plaque_inventory") == old["ongoing_plaque_inventory"]
    paragraph = """

## V598: ordinary Market purchase/sale and native heading graphics

A fresh24,100-frame New Game run uses ordinary controls, no battery save,
savestate or synthetic fixture. One staged Salt purchase is removed, one572
purchase commits, one288 sale commits, and reentry shows funds29716. No on the
sale confirmation restores the entire98,304-pixel Deal frame. Nine actual states
bind original CTradingView/model getters and all27 complete Sold/Local/Cargo
source crops:13,824 pixels and188 independent word-ink points pass, alongside72
complete HUD word/number masks. Source meanings and the post-sale Sold section
support those compact headings. Native/nearest-neighbor source texture review
does not establish identical unlettered donor cells or close the material audit.
The separate Sell/Buy price cells are not these actual heading rows and retain
their ordinary-parent gap. Ten unmodified ordinary screenshots/provenance are
on E under Guide candidates/V598 Market transactions;publication unapproved.
V593 ROM/patch unchanged;all18 plaques incomplete/all22 objects exact;goal active.
See [V598 ordinary trade checkpoint](market_transactions_v598_checkpoint.md).
"""
    for filename in ("translation_progress.md", "todo.md", "known_issues.md", "release_build.md"):
        target = Path("docs") / filename
        text = target.read_text(encoding="utf-8-sig")
        if "## V598: ordinary Market purchase/sale and native heading graphics" not in text:
            target.write_text(text + paragraph, encoding="utf-8")
    print("Recorded V598: normal purchase/sale,27 full heading crops,72 full HUD masks;10 guide candidates on E;3 audits/4 docs;18/22 exact;V593 unchanged.")


if __name__ == "__main__":
    main()
