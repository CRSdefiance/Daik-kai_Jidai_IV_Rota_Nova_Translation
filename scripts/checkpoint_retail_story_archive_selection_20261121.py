"""Check whether the original scene loader falls back to the alternate story archive."""

from pathlib import Path
from struct import pack, unpack_from

from unicorn import UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_LR, UC_ARM_REG_PC, UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_SP

from scripts import checkpoint_shared_treasure_map_offsets_20261121 as bound
from scripts import load_wedding_block_v676 as loader
from scripts import research_archive_callers_v264 as previous
from scripts.checkpoint_pending_shared_native_20261115 import components
from scripts.probe_button_prompt_native import STACK, STOP, call, machine


base, native, current = bound.base, bound.native, bound.current
OUTPUT = bound.OUTPUT.with_name("retail_story_archive_selection_20261121_v1.json")
RETAIL_EXIT = bound.OUTPUT.with_name("retail_exit_scope_20261119_v1.json")
EARLIER_OPEN = previous.ROOT / "proof.json"
ROUTE_ADDRESS = 0x022796B0
CAPTAIN_ARCHIVE_TABLE = 0x02134580
BLOCKS = (0, 0, 0, 164)
FAILED_OPEN_LOOP = (0x020D0488, 0x020D048C, 0x020D0490)


def unavailable_primary(rom, arm, route, index):
    """Withhold one production archive at SDK open and leave any other path available."""
    cpu = machine(arm)
    seen, loop = [], []
    stock = f"/data/SC{route}.DK4"
    paths = {name.casefold(): name for name in rom.path_map()}
    assert stock.casefold() in paths and f"/testdata/sc{route}.dk4" in paths
    obj = loader.OBJECT
    cpu.mem_write(ROUTE_ADDRESS, pack("<I", route))
    cpu.mem_write(obj - 16, b"\xA5" * (0x2420 + 32))

    def intercept(uc, pc, _size, _data):
        if pc in FAILED_OPEN_LOOP:
            loop.append(pc)
            if len(loop) == 48:
                uc.emu_stop()
        if pc not in (loader.OPEN, loader.READ, loader.SEEK, loader.CLOSE):
            return
        assert pc == loader.OPEN
        address = uc.reg_read(UC_ARM_REG_R1)
        filename = bytes(uc.mem_read(address, 32)).split(b"\0", 1)[0].decode("ascii")
        requested = "/" + filename.replace("\\", "/").lstrip("/")
        available = requested.casefold() in paths and requested.casefold() != stock.casefold()
        seen.append(dict(requested=requested, would_be_available=available))
        # The expected trace fails closed. An unexpected fallback invalidates this proof.
        assert not available and requested.casefold() == stock.casefold()
        uc.reg_write(UC_ARM_REG_R0, 0)
        uc.reg_write(UC_ARM_REG_PC, uc.reg_read(UC_ARM_REG_LR))

    hook = cpu.hook_add(UC_HOOK_CODE, intercept)
    try:
        call(cpu, 0x24214, (obj,))
        before = bytes(cpu.mem_read(obj - 16, 0x2420 + 32))
        for reg, value in ((UC_ARM_REG_R0, obj), (UC_ARM_REG_R1, index), (UC_ARM_REG_SP, STACK), (UC_ARM_REG_LR, STOP)):
            cpu.reg_write(reg, value)
        cpu.emu_start(0x02024134, STOP, count=1000)
        assert len(seen) == 1 and tuple(loop) == FAILED_OPEN_LOOP * 16
        assert cpu.reg_read(UC_ARM_REG_PC) == FAILED_OPEN_LOOP[-1] and cpu.reg_read(UC_ARM_REG_R0) == 0
        assert bytes(cpu.mem_read(obj - 16, len(before))) == before
    finally:
        cpu.hook_del(hook)
    return dict(captain=route, block=index, file_requests=seen, terminal_loop=FAILED_OPEN_LOOP,
        repeated_loop_iterations=16, cache_and_canaries_exact=True)


