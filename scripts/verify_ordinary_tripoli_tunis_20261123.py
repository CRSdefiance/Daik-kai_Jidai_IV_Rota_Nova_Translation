"""Verify naturally selected battle, docking and Inn dialogue in the original game."""

from PIL import Image, ImageDraw

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.script.common_message_table import common_message_entries
from scripts import observe_ordinary_tripoli_tunis_20261123 as replay
from scripts.check_tavern_round_digits_20261120 import wallet
from scripts.reconcile_elegy_acceptance_20261123 import common_rows
from scripts.reconcile_editorial_acceptance_20261123 import ARM, BASE, COMMON, GATES, OUT
from scripts.stage_cartridge_title_20261123 import CLEAN, REGISTRY, NdsImage, digest, read, reference, write
from scripts.verify_azores_return_20261123 import picture, shots
from scripts.verify_confirmed_name_widget_pixels_v198 import complete_mask
from scripts.verify_lisbon_azores_voyage_20261123 import body_mask, load_exact, town
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_plaque_release_v247 import find_mask


REPORT = OUT.with_name("tripoli_tunis_current_20261123.json")
SHEET = REPORT.with_suffix(".png")
CHARLES = "Charles Rochefort"
PANELS = {
    "battle": {
        10090: (614, CHARLES, ("to the southeast", "Hayreddin Clan"),
                ("Fleet spotted to the southeast!", "They belong to Hayreddin Clan!", "We're getting ready for battle!"),
                "The lookout reports a bearing, identifies the other faction and says the fleet is getting ready."),
        11340: (2006, CHARLES, (), ("Admiral, our flagship's been hit!", "We can't stop the flooding!"),
                "Charles first identifies the damaged flagship, then makes clear that the flooding is beyond their control."),
        11440: (2138, CHARLES, (), ("Our flagship is down. We've lost!",),
                "The result states what happened and immediately confirms defeat."),
    },
    "recovery": {
        3800: (85, "", ("38",), ("Sailing days left: about 38.",),
               "The departure estimate keeps its approximation and uses ordinary digits."),
        4500: (86, "", ("10", "16", "Sky: Cloudy", "Tripoli"), ("10/16", "Sky: Cloudy", "Departed Tripoli."),
               "The sailing notice presents the original date, weather and departure town in their own rows."),
        7740: (65, CHARLES, ("Tunis",), ("Dock at Tunis?",),
               "The brief question identifies the destination and leaves the decision with the admiral."),
        12940: (1180, "Innkeeper", ("30",), ("You're staying 30 nights, then?",),
                "The innkeeper checks the exact duration using a natural conversational tag."),
    },
}
TRANSITIONS = {"battle": (11640, "Game Over"), "recovery": (15000, "Inn menu after the stay")}


def verify_inputs(case, release):
    root = replay.ROOT / case
    cap, req, end = (root / item for item in ("capture/capture_report.json", "requests.json", "terminal.json"))
    capture, requests, terminal = map(read, (cap, req, end))
    assert capture["ROM_sha256"] == terminal["ROM_sha256"] == release["candidate_sha256"]
    assert capture["cold_boot"] and not capture["savestate_loaded"] and not capture["callback_errors"]
    assert not any(value for key, value in capture.items() if key.startswith("synthetic_"))
    events, frames, last, _, donor = replay.schedule(case)
    assert capture["frames"] == terminal["completed_frames"] == last
    assert capture["scripted_input_schedule"] == events and capture["exact_requested_capture_frames"] == list(frames)
    assert capture["battery_save_preloaded"]["source_sha256"] == donor["source_sha256"] == digest(donor["source"])
    assert capture["battery_save_preloaded"]["copied_byte_exact_before_cold_boot"]
    assert requests["all_host_slots_restored_and_core_file_exact"] and not requests["errors"] and not requests["mismatches"]
    assert all(digest(path) == proof for path, proof in terminal["evidence"].items())
    assert requests["source_requests"] == terminal["target_COMMON_calls"]
    return capture, requests["source_requests"], [reference(path) for path in (cap, req, end)]


