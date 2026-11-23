"""Check the focused emulator pages, nameplates and original artwork transitions."""

from hashlib import sha256
from types import SimpleNamespace

from scripts import check_rafael_mediterranean_gameplay_20261121 as panel
from scripts import replay_rafael_spain_london_20261121 as replay
from scripts import verify_rafael_spain_london_20261121 as display


stage, base, native, town = replay.stage, replay.base, replay.native, panel.town
PROOF = replay.ROOT / "verified_gameplay.json"
REFERENCE_STAGE = display.REFERENCE_STAGE
REFERENCE_ROOT = REFERENCE_STAGE / "focused_gameplay"
REFERENCE_GAMEPLAY = REFERENCE_ROOT / "verified_gameplay.json"


def planes_for(row, result, proof, image, paint, fe):
    if result.get("system_FE"):
        assert row["source_selector"] == 254
        body = bytes.fromhex(result["expanded_hex"])
        plane = fe(body)["physical"]
        assert native.digest(plane) == result["panel_mask_sha256"]
        return [plane]
    if row["decision"] == "revision":
        layout = result["layouts"][0]
        assert layout["scope"] == "registered default"
        body = bytes.fromhex(layout["expanded_hex"])
    else:
        raw = bytes.fromhex(row["current_hex"])[1:].decode("ascii")
        body = stage.review.TOKEN.sub(lambda m: proof["default_names"][m[0]], raw).encode("ascii")
    arm, font = (image.read_file(path) for path in (native.ARM, "/GRP/KANJI.FNT"))
    rendered = paint(arm, font, body)
    assert rendered["complete_consumed_bytes"] == len(body)
    planes = [bytes.fromhex(page["native_plane_hex"]) for page in rendered["pages"]]
    if row["decision"] == "revision":
        assert [native.digest(plane) for plane in planes] == layout["page_sha256"]
    return planes


def keep_verified_pages(image, proof, fresh):
    old_report, earlier, current, old_display, fixture = map(base.load, (
        REFERENCE_GAMEPLAY, REFERENCE_STAGE / stage.PROOF.name, stage.PROOF,
        display.REFERENCE_DISPLAY, REFERENCE_ROOT / "fixture.json"))
    old_rom = REFERENCE_STAGE / stage.ROM.name
    assert old_report["candidate_sha256"] == earlier["candidate_sha256"] == old_display["candidate_sha256"] == base.digest(old_rom)
    prior = base.NdsImage.open(old_rom)
    assert all(prior.read_file(asset) == image.read_file(asset) for asset in display.display.ASSETS)
    previous_bank, current_bank = [native.IlnkContainer.parse(rom.read_file(replay.PATH)).blocks for rom in (prior, image)]
    assert previous_bank[44] == current_bank[44] and earlier["groups"][-1]["commands"][-1]["stored"] == current["groups"][-1]["commands"][-1]["stored"]
    old_position = {(g["block"], c["stored_offset"]): c for g in earlier["groups"] for c in g["commands"]}
    new_source = {(g["block"], c["source_offset"]): c for g in current["groups"] for c in g["commands"]}
    for row in fixture["copied"]:
        if not row["ids"]:
            group = row["block"]
            before = old_position[group, row["actual_block_offset"]]
            after = new_source[group, before["source_offset"]]
            at, value = after["stored_offset"], bytes.fromhex(row["hex"])
            assert before["stored"] == after["stored"] == row["hex"]
            assert current_bank[group][at:at + len(value)] == value
    p, q = [{row["id"]: row for row in r["records"]} for r in (old_display, proof)]
    kept, retired = [], set()
    for hold in old_report["holds"]:
        ident, block = hold["id"], hold["block"]
        a, b = p[ident], q[ident]
        if a["stored_command_hex"] != b["stored_command_hex"]:
            retired.add(ident)
            continue
        at, value = b["stored_offset"], bytes.fromhex(a["stored_command_hex"])
        assert current_bank[block][at:at + len(value)] == value
        assert a.get("layouts") == b.get("layouts") and a.get("panel_mask_sha256") == b.get("panel_mask_sha256")
        assert base.digest(hold["observed"]["path"]) == hold["observed"]["PNG_sha256"]
        kept.append(hold)
    assert retired == fresh & set(old_report["observed_ids"])
    assert len(retired) == 2 and len(old_report["FE_top_screen_sha256"]) == 4
    assert old_report["reclaimed_page_turns_observed"] == 2
    assert all(base.digest(s["path"]) == s["sha256"] for s in old_report["sheets"])
    return old_report, kept, sorted(retired)


