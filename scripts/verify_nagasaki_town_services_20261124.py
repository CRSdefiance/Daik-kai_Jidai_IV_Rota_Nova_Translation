"""Verify the ordinary Nagasaki lodging branches and the Square after the stay."""

import json

from PIL import Image, ImageDraw

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.script.common_message_table import common_message_entries
from scripts import observe_nagasaki_town_services_20261124 as play
from scripts import verify_genoa_copenhagen_town_20261123 as panels
from scripts.reconcile_elegy_acceptance_20261123 import common_rows
from scripts.record_navigation_v327 import dark_text
from scripts.stage_cartridge_title_20261123 import CLEAN, GATES, REGISTRY, NdsImage, digest, read, reference, write


OUT = panels.OUT.with_name("nagasaki_town_services_20261124.json")
END = 17320
HOLDS = (
    (5720, 63), (6920, 1179), (8120, 1180), (8520, 1179), (9720, 1180), (10120, 1181),
    (11320, 1177), (12120, 1177), (12520, 1178), (14920, 656), (15720, 727), (16520, 656),
)
REVIEW = {
    63: ("Innkeeper", (), ("Welcome! Come in.",),
         "The two short clauses give the unnamed host a warm greeting before the stay choices open."),
    1177: ("Innkeeper", (), ("That'll be 1 gold coin.",),
           "The host gives the exact charge in conversational English before either one-night choice."),
    1178: ("Innkeeper", (), ("Sleep well!",),
           "The Japanese bids the guest goodnight. The English works as a friendly send-off after payment is accepted."),
    1179: ("Innkeeper", (), ("It's 1 gold coin for each night.", "How many nights will you stay?"),
           "The first row gives the nightly rate. The second gives an intact question that still makes sense on return from No."),
    1180: ("Innkeeper", ("10",), ("You're staying 10 nights, then?",),
           "Then keeps the Japanese confirmation tone and the regular-width digits show the exact selected duration."),
    1181: ("Innkeeper", (), ("Enjoy your stay.",),
           "The familiar hospitality phrase follows Yes on the longer stay and leaves the passage of time to the game."),
    656: ("Shopkeeper", (), ("We only sell retail.",),
          "The compact reply describes the retail counter without implying the same restriction at the Market."),
    727: ("Shopkeeper", (), ("They say Kurushima became obsessed", "with the power of ironclad ships", "after Nobunaga defeated him."),
          "They say preserves the rumor. The three rows keep the object of Kurushima's interest and the defeat that prompted it."),
}
MENU = (
    (6120, 0x143DA0, 12, "Stay 1 Day", "一日泊まる", "A clear one-day calendar option for a single overnight stay."),
    (6120, 0x143DAC, 16, "Stay More", "続けて泊まる", "A compact caption for opening the longer-stay chooser."),
    (7320, 0x143D78, 8, "3 Days", "３日", "The first duration option states the original number of days."),
    (7720, 0x143D90, 8, "10 Days", "１０日", "The middle option states the duration reflected by the confirmation and observed date change."),
    (7320, 0x143D88, 8, "30 Days", "３０日", "The third duration option states the original number of days and fits the chooser."),
)


def gameplay(release):
    root = play.ROOT
    links = [root / name for name in ("capture/capture_report.json", "trace/requests.json",
                                     "capture/navigation_command_journal.json", "terminal.json")]
    capture, trace, journal, terminal = map(read, links)
    sha = release["candidate_sha256"]
    assert capture["ROM_sha256"] == journal["ROM_sha256"] == terminal["candidate_sha256"] == sha
    assert terminal["ordinary_controller_inputs"] and capture["cold_boot"] and not capture["savestate_loaded"]
    assert not capture["callback_errors"] and not any(v for k, v in capture.items() if k.startswith("synthetic_"))
    assert terminal["total_frames"] == capture["frames"] == journal["last_command_frame"] == END
    assert all(digest(path) == sha for path, sha in terminal["evidence"].items())
    donor = capture["battery_save_preloaded"]
    assert donor["copied_byte_exact_before_cold_boot"] and not donor["savestate_loaded"]
    assert digest(donor["source"]) == donor["source_sha256"] == terminal["copied_save_sha256"]
    commands = [json.loads(line) for line in play.CONTROLLER.read_text("utf-8").splitlines()]
    assert commands == [row["command"] for row in journal["commands_received"]] and commands[-1] == {"stop": True}
    assert all(row["validation_passed"] for row in journal["commands_received"])
    assert trace["all_host_slots_restored_and_core_file_exact"] and not trace["mismatches"] and not trace["errors"]
    requests = trace["source_requests"]
    assert requests == terminal["common_requests"] and len(requests) == len(HOLDS) * 2
    frames = panels.shots(capture, "_navigation.png")
    previous = panels.shots(read(play.HISTORY), "_cold_boot.png")[3720]
    assert frames[3720]["framebuffer_sha256"] == previous["framebuffer_sha256"]
    return frames, list(zip(requests[::2], requests[1::2], strict=True)), donor, commands, links


