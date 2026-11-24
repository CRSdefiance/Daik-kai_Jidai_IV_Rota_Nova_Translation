"""Verify the Copenhagen and Narvik exchanges and preflight the lookout reflow."""

import json
from inspect import getsource
from pathlib import Path
from struct import unpack_from
from types import FunctionType, SimpleNamespace

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.patch.duel_editorial import owned_entries
from dk4tool.script.common_message_table import DIRECTORY_OFFSET, TABLE_OFFSET, common_message_entries
from scripts import observe_copenhagen_narvik_20261124 as ordinary
from scripts import observe_narvik_focused_visit_20261124 as focused
from scripts import read_narvik_navigation_20261124 as navigation
from scripts import stage_sea_approach_village_review_v1 as sea
from scripts import verify_genoa_copenhagen_town_20261123 as panels
from scripts.record_navigation_v327 import dark_text
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.stage_cartridge_title_20261123 import CLEAN, GATES, REGISTRY, NdsImage, digest, read, reference, sha256, write
from scripts.stage_expedition_report_wraps_20261115 import owned_deployment
from scripts.verify_lisbon_azores_voyage_20261123 import load_exact, text_at


RELEASE = ordinary.current.RELEASE
OUT = panels.OUT.with_name("copenhagen_narvik_20261124.json")
KEY = 1320
PROPOSED = "Admiral, we've spotted a village!"
LOOKOUT = "Manuel Almeida"
MATE = "Charles Rochefort"
WORKER = "Port Worker"
PORT_CONTEXT = ("Copenhagen quotes a resupply price and warns of the short crew before departure. "
                "After the fleet sails, Manuel asks whether to stop again. The player declines and continues.")
VILLAGE_CONTEXT = ("Manuel sights the village, the discovery notice names it, and Charles proposes docking. "
                   "At Narvik, the villagers provide supplies and repairs, and then accept the promised words.")
ORDINARY = (
    (3520, 49, WORKER, ("16",), ("Want to resupply for 16 gold?",),
     "The worker offers to resupply the fleet for 16 gold.",
     "The price and decision are explicit before payment. The brief question suits the worker."),
    (4160, 28, WORKER, (), ("You need more sailors on one ship.", "Check fleet setup before you sail."),
     "One ship is short of sailors. The worker advises checking the fleet's assignments before leaving.",
     "Two sentences distinguish the immediate problem and the advice, and both fit on complete rows."),
    (4480, 85, "", ("78",), ("Sailing days left: about 78.",),
     "The current provisions allow approximately 78 days at sea.",
     "About preserves the estimate, and the count is clear before the departure choice."),
    (5120, 86, "", ("9", "19", "Sky: Sunny", "Copenhagen"), ("9/19", "Sky: Sunny", "Departed Copenhagen."),
     "The departure log gives the month, day, weather and port.",
     "The short American date and separate weather and departure rows retain all four runtime values."),
    (6460, 70, LOOKOUT, ("Copenhagen",), ("Shall we stop at Copenhagen?",),
     "Manuel politely asks whether to call at Copenhagen.",
     "The courteous question fits Manuel and leaves both answers open."),
    (7250, 97, "", ("Hodram",), ("Hodram leveled up!",),
     "The game announces Hodram's level increase.",
     "The familiar announcement fits the temporary sailing notice and uses the supplied character name."),
)
FOCUSED = (
    (5400, KEY, LOOKOUT, (), ("Admiral, we've got", "a village in sight!"),
     "The lookout respectfully and emphatically tells the admiral that a village is visible.",
     "We've spotted keeps Manuel's watchful tone, the address and the discovery. The full exclamation fits one native line."),
    (5800, 297, "", ("Narvik",), ("Discovered Narvik.",),
     "The game announces discovery of the selected settlement.",
     "The short notice names the village for the first time and stays distinct from the docking choice."),
    (6200, 65, MATE, ("Narvik",), ("Dock at Narvik?",),
     "Charles asks whether to stop at the named village.",
     "The concise question invites the decision without implying the fleet has already docked."),
    (7000, 1321, MATE, (), ("The villagers shared", "their food and water with us."),
     "The villagers shared their food and water with the fleet.",
     "The second row keeps food and water together, and the wording acknowledges the villagers' generosity."),
    (7700, 1336, MATE, (), ("The villagers took care", "of our ship repairs."),
     "The villagers repaired the fleet's ship or ships.",
     "The phrasing acknowledges the villagers' work and applies to one ship or several."),
    (12600, 296, "", ("Svartisen",), ("Is Svartisen all right?",),
     "The game asks the player to confirm the entered words.",
     "The confirmation repeats the complete entry so the player can correct it before submitting."),
)
VILLAGE_TEXT = {
    "VILLAGE_MESSAGE_0": (8400, MATE, ("Admiral, the village chief asks to", "hear the promised words."),
        "The request keeps the chief, the address Admiral and the purpose of the visit clear."),
    "VILLAGE_MESSAGE_4": (8760, "", ("Enter the promised words.",),
        "The direct instruction introduces the keyboard and repeats the term used by Charles."),
    "VILLAGE_ANSWER_15": (12200, "", (),
        "Svartisen is the accepted name and matches the keyboard and confirmation display exactly."),
    "VILLAGE_MESSAGE_1": (13000, MATE, ('They say it means "the glacier', 'called Black Ice".'),
        "Charles attributes the explanation to the villagers and retains the clue as a quotation."),
    "VILLAGE_CLUE_15": (13000, MATE, ('They say it means "the glacier', 'called Black Ice".'),
        "The common term glacier and the name Black Ice match the source description and the accepted answer."),
    "VILLAGE_MESSAGE_2": (13400, MATE, ("Starting with your next visit, you",
        "can use the trading post, tavern,", "and other facilities."),
        "The notice says when access starts and gives the two examples the Japanese names."),
}


