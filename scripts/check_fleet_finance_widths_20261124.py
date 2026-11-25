"""Check unequal amounts and maximum digits on the legacy Fleet Info Report."""

import json
import sys
from argparse import ArgumentParser
from io import StringIO
from pathlib import Path
from types import FunctionType

from PIL import ImageChops

from dk4tool.dialogue.font_audit import GameAsciiFont
from scripts import headless_desmume_v193 as harness
from scripts import native_regional_finance_v617 as fixture
from scripts import register_assigned_fleet_info_20261123 as assigned
from scripts import register_nagasaki_contract_wrap_20261124 as current
from scripts.stage_cartridge_title_20261123 import CLEAN, REGISTRY, NdsImage, digest, read, reference, sha256, write
from scripts.verify_captain_biographies_v1 import captured
from scripts.verify_confirmed_name_widget_pixels_v198 import complete_mask
from scripts.verify_plaque_release_v247 import find_mask


ROOT = Path(".codex-release-work/shared_display_20261123/fleet_finance_widths_20261124")
REFERENCE = Path("E:/Rota Nova translations/Generated/work/fleet_info_packed_report_replay/capture/capture_report.json")
OUT = assigned.OUT.with_name("fleet_finance_widths_20261124.json")
FIRST_PAUSE, REPORT, END = 12200, 12400, 12800
FRAMES = (11800, 12000, FIRST_PAUSE, REPORT, 12600, END)
ROWS = (("Income", "income"), ("Expenses", "expenses"), ("Invested", "invested"))
INK = (230, 230, 230)


def context():
    latest, earlier, original = map(read, (current.RELEASE, assigned.OUT, REFERENCE))
    previous = earlier["trials"]["packed_report"]
    assert reference(REFERENCE) in previous["evidence"] and original["ROM_sha256"] == previous["rom"]["sha256"]
    assert original["cold_boot"] and not original["savestate_loaded"] and not original["callback_errors"]
    assert not any(v for key, v in original.items() if key.startswith("synthetic_"))
    donor = original["battery_save_preloaded"]
    assert donor["copied_byte_exact_before_cold_boot"] and digest(donor["source"]) == donor["source_sha256"]
    assert digest(REGISTRY) == latest["registry_sha256"] and digest(CLEAN) == latest["clean_input_sha256"]
    assert digest(current.ROM) == latest["candidate_sha256"]
    arm = NdsImage.open(current.ROM).read_file(current.ARM)
    assert sha256(arm).hexdigest() == latest["target_ARM9_sha256"]
    return latest, original, donor, arm


def observe():
    latest, original, donor, _ = context()
    assert original["scripted_input_schedule"][-3:] == [dict(start=n + 1, duration=8, buttons=[key])
        for n, key in ((FIRST_PAUSE, "A"), (REPORT, "B"), (12600, "B"))]
    ROOT.mkdir(parents=True)
    inputs = ROOT / "inputs.json"
    write(inputs, [row for row in original["scripted_input_schedule"] if row["start"] <= FIRST_PAUSE])
    commands = [dict(until=REPORT, buttons=["A"], duration=8, regional_finance_display=fixture.VALUES),
                dict(until=12600, buttons=["B"], duration=8), dict(until=END, buttons=["B"], duration=8), dict(stop=True)]
    original_populate, original_argv, original_stdin = fixture.populate, sys.argv, sys.stdin
    fixture.populate = FunctionType(original_populate.__code__, vars(fixture) | {"ARM": latest["target_ARM9_sha256"]})
    try:
        sys.argv = [__file__, "--rom", str(current.ROM), "--out", str(ROOT / "capture"), "--frames", str(END + 1),
            "--inputs-json", str(inputs), "--press-start", "-1", "--touchscreen", "--battery-save", donor["source"],
            "--capture-every", "999999", "--capture-at", *map(str, FRAMES), "--pause-at", str(FIRST_PAUSE),
            "--allow-regional-finance-fixtures"]
        sys.stdin = StringIO("\n".join(map(json.dumps, commands)) + "\n")
        harness.main()
    finally:
        fixture.populate, sys.argv, sys.stdin = original_populate, original_argv, original_stdin


def verify():
    latest, original, donor, arm = context()
    path = ROOT / "capture/capture_report.json"
    report = read(path)
    assert report["ROM_sha256"] == latest["candidate_sha256"] and report["frames"] == END
    assert report["cold_boot"] and not report["savestate_loaded"] and not report["callback_errors"]
    assert report["scripted_input_schedule"] == original["scripted_input_schedule"]
    assert report["battery_save_preloaded"]["source_sha256"] == donor["source_sha256"]
    evidence_key = "synthetic_regional_financial_display_fixtures"
    assert not any(v for key, v in report.items() if key.startswith("synthetic_") and key != evidence_key)
    edit, = report[evidence_key]
    assert edit["frame"] == FIRST_PAUSE and edit["only_three_declared_finance_words_changed"] and edit["fleet_index"] == 57
    assert edit["display_values"] == fixture.VALUES and set(edit["before_values"].values()) == {0}
    a, b = [{r["frame"]: r for r in run["frames_captured"] if r["path"].endswith("_navigation.png") or
             r["path"].endswith("_cold_boot.png")} for run in (original, report)]
    for frame in set(FRAMES) - {REPORT}:
        assert a[frame]["framebuffer_sha256"] == b[frame]["framebuffer_sha256"], frame
    font = GameAsciiFont.from_arm9(arm)
    old, new, detail = [captured(shot) for shot in (a[REPORT], b[REPORT], b[12000])]
    destination = find_mask(font, "To: Stockholm", detail, (78, 242, 237, 260))
    masks, permitted = [], set()
    for i, (label, field) in enumerate(ROWS):
        text, y = str(fixture.VALUES[field]), 269 + i * 14
        label_ink, label_box = complete_mask(font, label, new, 86, y, INK)
        amount_ink, amount_box = complete_mask(font, f"{text:>10}", new, 140, y, INK)
        assert label_box[2] <= amount_box[0] < amount_box[2] == 200
        masks.append(dict(label=label, amount=int(text), label_ink=label_ink, amount_ink=amount_ink,
                          label_box=label_box, right_aligned_amount_box=amount_box))
        permitted.update((x, row) for x in range(140, 200) for row in range(y, y + 11))
    assert ImageChops.difference(old, new).getbbox()
    assert all((x, y) in permitted for y in range(new.height) for x in range(new.width)
               if old.getpixel((x, y)) != new.getpixel((x, y)))
    sheet = OUT.with_suffix(".png")
    new.save(sheet)
    notes = ("The Report uses the original verified Manuel Fleet assignment and controller schedule. Only three finance words were supplied. "
             "The nine- and ten-digit cases verify the actual legacy report's layout. Earned income, expenses and investment remain unobserved here.")
    write(OUT, dict(candidate_sha256=latest["candidate_sha256"], fixture=edit, verified_destination=destination,
        unchanged_comparison_frames=sorted(set(FRAMES) - {REPORT}), glyph_masks=masks, latest_report=reference(path),
        earlier_zero_amount_report=reference(REFERENCE), visual=reference(sheet), evidence_kind="focused emulator fixture",
        fixture_scope=notes, new_editorial_credit=0, ROM_changed=False))
    print("Verified all three nine- and ten-digit amounts, complete report labels, and both exact return transitions.")


if __name__ == "__main__":
    cli = ArgumentParser(description=__doc__)
    cli.add_argument("--verify", action="store_true")
    (verify if cli.parse_args().verify else observe)()
