"""Bind the ordinary Stockholm arrival and both recruiting outcomes to the installed text."""

from hashlib import sha256
from pathlib import Path
from types import FunctionType, SimpleNamespace

from PIL import Image
from dk4tool.dialogue.reviewed_choice_object_v2 import labels
from scripts import observe_riga_auto_dock_20261124 as run
from scripts import verify_athens_auto_move_20261124 as auto
from scripts.verify_personal_gameplay_v841 import get_machine


panels, earlier = auto.panels, auto.earlier
OUT = auto.OUT.with_name("riga_stockholm_auto_dock_20261124.json")
STORY_REVIEW = Path("releases/all_routes_editorial_20261122_hodram_B131_B150_candidate")
COMMON = {
    28: (True, 3940, (), "Port Worker", "The warning identifies the understaffed ship and tells the player what to check before sailing."),
    814: (False, 4400, (), "Port Worker", "The port worker notices the crew's fatigue and points the player toward the inn in a friendly question."),
    85: (False, 4800, ("78",), None, "The status line presents the sailing estimate as approximate."),
    65: (False, 7600, ("Stockholm",), "Gerhard Adernkatz", "Gerhard asks for a decision about the port actually selected on the map."),
    51: (True, 10130, (), "Barkeep", "The welcome gives way to the drink and recruiting menu after Gerhard's lesson."),
}
STORY_FRAMES = {5: (False, 8640), 9: (False, 8950), 25: (True, 9550), 28: (True, 9820), 33: (False, 9820)}
RECRUITING = "Buy the house a round and anyone looking for work will come over. Then you can recruit them quickly."


def run_capture(folder, release):
    capture = FunctionType(panels.capture.__code__, vars(panels) | {"observed": SimpleNamespace(ROOT=folder.parent)})
    navigation, calls, evidence = capture(folder.name, release)
    report = auto.read(folder / "capture/capture_report.json")
    stills = {r["frame"]: r for r in report["frames_captured"] if r["path"].endswith("_cold_boot.png")}
    expected = set(COMMON) if folder != run.ROOT else set(COMMON) - {51}
    assert {r["message_ID"] for r in calls} == expected
    return navigation | stills, calls, evidence, report


def dock_state(arm, report):
    snapshot, = [r for r in report["read_only_pause_RAM_snapshots"] if r["frame"] == 8000]
    path = Path(snapshot["path"])
    assert snapshot["read_only_export"] and auto.digest(path) == snapshot["sha256"]
    data = path.read_bytes()
    cpu, get = get_machine(arm, data)
    party = get(0x2E58C)
    fleet = get(0xCB1A8) + 4 + 132 * party
    raw_town = bytes(cpu.mem_read(fleet + 0x3C, 1))
    assert get(0x7F244) == party == 1 and get(0xB65E4) == get(0x34674, fleet) == raw_town[0] == 7
    assert bytes(cpu.mem_read(0x02000000, 0x400000)) == data
    return dict(snapshot=snapshot, captain=party, current_town=7, native_docking_getter=7,
                fleet_docking_byte_address=fleet + 0x3C, fleet_docking_byte=raw_town.hex())


