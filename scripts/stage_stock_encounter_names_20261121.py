"""Bind the five stock encounter models to the existing victory spelling."""

from hashlib import sha256
from pathlib import Path
from struct import pack_into, unpack_from

from ndspy.code import MainCodeFile

from dk4tool.dialogue.review import REQUIRED_REVIEW_GATES
from dk4tool.patch.special_battle_target_names_v1 import ALIASES, CALL
from dk4tool.patch.xdelta import apply_xdelta, make_xdelta
from scripts import register_maria_starter_ship_names_20261121 as parent
from scripts.review_battle_commands_and_outcomes_v1 import MODELS
from scripts.stage_ship_class_names_20261115 import executable, references
from scripts.stage_specialized_ship_labels_20261115 import ARM, BASE, CLEAN, class_field, design_field
from scripts.verify_release_baseline import files


base = parent.base
ROOT = Path("work/stock_encounter_names_20261121")
ROM, PROOF = ROOT / "Stock_Encounter_Names_STAGED.nds", ROOT / "staged.json"
REVIEWED_VICTORIES = Path("releases/all_routes_editorial_20261111_battle_commands_and_outcomes_candidate/verification/registered_review.json")
INSPECTION_REVIEW = Path("releases/all_routes_editorial_20261115_special_target_labels_candidate/verification/registered_review.json")
TABLE = 0x01FFFCFC
NOTE = {
    149: "Use Monster Fish for the specific creature, matching the original victory wording and the separate inspection class.",
    150: "Preserve the size adjective in Giant Squid and use the same wording in the battle result and inspection.",
    151: "Use the ordinary singular name Shark for this individual target.",
    152: "Preserve the white color in this specific model name. The separate inspection class identifies it generically as Whale.",
    153: "Use the complete name Ghost Ship. Ghost alone describes a different kind of target.",
}


def pointer(raw, field):
    return unpack_from("<I", raw, field)[0]


def installed_aliases(arm):
    code = MainCodeFile(arm, BASE)
    branch = pointer(arm, CALL - BASE)
    assert branch >> 24 == 0xEB
    target = CALL + 8 + 4 * ((branch & 0xFFFFFF) - 0x1000000)
    assert target == 0x01FFFCAC
    section, = (s for s in code.sections if s.ramAddress <= target < s.ramAddress + len(s.data))
    alias_fields, result = [], {}
    for i, (source, english) in enumerate(ALIASES):
        row = TABLE - section.ramAddress + 12 * i
        assert section.data[row:row + 8] == source.encode("cp932").ljust(8, b"\0")
        field = pointer(section.data, row + 8)
        payload = english.encode("ascii") + b"\0"
        offset = field - section.ramAddress
        assert field >= TABLE + 12 * len(ALIASES)
        assert section.data[offset:offset + len(payload)] == payload
        alias_fields.append(field)
        if english not in result:
            result[english] = (field, TABLE + 12 * i + 8)
    assert len(alias_fields) == 6 and len(result) == 5
    return result


def transform(clean, current):
    original, active = map(executable, (clean, current))
    ja, before = original[ARM], active[ARM]
    existing = installed_aliases(before)
    target = bytearray(before)
    rows = []
    for model, source, old, english in MODELS:
        field = design_field(model)
        previous = pointer(before, field)
        assert previous == pointer(ja, field)
        source_bytes = source.encode("cp932") + b"\0"
        old_bytes = old.encode("cp932") + b"\0"
        at = previous - BASE
        assert ja[at:at + len(source_bytes)] == source_bytes
        assert before[at:at + len(old_bytes)] == old_bytes
        assert references(original, at, len(source_bytes)) == {previous: [(ARM, field)]}
        assert references(active, at, len(old_bytes)) == {previous: [(ARM, field)]}
        index = model - 115
        assert ja[field + 5] == before[field + 5] == index
        label = english.encode("ascii") + b"\0"
        assert len(label) <= 19
        address, alias_field = existing[english]
        pack_into("<I", target, field, address)
        rows.append(dict(
            id=f"SHIP_DESIGN_{model}", file_path=ARM, model_ID=model, class_ID=index,
            speaker="Special encounter model name", clean_Japanese=source, previous_English=old,
            english=english, decision="revision", source_meaning=f"The encounter target named {english}.",
            context="The original victory announcer reads the current encounter model name through its virtual getter.",
            localization_note=NOTE[model],
            source_reference=dict(pointer_field=field, address=previous, exact_hex=source_bytes.hex()),
            current_reference=dict(pointer_field=field, address=previous, exact_hex=old_bytes.hex()),
            staged_reference=dict(pointer_field=field, address=address, alias_table_pointer_field=alias_field,
                                  exact_hex=label.hex(), initialized_name_allocation_bytes=19),
            class_reference=dict(pointer_field=class_field(index), unchanged_pointer=pointer(before, class_field(index))),
            review=dict.fromkeys(sorted(REQUIRED_REVIEW_GATES), True) | {"formatting": False},
        ))
    arm = bytes(target)
    assert bytes(MainCodeFile(arm, BASE).save()) == arm
    for row in rows:
        field = row["source_reference"]["pointer_field"]
        target[field:field + 4] = before[field:field + 4]
    assert bytes(target) == before
    return arm, rows


def main():
    assert not ROM.exists() and not PROOF.exists()
    release = base.load(parent.RELEASE)
    assert base.digest(base.REGISTRY) == release["registry_sha256"]
    assert base.digest(parent.ROM) == release["candidate_sha256"]
    assert base.digest(CLEAN) == release["clean_input_sha256"]
    clean, current, image = [base.NdsImage.open(path) for path in (CLEAN, parent.ROM, parent.ROM)]
    arm, rows = transform(clean, current)
    before = files(current)
    image.replace_file(ARM, arm)
    after = files(image)
    assert before.keys() == after.keys() and {k for k in before if before[k] != after[k]} == {ARM}
    result = bytes(image.rom.save())
    image.replace_file(ARM, before[ARM])
    assert bytes(image.rom.save()) == parent.ROM.read_bytes()
    ROOT.mkdir(parents=True, exist_ok=True)
    ROM.write_bytes(result)
    patch, rebuilt = ROOT / "research.xdelta", ROOT / "clean_rebuilt.nds"
    make_xdelta(CLEAN, ROM, patch)
    apply_xdelta(CLEAN, patch, rebuilt)
    assert rebuilt.read_bytes() == result
    base.save(PROOF, dict(translation_policy="natural-dialogue-v2", target_locale="en-US",
        review_gates=sorted(REQUIRED_REVIEW_GATES), records=rows,
        parent_sha256=release["candidate_sha256"], candidate_sha256=base.digest(ROM),
        clean_input_sha256=release["clean_input_sha256"], target_ARM9_sha256=sha256(arm).hexdigest(),
        original_victory_review=str(REVIEWED_VICTORIES), original_inspection_review=str(INSPECTION_REVIEW),
        new_contextual_credit=0, changed_pointer_fields=5, runtime_code_unchanged=True))
    print("Staged five exact pointer changes and verified the clean-input patch.")


if __name__ == "__main__":
    main()