def verify(rom, clean_arm, historical):
    arm = rom.read_file("/__arm9__.bin")
    ranges = [(0x24134, 0x241CC), (0x24214, 0x24230), (0xD0398, 0xD0520), (0xD1EE0, 0xD2128), (0x134530, 0x134590)]
    assert all(arm[lo:hi] == clean_arm[lo:hi] for lo, hi in ranges)
    assert unpack_from("<I", arm, 0x241C8) == (CAPTAIN_ARCHIVE_TABLE,)
    assert unpack_from("<I", arm, 0x241C4) == (ROUTE_ADDRESS - 0x48,)
    cases = []
    for route, index in enumerate(BLOCKS):
        alternative = f"/testdata/SC{route}.DK4"
        result = loader.load(rom, route, index)
        filename, = [e for e in result["native_file_operations"] if e["operation"] == "open"]
        assert filename["path"] == historical[route]["actual_path"] == f"/data/SC{route}.DK4"
        assert historical[route]["SDK_events"][0]["requested_filename"] == filename["requested"]
        assert result["full_constructor_and_block_loader_return_ABI_and_guards_exact"]
        result.pop("executed_addresses")
        cases.append(dict(source=filename["path"], test_archive=alternative,
            test_archive_sha256=native.digest(rom.read_file(alternative)), full_original_load=result,
            missing_production_archive=unavailable_primary(rom, arm, route, index)))
    modules = []
    for name, start, data in components(rom.rom):
        hits = {encoding: data.lower().count("testdata".encode(encoding)) for encoding in ("ascii", "utf-16-le")}
        assert not any(hits.values())
        modules.append(dict(name=name, start=start, bytes=len(data), sha256=native.digest(data), exact_name_matches=hits))
    return dict(cases=cases, executable_name_scan=modules)


def main():
    assert not OUTPUT.exists()
    release = base.load(current.RELEASE)
    assert release["candidate_sha256"] == base.digest(current.ROM) == base.load(bound.OUTPUT)["candidate_sha256"]
    assert release["clean_input_sha256"] == base.digest(native.CLEAN)
    with current.mapped(base.LEDGER) as ledger:
        assert current.value(ledger, "current_integrated_candidate", 1)["sha256"] == release["candidate_sha256"]
    assert release["registry_sha256"] == base.digest(base.REGISTRY)
    earlier = base.load(EARLIER_OPEN)
    routes = {r["supplied_route"]: r for r in earlier["native_filename_selection_cases"] if r["parent_start"] == 0x02024134}
    assert set(routes) == set(range(4))
    clean, active = map(base.NdsImage.open, (native.CLEAN, current.ROM))
    ja = clean.read_file("/__arm9__.bin")
    evidence = {name: verify(rom, ja, routes) for name, rom in (("clean", clean), ("registered", active))}
    for a, b in zip(evidence["clean"]["cases"], evidence["registered"]["cases"], strict=True):
        assert a["test_archive_sha256"] == b["test_archive_sha256"]
    alt_maria = native.IlnkContainer.parse(active.read_file("/testdata/SC3.DK4")).blocks[164]
    assert alt_maria[:4] == b"CS\x01\x01" and unpack_from("<H", alt_maria, 4) == (750,)
    assert len(alt_maria) == 760 and alt_maria[-2:] == b"\0\0"
    base.save(OUTPUT, dict(candidate_sha256=release["candidate_sha256"], clean_sha256=release["clean_input_sha256"],
        source_selector=0x02024134, native_path_table=CAPTAIN_ARCHIVE_TABLE, versions=evidence,
        alternate_Maria_length_word=dict(file="/testdata/SC3.DK4", block=164, offset=4, value=750,
            block_sha256=native.digest(alt_maria), passed_in_cache_by_earlier_isolated_test=True,
            used_as_fallback_by_retail_chapter_loader=False),
        previous_native_cases=str(EARLIER_OPEN), earlier_alternate_cache_receipt=str(RETAIL_EXIT),
        scope="SDK file I/O bridged for the original chapter loader. Computed or external callers elsewhere remain open.",
        new_emulator_runs=0, new_dialogue_credit=0, raw_shared_rows_still_open=276,
        evidence={str(p): base.digest(p) for p in (EARLIER_OPEN, RETAIL_EXIT, current.RELEASE, bound.OUTPUT, Path(__file__))}))
    print("Verified eight full retail chapter loads and eight missing-file cases. The loader never falls back to /testdata.")


if __name__ == "__main__":
    main()
