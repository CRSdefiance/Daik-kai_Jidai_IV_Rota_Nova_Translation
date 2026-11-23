"""Check the stock-up choices using a copied Copenhagen save."""

from argparse import ArgumentParser
from pathlib import Path
from struct import unpack
import sys

from unicorn.arm_const import UC_ARM_REG_R0

from scripts import headless_desmume_v193 as harness
from scripts import native_condition_fixture_v520 as fixture_adapter
from scripts import register_rafael_sailing_modes_20261119 as current
from scripts import replay_port_supply_dialogue_20261115 as history
from scripts.probe_button_prompt_native import BASE, call, machine
from scripts.run_battle_cooking_livestock_live_v911 import GrowingCommands

base = current.base
ROOT = Path("work/port_resupply_options_20261119_v2")
FRAMES = (3200, 3400, 3550, 3750, 3950, 4200, 4400, 4600, 4750, 5000, 5400, 5750, 6000)


def state_for(arm, raw, request):
    release = base.load(current.RELEASE)
    assert current.native.digest(arm) == release["target_ARM9_sha256"]
    earlier = base.NdsImage.open("out/all_routes_combined_v762_candidate.nds").read_file(current.native.ARM)
    for start, stop in ((0x60518, 0x6063C), (0x34E60, 0x34FE4), (0x2E58C, 0x2E5A4),
                        (0xCB148, 0xCB15C), (0xCB1A8, 0xCB1B8), (0x3CC80, 0x3CCD4)):
        assert earlier[start:stop] == arm[start:stop]
    cpu = machine(arm)
    cpu.mem_write(BASE, raw)

    def get(fn, *args):
        call(cpu, fn, args)
        return cpu.reg_read(UC_ARM_REG_R0)

    fleet = get(0xCB1A8) + 4 + 0x84 * get(0x2E58C)
    root = get(0xCB148)
    ids = [cpu.mem_read(fleet+0x10+8*i, 1)[0] for i in range(5)]
    assert len(set(ids)) == 5 and max(ids) < 155
    ships = [root+4+0x8C*i for i in ids]
    capacity = get(0x34E60, fleet)
    get(0x34EB0, fleet, 0x02450000)
    assert unpack("<2I", cpu.mem_read(0x02450000, 8)) == (350, 350)
    assert capacity == 700
    owner = get(0xCB160)
    force = owner + 4 + get(0x397D8, owner) * 0x4C
    funds = get(0x3CCC8, force)
    assert funds == 25975
    mode = request["mode"]
    if mode == "mix":
        supplies, budget = (0, capacity), funds
    else:
        assert mode == "poor"
        supplies, budget = (0, 0), 10
        get(0x3CC80, force, budget-funds)
    get(0x60518, 0, *supplies)
    get(0x34EB0, fleet, 0x02450000)
    assert unpack("<2I", cpu.mem_read(0x02450000, 8)) == supplies and get(0x3CCC8, force) == budget
    after = bytes(cpu.mem_read(BASE, len(raw)))
    changes = [dict(address=BASE+i, before=x, after=y) for i, (x, y) in enumerate(zip(raw, after, strict=True)) if x != y]
    windows = [(p+0x3E, p+0x42) for p in ships] + ([(force+12, force+16)] if budget != funds else [])
    assert changes and all(any(lo <= x["address"] < hi for lo, hi in windows) for x in changes)
    return after, dict(mode=mode, before_water_food=[350, 350], after_water_food=supplies,
        before_gold=funds, after_gold=budget, changes=changes, native_fleet=fleet,
        all_other4MiB_RAM_exact=True, fixture_source_sha256=base.digest(__file__))


def run(mode):
    report = base.load(history.WATER)
    donor = report["battery_save_preloaded"]
    assert base.digest(donor["source"]) == donor["source_sha256"]
    folder = ROOT / mode
    folder.mkdir(parents=True)
    inputs, commands = folder / "inputs.json", folder / "commands.jsonl"
    schedule = [entry for entry in report["scripted_input_schedule"] if entry["start"] <= 3201]
    buttons = [(3601, "B"), (4901, "B")] if mode == "mix" else [(3601, "A"), (4001, "A"), (4901, "B")]
    schedule.extend(dict(start=when, duration=8, buttons=[button]) for when, button in buttons)
    base.save(inputs, schedule)
    commands.write_text(f'{{"until": 6000, "condition_fixture": {{"mode": "{mode}"}}}}\n{{"stop": true}}\n',
                        encoding="utf-8")
    argv = [sys.argv[0], "--rom", str(current.ROM), "--out", str(folder / "capture"),
        "--frames", "6001", "--inputs-json", str(inputs), "--press-start", "-1",
        "--battery-save", donor["source"], "--touchscreen", "--capture-every", "999999",
        "--capture-at", *map(str, FRAMES), "--pause-at", "3200", "--dump-pause-ram", "--allow-condition-fixtures"]
    stream = GrowingCommands(commands)
    old, old_stdin, old_argv = fixture_adapter.set_condition, sys.stdin, sys.argv
    try:
        fixture_adapter.set_condition = state_for
        sys.stdin, sys.argv = stream, argv
        harness.main()
    finally:
        fixture_adapter.set_condition, sys.stdin, sys.argv = old, old_stdin, old_argv
        stream.close()


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=("mix", "poor"))
    run(parser.parse_args().mode)
