"""Follow Fleet Info's original company catalogue through both order writers."""

from collections import Counter
from pathlib import Path
from struct import unpack_from

from unicorn import UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2

from scripts import reconcile_fleet_destination_inputs_20261124 as upstream
from scripts.reconcile_fleet_destination_writers_20261123 import BASE, FLEET_STRIDE, WRITER, code_at, references
from scripts.stage_cartridge_title_20261123 import CLEAN, REGISTRY, NdsImage, digest, read, reference, sha256, write
from scripts.verify_personal_gameplay_v841 import get_machine


PACKAGE = Path("releases/all_routes_editorial_20261124_guild_trade_numerals_candidate")
RELEASE = PACKAGE / "verification/registered_release_verification.json"
OUT = upstream.OUT.with_name("fleet_headquarters_current_20261124.json")
SAVES = OUT.with_name("fleet_save_backup_audit_20261124.json")
PORTS = OUT.with_name("fleet_port_origins_20261124.json")
ARM = "/__arm9__.bin"
COMPANY_COUNT, COMPANY_STRIDE, HQ = 20, 76, 11
CATALOG, ROW_STRIDE = 0x0211BC70, 68
INITIALIZER, GETTER = 0x020CD488, 0x0203CD24
WRAPPERS = {0x0203593C: (6, 0x02035960, 0x020359A4),
            0x020359B0: (3, 0x020359D4, 0x02035A18)}
SPANS = (
    (0x020352CC, 0x02035370), (0x0203593C, 0x02035A30),
    (0x0203A304, 0x0203A374), (GETTER, GETTER + 8), (0x0203D030, 0x0203D060),
    (0x020CB160, 0x020CB18C), (0x020CB1A8, 0x020CB1B4),
    (INITIALIZER, 0x020CD550), (0x02137218, 0x02137260),
)


def startup_companies(cpu, call, company_root, catalogue):
    checked = []
    for index in range(COMPANY_COUNT):
        company = company_root + COMPANY_STRIDE * index
        original = bytes(cpu.mem_read(company, COMPANY_STRIDE))
        assert unpack_from("<I", original)[0] == 0x02137240
        assert call(GETTER - BASE, company) == original[HQ]
        stock_hq = catalogue[ROW_STRIDE * index + 6]
        assert 0 <= stock_hq < 90 and 0 <= original[HQ] < 90
        # Force a different input to distinguish a real initialization from retention.
        cpu.mem_write(company + HQ, b"\xff")
        call(INITIALIZER - BASE, company)
        assert call(GETTER - BASE, company) == stock_hq
        cpu.mem_write(company, original)
        checked.append(dict(company_index=index, address=company, stock_address=CATALOG + ROW_STRIDE * index + 6,
                            stock_port=stock_hq, initialized_Lil_startup_port=original[HQ]))
    assert all(row["stock_port"] == row["initialized_Lil_startup_port"] for row in checked)
    first_failure = company_root + COMPANY_COUNT * COMPANY_STRIDE
    vtable, = unpack_from("<I", cpu.mem_read(first_failure, 4))
    assert vtable == 0x02137218
    assert unpack_from("<I", cpu.mem_read(vtable + 20, 4))[0] == 0x0203A304
    assert call(0x3A348, first_failure) == 0 and call(0x3A348, first_failure + 8) == 1
    return checked, dict(address=first_failure, vtable=vtable, object_stride=8, initializer=0x0203A304)


def wrapper_cases(cpu, call, fleet, company):
    original = bytes(cpu.mem_read(fleet, FLEET_STRIDE))
    original_hq = bytes(cpu.mem_read(company + HQ, 1))
    selected_company, writes = [], []

    def record_getter(u, pc, size, data):
        selected_company.append(u.reg_read(UC_ARM_REG_R0))

    def record_writer(u, pc, size, data):
        writes.append(tuple(u.reg_read(reg) for reg in (UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2)))

    hooks = (cpu.hook_add(UC_HOOK_CODE, record_getter, begin=GETTER, end=GETTER),
             cpu.hook_add(UC_HOOK_CODE, record_writer, begin=WRITER, end=WRITER))

    def run(start, order, headquarters, dock):
        selected_company.clear()
        writes.clear()
        prepared = bytearray(original)
        prepared[0x3C] = dock
        cpu.mem_write(fleet, bytes(prepared))
        cpu.mem_write(company + HQ, bytes((headquarters,)))
        call(start - BASE, fleet)
        assert selected_company == [company]
        if writes:
            (target, kind, destination), = writes
            assert target == fleet and kind == order and 0 <= destination < 256
            prepared[0x3E:0x40] = bytes((kind, destination))
        assert bytes(cpu.mem_read(fleet, FLEET_STRIDE)) == bytes(prepared)
        return writes[0][2] if writes else None

    direct, sentinel = [], []
    try:
        for start, (order, direct_writer, fallback_writer) in WRAPPERS.items():
            for headquarters in range(256):
                if headquarters == 115:
                    continue
                assert run(start, order, headquarters, original[0x3C]) == headquarters
            direct.append(dict(entry=start, writer_call=direct_writer, order=order, byte_cases=255,
                               values_passed_unchanged=[[0, 114], [116, 255]]))
            destinations = {dock: run(start, order, 115, dock) for dock in range(116)}
            assert all(value is None or 0 <= value < 90 for value in destinations.values())
            sentinel.append(dict(entry=start, writer_call=fallback_writer, order=order, headquarters=115,
                                 selected_destination_or_no_write_by_dock=destinations))
    finally:
        for hook in hooks:
            cpu.hook_del(hook)
        cpu.mem_write(company + HQ, original_hq)
        cpu.mem_write(fleet, original)
    return direct, sentinel


