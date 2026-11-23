"""Match the revised trade confirmation and ordinary No and Yes transitions."""

from pathlib import Path

from PIL import Image, ImageChops, ImageDraw

from dk4tool.dialogue.font_audit import GameAsciiFont
from scripts import replay_market_bargaining_20261120 as replay
from scripts import stage_market_bargaining_20261120 as stage
from scripts.checkpoint_market_shared_consumers_20261114 import font_mask
from scripts.verify_captain_biographies_v1 import captured, shots


base, ROOT = stage.base, stage.ROOT
PROOF, SHEET = ROOT / "gameplay_verification.json", ROOT / "lisbon_trade_comparison.png"
HOLD, FAREWELL = (11881, 12681), 13081
BOX = (16, 296, 232, 348)


def main():
    assert not PROOF.exists() and not SHEET.exists()
    stored = base.load(stage.STORED)
    paths = [ROOT / f"ordinary_{side}/capture/capture_report.json" for side in ("parent", "revised")]
    reports = [base.load(path) for path in paths]
    assert [r["ROM_sha256"] for r in reports] == [stored[k] for k in ("previous_sha256", "candidate_sha256")]
    inputs, frames, end, plan, donor = replay.schedule("revised")
    for report in reports:
        assert report["scripted_input_schedule"] == inputs and report["frames"] == end
        assert report["cold_boot"] and not report["savestate_loaded"] and not report["callback_errors"]
        assert not any(v for k, v in report.items() if k.startswith("synthetic_"))
        save = report["battery_save_preloaded"]
        assert save["copied_byte_exact_before_cold_boot"]
        assert save["source_sha256"] == donor["source_sha256"] == base.digest(donor["source"])
    assert reports[0]["core_DLL_sha256"] == reports[1]["core_DLL_sha256"]
    assert reports[0]["core_options"] == reports[1]["core_options"]
    before, after = map(shots, reports)
    arm = base.NdsImage.open(stage.ROM).read_file(stage.ARM)
    font = GameAsciiFont.from_arm9(arm)
    pixels, evidence = [], {str(p): base.digest(p) for p in (*paths, plan)}
    sheet = Image.new("RGB", (1032, 228), "#273034")
    draw = ImageDraw.Draw(sheet)
    for frame in frames:
        rows = before[frame], after[frame]
        a, b = map(captured, rows)
        evidence.update({r["path"]: r["PNG_sha256"] for r in rows})
        diff = ImageChops.difference(a, b).getbbox()
        if frame in HOLD:
            assert diff and BOX[0] <= diff[0] < diff[2] <= BOX[2] and BOX[1] <= diff[1] < diff[3] <= BOX[3]
            old = font_mask(a, font, "Good with this?", 22, 297, BOX, (0, 8, 0))
            revised = font_mask(b, font, stage.REVISIONS[14], 22, 297, BOX, (0, 8, 0))
            pixels.append(dict(frame=frame, message_ID=14, previous_complete_glyph_pixels=old,
                               revised_complete_glyph_pixels=revised))
            if frame == HOLD[0]:
                for i, (label, screen) in enumerate((("Before", a), ("Revised", b))):
                    draw.text((i * 516 + 6, 2), label, fill="white")
                    sheet.paste(screen.crop((0, 280, 256, 384)).resize((512, 208), Image.Resampling.NEAREST),
                                (i * 516 + 2, 18))
        else:
            assert diff is None, (frame, diff)
        if frame == FAREWELL:
            farewell_ink = font_mask(b, font, "Thanks! Come again.", 22, 297, BOX, (0, 8, 0))
    initial, cancelled, completed = (captured(after[frame]) for frame in (11600, 12281, 13481))
    left, top, right, bottom = ImageChops.difference(initial, cancelled).getbbox()
    assert 81 <= left < right <= 112 and 229 <= top < bottom <= 260
    assert ImageChops.difference(cancelled, completed).getbbox() is not None
    sheet.save(SHEET)
    base.save(PROOF, dict(previous_sha256=stored["previous_sha256"], candidate_sha256=stored["candidate_sha256"],
        actual_no_then_yes_confirmation_holds=pixels, same_pending_deal_after_no_frame=12281,
        complete_unchanged_farewell_pixels=farewell_ink, market_menu_return_frame=13481,
        offline_only_message_IDs=[25], hardware=False, sheet_sha256=base.digest(SHEET), evidence=evidence))
    print("Verified two complete original Trade confirmations, the No return, and the accepted purchase.")


if __name__ == "__main__":
    main()
