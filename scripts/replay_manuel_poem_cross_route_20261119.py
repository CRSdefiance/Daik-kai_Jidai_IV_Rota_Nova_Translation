"""Play the whole Lil aftermath scene with its original conditions and input path."""

from argparse import ArgumentParser
from inspect import getsource
from pathlib import Path
from struct import pack_into
import sys
from types import FunctionType

from scripts import observe_remaining_opening_shared_text_20261119 as opening
from scripts import replay_ceuta_lesson_20261119 as startup_template
from scripts import run_Rafael_B45_scenes_v7893 as runner
from scripts import stage_manuel_poem_cross_route_20261119 as build
from scripts.source_locked_derivation_v5118 import checked_text

base, native = build.base, build.native
ROOT = build.ROOT / "lil_aftermath"
FIXTURE, FIXTURES = ROOT / "Lil_Aftermath_RESEARCH_ONLY.nds", ROOT / "fixtures.json"
STARTUP = build.ROOT / "startup_fixture"
FILE, ROUTE, OPENING, AFTERMATH = "/data/SC2.DK4", 2, 22, 11
FRAMES = 11201


def prepare():
    assert not ROOT.exists()
    stage = base.load(build.PROOF)
    assert base.digest(build.ROM) == stage["candidate_sha256"]
    image = base.NdsImage.open(build.ROM)
    arm, archive = (image.read_file(p) for p in (native.ARM, FILE))
    bank = native.IlnkContainer.parse(archive)
    host, guest = (bank.blocks[n] for n in (OPENING, AFTERMATH))
    assert host[:4] == guest[:4] and host[6:8] == guest[6:8]
    inventory, _, _ = native.scoped_inventory()
    host_commands, host_speeches = inventory(arm, host)
    first = host_speeches[0]["offset"]
    last = host_speeches[-1]["offset"] + host_speeches[-1]["native_extent"]
    prefix = [r for r in host_commands if r["offset"] < first]
    tail = [r for r in host_commands if r["offset"] >= last]
    assert first == 56 and len(prefix) == 9 and tail[-1]["whole_command_hex"] == "00000000"
    guest_commands, guest_speeches = inventory(arm, guest)
    assert len(guest_commands) == 29 and len(guest_speeches) == 15
    assert guest_commands[-1]["whole_command_hex"] == tail[-1]["whole_command_hex"]
    assert sum(r["word"] == 0x8000 for r in guest_commands) == 2
    group, = (g for g in stage["groups"] if g["route"] == ROUTE and g["block"] == AFTERMATH)
    assert native.digest(guest) == group["after"]
    logical = bytearray(host[:first] + guest[8:build.logical_end(guest) - 4] + host[last:build.logical_end(host)])
    pack_into("<H", logical, 4, len(logical) - 8)
    fixture = bytes(logical) + bytes(-len(logical) % 4)
    commands, speeches = inventory(arm, fixture)
    assert len(speeches) == 15 and [r["whole_command_hex"] for r in commands] == [
        r["whole_command_hex"] for r in prefix + guest_commands[:-1] + tail]
    delta = first - 8
    ids = []
    for command in group["commands"]:
        if command["word"] != 0x4000:
            continue
        ident, = command["record_ids"]
        at = command["stored_offset"] + delta
        raw = bytes.fromhex(command["stored"])
        assert fixture[at:at + len(raw)] == raw
        ids.append(dict(id=ident, source_selector=raw[5], fixture_command_offset=at, native_command_hex=raw.hex()))
    assert len(ids) == 15
    ROOT.mkdir()
    bank.blocks[OPENING] = fixture
    image.replace_file(FILE, bank.to_bytes())
    image.save(FIXTURE)
    restored = base.NdsImage.open(FIXTURE)
    restored.replace_file(FILE, archive)
    assert bytes(restored.rom.save()) == build.ROM.read_bytes()
    base.save(FIXTURES, dict(candidate_sha256=stage["candidate_sha256"], exact_candidate_inverse=True,
        fixtures=[dict(route=ROUTE, version="English", source_file=FILE, source_block=AFTERMATH,
                       fixture_block=OPENING, research_ROM=str(FIXTURE), research_ROM_sha256=base.digest(FIXTURE),
                       original_opening_prelude_commands=prefix, original_text_records=ids, all_fixture_commands=commands,
                       original_both_branch_commands_present=True, initialized_fixture=True, natural_activation=False)]))
    print("Prepared the full Lil aftermath scene with both original conditions and the original New Game return.")


def capture():
    inputs, _, _, source_inputs, donor = opening.schedule("lil")
    assert not donor and sum(r["buttons"] == ["RIGHT"] for r in inputs) == 2
    data = checked_text(Path(runner.__file__).read_text(encoding="utf-8"), {
        "ROOT=Path('work/analysis/Rafael_B45_scene_runs_v7893')": "ROOT=ACTIVE_ROOT",
        "FIXTURES=Path('work/analysis/Rafael_B45_scene_fixtures_v7892/two_complete_source_English_original_Rafael_prelude_fixtures.json')":
            "FIXTURES=ACTIVE_FIXTURES",
        "choices=[0],required=True": "choices=[2],required=True",
        "cap=Path('E:/Rota Nova translations/Generated/work/emulation_v193')/f'Rafael_B45_route{route}_{version}_v7893'":
            "cap=folder/'capture'",
        "source_inputs=Path(f'work/analysis/papal_trade_route_runs_v7625/route{route}/ordinary_NewGame_inputs.json')":
            "source_inputs=SOURCE_INPUTS",
        "range(4000,15501,240)": "range(4000,FRAME_LIMIT-1,240)",
        "range(2350,16001,60))|{16000}": "range(2350,FRAME_LIMIT,45))|{FRAME_LIMIT-1}",
        "original_exchange_commands=24,original_exchange_speeches=12":
            "original_exchange_commands=29,original_exchange_speeches=15",
        "'16001'": "str(FRAME_LIMIT)",
        "16001": "FRAME_LIMIT",
    })
    scope = dict(__name__="__main__", __file__=__file__, ACTIVE_ROOT=ROOT, ACTIVE_FIXTURES=FIXTURES,
                 FRAME_LIMIT=FRAMES, SOURCE_INPUTS=source_inputs)
    previous = sys.argv
    try:
        sys.argv = [__file__, "--route", "2", "--version", "English"]
        exec(compile(data, __file__ + "::lil-aftermath-replay", "exec"), scope)
    finally:
        sys.argv = previous


def startup():
    FunctionType(startup_template.startup.__code__, vars(startup_template) | {"build": build, "STARTUP": STARTUP})()


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("prepare", "capture", "startup"))
    globals()[parser.parse_args().action]()
