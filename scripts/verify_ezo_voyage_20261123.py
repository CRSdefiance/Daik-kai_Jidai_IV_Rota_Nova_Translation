"""Bind Maria's ordinary post-Nagasaki combat and crew reports to the clean game."""

import json
from collections import Counter
from struct import unpack
from types import FunctionType, SimpleNamespace

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.script.common_message_table import common_message_entries
from scripts import observe_ezo_voyage_20261123 as voyage
from scripts import register_kurushima_surrender_20261122 as earlier
from scripts import verify_genoa_copenhagen_town_20261123 as panels
from scripts.reconcile_elegy_acceptance_20261123 import common_rows
from scripts.stage_cartridge_title_20261123 import CLEAN, GATES, REGISTRY, NdsImage, digest, read, reference, sha256, write
from scripts.verify_lisbon_seoul_trend_gameplay_20261121 import mask_check
from scripts.verify_moonlit_violin_20261121 import bytes_for
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_stock_encounter_names_20261121 import read_ram


OUT = panels.OUT.with_name("maria_post_nagasaki_voyage_20261123.json")
STORY = "/data/SC3.DK4"
STORY_FRAMES = range(4630, 6031, 200)
COMMON_HOLDS = {
    3600: ((85,), ("26",), "", ("Sailing days left: about 26.",),
        "The original estimate gives an approximate duration before the player chooses a sailing mode."),
    4400: ((86,), ("3", "12", "Sky: Sunny", "Nagasaki"), "", ("3/12", "Sky: Sunny", "Departed Nagasaki."),
        "The log preserves the actual date, weather and departing port in sequence."),
    4450: ((618,), ("to the east", "Kurushima"), "Sailor",
        ("We've got company to the east!", "They're with Kurushima! Get ready", "for a fight!"),
        "The lookout's urgency, bearing and fleet affiliation lead directly into the confrontation."),
    8680: ((2078,), ("Hua",), "Sailor", ("Admiral, they've taken over Hua!",),
        "The rough exclamation reports the hostile takeover of the named vessel in the current fight."),
    11800: ((2116, 2118), (), "Sailor", ("Admiral, we're pulling out!",),
        "The present-tense announcement in the middle of battle makes clear that our side is withdrawing."),
    14340: ((14,), (), "Sailor", ("All set, then?",),
        "The short question leaves the player to confirm or revisit crew assignments."),
    14570: ((339,), ("Hua",), "", ("Hua has no sailors!",),
        "The notice reports the empty crew roster and identifies the ship that needs a decision."),
    17980: ((2680,), ("Hua",), "Sailor", ("So, we're abandoning Hua, right?",),
        "The familiar confirmation follows the Abandon Ship menu and restates the selected ship."),
    21010: ((397,), (), "Sailor", ("Admiral, it looks like the sailors", "have scurvy!"),
        "It looks like preserves the sailor's inference. It is an urgent report of a condition that appeared at sea."),
    27500: ((605,), ("water",), "Sailor", ("We're out of water!",),
        "The short alarm identifies the depleted resource immediately and keeps the original urgency."),
    27720: ((605,), ("food",), "Sailor", ("We're out of food!",),
        "The shared alarm preserves the separate food substitution when that stock also runs out."),
    28700: ((609,), (), "Sailor", ("Ugh... My head's spinning...", "I'm so hungry... I can't go on..."),
        "The three fragments progress from dizziness to hunger and finally to exhaustion."),
    31480: ((339,), ("Chun",), "", ("Chun has no sailors!",),
        "The original warning substitutes the flagship's name. With no crew on the remaining vessel, the game ends the voyage."),
}


