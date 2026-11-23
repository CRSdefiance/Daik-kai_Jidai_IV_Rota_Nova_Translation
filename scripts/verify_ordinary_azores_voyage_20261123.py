"""Verify the ordinary Ceuta voyage's warnings, floating notices, and defeat."""

from collections import Counter
from hashlib import sha256
from pathlib import Path
from struct import unpack_from

from dk4tool.patch.duel_editorial import owned_entries
from dk4tool.script.common_message_table import DIRECTORY_OFFSET, TABLE_OFFSET, common_message_entries
from scripts import observe_ordinary_azores_voyage_20261123 as replay
from scripts import verify_additional_voyages_20261123 as prior
from scripts.record_navigation_v327 import dark_text
from scripts.review_ship_loss_context_v1 import OUTPUT as CREW_REVIEW
from scripts.verify_personal_gameplay_v841 import get_machine


base, current, root = replay.base, replay.current, replay.ROOT
check, town = prior.check, prior.town
OUT = Path("translations/editorial_checkpoints/shared_display_20261123/ordinary_azores_voyage_20261123.json")
ARM_BASE = 0x02000000
DEPARTURE = 4400
END = 17450
REVIEWS = {
    97: "20261111_sailing_alerts",
    383: "20261119_sea_hazard_dialogue",
    601: "20261122_ceuta_supply_alerts",
    609: "20261122_ceuta_supply_alerts",
}
HOLDS = {
    9000: (6364, 383, "Manuel Almeida", (), "The direct warning retains the admiral's title and announces the storm immediately."),
    12480: (11690, 601, "Charles Rochefort", ("food",), "The First Mate's concise warning names the depleted supply."),
    12780: (12745, 97, "", ("Charles",), "The brief notification names the officer who gained a level."),
    13135: (13080, 97, "", ("Manuel",), "The same notification retains the separate character name when Manuel gains a level."),
    13935: (13530, 601, "Charles Rochefort", ("water",), "Water stays distinct from the earlier food warning and uses the same natural phrasing."),
    15000: (14855, 609, "Sailor", (), "The pauses and two complete rows carry the sailor from dizziness through hunger to exhaustion."),
    17225: (17191, 339, "", ("Vestaros",), "The neutral warning gives the full ship name and the immediate fact that no sailors remain."),
}


def read_snapshot(row):
    data = Path(row["path"]).read_bytes()
    assert row["read_only_export"] and len(data) == row["bytes"] == 0x400000
    assert base.digest(row["path"]) == row["sha256"]
    return data


def text_buffers(arm, raw, offsets):
    result = []
    for offset in offsets:
        start = unpack_from("<I", arm, offset)[0] - ARM_BASE
        window = raw[start:start + 256]
        result.append(window[:window.index(0)])
    return result


def empty_ship(arm, state, name):
    cpu, get = get_machine(arm, state)
    fleet = get(0xCB1A8) + 4 + 132 * get(0x2E58C)
    ship = get(0x36C70, fleet + 12)
    vtable = unpack_from("<I", cpu.mem_read(ship, 4))[0]
    getter = unpack_from("<I", cpu.mem_read(vtable + 4, 4))[0]
    field = get(getter - ARM_BASE, ship)
    assert bytes(cpu.mem_read(field, 19)).split(b"\0", 1)[0] == name
    assert get(0x55444, ship) == 0
    return dict(name_getter=getter, ship_pointer=ship, name_pointer=field, remaining_sailors=0)


def reviewed_record(key, source, installed):
    if key == 339:
        path = CREW_REVIEW
        row, = [r for r in base.load(path)["records"] if r["message_ID"] == key]
        assert all(value for gate, value in row["review"].items() if gate != "formatting")
    else:
        package = Path(f"releases/all_routes_editorial_{REVIEWS[key]}_candidate")
        path = package / "verification/registered_review.json"
        assert base.digest(path) == base.load(package / "checksums.json")[path.relative_to(package).as_posix()]
        row, = [r for r in base.load(path)["records"] if r["id"] == f"COMMON_MESSAGE_{key}"]
        assert all(row["review"].values())
    assert row["source_reference"] == town.reference(source) and row["source_hex"] == source.text.hex()
    logical = row["english"].replace("{LB}", " ").removesuffix("{PAD}")
    assert logical.split() == installed.text.decode("ascii").split(), key
    return row, dict(path=str(path), sha256=base.digest(path))


