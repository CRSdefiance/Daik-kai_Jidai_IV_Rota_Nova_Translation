"""Compare the fog choices and both Verisa entries to the native raster output."""

from argparse import ArgumentParser
from types import FunctionType

from PIL import Image, ImageDraw

from scripts import check_forest_replay_20261118 as pixels
from scripts import replay_caves_offshore_monk_20261118 as game
from scripts import verify_forest_expeditions_20261118 as display
from scripts.analyze_maria301_display_v1 import verified_existing_unlock

stage, base, native, parent = game.stage, game.base, game.native, game.stage.parent
EARLIER = stage.ROOT.with_name("research_v1")
REPLY_STAGE = stage.ROOT.with_name("research_v2")
FOG_ROOT = EARLIER / game.ROOT.name
FOG_ROM, FOG_SETUP = FOG_ROOT / game.ROM.name, FOG_ROOT / game.SETUP.name
VERISA_ROOT = EARLIER / game.MARIA_ROOT.name
REPLY_ROOT = REPLY_STAGE / game.REPLY_ROOT.name
MENU_ROOT = EARLIER / "fog_menu"
LIVE = stage.ROOT / "verified_replays.json"
PICKS = ((1756, 4100, 4150, "Keep going"), (1984, 4800, 4850, "Push on anyway"))
FOG_REFS = (1602, 1804, 2026, 2244, 2800)
VERISA_CASES = (
    (VERISA_ROOT, VERISA_ROOT / game.MARIA_ROM.name, VERISA_ROOT / game.MARIA_FIXTURE.name, (12, 32, 116)),
    (REPLY_ROOT, REPLY_ROOT / game.REPLY_ROM.name, REPLY_ROOT / game.REPLY_FIXTURE.name, (244, 258, 280, 378, 432)),
)


def scene(proof, route, block):
    return next(g for g in proof["groups"] if (g["route"], g["block"]) == (route, block))


def menus():
    release = base.load(parent.RELEASE)
    staged = base.load(stage.PROOF)
    rows = {r["id"]: r for r in base.load(stage.review.OUTPUT)["records"] if r["route"] == 0}
    group = scene(staged, 0, 332)
    display_menu = FunctionType(display.menu_checker.__code__, vars(display) | {"parent": parent})
    ctx = native.RegisteredRuntime(parent.RELEASE, release["own_registered_startup"], captain=3)
    MENU_ROOT.mkdir()
    items = []
    for offset, _, _, label in PICKS:
        command = next(c for c in group["commands"] if c["source_offset"] == offset)
        assert command["word"] == 0x2100
        receipt = display_menu(ctx, release, command, [rows[i] for i in command["record_ids"]],
                               MENU_ROOT / str(offset))
        proof = base.load(receipt["menu_path"])
        assert proof["versions"][-1]["cases"][0]["native_VM"]["labels"][0] == label
        items.append(receipt | dict(source_offset=offset, changed=command["current"] != command["stored"]))
    base.save(MENU_ROOT / "menus.json", items)


