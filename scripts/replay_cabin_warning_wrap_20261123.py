"""Replay Auto Move from Riga with the captain's seat empty and the original voice selector."""

from argparse import ArgumentParser
from io import StringIO
import json
from pathlib import Path
from struct import unpack_from
import sys

from unicorn.arm_const import UC_ARM_REG_R0

from scripts import headless_desmume_v193 as harness
from scripts import native_condition_fixture_v520 as fixture
from scripts import stage_cabin_square_wrap_20261123 as stage
from scripts.probe_button_prompt_native import BASE, call, machine


base = stage.base
HISTORY = Path("work/emulation_v193/auto_move_riga_v399/capture_report.json")
DONOR = "c11024266a2f389bdbcad5d93b2e6aeda6ffc8e00ff358f82dccef2d7965eeaa"
FRAMES = (6800, 7200, 7500, 7800)
SPANS = ((0x994BC, 0x99638), (0x9963C, 0x99740), (0x82478, 0x8261C), (0x829C8, 0x82A44),
         (0x82BB8, 0x82BD0), (0x82E04, 0x82E2C), (0x53F4C, 0x53F9C),
         (0x7E988, 0x7E9A0), (0x7EB24, 0x7EB64))


def cabin_model_fixture(clean, expected_arm):
    previous = None

    def apply(arm, raw, request):
        nonlocal previous
        mode = request["mode"]
        assert request == {"mode": mode} and mode in ("empty-cabin", "restore")
        assert stage.native.digest(arm) == expected_arm and len(raw) == 0x400000
        assert all(arm[start:end] == clean[start:end] == raw[start:end] for start, end in SPANS)
        u = machine(arm)
        u.mem_write(BASE, raw)

        def get(entry, *args):
            call(u, entry, args)
            return u.reg_read(UC_ARM_REG_R0)

        ctrl = get(0xCB1A8) + 0x2090
        scratch = 0x02440000
        role = get(0x82478, ctrl, 4)
        assert get(0x829C8, ctrl, 3, scratch) >= 1 and 0 <= role < 207
        actors = get(0xCB184)
        captain = get(0x7F244)
        actor = actors + (0x19E4 if role == captain else 4 + role * 32)
        model = get(0x82E04, ctrl)
        room_getter = unpack_from("<I", u.mem_read(unpack_from("<I", u.mem_read(model, 4))[0] + 0x18, 4))[0]
        assigned = get(0x829C8, ctrl, 5, scratch)
        if mode == "empty-cabin":
            assert previous is None and assigned == 1
            room, = [i for i in range(31)
                     if get(room_getter - BASE, model, i) == 5 and get(0x82BC4, ctrl, i) != 208]
            occupant = get(0x82BC4, ctrl, room)
            assert occupant == captain and occupant != role
            voice_field = get(0x7EB24, actor) + 0x1C
            assert bytes(u.mem_read(voice_field, 1)) == bytes((1,))
            assert get(0x53F4C, actor, 0x02117820) == 646
            get(0x82BB8, ctrl, room, 208)
            u.mem_write(voice_field, bytes((4,)))
            assert get(0x82BC4, ctrl, room) == 208 and get(0x829C8, ctrl, 5, scratch) == 0
            assert get(0x53F4C, actor, 0x02117820) == 649
            previous = ctrl, room, occupant, role, voice_field
            changes = ((ctrl + 6 + room, occupant, 208), (voice_field, 1, 4))
        else:
            saved_ctrl, room, occupant, saved_role, voice_field = previous
            assert (ctrl, role, assigned) == (saved_ctrl, saved_role, 0)
            assert get(0x82BC4, ctrl, room) == 208 and get(0x53F4C, actor, 0x02117820) == 649
            get(0x82BB8, ctrl, room, occupant)
            u.mem_write(voice_field, bytes((1,)))
            assert get(0x82BC4, ctrl, room) == occupant and get(0x829C8, ctrl, 5, scratch) == 1
            assert get(0x53F4C, actor, 0x02117820) == 646
            changes = ((ctrl + 6 + room, 208, occupant), (voice_field, 4, 1))
        after = bytes(u.mem_read(BASE, len(raw)))
        assert get(0x829C8, ctrl, 3, scratch) >= 1 and get(0x82478, ctrl, 4) == role
        changed = {BASE + index: (time_a, time_b) for index, (time_a, time_b)
                   in enumerate(zip(raw, after, strict=True)) if time_a != time_b}
        assert changed == {address: (before, new) for address, before, new in changes}
        return after, dict(mode=mode, captain=captain, surveyor=role, cabin_room=room,
            only_cabin_occupant_and_surveyor_voice_changed=True, original_compiled_code_unmodified=True,
            source_selected_warning=649 if mode == "empty-cabin" else 646,
            changes=[dict(address=address, before=before, after=new) for address, before, new in changes])

    return apply


