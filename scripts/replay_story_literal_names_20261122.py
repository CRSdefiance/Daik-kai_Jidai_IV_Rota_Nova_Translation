"""Replay the same ordinary Hodram opening controls on the previous and fixed builds."""

from argparse import ArgumentParser
from struct import pack_into, unpack_from
import sys

from scripts import observe_hodram_custom_names_20261122 as original
from scripts import replay_hodram_early_confrontations_20261119 as host
from scripts import stage_story_literal_names_20261122 as stage


FRAMES = (14520, 23970, 24320, 24670, 25020, 25370)
END = FRAMES[-1] + 1
base = stage.base
ARCHIVE = "/data/SC1.DK4"
SYSTEM_BLOCK, CLEAN_AT, INSTALLED_AT = 205, 1052, 1064
FOCUSED_ROM = stage.ROOT / "system" / "Hodram_Literal_Name_System_FOCUSED_ONLY.nds"


def system_fixture(root):
    clean, image = map(base.NdsImage.open, (stage.native.CLEAN, stage.ROM))
    contract = base.load(host.HISTORICAL)
    raw_archive = image.read_file(ARCHIVE)
    original_archive = stage.native.IlnkContainer.parse(clean.read_file(ARCHIVE))
    bank = stage.native.IlnkContainer.parse(raw_archive)
    opening = bank.blocks[host.ENTRY]
    prelude = b"".join(bytes.fromhex(row["whole_command_hex"]) for row in contract["original_initializers"])
    leave = bytes.fromhex(contract["source_bound_QA_host_exit_hex"])
    end = 8 + unpack_from("<H", opening, 4)[0]
    assert opening[8:8+len(prelude)] == prelude and opening[end-len(leave):end] == leave
    installed = bank.blocks[SYSTEM_BLOCK]
    source = original_archive.blocks[SYSTEM_BLOCK]
    header, prose = bytes.fromhex("0040ffff00fe"), b"FI: Charm +1!"
    literal = header + prose + b"\0"
    # The clean scout indexes the selector byte. The installed inventory indexes the whole command.
    assert installed[INSTALLED_AT:INSTALLED_AT+len(literal)] == literal
    src_start = source.rfind(header, CLEAN_AT-8, CLEAN_AT+8)
    assert src_start >= 0
    jp = source[src_start+len(header):].split(b"\0",1)[0]
    assert b"FI" in jp and "魅力".encode("cp932") in jp
    layout = bytearray(opening[:8] + prelude + literal + leave)
    pack_into("<H",layout,4,len(layout)-8)
    payload = bytes(layout) + bytes(-len(layout) % 4)
    assert len(payload) < contract["source_bound_QA_block_limit"]
    inventory, _, _ = stage.native.scoped_inventory()
    rows, _ = inventory(image.read_file(stage.native.ARM), payload)
    assert {r["offset"]:r["whole_command_hex"] for r in rows}[8+len(prelude)] == literal.hex()
    bank.blocks[host.ENTRY] = payload
    image.replace_file(ARCHIVE,bank.to_bytes())
    image.save(FOCUSED_ROM)
    inverse = base.NdsImage.open(FOCUSED_ROM)
    inverse.replace_file(ARCHIVE,raw_archive)
    assert bytes(inverse.rom.save()) == stage.ROM.read_bytes()
    base.save(root/"fixture.json", dict(candidate_sha256=base.digest(stage.ROM),
        fixture_sha256=base.digest(FOCUSED_ROM), exact_candidate_inverse=True,
        natural_activation=False, entry_initializers=prelude.hex(), exit=leave.hex(),
        file_path=ARCHIVE, block=SYSTEM_BLOCK, clean_command_offset=src_start,
        current_command_offset=INSTALLED_AT, clean_japanese=jp.decode("cp932"), clean_body_hex=jp.hex(),
        clean_block_sha256=stage.native.digest(source), installed_block_sha256=stage.native.digest(installed),
        installed_command_hex=literal.hex()))
    return FOCUSED_ROM


def run(which):
    proof, controls = map(base.load, (stage.PROOF, stage.parent.stage.BASELINE))
    root = stage.ROOT / which
    root.mkdir()
    if which == "system":
        rom = system_fixture(root)
        expected = base.load(root/"fixture.json")["fixture_sha256"]
        captures = (14520,14870,15220,15570)
    else:
        rom, expected = {
        "previous": (stage.parent.ROM, proof["predecessor_sha256"]),
        "fixed": (stage.ROM, proof["candidate_sha256"]),
        }[which]
        captures = FRAMES
    end = captures[-1]+1
    assert base.digest(rom) == expected
    assert controls["cold_boot"] and not controls["savestate_loaded"]
    assert not controls.get("battery_save_preloaded") and not controls["callback_errors"]
    assert not any(v for k,v in controls.items() if k.startswith("synthetic_"))
    inputs = root / "inputs.json"
    base.save(inputs, [e for e in controls["scripted_input_schedule"] if e["start"] < end])
    argv = sys.argv
    try:
        sys.argv = [original.harness.__file__, "--rom", str(rom), "--out", str(root / "capture"),
                    "--frames", str(end), "--inputs-json", str(inputs), "--press-start", "-1", "--touchscreen",
                    "--capture-every", "999999", "--dump-capture-ram", "--capture-at", *map(str, captures)]
        original.harness.main()
    finally:
        sys.argv = argv


if __name__ == "__main__":
    cli = ArgumentParser(description=__doc__)
    cli.add_argument("build", choices=("previous", "fixed", "system"))
    run(cli.parse_args().build)
