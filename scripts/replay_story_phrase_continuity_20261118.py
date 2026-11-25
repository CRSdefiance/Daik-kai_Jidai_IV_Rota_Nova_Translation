"""Observe the repaginated tutorial and Verisa's live given-name greeting."""

from argparse import ArgumentParser
from struct import pack_into
import sys
from types import FunctionType

from scripts import headless_desmume_v193 as harness
from scripts import replay_hodram_final_wraps_20261114 as hodram_input
from scripts import replay_london_guild_assignments_20261118 as baseline
from scripts import replay_story_tag_wraps_20261118 as earlier
from scripts import stage_story_phrase_continuity_20261118 as stage

base, native = stage.base, stage.native
ROOT = stage.ROOT / "initialized_replays"
LIVE = ROOT / "replay.json"
R_ROOT, H_ROOT = ROOT / "rafael", ROOT / "hodram"
ROM = R_ROOT / "Rafael_Phrase_Excerpts_RESEARCH_ONLY.nds"
HODRAM_ROM = H_ROOT / "Hodram_Phrase_Excerpts_RESEARCH_ONLY.nds"
SETUP, HODRAM_SETUP = R_ROOT / "rafael_fixture.json", H_ROOT / "hodram_fixture.json"
RAFAEL = ((143, (375, 380, 383)), (152, (128, 131, 136)), (249, (23, 27, 31)))
HODRAM = ((251, (5, 9, 15)), (314, (6, 10, 14)))


def prepare(name):
    route, host_number, prefix_length, expected_prefix_count, suffix, snippets, rom, receipt = (
        (0, 44, 40, 10, bytes(4), RAFAEL, ROM, SETUP) if name == "rafael" else
        (1, 42, 42, 8, bytes.fromhex("00c200000000"), HODRAM, HODRAM_ROM, HODRAM_SETUP)
    )
    parent = base.load(stage.PROOF)
    assert parent["candidate_sha256"] == base.digest(stage.ROM)
    source = base.load(stage.review.SOURCE)
    source_groups = {g["block"]: g for g in source["groups"] if g["route"] == route}
    stored_groups = {g["block"]: g for g in parent["groups"] if g["route"] == route}
    image = base.NdsImage.open(stage.ROM)
    path = f"/data/SC{route}.DK4"
    old_file = image.read_file(path)
    bank = native.IlnkContainer.parse(old_file)
    host = bank.blocks[host_number]
    arm = image.read_file(native.ARM)
    inventory, _, _ = native.scoped_inventory()
    host_commands, host_speeches = inventory(arm, host)
    initial = [c["word"] for c in host_commands if c["offset"] < prefix_length]
    assert len(initial) == expected_prefix_count and host_speeches[0]["offset"] == prefix_length
    if route == 1:
        end = stage.logical_end(host)
        assert host[end - len(suffix):end] == suffix
    selected, bodies = [], []
    for n, ids in snippets:
        data = bank.blocks[n]
        group = stored_groups[n]
        assert group["after"] == native.digest(data)
        rows = {row["source_record_index"]: row for row in source_groups[n]["records"]}
        commands = {cmd["source_offset"]: cmd for cmd in group["commands"]}
        for index in ids:
            key = rows[index]["source_command_offset"]
            cmd = commands[key]
            assert cmd["word"] == 0x4000
            raw, off = bytes.fromhex(cmd["stored"]), cmd["stored_offset"]
            assert data[off:off + len(raw)] == raw
            bodies.append(raw)
            selected.append(dict(block=n, source_record_index=index, id=f"DK4_MES_B{n}_R{index:04}",
                                 stored_offset=off, stored_command_hex=raw.hex()))
    replacement = bytearray(host[:prefix_length] + b"".join(bodies) + suffix)
    pack_into("<H", replacement, 4, len(replacement) - 8)
    replacement.extend(bytes(-len(replacement) % 4))
    checked, speeches = inventory(arm, replacement)
    assert [c["word"] for c in checked[:expected_prefix_count]] == initial
    assert [row["whole_command_hex"] for row in speeches] == [body.hex() for body in bodies]
    rom.parent.mkdir(parents=True)
    bank.blocks[host_number] = bytes(replacement)
    image.replace_file(path, bank.to_bytes())
    image.save(rom)
    bank.blocks[host_number] = host
    assert bank.to_bytes() == old_file
    image.replace_file(path, old_file)
    assert bytes(image.rom.save()) == stage.ROM.read_bytes()
    if route == 0:
        inputs = base.load(baseline.precedent.stage.CAPTURE)["scripted_input_schedule"]
    else:
        inputs = [a for a in base.load(hodram_input.INPUTS) if a["start"] <= 2200]
    inputs += [dict(start=n, duration=5, buttons=["A"]) for n in range(3800, 6526 if route == 0 else 5801, 275)]
    input_path = rom.parent / "inputs.json"
    base.save(input_path, inputs)
    base.save(receipt, dict(candidate_sha256=parent["candidate_sha256"], fixture=str(rom),
        fixture_sha256=base.digest(rom), original_excerpt_commands_preserved=True, exact_ROM_inverse=True,
        initialized_route=route, natural_activation=False, selected=selected,
        original_prefix_sha256=native.digest(host[:prefix_length]), inputs=str(input_path), inputs_sha256=base.digest(input_path)))


