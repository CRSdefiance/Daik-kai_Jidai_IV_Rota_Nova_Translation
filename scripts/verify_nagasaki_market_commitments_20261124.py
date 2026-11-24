"""Verify ordinary paid Price Info, the Wheat page, and the investment settlement."""

import json
from pathlib import Path

from PIL import Image, ImageDraw

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.script.common_message_table import common_message_entries
from scripts import observe_nagasaki_market_commitments_20261124 as play
from scripts import verify_genoa_copenhagen_town_20261123 as panels
from scripts.checkpoint_price_info_wraps_20261115 import screen_pixels
from scripts.reconcile_elegy_acceptance_20261123 import common_rows
from scripts.stage_cartridge_title_20261123 import CLEAN, GATES, REGISTRY, NdsImage, digest, read, reference, write
from scripts.verify_trade_good_descriptions_v1 import exact_title


OUT = panels.OUT.with_name("nagasaki_market_commitments_20261124.json")
SHEET = OUT.with_suffix(".png")
DESCRIPTIONS = Path("releases/all_routes_editorial_20261111_trade_good_descriptions_candidate/verification/registered_review.json")
END = 19320
IDS = (8, 761, 1156, 1157, 1158, 8, 18, 137, 762, 747)
CAPTIONS = {13720: "Yizhou price quote", 14120: "Paid Price Info", 15320: "Wheat description", 15720: "Close the description",
            16920: "Market after the 200-coin fee", 18120: "Confirm the 1,350-gold investment", 18520: "Investment accepted",
            19320: "Return to Nagasaki"}


def read_capture(release):
    paths = [play.ROOT / name for name in ("capture/capture_report.json", "trace/requests.json",
             "capture/navigation_command_journal.json", "terminal.json")]
    capture, trace, journal, terminal = map(read, paths)
    assert release["candidate_sha256"] == capture["ROM_sha256"] == journal["ROM_sha256"] == terminal["candidate_sha256"]
    assert capture["cold_boot"] and not capture["savestate_loaded"] and not capture["callback_errors"]
    assert terminal["ordinary_controller_inputs"] and not any(v for key, v in capture.items() if key.startswith("synthetic_"))
    donor = capture["battery_save_preloaded"]
    assert donor["copied_byte_exact_before_cold_boot"] and digest(donor["source"]) == terminal["copied_save_sha256"] == donor["source_sha256"]
    commands = [json.loads(line) for line in play.CONTROLLER.read_text("utf-8").splitlines()]
    assert commands == [r["command"] for r in journal["commands_received"]]
    assert commands[0] == play.OPENING and commands[-1] == {"stop": True}
    assert all(row["validation_passed"] for row in journal["commands_received"])
    assert capture["frames"] == terminal["total_frames"] == journal["last_command_frame"] == END
    assert all(digest(path) == value for path, value in terminal["evidence"].items())
    assert trace["all_host_slots_restored_and_core_file_exact"] and not trace["errors"] and not trace["mismatches"]
    calls = trace["source_requests"]
    assert calls == terminal["common_requests"] and tuple(r["message_ID"] for r in calls[::2]) == IDS
    for first, second in zip(calls[::2], calls[1::2], strict=True):
        assert first["PC"] == 0x0205528C and second == first | {"PC": 0x020534F4}
    return capture, panels.shots(capture, "_navigation.png"), calls, commands, list(map(reference, paths))