def capture(run, release, location_only=False):
    scope = vars(panels) | dict(observed=SimpleNamespace(ROOT=run.ROOT.parent))
    if location_only:
        report = read(run.ROOT / "capture/capture_report.json")
        fixture, = report["synthetic_location_fixtures"]
        assert fixture["village_id"] == run.NARVIK
        assert fixture["only_eight_ship_coordinate_bytes_owned"]
        assert not any(value for key, value in report.items()
                       if key.startswith("synthetic_") and key != "synthetic_location_fixtures")
        source = checked_text(getsource(panels.capture), {
            'terminal["ordinary_controller_inputs"]': 'terminal["ordinary_controller_inputs_after_location_setup"]',
            'and not any(v for k, v in report.items() if k.startswith("synthetic_"))': "",
        })
        exec(compile(source, __file__ + "::position-only-capture", "exec"), scope)
        verify = scope["capture"]
    else:
        fixture = None
        verify = FunctionType(panels.capture.__code__, scope)
    frames, calls, evidence = verify(run.ROOT.name, release)
    assert len(calls) % 2 == 0
    for first, copied in zip(calls[::2], calls[1::2], strict=True):
        assert first["PC"] == 0x0205528C and copied == first | {"PC": 0x020534F4}
    return frames, calls[::2], evidence | dict(controller=reference(run.CONTROLLER), location_fixture=fixture)


def review_holds(specs, frames, calls, source, installed, font, context):
    records = []
    for frame, key, speaker, args, lines, gloss, reason in specs:
        request, = [row for row in calls if row["message_ID"] == key and 0 <= frame - row["frame"] < 500]
        ja, en = source[key], installed[key]
        assert ja.text.count(b"%s") == en.text.count(b"%s") == len(args), (key, ja.text, en.text)
        english = " ".join(en.text.decode("ascii").split())
        assert english % args == " ".join(lines), (key, english, args)
        picture = panels.picture(frames[frame])
        try:
            if key == 97:
                body = dark_text(font, lines[0], picture, (60, 260, 200, 298))
            else:
                body = panels.exact_body(font, lines, picture)
            plate = panels.nameplate(font, speaker, picture)
        except (AssertionError, ValueError) as error:
            raise ValueError((frame, key, lines)) from error
        old_ref = panels.text_reference(en) | dict(exact_hex=en.text.hex())
        records.append(dict(id=f"COMMON_MESSAGE_{key}", message_ID=key, file_path=sea.COMMON,
            speaker=speaker or "System",
            clean_Japanese=ja.text.decode("cp932"), source_meaning=gloss, current_English=english,
            english=PROPOSED if key == KEY else english, context=context, localization_note=reason,
            source_reference=panels.text_reference(ja) | dict(exact_hex=ja.text.hex()),
            current_reference=old_ref, installed_reference=old_ref, source_hex=ja.text.hex(), current_hex=en.text.hex(),
            current_layout=lines, arguments=args, body=body, nameplate=plate, capture=frames[frame], request=request,
            decision="revision" if key == KEY else "retention", review=dict.fromkeys(GATES, True)))
    return records


