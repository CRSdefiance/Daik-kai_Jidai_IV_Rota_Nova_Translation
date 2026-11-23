"""Stage the English cultural-region label used by Market Info."""

from pathlib import Path
from struct import unpack_from

from scripts import register_market_report_status_20261120 as parent
from scripts import stage_market_info_trends_20261115 as report
from scripts.stage_ruin_discovery_display_20261120 import apply_xdelta, cache_plan, make_xdelta


base = parent.base
CLEAN, ARM = report.CLEAN, report.ARM
ROOT = Path("work/market_english_region_20261120/staged_v2")
ROM, PROOF = ROOT / "Market_English_Region_RESEARCH_ONLY.nds", ROOT / "staged.json"
BASE, SLOT, SIZE = 0x02000000, 0x15C5CC, 12
FIELD, FORMAT, DRAW = 0x11F680, 0x159F7C, 0x020BEA04
CENTER = 0xBE9EC
ORIGINAL_CENTER, ENGLISH_CENTER = bytes.fromhex("241061e2"), bytes.fromhex("211061e2")
SOURCE, ENGLISH = "イギリス", "English"


def patch(clean, current):
    source = SOURCE.encode("cp932").ljust(SIZE, b"\0")
    translated = ENGLISH.encode("ascii").ljust(SIZE, b"\0")
    assert source == clean[SLOT:SLOT + SIZE] == current[SLOT:SLOT + SIZE]
    assert current[SLOT + SIZE:SLOT + SIZE + 4] == b"Dias"
    assert all(unpack_from("<I", a, FIELD) == (BASE + SLOT,) for a in (clean, current))
    assert current[0xBEE58:0xBEE5C] == clean[0xBEE58:0xBEE5C] == (BASE + FORMAT).to_bytes(4, "little")
    assert clean[FORMAT:FORMAT + 12] == b"%s" + "文化圏".encode("cp932") + bytes(4)
    assert current[FORMAT:FORMAT + 12] == b"%s Region" + bytes(3)
    for start, end in ((0xBE9B8, 0xBEA08), (0xB5188, 0xB51CC), (0xBEE88, 0xBEE90),
                       (0xCD208, 0xCD27C), (0x15EE00, 0x15EE10)):
        assert current[start:end] == clean[start:end]
    # The original six-cell Japanese suffix was centered within 108 pixels.
    # The seven-cell English suffix needs a three-pixel compensating shift.
    assert current[CENTER:CENTER + 4] == ORIGINAL_CENTER
    edited = bytearray(current)
    edited[SLOT:SLOT + SIZE] = translated
    edited[CENTER:CENTER + 4] = ENGLISH_CENTER
    target = bytes(edited)
    edited[SLOT:SLOT + SIZE] = source
    edited[CENTER:CENTER + 4] = ORIGINAL_CENTER
    assert bytes(edited) == current
    return target, dict(offset=SLOT, size=SIZE, pointer_field=FIELD, source_draw=DRAW,
        source_format="%s文化圏", current_format="%s Region", source_hex=source.hex(),
        current_hex=source.hex(), target_hex=translated.hex(), centering_instruction=BASE + CENTER,
        centering_source_hex=ORIGINAL_CENTER.hex(), centering_target_hex=ENGLISH_CENTER.hex())


def main():
    assert not ROOT.exists()
    previous = base.load(parent.RELEASE)
    assert base.digest(parent.ROM) == previous["candidate_sha256"]
    assert base.digest(CLEAN) == previous["clean_input_sha256"]
    assert base.digest(base.REGISTRY) == previous["registry_sha256"]
    clean, current = map(base.NdsImage.open, (CLEAN, parent.ROM))
    before = report.files(current)
    target, slot = patch(clean.read_file(ARM), before[ARM])
    assert cache_plan(target) == cache_plan(before[ARM])
    current.replace_file(ARM, target)
    after = report.files(current)
    assert before.keys() == after.keys() and {p for p in before if before[p] != after[p]} == {ARM}
    ROOT.mkdir()
    current.save(ROM)
    current.replace_file(ARM, before[ARM])
    assert bytes(current.rom.save()) == parent.ROM.read_bytes()
    delta, rebuilt = ROOT / "translation.xdelta", ROOT / "clean_rebuilt.nds"
    make_xdelta(CLEAN, ROM, delta)
    apply_xdelta(CLEAN, delta, rebuilt)
    assert rebuilt.read_bytes() == ROM.read_bytes()
    base.save(PROOF, dict(candidate_sha256=base.digest(ROM), parent_sha256=previous["candidate_sha256"],
        clean_input_sha256=previous["clean_input_sha256"], target_ARM9_sha256=parent.native.digest(target),
        target_COMMON_sha256=previous["target_COMMON_sha256"], clean_input_patch_sha256=base.digest(delta),
        changed_slot=slot, whole_parent_inverse=True, clean_input_patch_byte_exact=True))
    print("Staged English Region in the original Market Info text slot.")


if __name__ == "__main__":
    main()