def verify_inputs():
    release = base.load(current.RELEASE)
    sha = base.digest(current.ROM)
    assert sha == release["candidate_sha256"] and base.digest(base.REGISTRY) == release["registry_sha256"]
    terminal = base.load(root / "terminal.json")
    assert terminal["ordinary_controller_inputs"] and terminal["candidate_sha256"] == sha
    assert all(base.digest(path) == digest for path, digest in terminal["evidence"].items())
    report = base.load(root / "capture/capture_report.json")
    assert report["ROM_sha256"] == sha and report["frames"] == terminal["total_frames"] == END
    assert report["cold_boot"] and not report["savestate_loaded"] and not report["callback_errors"]
    assert not any(value for key, value in report.items() if key.startswith("synthetic_"))
    donor = report["battery_save_preloaded"]
    assert donor["copied_byte_exact_before_cold_boot"]
    assert base.digest(donor["source"]) == donor["source_sha256"] == terminal["copied_save_sha256"]
    journal = base.load(root / "capture/navigation_command_journal.json")
    assert journal["ROM_sha256"] == sha and journal["last_command_frame"] == END
    commands = journal["commands_received"]
    assert commands[0]["frame"] == DEPARTURE and commands[-1]["command"] == {"stop": True}
    assert all(row["validation_passed"] for row in commands)
    tail = []
    for row, following in zip(commands[:-1], commands[1:], strict=True):
        command = row["command"]
        assert set(command) == {"until", "buttons", "duration"}
        assert command["until"] == following["frame"]
        tail.append(dict(start=row["frame"] + 1, duration=command["duration"], buttons=command["buttons"]))
    prefix = [r for r in base.load(replay.HISTORY)["scripted_input_schedule"] if r["start"] <= DEPARTURE]
    assert base.load(root / "inputs.json") == prefix
    assert report["scripted_input_schedule"] == prefix + tail
    return release, report, terminal


