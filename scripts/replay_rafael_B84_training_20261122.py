"""Cold-boot the B84 excerpts and both original choice paths with controller input."""

from argparse import ArgumentParser
from struct import pack_into
import sys

from scripts import replay_north_sea_and_hodram_reconciliation_20261122 as prior
from scripts import stage_rafael_B84_training_20261122 as stage


base, native = stage.base, stage.native
ROOT = stage.ROOT / "focused_gameplay"
SPEECH = ("R0064", "R0089", "R0285", "R0314", "R0336", "R0358", "R0417", "R0439")
FE = ("R0470", "R0539")
BOOT = prior.rafael_scope["prior"].prior
HARNESS = BOOT.release_checks.template.games.harness
MENU_RUNS = {
    "defeat": ("R0215", ((4000, "A"), (4340, "A"), (5050, "A")), (3900, 4250, 4650, 4900, 5410)),
    "alternative": ("R0215", ((4000, "A"), (4340, "A"), (4780, "DOWN"), (5050, "A")), (3900, 4250, 4650, 4900, 5410)),
    "lesson_only": ("R0417", ((4000, "A"), (4380, "DOWN"), (4700, "A")), (3900, 4260, 4540, 5050)),
}


def commands_for():
    stored = base.load(stage.PROOF)
    assert stored["candidate_sha256"] == base.digest(stage.ROM) and stored["whole_parent_inverse"]
    group, = stored["groups"]
    return stored, group["commands"]


def is_id(command, ident):
    return any(tag.endswith(ident) for tag in command["record_ids"])


def run_root(name):
    root = ROOT/name
    if name in ("alternative","lesson_only"):
        return root/"controller_retry"
    return root


def fixture(kind):
    stored, objects = commands_for()
    root = ROOT / kind
    config = root / "fixture.json"
    if config.exists():
        saved = base.load(config)
        assert saved["candidate_sha256"] == stored["candidate_sha256"] and saved["exact_inverse"]
        assert base.digest(saved["path"]) == saved["rom_sha256"]
        return
    rom = base.NdsImage.open(stage.ROM)
    archive = rom.read_file(stage.PATH)
    bank = native.IlnkContainer.parse(archive)
    scene, host = bank.blocks[84], bank.blocks[44]
    prelude = bytes.fromhex(base.load(prior.rafael_scope["OLD_FIXTURE"])["original_prelude"])
    assert host[8:40] == prelude and len(prelude) == 32
    assert host[:4] == scene[:4] and host[6:8] == scene[6:8]
    logical = bytearray(host[:40])
    menu = kind != "speech"
    if menu:
        start = "R0417" if kind == "lesson_entry" else "R0215"
        first = next(i for i,c in enumerate(objects) if is_id(c,start))
        sequence = objects[first:]
        for c in sequence:
            if "target_command_index" in c:
                assert c["target_command_index"] >= first
    else:
        sequence = [next(c for c in objects if is_id(c,k)) for k in SPEECH]
        for k in FE:
            sequence.extend(c for c in objects if is_id(c,k) or (c.get("retained_continuation_of") or "").endswith(k))
        assert len(sequence)==12
        sequence.append(objects[-1])
    receipt = []
    for c in sequence:
        at, raw = c["stored_offset"],bytes.fromhex(c["stored"])
        assert scene[at:at+len(raw)] == raw
        receipt.append(c | dict(fixture_offset=len(logical)))
        logical.extend(raw)
    pack_into("<H",logical,4,len(logical)-8)
    body = bytes(logical) + bytes(-len(logical)%4)
    inventory, _, _ = native.scoped_inventory()
    commands, _ = inventory(rom.read_file(native.ARM),body)
    by_offset = {c["offset"]:c for c in commands}
    for c in receipt:
        check = by_offset[c["fixture_offset"]]
        if c["word"] == 0x0100 and menu:
            at = c["stored_offset"]
            expected = scene[at:at + check["native_extent"]].hex()
        else:
            expected = c["stored"]
        assert expected == check["whole_command_hex"] and c["word"] == check["word"], (
            kind,c["stored_offset"],c["fixture_offset"],hex(c["word"]))
        if menu and "target_command_index" in c:
            old = objects[c["target_command_index"]]["stored_offset"]
            raw = bytes.fromhex(c["stored"])
            assert stage.forest.jump(raw,c["fixture_offset"]) == old + c["fixture_offset"] - c["stored_offset"]
    root.mkdir(parents=True)
    bank.blocks[44] = body
    rom.replace_file(stage.PATH,bank.to_bytes())
    path = root / f"B84_{kind}_FOCUSED_ONLY.nds"
    rom.save(path)
    inverse = base.NdsImage.open(path)
    inverse.replace_file(stage.PATH,archive)
    assert bytes(inverse.rom.save()) == stage.ROM.read_bytes()
    base.save(root/"fixture.json",dict(candidate_sha256=stored["candidate_sha256"],path=str(path),
         rom_sha256=base.digest(path),exact_inverse=True,original_B44_initializers=prelude.hex(),
         contiguous_B84_suffix_with_original_branches=menu,original_commands=receipt,natural_activation=False))


def play(name):
    if name == "speech":
        kind = "speech"
        actions = tuple((4000 + 370*i,"A") for i in range(12))
        captures = (3900, *(f+300 for f,_ in actions))
    else:
        selected,actions,captures = MENU_RUNS[name]
        kind = "lesson_entry" if selected=="R0417" else "pact_entry"
    config = base.load(ROOT/kind/"fixture.json")
    assert config["candidate_sha256"]==base.digest(stage.ROM)
    root=run_root(name)
    root.mkdir(exist_ok=True,parents=True)
    path=config["path"]
    assert base.digest(path)==config["rom_sha256"]
    inputs=root/"inputs.json"
    base.save(inputs,base.load(BOOT.INPUTS)+[dict(start=f,duration=5,buttons=[button]) for f,button in actions])
    sys.argv=[HARNESS.__file__,"--rom",path,"--out",str(root/"capture"),"--frames",str(max(captures)+120),
        "--inputs-json",str(inputs),"--press-start","-1","--capture-every","999999","--capture-at",*map(str,captures)]
    HARNESS.main()


if __name__=="__main__":
    cli=ArgumentParser(description=__doc__)
    cli.add_argument("action",choices=("fixtures","speech",*MENU_RUNS))
    action=cli.parse_args().action
    if action=="fixtures":
        for kind in ("speech","pact_entry","lesson_entry"):
            fixture(kind)
    else:
        play(action)
