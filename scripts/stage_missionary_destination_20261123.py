"""Reuse the approved Missionary label in the original Fleet Info destination getter."""

from inspect import getsource
from pathlib import Path
from struct import pack, unpack_from

from scripts import reconcile_fleet_destination_name_caller_20261123 as prior
from scripts import register_london_relic_tip_20261123 as parent
from scripts.inventory_arm9_text import loaded_components
from scripts.reconcile_class_names_20261123 import word
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.stage_cartridge_title_20261123 import CLEAN, REGISTRY, NdsImage, digest, read, reference, sha256, write
from scripts.verify_assigned_fleet_detail_20261123 import format_checks
from scripts.verify_stock_encounter_names_20261121 import read_ram


ROOT = Path(".codex-release-work/missionary_destination_20261123")
ROM, STORED = ROOT / "Missionary_Destination_STAGED.nds", ROOT / "stored_proof.json"
ARM, BASE = prior.ARM, prior.BASE
GETTER, LITERAL = prior.MISSIONARY_GETTER, prior.MISSIONARY_GETTER + 8
OLD_NAME, RESIDENT_NAME = 0x02134DA0, 0x02388986
ROLE_REPORT = prior.OUT.with_name("crew_role_storage_current_20261123.json")
CLASS_REPORT = prior.OUT.with_name("native_class_names_20261123.json")
JAPANESE = "伝道師"
ENGLISH = "Missionary"
SOURCE, TARGET = JAPANESE.encode("cp932") + b"\0", ENGLISH.encode("ascii") + b"\0"


def stage():
    release = read(parent.RELEASE)
    assert digest(REGISTRY) == release["registry_sha256"] and digest(CLEAN) == release["clean_input_sha256"]
    assert digest(release["candidate"]) == release["candidate_sha256"]
    previous = Path(release["candidate"]).read_bytes()
    clean, image = map(NdsImage.open, (CLEAN, release["candidate"]))
    original, arm = (obj.read_file(ARM) for obj in (clean, image))
    assert sha256(arm).hexdigest() == release["target_ARM9_sha256"]
    old_literal, new_literal = pack("<I", OLD_NAME), pack("<I", RESIDENT_NAME)
    getter = prior.code_at(arm, GETTER, GETTER + 12)
    assert getter == prior.code_at(original, GETTER, GETTER + 12)
    assert getter == bytes.fromhex("00009fe51eff2fe1") + old_literal
    assert prior.code_at(arm, OLD_NAME, OLD_NAME + len(SOURCE)) == SOURCE
    assert prior.code_at(original, OLD_NAME, OLD_NAME + len(SOURCE)) == SOURCE
    class_proof = next(row for row in read(CLASS_REPORT)["records"] if row["getter"] == GETTER)
    assert class_proof["source_reference"] == {"address": OLD_NAME, "hex": SOURCE.hex()}
    table, = (row["address"] for row in class_proof["class_tables"])
    assert word(arm, table + 8) == word(original, table + 8) == GETTER
    assert class_proof["class_tables"][0]["rtti"] == "6CAdman"
    name_references = [(area, base + i) for area, base, data in loaded_components(image)
                       for i in range(0, len(data) & ~3, 4)
                       if data[i:i + 4] == old_literal]
    assert name_references == [("arm9_section_0", LITERAL)]
    role = next(row for row in read(ROLE_REPORT)["role_records"] if row["approved_English"] == ENGLISH)
    assert role["runtime_selected"]["string_pointer"] == RESIDENT_NAME
    assert bytes.fromhex(role["runtime_selected"]["exact_C_string_hex"]) == TARGET
    staged_pool, = [(base, data) for name, base, data in loaded_components(image) if name == "arm9_section_3"]
    assert staged_pool[1].count(TARGET) == 1
    at = staged_pool[1].index(TARGET)
    assert staged_pool[0] + at - RESIDENT_NAME == 0x1F7E0

    boot = Path(release["own_registered_startup"])
    assert digest(boot) == release["own_registered_startup_sha256"]
    startup = read(boot)
    assert startup["candidate_sha256"] == release["candidate_sha256"] and startup["cold_boot"]
    snapshot = startup["read_only_snapshot"]
    raw = read_ram(snapshot)
    assert raw[LITERAL - BASE:LITERAL - BASE + 4] == old_literal
    assert raw[RESIDENT_NAME - BASE:RESIDENT_NAME - BASE + len(TARGET)] == TARGET
    arm_offset, _, load_address, arm_size = unpack_from("<4I", previous, 0x20)
    assert load_address == BASE and arm_size == len(arm) and previous[arm_offset:arm_offset + arm_size] == arm
    rom_offset = arm_offset + LITERAL - BASE
    changed = bytearray(previous)
    changed[rom_offset:rom_offset + 4] = new_literal
    ROOT.mkdir(parents=True, exist_ok=True)
    if ROM.exists():
        assert ROM.read_bytes() == changed
    else:
        ROM.write_bytes(changed)
    changed[rom_offset:rom_offset + 4] = old_literal
    assert changed == previous
    revised = NdsImage.open(ROM).read_file(ARM)
    assert prior.code_at(revised, LITERAL, LITERAL + 4) == new_literal

    revised_ram = bytearray(raw)
    revised_ram[LITERAL - BASE:LITERAL - BASE + 4] = new_literal
    expected = read(prior.CATALOGUE)["town_table"]["installed"]
    before = prior.test_destination(arm, snapshot, expected)
    source = checked_text(getsource(prior.test_destination), {
        'assert text == "伝道師".encode("cp932") + b"\\0"': 'assert text == TARGET',
    })
    namespace = vars(prior) | dict(read_ram=lambda _: bytes(revised_ram), TARGET=TARGET)
    exec(compile(source, __file__ + "::relocated-label", "exec"), namespace)
    after = namespace["test_destination"](revised, snapshot, expected)
    assert before["destinations"][:114] == after["destinations"][:114]
    assert before["destinations"][115] == after["destinations"][115]
    assert after["destinations"][114]["name"] == ENGLISH
    assert before["picker"] == after["picker"] and before["menu_mode_test"] == after["menu_mode_test"]
    formatted = format_checks(revised, {"offline": {"installed": after}})
    assert formatted["destination_names"][114]["output_hex"] == b"To: Missionary".hex()
    assert formatted["destination_names"][114]["width_px"] == 84
    write(STORED, dict(candidate_sha256=digest(ROM), predecessor_sha256=release["candidate_sha256"],
        target_ARM9_sha256=sha256(revised).hexdigest(), clean_sha256=release["clean_input_sha256"],
        exact_whole_parent_inverse=True, rom_offset=rom_offset, arm9_virtual_address=LITERAL,
        current_hex=old_literal.hex(), staged_hex=new_literal.hex(),
        class_evidence=reference(CLASS_REPORT), role_evidence=reference(ROLE_REPORT),
        prior_destination_evidence=reference(prior.OUT), resident_string_address=RESIDENT_NAME,
        resident_string_hex=TARGET.hex(), snapshots_are_offline=True, startup_reference=reference(boot),
        original_japanese=dict(address=OLD_NAME, exact_hex=SOURCE.hex(), text=JAPANESE),
        reviewed_english=ENGLISH, ordinary_town_controls=114,
        offline_destination_cases=116, destination_114_before=before["destinations"][114],
        destination_114_after=after["destinations"][114], focused_picker=after["picker"],
        formatted_destination=formatted["destination_names"][114]))
    print("Staged the Missionary destination. The 114 town controls and no-target case match.")


if __name__ == "__main__":
    stage()
