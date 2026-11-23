"""Review the observed Riga and Seoul exchanges and preflight the Seoul rumor."""

from pathlib import Path
from struct import unpack_from

from PIL import Image, ImageDraw

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.country_editorial import compile_paragraph
from dk4tool.script.common_message_table import common_message_entries
from scripts.observe_baltic_seoul_town_20261123 import ROOT, RELEASE
from scripts.registered_editorial_runtime_v2 import RegisteredRuntime
from scripts.stage_azores_wording_20261123 import ARM, COMMON, common_rows, digest_bytes
from scripts.stage_cartridge_title_20261123 import CLEAN, REGISTRY, NdsImage, digest, read, reference, write
from scripts.stage_square_country_briefings_20261115 import (
    GATES, font_tools, glyph_codes, native_layout, owned_deployment, render_portrait,
)
from scripts.verify_captain_biographies_v1 import captured
from scripts.preflight_shared_crew_notices_v1 import with_components
from scripts.verify_confirmed_name_widget_pixels_v198 import complete_mask
from scripts.verify_lisbon_azores_voyage_20261123 import body_mask, text_at
from scripts.verify_stock_encounter_names_20261121 import read_ram


STAGE = ROOT / "stage"
ROM = STAGE / "Seoul_Square_Rumor_STAGED.nds"
OUT = Path("translations/editorial_checkpoints/shared_display_20261123")
REPORT = OUT / "riga_seoul_ordinary_20261123.json"
YIFA = Path("releases/all_routes_editorial_20261115_seoul_recruitment_candidate/verification/registered_review.json")
YIFA_FOLLOWUP = Path("releases/all_routes_editorial_20261118_next_review_wraps_candidate/verification/registered_review.json")
RUMOR = 726
NEW = "Hideyoshi? Kurushima? Who cares? I'll drive them off every time!"
NEW_LINES = ("Hideyoshi? Kurushima? Who cares?", "I'll drive them off every time!")
OLD_LINES = ("Hideyoshi or Kurushima? I'll drive", "them off every time they come!")
OBSERVED = {
    "riga": {3980: (658,), 4310: (656,), 4790: (691,), 5110: (656,), 5590: (657,),
             5910: (658,), 7380: (51,), 7700: (53,), 7860: (821, "Clifford", "London", "soldier"),
             8340: (821, "Argot", "Amsterdam", "trader")},
    "seoul": {9850: (657,), 10170: (726,), 10490: (726,), 10970: (656,), 11290: (656,),
              12090: (51,), 12410: (53,), 12570: (55, "Reika"), 12730: (56,), 12890: (59,),
              13050: (61,), 13210: (827, "Maria"), 13850: (57,), 14010: (59,), 14170: (61,), 14330: (824,)},
}
NOTES = {
    51: ("The barkeep greets the player and asks for an order.", "The open question fits the drink and crew menus that follow."),
    53: ("The barkeep charges five gold coins.", "The short price keeps the exact charge and fits the original payment moment."),
    55: ("The barkeep calls the named attendant for a customer.", "The casual call and name make the handoff to Reika clear."),
    56: ("The attendant calls back an affirmative acknowledgment.", "The brisk reply fits the call from the barkeep before she arrives."),
    57: ("The attendant greets the customer directly.", "The short welcome fits a different entrance from her call from across the room."),
    59: ("The attendant urges the customer to have another drink.", "The friendly invitation fits the original Yes and No choices."),
    61: ("The barkeep quotes ten gold coins for the additional drink.", "The quoted amount stays exact after accepting Reika's invitation."),
    656: ("The shop specializes in retail.", "The concise notice contrasts with the Market's bulk orders."),
    657: ("The shopkeeper recognizes a sailor and recommends the Market for large orders.", "The question tag stays with the friendly question. The referral occupies its own complete line."),
    658: ("Business has been acceptable and the shopkeeper hopes for a good opportunity.", "The repeated question and modest answer precede the shopkeeper's wish for a better deal."),
    691: ("Sweden recently gained independence from the Kalmar Union with Denmark and Norway.", "The recent independence, historical name, and both countries carry through. The last row keeps the two countries together."),
    726: ("Whether it is Hideyoshi or Kurushima, the shopkeeper vows to drive them away however often they come.", "The two short questions and the dismissal keep the speaker's defiance. The complete vow retains the repeated threat on one line."),
    821: ("The named person from the given town and occupation has influence here.", "Real pull is colloquial and the two samples retain the person, home town and role as separate arguments."),
    824: ("The attendant has no particular information at the moment.", "The qualifier right now gives a natural answer after the second round."),
    827: ("The attendant confirms the player's name and offers a toast to their acquaintance.", "The familiar confirmation and toast suit Reika's first drink with Maria."),
}


