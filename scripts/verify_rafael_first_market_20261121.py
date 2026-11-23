"""Check native render, exact retention, and ordinary play for the Market lesson."""
from argparse import ArgumentParser
from types import FunctionType

from PIL import ImageChops

from scripts import replay_rafael_first_market_20261121 as run
from scripts import verify_all_routes_next_phrase_wraps_20261118 as native_display
from scripts import verify_lisbon_seoul_trend_gameplay_20261121 as panel


stage, town = run.stage, panel.town
base, native = stage.base, stage.native
ROOT = stage.ROOT / "native_display"
PROOF = ROOT / "native_display.json"
LIVE = run.ROOT / "verified_market.json"


def verify_native():
    assert not PROOF.exists()
    parent = base.load(stage.parent.RELEASE)
    ctx = native.RegisteredRuntime(stage.parent.RELEASE, parent["own_registered_startup"], captain=3)
    stored, review = map(base.load, (stage.PROOF, stage.review.OUTPUT))
    candidate = base.digest(stage.ROM)
    assert stored["candidate_sha256"] == candidate and stored["manuscript_sha256"] == base.digest(stage.review.OUTPUT)
    assert stored["predecessor_sha256"] == parent["candidate_sha256"] and stored["whole_parent_inverse"]
    image = base.NdsImage.open(stage.ROM)
    assert all(ctx.image.read_file(path) == image.read_file(path) for path in native_display.ASSETS)
    font = image.read_file("/GRP/KANJI.FNT")
    paint, expand = native_display.clipped_renderer(ctx), native_display.original_expander()
    validate = native_display.display.paragraph
    validate = FunctionType(validate.__code__, validate.__globals__ | {"build": stage})
    group, = stored["groups"]
    path = group["file_path"]
    block = native.IlnkContainer.parse(image.read_file(path)).blocks[137]
    assert native.digest(block) == group["after"]
    rows = {row["id"]: row for row in review["records"]}
    verified, previews = [], []
    for command in group["commands"]:
        raw = bytes.fromhex(command["stored"])
        at = command["stored_offset"]
        assert block[at:at + len(raw)] == raw
        for ident in command["record_ids"]:
            row = rows.pop(ident)
            result = dict(id=ident, file_path=path, decision=row["decision"], stored_offset=at, stored_command_hex=raw.hex())
            if row["decision"] == "retention":
                assert command["stored"] == command["current"]
            else:
                assert command["word"] == 0x4000 and raw[:6] == b"\0\x40\xff\xff\0\x06"
                assert raw[:6].hex() == command["current"][:12]
                end = raw.index(0, 6)
                assert not any(raw[end:]) and not stage.review.TOKEN.findall(row["english"])
                audit = validate(ctx, font, paint, expand, None, {}, row, raw[5:end], group["plans"][ident])
                layout, = audit["layouts"]
                page, = layout["pages"]
                assert page["native_independent_plane_equal"]
                pixels = bytes.fromhex(page["native_plane_hex"])
                previews.append((ident, pixels))
                result.update(native_pages=1, expanded_hex=layout["expanded_hex"], lines=layout["lines"],
                              plane_sha256=native.digest(pixels), original_expansion=audit["macro_alignment_checks"])
            verified.append(result)
    assert not rows and len(verified) == 14 and len(previews) == 7
    ROOT.mkdir()
    contact = native_display.display.inherited.early.contact_sheets
    sheets = FunctionType(contact.__code__, contact.__globals__ | {"ROOT": ROOT})(previews)
    base.save(PROOF, dict(candidate_sha256=candidate, stage_proof_sha256=base.digest(stage.PROOF),
        records=verified, newly_rendered_pages=len(previews), offline_native_only=True, sheets=sheets))
    print("Seven new pages passed original native expansion, rendering, and bounds. Seven commands retain their exact wording.")


