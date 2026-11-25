"""Verify ordinary Azores redocking, preserved display fields, and the nearby recruit exchange."""

from pathlib import Path
from struct import unpack_from

from PIL import Image, ImageDraw

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.script.common_message_table import common_message_entries
from scripts import observe_azores_return_20261123 as observed
from scripts import stage_azores_return_20261123 as stage
from scripts.reconcile_elegy_acceptance_20261123 import common_rows
from scripts.reconcile_editorial_acceptance_20261123 import COMMON, OUT
from scripts.reconcile_queued_sailing_hints_20261123 import ARM, CLEAN, NdsImage, digest, read, reference, write
from scripts.verify_confirmed_name_widget_pixels_v198 import complete_mask
from scripts.verify_lisbon_azores_voyage_20261123 import body_mask, load_exact, text_at, town
from scripts.verify_plaque_release_v247 import find_mask
from scripts.verify_regional_ui_v616 import glyphs
from scripts.verify_village_visits_v664 import model


OUTPUT = OUT.with_name("azores_return_current_20261123.json")
SHEET = OUTPUT.with_suffix(".png")
HERO = "Manuel Almeida"
DIALOGUE = {
    13600: (70, ("Shall we stop at Azores?",), HERO,
            "Manuel keeps his courteous invitation and the selected port. Add the normal English article in the sentence."),
    14360: (8, ("Need help?",), "Trader", "Keep the quick, informal shop greeting as Trade opens."),
    15900: (51, ("Welcome! What will you have?",), "Barkeep",
            "Keep the friendly general entrance greeting before the Tavern menu appears."),
    16400: (896, ("I'll use 700 gold", "to recruit sailors."), HERO,
            "Manuel states the exact expenditure and purpose before asking for confirmation."),
    17240: (903, ("Anyone for the Admiral's crew?",), HERO,
            "A brief call for volunteers preserves the original admiral's crew and suits the public announcement."),
    17520: (907, ("Aye!",), "Patron", "The short affirmative response fits a volunteer calling out in the Tavern."),
    17800: (904, ("We've got 18 willing to join.",), HERO,
            "Manuel's concise report preserves the original count and the volunteers' willingness."),
    18080: (1048, ("There's still room for 67 more", "aboard. Shall I try", "recruiting more?"), HERO,
            "Reflow the follow-up to keep the question together and the capacity substitution intact."),
}


def shots(capture, suffix):
    return {row["frame"]: row for row in capture["frames_captured"] if row["path"].endswith(suffix)}


def picture(shot):
    assert digest(shot["path"]) == shot["PNG_sha256"]
    with Image.open(shot["path"]) as image:
        return image.convert("RGB")


def replay(case, sha):
    folder = observed.ROOT / case
    capture, trace, terminal = map(read, (folder / item for item in (
        "capture/capture_report.json", "requests.json", "terminal.json")))
    assert terminal["ROM_sha256"] == capture["ROM_sha256"] == sha
    assert capture["cold_boot"] and not capture["savestate_loaded"] and not capture["callback_errors"]
    assert trace["all_host_slots_restored_and_core_file_exact"] and not trace["mismatches"] and not trace["errors"]
    for path, expected in terminal["evidence"].items():
        if case == "current" and Path(path).resolve() == Path(observed.__file__).resolve():
            path = folder / "observer_source.py"
        assert digest(path) == expected
    assert trace["source_requests"] == terminal["target_COMMON_calls"]
    assert len(trace["rows"]) == 4
    a, owner, b, c = trace["rows"]
    assert [r["PC"] for r in (a, owner, b, c)] == [observed.VILLAGE_NAME_RETURN, observed.TOWN_NAME_CALL,
                                                   observed.TOWN_NAME_RETURN, observed.TOWN_FORMAT_CALL]
    assert [r["frame"] for r in (a, owner, b, c)] == [8441, 13456, 13456, 13456]
    assert owner["vtable"] == 0x0215658C and owner["getter"] == 0x020B5630
    assert bytes.fromhex(a["text_hex"]) == b"the Azores"
    assert b == c | dict(PC=observed.TOWN_NAME_RETURN)
    expected = b"Azores" if case == "current" else b"the Azores"
    assert bytes.fromhex(c["text_hex"]) == expected
    return capture, trace


