"""Find the native producers of two preserved Japanese sailing hints."""

from itertools import pairwise
from pathlib import Path
from struct import iter_unpack, pack, unpack_from

from ndspy.code import MainCodeFile
from unicorn import UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_LR, UC_ARM_REG_PC, UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2
from unicorn.arm_const import UC_ARM_REG_SP

from scripts.inventory_arm9_text import loaded_components
from scripts.inventory_native_common_calls import direct_bl_target
from scripts.native_call_abi_v764 import STACK, call
from scripts.stage_cartridge_title_20261123 import CLEAN, REGISTRY, NdsImage, digest, read, reference, sha256, write
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_stock_encounter_names_20261121 import read_ram


BASE = 0x02000000
ARM = "/__arm9__.bin"
RELEASES = Path("releases")
RELEASE = RELEASES / "all_routes_editorial_20261123_hodram_elegy_candidate/verification/registered_release_verification.json"
PRIOR = RELEASES / "all_routes_editorial_20261118_sailing_mode_prose_candidate/verification"
OUT = Path("translations/editorial_checkpoints/shared_display_20261123/queued_sailing_hints_20261123.json")
QUEUE_COUNT, QUEUE_SLOT = 0x0217035C, 0x021703F4
ENQUEUE, READER, TRANSFER = 0x02070950, 0x020CDE20, 0x020CE238
READ_CALL, TRANSFER_CALL = 0x020CE6D0, 0x020CE6F8
GMONS, OCETC = 0x0207C668, 0x0207BB98
FONT_OVERLAY, SDK_OPEN = 0x01FFB4B0, 0x020DED50
SCRATCH_IMAGE = 0x022E1794
# Start on the caller's own type assignment and execute the remaining argument setup.
DIRECT = (
    (0x0200B834, 0x0200B838, 4), (0x0200B844, 0x0200B848, 3),
    (0x0200E6E4, 0x0200E6F0, 5), (0x0200E700, 0x0200E70C, 8),
    (0x0200E71C, 0x0200E728, 7), (0x0200E738, 0x0200E744, 6),
    (0x02010DDC, 0x02010DE4, 4), (0x02010DEC, 0x02010DF4, 3),
    (0x0206E170, 0x0206E174, 0), (0x0207A44C, 0x0207A450, 0),
    (0x0207AAD0, 0x0207AAD8, 0),
)
WRAPPERS = ((GMONS, 1, 0x0207C680), (OCETC, 2, 0x0207BBB0))
LABELS = {
    10: (0x0215F72C, 0x020CE210, 0x020CE070, "Search: press A. Finds may include supplies or items. Failure adds three fatigue. Sailors can desert or be attacked during a search."),
    11: (0x0215F870, 0x020CE218, 0x020CE090, "Declare War: select a town or fleet to fight. This starts war with its faction and lowers goodwill sharply. Allied fleets are excluded."),
}


def code(arm, lo, hi):
    return arm[lo - BASE:hi - BASE]


def word(arm, pc):
    return unpack_from("<I", arm, pc - BASE)[0]


def hash_bytes(data):
    return sha256(data).hexdigest()