def verify_live():
    assert not LIVE.exists()
    candidate = base.digest(stage.ROM)
    report, prior, verified, draft = map(base.load, (run.REPORT, stage.review.replay.REPORT, PROOF, stage.review.OUTPUT))
    assert candidate == report["ROM_sha256"] == verified["candidate_sha256"]
    assert prior["ROM_sha256"] == draft["previous_sha256"] == base.digest(stage.parent.ROM)
    assert base.digest(stage.review.replay.REPORT) == draft["previous_gameplay_report_sha256"]
    for live in (report, prior):
        assert live["cold_boot"] and not live["savestate_loaded"] and not live["callback_errors"]
        assert not live.get("battery_save_preloaded")
        assert not any(value for key, value in live.items() if key.startswith("synthetic_"))
    assert report["scripted_input_schedule"] == prior["scripted_input_schedule"]
    assert report["frames"] == prior["frames"] == 40735
    assert report["core_options"] == prior["core_options"]
    assert base.digest(stage.ROOT / "clean_rebuilt.nds") == candidate
    frames = {r["frame"]: r for r in report["frames_captured"] if r["path"].endswith("_cold_boot.png")}
    previous_frames = {r["frame"]: r for r in prior["frames_captured"] if r["path"].endswith("_navigation.png")}
    image = base.NdsImage.open(stage.ROM)
    arm, font = (image.read_file(path) for path in (native.ARM, "/GRP/KANJI.FNT"))
    ctx = native.RegisteredRuntime(stage.parent.RELEASE, base.load(stage.parent.RELEASE)["own_registered_startup"], captain=3)
    painter, names = native_display.clipped_renderer(ctx), panel.GameAsciiFont.from_arm9(arm)
    layout = {r["id"]: r for r in verified["records"]}
    holds, unchanged, pairs = [], [], []
    for row in draft["records"]:
        if row["kind"] == "typed-choice-label":
            continue
        frame = row["previous_capture"]["frame"]
        old_shot, old = town.read_frame(previous_frames, frame)
        shot, picture = town.read_frame(frames, frame)
        if row["decision"] == "retention":
            assert old_shot["framebuffer_sha256"] == shot["framebuffer_sha256"], row["id"]
            unchanged.append(shot)
            continue
        result = layout[row["id"]]
        body = bytes.fromhex(result["expanded_hex"])
        painted = painter(arm, font, body)
        page, = painted["pages"]
        raw = bytes.fromhex(page["native_plane_hex"])
        assert native.digest(raw) == result["plane_sha256"] and panel.mask_check(raw, 216, picture), row["id"]
        panel.complete_mask(names, "Julio Erneco", picture, 16, 277, town.INKS[1])
        diff = ImageChops.difference(old, picture)
        diff.paste((0, 0, 0), (16, 296, 232, 360))
        assert diff.getbbox() is None
        pairs.extend(((row["id"] + " before", old), (row["id"] + " revised", picture)))
        holds.append(dict(id=row["id"], file_path=row["file_path"], frame=frame, previous=old_shot, revised=shot))
    for frame in (32225, 32765, 37085, 39435, 40735):
        shot, _ = town.read_frame(frames, frame)
        old_shot, _ = town.read_frame(previous_frames, frame)
        assert old_shot["framebuffer_sha256"] == shot["framebuffer_sha256"], frame
        unchanged.append(shot)
    assert len(holds) == 7 and len(unchanged) == 10
    sheets = []
    for pos in range(0, len(pairs), 6):
        target = run.ROOT / f"market_before_after_{pos // 6 + 1}.png"
        town.sheet(pairs[pos:pos + 6], target)
        sheets.append(dict(path=str(target), sha256=base.digest(target)))
    base.save(LIVE, dict(candidate_sha256=candidate, holds=holds, unchanged_controls=unchanged,
        natural_activation=True, exact_native_glyph_matches=True, hardware_verified=False,
        original_preparation_menu_market_share_choice_and_market_return=True, sheets=sheets,
        evidence={str(p): base.digest(p) for p in (run.REPORT, stage.review.replay.REPORT, stage.review.replay.PROOF, PROOF)}))
    print("Seven revised Market panels matched the complete native glyph masks. Ten unchanged holds matched byte for byte.")


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("check", choices=("native", "live"))
    (verify_native if parser.parse_args().check == "native" else verify_live)()