def ref(row):
    return dict(block=row.block, offset=row.block_offset, copy_end=row.copy_end,
                table_offset=row.table_offset, hex=row.text.hex())


def scope(case, release):
    folder = ROOT / case
    path = folder / "capture/capture_report.json"
    terminal_path = folder / "terminal.json"
    report, terminal = read(path), read(terminal_path)
    assert report["ROM_sha256"] == terminal["candidate_sha256"] == release["candidate_sha256"]
    assert report["cold_boot"] and not report["savestate_loaded"] and not report["callback_errors"]
    assert terminal["ordinary_controller_inputs"] and not any(v for k, v in report.items() if k.startswith("synthetic_"))
    donor = report["battery_save_preloaded"]
    assert donor["copied_byte_exact_before_cold_boot"] and digest(donor["source"]) == terminal["copied_save_sha256"]
    # The Riga process started before the Seoul adapter change. Its terminal
    # lists the adapter hash at exit. Keep exact file bindings for both journals.
    assert all(digest(p) == h for p, h in terminal["evidence"].items() if not p.endswith(".py"))
    frames = {row["frame"]:row for row in report["frames_captured"] if row["path"].endswith("_navigation.png")}
    snapshots = {row["frame"]:row for row in report["read_only_pause_RAM_snapshots"]}
    return dict(capture=reference(path), terminal=reference(terminal_path), donor=reference(donor["source"]),
                journal=reference(folder / "controller.jsonl"), finish_frame=report["frames"]), frames, snapshots, terminal["common_requests"]


def observations(release, font, source, installed):
    selections, pictures = {}, {}
    for case, samples in OBSERVED.items():
        run, frames, snapshots, calls = scope(case, release)
        notes, panes = [], []
        previous = 0
        for frame, (n, *args) in samples.items():
            jp, en = source[n], installed[n]
            visible = captured(frames[frame])
            raw = read_ram(snapshots[frame])
            plain, layout = [text_at(raw, unpack_from("<I", raw, off)[0]) for off in (0x5444C, 0x54450)]
            encoded = tuple(value.encode("ascii") for value in args)
            assert jp.text.count(b"%s") == en.text.count(b"%s") == len(encoded)
            assert (en.text % encoded).split() == plain.split() == layout.split()
            lines = [line.strip().decode("ascii") for line in layout.split(b"\n")]
            assert 0 < len(lines) <= 4 and all(0 < len(line) <= 35 for line in lines)
            matched = [call for call in calls if max(previous, frame - 200) < call["frame"] < frame and call["message_ID"] == n]
            assert len(matched) == 2, (case, frame, n, matched)
            a, b = matched
            assert a["PC"] == 0x0205528C and b["PC"] == 0x020534F4 and dict(a, PC=b["PC"]) == b
            name = ("Shopkeeper" if 656 <= n <= 726 else
                    "Reika" if n in (56, 57, 59, 824, 827) else "Barkeep")
            count, bounds = complete_mask(font, name, visible, 16, 277, (98, 97, 98))
            glyphs = body_mask(font, visible, lines)
            mean, rationale = NOTES[n]
            notes.append(dict(message_ID=n, speaker=name, source=ref(jp), installed=ref(en),
                Japanese=jp.text.decode("cp932"), source_meaning=mean, English=" ".join(en.text.decode("ascii").split()),
                substitutions=args, capture=frames[frame], input_snapshot=snapshots[frame], calls=[a,b],
                lines=glyphs, nameplate=dict(pixels=count, bounds=bounds), note=rationale,
                decision="revision" if n == RUMOR else "retention",
                review=dict.fromkeys(GATES, True) | {"formatting": n != RUMOR}))
            if n not in {row[0] for row in panes} or n == 821:
                panes.append((n, visible))
            previous = frame
        selections[case] = run | dict(observed_panels=notes, all_COMMON_calls=calls)
        pictures[case] = panes
    return selections, pictures


