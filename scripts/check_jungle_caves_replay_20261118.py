"""Verify the cave choice pixels and each branch's representative body planes."""

from argparse import ArgumentParser
from types import FunctionType

from PIL import Image, ImageDraw

from scripts import check_forest_replay_20261118 as pixels
from scripts import replay_jungle_caves_20261118 as replay
from scripts import verify_forest_expeditions_20261118 as native_check
from scripts.analyze_maria301_display_v1 import verified_existing_unlock


stage, base, native, parent = replay.stage, replay.base, replay.native, replay.stage.parent
MENU = replay.ROOT / "native_retained_menu"
OUTPUT = replay.ROOT / "verified.json"
COMMON = (504, 548, 664, 782, 800, 1068)
ATTACK = COMMON + (1126, 1228, 1784, 1882, 2144, 2718, 2754)
RETREAT = COMMON + (2186, 2674, 2718, 2754)


def maria_group(proof):
    return next(g for g in proof["groups"] if g["route"] == 3 and g["block"] == 259)


def check_menu():
    release = base.load(parent.RELEASE)
    proof = base.load(stage.PROOF)
    ctx = native.RegisteredRuntime(parent.RELEASE, release["own_registered_startup"], captain=3)
    cmd = next(c for c in maria_group(proof)["commands"] if c["word"] == 0x2100)
    assert cmd["stored"] == cmd["current"]
    draft = base.load(stage.review.OUTPUT)
    identity = {r["id"]: r for r in draft["records"] if r["route"] == 3}
    rows = [identity[i] for i in cmd["record_ids"]]
    check = FunctionType(native_check.menu_checker.__code__, vars(native_check) | {"parent": parent})
    check(ctx, release, cmd, rows, MENU)