def preflight(release, row, clean_arm, installed):
    ctx = sea.RegisteredRuntime(RELEASE, release["own_registered_startup"], captain=3)
    original = read(sea.OUTPUT)
    assert original["source_ROM_sha256"] == release["clean_input_sha256"]
    group, = [item for item in original["exact_native_groups"] if item["first_ID"] <= KEY <= item["last_ID"]]
    assert group["original_role_argument"] == 7 and group["table_slots"][-1] == KEY and not group["arguments"]
    for call in group["native_callers"]:
        start = call["load_PC"] - sea.BASE
        assert ctx.arm[start:start + 12] == clean_arm[start:start + 12] == bytes.fromhex(call["clean_and_current_hex"])
    at = group["table"] - sea.BASE
    assert ctx.arm[at:at + 32] == clean_arm[at:at + 32]
    assert ctx.arm[0x53D44:0x53DCC] == clean_arm[0x53D44:0x53DCC]
    current = installed[KEY].text
    assert current == b" Admiral, we've got\n  a village in sight!"
    target = PROPOSED.encode("ascii").ljust(len(current))
    directory = sha256(ctx.arm[DIRECTORY_OFFSET:TABLE_OFFSET]).hexdigest()
    rows = owned_entries(ctx.common, ctx.arm, directory)
    new, rebound, allocation = owned_deployment(ctx.common, ctx.arm, rows, {KEY: target})
    assert [b.message_id for a, b in zip(rows, rebound, strict=True) if a != b] == [KEY]
    candidate = sea.with_components(ctx, ctx.arm, new)
    raster, _, _ = sea.font_tools(ctx.image)
    kanji = ctx.image.read_file("/GRP/KANJI.FNT")
    pages, native = [], []
    for label, runtime, raw in (("Current", ctx, current), ("Proposed", candidate, target)):
        display, receipt = sea.original_portrait(runtime, row, group, raw, b"")
        plane, events = sea.render_portrait(raster, ctx.arm, kanji, display)
        visible = [part.strip() for part in display.split(b"\n")]
        assert all(0 < len(line) <= 36 for line in visible)
        assert all(0 <= item["x"] < 228 and 0 <= item["y"] < 64 for item in events)
        assert [events[0]["code"], events[-1]["code"]] == [visible[0][0], visible[-1][-1]]
        if label == "Proposed":
            assert visible == [PROPOSED.encode("ascii")]
            assert [event["code"] for event in events] == list(PROPOSED.replace(" ", "").encode("ascii"))
        pages.append((label, plane))
        native.append(receipt | dict(display_hex=display.hex(), lines=[part.decode("ascii") for part in visible],
                                     complete_visible_glyphs=len(events), ink_sha256=sha256(plane).hexdigest()))
    preview = OUT.with_suffix("")
    preview.mkdir(exist_ok=True)
    row.update(proposed_hex=target.hex(), proposed_reference=panels.text_reference(rebound[KEY]))
    return dict(proposed_sheets=sea.portrait_sheets(preview, pages), native=native,
                proposed_COMMON_sha256=sha256(new).hexdigest(), allocation=allocation[KEY],
                original_voice_table=group["table"], historical_review=reference(sea.OUTPUT))


def village_words(release, clean_arm, arm, frames, font):
    manuscript = Path("translations/village_promised_words_manuscript_v1.json")
    startup = Path(release["own_registered_startup"])
    assert digest(startup) == release["own_registered_startup_sha256"]
    checked = read(startup)
    capture = Path(checked["exact_matching_frames"][0]["path"]).parent / "capture_report.json"
    report = read(capture)
    assert report["ROM_sha256"] == release["candidate_sha256"]
    ram = load_exact(report["read_only_RAM_snapshot"])
    rows = []
    for row in read(manuscript)["records"]:
        if row["id"] not in VILLAGE_TEXT:
            continue
        frame, speaker, lines, reason = VILLAGE_TEXT[row["id"]]
        field = row["field"]
        old, new = (unpack_from("<I", data, field)[0] for data in (clean_arm, arm))
        assert old == row["source_pointer"] and new != old
        source = text_at(clean_arm, old)
        current = text_at(ram, new)
        assert source.hex() == row["source_hex"] and source.decode("cp932") == row["japanese"]
        english = " ".join(current.decode("ascii").split())
        expected = row["english"].replace("Captain,", "Admiral,", 1)
        assert english == expected
        screen = panels.picture(frames[frame])
        ink = panels.exact_body(font, lines, screen) if lines else panels.find_mask(font, english, screen, (45, 234, 140, 262))
        source_ref = dict(path=sea.ARM, pointer_field_offset=field, native_text_address=old, exact_hex=source.hex())
        current_ref = dict(path=sea.ARM, pointer_field_offset=field, native_text_address=new, exact_hex=current.hex())
        rows.append(dict(id=row["id"], file_path=sea.ARM, clean_Japanese=row["japanese"], speaker=speaker or "System",
            source_reference=source_ref, current_reference=current_ref, installed_reference=current_ref,
            source_meaning=row["source_meaning"], context=VILLAGE_CONTEXT, english=english,
            localization_note=reason, decision="retention", review=dict.fromkeys(GATES, True),
            capture=frames[frame], body=ink, nameplate=panels.nameplate(font, speaker, screen)))
    assert len(rows) == len(VILLAGE_TEXT)
    return rows, dict(manuscript=reference(manuscript), startup=reference(startup),
                      initialized_RAM=reference(report["read_only_RAM_snapshot"]["path"]))


