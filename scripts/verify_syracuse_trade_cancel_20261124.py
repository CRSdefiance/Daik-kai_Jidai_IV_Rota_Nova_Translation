"""Verify the Syracuse decline, Back, and reopen transitions on the Lisbon build."""

from types import FunctionType

from PIL import Image, ImageDraw

from scripts import observe_syracuse_mixed_trade_cancel_20261124 as play
from scripts import verify_syracuse_local_purchase_20261124 as purchase
from scripts.stage_cartridge_title_20261123 import CLEAN, REGISTRY, NdsImage, digest, read, reference, write


prior, panels = purchase.prior, purchase.prior.panels
OUT = purchase.OUT.with_name("syracuse_trade_cancel_current_20261124.json")
SHEET = OUT.with_suffix(".png")
OPEN = {284, 318, 750, 751, 752}
HOLDS = (16900, 17700, 18100, 18500, 18900, 19300)
ANCHOR = 16900
CASE = "mixed_cancel_with_purchase"


def verify():
    directory = play.ROOT / CASE
    capture, requests, terminal, controls = [
        directory / name for name in
        ("capture/capture_report.json", "requests.json", "terminal.json", "inputs.json")
    ]
    release = read(play.current.RELEASE)
    report, trace, receipt, inputs = map(read, (capture, requests, terminal, controls))
    assert digest(REGISTRY) == release["registry_sha256"] and digest(CLEAN) == release["clean_input_sha256"]
    assert report["ROM_sha256"] == receipt["ROM_sha256"] == digest(release["candidate"]) == release["candidate_sha256"]
    assert report["cold_boot"] and not report["savestate_loaded"] and not report["callback_errors"]
    assert not any(value for key, value in report.items() if key.startswith("synthetic_"))
    assert report["scripted_input_schedule"] == inputs and report["frames"] == receipt["completed_frames"] == play.END
    assert trace["all_host_slots_restored_and_core_file_exact"] and not trace["errors"] and not trace["mismatches"]
    assert all(digest(path) == expected for path, expected in receipt["evidence"].items())
    previous = read(purchase.OUT)
    donor = report["battery_save_preloaded"]
    assert donor["copied_byte_exact_before_cold_boot"] and digest(donor["source"]) == previous["evidence"]["donor"]["sha256"]

    frames = panels.shots(report, "_cold_boot.png")
    screens = {frame: panels.picture(frames[frame]) for frame in HOLDS}
    clean, active = map(NdsImage.open, (CLEAN, release["candidate"]))
    arm = active.read_file(prior.ARM)
    font = prior.GameAsciiFont.from_arm9(arm)
    jp = prior.common_message_entries(clean.read_file(prior.COMMON), clean.read_file(prior.ARM))
    rows = prior.common_rows(active.read_file(prior.COMMON), arm)
    calls = trace["source_requests"]
    assert OPEN.isdisjoint(row["message_ID"] for row in calls)
    cancellation = [row for row in calls if row["frame"] > ANCHOR]
    verified_dialogue = FunctionType(prior.dialogue.__code__, vars(prior) | dict(HOLDS=((18100, 11),)))
    record, = verified_dialogue(jp, rows, frames, cancellation, screens, font)
    record["context"] = ("Charles asks the player to approve the pending trade. No returns to that deal. "
                         "Back then cancels the deal and returns to the Market menu.")
    record["localization_note"] = ("The deferential question suits Charles and leaves both decisions open. "
                                   "The two choice captions fit and the question retains its complete first and last characters.")

    totals = (38702, 1764, 442, 38702 + 1764 - 442)
    ledger = {frame: purchase.exact_ledger(font, screens[frame], values) for frame, values in {
        16900: (38702, 1764, 0, 40466), 17700: totals, 18100: totals,
        18500: totals, 19300: (38702, 0, 0, 38702),
    }.items()}
    choices = [panels.find_mask(font, text, screens[18100], rect) for text, rect in
               (("No", (118, 360, 165, 376)), ("Yes", (188, 360, 235, 376)))]
    market_wallet = panels.find_mask(font, "38702", screens[18900], (55, 348, 139, 366))
    goods = prior.exact_label(screens[19300], font, "Iron Ore\n  Ore 70%", (144, 127), (144, 126, 256, 162))
    wheat = {frame: prior.exact_label(screens[frame], font, "Wheat\n  Food 97%", (144, 127), (144, 126, 256, 162))
             for frame in (17700, 18500)}

    sheet = Image.new("RGB", (1024, 408), "#263238")
    labels = ImageDraw.Draw(sheet)
    for index, (frame, title) in enumerate(zip(HOLDS[1:5], ("Pending deal", "Ask to finish", "Decline keeps the deal", "Back returns to Market"), strict=True)):
        labels.text((index * 256 + 6, 5), title, fill="white")
        sheet.paste(screens[frame], (index * 256, 24))
    sheet.save(SHEET)
    result = dict(
        translation_policy="natural-dialogue-v2", encoder="dialogue-relocatable-v1", target_locale="en-US",
        review_gates=list(prior.GATES), records=[record], candidate_sha256=release["candidate_sha256"],
        ordinary_controls=True, prior_save=reference(donor["source"]),
        evidence=list(map(reference, (capture, requests, terminal, controls))), new_gameplay_scene="Syracuse deal cancellation and reopen",
        scene_scope="Mixed purchase and sale",
        native_requests=calls, archived_IDs_absent_from_these_requests=sorted(OPEN), net_pending=totals[-1], pending_spent=442,
        ledger_checks=ledger, complete_choice_labels=choices, market_wallet=market_wallet,
        iron_ore_goods_info_after_reopen=goods, wheat_goods_info=wheat, contact_sheet=reference(SHEET),
        ROM_changed=False, new_editorial_credit=0,
    )
    prior.validate_natural_dialogue_batch(result)
    write(OUT, result)
    print(f"Verified {result['scene_scope'].lower()}, Charles's confirmation, and all five pending/cleared ledgers.")


if __name__ == "__main__":
    verify()
