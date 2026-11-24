"""Bind Nagasaki Tavern gameplay and recruiting prose to exact source records."""

import json
from struct import unpack_from

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.script.common_message_table import common_message_entries
from scripts import observe_nagasaki_tavern_20261124 as play
from scripts import verify_genoa_copenhagen_town_20261123 as panels
from scripts.reconcile_elegy_acceptance_20261123 import common_rows
from scripts.stage_cartridge_title_20261123 import CLEAN, GATES, REGISTRY, NdsImage, digest, read, reference, write
from scripts.verify_crew_policy_matrix_v657 import BASE, find_complete, string


OUT = panels.OUT.with_name("nagasaki_tavern_20261124.json")
END = 16520
REQUESTS = (51, 53, 823, 53, 823, 855, 867, 872, 874, 870, 893, 900, 907, 904, 1045, 14)
HOLDS = (
    (4520, 51, "Barkeep", (), ("Welcome! What will you have?",),
     "A warm, brief greeting leaves room for the player to order."),
    (5320, 53, "Barkeep", (), ("5 coins.",),
     "The terse price answers an ordinary drink order and matches the charge."),
    (5720, 823, "Barkeep", ("Naha",), ("Have you heard of a nearby town", "called Naha?"),
     "The barkeep turns the location into a conversational tip and keeps the fact that the town is nearby."),
    (8120, 855, "Sailor", ("208",), ("Looks like it'll cost 208 gold.", "Okay with you?"),
     "The estimate and informal tag fit the sailor's voice and let Maria confirm before spending."),
    (8520, 867, "Maria Li", (), ("Barkeep, serve everyone", "a drink, please."),
     "Maria's request stays direct and courteous. She includes the whole room."),
    (8920, 872, "Barkeep", ("Li",), ("This round's on Li. Enjoy!",),
     "The barkeep names the payer and tells the room to enjoy the drinks. Keep the previously verified optional address mapping."),
    (9320, 874, "Patron", (), ("Whoa! Really? Thanks for the round!", "Mighty generous of you!"),
     "The patron moves quickly from surprise to thanks and praise for the player's generosity."),
    (9720, 870, "Patron", ("Ma'am", "Pink Apron", "East Asia"),
     ("Ma'am, here's a tip. They say", "a rare treasure called Pink Apron", "is hidden in East Asia."),
     "The patron offers a tip in return. The rumor stays hearsay, with the item and region intact."),
    (11320, 893, "Sailor", ("1040",), ("I'll get us sailors for 1040 gold.",),
     "The sailor volunteers to find crew in the same informal voice as the drinks quote. The stated cost precedes the choice."),
    (11720, 900, "Sailor", (), ("Anyone here want to sail", "with the Admiral?"),
     "The sailor calls for volunteers in a room of patrons. Admiral follows the source term for the fleet commander."),
    (12120, 907, "Patron", (), ("Aye!",),
     "The one-word call answers the recruiting pitch and leads into the tally."),
    (12520, 904, "Sailor", ("57",), ("We've got 57 willing to join.",),
     "The sailor reports the turnout before the prompt to recruit more."),
    (12920, 1045, "Sailor", ("29",), ("There's space aboard for 29 more.", "Want me to round up more?"),
     "The sentences repeat ‘more’ in quick succession. Keep the open-berth count and the offer to continue recruiting."),
    (15720, 14, "Sailor", (), ("All set, then?",),
     "The short confirmation fits the sailor's voice and gives the player a clear handoff after assignment."),
)
PROPOSED = "There's room aboard for %s more. Should I keep looking?"


