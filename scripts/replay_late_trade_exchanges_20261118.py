"""Play exact dialogue excerpts through the initialized Lil and Maria openings."""

from argparse import ArgumentParser
from struct import pack_into
import sys
from types import FunctionType

from PIL import Image, ImageDraw

from scripts import headless_desmume_v193 as harness
from scripts import replay_forest_expeditions_20261118 as maria
from scripts import replay_london_guild_assignments_20261118 as precedent
from scripts import stage_late_trade_exchanges_20261118 as stage
from scripts.analyze_maria301_display_v1 import verified_existing_unlock
from scripts.verify_late_trade_exchanges_20261118 import lil_context

base, native = stage.base, stage.native
ROOT = stage.ROOT / "trade_initialized"
LIVE = ROOT / "trade_replay.json"
SETUP = ROOT / "trade_fixture.json"
ROM = ROOT / "lil/Lil_Trade_Excerpts_RESEARCH_ONLY.nds"
MARIA_ROM = ROOT / "maria/Maria_Trade_Excerpts_RESEARCH_ONLY.nds"
MARIA_SETUP = ROOT / "maria/fixture.json"
LIL = ((319, (5, 8, 11, 14, 18, 22)), (327, (28, 31, 35)), (328, (40,)))
MARIA = ((289, (26,)), (290, (5, 9, 14, 36, 47, 50, 53, 57)))


def prepare_excerpts(route, host_index, entry_end, pairs, rom):
    stored = base.load(stage.PROOF)
    assert stored["candidate_sha256"] == base.digest(stage.ROM)
    rows = {(r["block"], r["source_reference"]["record_index"]): r["id"]
            for r in base.load(stage.review.OUTPUT)["records"] if r["route"] == route}
    groups = {g["block"]: g for g in stored["groups"] if g["route"] == route}
    image = base.NdsImage.open(stage.ROM)
    file = f"/data/SC{route}.DK4"
    original = image.read_file(file)
    bank = native.IlnkContainer.parse(original)
    host = bank.blocks[host_index]
    arm = image.read_file(native.ARM)
    inventory, _, _ = native.scoped_inventory()
    host_commands, host_speeches = inventory(arm, host)
    prefix = [cmd["word"] for cmd in host_commands if cmd["offset"] < entry_end]
    assert host_speeches[0]["offset"] == entry_end
    if route == 2:
        suffix = host[stage.logical_end(host) - 14:stage.logical_end(host)]
        assert suffix == bytes.fromhex("00c200a0ffff2c081b8200000000") and len(prefix) == 9
    else:
        last = host_speeches[-1]
        suffix = host[last["offset"] + last["native_extent"]:stage.logical_end(host)]
        assert suffix[:2] == b"\x40\x62" and suffix[-4:] == bytes(4) and len(prefix) == 7
    selected = []
    for n, indices in pairs:
        assert native.digest(bank.blocks[n]) == groups[n]["after"]
        for index in indices:
            ident = rows[n, index]
            cmd = next(c for c in groups[n]["commands"] if c["record_ids"] == [ident])
            raw = bytes.fromhex(cmd["stored"])
            offset = cmd["stored_offset"]
            assert cmd["word"] == 0x4000 and bank.blocks[n][offset:offset + len(raw)] == raw
            selected.append(dict(id=ident, block=n, source_record_index=index, stored_offset=offset,
                                 stored_command_hex=raw.hex()))
    host_excerpt = bytearray(host[:entry_end] + bytes.fromhex("".join(r["stored_command_hex"] for r in selected)) + suffix)
    pack_into("<H", host_excerpt, 4, len(host_excerpt) - 8)
    host_excerpt = bytes(host_excerpt) + bytes(-len(host_excerpt) % 4)
    commands, speeches = inventory(arm, host_excerpt)
    assert [cmd["word"] for cmd in commands[:len(prefix)]] == prefix
    assert [cmd["whole_command_hex"] for cmd in speeches] == [r["stored_command_hex"] for r in selected]
    rom.parent.mkdir(parents=True)
    bank.blocks[host_index] = host_excerpt
    image.replace_file(file, bank.to_bytes())
    image.save(rom)
    bank.blocks[host_index] = host
    assert bank.to_bytes() == original
    image.replace_file(file, original)
    assert bytes(image.rom.save()) == stage.ROM.read_bytes()
    return dict(candidate_sha256=stored["candidate_sha256"], fixture=str(rom),
                fixture_sha256=base.digest(rom), exact_original_commands=True, whole_source_ROM_inverse=True,
                route=route, host_sha256=native.digest(host), selected=selected)


def prepare():
    lil = prepare_excerpts(2, 22, 56, LIL, ROM)
    inputs = base.load(stage.ROOT.with_name("research_v1") / "lil_snapshot_inputs.json")
    inputs += [dict(start=n, duration=5, buttons=["A"]) for n in range(3800, 7051, 275)]
    input_path = ROM.parent / "inputs.json"
    base.save(input_path, inputs)
    base.save(SETUP, lil | dict(inputs=str(input_path), inputs_sha256=base.digest(input_path)))

    schema = prepare_excerpts(3, 33, 34, MARIA, MARIA_ROM)
    unlock_ref = maria.quest.prior.precedent
    unlock = base.load(unlock_ref.HISTORICAL)
    unlock.update(production_ROM=str(MARIA_ROM), production_ROM_sha256=base.digest(MARIA_ROM),
                  current_test_scope="Initialized Maria dialogue excerpts only, without trade outcomes.")
    unlock_path = MARIA_ROM.parent / "existing_system_only_unlock.json"
    base.save(unlock_path, unlock)
    unlock_ref.validate_fixture(unlock_path)
    base.save(MARIA_SETUP, schema | dict(unlock=str(unlock_path)))