def common_records(runs, clean, rom, arm, font, kanji):
    source = panels.common_message_entries(clean.read_file(auto.COMMON), clean.read_file(auto.ARM))
    installed = auto.common_rows(rom.read_file(auto.COMMON), arm)
    system = earlier.font_tools(rom)[0]
    rows, figures = [], []
    for key, (upper, frame, args, speaker, rationale) in COMMON.items():
        shots, calls, _, _ = runs[upper]
        first, second = [r for r in calls if r["message_ID"] == key]
        assert first["PC"] == 0x0205528C and second == first | {"PC": 0x020534F4}
        assert 0 < frame - first["frame"] <= 400
        jp, text = source[key], installed[key]
        assert jp.text.count(b"%s") == text.text.count(b"%s") == len(args)
        raw = (text.text % tuple(a.encode("ascii") for a in args)).rstrip(b" ")
        shot = shots[frame]
        screen = panels.picture(shot)
        if speaker:
            lines = tuple(line.strip() for line in raw.decode("ascii").splitlines())
            if key == 28:
                lines = ("You need more sailors on one ship.", "Check fleet setup before you sail.")
                assert " ".join(lines).encode("ascii") == raw
            pixels = panels.exact_body(font, lines, screen)
            glyphs = dict(body_ink_pixels=pixels, nameplate=panels.nameplate(font, speaker, screen))
        else:
            _, mask = earlier.system_plane(system, arm, kanji, raw, screen)
            glyphs = dict(native_plane_sha256=mask)
        rows.append(dict(id=f"COMMON_MESSAGE_{key}", clean_Japanese=jp.text.decode("cp932"), english=raw.decode("ascii"),
            source_reference=panels.text_reference(jp) | {"exact_hex": jp.text.hex()},
            installed_reference=panels.text_reference(text) | {"exact_hex": text.text.hex()},
            speaker=speaker, context="Departure from Riga, Auto Move and arrival at Stockholm.", arguments=args,
            rationale=rationale, decision="retention", review=dict.fromkeys(auto.GATES, True),
            complete_glyphs=glyphs, capture=shot, requests=(first, second)))
        figures.append((rows[-1]["id"], screen))
    return rows, figures


def story_records(runs, clean, rom, arm, font, kanji, release):
    relative = "verification/registered_review.json"
    ledger = STORY_REVIEW / relative
    assert auto.digest(ledger) == auto.read(STORY_REVIEW / "checksums.json")[relative]
    jp, en = (image.read_file(panels.STORY) for image in (clean, rom))
    source, installed = (panels.IlnkContainer.parse(data).blocks[134] for data in (jp, en))
    ctx = SimpleNamespace(image=rom, arm=arm)
    paint, fe = panels.town.clipped_renderer(ctx), panels.town.current_fe_painter(ctx)
    rows, figures, proposal = [], [], None
    for row in auto.read(ledger)["records"]:
        if row["block"] != 134:
            continue
        src, dst = row["source_reference"], row["registered_reference"]
        assert src["archive_sha256"] == sha256(jp).hexdigest() and src["block_sha256"] == sha256(source).hexdigest()
        body, start = bytes.fromhex(src["exact_body_hex"]), src["offset"]
        body_start = start + (row["source_selector"] is not None)
        assert source[body_start:body_start + len(body)] == body and body.decode("cp932") == row["Japanese"]
        native = panels.exact_command(installed, dst)
        assert row["review"] == dict.fromkeys(auto.GATES, True)
        if row["id"].startswith("SC1_B134_CHOICE_"):
            index = int(row["id"][-1])
            assert labels(native)[index].decode("ascii") == row["english"]
            offset = src["command_offset"]
            assert source[offset:offset + 4] == native[:4] == b"\x00\x21\x00\x00"
            holds = [runs[False][0][frame] for frame in (9260, 9550)]
            screens = [panels.picture(hold) for hold in holds]
            masks = [panels.find_line(font, row["english"], screen, range(70, 125),
                       range(269 + 20 * index, 280 + 20 * index), (8, 8, 8)) for screen in screens]
            assert [screen.getpixel((128, 269 + 20 * index)) == (0, 165, 172) for screen in screens] == [index == 0, index == 1]
            if index == 0:
                figures.extend(zip(("B134 / All right", "B134 / You handle it"), screens))
            display = dict(captures=holds, complete_labels=masks)
        else:
            assert source[src["command_offset"]:start + 1] == native[:6]
            raw = panels.bytes_for(native)
            assert " ".join(raw.decode("ascii").split()) == row["english"]
            upper, frame = STORY_FRAMES[int(row["id"].rsplit("_R", 1)[1])]
            shot = runs[upper][0][frame]
            screen = panels.picture(shot)
            if native[5] == 254:
                native_display = fe(raw)
                plane, width, nameplate = native_display["physical"], 228, None
            else:
                native_display = paint(arm, kanji, raw)
                page, = native_display["pages"]
                assert page["native_independent_plane_equal"]
                plane, width = bytes.fromhex(page["native_plane_hex"]), 216
                nameplate = panels.nameplate(font, row["speaker"], screen)
            assert native_display["complete_consumed_bytes"] == len(raw) and panels.mask_check(plane, width, screen), row["id"]
            display = dict(capture=shot, native_plane_sha256=sha256(plane).hexdigest(), complete_nameplate=nameplate)
            figures.append((row["id"], screen))
            if row["id"] == "DK4_MES_B134_R0025":
                draft = dict(id=row["id"], english=RECRUITING, protected_phrases=["looking for work", "will come over"])
                target, plan = panels.layout.plan_progressive(draft, native[5], raw, body)
                assert plan["expected_native_pages"] == 1 and len(target) <= len(raw) and target != raw
                proof = paint(arm, kanji, target)
                preview, = proof["pages"]
                assert proof["complete_consumed_bytes"] == len(target) and preview["native_independent_plane_equal"]
                proposal = draft | dict(lines=plan["lines"], exact_fitted_body_hex=target.hex(),
                    native_preview=preview, rationale="Keep 'will come over' together and preserve the source's emphasis on recruiting quickly.")
        rows.append({k: row[k] for k in ("id", "Japanese", "english", "speaker", "context", "source_meaning", "localization_note", "review")} |
            dict(source_reference=src, installed_reference=dst | {"archive_sha256": sha256(en).hexdigest(),
                 "candidate_sha256": release["candidate_sha256"]},
                 decision="revision proposed" if row["id"] == "DK4_MES_B134_R0025" else "retention", display=display))
    assert len(rows) == 7 and proposal
    return rows, figures, auto.reference(ledger), proposal