def referenced_routines(image):
    routines = (ENQUEUE, READER, TRANSFER, GMONS, OCETC)
    branches = {p: [] for p in routines}
    thumb = {p: [] for p in routines}
    references = {p: [] for p in (*routines, QUEUE_COUNT, QUEUE_SLOT, QUEUE_SLOT + 4, QUEUE_SLOT + 8)}
    for component, base, raw in loaded_components(image):
        for i, (value,) in enumerate(iter_unpack("<I", raw[:len(raw) // 4 * 4])):
            pc = base + 4 * i
            if value in references:
                references[value].append([component, pc])
            if value & 0x0E000000 == 0x0A000000:
                target = direct_bl_target(value | 0x01000000, pc)
                if target in branches:
                    branches[target].append([component, pc, value >> 24])
        halfwords = (value for (value,) in iter_unpack("<H", raw[:len(raw) // 2 * 2]))
        for i, (first, second) in enumerate(pairwise(halfwords)):
            if first & 0xF800 == 0xF000 and second & 0xF801 == 0xE800:
                offset = ((first & 0x7FF) << 12) | ((second & 0x7FF) << 1)
                if offset & 0x400000:
                    offset -= 0x800000
                target = (base + i * 2 + 4 + offset) & ~3
                if target in thumb:
                    thumb[target].append([component, base+i*2])
    assert branches[ENQUEUE] == [["arm9_section_0", p, 0xEB] for _, p, _ in DIRECT]
    assert branches[READER] == [["arm9_section_0", READ_CALL, 0xEB]]
    assert branches[TRANSFER] == [["arm9_section_0", TRANSFER_CALL, 0xEB]]
    assert branches[GMONS] == [["arm9_section_0", p, 0xEB] for p in
                               (0x0202E958, 0x02070FEC, 0x0207BACC, 0x0207BE44)]
    assert branches[OCETC] == [["arm9_section_0", p, 0xEB] for p in
                               (0x0207A658, 0x0207AB28, 0x0207AC74, 0x0207ACE0,
                                0x0207AD24, 0x0207AD7C, 0x0207ADC0, 0x0207AE04)]
    assert references[ENQUEUE] == [["arm9_section_0", p] for p in (0x0207BBB0, 0x0207C680)]
    assert all(not references[p] for p in (READER, TRANSFER, GMONS, OCETC))
    assert references[QUEUE_SLOT] == [["arm9_section_0", p] for p in (0x0207098C, 0x020CE220)]
    assert references[QUEUE_SLOT + 4] == [["arm9_section_0", p] for p in (0x02070990, 0x020CE1E0, 0x020CE4B4)]
    assert references[QUEUE_SLOT + 8] == [["arm9_section_0", p] for p in (0x02070994, 0x020CE1E8, 0x020CE4BC)]
    assert not any(thumb.values())
    return dict(aligned_arm_branches=branches, thumb_blx_immediate=thumb, aligned_literals=references)


def produce(cpu, arm, original_ram):
    reports = []
    addr = QUEUE_SLOT - BASE
    assert word(arm, 0x02070988) == QUEUE_COUNT
    for start, site, kind in DIRECT:
        assert word(arm, start) == (0xE3A01000 | kind)
        cpu.mem_write(QUEUE_COUNT, pack("<H", 2))
        cpu.mem_write(QUEUE_SLOT, bytes([0xCC]) * 48)
        # The instruction after BL is the return sentinel for this test.
        call_fragment(cpu, start, site + 4)
        values = unpack_from("<12I", bytes(cpu.mem_read(QUEUE_SLOT, 48)))
        assert values[7] == kind and values[:6] == (0xCCCCCCCC,) * 6 and values[9:] == (0xCCCCCCCC,) * 3
        assert bytes(cpu.mem_read(QUEUE_COUNT, 2)) == pack("<H", 3)
        reports.append(dict(start=start, writer_call=site, exact_caller_hex=code(arm, start, site+4).hex(),
                            written_kind=values[7]))
    for entry, kind, literal in WRAPPERS:
        assert word(arm, literal) == ENQUEUE
        cpu.mem_write(QUEUE_COUNT, bytes(2))
        call(cpu, entry - BASE, (7, 3, 9))
        queue = unpack_from("<3I", bytes(cpu.mem_read(QUEUE_SLOT, 12)))
        assert queue == (0x2F000, kind, 7 if entry == GMONS else 3)
        assert bytes(cpu.mem_read(QUEUE_COUNT, 2)) == pack("<H", 1)
        reports.append(dict(start=entry, writer_literal=literal, queue_words=queue, written_kind=kind))
    assert sorted({row["written_kind"] for row in reports}) == list(range(9))
    cpu.mem_write(QUEUE_COUNT, original_ram[QUEUE_COUNT - BASE:QUEUE_COUNT - BASE + 2])
    cpu.mem_write(QUEUE_SLOT, original_ram[addr:addr + 48])
    assert bytes(cpu.mem_read(BASE, len(original_ram))) == original_ram
    return reports


def call_fragment(cpu, start, stop, first_argument=0x1800, stack_frame=0):
    for reg, value in ((UC_ARM_REG_R0, first_argument), (UC_ARM_REG_R1, 0xFFFFFFFF),
                       (UC_ARM_REG_R2, 13), (UC_ARM_REG_SP, STACK)):
        cpu.reg_write(reg, value)
    cpu.emu_start(start, stop, count=100)
    assert cpu.reg_read(UC_ARM_REG_PC) == stop and cpu.reg_read(UC_ARM_REG_SP) == STACK - stack_frame


def source_fields(cpu, clean, arm, raw):
    results = []
    for kind, (pointer, literal, font_call, meaning) in LABELS.items():
        assert word(arm, literal) == pointer
        assert direct_bl_target(word(arm, font_call), font_call) == FONT_OVERLAY
        at = pointer - BASE
        text = arm[at:].split(b"\0", 1)[0]
        assert len(text) > 240 and clean[at:at+len(text)+1] == raw[at:at+len(text)+1] == text + b"\0"
        cpu.mem_write(QUEUE_SLOT, pack("<3I", 0, kind, 0))
        observed = []

        def opened(core, _pc, _size, _data):
            name = bytes(core.mem_read(core.reg_read(UC_ARM_REG_R1), 64)).split(b"\0", 1)[0]
            observed.append(name.decode("ascii"))
            core.reg_write(UC_ARM_REG_R0, 1)
            core.reg_write(UC_ARM_REG_PC, core.reg_read(UC_ARM_REG_LR))

        hook = cpu.hook_add(UC_HOOK_CODE, opened, begin=SDK_OPEN, end=SDK_OPEN)
        try:
            call_fragment(cpu, READER, font_call, first_argument=0, stack_frame=0x90)
        finally:
            cpu.hook_del(hook)
        filename, = observed
        p, color, output = (cpu.reg_read(reg) for reg in (UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2))
        assert (p, color, output) == (pointer, 15, SCRATCH_IMAGE)
        assert filename.lstrip("/\\").replace("\\", "/").upper() == "GRP/DSCHR.DK4"
        results.append(dict(forced_kind=kind, literal=literal, painter_call=font_call, callee=FONT_OVERLAY,
            source_reference=dict(path=ARM, address=pointer, exact_hex=(text+b"\0").hex()),
            installed_reference=dict(path=ARM, address=pointer, exact_hex=(text+b"\0").hex()),
            source_Japanese=text.decode("cp932"), source_meaning=meaning, verified_file_selector=filename,
            produced_arguments=[p, color, output], generated_pixels_or_gameplay_verified_here=False))
    cpu.mem_write(QUEUE_SLOT, raw[QUEUE_SLOT-BASE:QUEUE_SLOT-BASE+12])
    assert bytes(cpu.mem_read(BASE, len(raw))) == raw
    return results


def bind_current_panels(clean, arm, raw, candidate_sha256):
    proof = read(PRIOR / "registered_review.json")
    receipt = read(PRIOR / "registered_release_verification.json")
    assert digest(receipt["candidate"]) == receipt["candidate_sha256"] == proof["candidate_sha256"]
    previous = NdsImage.open(receipt["candidate"]).read_file(ARM)
    preparation = read("work/analysis/sailing_panels_v217/preparation.json")
    entry = preparation["entry"] - BASE
    N = preparation["helper_bytes"]
    assert raw[entry:entry+N] == staged_helper(previous, preparation) == staged_helper(arm, preparation)
    active_spans = ((0x0206ED2C, 0x0206F428), (0x020702D0, 0x02070360))
    assert all(code(previous, a, b) == code(arm, a, b) for a,b in active_spans)
    rows = []
    for row in proof["records"]:
        installed = row["registered_reference"]
        offset, p, n = (installed[key] for key in ("offset", "runtime_pointer", "bytes"))
        source = row["source_reference"]
        expected = bytes.fromhex(source["exact_clean_hex"])
        assert code(clean, source["address"], source["address"] + len(expected)) == expected
        assert raw[p-BASE:p-BASE+n] == arm[offset:offset+n] == previous[offset:offset+n]
        assert hash_bytes(arm[offset:offset+n]) == installed["packed_sha256"]
        assert all(row["review"].values())
        rows.append(dict(heading=row["heading"], english=row["english"], source=source,
            current_packed_panel=installed | dict(candidate_sha256=candidate_sha256),
            justified_retention=row["localization_note"],
            earlier_replay_holds=[r for r in proof["actual_mode_panels"]["native_display_matches"] if r["id"] == row["id"]],
            review=row["review"]))
    return dict(earlier_registered_review=reference(PRIOR / "registered_review.json"), native_active_panels=rows,
                unchanged_active_caller_spans=[dict(start=a, end=b, sha256=hash_bytes(code(arm,a,b))) for a,b in active_spans],
                unchanged_deployed_helper_sha256=hash_bytes(raw[entry:entry+N]))


def staged_helper(arm, preparation):
    start = preparation["staging_span"][0] + preparation["entry"] - preparation["pool_span"][0]
    n = preparation["helper_bytes"]
    for s in MainCodeFile(arm, BASE).sections:
        i = start - s.ramAddress
        if 0 <= i and i + n <= len(s.data):
            return bytes(s.data[i:i+n])
    raise AssertionError("Missing staged sailing panel helper")


def main():
    release = read(RELEASE)
    assert digest(release["candidate"]) == release["candidate_sha256"]
    assert digest(CLEAN) == release["clean_input_sha256"] and digest(REGISTRY) == release["registry_sha256"]
    clean, current = map(NdsImage.open, (CLEAN, release["candidate"]))
    original, arm = (image.read_file(ARM) for image in (clean, current))
    assert hash_bytes(arm) == release["target_ARM9_sha256"]
    refs = referenced_routines(current)
    assert refs == referenced_routines(clean)
    startup = Path(release["own_registered_startup"])
    assert digest(startup) == release["own_registered_startup_sha256"]
    snapshot = read(startup)["read_only_snapshot"]
    raw = read_ram(snapshot)
    spans = [(ENQUEUE, 0x02070998), (READER, 0x020CE4D0), (0x020CE6A4, 0x020CE74C),
             *[(start, end+4) for start, end, _ in DIRECT], *[(start, literal+4) for start, _, literal in WRAPPERS]]
    exact = []
    for a, b in spans:
        blob = code(arm,a,b)
        assert blob == code(original,a,b) == code(raw,a,b)
        exact.append(dict(start=a,end=b,sha256=hash_bytes(blob),exact_hex=blob.hex()))
    cpu, _ = get_machine(arm, raw)
    supplied = produce(cpu, arm, raw)
    fields = source_fields(cpu, original, arm, raw)
    active_panels = bind_current_panels(original, arm, raw, release["candidate_sha256"])
    write(OUT, dict(candidate_sha256=release["candidate_sha256"], registered_release=reference(RELEASE),
        startup_snapshot=snapshot, exact_source_current_and_loaded_spans=exact, scoped_reference_census=refs,
        producer_executions=supplied, admitted_kinds=sorted({p["written_kind"] for p in supplied}),
        archived_language_fields=fields, current_visible_path=active_panels,
        scope="The verified stock writer, immediate ARM and Thumb branches and its two indirect wrappers. Direct queue writes through pointers synthesized at runtime would require independent evidence.",
        new_gameplay=False, ROM_changed=False, new_credit=0))
    print("Eleven direct and two wrapper producers wrote kinds 0-8. Supplied kinds 10/11 reach the archived Japanese templates.")


if __name__ == "__main__":
    main()
