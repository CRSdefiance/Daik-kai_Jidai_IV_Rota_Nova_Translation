"""Bind the complete ordinary London Tavern orders to clean and installed text."""

import json
from collections import Counter

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.script.common_message_table import common_message_entries
from scripts import observe_london_tavern_20261123 as observed
from scripts import verify_genoa_copenhagen_town_20261123 as genoa
from scripts.reconcile_elegy_acceptance_20261123 import common_rows
from scripts.reconcile_genoa_acceptance_20261123 import ARM, COMMON
from scripts.stage_cartridge_title_20261123 import CLEAN, GATES, REGISTRY, NdsImage, digest, read, reference, write


OUT = genoa.OUT.with_name("london_tavern_current_20261123.json")
ITEM_ARGS = ("Blue Oak Shield", "far", "south", "far", "west")
PROPOSAL = "%s? I know the one. Try %s %s and %s %s of here."
HOLDS = {
    51: ("Barkeep", (), ("Welcome! What will you have?",),
         "A quick welcome invites the customer's order and leads straight to the menu."),
    53: ("Barkeep", (), ("5 coins.",),
         "The barkeep quotes the exact price of the first drink in a brisk reply."),
    55: ("Barkeep", ("Marie",), ("Hey, Marie! We've got a customer!",),
         "The barkeep calls Marie by name and tells her a customer is waiting."),
    56: ("Marie", (), ("On it!",),
         "Marie's quick acknowledgment answers the barkeep's call before her offer."),
    57: ("Marie", (), ("Welcome!",),
         "Keep this warmer greeting to the customer distinct from her reply to the barkeep."),
    59: ("Marie", (), ("How about one more drink?",),
         "The invitation is friendly and leaves the second drink to the customer's choice."),
    61: ("Barkeep", (), ("Ten coins.",),
         "The separate quote states the actual second-drink price. It stays distinct from the five-coin quote."),
    823: ("Barkeep", ("Bristol",), ("Have you heard of a nearby town", "called Bristol?"),
          "The question gives the town's name and proximity. Called Bristol stays together."),
    827: ("Marie", ("Hodram",), ("Hodram, huh? Cheers! Glad we met.",),
          "Marie checks his name and toasts the acquaintance in her own casual voice."),
    828: ("Marie", ("Rainbow Marbles",), ("Have you heard of Rainbow Marbles?",
          "It's out there somewhere, and they", "say it's beautiful."),
          "Keep the official name of the single collectible, the vague location and the hearsay about its beauty."),
    843: ("Marie", ITEM_ARGS, ("I know of Blue Oak Shield. You", "might find it far south and far", "west of here."),
          "Use the relic's name as Marie's question, then her answer. Keep the tentative advice and both original distance-direction pairs."),
    995: ("Marie", (), ("It's such a nuisance when people", "get drunk and fall asleep."),
          "Her complaint about other customers keeps the familiar tone and the cause of the nuisance."),
}