def yifa_dependency(image, clean, font, release):
    rows = read(YIFA)["records"]
    assert len(rows) == 35 and all(all(row["review"].values()) for row in rows)
    src, dst = [IlnkContainer.parse(i.read_file("/data/SC3.DK4")).blocks[140] for i in (clean, image)]
    followup, = [r for r in read(YIFA_FOLLOWUP)["records"] if r["id"] == "DK4_MES_B140_R0124"]
    assert all(followup["review"].values())
    new = followup["registered_reference"]
    positions, shift = [], 0
    for row in rows:
        jp, en = (row[name] for name in ("source_reference", "registered_reference"))
        source_offset = jp["offset"] - 5
        old_offset = en["offset"] - 5
        preamble = bytes.fromhex(en["complete_preamble_hex"])
        source_data = bytes.fromhex(jp["complete_preamble_hex"] + jp["raw_hex"][2:] + "00")
        old_data = preamble + bytes.fromhex(en["raw_hex"][2:] + "00")
        assert src[source_offset:source_offset+len(source_data)] == source_data, row["id"]
        offset, data = old_offset + shift, old_data
        if row["id"] == followup["id"]:
            assert offset == new["command_offset"] and jp["raw_hex"] == followup["source_hex"]
            data = preamble + bytes.fromhex(new["exact_stored_hex"][2:] + "00")
            shift = len(data) - len(old_data)
        assert dst[offset:offset+len(data)] == data, row["id"]
        positions.append(dict(id=row["id"], source_command_offset=source_offset, installed_command_offset=offset,
                              installed_command_hex=data.hex(), followup=row["id"] == followup["id"]))
    _, frames, _, calls = scope("seoul", release)
    hold, = [call for call in calls if call["message_ID"] == 341 and call["PC"] == 0x0205528C]
    assert 8930 < hold["frame"] < 9230
    start = captured(frames[3830])
    full_name = complete_mask(font, "Yukihisa Shiraki", start, 16, 277, (98, 97, 98))
    pixels = body_mask(font, start, ("Halt! Who goes there?!",))
    return dict(review=reference(YIFA), followup_review=reference(YIFA_FOLLOWUP),
                clean_block_sha256=digest_bytes(src), installed_block_sha256=digest_bytes(dst),
                exact_registered_commands=positions, opening=frames[3830], opening_body=pixels, opening_name=full_name,
                joined_request=hold, returned_to_Square=frames[9530]), start


