"""Exercise the original shore Search outcome at a source-checked coastline."""

from argparse import ArgumentParser
from inspect import getsource
from io import StringIO
from json import dumps
from pathlib import Path
from struct import pack, unpack_from
import sys
from types import SimpleNamespace

from scripts import headless_desmume_v193 as harness
from scripts import native_battle_fixture_v620 as dispatcher
from scripts import stage_power_and_gold_digits_20261121 as stage
from scripts.research_fatigue_shore_v1587c import original_terrain
from scripts.verify_personal_gameplay_v841 import get_machine


base = stage.base
PLAN = Path("work/analysis/search_reports_live_v1680/run_plan.json")
POINT = (7394, 1256)
BASE = 0x02000000
SELECTORS = 0x119164
SPAN = ((0x699F0, 0x69B5C), (0x797A0, 0x79958), (0x79E50, 0x79E98), (SELECTORS, SELECTORS + 48))
REQUEST = {"search_gold_qa": "verified_coast"}


def terrain(rom, arm):
    source = getsource(original_terrain)
    statement = "        rows.append({'map_point': list(point), 'native_collision_result': result, 'collision_free': result == 0})"
    assert source.count(statement) == 1
    revised = statement + """
        call(u,0x699f0,(0x02468000,0x02460100))
        rows[-1]['land_in_Search_range'] = bool(u.reg_read(UC_ARM_REG_R0))
        call(u,0x797a0,(0x02460100,))
        rows[-1]['region'] = u.reg_read(UC_ARM_REG_R0)"""

    def open_rom(path):
        return rom if path == "out/all_routes_combined_v604_candidate.nds" else base.NdsImage.open(path)

    env = original_terrain.__globals__ | {"NdsImage": SimpleNamespace(open=open_rom)}
    exec(compile(source.replace(statement, revised), __file__ + "::terrain-proof", "exec"), env)
    report = env["terrain_queries"](arm, [POINT])
    row, = report["queries"]
    assert row["collision_free"] and row["land_in_Search_range"] and row["region"] == 5
    return report


def place(arm, raw, request):
    assert request == REQUEST and len(raw) == 0x400000
    cpu, get = get_machine(arm, raw)
    captain = get(0x7F244)
    assert captain == get(0x2E58C) == 1
    fleet = get(0xCB1A8) + 4 + 132 * captain
    owned = {}
    for slot in range(5):
        model = get(0x36C70, fleet + 12 + 8 * slot)
        assert model and get(0x564C8, model)
        owned[model + 16] = pack("<2i", *(component * 128 for component in POINT))
    owned[fleet + 0x34] = pack("<2i", *POINT)
    after = bytearray(raw)
    for address, replacement in owned.items():
        at = address - BASE
        after[at:at + 8] = replacement
    changed = [dict(address=address + i, before=raw[address + i - BASE], after=value)
               for address, replacement in owned.items() for i, value in enumerate(replacement)
               if value != raw[address + i - BASE]]
    assert len(owned) == 6 and 0 < len(changed) <= 48
    assert sum(a != b for a, b in zip(raw, after, strict=True)) == len(changed)
    after = bytes(after)
    check, query = get_machine(arm, after)
    pointer = 0x02470000
    query(0x2C1C4, pointer, fleet)
    assert bytes(check.mem_read(pointer, 8)) == pack("<2i", *POINT)
    assert query(0x797A0, pointer) == 5
    return after, dict(context="five own ships and cached fleet position", changes=changed,
                       copied_original_fleet_coordinates_only=True, stats_and_event_state_untouched=True,
                       original_region=5, world_map_point=POINT, owned_bytes=48,
                       before_RAM_sha256=stage.native.digest(raw), after_RAM_sha256=stage.native.digest(after))


def run(version, plan_path, label):
    destination = stage.ROOT / label
    assert not destination.exists()
    release = base.load(stage.parent.RELEASE if version == "before" else stage.PROOF)
    path = stage.parent.ROM if version == "before" else stage.ROM
    assert base.digest(path) == release["candidate_sha256"]
    rom = base.NdsImage.open(path)
    arm = rom.read_file(stage.rewards.shared.ARM)
    clean = base.NdsImage.open(stage.rewards.shared.CLEAN).read_file(stage.rewards.shared.ARM)
    assert all(arm[lo:hi] == clean[lo:hi] for lo, hi in SPAN)
    assert unpack_from("<I", arm, SELECTORS + 40) == (0x02079190,)
    geography = terrain(rom, arm)
    history = base.load(PLAN)
    donor, inputs = map(Path, (history["disposable_donor"], history["original_load_inputs"]))
    assert base.digest(donor) == history["source_donor_sha256"]
    assert base.digest(inputs) == history["original_load_inputs_sha256"]
    commands = base.load(plan_path)
    assert [c["battle_fixture"] for c in commands if "battle_fixture" in c] == [REQUEST]
    assert commands[-1] == {"stop": True}
    last = commands[-2]["until"]
    destination.mkdir()
    base.save(destination / "inputs.json", commands)
    base.save(destination / "terrain.json", geography)
    old = sys.argv, sys.stdin, dispatcher.apply_fixture
    try:
        sys.argv = [__file__, "--rom", str(path), "--out", str(destination / "capture"), "--frames", str(last + 1),
                    "--inputs-json", str(inputs), "--battery-save", str(donor), "--touchscreen",
                    "--capture-every", "999999", "--pause-at", "4800", "--dump-ram", "--allow-battle-fixtures"]
        sys.stdin = StringIO("".join(dumps(item) + "\n" for item in commands))
        dispatcher.apply_fixture = place
        harness.main()
    finally:
        sys.argv, sys.stdin, dispatcher.apply_fixture = old
    record = base.load(destination / "capture/capture_report.json")
    assert record["frames"] == last and record["cold_boot"] and not record["savestate_loaded"] and not record["callback_errors"]
    assert record["ROM_sha256"] == release["candidate_sha256"] and base.digest(donor) == history["source_donor_sha256"]


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("version", choices=("before", "after"))
    parser.add_argument("plan", type=Path)
    parser.add_argument("label")
    args = parser.parse_args()
    run(args.version, args.plan, args.label)
