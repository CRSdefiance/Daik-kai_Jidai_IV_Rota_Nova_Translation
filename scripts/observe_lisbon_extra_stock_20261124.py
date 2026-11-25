"""Exercise the Lisbon extra-stock offer with an isolated Finance prerequisite."""

import json
import sys
from inspect import getsource
from struct import pack, unpack_from

from scripts import observe_lisbon_purchase_variants_20261124 as prior
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.stage_cartridge_title_20261123 import CLEAN, NdsImage, REGISTRY, digest, read, sha256, write
from scripts.verify_personal_gameplay_v841 import get_machine

ROOT = prior.ROOT.with_name("editorial_20261124_lisbon_extra_stock_v2")
CONTROLLER = ROOT / "controller.jsonl"
PAUSE = prior.PAUSE
BASE = 0x02000000
ACTIONS = (
    dict(until=37700, buttons=["A"], duration=8, extra_stock_fixture=True),
    dict(until=38100, buttons=["A"], duration=8),
    dict(until=38500, duration=8, touch=[94, 105]),
    dict(until=38900, duration=8, buttons=["A"]),
    dict(until=39300, duration=8, buttons=["A"]),
    dict(until=39700, duration=8, buttons=["B"]),
    dict(until=40100, duration=8, buttons=["A"]),
    dict(until=40500, duration=8, buttons=["A"]),
    dict(stop=True),
)


def finance_prerequisite(arm, raw, request):
    """Set Julio's existing XP word just high enough for the original Finance test."""
    release = read(prior.current.RELEASE)
    assert request is True and len(raw) == 0x400000
    assert sha256(arm).hexdigest() == release["target_ARM9_sha256"]
    clean = NdsImage.open(CLEAN).read_file(prior.current.ARM)
    spans = ((0x7DD38, 0x7DE20), (0xBAA74, 0xBAB3C), (0xBB238, 0xBB26C))
    assert all(arm[lo:hi] == clean[lo:hi] for lo, hi in spans)
    cpu, get = get_machine(arm, raw)
    role = get(0xCB1A8) + unpack_from("<I", arm, 0xBAB34)[0]
    assert get(0x825E4, role, 3) == 6 and get(0x7F244) == 0
    actor = get(0xCB184) + 4 + 6 * 32
    xp = actor + 16
    town = get(0xB6618)
    eligible = [(slot, get(0xB39B0, town, slot)) for slot in range(5) if get(0xB3AE8, town, slot)]
    assert get(0xB65E4) == 11 and get(0xB4A88, town) == 20
    assert eligible and any(quantity > 0 for _, quantity in eligible)
    assert get(0x7DD38, actor, 4, 20) == 115 and get(0xBAA74) == 0
    lo = unpack_from("<I", raw, xp - BASE)[0]
    original = lo
    hi = 250000
    cpu.mem_write(xp, pack("<I", hi))
    assert get(0x7DD38, actor, 4, 20) >= 160 and get(0xBAA74) == 1
    while lo + 1 < hi:
        mid = (lo + hi) // 2
        cpu.mem_write(xp, pack("<I", mid))
        if get(0x7DD38, actor, 4, 20) >= 160:
            hi = mid
        else:
            lo = mid
    cpu.mem_write(xp, pack("<I", lo))
    assert get(0x7DD38, actor, 4, 20) < 160 and get(0xBAA74) == 0
    cpu.mem_write(xp, pack("<I", hi))
    finance = get(0x7DD38, actor, 4, 20)
    assert finance == 160 and get(0xBAA74) == 1
    voice = get(0x7E988, actor)
    after = bytearray(raw)
    changes = []
    for i, new in enumerate(pack("<I", hi)):
        position = xp - BASE + i
        old = raw[position]
        if new != old:
            after[position] = new
            changes.append(dict(address=xp + i, before=old, after=new))
    return bytes(after), dict(changes=changes, boundary=dict(experience_below=lo, experience=hi, original_experience=original),
        actor=6, finance_before=115, finance_after=finance, town=11, share=20, source_stock_slots=eligible,
        native_predicate_before=0, native_predicate_after=1, native_voice=voice, message=754 if voice in (0, 1) else 753 + voice,
        full_RAM_before_sha256=sha256(raw).hexdigest(), full_RAM_after_sha256=sha256(after).hexdigest())


def main():
    release = read(prior.current.RELEASE)
    assert digest(REGISTRY) == release["registry_sha256"] and digest(prior.current.ROM) == release["candidate_sha256"]
    book = read(prior.BOOK)
    parent = book["evidence"]["capture"]
    assert digest(parent["path"]) == parent["sha256"]
    history = read(parent["path"])
    donor = history["battery_save_preloaded"]
    assert history["frames"] == PAUSE and history["cold_boot"] and not history["savestate_loaded"]
    assert not history["callback_errors"] and not any(v for k, v in history.items() if k.startswith("synthetic_"))
    assert digest(donor["source"]) == donor["source_sha256"] == book["evidence"]["donor"]["sha256"]
    ROOT.mkdir()
    plan = ROOT / "inputs.json"
    write(plan, history["scripted_input_schedule"])
    with CONTROLLER.open("x", encoding="utf-8") as control:
        for action in ACTIONS:
            control.write(json.dumps(action) + "\n")
    original = getsource(prior.harness.main)
    adapted = checked_text(original, {
        "from scripts.native_missionary_fixture_v623 import assign as assign_missionary":
            "assign_missionary = finance_prerequisite",
        "'missionary_fixture'": "'extra_stock_fixture'",
        "synthetic_missionary_Chapel_assignment_fixtures": "synthetic_market_finance_prerequisite",
        "earned_qualifications_refit_assignment_or_goods_acquisition_verified": "earned_finance_prerequisite_verified",
        "Isolated Chapel/Manuel fixture applied; no earned refit, qualification or assignment credit.":
            "Isolated Market Finance prerequisite applied.",
    })
    scope = vars(prior.harness) | {"finance_prerequisite": finance_prerequisite}
    exec(compile(adapted, __file__ + "::finance-prerequisite", "exec"), scope)
    stream = prior.GrowingCommands(CONTROLLER)
    args, stdin = sys.argv, sys.stdin
    try:
        sys.argv = [__file__, "--rom", str(prior.current.ROM), "--out", str(ROOT / "capture"),
            "--frames", "100000", "--inputs-json", str(plan), "--battery-save", donor["source"],
            "--touchscreen", "--press-start", "-1", "--capture-every", "999999", "--pause-at", str(PAUSE),
            "--dump-pause-ram", "--allow-missionary-fixtures"]
        sys.stdin = stream
        scope["main"]()
    finally:
        sys.argv, sys.stdin = args, stdin
        stream.close()
    assert digest(donor["source"]) == donor["source_sha256"]
    write(ROOT / "runner.json", dict(harness_sha256=digest(prior.harness.__file__),
        in_memory_adapter_sha256=sha256(adapted.encode()).hexdigest(), original_donor_sha256=donor["source_sha256"]))


if __name__ == "__main__":
    main()
