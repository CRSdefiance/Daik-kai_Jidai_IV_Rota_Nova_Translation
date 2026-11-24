"""Bind ordinary cancellation and Market choices to their exact source and display."""

import json

from PIL import Image, ImageDraw

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.script.common_message_table import common_message_entries
from scripts import observe_nagasaki_contract_decline_20261124 as played
from scripts import verify_genoa_copenhagen_town_20261123 as panels
from scripts.reconcile_elegy_acceptance_20261123 import common_rows
from scripts.stage_cartridge_title_20261123 import CLEAN, GATES, REGISTRY, NdsImage, digest, read, reference, write


OUT = panels.OUT.with_name("nagasaki_contract_decline_20261124.json")
SHEET = OUT.with_suffix(".png")
END = 15320
REQUESTS = (8, 761, 1156, 1157, 1158, 8, 18, 762, 746)
HOLDS = {
    8920: (1158, "Daimyo", ("Bah! Make up your mind.",),
           "The brusque rebuke conveys the Daimyo's impatience at the canceled offer."),
    12120: (18, "Trader", ("There's a fee for each price check.", "Which town did you have in mind?"),
            "The dealer explains that the charge applies per check before asking which town to look up. Both sentences stay together."),
    13720: (762, "Trader", ("You need market share to trade.", "You still want to invest?",
            "That's generous of you.", "How much will you put in?"),
            "The prerequisite explains the trader's surprise. The thanks and the short amount question each get a beat before the amount picker."),
    14520: (746, "Trader", ("Just browsing?",),
            "After Maria backs out of the amount picker, the dealer's short question conveys mild disappointment."),
}
CAPTIONS = {8920: "Decline the Palace offer", 9720: "Return with the same balance", 12120: "Ask about prices",
            12520: "Town price chooser", 13720: "Invest without market share", 14120: "Unconfirmed investment",
            14520: "Cancel the investment", 15320: "Return to town"}


def checked_capture(release):
    paths = [played.ROOT / name for name in ("capture/capture_report.json", "trace/requests.json",
             "capture/navigation_command_journal.json", "terminal.json")]
    capture, trace, journal, terminal = map(read, paths)
    assert release["candidate_sha256"] == capture["ROM_sha256"] == journal["ROM_sha256"] == terminal["candidate_sha256"]
    assert terminal["ordinary_controller_inputs"] and capture["cold_boot"] and not capture["savestate_loaded"]
    assert not capture["callback_errors"] and not any(v for k, v in capture.items() if k.startswith("synthetic_"))
    donor = capture["battery_save_preloaded"]
    assert donor["copied_byte_exact_before_cold_boot"]
    assert digest(donor["source"]) == donor["source_sha256"] == terminal["copied_save_sha256"]
    commands = [json.loads(line) for line in played.CONTROLLER.read_text("utf-8").splitlines()]
    assert commands == [r["command"] for r in journal["commands_received"]]
    assert commands[0] == played.CHOICE and commands[-1] == {"stop": True}
    assert all(row["validation_passed"] for row in journal["commands_received"])
    assert capture["frames"] == terminal["total_frames"] == journal["last_command_frame"] == END
    assert all(digest(path) == value for path, value in terminal["evidence"].items())
    assert trace["all_host_slots_restored_and_core_file_exact"] and not trace["errors"] and not trace["mismatches"]
    calls = trace["source_requests"]
    assert calls == terminal["common_requests"] and tuple(r["message_ID"] for r in calls[::2]) == REQUESTS
    for first, second in zip(calls[::2], calls[1::2], strict=True):
        assert first["PC"] == 0x0205528C and second == first | {"PC": 0x020534F4}
    return capture, panels.shots(capture, "_navigation.png"), calls, commands, list(map(reference, paths))


def main():
    active = played.current
    release = read(active.RELEASE)
    assert digest(active.ROM) == release["candidate_sha256"] and digest(REGISTRY) == release["registry_sha256"]
    assert digest(CLEAN) == release["clean_input_sha256"]
    capture, frames, calls, commands, evidence = checked_capture(release)
    screens = {frame: panels.picture(shot) for frame, shot in frames.items()}
    old = panels.shots(read(active.build.BEFORE), "_navigation.png")
    registered = panels.shots(read(played.HISTORY), "_cold_boot.png")
    assert frames[8520]["framebuffer_sha256"] == registered[8520]["framebuffer_sha256"]
    returns = {9720: 6920, 14920: 5320, 15320: 6520}
    assert all(frames[new]["framebuffer_sha256"] == old[prior]["framebuffer_sha256"] for new, prior in returns.items())
    clean, image = map(NdsImage.open, (CLEAN, active.ROM))
    arm = image.read_file(active.ARM)
    font = GameAsciiFont.from_arm9(arm)
    source = common_message_entries(clean.read_file(active.COMMON), clean.read_file(active.ARM))
    installed = common_rows(image.read_file(active.COMMON), arm)
    rows = []
    for frame, (key, speaker, lines, note) in HOLDS.items():
        ja, en = source[key], installed[key]
        assert b"%" not in ja.text and b"%" not in en.text
        assert en.text.decode("ascii").split() == " ".join(lines).split()
        requests = [row for row in calls if row["message_ID"] == key and 0 < frame - row["frame"] < 400]
        assert len(requests) == 2
        rows.append(dict(message_ID=key, speaker=speaker, decision="retention", localization_note=note,
            clean_Japanese=ja.text.decode("cp932"), current_English=en.text.decode("ascii"),
            source_reference=panels.text_reference(ja), installed_reference=panels.text_reference(en),
            review=dict.fromkeys(GATES, True), observed_lines=lines, complete_body_pixels=panels.exact_body(font, lines, screens[frame]),
            nameplate=panels.nameplate(font, speaker, screens[frame]), capture=frames[frame], requests=requests))
    wallet = [dict(frame=n, **panels.find_mask(font, "38493", screens[n], (76, 348, 136, 364)))
              for n in (9720, 12920, 14920, END)]
    proposed_amount = panels.find_mask(font, "1350", screens[14120], (134, 327, 192, 349))
    sheet = Image.new("RGB", (1024, 808), "#263238")
    captions = ImageDraw.Draw(sheet)
    for i, (frame, label) in enumerate(CAPTIONS.items()):
        x, y = 256 * (i % 4), 404 * (i // 4)
        captions.text((x + 4, y + 3), label, fill="white")
        sheet.paste(screens[frame], (x, y + 20))
    sheet.save(SHEET)
    write(OUT, dict(candidate_sha256=release["candidate_sha256"], ordinary_gameplay=True, played_with_pristine_battery_copy=True,
        replay_commands=commands, exact_source_requests=calls, ordinary_input_schedule=capture["scripted_input_schedule"],
        contextual_retentions=rows, unchanged_wallet_masks=wallet, unconfirmed_investment=proposed_amount,
        observed_free_current_town_quote=dict(text="Nagasaki: 0 coins", capture=frames[12520]),
        pixel_exact_return_comparisons=[dict(return_hold=frames[n], previous_menu=old[p]) for n, p in returns.items()],
        unvisited=["Paid check of another town's prices", "Approved investment without a contract", "Other rulers' cancellation branches"],
        evidence=evidence + list(map(reference, (active.RELEASE, active.build.BEFORE, played.HISTORY, SHEET))),
        new_editorial_credit=0, ROM_changed=False))
    print("Verified four dialogue retentions, three exact return frames, and unchanged funds through the ordinary cancellations.")


if __name__ == "__main__":
    main()