def main():
    assert not PROOF.exists()
    fixture_path, inputs = [replay.ROOT / name for name in ("fixture.json", "inputs.json")]
    fixture, report, proof, draft = map(base.load, (fixture_path, replay.REPORT, display.PROOF, stage.OUTPUT))
    candidate = base.digest(stage.ROM)
    assert candidate == proof["candidate_sha256"] == fixture["candidate_sha256"] == base.digest(stage.ROOT / "clean_rebuilt.nds")
    assert report["ROM_sha256"] == fixture["fixture_ROM_sha256"] == base.digest(fixture["fixture_ROM"])
    assert fixture["exact_candidate_inverse"] and fixture["final_wrap_refinements"]
    assert fixture["original_scene_branches_unexecuted"] and not fixture["natural_activation"]
    assert report["cold_boot"] and not report["savestate_loaded"] and not report["callback_errors"]
    assert not report.get("battery_save_preloaded") and report["frames"] == fixture["end"]
    assert not any(value for key, value in report.items() if key.startswith("synthetic_"))
    assert report["scripted_input_schedule"] == base.load(inputs)

    image = base.NdsImage.open(stage.ROM)
    bank = native.IlnkContainer.parse(image.read_file(replay.PATH)).blocks
    assert bank[44][8:40].hex() == fixture["original_prelude"]
    assert all(bank[x["block"]][x["actual_block_offset"]:][:len(bytes.fromhex(x["hex"]))].hex() == x["hex"]
               for x in fixture["copied"])
    arm = image.read_file(native.ARM)
    context = SimpleNamespace(image=image, arm=arm)
    paint, fe = town.clipped_renderer(context), town.current_fe_painter(context)
    name_font = panel.panel.GameAsciiFont.from_arm9(arm)
    captures = {row["frame"]: row for row in report["frames_captured"] if row["path"].endswith("_cold_boot.png")}
    records = {row["id"]: row for row in draft["records"]}
    native_rows = {row["id"]: row for row in proof["records"]}
    frames = iter(fixture["scheduled_holds"][:-1])
    held, pictures, pictures_top = [], [], {}
    for command in fixture["copied"]:
        if not command["ids"]:
            continue
        ident, = command["ids"]
        source, native_row = records[ident], native_rows[ident]
        system = source["source_selector"] == 254
        for index, plane in enumerate(planes_for(source, native_row, proof, image, paint, fe), 1):
            for frame in frames:
                captured, shown = town.read_frame(captures, frame)
                body_rect = shown.crop((16, 296, 16 + (228 if system else 216), 360))
                if town.INKS[1] in body_rect.get_flattened_data():
                    continue
                if panel.panel.mask_check(plane, 228 if system else 216, shown):
                    break
            else:
                raise AssertionError((ident, index, [r["id"] for r in held][-3:]))
            if not system:
                panel.panel.complete_mask(name_font, source["speaker"], shown, 16, 277, town.INKS[1])
            else:
                pictures_top[ident] = sha256(shown.crop((0, 0, 256, 192)).tobytes()).hexdigest()
            held.append(dict(id=ident, block=source["block"], page=index, frame=frame, decision=source["decision"],
                             speaker=source["speaker"], system_FE=system, observed=captured))
            pictures.append((ident, shown))
    assert not pictures_top and len(held) == len(replay.REFINEMENTS)
    final, shown = town.read_frame(captures, fixture["scheduled_holds"][-1])
    pictures.append(("Return after the focused excerpts", shown))
    sheets = []
    for index in range(0, len(pictures), 6):
        path = replay.ROOT / f"spain_london_refinements_{index // 6 + 1}.png"
        town.sheet(pictures[index:index + 6], path)
        sheets.append(dict(path=str(path), sha256=base.digest(path)))
    previous, reused, retired = keep_verified_pages(image, proof, {row["id"] for row in held})
    held = reused + held
    ids = {row["id"] for row in held}
    assert len(ids) == len(held) == 43
    evidence = previous["evidence"] | {str(path): base.digest(path) for path in (
        fixture_path, inputs, replay.REPORT, display.PROOF, fixture["fixture_ROM"], REFERENCE_GAMEPLAY)}
    base.save(PROOF, dict(candidate_sha256=candidate, initialized_excerpts=True, natural_activation=False,
        exact_native_glyph_matches=True, hardware_verified=False, holds=held, observed_ids=sorted(ids),
        original_story_branches_unvisited=True, original_picture_switches_exercised=True,
        FE_top_screen_sha256=previous["FE_top_screen_sha256"], retired_ids=retired,
        reclaimed_page_turns_observed=2, final_hold=final, reference_final_hold=previous["final_hold"],
        sheets=previous["sheets"] + sheets, evidence=evidence,
        offline_only=[row["id"] for row in draft["records"] if row["decision"] == "revision" and row["id"] not in ids]))
    print(f"Verified {len(held)} replayed pages, all four FE panels and two one-press transitions.")


if __name__ == "__main__":
    main()