def sheets(folder, images, photos, label):
    receipts = []
    for start in range(0, len(images), 6):
        rows = images[start:start + 6]
        sheet = Image.new("RGB", (1024, 404 * ((len(rows) + 1) // 2)), "#263238")
        draw = ImageDraw.Draw(sheet)
        for i, (title, frame) in enumerate(rows):
            x, y = i % 2 * 512, i // 2 * 404
            draw.text((x + 4, y + 2), f"{title} at {frame}", fill="white")
            body = photos[frame][1].crop((0, 192, 256, 384))
            sheet.paste(body.resize((512, 384), Image.Resampling.NEAREST), (x, y + 16))
        path = folder / f"{label}_{start // 6 + 1}.png"
        sheet.save(path)
        receipts.append(dict(path=str(path), sha256=base.digest(path)))
    return receipts


def match_bodies(commands, offsets, masks, raster, name, tool, photos, first_frame):
    found = []
    cursor = first_frame
    for offset in offsets:
        cmd = commands[offset]
        raw = bytes.fromhex(cmd["stored"])
        if cmd["word"] == 0x4100:
            _, segments = display.unpack(raw)
            variants = [(raw[19], segments[at]) for at in sorted(segments)]
        else:
            assert cmd["word"] == 0x4000
            variants = [(raw[5], raw[6:raw.index(0, 6)])]
        expected = {}
        for ident, (selector, body) in zip(cmd["record_ids"], variants, strict=True):
            if selector != 254:
                body = body.replace(b"FI", name)
            plane = raster(body, selector)
            key = tuple(map(frozenset, tool.prior.masks(plane)))
            expected.setdefault(key, []).append((ident, selector))
        hit = next(((frame, expected[bits]) for frame, bits in masks if frame > cursor and bits in expected), None)
        assert hit is not None, (offset, cursor, variants)
        cursor, matches = hit
        found.append(dict(source_offset=offset, frame=cursor, id=matches[0][0] if len(matches) == 1 else None,
                          selector=matches[0][1], matching_record_ids=[r[0] for r in matches],
                          capture=photos[cursor][0]))
    return found


def verify():
    assert not LIVE.exists()
    proof, release = map(base.load, (stage.PROOF, parent.RELEASE))
    group = scene(proof, 0, 332)
    earlier_proof = base.load(EARLIER / stage.PROOF.name)
    earlier_rom = EARLIER / stage.ROM.name
    assert earlier_proof["candidate_sha256"] == base.digest(earlier_rom)
    earlier = base.NdsImage.open(earlier_rom)
    image = base.NdsImage.open(stage.ROM)
    assert pixels.assets(image) == pixels.assets(earlier)
    reply_image = base.NdsImage.open(REPLY_STAGE / stage.ROM.name)
    reply_proof = base.load(REPLY_STAGE / stage.PROOF.name)
    assert reply_proof["candidate_sha256"] == base.digest(REPLY_STAGE / stage.ROM.name)
    assert pixels.assets(image) == pixels.assets(reply_image)
    arm, font = [image.read_file(p) for p in (native.ARM, "/GRP/KANJI.FNT")]
    assert proof["candidate_sha256"] == base.digest(stage.ROM)
    ctx = native.RegisteredRuntime(parent.RELEASE, release["own_registered_startup"], captain=3)
    assert ctx.arm == arm
    _, paint = stage.stage.progressive.layout.prior.precedent.planners(arm)
    fe_paint = stage.stage.system.native_painter(ctx)
    tool = game.rafael.scope["quest"].prior.TOOL

    def raster(body, selector):
        if selector == 254:
            physical = fe_paint(body)["physical"]
            return bytes(int(bool(v)) for y in range(64) for v in physical[y * 228:y * 228 + 216])
        page, = paint(arm, font, body)["pages"]
        return bytes.fromhex(page["native_plane_hex"])

    def images(report):
        photos = tool.photos(report)
        masks = [(n, tuple(map(frozenset, tool.body_masks(img)))) for n, (_, img) in sorted(photos.items())]
        return photos, masks

    evidence = {}
    path = FOG_ROOT / "capture/capture_report.json"
    report, setup = map(base.load, (path, FOG_SETUP))
    assert report["cold_boot"] and not report["savestate_loaded"] and not report["callback_errors"]
    assert not report.get("battery_save_preloaded")
    assert report["ROM_sha256"] == setup["fixture_sha256"] == base.digest(FOG_ROM)
    assert setup["candidate_sha256"] == earlier_proof["candidate_sha256"] and setup["whole_ROM_inverse"]
    assert setup["original_fog_commands_exact"] and not setup["natural_activation"]
    assert pixels.assets(image) == pixels.assets(base.NdsImage.open(FOG_ROM))
    old, new = [native.IlnkContainer.parse(i.read_file("/data/SC0.DK4")).blocks for i in (earlier, image)]
    assert old[44] == new[44] and old[332] == new[332]
    assert native.digest(new[332]) == group["after"]
    evidence.update({str(p): base.digest(p) for p in (path, FOG_SETUP, EARLIER / stage.PROOF.name)})
    commands = {c["source_offset"]: c for c in group["commands"]}
    assert all(n in setup["included_source_offsets"] for n in (*FOG_REFS, *(x[0] for x in PICKS)))
    photos, masks = images(report)
    fog = match_bodies(commands, FOG_REFS, masks, raster, b"Rafael", tool, photos, 3650)
    menu_notes, contacts = [], []
    captions = base.load(MENU_ROOT / "menus.json")
    for (offset, frame, confirm, label), caption in zip(PICKS, captions, strict=True):
        menu_path = caption["menu_path"]
        assert caption["proof_sha256"] == base.digest(menu_path)
        actual = base.load(menu_path)
        assert actual["native_choice_object_hex"] == commands[offset]["stored"]
        assert pixels.selected_option(photos[frame][1], actual, 0) == label
        assert [i["start"] for i in report["scripted_input_schedule"]
                if i["buttons"] == ["A"] and frame < i["start"] <= confirm] == [confirm]
        assert any(h["frame"] < frame for h in fog) and any(h["frame"] > confirm for h in fog)
        menu_notes.append(dict(source_offset=offset, capture=photos[frame][0], selected=label,
                               confirmation=confirm, native_receipt=caption))
        contacts.append(actual["review_sheet"])
        evidence[menu_path] = caption["proof_sha256"]
    fog_timeline = [(h["id"] or "Crew reply", h["frame"]) for h in fog]
    fog_timeline.extend((n["selected"], n["capture"]["frame"]) for n in menu_notes)
    fog_timeline.sort(key=lambda item: item[1])
    contacts += sheets(stage.ROOT, fog_timeline, photos, "fog_live")
    all_holds = list(fog)
    for case, rom, fixture, offsets in VERISA_CASES:
        path = case / "live/capture/capture_report.json"
        report, setup = map(base.load, (path, fixture))
        assert verified_existing_unlock(report) and report["cold_boot"] and not report["callback_errors"]
        assert not report["savestate_loaded"] and not setup["natural_unlock"]
        assert report["ROM_sha256"] == setup["fixture_sha256"] == base.digest(rom)
        assert setup["whole_source_ROM_inverse"]
        assert setup["original_scene_commands_exact"] and set(offsets) <= set(setup["included_source_offsets"])
        assert pixels.assets(image) == pixels.assets(base.NdsImage.open(rom))
        group = scene(proof, 3, 286)
        if case == VERISA_ROOT:
            assert setup["reference_ROM_sha256"] == earlier_proof["candidate_sha256"]
            original = scene(earlier_proof, 3, 286)
            assert original["after"] == setup["forest_sha256"]
            assert [c["stored"] for c in original["commands"] if c["source_offset"] <= 220] == [
                c["stored"] for c in group["commands"] if c["source_offset"] <= 220]
            a, b = [native.IlnkContainer.parse(rom.read_file("/data/SC3.DK4")).blocks[33] for rom in (earlier, image)]
            assert native.digest(a) == native.digest(b) == setup["current_host_sha256"]
        else:
            assert setup["reference_ROM_sha256"] == reply_proof["candidate_sha256"]
            now, prior = [native.IlnkContainer.parse(rom.read_file("/data/SC3.DK4")).blocks
                          for rom in (image, reply_image)]
            assert now[286] == prior[286] and native.digest(now[286]) == setup["forest_sha256"]
            assert now[33] == prior[33] and native.digest(now[33]) == setup["current_host_sha256"]
            assert group["after"] == setup["forest_sha256"] == scene(reply_proof, 3, 286)["after"]
            evidence[str(REPLY_STAGE / stage.PROOF.name)] = base.digest(REPLY_STAGE / stage.PROOF.name)
        commands = {c["source_offset"]: c for c in group["commands"]}
        photos, masks = images(report)
        holds = match_bodies(commands, offsets, masks, raster, b"Maria", tool, photos, 4250)
        assert [h["selector"] for h in holds] == ([204] * 3 if len(offsets) == 3 else [0, 204, 204, 0, 204])
        contacts += sheets(stage.ROOT, [(h["id"], h["frame"]) for h in holds], photos, f"{case.name}_live")
        all_holds.extend(holds)
        evidence.update({str(p): base.digest(p) for p in (path, fixture)})
    assert len(all_holds) == 13 and len(menu_notes) == 2
    base.save(LIVE, dict(candidate_sha256=proof["candidate_sha256"], initialized_Rafael=True,
        initialized_Maria=True, exact_original_commands=True, natural_activation=False, hardware=False,
        two_fog_choices_confirmed=True, Verisa_entries_sampled_separately=True, holds=all_holds,
        exact_reused_dependency_scope=dict(Rafael_fog_block=332, Maria_Verisa_entry_through_original_return=220,
                                           fog_and_opening_source_candidate_sha256=earlier_proof["candidate_sha256"],
                                           Maria_Verisa_reply_source_candidate_sha256=reply_proof["candidate_sha256"]),
        menus=menu_notes, sheets=contacts, evidence=evidence))
    print("Matched both fog choices, five Rafael fog holds and both original Verisa entries.", flush=True)


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("menus", "verify"))
    globals()[parser.parse_args().action]()