def main():
    release, staged, first = map(read, (stage.RELEASE, stage.PROOF, observed.VISIT))
    assert digest(observed.VISIT) == observed.VISIT_SHA
    parent, target = release["candidate_sha256"], staged["candidate_sha256"]
    assert target == digest(stage.ROM) and parent == first["ROM_sha256"] == digest(release["candidate"])
    clean, original, changed = map(NdsImage.open, (CLEAN, release["candidate"], stage.ROM))
    arm = changed.read_file(ARM)
    font = GameAsciiFont.from_arm9(arm)
    current, before_trace = replay("current", parent)
    revised, after_trace = replay("revised", target)
    assert current["scripted_input_schedule"] == revised["scripted_input_schedule"] == first["scripted_input_schedule"]
    assert before_trace["source_requests"] == after_trace["source_requests"]
    assert after_trace["rows"][-1]["text_address"] == staged["alias_address"]
    assert before_trace["rows"][-1]["text_address"] == stage.prior.AZORES_TOWN
    assert all(r["ROM_sha256"] == expected for r, expected in ((current, parent), (revised, target)))
    before, after, actual = shots(current, "cold_boot.png"), shots(revised, "cold_boot.png"), shots(first, "navigation.png")
    assert tuple(before) == tuple(after)
    for frame in observed.FRAMES:
        if frame in actual:
            assert before[frame]["framebuffer_sha256"] == actual[frame]["framebuffer_sha256"]
    assert [f for f in before if before[f]["framebuffer_sha256"] != after[f]["framebuffer_sha256"]] == [13600]

    snapshots = {row["frame"]: row for row in first["read_only_pause_RAM_snapshots"]}
    assert len(arm) == len(original.read_file(ARM))
    stock = model(original.read_file(ARM), load_exact(snapshots[13880]), 13, "Azores", True)
    assert stock["native_development"] == 2 and stock["town"] == before_trace["rows"][1]["object_address"]
    ports = picture(after[13880])
    town_name = find_mask(font, "Azores", ports, (28, 14, 136, 34))
    specialty = {(x, y) for y in range(12) for x in range(96)
                 if ports.getpixel((160 + x, 89 + y)) == (230, 230, 230)}
    assert specialty == glyphs(font, "Azores Wine", 5)

    entries = [common_message_entries(clean.read_file(COMMON), clean.read_file(ARM))]
    entries.extend(common_rows(image.read_file(COMMON), image.read_file(ARM)) for image in (original, changed))
    ledger = []
    for frame, (key, lines, speaker, reason) in DIALOGUE.items():
        source, current_entry, new = (rows[key] for rows in entries)
        assert current_entry.text == new.text and town.reference(current_entry) == town.reference(new)
        holds = picture(actual[frame])
        raw = load_exact(snapshots[frame])
        pointer, = unpack_from("<I", arm, 0x54450)
        assert tuple(line.strip() for line in text_at(raw, pointer).decode("cp932").split('\n')) == lines
        mask = body_mask(font, holds, lines)
        complete_mask(font, speaker, holds, 16, 277, (98, 97, 98))
        shown = lines
        if key == 70:
            shown = ("Shall we stop at the Azores?",)
            mask = body_mask(font, picture(after[frame]), shown)
            complete_mask(font, speaker, picture(after[frame]), 16, 277, (98, 97, 98))
        ledger.append(dict(id=f"COMMON_MESSAGE_{key}", speaker=speaker, frame=frame, source_Japanese=source.text.decode("cp932"),
            source_reference=town.reference(source), source_hex=source.text.hex(),
            current_reference=town.reference(current_entry), current_hex=current_entry.text.hex(),
            installed_reference=town.reference(new), installed_hex=new.text.hex(), text_changed=False,
            observed_before=lines, observed_after=shown, reason=reason, complete_visible_body=mask,
            decision="runtime revision" if key == 70 else "wrap lead" if key == 1048 else "retention",
            review=dict(source=True, context=True, localization=True, naturalness=True, formatting=key != 1048)))

    holds = (("Before redocking", picture(before[13600])), ("Corrected redocking", picture(after[13600])),
             ("Developed Azores", ports), ("Azores Wine in Trade", picture(after[15050])),
             ("Tavern and crew offer", picture(after[16400])), ("Recruiting follow-up", picture(actual[18080])))
    sheet = Image.new("RGB", (3 * 268, 2 * 412), "#28313b")
    captions = ImageDraw.Draw(sheet)
    for i, (label, frame) in enumerate(holds):
        x, y = 268 * (i % 3) + 6, 412 * (i // 3)
        captions.text((x, y + 4), label, fill="white")
        sheet.paste(frame, (x, y + 24))
    sheet.save(SHEET)
    write(OUTPUT, dict(registered_parent=reference(stage.RELEASE), original_sha256=parent, candidate_sha256=target,
        ordinary_lisbon_to_azores_and_redocking=True, emulator_only=True, all_other_replayed_frames_identical=True,
        stock_developed_town=stock, bare_town_heading=town_name, complete_Azores_Wine_specialty=True,
        original_name_calls=before_trace["rows"], revised_name_calls=after_trace["rows"],
        records=ledger, screenshot=reference(SHEET), exact_gameplay_schedule=reference(observed.VISIT),
        unvisited=["Other docking voices in this replay", "Other village layouts", "Physical hardware"], new_editorial_credit=0))
    print("Verified both docking paths and the exact unchanged heading, Trade and Tavern frames.")


if __name__ == "__main__":
    main()