def main():
    release, saves, ports = map(read, (RELEASE, SAVES, PORTS))
    startup_path = Path(release["own_registered_startup"])
    startup = read(startup_path)
    assert digest(REGISTRY) == release["registry_sha256"] and digest(CLEAN) == release["clean_input_sha256"]
    assert digest(release["candidate"]) == release["candidate_sha256"] == startup["candidate_sha256"]
    assert startup["cold_boot"] and not startup["savestate"] and startup["actual_captain_getter"] == 3
    snapshot = startup["read_only_snapshot"]
    raw = Path(snapshot["path"]).read_bytes()
    assert snapshot["read_only_export"] and len(raw) == 0x400000 and sha256(raw).hexdigest() == snapshot["sha256"]
    clean, current = map(NdsImage.open, (CLEAN, release["candidate"]))
    jp, en = (image.read_file(ARM) for image in (clean, current))
    assert sha256(en).hexdigest() == release["target_ARM9_sha256"]
    current_references = references(current)
    assert references(clean) == current_references and len(current_references[WRITER]["aligned_ARM_BL"]) == 27
    assert upstream.wrapper_calls(clean) == upstream.wrapper_calls(current)

    code = []
    for start, end in SPANS:
        exact = code_at(en, start, end)
        assert exact == code_at(jp, start, end) == code_at(raw, start, end)
        code.append(dict(start=start, end=end, exact_hex=exact.hex()))
    assert unpack_from("<I", en, 0x020CD54C - BASE)[0] == CATALOG
    assert unpack_from("<I", en, 0x02137254 - BASE)[0] == INITIALIZER
    catalogue = code_at(en, CATALOG, CATALOG + COMPANY_COUNT * ROW_STRIDE)
    assert catalogue == code_at(jp, CATALOG, CATALOG + len(catalogue)) == code_at(raw, CATALOG, CATALOG + len(catalogue))
    prior_spans = [row for row in ports["clean_current_and_resident_code"]
                   if row["start"] in (0x020340A8, 0x0203A5F8, 0x0203A8B0)]
    assert len(prior_spans) == 3
    for row in prior_spans:
        assert code_at(en, row["start"], row["end"]) == code_at(jp, row["start"], row["end"]) == bytes.fromhex(row["exact_hex"])
    for row in saves["exact_source_and_current_restore_spans"]:
        stored = code_at(en, row["start"], row["end"])
        assert stored == code_at(jp, row["start"], row["end"]) and sha256(stored).hexdigest() == row["exact_sha256"]
    assert saves["slot_states"]["valid"] == 125 and not saves["special_inputs"]

    cpu, call = get_machine(en, raw)
    assert call(0x7F244) == 3
    company_root, fleet_root = call(0xCB160) + 4, call(0xCB1A8) + 4
    companies, adjacent_failure = startup_companies(cpu, call, company_root, catalogue)
    owners = []
    for index in range(64):
        fleet = fleet_root + index * FLEET_STRIDE
        owner = call(0x352F4, fleet)
        if owner:
            company_index, remainder = divmod(owner - company_root, COMPANY_STRIDE)
            assert remainder == 0 and 0 <= company_index < COMPANY_COUNT
            owners.append(dict(fleet_index=index, fleet_address=fleet, company_index=company_index, company_address=owner))
    example = next(row for row in owners if row["fleet_index"] == 1)
    assert example["company_index"] == 2
    byte_cases, sentinel_cases = wrapper_cases(cpu, call, example["fleet_address"], example["company_address"])
    write(OUT, dict(candidate_sha256=release["candidate_sha256"], registry_sha256=release["registry_sha256"],
        exact_clean_installed_and_resident_code=code, startup_snapshot=snapshot,
        original_catalogue=dict(start=CATALOG, row_bytes=ROW_STRIDE, rows=COMPANY_COUNT, headquarters_offset=6,
                                sha256=sha256(catalogue).hexdigest(), cases=companies),
        adjacent_failure_object=adjacent_failure, aligned_destination_writer_calls=27, startup_fleet_owner_cases=64,
        fleets_by_resolved_company=dict(sorted(Counter(row["company_index"] for row in owners).items())),
        tested_fleet=example, direct_headquarters_byte_cases=byte_cases, no_headquarters_sentinel_cases=sentinel_cases,
        unchanged_reassignment_spans=prior_spans, unchanged_restore_spans=len(saves["exact_source_and_current_restore_spans"]),
        proof_sources=list(map(reference, (RELEASE, startup_path, upstream.OUT, PORTS, SAVES))),
        limits="Offline copied-RAM runs. Every resolved owner at the Lil startup hold is an ordinary company row. "
               "Unobserved indirect runtime inputs and sessions remain open.",
        new_gameplay=False, ROM_changed=False, new_editorial_credit=0))
    print("Verified 20 stock company rows, 64 fleet owner lookups, 510 direct headquarters cases and 232 fallback cases.")


if __name__ == "__main__":
    main()
