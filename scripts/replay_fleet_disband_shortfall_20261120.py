"""Verify the original Cancel and Disband responses with a supplied fleet debt."""

from argparse import ArgumentParser
from hashlib import sha256
from io import StringIO
from json import dumps, loads
from pathlib import Path
from struct import pack, unpack_from
from subprocess import run
import sys
from types import ModuleType

ROOT = Path("work/fleet_disband_shortfall_20261120") / "plain_child"
BASE = 0x02000000
FLEET_ID, INIT_FRAME, FINAL_FRAME = 57, 10000, 12000
WALLET, EXPENSES = 37, 100_500
FRAMES = (9400, 10000, 10360, 10840, 11080, 11440, 11560, 11680, 11800)
DEPENDENCIES = ((0x5A27C, 0x5A388), (0x5A4B4, 0x5A528), (0x3CC80, 0x3CCD0), (0x3FA9C, 0x3FAA0))


def supply_shortfall(arm, raw, request):
    from dk4tool.rom.nds import NdsImage
    from scripts import checkpoint_fleet_debt_disband_20261115 as prior
    from scripts.verify_personal_gameplay_v841 import get_machine

    clean = NdsImage.open(prior.CLEAN).read_file(prior.ARM)
    assert len(raw) == 0x400000 and request == {"mode": "disband-shortfall"}
    assert all(raw[lo:hi] == arm[lo:hi] == clean[lo:hi] for lo, hi in DEPENDENCIES)
    assert unpack_from("<3I", arm, 0x5A37C) == (100_000, 285, 286)
    _, owner = prior.setup(raw, arm, FLEET_ID)
    _, get = get_machine(arm, raw)
    finance = get(0x367FC, owner["fleet"])
    assert owner["finance"] == finance
    assert unpack_from("<3I", raw, finance + 0xC - BASE) == (0, 0, 0)
    assert prior.field(raw, owner["wallet"]) == 897_400
    amended = bytearray(raw)
    edit = {owner["wallet"]: WALLET, finance + 0xC: EXPENSES}
    for address, value in edit.items():
        assert BASE <= address < BASE + len(raw) - 4
        amended[address - BASE:address - BASE + 4] = pack("<I", value)
    changes = [dict(address=BASE + i, before=a, after=b)
               for i, (a, b) in enumerate(zip(raw, amended, strict=True)) if a != b]
    assert changes and all(any(addr <= r["address"] < addr + 4 for addr in edit) for r in changes)
    return bytes(amended), dict(fleet_ID=FLEET_ID, wallet_address=owner["wallet"], fleet_expenses_address=finance + 0xC,
        company_gold=WALLET, fleet_expenses=EXPENSES, original_disband_delta=100_000 - EXPENSES, changes=changes,
        two_original_finance_words_only=True)


def main(case):
    from scripts import checkpoint_fleet_debt_disband_20261115 as prior
    from scripts import register_market_bargaining_20261120 as current

    base, rom = current.base, current.stage.ROM
    release = base.load(current.RELEASE)
    assert base.digest(rom) == base.digest(current.ROM) == release["candidate_sha256"]
    assert base.digest(prior.CLEAN) == release["clean_input_sha256"] and base.digest(base.REGISTRY) == release["registry_sha256"]
    events, _, end, _, donor = prior.playback.schedule("fleet")
    assert end == FINAL_FRAME and base.digest(donor["source"]) == donor["source_sha256"]
    folder = ROOT / ("shortfall_isolated" if case == "shortfall" else case)
    folder.mkdir(parents=True)
    plan = folder / "inputs.json"
    base.save(plan, events)
    args = ["--rom", str(rom), "--out", str(folder / "capture"),
        "--frames", str(FINAL_FRAME), "--inputs-json", str(plan), "--battery-save", donor["source"],
        "--touchscreen", "--press-start", "-1", "--capture-every", "999999",
        "--capture-at", *map(str, FRAMES), "--dump-capture-ram"]
    if case == "shortfall":
        control = ROOT / "control/capture"
        report = base.load(control / "capture_report.json")
        snapshot, = [r for r in report["read_only_capture_RAM_snapshots"] if r["frame"] == INIT_FRAME]
        raw = Path(snapshot["path"]).read_bytes()
        assert report["ROM_sha256"] == release["candidate_sha256"]
        assert snapshot["read_only_export"] and sha256(raw).hexdigest() == snapshot["sha256"]
        arm = base.NdsImage.open(rom).read_file(prior.ARM)
        request = {"mode": "disband-shortfall"}
        after, receipt = supply_shortfall(arm, raw, request)
        recipe = folder / "scoped_runtime_inputs.json"
        base.save(recipe, dict(arm_sha256=sha256(arm).hexdigest(), before_sha256=sha256(raw).hexdigest(),
            after_sha256=sha256(after).hexdigest(), request=request, receipt=receipt))
        args.extend(("--pause-at", str(INIT_FRAME), "--allow-condition-fixtures"))
        entry = [__file__, "--shortfall-emulator", str(recipe)]
    else:
        entry = ["-m", "scripts.headless_desmume_v193"]
    run([sys.executable, "-B", *entry, *args], check=True)
    assert base.digest(donor["source"]) == donor["source_sha256"]


def run_shortfall_emulator():
    from scripts import headless_desmume_v193 as harness

    recipe = loads(Path(sys.argv[2]).read_text(encoding="utf-8"))
    receipt = recipe["receipt"]

    def apply(arm, raw, request):
        assert request == recipe["request"] and sha256(arm).hexdigest() == recipe["arm_sha256"]
        assert sha256(raw).hexdigest() == recipe["before_sha256"] and len(raw) == 0x400000
        amended = bytearray(raw)
        for row in receipt["changes"]:
            offset = row["address"] - BASE
            assert amended[offset] == row["before"]
            amended[offset] = row["after"]
        assert sha256(amended).hexdigest() == recipe["after_sha256"]
        return bytes(amended), receipt.copy()

    # Keep the native snapshot analyzer in the parent process. Loading its
    # emulator libraries in the DeSmuME process can invalidate core handles.
    adapter = ModuleType("scripts.native_condition_fixture_v520")
    adapter.set_condition = apply
    legacy = ModuleType("scripts.native_condition_fixture_v637")
    legacy.ARM_SHA = "1f6ed33c8ee91bdeb1667e3f7524f3731ac7b0ba89a07f4be4ee1422cd7851bb"
    sys.modules[adapter.__name__], sys.modules[legacy.__name__] = adapter, legacy
    commands = (dict(until=FINAL_FRAME, condition_fixture={"mode": "disband-shortfall"}), {"stop": True})
    sys.stdin = StringIO("".join(dumps(command) + "\n" for command in commands))
    del sys.argv[1:3]
    harness.main()


if __name__ == "__main__":
    if sys.argv[1:2] == ["--shortfall-emulator"]:
        run_shortfall_emulator()
    else:
        cli = ArgumentParser(description=__doc__)
        cli.add_argument("case", choices=("control", "shortfall"))
        main(cli.parse_args().case)
