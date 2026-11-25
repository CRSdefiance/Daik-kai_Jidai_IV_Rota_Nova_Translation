"""Replay Monster Fish using the stock registration path's complete position history."""

from inspect import getsource
from json import dumps, loads
from pathlib import Path
from struct import pack
from hashlib import sha256

from unicorn import UC_HOOK_CODE

from scripts import play_special_target_battle_20261123 as previous
from scripts.observe_monster_fish_transition_20261123 import RELEASE, ROOT
from scripts.stage_cartridge_title_20261123 import CLEAN, NdsImage, digest, read, write
from scripts.verify_personal_gameplay_v841 import get_machine

BASE = 0x02000000
WRAPPER = 0x0202CFFC
HISTORY_WRITER = 0x02055790
ENTRY = 0x0202D08C
FILL = 0x0202D114


def with_position_history(starter, rom, arm_sha, model, arm, raw, request):
    registered, proof = starter(rom, arm_sha, model, arm, raw, request)
    assert model == 149 and proof["original_existing_fleet_ID"] == 39
    stock = NdsImage.open(CLEAN).read_file("/__arm9__.bin")
    spans = ((WRAPPER, 0x0202D124), (HISTORY_WRITER, 0x020557C8), (0x02033760, 0x020338E4))
    assert all(arm[lo-BASE:hi-BASE] == stock[lo-BASE:hi-BASE] == raw[lo-BASE:hi-BASE] for lo, hi in spans)
    cpu, get = get_machine(arm, raw)
    fleets, world = (get(offset) for offset in (0xCB1A8, 0xCB19C))
    assert bytes(cpu.mem_read(fleets + 0x2084, 12))[::4] == bytes([64, 64, 64])
    assert get(0x2E58C) == 1
    offset, length = world + 0x234 + 0x30C - BASE, 65 * 12
    assert raw[offset:offset + length] == registered[offset:offset + length] == bytes(length)
    target = fleets + 4 + 39 * 132
    cpu.mem_write(target + 0x34, pack("<2i", *proof["target_point"]))
    visited = []
    points = (ENTRY, FILL, HISTORY_WRITER)
    hooks = [cpu.hook_add(UC_HOOK_CODE, lambda _u, pc, _n, _d: visited.append(pc), begin=a, end=a) for a in points]
    try:
        assert get(WRAPPER - BASE, fleets, 39, 1) == 1
    finally:
        for hook in hooks:
            cpu.hook_del(hook)
    assert visited == list(points)
    full = bytearray(cpu.mem_read(BASE, len(raw)))
    lookout = {f["address"] for f in proof["declared_regions"] if f["label"] in ("lookout_slot3", "previous_Charles_slot9")}
    outside = {BASE + i for i, (a, b) in enumerate(zip(full, registered, strict=True)) if a != b
               and not offset <= i < offset + length}
    assert outside == lookout
    for address in lookout:
        full[address - BASE] = registered[address - BASE]
    trail = bytes(full[offset:offset + length])
    record = trail[:12]
    assert trail == record * 65
    assert record[4:] == pack("<2i", *(value * 128 for value in proof["target_point"]))
    assert full[:offset] == registered[:offset] and full[offset + length:] == registered[offset + length:]
    # Preserve the original inspection fixture receipt nested in the new one.
    changes = [dict(address=BASE + i, before=a, after=b) for i, (a, b) in enumerate(zip(raw, full, strict=True)) if a != b]
    owned = sorted(set(proof["owned_bytes"]) | set(range(BASE + offset, BASE + offset + length)))
    assert all(row["address"] in owned for row in changes)
    full = bytes(full)
    return full, proof | dict(before_trail_fixture=proof, after_RAM_sha256=sha256(full).hexdigest(),
        changes=changes, owned_bytes=owned, complete_stock_registration_wrapper=WRAPPER,
        exact_wrapper_call_chain=visited, position_history_address=BASE + offset, position_history_size=length,
        position_history_records=65, each_record_hex=record.hex(), source_exact_spans=spans,
        all_other_bytes_equal_to_previous_inspection_fixture=True, no_outcome_or_text_supply=True)


def main():
    folder = ROOT / "position_history"
    release = read(RELEASE)
    assert digest(release["candidate"]) == release["candidate_sha256"]
    assert not folder.exists()
    source = (previous.ROOT / "fish_approach/controller.jsonl").read_text(encoding="utf8")
    commands = [loads(line) for line in source.splitlines()][:7]
    assert commands[-1]["until"] == 7600
    commands.append(dict(until=8000))
    journal = ROOT / "position_history_prefix.jsonl"
    journal.write_text("".join(dumps(row) + "\n" for row in commands), encoding="utf8")
    play = getsource(previous.play)
    old = 'lambda arm, raw, request: env["special_target"]('
    assert play.count(old) == 1
    play = play.replace(old, 'lambda arm, raw, request: through_history(env["special_target"], ')
    scope = vars(previous) | dict(ROOT=ROOT, RELEASE=RELEASE, __file__=__file__, through_history=with_position_history)
    exec(compile(play, __file__ + "::stock_position_history_replay", "exec"), scope)
    scope["play"]("fish", folder.name, journal)
    target = folder / "capture/capture_report.json"
    report = read(target)
    fixture, = report["synthetic_condition_fixtures"]
    assert fixture["complete_stock_registration_wrapper"] == WRAPPER
    assert fixture["position_history_records"] == 65 and fixture["all_other_bytes_equal_to_previous_inspection_fixture"]
    write(folder / "terminal.json", dict(capture=str(target), capture_sha256=digest(target),
          release=report["ROM_sha256"], last_frame=report["frames"], source_position_history_filled=True))


if __name__ == "__main__":
    main()