def main():
    active = play.decline.current
    release = read(active.RELEASE)
    assert digest(active.ROM) == release["candidate_sha256"] and digest(REGISTRY) == release["registry_sha256"]
    assert digest(CLEAN) == release["clean_input_sha256"]
    capture, frames, calls, commands, evidence = read_capture(release)
    screens = {f: panels.picture(shot) for f, shot in frames.items()}
    prior = read(play.verified.OUT)
    earlier = panels.shots(read(play.HISTORY), "_navigation.png")
    assert frames[12520]["framebuffer_sha256"] == earlier[12520]["framebuffer_sha256"]
    assert frames[14920]["framebuffer_sha256"] == frames[15720]["framebuffer_sha256"]
    assert frames[14120]["framebuffer_sha256"] == frames[16120]["framebuffer_sha256"]

    clean, image = map(NdsImage.open, (CLEAN, active.ROM))
    arm = image.read_file(active.ARM)
    font = GameAsciiFont.from_arm9(arm)
    original = common_message_entries(clean.read_file(active.COMMON), clean.read_file(active.ARM))
    installed = common_rows(image.read_file(active.COMMON), arm)
    historical, = [row for row in read(DESCRIPTIONS)["records"] if row["commodity_index"] == 0]
    assert historical["commodity_name"] == "Wheat" and historical["source_hex"] == original[137].text.hex()
    assert historical["registered_reference"]["exact_stored_hex"] == installed[137].text.hex()
    page, = historical["native_pages"]
    assert page["remaining_bytes"] == 0 and screen_pixels(screens[15320]) == page["pixel_sha256"]
    assert all(historical["review"].values()) and not historical["original_substitutions"]
    wheat = dict(message_ID=137, name=historical["commodity_name"], decision="retention", review=historical["review"],
        source_reference=panels.text_reference(original[137]), current_reference=panels.text_reference(installed[137]),
        clean_Japanese=original[137].text.decode("cp932"), current_English=historical["english"],
        localization_note="The comparison with rice and corn, Mediterranean origin and flour uses all match the source. The four lines fill one complete page.",
        title=exact_title(font, "Wheat", screens[15720]), page=page, displayed_capture=frames[15320], prior_review=reference(DESCRIPTIONS))
    assert exact_title(font, "Wheat", screens[14920]) == wheat["title"]
    invest_rows = []
    for frame, key, lines, note in (
        (17720, 762, ("You need market share to trade.", "You still want to invest?", "That's generous of you.", "How much will you put in?"),
         "The surprised response gives the trading restriction, willingness and amount question their own beats before the offer."),
        (18520, 747, ("Thanks. We'll put it to good use.",),
         "The short thanks follows the payment naturally and keeps the assurance that the contribution will be used."),
    ):
        ja, en = original[key], installed[key]
        assert en.text.decode("ascii").split() == " ".join(lines).split() and b"%" not in ja.text + en.text
        requests = [r for r in calls if r["message_ID"] == key and 0 < frame - r["frame"] < 400]
        assert len(requests) == 2
        invest_rows.append(dict(message_ID=key, speaker="Trader", decision="retention", review=dict.fromkeys(GATES, True),
            clean_Japanese=ja.text.decode("cp932"), current_English=en.text.decode("ascii"), localization_note=note,
            source_reference=panels.text_reference(ja), current_reference=panels.text_reference(en),
            body_pixels=panels.exact_body(font, lines, screens[frame]), nameplate=panels.nameplate(font, "Trader", screens[frame]),
            capture=frames[frame], requests=requests))
    starting_balance = next(row for row in prior["unchanged_wallet_masks"] if row["frame"] == 9720)
    assert starting_balance["text"] == "38493"
    balances = [dict(frame=n, **panels.find_mask(font, str(gold), screens[n], (76, 348, 136, 364)))
                for n, gold in ((16920, 38293), (18920, 36943), (END, 36943))]
    amount = panels.find_mask(font, "1350", screens[18120], (134, 327, 192, 349))
    town_title = panels.find_mask(font, "Yizhou", screens[14120], (40, 0, 117, 17))
    sheet = Image.new("RGB", (1024, 808), "#263238")
    labels = ImageDraw.Draw(sheet)
    for i, (frame, label) in enumerate(CAPTIONS.items()):
        x, y = 256 * (i % 4), 404 * (i // 4)
        labels.text((x + 4, y + 3), label, fill="white")
        sheet.paste(screens[frame], (x, y + 20))
    sheet.save(SHEET)

    write(OUT, dict(candidate_sha256=release["candidate_sha256"], ordinary_gameplay=True, exact_source_requests=calls,
        replay_commands=commands, ordinary_input_schedule=capture["scripted_input_schedule"], verified_retained_records=[wheat, *invest_rows],
        prices=dict(town="Yizhou", observed_quote="Yizhou: 200 coins", charged_gold=200, title_mask=town_title, quote_capture=frames[13720],
                    Wheat_description_exit_pixel_exact=True, category_screen_on_exit_pixel_exact=True),
        investment=dict(charged_gold=1350, proposed_amount=amount, confirmation=frames[18520]), starting_balance=starting_balance,
        balance_masks=balances, returned_to_town=frames[END], archived_market_ids_seen=sorted(set(IDS) & {750, 751, 752}),
        unvisited=["High-fee remote price checks", "Investment when funds are insufficient"],
        evidence=evidence + list(map(reference, (active.RELEASE, play.HISTORY, play.verified.OUT, SHEET))), new_editorial_credit=0, ROM_changed=False))
    print("Verified paid Yizhou Price Info, the complete Wheat page, and Nagasaki's 1350-gold investment settlement.")


if __name__ == "__main__":
    main()
