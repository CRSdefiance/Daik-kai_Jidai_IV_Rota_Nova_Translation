"""Exercise the current Disband dialog with a bounded finance fixture and original inputs."""

from inspect import getsource
from pathlib import Path
from struct import pack, unpack_from

from scripts import checkpoint_fleet_debt_disband_20261115 as debt
from scripts import observe_online_gallery_common_v1 as playback
from scripts import observe_setup_save_common_v1 as trace
from scripts import register_tavern_nearby_town_wrap_20261123 as current
from scripts.source_locked_derivation_v5118 import checked_text


base, native = current.base, current.native
ROOT = Path(".codex-release-work/disband_shortfall_20261123")
CASE, FRAME, FLEET_ID = "fleet", 9800, 57
EXPENSES, GOLD = 100_500, 37
SCHEDULE = debt.playback.schedule
FIXTURE = ROOT / CASE / "finance_fixture.json"
SPANS = ((0x5A27C, 0x5A388), (0x5A4B4, 0x5A528), (0x3CC80, 0x3CCD0), (0x3FA9C, 0x3FAA0))


def supply_shortfall(core, arm):
    ct = playback.harness.ct
    core.retro_get_memory_data.argtypes = [ct.c_uint]
    core.retro_get_memory_data.restype = ct.c_void_p
    core.retro_get_memory_size.argtypes = [ct.c_uint]
    core.retro_get_memory_size.restype = ct.c_size_t
    pointer, size = core.retro_get_memory_data(2), core.retro_get_memory_size(2)
    assert pointer and size == 0x400000
    before = ct.string_at(pointer, size)
    _, owner = debt.setup(before, arm, FLEET_ID)
    assert owner["company"] == 2 and owner["fleet_id"] == FLEET_ID
    wallet, expense = owner["wallet"] - debt.BASE, owner["finance"] - debt.BASE + 0xC
    assert unpack_from("<3I", before, expense) == (0, 0, 0)
    assert unpack_from("<I", before, wallet) == (897_400,)
    after = bytearray(before)
    for offset, value in ((wallet, GOLD), (expense, EXPENSES)):
        raw = pack("<I", value)
        ct.memmove(pointer + offset, raw, len(raw))
        after[offset:offset + len(raw)] = raw
    assert bytes(after) == ct.string_at(pointer, size)
    base.save(FIXTURE, dict(frame=FRAME, owner=owner, only_supplied_words=["company cash", "regional expenses"],
        initial_gold=897_400, supplied_gold=GOLD, supplied_expenses=EXPENSES, fleet_fixture_prerequisites=True,
        original_save_persisted=False, controlled_RAM_before_sha256=native.digest(before),
        controlled_RAM_after_sha256=native.digest(after), changes=[dict(offset=offset,
            before=before[offset:offset + 4].hex(), after=after[offset:offset + 4].hex()) for offset in (wallet, expense)]))


def main():
    release = base.load(current.RELEASE)
    assert release["candidate_sha256"] == base.digest(current.ROM)
    assert release["registry_sha256"] == base.digest(base.REGISTRY)
    assert release["clean_input_sha256"] == base.digest(native.CLEAN)
    clean, image = map(base.NdsImage.open, (native.CLEAN, current.ROM))
    original, arm = (rom.read_file(current.ARM) for rom in (clean, image))
    assert native.digest(arm) == release["target_ARM9_sha256"]
    assert all(original[start:end] == arm[start:end] for start, end in SPANS)
    assert not (ROOT / CASE).exists()
    script = checked_text(getsource(playback.main), {
        '    installed = []': "    argv += ['--dump-capture-ram']\n    installed = []",
        '                    trace.header[0] += 1\n                    advance()':
            '                    if trace.header[0] == FRAME:\n'
            '                        supply_shortfall(core, arm)\n'
            '                    trace.header[0] += 1\n                    advance()',
    })
    scope = vars(playback) | globals() | dict(parent=current, observer=trace.scoped_observer,
        get_schedule=SCHEDULE, FOCUS=set(range(3668)), arm=arm)
    exec(compile(script, __file__ + "::focused-fleet-debt", "exec"), scope)
    scope["main"](CASE)
    capture, terminal = ROOT / CASE / "capture/capture_report.json", ROOT / CASE / "terminal.json"
    result = base.load(terminal)
    result.update(focused_finance_fixture=True, observation_is_ordinary_gameplay=False,
        finance_fixture=dict(path=str(FIXTURE), sha256=base.digest(FIXTURE)),
        available_capture_ram=base.load(capture)["read_only_capture_RAM_snapshots"])
    base.save(terminal, result)


if __name__ == "__main__":
    main()
