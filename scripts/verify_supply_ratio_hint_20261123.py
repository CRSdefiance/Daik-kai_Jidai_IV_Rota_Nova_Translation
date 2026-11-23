"""Check the complete Supply Ratio hint and nearby controls in paired native replays."""

import json
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.rom.nds import NdsImage
from scripts.observe_supply_ratio_selector_20261123 import FRAMES
from scripts.reconcile_editorial_acceptance_20261123 import ARM, digest, read, reference
from scripts.stage_supply_ratio_hint_20261123 import ENGLISH, RELEASE, SLOT, SOURCE
from scripts.verify_plaque_release_v247 import find_mask


ROOT = Path(".codex-release-work/supply_ratio_mix_probe_20261123")
OUTPUT = ROOT / "verified_supply_ratio_hint.json"
SHEET = ROOT / "supply_ratio_hint.png"
HOLDS = (4200, 4450, 4700, 4950)
DIFF = (88, 368, 149, 384)


def replay(case, candidate):
    root = ROOT / case
    paths = [root / p for p in ("mix/capture/capture_report.json", "observer/requests.json", "observer/source_contract.json")]
    report, trace, contract = map(read, paths)
    assert report["ROM_sha256"] == digest(report["ROM"]) == candidate
    assert report["cold_boot"] and not report["savestate_loaded"] and not report["callback_errors"]
    assert report["frames"] == FRAMES[-1] and not report["natural_condition_event_verified"]
    fixture, = report["synthetic_condition_fixtures"]
    assert fixture["after_water_food"] == [0, 700] and fixture["all_other4MiB_RAM_exact"]
    assert report["battery_save_preloaded"]["copied_byte_exact_before_cold_boot"]
    assert not trace["errors"] and not trace["source_requests"] and not trace["mismatches"]
    assert trace["all_host_slots_restored_and_core_file_exact"]
    assert trace["source_contract_sha256"] == digest(paths[-1])
    assert trace["observer_sha256"] == digest("scripts/observe_supply_ratio_selector_20261123.py")
    assert contract["core_sha256"] == report["core_DLL_sha256"]
    frames = {row["frame"]: row for row in report["frames_captured"] if row["path"].endswith("_cold_boot.png")}
    assert set(FRAMES) <= frames.keys()
    return report, trace["rows"], frames, {str(p): digest(p) for p in paths}


def picture(row):
    assert digest(row["path"]) == row["PNG_sha256"]
    with Image.open(row["path"]) as image:
        assert image.size == (256, 384)
        return image.convert("RGB")


def main():
    assert not OUTPUT.exists() and not SHEET.exists()
    proof = read(ROOT / "stored_proof.json")
    release = read(RELEASE)
    before = replay("before", proof["predecessor_sha256"])
    after = replay("after", proof["candidate_sha256"])
    assert release["candidate_sha256"] == proof["predecessor_sha256"] and proof["exact_parent_inverse"]
    for key in ("core_DLL_sha256", "core_options", "scripted_input_schedule", "synthetic_condition_fixtures"):
        assert before[0][key] == after[0][key]
    assert before[0]["battery_save_preloaded"]["source_sha256"] == after[0]["battery_save_preloaded"]["source_sha256"]
    old_calls, new_calls = before[1], after[1]
    assert [row["PC"] for row in old_calls] == [0x02060500, 0x020D5404, 0x02086390, 0x020D5404]
    assert all(row["frame"] == 4072 for row in old_calls)
    assert [row["text_hex"] for row in old_calls] == ["", b"Supply Ratio".hex(), SOURCE[:4].hex(), SOURCE[:4].hex()]
    assert new_calls == old_calls[:2] + [row | {"text_hex": ENGLISH[:3].hex()} for row in old_calls[2:]]
    final = NdsImage.open(proof["candidate"]).read_file(ARM)
    assert final[SLOT:SLOT + len(SOURCE)] == ENGLISH
    font = GameAsciiFont.from_arm9(final)

    observed = {}
    images = {}
    for frame in FRAMES:
        old, new = (picture(item[2][frame]) for item in (before, after))
        change = ImageChops.difference(old, new).getbbox()
        assert change == (DIFF if frame in HOLDS else None)
        images[frame] = old, new
        row = {"whole_frame_difference_bounds": change}
        if frame in HOLDS:
            label = find_mask(font, "Mix", new, (87, 366, 151, 384))
            assert label["bounds"] == [131, 371, 149, 382] and label["ink_pixels"] == 49
            back = find_mask(font, "Back", new, (149, 367, 204, 384))
            select = find_mask(font, "Select", new, (198, 367, 256, 384))
            assert back["bounds"] == [171, 371, 195, 382] and select["bounds"] == [217, 371, 253, 382]
            assert back == find_mask(font, "Back", old, (149, 367, 204, 384))
            assert select == find_mask(font, "Select", old, (198, 367, 256, 384))
            row["font_checks"] = [label, back, select]
        observed[frame] = row
    slider = (30, 284, 153, 322)
    frames = {i: images[i][1].crop(slider).tobytes() for i in HOLDS}
    assert frames[4200] == frames[4700] and frames[4450] == frames[4950] and frames[4200] != frames[4450]

    sheet = Image.new("RGB", (560, 780), "#17212a")
    captions = ImageDraw.Draw(sheet)
    for i, title in enumerate(("Registered Sound Setup build", "Staged Supply Ratio fix")):
        x = 16 + i * 272
        captions.text((x, 8), title, fill="white")
        sheet.paste(images[4200][i].crop((0, 192, 256, 384)), (x, 27))
        for j, (frame, label) in enumerate(((3950, "Port Worker asks about the mix"), (4450, "L changes the shares"),
                                          (4700, "R restores the shares"), (5200, "A returns to the stock-up question"))):
            y = 240 + j * 133
            captions.text((x, y), label, fill="white")
            sheet.paste(images[frame][i].crop((0, 272, 256, 384)), (x, y + 15))
    sheet.save(SHEET)

    record = proof["record"] | {"review": proof["record"]["review"] | {"formatting": True}}
    result = dict(candidate_sha256=proof["candidate_sha256"], predecessor_sha256=proof["predecessor_sha256"],
        target_locale="en-US", translation_policy="natural-dialogue-v2", encoder="dialogue-relocatable-v1",
        review_gates=list(record["review"]), records=[record], observed_frames=observed,
        native_source_and_proposal_calls={"before": old_calls, "after": new_calls},
        controls=dict(initial="[50%, 50%]", after_L="[49%, 51%]", after_R="[50%, 50%]",
                      after_second_L="[49%, 51%]", after_A="stock-up question", after_B="mix question"),
        focused_emulator_fixture=True, fixture_changes_label=False, source_storage_staged_and_read_by_native_renderer=True,
        naturally_earned_shortage=False, handheld_verified=False, sheet=reference(SHEET),
        evidence=before[3] | after[3] | {str(ROOT / "stored_proof.json"): digest(ROOT / "stored_proof.json")})
    validate_natural_dialogue_batch(result)
    OUTPUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    print("Verified every letter in Mix, unchanged Back and Select masks, both adjustment directions and the paired return frames.")


if __name__ == "__main__":
    main()
