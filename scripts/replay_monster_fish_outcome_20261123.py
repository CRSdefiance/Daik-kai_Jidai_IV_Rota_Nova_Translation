"""Replay the original Monster Fish outcome after shortening the test encounter."""

from argparse import ArgumentParser
from inspect import getsource
from json import dumps, loads
from pathlib import Path
from struct import pack

from unicorn.arm_const import UC_ARM_REG_PC, UC_ARM_REG_R0, UC_ARM_REG_R4

from scripts import replay_monster_fish_trail_20261123 as trail
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.stage_cartridge_title_20261123 import CLEAN, NdsImage, digest, read, reference, sha256
from scripts.verify_personal_gameplay_v841 import get_machine


BASE = trail.BASE
RELEASE = trail.RELEASE
ROOT = trail.ROOT.with_name("monster_fish_outcome_current_20261123")
PRIOR = trail.ROOT / "position_history"
HULL_GETTER = 0x0205543C
FLEET_ACTIVE = 0x0202BDD8
ACTIVATION_TAIL = 0x0202E9AC
ACTIVATION_END = 0x0202E9BC
TEST_HULL = 3
OUTCOME_REQUEST = {"sea_inspection_context": "restore_original_Monster_Fish_activity_at_outcome"}


def activate_stock_fleet(cpu, native, target, before_ram, stock, arm):
    lo, hi = ACTIVATION_TAIL - BASE, ACTIVATION_END - BASE
    assert stock[lo:hi] == arm[lo:hi] == before_ram[lo:hi]
    assert native(FLEET_ACTIVE - BASE, target) == 0
    flag = target + 0x50
    before, = cpu.mem_read(flag, 1)
    assert before & 1
    # The original special-model initializer clears the inactive bit after
    # the virtual predicate returns zero.
    cpu.reg_write(UC_ARM_REG_R0, 0)
    cpu.reg_write(UC_ARM_REG_R4, target)
    cpu.emu_start(ACTIVATION_TAIL, ACTIVATION_END, count=16)
    assert cpu.reg_read(UC_ARM_REG_PC) == ACTIVATION_END
    assert native(FLEET_ACTIVE - BASE, target) == 1
    prepared = bytes(cpu.mem_read(BASE, len(before_ram)))
    idx = flag - BASE
    assert prepared == before_ram[:idx] + bytes([before & ~1]) + before_ram[idx + 1:]
    return prepared, dict(address=flag, before=before, after=before & ~1,
                          original_start=ACTIVATION_TAIL, original_end=ACTIVATION_END,
                          original_hex=stock[lo:hi].hex(), original_predicate=FLEET_ACTIVE)


def activate_after_played_damage(arm, raw):
    cpu, native = get_machine(arm, raw)
    fleets = native(0xCB1A8)
    target = fleets + 4 + 39 * 132
    assert bytes(cpu.mem_read(target + 16, 1)) == bytes([149])
    assert bytes(cpu.mem_read(fleets + 0x2084, 2)) == bytes([39, 2])
    mobile = native(0x36C70, target + 12)
    assert mobile and native(HULL_GETTER - BASE, mobile) == 0
    assert native(0x564C8, mobile) == 1  # The stock loop still considers the mobile for sinking.
    stock = NdsImage.open(CLEAN).read_file("/__arm9__.bin")
    prepared, activation = activate_stock_fleet(cpu, native, target, raw, stock, arm)
    return prepared, dict(context=OUTCOME_REQUEST, original_existing_model_ID=149, battle_hull_before=0,
                          original_activation_tail=activation, owned_bytes=[activation["address"]],
                          changes=[{field: activation[field] for field in ("address", "before", "after")}],
                          before_RAM_sha256=sha256(raw).hexdigest(), after_RAM_sha256=sha256(prepared).hexdigest(),
                          no_outcome_or_text_supply=True)