def capture(name):
    folder, rom, setup, frames = (R_ROOT, ROM, SETUP, 6701) if name == "rafael" else (H_ROOT, HODRAM_ROM, HODRAM_SETUP, 6001)
    receipt = base.load(setup)
    assert base.digest(rom) == receipt["fixture_sha256"] and base.digest(receipt["inputs"]) == receipt["inputs_sha256"]
    sys.argv = [sys.argv[0], "--rom", str(rom), "--out", str(folder / "capture"), "--frames", str(frames),
                "--inputs-json", receipt["inputs"], "--capture-every", "999999",
                "--capture-at", *map(str, range(3650, frames, 25))]
    harness.main()


def verify():
    assert not LIVE.exists()
    verifier = FunctionType(earlier.verify_one.__code__, vars(earlier) | {"stage": stage})

    rafael_receipt = R_ROOT / "verified.json"
    if rafael_receipt.is_file():
        r = base.load(rafael_receipt) | {"receipt": str(rafael_receipt)}
        assert r["fixture_sha256"] == base.digest(ROM) == base.load(SETUP)["fixture_sha256"]
        assert r["exact_native_panel_masks"] and len(r["holds"]) == 10
        assert all(base.digest(path) == sha for path, sha in r["evidence"].items())
        assert all(base.digest(row["capture"]["path"]) == row["capture"]["PNG_sha256"] for row in r["holds"])
    else:
        r = verifier(R_ROOT, ROM, SETUP, "Rafael", "Castor", 10)
    h = verifier(H_ROOT, HODRAM_ROM, HODRAM_SETUP, "Hodram", "Bergstrom", 6)
    assert all(x["candidate_sha256"] == base.digest(stage.ROM) for x in (r, h))
    assert any(b"Hodram, have you heard" in bytes.fromhex(row["body_hex"]) for row in h["holds"])
    tutorial = next(row for row in r["holds"] if row["id"] == "DK4_MES_B143_R0380")
    followup = next(row for row in r["holds"] if row["id"] == "DK4_MES_B143_R0383")
    assert tutorial["page"] == 1 and followup["page"] == 1 and followup["frame"] > tutorial["frame"]
    evidence = r["evidence"] | h["evidence"]
    evidence.update({str(p): base.digest(p) for p in (r["receipt"], h["receipt"], ROM, HODRAM_ROM)})
    base.save(LIVE, dict(candidate_sha256=r["candidate_sha256"], initialized_Rafael_and_Hodram=True,
        actual_given_name_and_pagination=True, exact_original_commands=True, natural_activation=False, hardware=False,
        holds=r["holds"] + h["holds"], sheets=r["sheets"] + h["sheets"], evidence=evidence))


if __name__ == "__main__":
    cli = ArgumentParser(description=__doc__)
    cli.add_argument("action", choices=("prepare", "capture", "verify"))
    cli.add_argument("route", nargs="?", choices=("rafael", "hodram"))
    args = cli.parse_args()
    if args.action == "verify":
        verify()
    else:
        assert args.route
        globals()[args.action](args.route)
