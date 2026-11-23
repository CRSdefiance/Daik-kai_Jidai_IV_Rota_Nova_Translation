"""Restore the two full names of Maria's starting ships."""

from hashlib import sha256
from pathlib import Path
from struct import pack_into, unpack_from

from ndspy.code import MainCodeFile

from dk4tool.dialogue.review import REQUIRED_REVIEW_GATES
from dk4tool.patch.xdelta import apply_xdelta, make_xdelta
from scripts import register_item_gallery_wraps_20261121 as parent
from scripts.stage_ship_class_names_20261115 import executable, references
from scripts.stage_specialized_ship_labels_20261115 import ARM, BASE, CLEAN, design_field
from scripts.verify_release_baseline import files


base = parent.base
ROOT = Path("work/shipyard_fleet_ui_20261121/maria")
ROM, PROOF = ROOT / "Maria_Starter_Ship_Names_STAGED.nds", ROOT / "staged.json"
NAMES = {
    147: ("春申", "Chun", "Chunshen", 0x15B8E0, 0x15B8E8, 0x121F20, "配下"),
    148: ("華昌", "Hua", "Huachang", 0x15B9E0, 0x15B9E0, 0x122220, "怪物"),
}


def c_string(data, offset):
    return data[offset:data.index(0, offset) + 1]


def transform(clean, current):
    original, active = map(executable, (clean, current))
    japanese, before = original[ARM], active[ARM]
    target = bytearray(before)
    rows = []
    for model, (source, old, english, start, previous, retired_field, retired_text) in NAMES.items():
        field = design_field(model)
        end = start + 16
        retired = start + (8 if start == previous else 0)
        assert unpack_from("<I", japanese, field)[0] == unpack_from("<I", before, field)[0] == BASE + previous
        assert unpack_from("<I", japanese, retired_field)[0] == BASE + retired
        relocated_owner = unpack_from("<I", before, retired_field)[0]
        assert not BASE + start <= relocated_owner < BASE + end
        assert c_string(japanese, previous) == source.encode("cp932") + b"\0"
        assert c_string(japanese, retired) == retired_text.encode("cp932") + b"\0"
        assert references(original, start, 16) == {
            BASE + previous: [(ARM, field)], BASE + retired: [(ARM, retired_field)]
        }
        assert references(active, start, 16) == {BASE + previous: [(ARM, field)]}
        old_bytes = old.encode("ascii") + b"\0"
        assert before[previous:previous + 8] == old_bytes.ljust(8, b"\0")
        assert before[retired:retired + 8] == japanese[retired:retired + 8]
        label = english.encode("ascii") + b"\0"
        assert len(label) <= 16 and len(label) <= 19
        target[start:end] = label.ljust(16, b"\0")
        pack_into("<I", target, field, BASE + start)
        rows.append(dict(
            id=f"SHIP_DESIGN_{model}", file_path=ARM, model_ID=model, speaker="Ship name",
            clean_Japanese=source, previous_English=old, english=english, decision="revision",
            source_meaning=f"Named junk in Maria's starting fleet, {english} in Mandarin pinyin.",
            context=f"Starting fleet slot {model - 146}. The hull class remains Junk.",
            localization_note=f"Use both syllables of the Chinese proper name. {old} omitted the second character.",
            source_reference=dict(pointer_field=field, offset=previous, exact_hex=c_string(japanese, previous).hex()),
            current_reference=dict(pointer_field=field, offset=previous, exact_hex=old_bytes.hex()),
            staged_reference=dict(pointer_field=field, offset=start, exact_hex=label.hex(), allocation_bytes=16),
            reclaimed_reference=dict(source_pointer_field=retired_field, source_pointer=BASE + retired,
                                     current_pointer=relocated_owner, source_text=retired_text,
                                     before_hex=before[start:end].hex()),
            review=dict.fromkeys(REQUIRED_REVIEW_GATES, True) | {"formatting": False},
        ))
    arm = bytes(target)
    assert len(arm) == len(before) and bytes(MainCodeFile(arm, BASE).save()) == arm
    original_sections = MainCodeFile(before, BASE).sections
    target_sections = MainCodeFile(arm, BASE).sections
    assert len(original_sections) == len(target_sections)
    for index, (a, b) in enumerate(zip(original_sections, target_sections, strict=True)):
        assert (a.ramAddress, a.bssSize, len(a.data)) == (b.ramAddress, b.bssSize, len(b.data))
        if index:
            assert a.data == b.data
    for row in rows:
        start = row["staged_reference"]["offset"]
        field = row["source_reference"]["pointer_field"]
        target[start:start + 16] = before[start:start + 16]
        target[field:field + 4] = before[field:field + 4]
    assert bytes(target) == before
    return arm, rows


def main():
    assert not ROM.exists() and not PROOF.exists()
    release = base.load(parent.RELEASE)
    assert base.digest(parent.ROM) == release["candidate_sha256"]
    assert base.digest(base.REGISTRY) == release["registry_sha256"]
    assert base.digest(CLEAN) == release["clean_input_sha256"]
    clean, current, image = [base.NdsImage.open(path) for path in (CLEAN, parent.ROM, parent.ROM)]
    arm, rows = transform(clean, current)
    old_parts = files(current)
    image.rom.arm9 = arm
    new_parts = files(image)
    assert old_parts.keys() == new_parts.keys()
    assert {name for name in old_parts if new_parts[name] != old_parts[name]} == {ARM}
    output = bytes(image.rom.save())
    image.rom.arm9 = current.rom.arm9
    assert bytes(image.rom.save()) == parent.ROM.read_bytes()
    ROOT.mkdir(parents=True, exist_ok=True)
    ROM.write_bytes(output)
    patch, rebuilt = ROOT / "research.xdelta", ROOT / "clean_rebuilt.nds"
    make_xdelta(CLEAN, ROM, patch)
    apply_xdelta(CLEAN, patch, rebuilt)
    assert rebuilt.read_bytes() == output
    base.save(PROOF, dict(
        translation_policy="natural-dialogue-v2", target_locale="en-US",
        review_gates=list(REQUIRED_REVIEW_GATES), records=rows,
        candidate_sha256=base.digest(ROM), parent_sha256=release["candidate_sha256"],
        clean_input_sha256=release["clean_input_sha256"], target_ARM9_sha256=sha256(arm).hexdigest(),
        status="staged; original ship UI verification pending", new_contextual_credit=0,
    ))
    print("Staged the two full ship names with a byte-exact clean-input patch.")


if __name__ == "__main__":
    main()
