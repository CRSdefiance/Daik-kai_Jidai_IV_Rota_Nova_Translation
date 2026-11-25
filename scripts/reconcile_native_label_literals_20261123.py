"""Reconcile the Japanese literals near the four tested native text-call forms."""

import json
from pathlib import Path
from struct import unpack_from

from dk4tool.rom.nds import NdsImage
from scripts.inventory_arm9_text import japanese_char
from scripts.inventory_native_common_calls import direct_bl_target
from scripts.reconcile_editorial_acceptance_20261123 import ARM, BASE, OUT, digest, read, reference


RELEASE = Path("releases/all_routes_editorial_20261123_supply_ratio_hint_candidate/verification/registered_release_verification.json")
REPORT = OUT.with_name("native_label_literal_calls_20261123.json")
CONSUMERS = {0x020D5404: {1}, 0x020D5200: {1}, 0x020D4A7C: {2, 3}, 0x020D4988: {1}}
WINDOW = 24
SCAN_END = 0x110000
EXPECTED = {
    0x021370F8: ("目標街：%s", 0x02037660, 0x02037668, 0x020D5200, "editorial_pirate_and_legacy_fleet_20261123.md"),
    0x02137118: ("収入額%8lu支出額%8lu投資額%8lu", 0x02038DA4, 0x02038DA8, 0x020D5200, "editorial_pirate_and_legacy_fleet_20261123.md"),
    0x0213795C: ("友好度", 0x0203D7AC, 0x0203D7B4, 0x020D5404, "editorial_faction_information_visibility_20261115.md"),
}


def scans(arm):
    def word(at):
        return unpack_from("<I", arm, at)[0]

    found = {}
    for pc in range(WINDOW, SCAN_END, 4):
        called = direct_bl_target(word(pc), BASE + pc)
        if called not in CONSUMERS:
            continue
        for load in range(pc - WINDOW, pc, 4):
            ins = word(load)
            if ins & 0x0F7F0000 != 0x051F0000 or (ins >> 12) & 15 not in CONSUMERS[called]:
                continue
            displacement = ins & 0xFFF
            literal = load + 8 + (displacement if ins & 0x800000 else -displacement)
            address = word(literal)
            if not 0x02110000 <= address < BASE + len(arm) - 100:
                continue
            at = address - BASE
            raw, terminator, _ = arm[at:at + 100].partition(b"\0")
            if not terminator:
                continue
            try:
                text = raw.decode("cp932")
            except UnicodeError:
                continue
            if sum(map(japanese_char, text)) < 2 or not all(x.isprintable() or x in "\r\n" for x in text):
                continue
            found.setdefault(address, []).append((text, BASE + load, BASE + pc, called, raw + terminator))
    return found


def main():
    assert not REPORT.exists()
    release = read(RELEASE)
    assert digest(release["candidate"]) == release["candidate_sha256"]
    assert digest("work/clean.nds") == release["clean_input_sha256"]
    source, arm = (NdsImage.open(p).read_file(ARM) for p in ("work/clean.nds", release["candidate"]))
    found = scans(arm)
    assert set(found) == EXPECTED.keys()
    records = []
    for address, rows in sorted(found.items()):
        text, load, call, called, raw = rows[0]
        intended = EXPECTED[address]
        assert len(rows) == 1 and (text, load, call, called) == intended[:4]
        at = address - BASE
        assert raw == source[at:at + len(raw)]
        records.append(dict(source_Japanese=text, C_string_file_offset=at, exact_clean_and_installed_hex=raw.hex(),
            pointer_load=load, caller=call, consumer=called, prior_display_evidence=reference(Path("docs") / intended[-1])))
    report = dict(candidate_sha256=release["candidate_sha256"], clean_sha256=release["clean_input_sha256"],
        registered_release=reference(RELEASE), scanned_ARM9_file_offsets=[WINDOW, SCAN_END],
        direct_ARM_BL_argument_registers={f"0x{pc:08X}": sorted(regs) for pc, regs in CONSUMERS.items()},
        lookback_bytes=WINDOW, minimum_Japanese_letters=2, records=records, new_count=0,
        offline=True, indirect_tables_and_other_consumers_outside_scope=True)
    REPORT.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
    print("All three Japanese literals in the direct-call scan match previously scoped display leads.")


if __name__ == "__main__":
    main()
