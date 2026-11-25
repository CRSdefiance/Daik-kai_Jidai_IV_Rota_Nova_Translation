"""Stage Claudio's wrap in its existing command and check native font output."""

from pathlib import Path
from types import SimpleNamespace

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.script.format_safety_relocated_v2 import bind_registered_story_percent_guard
from PIL import Image, ImageDraw

from scripts import inventory_lil_after_crew_items_complete_v3152 as commands
from scripts import register_cartridge_title_20261123 as registry_guards
from scripts import stage_london_guild_assignments_20261118 as formatter
from scripts import stage_story_tag_wraps_20261118 as fixed
from scripts import verify_all_routes_next_phrase_wraps_20261118 as display
from scripts import verify_rafael_new_game_fleet_20261124 as review
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.stage_cartridge_title_20261123 import CLEAN, NdsImage, REGISTRY, digest, read, reference, sha256, write
from inspect import getsource

parent = review.play.current
ROOT = parent.ROM.parent.with_name("editorial_20261124_claudio_opening_wrap")
ROM = ROOT / "Claudio_Opening_Wrap_STAGED.nds"
STORED = ROOT / "stored_proof.json"
NATIVE = review.OUT.with_name("claudio_opening_wrap_preflight_20261124.json")
SHEET = NATIVE.with_suffix(".png")
STORY, BLOCK = review.STORY, 44


def paths(rom):
    return dict(rom.iter_components()) | {path: payload for _, path, payload in rom.iter_files()}


def preview(release, image, body, plan, earlier):
    arm = image.read_file(parent.ARM)
    ctx = SimpleNamespace(arm=arm, image=image)
    paint = display.clipped_renderer(ctx)
    font = image.read_file("/GRP/KANJI.FNT")
    layouts, panels = [], []
    examples = (("Previous view", "Rafael", earlier, ["Yeah. Rafael needs someone at his", "side. That's me."]),
                ("Revised with Rafael", "Rafael", body, None),
                ("Revised with one-letter name", "I", body, None),
                ("Revised with 16-letter name", "W" * 16, body, None))
    for title, name, data, before in examples:
        rows = before or [display.display.expected(template, {"FI": name}) for template in plan["lines"]]
        expanded = data.replace(b"FI", name.encode("ascii"))
        page, = display.display.raster(ctx, font, paint, expanded, rows, 1)
        assert page["native_independent_plane_equal"]
        if before is None:
            assert all("at his" not in row or "at his side." in row for row in rows)
        plane = bytes.fromhex(page["native_plane_hex"])
        assert len(plane) == 216 * 64
        rendered = Image.frombytes("L", (216, 64), bytes(240 if x == 0 else 20 for x in plane)).convert("RGB")
        panels.append((title, rendered))
        layouts.append(dict(scope=title, supplied_name=name, lines=rows, expanded_hex=expanded.hex(), native_page=page))
    sheet = Image.new("RGB", (896, 304), "#263238")
    labels = ImageDraw.Draw(sheet)
    for index, (title, panel) in enumerate(panels):
        x, y = index % 2 * 448, index // 2 * 152
        labels.text((x + 5, y + 3), title, fill="white")
        sheet.paste(panel.resize((432, 128), Image.Resampling.NEAREST), (x + 5, y + 19))
    sheet.save(SHEET)
    return dict(parent_sha256=release["candidate_sha256"], layouts=layouts, sheet=reference(SHEET),
                offline_native_renderer=True, original_name_token_count=1,
                display_cases_use_supplied_names=True)


def main():
    release, receipt = map(read, (parent.RELEASE, review.OUT))
    assert digest(REGISTRY) == release["registry_sha256"] and digest(CLEAN) == release["clean_input_sha256"]
    assert digest(parent.ROM) == release["candidate_sha256"] == receipt["candidate_sha256"]
    assert digest(release["manifest"]) == release["manifest_sha256"]
    row = receipt["story"]["encounter_records"][review.WRAP_ID]
    assert row["decision"] == "pending_wrap_only"
    source, target = map(NdsImage.open, (CLEAN, parent.ROM))
    clean, before = map(paths, (source, target))
    arm = before[parent.ARM]
    assert sha256(arm).hexdigest() == release["target_ARM9_sha256"]
    assert registry_guards.right_bound(arm, release["right_bound_configuration"])["matched_repair_spans"] == 8

    source_block = IlnkContainer.parse(clean[STORY]).blocks[BLOCK]
    bank = IlnkContainer.parse(before[STORY])
    current_block = bank.blocks[BLOCK]
    source_ref, current_ref = row["source_reference"], row["current_reference"]
    original = bytes.fromhex(source_ref["exact_command_hex"])
    current = bytes.fromhex(current_ref["exact_command_hex"])
    assert original[:6] == current[:6] == b"\x00\x40\xff\xff\x00\x05"
    previous_body = current[6:current.index(0, 6)]
    draft = row | dict(source_hex=original[5:original.index(0, 6)].hex(),
                       current_hex=current[5:current.index(0, 6)].hex(),
                       protected_phrases=["at his side."])
    inventory, _, _ = commands.scoped_inventory()
    compiler = checked_text(getsource(fixed.fit_training_offer), {
        "old[0] == japanese[0] == 16": "old[0] == japanese[0] == 5",
    })
    scope = vars(fixed) | dict(precedent=formatter)
    exec(compile(compiler, __file__ + "::existing-allocation", "exec"), scope)
    new, records, plans = scope["fit_training_offer"]([draft], source_block, current_block, inventory, arm)
    change, = records
    plan = plans[review.WRAP_ID]
    assert all(plan[key] == row["proposed_layout"][key] for key in ("encoded_hex", "lines"))
    assert change["current"] == current.hex() and change["current_offset"] == change["stored_offset"]
    fitted = bytes.fromhex(change["stored"])
    assert fitted[:6] == current[:6] and fitted[6:].count(b"FI") == previous_body.count(b"FI") == 1
    bank.blocks[BLOCK] = new
    archive = bank.to_bytes()
    directory_end = 8 + (len(bank.blocks) + 1) * 4
    assert archive[:directory_end] == before[STORY][:directory_end]
    target.replace_file(STORY, archive)
    after = paths(target)
    assert before.keys() == after.keys() and {key for key in after if after[key] != before[key]} == {STORY}

    guard_spec = read(REGISTRY)["profiles"][release["profile"]]["source25_multiarchive_guard"]
    guard = bind_registered_story_percent_guard(guard_spec)(clean, after)
    assert guard["total_exact_source_bound_relocated_leading25_count"] == 7
    assert not any(guard["source_bound_new_command_counts"].values())
    built = bytes(target.rom.save())
    target.replace_file(STORY, before[STORY])
    assert bytes(target.rom.save()) == parent.ROM.read_bytes()
    formatted = preview(release, target, fitted[6:fitted.index(0, 6)], plan, previous_body)
    write(NATIVE, formatted)
    ROOT.mkdir()
    ROM.write_bytes(built)
    assert paths(NdsImage.open(ROM)) == after
    write(STORED, dict(candidate=reference(ROM), previous=reference(parent.ROM), clean=reference(CLEAN),
        review=reference(review.OUT), preview=reference(NATIVE), formatting_plan=plan, edit=change,
        archive=STORY, block=BLOCK, target_archive_sha256=sha256(archive).hexdigest(),
        unchanged_archive_directory=True, unchanged_other_components=True, complete_parent_inverse=True,
        format_guard=guard, registration_pending=True))
    print("Staged Claudio's reflow in the original allocation and checked the original renderer with three name widths.")


if __name__ == "__main__":
    main()
