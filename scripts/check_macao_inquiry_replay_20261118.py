"""Match all spoken bodies in Maria's initialized Macao inquiry to native glyph planes."""

from PIL import Image, ImageDraw

from scripts import check_forest_replay_20261118 as pixels
from scripts import replay_sakura_expeditions_macao_20261118 as replay
from scripts.analyze_maria301_display_v1 import verified_existing_unlock

stage, base, native = replay.stage, replay.base, replay.native
macao = replay.MACAO


def verify():
    assert not macao.LIVE.exists()
    report_path = macao.ROOT / "live/capture/capture_report.json"
    report, setup, stored = map(base.load, (report_path, macao.FIXTURE, stage.PROOF))
    assert report["cold_boot"] and not report["savestate_loaded"] and not report["callback_errors"]
    assert verified_existing_unlock(report)
    assert report["ROM_sha256"] == setup["fixture_sha256"] == base.digest(macao.ROM)
    assert setup["original_scene_commands_exact"] and setup["whole_source_ROM_inverse"]
    assert setup["reference_ROM_sha256"] == stored["candidate_sha256"] == base.digest(stage.ROM)
    image = base.NdsImage.open(stage.ROM)
    assert pixels.assets(image) == pixels.assets(base.NdsImage.open(macao.ROM))
    arm, font = [image.read_file(path) for path in (native.ARM, "/GRP/KANJI.FNT")]
    _, paint = stage.stage.progressive.layout.prior.precedent.planners(arm)
    group = next(g for g in stored["groups"] if (g["route"], g["block"]) == (3, 276))
    assert group["after"] == setup["forest_sha256"]
    bank = native.IlnkContainer.parse(image.read_file("/data/SC3.DK4"))
    assert native.digest(bank.blocks[276]) == setup["forest_sha256"]
    assert native.digest(bank.blocks[33]) == setup["current_host_sha256"]
    assert setup["included_source_offsets"] == [c["source_offset"] for c in group["commands"][:-1]]
    tool = replay.maria.previous.previous.quest.prior.TOOL
    photos = tool.photos(report)
    masks = [(frame, tool.body_masks(image)) for frame, (_, image) in sorted(photos.items())]
    observed, cursor = [], 4250
    for cmd in group["commands"]:
        if cmd["word"] != 0x4000:
            continue
        assert cmd["source_offset"] in setup["included_source_offsets"]
        raw = bytes.fromhex(cmd["stored"])
        encoded = raw[6:raw.index(0, 6)]
        assert raw[5] != 254 and not any(token in encoded for token in (b"FI", b"FO", b"FA", b"FU"))
        target, = paint(arm, font, encoded)["pages"]
        want = tool.prior.masks(bytes.fromhex(target["native_plane_hex"]))
        found = next((n for n, bits in masks if n > cursor and bits == want), None)
        assert found is not None, (cmd["source_offset"], encoded)
        cursor = found
        ident, = cmd["record_ids"]
        observed.append(dict(id=ident, source_offset=cmd["source_offset"], frame=cursor,
                             selector=raw[5], capture=photos[cursor][0]))
    assert len(observed) == 14
    assert observed[0]["selector"] == 102 and observed[2]["selector"] == 101
    assert observed[6]["source_offset"] == 238 and observed[6]["selector"] == 101
    images = []
    for start in range(0, len(observed), 8):
        part = observed[start:start + 8]
        sheet = Image.new("RGB", (1024, 404 * ((len(part) + 1) // 2)), "#263238")
        draw = ImageDraw.Draw(sheet)
        for i, hold in enumerate(part):
            x, y = i % 2 * 512, i // 2 * 404
            draw.text((x + 4, y + 2), f"{hold['id']} at {hold['frame']}", fill="white")
            body = photos[hold["frame"]][1].crop((0, 192, 256, 384))
            sheet.paste(body.resize((512, 384), Image.Resampling.NEAREST), (x, y + 16))
        path = macao.ROOT / f"macao_live_{start // 8 + 1}.png"
        sheet.save(path)
        images.append(dict(path=str(path), sha256=base.digest(path)))
    base.save(macao.LIVE, dict(candidate_sha256=stored["candidate_sha256"], initialized_Maria=True,
        exact_original_commands=True, natural_activation=False, hardware=False,
        observed_dialogue_fee_only=True, payment_accounting_not_sampled=True,
        holds=observed, sheets=images,
        evidence={str(path): base.digest(path) for path in (report_path, macao.FIXTURE)}))
    print("Matched all 14 complete Macao inquiry holds, including the 1,000-gold-coin fee.")

if __name__ == "__main__":
    verify()