def main():
    release = auto.read(run.current.RELEASE)
    assert auto.digest(auto.REGISTRY) == release["registry_sha256"] and auto.digest(auto.CLEAN) == release["clean_input_sha256"]
    assert auto.digest(run.current.ROM) == release["candidate_sha256"]
    folders = (run.ROOT, run.ROOT.with_name("riga_auto_dock_upper_20261124"))
    runs = [run_capture(folder, release) for folder in folders]
    clean, rom = [auto.NdsImage.open(path) for path in (auto.CLEAN, run.current.ROM)]
    arm, kanji = rom.read_file(auto.ARM), rom.read_file("/GRP/KANJI.FNT")
    font = auto.GameAsciiFont.from_arm9(arm)
    common, common_figures = common_records(runs, clean, rom, arm, font, kanji)
    story, story_figures, ledger, proposal = story_records(runs, clean, rom, arm, font, kanji, release)
    returns = [run[0][frame] for run, frame in zip(runs, (10130, 10430))]
    for shot in [runs[0][0][8000], *returns]:
        panels.find_mask(font, "Stockholm", panels.picture(shot), (45, 10, 115, 35))
    sheets = FunctionType(panels.sheets_for.__code__, vars(panels) | {"OUT": OUT})
    preview = Image.new("RGB", (256, 384), (245, 245, 226))
    native_plane = bytes.fromhex(proposal["native_preview"]["native_plane_hex"])
    preview.paste(Image.frombytes("L", (216, 64), bytes(12 if px else 245 for px in native_plane)), (16, 296))
    proposal["contact_sheet"], = sheets("stockholm_recruiting_proposal", [(proposal["id"], preview)], (0, 289, 256, 364))
    auto.write(OUT, dict(candidate_sha256=release["candidate_sha256"], ordinary_existing_battery_save=True,
        branch_names=["You handle it.", "All right."], evidence=[r[2] for r in runs], source_story_review=ledger,
        dock_prompt=runs[0][0][7600], arrived_in_Stockholm=runs[0][0][8000], returned_to_Stockholm=returns,
        docked_fleet_state=dock_state(arm, runs[0][3]), common=common, recruiting=story, open_revision=proposal,
        sheets=sheets("riga_stockholm_auto_dock", common_figures + story_figures, (0, 264, 256, 374)),
        ROM_changed=False, new_editorial_credit=0))
    print(f"Verified ordinary docking at Stockholm, {len(common)} port notices and all {len(story)} recruiting records.")


if __name__ == "__main__":
    main()
