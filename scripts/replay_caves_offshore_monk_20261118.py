"""Exercise both Rafael fog menus and Verisa's exchange on Maria's route."""

from argparse import ArgumentParser
from struct import pack_into
from types import FunctionType

from scripts import replay_rafael_mosque_20261118 as rafael
from scripts import replay_sakura_expeditions_macao_20261118 as maria
from scripts import stage_caves_offshore_monk_20261118 as stage
from scripts.source_locked_derivation_v5118 import checked_text

base, native = stage.base, stage.native
ROOT = stage.ROOT / "fog"
ROM, SETUP = ROOT / "Rafael_Fog_RESEARCH_ONLY.nds", ROOT / "fixture.json"
LAST = 6901
FIRST = 1598


def prepare_fog():
    image = base.NdsImage.open(stage.ROM)
    path = "/data/SC0.DK4"
    archive = image.read_file(path)
    bank = native.IlnkContainer.parse(archive)
    proof = base.load(stage.PROOF)
    assert base.digest(stage.ROM) == proof["candidate_sha256"]
    group = next(g for g in proof["groups"] if g["file_path"] == path and g["block"] == 332)
    host, block = bank.blocks[44], bank.blocks[332]
    assert native.digest(block) == group["after"]
    commands = group["commands"]
    first = next(i for i, c in enumerate(commands) if c["source_offset"] == FIRST)
    guest = commands[first:]
    assert len(guest) == 30 and guest[-1]["stored"] == guest[-1]["source"] == "00000080"
    assert all(first <= c.get("target_command_index", first) < len(commands) for c in guest)
    start = guest[0]["stored_offset"]
    fixture = bytearray(host[:40] + block[start:stage.logical_end(block)])
    pack_into("<H", fixture, 4, len(fixture) - 8)
    fixture += bytes(-len(fixture) % 4)
    inventory, _, _ = native.scoped_inventory()
    actual, _ = inventory(image.read_file(native.ARM), fixture)
    assert len(actual) == 10 + len(guest)
    for cmd, expected in zip(actual[10:], guest, strict=True):
        offset = expected["stored_offset"] - start + 40
        raw = bytes.fromhex(expected["stored"])
        assert cmd["offset"] == offset and cmd["word"] == expected["word"]
        assert fixture[offset:offset + len(raw)] == raw
    ROOT.mkdir()
    bank.blocks[44] = bytes(fixture)
    image.replace_file(path, bank.to_bytes())
    image.save(ROM)
    image.replace_file(path, archive)
    assert bytes(image.rom.save()) == stage.ROM.read_bytes()
    previous = rafael.scope["precedent"].stage.CAPTURE
    schedule = base.load(previous)["scripted_input_schedule"] + [
        dict(start=n, duration=5, buttons=["A"]) for n in range(3800, LAST, 350)]
    inputs = ROOT / "inputs.json"
    base.save(inputs, schedule)
    base.save(SETUP, dict(candidate_sha256=proof["candidate_sha256"], fixture_sha256=base.digest(ROM),
        inputs=str(inputs), inputs_sha256=base.digest(inputs), original_fog_commands_exact=True,
        included_source_offsets=[c["source_offset"] for c in guest], whole_ROM_inverse=True,
        initialized_Rafael=True, natural_activation=False))


rafael_scope = rafael.scope | globals()
fog = FunctionType(rafael.capture.__code__, rafael_scope)
startup = FunctionType(rafael.startup.__code__, rafael_scope)

MARIA_ROOT = stage.ROOT / "verisa"
MARIA_ROM = MARIA_ROOT / "Maria_Verisa_RESEARCH_ONLY.nds"
MARIA_FIXTURE = MARIA_ROOT / "fixture.json"
maria_scope = maria.maria_scope | {
    "ROOT": MARIA_ROOT, "ROM": MARIA_ROM, "FIXTURE": MARIA_FIXTURE,
    "stage": stage, "FOREST": 286, "FIRST": 8,
}
verisa = checked_text(maria.maria_prep, {
    "The complete original Macao inquiry, played in the initialized Maria opening.":
        "Verisa's complete original incense burner exchange in the initialized Maria opening.",
})
exec(compile(verisa, __file__ + "::original-Verisa-entry", "exec"), maria_scope)
capture_maria = FunctionType(maria.maria_capture.__code__, maria_scope)

REPLY_ROOT = stage.ROOT / "reply"
REPLY_ROM = REPLY_ROOT / "Maria_Verisa_Reply_RESEARCH_ONLY.nds"
REPLY_FIXTURE = REPLY_ROOT / "fixture.json"
reply_scope = maria_scope | {"ROOT": REPLY_ROOT, "ROM": REPLY_ROM, "FIXTURE": REPLY_FIXTURE, "FIRST": 224}
exec(compile(verisa, __file__ + "::original-Verisa-reply-entry", "exec"), reply_scope)
capture_reply = FunctionType(maria.maria_capture.__code__, reply_scope)

if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("prepare_fog", "prepare_verisa", "prepare_reply", "fog", "verisa", "reply", "startup"))
    action = parser.parse_args().action
    if action == "prepare_verisa":
        maria_scope["prepare"]()
    elif action == "prepare_reply":
        reply_scope["prepare"]()
    elif action == "verisa":
        capture_maria("live", [(n, "A") for n in range(4200, 7701, 350)], 7901)
    elif action == "reply":
        capture_reply("live", [(n, "A") for n in range(4200, 6001, 350)], 6301)
    else:
        globals()[action]()