def main():
    active = play.current
    release = read(active.RELEASE)
    assert digest(active.ROM) == release["candidate_sha256"] and digest(REGISTRY) == release["registry_sha256"]
    assert digest(CLEAN) == release["clean_input_sha256"]
    paths = [play.ROOT / name for name in ("capture/capture_report.json", "trace/requests.json",
             "capture/navigation_command_journal.json", "terminal.json")]
    capture, trace, journal, terminal = map(read, paths)
    assert capture["ROM_sha256"] == journal["ROM_sha256"] == terminal["candidate_sha256"] == release["candidate_sha256"]
    assert capture["cold_boot"] and not capture["savestate_loaded"] and not capture["callback_errors"]
    assert terminal["ordinary_controller_inputs"] and not any(v for k, v in capture.items() if k.startswith("synthetic_"))
    donor = capture["battery_save_preloaded"]
    assert donor["copied_byte_exact_before_cold_boot"] and digest(donor["source"]) == terminal["copied_save_sha256"] == donor["source_sha256"]
    commands = [json.loads(line) for line in play.CONTROLLER.read_text("utf-8").splitlines()]
    assert commands == [row["command"] for row in journal["commands_received"]]
    assert commands[0] == play.OPENING and commands[-1] == {"stop": True}
    assert all(row["validation_passed"] for row in journal["commands_received"])
    assert capture["frames"] == terminal["total_frames"] == journal["last_command_frame"] == END
    assert all(digest(path) == value for path, value in terminal["evidence"].items())
    assert trace["all_host_slots_restored_and_core_file_exact"] and not trace["errors"] and not trace["mismatches"]
    calls = trace["source_requests"]
    assert calls == terminal["common_requests"] and tuple(row["message_ID"] for row in calls[::2]) == REQUESTS
    for first, second in zip(calls[::2], calls[1::2], strict=True):
        assert first["PC"] == 0x0205528C and second == first | {"PC": 0x020534F4}

    frames = panels.shots(capture, "_navigation.png")
    screens = {frame: panels.picture(shot) for frame, shot in frames.items()}
    earlier = panels.shots(read(play.HISTORY), "_cold_boot.png")
    assert frames[play.FIRST_PAUSE]["framebuffer_sha256"] == earlier[play.FIRST_PAUSE]["framebuffer_sha256"]
    assert frames[5720]["framebuffer_sha256"] == frames[6920]["framebuffer_sha256"]
    clean, image = map(NdsImage.open, (CLEAN, active.ROM))
    original_arm, arm = [rom.read_file(active.ARM) for rom in (clean, image)]
    source = common_message_entries(clean.read_file(active.COMMON), original_arm)
    installed = common_rows(image.read_file(active.COMMON), arm)
    font = GameAsciiFont.from_arm9(arm)
    records, figures = [], []
    for frame, key, speaker, arguments, lines, reason in HOLDS:
        ja, en = source[key], installed[key]
        assert ja.text.count(b"%s") == len(arguments) + (key == 872)
        assert en.text.count(b"%s") == len(arguments)
        expanded = en.text % tuple(arg.encode("ascii") for arg in arguments)
        assert expanded.decode("ascii").split() == " ".join(lines).split()
        first, second = [row for row in calls if row["message_ID"] == key and 0 < frame - row["frame"] < 400]
        assert second == first | {"PC": 0x020534F4}
        review = dict.fromkeys(GATES, True)
        decision = "retention"
        if key == 1045:
            review["naturalness"] = False
            decision = "revision proposed"
        records.append(dict(message_ID=key, speaker=speaker, source=panels.text_reference(ja),
            installed=panels.text_reference(en), Japanese=ja.text.decode("cp932"), English=en.text.decode("ascii").strip(),
            arguments=arguments, display_lines=lines, decision=decision, rationale=reason, review=review,
            body_ink_pixels=panels.exact_body(font, lines, screens[frame]),
            nameplate=panels.nameplate(font, speaker, screens[frame]), capture=frames[frame], requests=[first, second]))
        figures.append((f"{frame} / {speaker} / COMMON {key}", screens[frame]))
    assert PROPOSED.count("%s") == 1 and PROPOSED.count("more") == 1
    next(row for row in records if row["message_ID"] == 1045)["proposed_english"] = PROPOSED

    pointer = unpack_from("<I", arm, 0x1E27C)[0]
    assert pointer == unpack_from("<I", original_arm, 0x1E27C)[0]
    ja, en = [string(data, pointer) for data in (original_arm, arm)]
    assert en == b"Sailors assigned evenly."
    even = dict(arm9_pointer_offset=0x1E27C, arm9_text_offset=pointer - BASE, source_hex=ja.hex(), installed_hex=en.hex(),
        Japanese=ja.decode("cp932"), English=en.decode("ascii"), decision="retention", review=dict.fromkeys(GATES, True),
        rationale="The notice confirms that Even distributed the crew without repeating the menu instructions.",
        body_ink_pixels=panels.exact_body(font, (en.decode("ascii"),), screens[14920]),
        nameplate=panels.nameplate(font, "Sailor", screens[14920]), capture=frames[14920])
    figures.append(("14920 / Assign Sailors / Even", screens[14920]))
    balances = [dict(frame=frame, **panels.find_mask(font, gold, screens[frame], (76, 348, 136, 364)))
                for frame, gold in ((4920, "38493"), (7320, "38483"), (10120, "38275"), (END, "37235"))]
    distribution = [find_complete(font, value, screens[15320], bounds) for value, bounds in (
        ("171", (86, 18, 127, 37)), ("0", (216, 18, 255, 37)),
        ("86", (174, 206, 198, 227)), ("85", (174, 238, 198, 259)))]
    title_box = (36, 14, 220, 32)
    assert screens[END].crop(title_box).tobytes() == screens[play.FIRST_PAUSE].crop(title_box).tobytes()
    returned_title = find_complete(font, "Nagasaki", screens[END], (45, 14, 123, 32))
    sheets = panels.sheets_for("nagasaki_tavern_dialogue", figures)
    write(OUT, dict(candidate_sha256=release["candidate_sha256"], ordinary_gameplay=True,
        verified_common_records=records, ARM9_even_notice=even, source_requests=calls, commands=commands,
        two_identical_Naha_holds=[frames[5720], frames[6920]], wallet_balances=balances,
        earned_recruits=57, picked_even_policy=True, visible_distribution=distribution,
        returned_to_town=frames[END], town_title=returned_title, archived_ids_seen=sorted(set(REQUESTS) & {284, 318, 750, 751, 752}),
        unvisited=["Accept another round of recruitment", "Alternate local rumors and patron responses"],
        ROM_changed=False, new_editorial_credit=0, evidence=list(map(reference, (*paths, active.RELEASE, play.HISTORY))) + sheets))
    print("Verified Nagasaki's drinks, local tips, crew recruitment, even distribution and town return.")


if __name__ == "__main__":
    main()