def images_for_case(case, menu, wanted_index, offsets, group, body):
    report_path = replay.ROOT / case / "capture/capture_report.json"
    report = base.load(report_path)
    setup = base.load(replay.FIXTURE)
    assert report["ROM_sha256"] == setup["fixture_sha256"] == base.digest(replay.ROM)
    assert setup["reference_ROM_sha256"] == base.digest(stage.ROM)
    assert report["cold_boot"] and not report["savestate_loaded"] and not report["callback_errors"]
    assert verified_existing_unlock(report) and setup["original_scene_commands_exact"]
    assert setup["whole_source_ROM_inverse"]
    records = {r["source_offset"]: r for r in group["commands"]}
    vm = menu["versions"][-1]["cases"][0]["native_VM"]
    assert menu["native_choice_object_hex"] == records[1090]["stored"]
    assert vm["labels"] == ["Attack!", "Run!"]
    photos = replay.previous.quest.prior.TOOL.photos(report)
    holds, cursor = [], 4350
    menu_frame = 7275
    menu_info, menu_image = photos[menu_frame]
    label = pixels.selected_option(menu_image, menu, wanted_index)
    assert label == vm["labels"][wanted_index]
    assert [item["start"] for item in report["scripted_input_schedule"]
            if item["buttons"] == ["A"] and menu_frame < item["start"] <= 7450] == [7350]
    masks = [(n, tuple(map(frozenset, replay.previous.quest.prior.TOOL.body_masks(image))))
             for n, (_, image) in sorted(photos.items())]
    for offset in offsets:
        if offset > 1090:
            cursor = max(cursor, 7350)
        cmd = records[offset]
        assert offset in setup["included_source_offsets"]
        encoded = bytes.fromhex(cmd["stored"])
        if cmd["word"] == 0x4100:
            _, bodies = native_check.unpack(encoded)
            variants = [(encoded[19], bodies[sub]) for sub in sorted(bodies)]
        else:
            assert cmd["word"] == 0x4000
            variants = [(encoded[5], encoded[6:encoded.index(0, 6)])]
        expected = {}
        for (selector, payload), ident in zip(variants, cmd["record_ids"], strict=True):
            expected.setdefault(tuple(map(frozenset, body(payload, selector))), []).append(ident)
        found = next(((n, expected[bits]) for n, bits in masks
                      if n > cursor and bits in expected), None)
        assert found is not None, (case, offset, cursor, cmd["record_ids"])
        cursor, possible = found
        ident = possible[0] if len(possible) == 1 else None
        holds.append(dict(id=ident, matching_record_ids=possible, source_offset=offset,
                          frame=cursor, capture=photos[cursor][0]))
    evidence = {str(report_path): base.digest(report_path), str(replay.FIXTURE): base.digest(replay.FIXTURE)}
    rows = [(hold["id"] or "Same body in multiple style variants", hold["frame"]) for hold in holds]
    rows.append((label, menu_frame))
    rows.sort(key=lambda item: item[1])
    sheets = []
    for start in range(0, len(rows), 8):
        part = rows[start:start + 8]
        sheet = Image.new("RGB", (888, ((len(part) + 1) // 2) * 212), "#263238")
        draw = ImageDraw.Draw(sheet)
        for i, (title, frame) in enumerate(part):
            x, y = i % 2 * 444, i // 2 * 212
            draw.text((x + 4, y + 2), f"{title} at {frame}", fill="white")
            sheet.paste(photos[frame][1].crop((0, 192, 256, 384)), (x + 4, y + 15))
        path = replay.ROOT / f"live_{case}_{start // 8 + 1}.png"
        sheet.save(path)
        sheets.append(dict(path=str(path), sha256=base.digest(path)))
    return dict(case=case, selected_label=label, menu_capture=menu_info, menu_frame=menu_frame,
                confirmed_at=7350, holds=holds, evidence=evidence, sheets=sheets)


def verify():
    assert not OUTPUT.exists()
    candidate = base.load(stage.PROOF)
    group = maria_group(candidate)
    release = base.load(parent.RELEASE)
    ctx = native.RegisteredRuntime(parent.RELEASE, release["own_registered_startup"], captain=3)
    image = base.NdsImage.open(stage.ROM)
    assert pixels.assets(image) == pixels.assets(base.NdsImage.open(replay.ROM))
    font = image.read_file("/GRP/KANJI.FNT")
    _, paint = native_check.early.prior.precedent.planners(ctx.arm)
    fe = stage.stage.system.native_painter(ctx)
    mask = replay.previous.quest.prior.TOOL.prior.masks

    def body(raw, selector):
        if selector == 254:
            plane = fe(raw)["physical"]
            cropped = b"".join(plane[y * 228:y * 228 + 216] for y in range(64))
            return mask(bytes(int(bool(value)) for value in cropped))
        current = raw.replace(b"FI", b"Maria").replace(b"FA", b"Li")
        page, = paint(ctx.arm, font, current)["pages"]
        return mask(bytes.fromhex(page["native_plane_hex"]))

    menu_path = MENU / "menu_provider_and_planes.json"
    menu = base.load(menu_path)
    attack = images_for_case("attack", menu, 0, ATTACK, group, body)
    retreat = images_for_case("run", menu, 1, RETREAT, group, body)
    assert attack["holds"][-2]["id"] == retreat["holds"][-2]["id"]
    assert attack["holds"][-1]["id"] == retreat["holds"][-1]["id"]
    assert any(hold["source_offset"] == 2144 for hold in attack["holds"])
    assert any(hold["source_offset"] == 2186 for hold in retreat["holds"])
    base.save(OUTPUT, dict(candidate_sha256=candidate["candidate_sha256"], actual_initialized_Maria=True,
        natural_activation=False, hardware=False, native_menu_proof=str(menu_path),
        native_menu_proof_sha256=base.digest(menu_path), cases=[attack, retreat]))
    print(f"Matched {len(attack['holds'])} Attack holds and {len(retreat['holds'])} Run holds.", flush=True)


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("check_menu", "verify"))
    globals()[parser.parse_args().action]()