def main():
    root = observed.ROOT
    capture_path, trace_path, journal_path, terminal_path = (root / path for path in (
        "capture/capture_report.json", "trace/requests.json", "capture/navigation_command_journal.json", "terminal.json"))
    release = read(observed.current.RELEASE)
    capture, trace, journal, terminal = map(read, (capture_path, trace_path, journal_path, terminal_path))
    candidate_sha = release["candidate_sha256"]
    assert candidate_sha == digest(release["candidate"]) == capture["ROM_sha256"] == journal["ROM_sha256"]
    assert candidate_sha == terminal["candidate_sha256"] and digest(REGISTRY) == release["registry_sha256"]
    assert terminal["ordinary_controller_inputs"] and capture["cold_boot"] and not capture["savestate_loaded"]
    assert not capture["callback_errors"] and not any(v for k, v in capture.items() if k.startswith("synthetic_"))
    commands = [json.loads(line) for line in observed.CONTROLLER.read_text("utf-8").splitlines()]
    assert [r["command"] for r in journal["commands_received"]] == commands and commands[-1] == {"stop": True}
    assert all(r["validation_passed"] for r in journal["commands_received"])
    assert journal["last_command_frame"] == terminal["total_frames"] == capture["frames"] == 24300
    assert all(digest(p) == h for p, h in terminal["evidence"].items())
    donor = capture["battery_save_preloaded"]
    assert donor["copied_byte_exact_before_cold_boot"] and digest(donor["source"]) == terminal["copied_save_sha256"]
    assert trace["all_host_slots_restored_and_core_file_exact"] and not trace["errors"] and not trace["mismatches"]
    calls = trace["source_requests"]
    assert calls == terminal["common_requests"]
    counts = Counter(row["message_ID"] for row in calls[::2])
    assert set(counts) == set(HOLDS) and counts[53] == counts[823] == counts[59] == counts[61] == 6
    assert counts[828] == counts[995] == 1 and counts[843] == 3
    frames = genoa.shots(capture, "_navigation.png")
    clean, installed = map(NdsImage.open, (CLEAN, release["candidate"]))
    assert digest(CLEAN) == release["clean_input_sha256"]
    jp = common_message_entries(clean.read_file(COMMON), clean.read_file(ARM))
    arm = installed.read_file(ARM)
    en = common_rows(installed.read_file(COMMON), arm)
    font = GameAsciiFont.from_arm9(arm)
    rows, figures = {}, []
    for first, second in zip(calls[::2], calls[1::2], strict=True):
        assert first["PC"] == 0x0205528C and second == first | {"PC": 0x020534F4}
        key = first["message_ID"]
        frame = min(n for n in frames if n > first["frame"])
        assert frame - first["frame"] < 400
        speaker, args, lines, reason = HOLDS[key]
        assert jp[key].text.count(b"%s") == en[key].text.count(b"%s") == len(args)
        assert (en[key].text % tuple(arg.encode("ascii") for arg in args)).decode("ascii").split() == " ".join(lines).split()
        screen = genoa.picture(frames[frame])
        evidence = dict(frame=frame, requests=[first, second], capture=frames[frame],
                        body_ink_pixels=genoa.exact_body(font, lines, screen),
                        complete_nameplate=genoa.nameplate(font, speaker, screen))
        if key in rows:
            rows[key]["holds"].append(evidence)
            continue
        figures.append((f"{frame} / COMMON {key}", screen))
        gates = dict.fromkeys(GATES, True)
        row = dict(message_ID=key, speaker=speaker, arguments=args, lines=lines, holds=[evidence],
            clean_Japanese=jp[key].text.decode("cp932"), source_reference=genoa.text_reference(jp[key]),
            installed_reference=genoa.text_reference(en[key]), source_hex=jp[key].text.hex(),
            installed_hex=en[key].text.hex(), rationale=reason, review=gates, decision="retention")
        if key == 843:
            gates["formatting"] = False
            row.update(decision="revision proposed", proposal=PROPOSAL,
                finding="The shield's name sounds bare after 'I know of'. The displayed wrap splits 'far west' and leaves 'west of here.' alone.")
        rows[key] = row

    for frame in (3200, 23900):
        screen = genoa.picture(frames[frame])
        genoa.find_mask(font, "London", screen, (40, 9, 111, 38))
    sheets = genoa.sheets_for("london_tavern_ordinary", figures)
    write(OUT, dict(candidate_sha256=candidate_sha, ordinary_controller_inputs=True, cold_boot=True,
        source_battery_save=reference(donor["source"]), observed_orders=counts[53], distinct_dialogue=len(rows),
        total_dialogue_holds=sum(counts.values()), records=list(rows.values()), return_to_London=frames[23900],
        unvisited=["Marie's gift transaction and other relationship branches", "Other relic-location selectors"],
        contact_sheets=sheets, trace=reference(trace_path), release=reference(observed.current.RELEASE),
        capture=reference(capture_path), journal=reference(journal_path), editorial_credit_added=0, changed_ROM=False))
    print(f"Verified {sum(counts.values())} holds across {len(rows)} distinct London Tavern lines.")


if __name__ == "__main__":
    main()