def preview_release(release, clean, image, arm, before, source):
    working = image.read_file(COMMON)
    edit = compile_paragraph(NEW).ljust(len(before[RUMOR].text), b" ")
    assert len(edit) == len(before[RUMOR].text) and b"%" not in edit and b"\n" not in edit
    deployed, after, slots = owned_deployment(working, arm, before, {RUMOR: edit})
    assert {a.message_id for a,b in zip(before, after, strict=True) if a != b} == {RUMOR}
    assert not slots[RUMOR]["new_null_fields"]
    ctx = RegisteredRuntime(RELEASE, release["own_registered_startup"], captain=3)
    raster, _, _ = font_tools(image)
    kanji = image.read_file("/GRP/KANJI.FNT")
    cases = []
    sheet = Image.new("RGB", (510, 306), "#263238")
    draw = ImageDraw.Draw(sheet)
    for idx, (common, row, expected) in enumerate(((working, before[RUMOR], OLD_LINES), (deployed, after[RUMOR], NEW_LINES))):
        view_context = with_components(ctx, arm, common)
        cpu, get, _ = view_context.machine(arm, common, view_context.raw, view_context.plan)
        stored = get(0x5528C, RUMOR)
        assert bytes(cpu.mem_read(stored, len(row.text) + 1)) == row.text + b"\0"
        body, lines = native_layout(cpu, row.text, RUMOR, ())
        assert tuple(lines) == expected and b" ".join(body.split()) == b" ".join(row.text.split())
        pixels, glyphs = render_portrait(raster, arm, kanji, body)
        codes = glyph_codes(body)
        assert [entry["code"] for entry in glyphs] == codes
        assert codes[0] == ord("H") and codes[-1] == ord("!")
        view = Image.frombytes("L", (228, 64), bytes(0 if p else 255 for p in pixels))
        draw.text((12, 4 + idx * 151), ("Installed wrapping", "Proposed wrapping")[idx], fill="white")
        sheet.paste(view.convert("RGB").resize((456,128), Image.Resampling.NEAREST), (12, 20 + idx * 151))
        cases.append(dict(lines=lines, complete_plane_sha256=digest_bytes(bytes(pixels)), formatted_hex=body.hex()))
    assert clean.read_file(ARM)[0x5F9B8:0x5FB54] == arm[0x5F9B8:0x5FB54]
    jp = source[RUMOR]
    mean, note = NOTES[RUMOR]
    record = dict(id=f"COMMON_MESSAGE_{RUMOR}", message_ID=RUMOR, file_path=COMMON, speaker="Shopkeeper", context=(
        "Two ordinary Seoul Food Shop visits select this regional reply. The shopkeeper treats both opponents "
        "as equally unwelcome and says repeated visits will end the same way."),
        source_meaning=mean, localization_note=note, review=dict.fromkeys(GATES, True), decision="revision",
        source_Japanese=jp.text.decode("cp932"), source_reference=ref(jp), current_reference=ref(before[RUMOR]),
        staged_reference=ref(after[RUMOR]), english=NEW, native_layouts=cases)
    batch = dict(translation_policy="natural-dialogue-v2", target_locale="en-US",
                 encoder="dialogue-relocatable-v1", review_gates=list(GATES), records=[record])
    validate_natural_dialogue_batch(batch)
    STAGE.mkdir()
    sheet.save(STAGE / "seoul_rumor_before_after.png")
    image.replace_file(COMMON, deployed)
    result = bytes(image.rom.save())
    image.replace_file(COMMON, working)
    assert bytes(image.rom.save()) == image.source.read_bytes()
    ROM.write_bytes(result)
    write(STAGE / "stored_proof.json", batch | dict(predecessor=reference(image.source), candidate=reference(ROM),
        clean=reference(CLEAN), changed_internal_files=[COMMON], changed_ids=[RUMOR], slots=slots,
        target_COMMON_sha256=digest_bytes(deployed), target_ARM9_sha256=digest_bytes(arm),
        exact_whole_parent_inverse=True, preview=reference(STAGE / "seoul_rumor_before_after.png"),
        actual_revised_ROM_replay_pending=True, registered=False))


def main():
    release = read(RELEASE)
    assert all(digest(path) == release[key] for path,key in ((CLEAN, "clean_input_sha256"),
        (REGISTRY, "registry_sha256"), (release["candidate"], "candidate_sha256")))
    clean, image = [NdsImage.open(p) for p in (CLEAN, release["candidate"])]
    arm, common = [image.read_file(p) for p in (ARM, COMMON)]
    assert digest_bytes(arm) == release["target_ARM9_sha256"] and digest_bytes(common) == release["target_COMMON_sha256"]
    source = common_message_entries(clean.read_file(COMMON), clean.read_file(ARM))
    installed = common_rows(common, arm)
    font = GameAsciiFont.from_arm9(arm)
    visits, images = observations(release, font, source, installed)
    yifa, start = yifa_dependency(image, clean, font, release)
    images["seoul"].insert(0, ("Yifa event opening", start))
    sheets = []
    for case, panes in images.items():
        sheet = Image.new("RGB", (1040, 258 * ((len(panes) + 1) // 2)), "#263238")
        draw = ImageDraw.Draw(sheet)
        for i, (label, picture) in enumerate(panes):
            x, y = i % 2 * 520 + 4, i // 2 * 258
            draw.text((x, y + 6), f"{case.title()} / {label}", fill="white")
            crop = picture.crop((0, 266, 256, 383)).resize((512, 234), Image.Resampling.NEAREST)
            sheet.paste(crop, (x, y + 21))
        path = REPORT.with_name(f"{case}_ordinary_20261123.png")
        sheet.save(path)
        sheets.append(reference(path))
    write(REPORT, dict(candidate=reference(image.source), visits=visits, yifa=yifa, visual_sheets=sheets,
        ordinary_saved_gameplay=True, new_credited_records=0, full_goal_complete=False))
    preview_release(release, clean, image, arm, installed, source)


if __name__ == "__main__":
    main()