def panels(cases, font, capture, calls, source, installed, images):
    held = shots(capture, "_cold_boot.png")
    records = []
    for frame, (key, speaker, args, lines, reason) in cases.items():
        pairs = [row for row in calls if row["message_ID"] == key and 0 <= frame - row["frame"] <= 400]
        a, b = pairs
        assert a["PC"] == 0x0205528C and b == a | {"PC": 0x020534F4}
        jp, en = source[key], installed[key]
        assert jp.text.count(b"%s") == en.text.count(b"%s") == len(args)
        formatted = (en.text % tuple(arg.encode("ascii") for arg in args)).decode("ascii")
        assert formatted.split() == " ".join(lines).split()
        screen = picture(held[frame])
        body = body_mask(font, screen, lines)
        name = complete_mask(font, speaker, screen, 16, 277, (98, 97, 98)) if speaker else None
        images.append((f"{frame} / COMMON {key}", screen))
        records.append(dict(message_ID=key, frame=frame, speaker=speaker, runtime_arguments=args, lines=lines,
            exact_clean_reference=town.reference(jp), exact_installed_reference=town.reference(en),
            clean_Japanese=jp.text.decode("cp932"), source_hex=jp.text.hex(), installed_hex=en.text.hex(),
            decision="retention", reason=reason, review=dict.fromkeys(sorted(GATES), True),
            full_body_glyphs=body, full_nameplate_mask=name, original_requests=pairs, image=held[frame]))
    return records


def state(arm, snapshot):
    cpu, get = get_machine(arm, load_exact(snapshot))
    assert get(0x7F244) == 1
    fleet = get(0xCB1A8) + 4 + 132 * get(0x2E58C)
    flagship = get(0x36C70, fleet + 12)
    return [get(0x5543C, flagship), get(0x55444, flagship)]


def main():
    release = read(replay.RELEASE)
    assert digest(release["candidate"]) == release["candidate_sha256"]
    assert digest(REGISTRY) == release["registry_sha256"] and digest(CLEAN) == release["clean_input_sha256"]
    clean, rom = map(NdsImage.open, (CLEAN, release["candidate"]))
    ja, arm = clean.read_file(ARM), rom.read_file(ARM)
    source = common_message_entries(clean.read_file(COMMON), ja)
    installed = common_rows(rom.read_file(COMMON), arm)
    font = GameAsciiFont.from_arm9(arm)
    images, results = [], {}
    for case in PANELS:
        capture, calls, evidence = verify_inputs(case, release)
        frames = shots(capture, "_cold_boot.png")
        records = panels(PANELS[case], font, capture, calls, source, installed, images)
        transition, label = TRANSITIONS[case]
        images.append((label, picture(frames[transition])))
        snapshots = {row["frame"]: row for row in capture["read_only_capture_RAM_snapshots"]}
        details = {}
        if case == "battle":
            health = {frame: state(arm, snapshots[frame]) for frame in (10090, 11220, 11340, 11440)}
            assert health == {10090: [60, 39], 11220: [11, 24], 11340: [0, 24], 11440: [0, 24]}
            details.update(flagship_hull_and_crew=health, trace_only_message_IDs=[2164, 2172],
                           returned_to_title_after_game_over_frame=12140)
        else:
            charles = {}
            for f in (10540, 18740):
                screen = picture(frames[f])
                charles[f] = [find_mask(font, text, screen, region) for text, region in (
                    ("Charles Jean Rochefort", (80, 28, 256, 54)),
                    ("Healthy", (48, 104, 121, 124)),
                    ("Relaxed", (48, 124, 121, 144)),
                )]
            assert not any(394 <= call["message_ID"] <= 400 for call in calls)
            before, after = (wallet(arm, load_exact(snapshots[f])) for f in (12940, 15000))
            assert (before, after) == (7454, 7424)
            details.update(charles_status_masks=charles, inn_gold_before_and_after=[before, after],
                           observed_scurvy=False)
        results[case] = dict(ordinary_controller_and_stylus_inputs=True, fixture=False, cold_boot=capture["cold_boot"],
            reviews=records, native_requests=calls, transition=frames[transition], details=details, evidence=evidence)

    contact = Image.new("RGB", (3 * 268, 3 * 218), "#273034")
    draw = ImageDraw.Draw(contact)
    for i, (label, image) in enumerate(images):
        x, y = 268 * (i % 3) + 6, 218 * (i // 3)
        draw.text((x, y + 4), label, fill="white")
        contact.paste(image.crop((0, 192, 256, 384)), (x, y + 22))
    contact.save(SHEET)
    write(REPORT, dict(candidate_sha256=release["candidate_sha256"], clean_input_sha256=release["clean_input_sha256"],
        runs=results, registered_release=reference(replay.RELEASE), contact_sheet=reference(SHEET),
        unvisited=["Scurvy in the current ROM on this voyage", "Other alert voice selections", "Handheld hardware"],
        editorial_credit_added=0, changed_ROM=False))
    print("Verified seven current dialogue holds, a natural battle defeat and an ordinary Tunis Inn visit.")


if __name__ == "__main__":
    main()