def capture_lil():
    setup = base.load(SETUP)
    assert setup["fixture_sha256"] == base.digest(ROM) and setup["inputs_sha256"] == base.digest(setup["inputs"])
    sys.argv = [sys.argv[0], "--rom", str(ROM), "--out", str(ROM.parent / "capture"),
                "--frames", "7301", "--inputs-json", setup["inputs"], "--capture-every", "999999",
                "--capture-at", *map(str, range(3650, 7301, 25))]
    harness.main()


def capture_maria():
    scope = vars(maria) | {"ROOT": MARIA_ROM.parent, "ROM": MARIA_ROM, "FIXTURE": MARIA_SETUP}
    FunctionType(maria.capture.__code__, scope)("live", [(n, "A") for n in range(4200, 7601, 350)], 7801)


def verify():
    assert not LIVE.exists()
    image = base.NdsImage.open(stage.ROM)
    arm = image.read_file(native.ARM)
    font = image.read_file("/GRP/KANJI.FNT")
    _, paint = stage.stage.progressive.layout.prior.precedent.planners(arm)
    fe_paint = stage.stage.system.native_painter(lil_context())
    tool = precedent.quest.prior.TOOL
    observed, evidence, sheets = [], {}, []
    for label, setup_path, report_path in (
        ("lil", SETUP, ROM.parent / "capture/capture_report.json"),
        ("maria", MARIA_SETUP, MARIA_ROM.parent / "live/capture/capture_report.json"),
    ):
        setup, report = map(base.load, (setup_path, report_path))
        assert report["ROM_sha256"] == setup["fixture_sha256"] == base.digest(setup["fixture"])
        assert setup["candidate_sha256"] == base.digest(stage.ROM) and setup["whole_source_ROM_inverse"]
        assert report["cold_boot"] and not report["savestate_loaded"] and not report["callback_errors"]
        if label == "lil":
            assert report["scripted_input_schedule"] == base.load(setup["inputs"]) and not report.get("battery_save_preloaded")
        else:
            assert verified_existing_unlock(report)
        fixture = base.NdsImage.open(setup["fixture"])
        assert all(fixture.read_file(asset) == image.read_file(asset)
                   for asset in (native.ARM, "/GRP/KANJI.FNT", "/COMMON/MESFILE.DK4"))
        photos = tool.photos(report)
        masks = [(n, tool.body_masks(picture)) for n, (_, picture) in sorted(photos.items())]
        panels, cursor = [], 3650 if label == "lil" else 4100
        for row in setup["selected"]:
            raw = bytes.fromhex(row["stored_command_hex"])
            body = raw[6:raw.index(0, 6)].replace(b"FO", b"Argot Co.").replace(b"FI", b"Lil").replace(b"FA", b"Argot")
            if raw[5] == 254:
                physical = fe_paint(body)["physical"]
                planes = [bytes(int(bool(v)) for y in range(64) for v in physical[y * 228:y * 228 + 216])]
            else:
                planes = [bytes.fromhex(p["native_plane_hex"]) for p in paint(arm, font, body)["pages"]]
            for p, plane in enumerate(planes, 1):
                wanted = tool.prior.masks(plane)
                frame = next((n for n, bits in masks if n > cursor and bits == wanted), None)
                assert frame is not None, (label, row["id"], cursor, body)
                panels.append(dict(id=row["id"], page=p, frame=frame, capture=photos[frame][0],
                                   body_hex=body.hex(), route=setup["route"]))
                cursor = frame
        for start in range(0, len(panels), 8):
            part = panels[start:start + 8]
            sheet = Image.new("RGB", (1024, 404 * ((len(part) + 1) // 2)), "#263238")
            draw = ImageDraw.Draw(sheet)
            for i, hold in enumerate(part):
                x, y = i % 2 * 512, i // 2 * 404
                draw.text((x + 4, y + 2), f"{hold['id']} at {hold['frame']}", fill="white")
                bottom = photos[hold["frame"]][1].crop((0, 192, 256, 384))
                sheet.paste(bottom.resize((512, 384), Image.Resampling.NEAREST), (x, y + 16))
            path = ROOT / f"{label}_live_{start // 8 + 1}.png"
            sheet.save(path)
            sheets.append(dict(path=str(path), sha256=base.digest(path)))
        observed.extend(panels)
        evidence.update({str(path):base.digest(path) for path in (report_path, setup_path, setup["fixture"])})

    assert len(observed) == 19
    assert any(b"Argot Co." in bytes.fromhex(row["body_hex"]) for row in observed)
    assert any(b"77,000" in bytes.fromhex(row["body_hex"]) for row in observed)
    base.save(LIVE, dict(candidate_sha256=base.digest(stage.ROM), initialized_Lil_and_Maria=True,
        exact_original_commands=True, actual_substitution_and_FE_receipt=True, natural_activation=False,
        inventory_and_payment_accounting=False, hardware=False, holds=observed, sheets=sheets, evidence=evidence))
    print(f"Matched {len(observed)} initialized Lil and Maria dialogue holds.", flush=True)


if __name__ == "__main__":
    cli = ArgumentParser(description=__doc__)
    cli.add_argument("action", choices=("prepare", "capture_lil", "capture_maria", "verify"))
    globals()[cli.parse_args().action]()