def shortened_encounter(starter, rom, arm_sha, model, arm, raw, request, *, activate):
    registered, proof = trail.with_position_history(starter, rom, arm_sha, model, arm, raw, request)
    cpu, native = get_machine(arm, registered)
    fleets = native(0xCB1A8)
    target = fleets + 4 + 39 * 132
    assert bytes(cpu.mem_read(target + 16, 1)) == bytes([149])
    mobile = native(0x36C70, target + 12)
    own_mobile = native(0x36C70, fleets + 4 + 132 + 12)
    assert mobile and own_mobile and mobile != own_mobile
    assert native(HULL_GETTER - BASE, mobile) == 800
    assert native(HULL_GETTER - BASE, own_mobile) == 60
    stock = NdsImage.open(CLEAN).read_file("/__arm9__.bin")
    at = HULL_GETTER - BASE
    assert stock[at:at + 8] == arm[at:at + 8] == raw[at:at + 8] == bytes.fromhex("b801d0e11eff2fe1")
    address = mobile + 0x18
    offset = address - BASE
    assert registered[offset:offset + 2] == pack("<H", 800)
    shortened = registered[:offset] + pack("<H", TEST_HULL) + registered[offset + 2:]
    cpu.mem_write(address, pack("<H", TEST_HULL))
    assert native(HULL_GETTER - BASE, mobile) == TEST_HULL
    assert bytes(cpu.mem_read(BASE, len(raw))) == shortened
    owned = set(proof["owned_bytes"]) | {address, address + 1}
    activation = None
    prepared = shortened
    if activate:
        prepared, activation = activate_stock_fleet(cpu, native, target, shortened, stock, arm)
        owned.add(activation["address"])
    changes = [dict(address=BASE + i, before=a, after=b)
               for i, (a, b) in enumerate(zip(raw, prepared, strict=True)) if a != b]
    assert all(row["address"] in owned for row in changes)
    return prepared, proof | dict(
        before_hull_fixture_RAM_sha256=proof["after_RAM_sha256"],
        after_RAM_sha256=sha256(prepared).hexdigest(), owned_bytes=sorted(owned), changes=changes,
        added_fixture=dict(address=address, storage_bytes=2, before_hull=800, supplied_hull=TEST_HULL,
                           original_getter=HULL_GETTER, original_getter_hex=stock[at:at + 8].hex()),
        original_activation_tail=activation, all_other_bytes_equal_to_position_history_fixture=True,
        no_outcome_or_text_supply=True,
    )


def open_replay(activate, label=None):
    prior = read(PRIOR / "capture/capture_report.json")
    release = read(RELEASE)
    assert prior["ROM_sha256"] == release["candidate_sha256"] == digest(release["candidate"])
    assert prior["cold_boot"] and not prior["savestate_loaded"] and not prior["callback_errors"]
    mode = {"none": "hull_3", "initial": "active_hull_3", "outcome": "outcome_hull_3"}
    label = label or mode[activate]
    assert label.isascii() and label.replace("_", "").isalnum()
    assert not (ROOT / label).exists()
    ROOT.mkdir(exist_ok=True)
    # Begin with the established declaration and steering inputs. Additional
    # actions can be written to the game's control stream at the current holds.
    prefix = ROOT / f"{label}_inputs.jsonl"
    commands = [loads(line) for line in (PRIOR / "controller.jsonl").read_text(encoding="utf-8").splitlines()]
    commands = [row for row in commands if row.get("until", 999999) <= 8640]
    assert len(commands) == 10 and commands[-1]["until"] == 8640
    commands.extend((dict(until=8870, buttons=["UP"], duration=210), dict(until=9030)))
    if activate == "outcome":
        commands.append(dict(until=9180, condition_fixture=OUTCOME_REQUEST))
    commands.append(dict(until=9300))
    prefix.write_text("".join(dumps(row) + "\n" for row in commands), encoding="utf-8")
    def fixture(starter, rom, arm_sha, model, arm, raw, request):
        if request == OUTCOME_REQUEST:
            assert activate == "outcome"
            return activate_after_played_damage(arm, raw)
        return shortened_encounter(starter, rom, arm_sha, model, arm, raw, request, activate=activate == "initial")

    scope = vars(trail.previous) | dict(ROOT=ROOT, RELEASE=RELEASE, __file__=__file__, through_history=fixture)
    play = checked_text(getsource(trail.previous.play), {
        'lambda arm, raw, request: env["special_target"](':
            'lambda arm, raw, request: through_history(env["special_target"], ',
        "fixture, = report[fixtures[0]]": "fixture = report[fixtures[0]][0]",
    })
    exec(compile(play, __file__ + "::shortened_stock_encounter", "exec"), scope)
    scope["play"]("fish", label, prefix)
    target = ROOT / label / "capture/capture_report.json"
    result = read(target)
    supplied, *outcomes = result["synthetic_condition_fixtures"]
    original, = prior["synthetic_condition_fixtures"]
    assert supplied["before_hull_fixture_RAM_sha256"] == original["after_RAM_sha256"]
    assert supplied["added_fixture"]["supplied_hull"] == TEST_HULL
    assert (supplied.get("original_activation_tail") is not None) == (activate == "initial")
    assert len(outcomes) == int(activate == "outcome")
    if outcomes:
        assert outcomes[0]["frame"] == 9030 and outcomes[0]["battle_hull_before"] == 0
    assert result["ROM_sha256"] == release["candidate_sha256"] and not result["callback_errors"]
    assert result["cold_boot"] and not result["savestate_loaded"]
    assert supplied["no_outcome_or_text_supply"]
    print("Monster Fish outcome replay:", reference(target))


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("--activate", choices=("none", "initial", "outcome"), default="none")
    parser.add_argument("--label")
    args = parser.parse_args()
    open_replay(args.activate, args.label)
