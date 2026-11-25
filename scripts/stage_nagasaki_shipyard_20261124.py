"""Stage and compare the source-reviewed Nagasaki Yard changes."""

from argparse import ArgumentParser
from collections import Counter
from pathlib import Path
from types import FunctionType

from PIL import Image, ImageChops, ImageDraw
from dk4tool.dialogue.font_audit import GameAsciiFont
from scripts import preflight_nagasaki_shipyard_20261124 as preflight
from scripts import stage_nagasaki_contract_wrap_20261124 as earlier
from scripts.stage_cartridge_title_20261123 import CLEAN, REGISTRY, NdsImage, digest, read, reference, sha256, write


yard = preflight.yard
parent, panels = yard.play.current, yard.panels
ARM, COMMON = parent.ARM, parent.COMMON
ROOT = Path(".codex-release-work/nagasaki_yard_reflow_20261124")
ROM, STORED = ROOT / "Nagasaki_Yard_Reflow_STAGED.nds", ROOT / "stored_proof.json"
PATCH, REBUILT, PATCH_PROOF = (ROOT / name for name in ("translation.xdelta", "clean_rebuilt.nds", "clean_patch_proof.json"))
STARTUP_CAPTURE = ROOT / "startup/capture/capture_report.json"
REPLAY = ROOT / "replay/capture/capture_report.json"
BEFORE = yard.play.ROOT / "capture/capture_report.json"
SHEET, PAIRED = ROOT / "nagasaki_yard_paired.png", ROOT / "paired_gameplay.json"
REVISIONS = {16920: 1287, 17320: 1285, 20120: 1264, 21720: 1264}
HIGHLIGHT = (0, 165, 172)
PAPER = (205, 198, 180)
BLINKS = {
    22120: ((32, 192, 256, 224), {HIGHLIGHT: {(24, 40, 49), (24, 48, 57), (41, 48, 57), (41, 48, 65)}}),
    22520: ((101, 268, 155, 288), {PAPER: {HIGHLIGHT}}),
    23720: ((98, 258, 158, 278), {HIGHLIGHT: {PAPER}}),
    24920: ((104, 238, 152, 258), {PAPER: {HIGHLIGHT}}),
}


def stage():
    release, draft = map(read, (parent.RELEASE, preflight.OUT))
    assert digest(CLEAN) == release["clean_input_sha256"] and digest(REGISTRY) == release["registry_sha256"]
    assert digest(parent.ROM) == release["candidate_sha256"] == draft["candidate_sha256"] and draft["gameplay"] == reference(yard.OUT)
    native = read(draft["checked_refit_pages"]["path"])
    assert reference(draft["checked_refit_pages"]["path"]) == draft["checked_refit_pages"]
    previews = native["review_sheets"] + draft["checked_rename_prompt"]["sheets"]
    assert all(digest(row["path"]) == row["sha256"] for row in previews)
    clean, image = map(NdsImage.open, (CLEAN, parent.ROM))
    arm, common = (image.read_file(path) for path in (ARM, COMMON))
    assert sha256(arm).hexdigest() == release["target_ARM9_sha256"] and sha256(common).hexdigest() == release["target_COMMON_sha256"]
    assert earlier.template.right_bound(arm, release["right_bound_configuration"])["matched_repair_spans"] == 8
    source = yard.common_message_entries(clean.read_file(COMMON), clean.read_file(ARM))
    before = yard.common_rows(common, arm)
    edits = {item["message_id"]: bytes.fromhex(item["payload_hex"]) for item in draft["records"]}
    assert set(edits) == set(yard.PROPOSALS)
    for row in draft["records"]:
        key = row["message_id"]
        assert panels.text_reference(source[key]) == row["source_reference"] and panels.text_reference(before[key]) == row["current_reference"]
        assert len(edits[key]) == len(before[key].text) and b"%" not in edits[key] + source[key].text
        assert " ".join(edits[key].decode("ascii").split()) == yard.PROPOSALS[key]
    revised, entries, slots = preflight.owned_deployment(common, arm, before, edits)
    assert sha256(revised).hexdigest() == draft["proposed_archive_sha256"]
    assert {str(k): v for k, v in slots.items()} == draft["exact_storage_slots"] and all(not row["new_null_fields"] for row in slots.values())
    assert [new.message_id for old, new in zip(before, entries, strict=True) if old != new] == sorted(edits)
    image.replace_file(COMMON, revised)
    candidate = bytes(image.rom.save())
    image.replace_file(COMMON, common)
    assert bytes(image.rom.save()) == parent.ROM.read_bytes()
    ROOT.mkdir()
    ROM.write_bytes(candidate)
    final = NdsImage.open(ROM)
    assert final.read_file(COMMON) == revised and final.read_file(ARM) == arm
    installed = yard.common_rows(final.read_file(COMMON), arm)
    assert all(installed[key].text == text for key, text in edits.items())
    write(STORED, dict(candidate=reference(ROM), previous=reference(parent.ROM), clean=reference(CLEAN),
        target_COMMON_sha256=sha256(revised).hexdigest(), target_ARM9_sha256=release["target_ARM9_sha256"],
        changed_messages=sorted(edits), exact_source_rows={key: panels.text_reference(source[key]) for key in edits},
        exact_predecessor_rows={key: panels.text_reference(before[key]) for key in edits},
        exact_installed_rows={key: panels.text_reference(installed[key]) for key in edits},
        whole_parent_inverse=True, allocations=slots, preflight=reference(preflight.OUT), reviewed_native_previews=previews))
    print(f"Staged only COMMON 1264, 1285 and 1287. {digest(ROM)}", flush=True)


