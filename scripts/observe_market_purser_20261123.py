"""Exercise the original Market discount after assigning a Purser in a focused replay."""

from inspect import getsource
from pathlib import Path
from struct import unpack_from
from types import SimpleNamespace

from scripts import observe_market_context_v2112 as native
from scripts import observe_online_gallery_common_v1 as playback
from scripts import replay_market_bargaining_20261120 as prior
from scripts.inventory_native_common_calls import direct_bl_target
from scripts.observe_setup_save_common_v1 import REQUESTS
from scripts.reconcile_editorial_acceptance_20261123 import BASE
from scripts.register_recruitment_shortfall_20261123 import RELEASE
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.stage_cartridge_title_20261123 import CLEAN, REGISTRY, NdsImage, digest, read, write
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_shared_number_call_followups_20261123 import HELPER, NUMBER


ROOT = Path(".codex-release-work/shared_display_20261123/market_purser")
CASE, BEFORE_FINISH, SLOT, ACTOR = "assigned_purser", 11600, 2, 6
CONTROL, ROLE = 0x2090, 20
DISCOUNT_CALL, ROLL_CHECK, PRICE_RETURN = 0x020BB4A8, 0x020BC318, 0x020BB4AC
SPANS = ((0x7B60, 0x7C34), (0x132C0, 0x132CC), (0x825E4, 0x8261C),
         (0x829C8, 0x82A44), (0x82BC4, 0x82BD0), (0x82E04, 0x82E2C),
         (0xBB3C4, 0xBC3A4), (0x118A80, 0x118AC0))


def schedule(_):
    events, _, _, plan, donor = prior.schedule("revised")
    events = [event for event in events if event["start"] <= 11601]
    events.extend(dict(start=frame, duration=8, buttons=["A"]) for frame in (12001, 12401, 12801))
    return events, (11600, 11881, 12281, 12681, 13081), 13100, plan, donor


def observer(rom, folder):
    scope = vars(native) | dict(ROOT=folder, ROM=rom, REQUESTS=REQUESTS,
        TARGETS=(*REQUESTS, DISCOUNT_CALL, ROLL_CHECK, PRICE_RETURN))
    setup = checked_text(getsource(native.prepare_contract), {
        "for pc in(REQUEST,FONT):": "for pc in TARGETS:",
    })
    exec(compile(setup, __file__ + "::market-native-contract", "exec"), scope)
    scope["prepare_contract"]()
    body = getsource(native.Observer)
    start = body.index("    if frame<31000:return")
    end = body.index("   except BaseException as exc:", start)
    trace = """    if pc in REQUESTS:
     self.requests.append(dict(frame=frame,PC=pc,message_ID=v[REQUESTS[pc]],caller_LR=v[18]))
    else:
     self.rows.append(dict(frame=frame,PC=pc,registers=list(v[4:17])))
"""
    exec(compile(body[:start] + trace + body[end:], __file__ + "::market-purser-read-only", "exec"), scope)
    return scope["Observer"]


def assign_purser(core, arm):
    ct = playback.harness.ct
    core.retro_get_memory_data.argtypes = [ct.c_uint]
    core.retro_get_memory_data.restype = ct.c_void_p
    core.retro_get_memory_size.argtypes = [ct.c_uint]
    core.retro_get_memory_size.restype = ct.c_size_t
    pointer, length = core.retro_get_memory_data(2), core.retro_get_memory_size(2)
    assert pointer and length == 0x400000
    before = ct.string_at(pointer, length)
    cpu, get = get_machine(arm, before)
    controller = get(0xCB1A8) + CONTROL
    model = get(0x82E04, controller)
    actor = get(0xCB184) + 4 + ACTOR * 32
    company = get(0x397D8, get(0xCB160))
    assert company == get(0x7E958, actor) == 0 and get(0x7F244) == 0
    assert get(0x7DD38, actor, 4, ROLE) == 115
    assert get(0x7B60, 3) == ROLE and get(0x825E4, controller, 3) == 208
    assert get(0x132C0, model, SLOT) == 24 and get(0x82BC4, controller, SLOT) == 208
    assert ACTOR not in [get(0x82BC4, controller, i) for i in range(31)]
    after = bytearray(before)
    changes = []
    for address, old, value in ((model + 0x1E + SLOT, 24, ROLE), (controller + 6 + SLOT, 208, ACTOR)):
        offset = address - BASE
        assert after[offset] == old
        after[offset] = value
        cpu.mem_write(address, bytes([value]))
        ct.memmove(pointer + offset, bytes([value]), 1)
        changes.append(dict(address=address, before=old, after=value))
    assert ct.string_at(pointer, length) == after
    assert get(0x825E4, controller, 3) == ACTOR
    write(ROOT / CASE / "purser_fixture.json", dict(frame=BEFORE_FINISH, actor=ACTOR, slot=SLOT,
        finance=115, changes=changes, before_sha256=native.sha(before), after_sha256=native.sha(after)))


def main():
    release = read(RELEASE)
    assert release["registry_sha256"] == digest(REGISTRY)
    assert release["clean_input_sha256"] == digest(CLEAN)
    current = SimpleNamespace(ROM=Path(release["candidate"]), RELEASE=RELEASE)
    arm, clean = (NdsImage.open(path).read_file("/__arm9__.bin") for path in (current.ROM, CLEAN))
    assert native.sha(arm) == release["target_ARM9_sha256"]
    award = 0xBC148
    assert direct_bl_target(unpack_from("<I", clean, award)[0], BASE + award) == NUMBER
    assert direct_bl_target(unpack_from("<I", arm, award)[0], BASE + award) == HELPER
    normalized = arm[:award] + clean[award:award + 4] + arm[award + 4:]
    assert all(normalized[start:end] == clean[start:end] for start, end in SPANS)
    source = checked_text(getsource(playback.main), {
        "    installed = []": "    argv += ['--dump-capture-ram']\n    installed = []",
        "                    trace.header[0] += 1\n                    advance()":
            "                    if trace.header[0] == BEFORE_FINISH:\n"
            "                        assign_purser(core, arm)\n"
            "                    trace.header[0] += 1\n                    advance()",
    })
    scope = vars(playback) | globals() | dict(parent=current,
        get_schedule=schedule, FOCUS=set(range(3668)), arm=arm)
    exec(compile(source, __file__ + "::focused-market-purser", "exec"), scope)
    scope["main"](CASE)


if __name__ == "__main__":
    main()