def review_dialogue(source, installed, frames, screens, requests, font):
    rows = {}
    for (frame, key), (getter, copier) in zip(HOLDS, requests, strict=True):
        assert getter["PC"] == 0x0205528C and copier == getter | {"PC": 0x020534F4}
        assert getter["message_ID"] == key and 0 < frame - getter["frame"] < 400
        speaker, args, lines, reason = REVIEW[key]
        ja, en = source[key], installed[key]
        assert ja.text.count(b"%s") == en.text.count(b"%s") == len(args)
        expanded = (en.text % tuple(a.encode("ascii") for a in args)).decode("ascii")
        assert expanded.split() == " ".join(lines).split()
        parsed = dict(frame=frame, complete_body_ink=panels.exact_body(font, lines, screens[frame]),
                      nameplate=panels.nameplate(font, speaker, screens[frame]), requests=[getter, copier], capture=frames[frame])
        if key not in rows:
            rows[key] = dict(message_ID=key, speaker=speaker, clean_Japanese=ja.text.decode("cp932"),
                             source_reference=panels.text_reference(ja) | {"exact_hex": ja.text.hex()},
                             installed_reference=panels.text_reference(en) | {"exact_hex": en.text.hex()},
                             current_English=en.text.decode("ascii").strip(), decision="retention", rationale=reason,
                             arguments=args, actual_lines=lines, review=dict.fromkeys(GATES, True), observed=[])
        rows[key]["observed"].append(parsed)
    assert set(rows) == set(REVIEW)
    return list(rows.values())


def review_menu(clean_arm, arm, screens, font):
    rows = []
    for frame, offset, size, text, japanese, reason in MENU:
        ja, en = clean_arm[offset:offset + size], arm[offset:offset + size]
        assert ja.split(b"\0", 1)[0].decode("cp932") == japanese and en == text.encode("ascii").ljust(size, b"\0")
        mask = dark_text(font, text, screens[frame], (70, 255, 180, 325))
        rows.append(dict(file="/__arm9__.bin", offset=offset, size=size, source_hex=ja.hex(), installed_hex=en.hex(),
                         clean_Japanese=japanese, current_English=text, frame=frame, decision="retention",
                         rationale=reason, review=dict.fromkeys(GATES, True), mask=mask))
    return rows


def transition_sheet(screens):
    path = OUT.with_name("nagasaki_lodging_transitions_20261124.png")
    visits = ((6120, "Inn menu"), (7720, "Ten-day option"), (8520, "No returns to the quote"),
              (10920, "Ten nights paid"), (12920, "One more night paid"), (17320, "Return to the Square menu"))
    image = Image.new("RGB", (768, 424), "#263238")
    draw = ImageDraw.Draw(image)
    for index, (frame, caption) in enumerate(visits):
        x, y = 256 * (index % 3), 212 * (index // 3)
        draw.text((x + 4, y + 3), f"{frame} / {caption}", fill="white")
        image.paste(screens[frame].crop((0, 192, 256, 384)), (x, y + 20))
    image.save(path)
    return reference(path)


def main():
    active = play.active
    release = read(active.RELEASE)
    assert digest(active.ROM) == release["candidate_sha256"] and digest(CLEAN) == release["clean_input_sha256"]
    assert digest(REGISTRY) == release["registry_sha256"]
    frames, requests, donor, commands, links = gameplay(release)
    screens = {frame: panels.picture(shot) for frame, shot in frames.items()}
    clean, current = map(NdsImage.open, (CLEAN, active.ROM))
    clean_arm, arm = (rom.read_file(active.ARM) for rom in (clean, current))
    source = common_message_entries(clean.read_file(active.COMMON), clean_arm)
    installed = common_rows(current.read_file(active.COMMON), arm)
    font = GameAsciiFont.from_arm9(arm)
    prose = review_dialogue(source, installed, frames, screens, requests, font)
    menu = review_menu(clean_arm, arm, screens, font)

    wallet = [(3720, 38493, "12"), (7720, 38493, "12"), (10920, 38483, "22"), (11720, 38483, "22"),
              (12920, 38482, "23"), (13320, 38482, "23")]
    states = [dict(frame=frame, coins=gold, day=day, coin_mask=panels.find_mask(font, str(gold), screens[frame], (38, 348, 136, 367)),
                   date_mask=panels.find_mask(font, day, screens[frame], (122, 330, 156, 347))) for frame, gold, day in wallet]
    choices = [(8120, 9720), (11320, 12120)]
    for first, second in choices:
        assert frames[first]["framebuffer_sha256"] == frames[second]["framebuffer_sha256"]
    return_to_town = panels.find_mask(font, "Nagasaki", screens[13320], (14, 14, 147, 31))
    final_square = dark_text(font, "Trends", screens[END], (92, 273, 164, 306))
    figures = [(f'{row["observed"][0]["frame"]} / COMMON {row["message_ID"]}', screens[row["observed"][0]["frame"]]) for row in prose]
    sheets = [*panels.sheets_for("nagasaki_lodging_and_square", figures), transition_sheet(screens)]
    write(OUT, dict(candidate_sha256=release["candidate_sha256"], clean_input_sha256=release["clean_input_sha256"],
                    ordinary_gameplay=True, source_donor=reference(donor["source"]), visited_frames=END,
                    dialogue_records=prose, menu_records=menu, matched_confirmation_frames=choices, observed_balances_and_days=states,
                    commands=commands, paired_native_calls=len(requests), return_to_town=return_to_town,
                    terminal_square_menu=final_square, sheets=sheets,
                    proof_sources=list(map(reference, [active.RELEASE, play.HISTORY, play.CONTROLLER, *links])),
                    unvisited=["Insufficient-funds and early departure prompts", "Other stay lengths and conditional Inn rumors", "Additional Square variants"],
                    ROM_changed=False, new_editorial_credit=0))
    print(f"Verified {len(HOLDS)} dialogue holds, {len(menu)} menu labels, both completed payments and both return transitions.")


if __name__ == "__main__":
    main()