def verify(stored):
    old, new = map(read, (BEFORE, REPLAY))
    assert old["ROM_sha256"] == stored["previous"]["sha256"] and new["ROM_sha256"] == stored["candidate"]["sha256"] == digest(ROM)
    assert new["cold_boot"] and not new["callback_errors"] and not new["savestate_loaded"]
    assert not any(value for key, value in new.items() if key.startswith("synthetic_"))
    assert new["frames"] == old["frames"] and new["scripted_input_schedule"] == old["scripted_input_schedule"]
    donor = new["battery_save_preloaded"]
    assert digest(donor["source"]) == donor["source_sha256"] == old["battery_save_preloaded"]["source_sha256"]
    before, after = (panels.shots(run, suffix) for run, suffix in ((old, "_navigation.png"), (new, "_cold_boot.png")))
    assert before.keys() <= after.keys() and REVISIONS.keys() <= before.keys()
    image = NdsImage.open(ROM)
    arm = image.read_file(ARM)
    installed = yard.common_rows(image.read_file(COMMON), arm)
    font = GameAsciiFont.from_arm9(arm)
    matches, revisions, blinks = [], [], []
    sheet = Image.new("RGB", (672, 465), "#263238")
    draw = ImageDraw.Draw(sheet)
    for frame in sorted(before):
        a, b = (panels.picture(group[frame]) for group in (before, after))
        bbox = ImageChops.difference(a, b).getbbox()
        if frame in BLINKS:
            area, permitted = BLINKS[frame]
            assert bbox == area, (frame, bbox)
            changes = Counter((s, t) for s, t in zip(a.crop(area).get_flattened_data(), b.crop(area).get_flattened_data(), strict=True) if s != t)
            assert set(changes) == {(s, t) for s, colors in permitted.items() for t in colors}
            if frame == 22120:
                assert a.tobytes() == panels.picture(before[20520]).tobytes()
            blinks.append(dict(frame=frame, background_only=True, box=area,
                changed_colors=[dict(previous=s, current=t, pixels=count) for (s, t), count in sorted(changes.items())],
                previous=before[frame], revised=after[frame]))
            continue
        if frame not in REVISIONS:
            assert bbox is None, (frame, bbox)
            matches.append(frame)
            continue
        key = REVISIONS[frame]
        if key == 1264:
            region = (16, 296, 245, 360)
            lines = [yard.PROPOSALS[key]]
            ink = panels.exact_body(font, lines, b)
            assert panels.nameplate(font, "Shipwright", a) == panels.nameplate(font, "Shipwright", b)
        else:
            region = yard.BOX
            lines, ink = yard.exact_refit(font, installed[key].text, b)
            assert " ".join(" ".join(lines).split()) == yard.PROPOSALS[key]
        assert bbox and region[0] <= bbox[0] < bbox[2] <= region[2] and region[1] <= bbox[1] < bbox[3] <= region[3]
        revisions.append(dict(frame=frame, message_ID=key, lines=lines, valid_change_region=region,
            complete_foreground_pixels=ink, previous=before[frame], revised=after[frame]))
        if frame == 21720:
            continue
        row = len(revisions) - 1
        for index, (name, screen) in enumerate((("Previous", a), ("Revised", b))):
            x, y = index * 336, row * 155
            draw.text((x + 6, y + 4), f"{key} / {name}", fill="white")
            block = screen.crop(region).resize((336, 128), Image.Resampling.NEAREST)
            sheet.paste(block, (x, y + 22))
    assert {785, 786, 789, 1284} <= {r["message_ID"] for r in read(yard.OUT)["records"] if r["capture"]["frame"] in matches}
    assert yard.END in matches and len(revisions) == 4
    sheet.save(SHEET)
    write(PAIRED, dict(candidate_sha256=new["ROM_sha256"], previous_sha256=old["ROM_sha256"], before=reference(BEFORE), after=reference(REPLAY),
        stored=reference(STORED), sheet=reference(SHEET), unchanged_frames=matches, revised=revisions,
        menu_highlight_only=blinks, ordinary_saved_game=True))
    print(f"Verified four revised holds, {len(matches)} pixel-identical controls and {len(blinks)} background-only highlight changes.")


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("stage", "patch", "startup", "replay", "verify"))
    action = parser.parse_args().action
    if action == "stage":
        stage()
    elif action == "verify":
        verify(read(STORED))
    else:
        scope = vars(earlier) | globals()
        name = "replay" if action == "replay" else "release_check"
        FunctionType(getattr(earlier, name).__code__, scope)(read(STORED), *(() if action == "replay" else (action,)))