def main():
    release, report, terminal = verify_inputs()
    assert base.digest(current.native.CLEAN) == release["clean_input_sha256"]
    clean, image = map(base.NdsImage.open, (current.native.CLEAN, current.ROM))
    arm, common = image.read_file(current.ARM), image.read_file(current.COMMON)
    assert sha256(arm).hexdigest() == release["target_ARM9_sha256"]
    assert sha256(common).hexdigest() == release["target_COMMON_sha256"]
    source = common_message_entries(clean.read_file(current.COMMON), clean.read_file(current.ARM))
    installed = owned_entries(common, arm, sha256(arm[DIRECTORY_OFFSET:TABLE_OFFSET]).hexdigest())
    font, snapshots = check.GameAsciiFont.from_arm9(arm), {r["frame"]: r for r in report["read_only_pause_RAM_snapshots"]}
    frames = {r["frame"]: r for r in report["frames_captured"] if r["path"].endswith("_navigation.png")}
    raster, kanji = town.font_tools(image)[0], image.read_file("/GRP/KANJI.FNT")
    system = prior.font_tools(image)[0]
    requests = terminal["common_requests"]
    counts = Counter(r["message_ID"] for r in requests if r["PC"] == 0x0205528C)
    pending = {r["message_ID"] for r in base.load(current.REVIEW)["shared_consumer_binding"]["records"]}
    positions = []
    for frame in (DEPARTURE, 9000, 12480, 12780, 16830, 17225):
        state = read_snapshot(snapshots[frame])
        _, get = get_machine(arm, state)
        fleet = get(0xCB1A8) + 4 + 132 * get(0x2E58C)
        point = unpack_from("<2i", state, fleet - ARM_BASE + 0x34)
        positions.append(dict(frame=frame, map_point=point, read_only_snapshot=snapshots[frame]))
    assert [r["map_point"] for r in positions] == [
        (19339, 6005), (18527, 5700), (16999, 5700), (16778, 5165), (16799, 5692), (16848, 5523),
    ]
    rows, pictures = [], []
    for frame, (call, key, speaker, arguments, note) in HOLDS.items():
        picked = [r for r in requests if r["frame"] == call and r["message_ID"] == key]
        assert [r["PC"] for r in picked] == [0x0205528C, 0x020534F4]
        assert dict(picked[0], PC=picked[1]["PC"]) == picked[1]
        jp, en = source[key], installed[key]
        history, reference = reviewed_record(key, jp, en)
        substitutions = tuple(argument.encode("ascii") for argument in arguments)
        assert jp.text.count(b"%s") == en.text.count(b"%s") == len(substitutions)
        expanded = en.text.rstrip(b" ") % substitutions
        shot, snapshot = frames[frame], snapshots[frame]
        screen, state = check.captured(shot), read_snapshot(snapshot)
        if key == 97:
            assert expanded + b"\0" in state
            rendered = expanded
            geometry = dark_text(font, expanded.decode("ascii"), screen, (60, 260, 200, 298))
        elif key == 339:
            plain, rendered = text_buffers(arm, state, (0x54890, 0x54894))
            assert expanded == plain == rendered, (expanded, plain, rendered)
            matched, plane = prior.system_plane(system, arm, kanji, rendered, screen)
            assert matched == rendered
            geometry = dict(exact_native_plane_sha256=plane, native_ship=empty_ship(arm, state, substitutions[0]))
        else:
            plain, rendered = text_buffers(arm, state, (0x5444C, 0x54450))
            assert plain.split() == expanded.split() == rendered.split()
            plane, glyphs = town.render_portrait(raster, arm, kanji, rendered)
            assert [glyph["code"] for glyph in glyphs] == town.glyph_codes(rendered)
            assert prior.masks.mask_check(bytes(plane), 228, screen), (key, frame, rendered)
            ink, bounds = check.complete_mask(font, speaker, screen, 16, 277, (98, 97, 98))
            geometry = dict(complete_body_glyphs=len(glyphs), nameplate=dict(ink=ink, bounds=bounds))
        rows.append(dict(message_ID=key, file_path=current.COMMON, source_reference=town.reference(jp),
            current_and_installed_reference=town.reference(en), Japanese=jp.text.decode("cp932"),
            source_hex=jp.text.hex(), installed_hex=en.text.hex(), speaker=speaker or "System",
            arguments=arguments, displayed=rendered.decode("ascii"), decision="retention", localization_note=note,
            review=dict(history["review"], formatting=True), prior_review=reference, caller_requests=picked,
            exact_render_geometry=geometry, screenshot=shot, read_only_snapshot=snapshot))
        pictures.append((f"{frame} / COMMON {key} / {speaker or 'System'}", screen))
    assert not pending.intersection(counts)
    ending = check.captured(frames[END])
    assert ending.tobytes() != check.captured(frames[17225]).tobytes()
    pictures.append((f"{END} / Game Over", ending))
    sheets = []
    for index in range(0, len(pictures), 4):
        path, digest = prior.visual.make_sheet(OUT.with_name(f"ordinary_azores_voyage_{index // 4 + 1}.png"),
            pictures[index:index + 4])
        sheets.append(dict(path=str(path), sha256=digest))
    base.save(OUT, dict(candidate_sha256=release["candidate_sha256"], actual_ordinary_emulator_gameplay=True,
        copied_save_sha256=terminal["copied_save_sha256"], positions=positions, holds=rows, sheets=sheets,
        replay_input_schedule=report["scripted_input_schedule"],
        last_observed_screen=frames[END], common_getter_counts=counts, pending_common_requests=[],
        reached_game_over=True, village_discovery_docking_resupply_unvisited=True, hardware=False,
        new_translation_credit=0, evidence=terminal["evidence"] | {str(root / "terminal.json"): base.digest(root / "terminal.json"),
            str(Path(__file__)): base.digest(Path(__file__))}))
    print(f"Verified {len(rows)} ordinary holds across {len({row['message_ID'] for row in rows})} source records.")


if __name__ == "__main__":
    main()