def capture(release):
    paths = [voyage.ROOT / p for p in ("capture/capture_report.json", "capture/navigation_command_journal.json",
             "trace/requests.json", "terminal.json")]
    report, journal, trace, terminal = map(read, paths)
    assert report["ROM_sha256"] == journal["ROM_sha256"] == terminal["candidate_sha256"] == release["candidate_sha256"]
    assert report["cold_boot"] and not report["savestate_loaded"] and terminal["ordinary_controller_inputs"]
    assert not report["callback_errors"] and not any(v for k, v in report.items() if k.startswith("synthetic_"))
    assert trace["all_host_slots_restored_and_core_file_exact"] and not trace["errors"] and not trace["mismatches"]
    assert trace["source_requests"] == terminal["common_requests"]
    commands = [json.loads(line) for line in voyage.CONTROLLER.read_text("utf-8").splitlines()]
    assert commands == [row["command"] for row in journal["commands_received"]]
    assert commands[-1] == {"stop": True} and all(row["validation_passed"] for row in journal["commands_received"])
    donor = report["battery_save_preloaded"]
    assert donor["copied_byte_exact_before_cold_boot"] and digest(donor["source"]) == donor["source_sha256"] == terminal["copied_save_sha256"]
    assert all(digest(p) == h for p, h in terminal["evidence"].items())
    return report, panels.shots(report, "_navigation.png"), trace["source_requests"], dict(
        files=[reference(p) for p in paths], save=reference(donor["source"]),
        save_provenance=reference("docs/nagasaki_shiraki_v518_checkpoint.md"))


def common(clean, image, font, frames, requests):
    arm, archive = voyage.active.ARM, voyage.active.COMMON
    source = common_message_entries(clean.read_file(archive), clean.read_file(arm))
    installed = common_rows(image.read_file(archive), image.read_file(arm))
    records, figures = [], []
    for frame, (keys, arguments, speaker, lines, rationale) in COMMON_HOLDS.items():
        calls = [row for row in requests if row["message_ID"] in keys and 0 <= frame - row["frame"] <= 3000]
        assert calls, (frame, keys)
        closest_frame = max(row["frame"] for row in calls)
        calls = [row for row in calls if row["frame"] == closest_frame]
        key, = {row["message_ID"] for row in calls}
        ja, en = source[key], installed[key]
        assert ja.text.count(b"%s") == en.text.count(b"%s") == len(arguments)
        expected = (en.text % tuple(arg.encode("ascii") for arg in arguments)).decode("ascii")
        assert expected.split() == " ".join(lines).split(), (frame, expected, lines)
        screen = panels.picture(frames[frame])
        try:
            ink = panels.exact_body(font, lines, screen)
        except (AssertionError, ValueError) as error:
            raise ValueError((frame, key, lines)) from error
        records.append(dict(message_ID=key, clean_Japanese=ja.text.decode("cp932"), english=en.text.decode("ascii"),
            source_reference=panels.text_reference(ja), current_reference=panels.text_reference(en),
            source_hex=ja.text.hex(), installed_hex=en.text.hex(), speaker=speaker or "System", arguments=arguments,
            body_ink_pixels=ink, nameplate=panels.nameplate(font, speaker, screen), captured=frames[frame],
            lines=lines, original_requests=calls, rationale=rationale, decision="retention", review=dict.fromkeys(GATES, True)))
        figures.append((f"{frame} / COMMON {key}", screen))
    return records, figures


def confrontation(clean, image, release, font, frames):
    old_release, reviewed = map(read, (earlier.RELEASE, earlier.REVIEW))
    assert digest(earlier.REVIEW) == read(earlier.REVIEW.parent.parent / "checksums.json")["verification/registered_review.json"]
    assert reviewed["candidate_sha256"] == old_release["candidate_sha256"]
    origin, current = (IlnkContainer.parse(rom.read_file(STORY)).blocks[3] for rom in (clean, image))
    arm, kanji = image.read_file(voyage.active.ARM), image.read_file("/GRP/KANJI.FNT")
    paint = panels.town.clipped_renderer(SimpleNamespace(image=image, arm=arm))
    records, figures = [], []
    for frame, row in zip(STORY_FRAMES, reviewed["records"], strict=True):
        source, installed = row["source_reference"], row["registered_reference"]
        a, b = (bytes.fromhex(record["complete_command_hex"]) for record in (source, installed))
        for block, offset, command in ((origin, source["command_offset"], a), (current, installed["command_offset"], b)):
            assert block[offset:offset + len(command)] == command
        assert a[:6] == b[:6] and row["review"] == dict.fromkeys(GATES, True)
        text = bytes_for(b).replace(b"FI", b"Maria")
        display = paint(arm, kanji, text)
        page, = display["pages"]
        assert page["native_independent_plane_equal"] and display["complete_consumed_bytes"] == len(text)
        screen = panels.picture(frames[frame])
        plane = bytes.fromhex(page["native_plane_hex"])
        assert mask_check(plane, 216, screen), (row["id"], frame)
        records.append(dict(id=row["id"], file=STORY, block=3, clean_Japanese=row["Japanese"], english=row["english"],
            previous_review=reference(earlier.REVIEW), source_reference=source,
            current_reference=installed | dict(candidate_sha256=release["candidate_sha256"], block_sha256=sha256(current).hexdigest()),
            speaker=row["speaker"], nameplate=panels.nameplate(font, row["speaker"], screen),
            native_plane_sha256=sha256(plane).hexdigest(), captured=frames[frame],
            rationale=row["localization_note"], decision="retention", review=row["review"]))
        figures.append((f"{frame} / {row['speaker']}", screen))
    return records, figures