def main():
    release = read(RELEASE)
    assert digest(REGISTRY) == release["registry_sha256"] and digest(CLEAN) == release["clean_input_sha256"]
    assert digest(release["candidate"]) == release["candidate_sha256"]
    en, ja = [NdsImage.open(path) for path in (release["candidate"], CLEAN)]
    arm, clean_arm = [rom.read_file(sea.ARM) for rom in (en, ja)]
    common = en.read_file(sea.COMMON)
    assert sha256(arm).hexdigest() == release["target_ARM9_sha256"]
    assert sha256(common).hexdigest() == release["target_COMMON_sha256"]
    installed = panels.common_rows(common, arm)
    source = common_message_entries(ja.read_file(sea.COMMON), clean_arm)
    font = panels.GameAsciiFont.from_arm9(arm)
    del en, ja
    frames, calls, played = capture(ordinary, release)
    focus, requests, near_village = capture(focused, release, location_only=True)
    records = review_holds(ORDINARY, frames, calls, source, installed, font, PORT_CONTEXT)
    records += review_holds(FOCUSED, focus, requests, source, installed, font, VILLAGE_CONTEXT)
    words, words_inputs = village_words(release, clean_arm, arm, focus, font)
    records.extend(words)
    archive = ordinary.ROOT / "capture/lossless_ram_archive.jsonl"
    snapshots = {item["frame"]: item for item in map(json.loads, archive.read_text(encoding="utf-8").splitlines())}
    positions = {}
    for frame in (5940, 6460, 8150, 8770):
        snapshot = Path(snapshots[frame]["gzip_path"])
        assert digest(snapshot) == snapshots[frame]["gzip_sha256"]
        assert sha256(navigation.load_snapshot(snapshot)).hexdigest() == snapshots[frame]["sha256"]
        positions[str(frame)] = navigation.position(snapshot)
    assert max(frames) == 9470 and max(focus) == 13800
    menus = {frame: [panels.find_line(font, word, panels.picture(focus[frame]), range(69, 120),
                                     range(240, 337), (8, 8, 8))
                     for word in words]
             for frame, words in ((6600, ("Resupply", "Repair Ship", "Recruit Sailors", "Set Sail", "Promised Words")),
                                  (13800, ("Recruit Sailors", "Set Sail")))}
    result = dict(translation_policy="natural-dialogue-v2", target_locale="en-US", encoder="dialogue-relocatable-v1",
        review_gates=list(GATES), candidate_sha256=release["candidate_sha256"], source_sha256=release["clean_input_sha256"],
        unchanged_ARM9_sha256=release["target_ARM9_sha256"], records=records, ordinary_copenhagen=played,
        location_only_narvik=near_village, read_only_positions=positions, lossless_RAM_archive=reference(archive),
        promised_words_references=words_inputs, actual_village_menus=menus, accepted_reply=focus[13000],
        next_visit_facilities=focus[13400], unanchored_level_up_requests=calls[6:],
        independent_new_coverage_credit=0, new_candidate_registered=False)
    result.update(preflight(release, next(row for row in records if row["message_ID"] == KEY), clean_arm, installed))
    validate_natural_dialogue_batch(result)
    write(OUT, result)
    print(f"Verified {len(records)} current holds and one proposed native layout.")


if __name__ == "__main__":
    main()
