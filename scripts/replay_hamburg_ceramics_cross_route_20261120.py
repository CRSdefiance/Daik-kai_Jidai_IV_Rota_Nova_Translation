"""Replay the complete Lil ceramics scene and the cumulative startup."""

from argparse import ArgumentParser
from pathlib import Path
from struct import pack_into, unpack_from
from types import FunctionType

from dk4tool.patch.xdelta import apply_xdelta, make_xdelta
from scripts import replay_damaged_save_digits_20261120 as boot
from scripts import replay_lil_ceramics_wrap_20261111 as prior
from scripts import stage_hamburg_ceramics_cross_route_20261120 as build


base, native = build.base, build.native
ROOT = build.ROOT / "emulator"
SETUP = ROOT / "fixture_receipt.json"


def prepare():
    assert not ROOT.exists()
    stage, release = map(base.load, (build.PROOF, build.parent.RELEASE))
    assert base.digest(build.parent.ROM) == release["candidate_sha256"] == stage["predecessor_sha256"]
    assert base.digest(build.ROM) == stage["candidate_sha256"]
    assert base.digest(prior.INPUTS) == "097df0c69d30d00532373b2b8b7fe2f5969ba581a0bd35e27074c22749631541"
    original = next(row for row in base.load(prior.HISTORICAL)["versions"] if row["case"] == "static_target")
    source_path = Path("work/analysis/square_shopkeeper_scenes_v7022/four_complete_static_staged_nameplate_fixtures.json")
    reference = next(row for row in base.load(source_path)["fixtures"] if row["case"] == "static_target")
    frames = [r["complete_page_holds"][0][-1]["frame"] for r in original["panels"]]
    assert len(frames) == 17 and frames[-1] == 6910
    inventory, _, _ = native.scoped_inventory()
    ROOT.mkdir()
    variants = {}
    for side, rom in (("before", build.parent.ROM), ("after", build.ROM)):
        image = base.NdsImage.open(rom)
        bank = native.IlnkContainer.parse(image.read_file(prior.stage.FILE))
        entry, scene = bank.blocks[22], bank.blocks[189]
        prelude = entry[8:56]
        assert prelude.hex() == reference["original_B22_prelude_hex"]
        end = 8 + unpack_from("<H", scene, 4)[0]
        logical = bytearray(entry[:8] + prelude + scene[8:end])
        pack_into("<H", logical, 4, len(logical) - 8)
        fixture = bytes(logical) + bytes(-len(logical) % 4)
        arm = image.read_file(native.ARM)
        original_commands, _ = inventory(arm, scene)
        inserted_commands, _ = inventory(arm, fixture)
        assert len(original_commands) == 20 and len(inserted_commands) == 29
        for src, inserted in zip(original_commands, inserted_commands[9:], strict=True):
            assert src["whole_command_hex"] == inserted["whole_command_hex"]
            assert src["offset"] + len(prelude) == inserted["offset"]
        bank.blocks[22] = fixture
        image.replace_file(prior.stage.FILE, bank.to_bytes())
        fixture_rom = ROOT / f"{side}_Lil_entry_RESEARCH_ONLY.nds"
        image.save(fixture_rom)
        bank.blocks[22] = entry
        image.replace_file(prior.stage.FILE, bank.to_bytes())
        assert bytes(image.rom.save()) == rom.read_bytes()
        variants[side] = dict(path=str(fixture_rom), sha256=base.digest(fixture_rom),
                              fixture_sha256=native.digest(fixture), underlying_ROM_sha256=base.digest(rom))
    schedule = base.load(prior.INPUTS) + [dict(start=f, duration=5, buttons=["A"]) for f in range(2600, 7600, 240)]
    base.save(ROOT / "inputs.json", schedule)
    base.save(SETUP, dict(candidate_sha256=stage["candidate_sha256"], parent_sha256=stage["predecessor_sha256"],
        fixture_ROMs=variants, representative_frames=frames, end=7600,
        fixture_is_original_prelude_followed_by_complete_original_scene=True,
        natural_Hamburg_activation=False, source_scene_scope=str(prior.HISTORICAL)))
    delta, rebuilt = build.ROOT / "translation.xdelta", build.ROOT / "clean_rebuilt.nds"
    make_xdelta(native.CLEAN, build.ROM, delta)
    apply_xdelta(native.CLEAN, delta, rebuilt)
    assert rebuilt.read_bytes() == build.ROM.read_bytes()


def startup():
    history = base.load(build.parent.STARTUP_CAPTURE)
    donor = history["battery_save_preloaded"]
    assert base.digest(donor["source"]) == donor["source_sha256"]
    assert base.digest(build.ROM) == base.load(build.PROOF)["candidate_sha256"]
    folder = FunctionType(boot.replay.__code__, boot.replay.__globals__ | {"stage": build})
    folder(build.ROM, history, donor["source"], "startup")


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("case", choices=("prepare", "before", "after", "startup"))
    case = parser.parse_args().case
    if case in ("before", "after"):
        FunctionType(prior.capture.__code__, prior.capture.__globals__ | {"ROOT": ROOT, "SETUP": SETUP})(case)
    else:
        globals()[case]()