def replay(side):
    previous = base.load(stage.parent.RELEASE)
    if side == "old":
        rom, sha = stage.parent.ROM, previous["candidate_sha256"]
    else:
        proof = base.load(stage.PROOF)
        assert proof["predecessor_sha256"] == previous["candidate_sha256"]
        rom, sha = stage.ROM, proof["candidate_sha256"]
    assert base.digest(rom) == sha
    arm = base.NdsImage.open(rom).read_file(stage.ARM)
    clean = base.NdsImage.open(stage.CLEAN).read_file(stage.ARM)
    assert stage.native.digest(arm) == previous["target_ARM9_sha256"]
    report = base.load(HISTORY)
    donor = report["battery_save_preloaded"]
    assert base.digest(donor["source"]) == donor["source_sha256"] == DONOR
    focus = stage.ROOT / f"{side}_cabin"
    focus.mkdir(parents=True)
    inputs = focus / "inputs.json"
    base.save(inputs, [row for row in report["scripted_input_schedule"] if row["start"] <= 7200])
    requests = [
        {"until": 7500, "buttons": ["A"], "duration": 8, "condition_fixture": {"mode": "empty-cabin"}},
        {"until": 7800, "buttons": ["A"], "duration": 8, "condition_fixture": {"mode": "restore"}},
        {"stop": True},
    ]
    original_argv, original_stdin, original_fixture = sys.argv, sys.stdin, fixture.set_condition
    fixture.set_condition = cabin_model_fixture(clean, previous["target_ARM9_sha256"])
    try:
        sys.stdin = StringIO("".join(json.dumps(row) + "\n" for row in requests))
        sys.argv = [__file__, "--rom", str(rom), "--out", str(focus / "capture"), "--frames", "7800",
            "--inputs-json", str(inputs), "--battery-save", donor["source"], "--touchscreen",
            "--capture-every", "999999", "--capture-at", *map(str, FRAMES),
            "--pause-at", "7200", "--allow-condition-fixtures"]
        harness.main()
    finally:
        sys.argv, sys.stdin, fixture.set_condition = original_argv, original_stdin, original_fixture
    path = focus / "capture/capture_report.json"
    result = base.load(path)
    assert result["ROM_sha256"] == sha and result["frames"] == FRAMES[-1]
    assert result["cold_boot"] and not result["savestate_loaded"] and not result["callback_errors"]
    assert base.digest(donor["source"]) == result["battery_save_preloaded"]["source_sha256"] == DONOR
    supplied = result["synthetic_condition_fixtures"]
    assert [row["mode"] for row in supplied] == ["empty-cabin", "restore"]
    assert [row["source_selected_warning"] for row in supplied] == [649, 646]
    for original, restored in zip(*(row["changes"] for row in supplied), strict=True):
        assert (original["address"], original["before"], original["after"]) == (
            restored["address"], restored["after"], restored["before"])
    base.save(focus / "terminal.json", dict(candidate_sha256=sha, capture=str(path), report_sha256=base.digest(path),
        earlier_reference=str(HISTORY), donor_sha256=DONOR, focused_commands=requests,
        only_fixture_fields_restored=True, natural_activation=False))


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("side", choices=("old", "new"))
    replay(parser.parse_args().side)