def fleet_state(clean, image, report):
    arm = image.read_file(voyage.active.ARM)
    original = clean.read_file(voyage.active.ARM)
    for start, stop in ((0xCB1A8, 0xCB1B4), (0x2E58C, 0x2E5A8), (0x36C70, 0x36C94), (0x55444, 0x5544C)):
        assert arm[start:stop] == original[start:stop]
    snapshots = {row["frame"]: row for row in report["read_only_pause_RAM_snapshots"]}
    states = {}
    for frame, expected in ((4400, [57, None]), (14130, [48, 0]), (18210, [48, None]), (29900, [12, None]), (31480, [0, None])):
        ref = snapshots[frame]
        raw = read_ram(ref)
        cpu, get = get_machine(arm, raw)
        fleet = get(0xCB1A8) + 4 + get(0x2E58C) * 132
        ships = [get(0x36C70, fleet + 12 + 8 * slot) for slot in range(5)]
        crews = [get(0x55444, ship) if ship else None for ship in ships]
        assert crews[0] == expected[0], (frame, crews)
        # The departing fleet had a crewed Hua. The departure count above refers to Maria's flagship.
        if frame != 4400:
            assert crews[1:] == [expected[1], None, None, None], (frame, crews)
        point = [round(n / 128, 3) for n in unpack("<2i", cpu.mem_read(ships[0] + 16, 8))]
        assert bytes(cpu.mem_read(0x02000000, len(raw))) == raw
        states[frame] = dict(snapshot=ref, crew_by_ship_slot=crews, flagship_map_point=point)
    return states


def main():
    release = read(voyage.active.RELEASE)
    assert digest(REGISTRY) == release["registry_sha256"] and digest(CLEAN) == release["clean_input_sha256"]
    assert digest(release["candidate"]) == release["candidate_sha256"]
    report, frames, requests, evidence = capture(release)
    clean, image = map(NdsImage.open, (CLEAN, release["candidate"]))
    font = GameAsciiFont.from_arm9(image.read_file(voyage.active.ARM))
    story, story_figures = confrontation(clean, image, release, font, frames)
    shared, shared_figures = common(clean, image, font, frames, requests)
    ship_changes = fleet_state(clean, image, report)
    sheets = FunctionType(panels.sheets_for.__code__, vars(panels) | {"OUT": OUT})
    rendered = sheets("maria_kurushima_current", story_figures, (0, 272, 256, 380))
    rendered += sheets("maria_post_nagasaki_voyage", shared_figures, (0, 272, 256, 380))
    write(OUT, dict(candidate_sha256=release["candidate_sha256"], ordinary_controller_gameplay=True,
        frames_played=report["frames"], source_and_capture_evidence=evidence, story=story, shared=shared,
        control_frames={f: frames[f] for f in (4000, 6230, 14130, 17750, 18210, 24250, 31700, 32200)},
        observed_fleet_state=ship_changes,
        requests=dict(Counter(row["message_ID"] for row in requests if row["PC"] == 0x0205528C)),
        terminal_frame=frames[report["frames"]], ezo_docking_observed=False, sheets=rendered, new_editorial_credit=0))
    print(f"Verified {len(story)} story pages and {len(shared)} ordinary shared panels on the registered ROM.")


if __name__ == "__main__":
    main()
