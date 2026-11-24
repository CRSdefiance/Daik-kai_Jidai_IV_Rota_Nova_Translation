"""Check the complete Nagasaki contract exchange and three live Goods Info selections."""

import json

from PIL import Image, ImageDraw

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.script.common_message_table import common_message_entries
from scripts import observe_nagasaki_market_20261124 as played
from scripts import verify_genoa_copenhagen_town_20261123 as panels
from scripts.reconcile_elegy_acceptance_20261123 import common_rows
from scripts.stage_cartridge_title_20261123 import CLEAN, GATES, REGISTRY, NdsImage, digest, read, reference, write
from scripts.verify_commodity_private_market_live_v354 import exact_label


OUT = panels.OUT.with_name("nagasaki_market_current_20261124.json")
SHEET = OUT.with_suffix(".png")
HOLDS = {
    4920: (8, "Trader", (), ("Need help?",), "The brief greeting invites Maria to select a service."),
    5720: (761, "Trader", ("Palace",), ("Sorry. Please sign a contract", "at the Palace, then come back."),
           "The apology, specific Palace instruction and invitation to return preserve the polite refusal."),
    7720: (1156, "Daimyo", ("1125",), ("You'd like to trade here? Hmm...", "Very well. The minimum contract fee",
           "is 1125 gold coins."), "The hesitation marks the ruler's consideration, followed by permission and the exact minimum."),
    8120: (1157, "Daimyo", (), ("Your market share will depend on", "the contract fee you pay. How much",
           "will you offer?"), "The relationship between the fee and share is correct. The short question splits across rows."),
    8920: (1159, "Daimyo", (), ("Very well. You may trade", "in this city."),
           "The ruler grants the trading permission just purchased. The city phrase stays together."),
    10520: (8, "Trader", (), ("Need help?",), "The same greeting follows the Palace permission and leads into Trade."),
}
GOODS = {11320: ("Silver", "Metals 100%"), 11720: ("Cotton Cloth", "Textiles 100%"),
         12120: ("Tortoiseshell", "Jewelry 102%")}
CAPTIONS = {4920: "Market greeting", 5720: "Trade requires a contract", 7720: "Minimum contract fee",
            8120: "Market share and offer", 8520: "Contract payment", 8920: "Trade permission",
            9720: "Town after purchase", 10520: "Market greeting after purchase", 11320: "Silver",
            11720: "Cotton Cloth", 12120: "Tortoiseshell", 12920: "Return to Nagasaki"}


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
    assert commands == [r["command"] for r in journal["commands_received"]] and commands[-1] == {"stop": True}
    assert all(row["validation_passed"] for row in journal["commands_received"])
    assert capture["frames"] == terminal["total_frames"] == journal["last_command_frame"] == 12920
    assert all(digest(path) == value for path, value in terminal["evidence"].items())
    assert trace["all_host_slots_restored_and_core_file_exact"] and not trace["errors"] and not trace["mismatches"]
    calls = trace["source_requests"]
    assert calls == terminal["common_requests"] and [r["message_ID"] for r in calls[::2]] == [row[0] for row in HOLDS.values()]
    for first, second in zip(calls[::2], calls[1::2], strict=True):
        assert first["PC"] == 0x0205528C and second == first | {"PC": 0x020534F4}
    return capture, panels.shots(capture, "_navigation.png"), calls, commands, list(map(reference, paths))


def main():
    release = read(played.current.RELEASE)
    assert digest(played.current.ROM) == release["candidate_sha256"] and digest(REGISTRY) == release["registry_sha256"]
    assert digest(CLEAN) == release["clean_input_sha256"]
    capture, frames, calls, commands, evidence = checked_capture(release)
    screens = {frame: panels.picture(shot) for frame, shot in frames.items()}
    clean, rom = map(NdsImage.open, (CLEAN, played.current.ROM))
    arm = rom.read_file(played.current.ARM)
    font = GameAsciiFont.from_arm9(arm)
    source = common_message_entries(clean.read_file(played.current.COMMON), clean.read_file(played.current.ARM))
    installed = common_rows(rom.read_file(played.current.COMMON), arm)
    rows = []
    for frame, (key, speaker, args, lines, reason) in HOLDS.items():
        ja, en = source[key], installed[key]
        assert ja.text.count(b"%s") == en.text.count(b"%s") == len(args)
        display = en.text % tuple(arg.encode("ascii") for arg in args)
        assert display.decode("ascii").split() == " ".join(lines).split()
        requests = [r for r in calls if r["message_ID"] == key and 0 <= frame - r["frame"] < 400]
        assert len(requests) == 2
        gates = dict.fromkeys(GATES, True)
        gates["formatting"] = key != 1157
        rows.append(dict(message_ID=key, decision="wrap finding" if key == 1157 else "retention", speaker=speaker,
            clean_Japanese=ja.text.decode("cp932"), clean_reference=panels.text_reference(ja),
            current_English=en.text.decode("ascii"), installed_reference=panels.text_reference(en),
            substitution_values=args, observed_lines=lines, localization_note=reason, review=gates,
            complete_body_pixels=panels.exact_body(font, lines, screens[frame]),
            nameplate=panels.nameplate(font, speaker, screens[frame]), capture=frames[frame], requests=requests))
    goods = []
    for frame, (item, status) in GOODS.items():
        mask = exact_label(screens[frame], font, f"{item}\n  {status}", (144, 127), (144, 126, 256, 162))
        goods.append(dict(frame=frame, capture=frames[frame], complete_Goods_Info_mask=mask))
    before, after = (panels.find_mask(font, str(funds), screens[frame], (76, 348, 136, 364))
                     for frame, funds in ((6520, 38493), (9720, 37368)))
    assert frames[5320]["framebuffer_sha256"] == frames[6120]["framebuffer_sha256"]
    assert frames[10920]["framebuffer_sha256"] == frames[12520]["framebuffer_sha256"]
    assert frames[10120]["framebuffer_sha256"] == frames[12920]["framebuffer_sha256"]
    share = dict(observed="1%", frame=9720, capture=frames[9720])
    sheet = Image.new("RGB", (768, 4 * 404), "#263238")
    draw = ImageDraw.Draw(sheet)
    for i, (frame, caption) in enumerate(CAPTIONS.items()):
        x, y = i % 3 * 256, i // 3 * 404
        draw.text((x + 4, y + 3), caption, fill="white")
        sheet.paste(screens[frame], (x, y + 20))
    sheet.save(SHEET)
    write(OUT, dict(candidate_sha256=release["candidate_sha256"], ordinary_gameplay=True,
        hardware_verified=False, replay_commands=commands, input_schedule=capture["scripted_input_schedule"],
        observed_dialogue=rows, goods_info=goods, wallet_before=before, wallet_after=after, market_share=share,
        paid_gold=1125, returns_to_matching_Market_and_town=True,
        unvisited=["Cargo Goods Info in this replay", "Declined contract offer", "Other cities' contract variants"],
        evidence=evidence + list(map(reference, (played.HISTORY, played.current.RELEASE, SHEET))),
        ROM_changed=False, new_editorial_credit=0))
    print("Verified six dialogue holds, the 1125-gold contract, three complete Goods Info panels and both returns.")


if __name__ == "__main__":
    main()
