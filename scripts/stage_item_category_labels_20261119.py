"""Review the complete item category row and stage its Source Item correction."""

from pathlib import Path
from struct import iter_unpack, unpack_from

from ndspy.code import MainCodeFile

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.gallery_description_release import compile_rows
from dk4tool.patch.item_interface_research import BASE, TYPE_CALLS, POOL
from scripts import register_tavern_strategist_followup_20261119 as parent
from scripts.stage_source_item_cards_and_coin_v1 import ITEM_PLAN

base, native = parent.base, parent.native
CLEAN, ARM, COMMON = parent.stage.CLEAN, parent.stage.ARM, parent.stage.COMMON
ROOT = Path("work/item_category_labels_20261119/research_v1")
ROM, PROOF = ROOT / "Item_Category_Labels_RESEARCH_ONLY.nds", ROOT / "staged.json"
CONTEXT = Path("work/analysis/lil_Goods_Mediterranean_source_v2820/source_item_terminology_and_empty_B42_context.json")
EXCHANGE = CONTEXT.with_name("complete90_clean_current_native_context.json")
REASONS = (
    "Use the Help term in singular form. In the Market exchange the item can create a trade specialty. Local Product suggests a commodity the city already sells.",
    "Navigation Gear covers instruments and equipment used for sailing and finding one's way without calling them consumable supplies.",
    "Weapon is the short singular category for offensive equipment.",
    "Armor distinguishes protective equipment from general equipment on the next category row.",
    "Equipment is a natural collective label for usable or wearable gear beyond weapons and armor.",
    "Figurehead is the established nautical term for the item mounted at the bow.",
    "Mystery Item preserves the unknown purpose of the object without implying a quest or a reward.",
    "Gift describes the intended use without promising a relationship or reaction.",
    "Proof is the established short label for an actual Proof of Conquest and distinguishes it from the map in the next category.",
    "Proof Map describes a map pointing to a Proof of Conquest and keeps it distinct from the actual Proof.",
    "Ruin Map clearly identifies the map's destination without asserting that the ruin has been discovered.",
    "Other is a conventional catch-all label and does not invent a criterion shared by its members.",
    "Ancient Map keeps the separate named map category whose hints the player can inspect.",
)
MEANINGS = (
    "An item that can become the source of a local trade specialty.",
    "Gear for a voyage or navigation.", "A weapon.", "Protective armor.", "Equipment.",
    "A ship's figurehead.", "A small object of mysterious purpose.", "A gift.",
    "A Proof of Conquest.", "A map to a Proof of Conquest.", "A map to a ruin.",
    "The remaining items.", "An ancient map.",
)


def word(data, offset):
    return unpack_from("<I", data, offset)[0]


def cstring(data, offset):
    return bytes(data[offset:data.index(0, offset)])


def branch(data, offset, origin):
    assert data[offset + 3] == 0xEB
    return origin + offset + 8 + 4 * int.from_bytes(data[offset:offset + 3], "little", signed=True)


def main():
    assert not ROOT.exists()
    release, catalogue, context = map(base.load, (parent.RELEASE, ITEM_PLAN, CONTEXT))
    assert base.digest(parent.ROM) == release["candidate_sha256"]
    assert base.digest(base.REGISTRY) == release["registry_sha256"]
    assert base.digest(CLEAN) == release["clean_input_sha256"]
    clean, image = map(base.NdsImage.open, (CLEAN, parent.ROM))
    source, arm = (im.read_file(ARM) for im in (clean, image))
    assert native.digest(arm) == release["target_ARM9_sha256"]
    sections = MainCodeFile(arm, BASE).sections
    payload = bytes(sections[3].data)
    storage = arm.index(payload)
    assert arm.count(payload) == 1
    category, = (r for r in catalogue["item_only_projection"] if r["kind"] == "CATEGORY")
    wrapper, = {branch(arm, at, BASE) for at in TYPE_CALLS}
    getter = branch(payload, wrapper - POOL + 12, POOL)
    table = word(payload, getter - POOL + 32)
    assert table == category["target_table"]
    assert list(unpack_from("<13I", payload, table - POOL)) == category["compiled_pointers"]
    assert arm[0x13C350:0x13C384] == source[0x13C350:0x13C384]

    terminology = context["terminology"]
    assert terminology["HELP_TOPIC_194"]["record"]["heading"] == "Source Items"
    assert terminology["HELP_TOPIC_194"]["record"]["clean_source_hex"].startswith("8cb48e5995a8")
    lil = base.load(EXCHANGE)
    assert lil["source_ROM_sha256"] == release["clean_input_sha256"]
    block = IlnkContainer.parse(clean.read_file("/data/SC2.DK4")).blocks[43]
    lil_rows = [r for r in lil["records"] if r["block"] == 43]
    assert lil_rows and any("原産物" in r["source_Japanese"] for r in lil_rows)
    assert all(bytes.fromhex(r["source_hex"]) in block for r in lil_rows)
    records = []
    for index, (ptr, meaning, reason) in enumerate(zip(category["compiled_pointers"], MEANINGS, REASONS, strict=True)):
        ident = f"ITEM_CATEGORY_{index:02d}"
        earlier, = (r for r in catalogue["records"] if r["id"] == ident)
        source_field = 0x13C350 + index * 4
        source_ptr = word(source, source_field)
        original = cstring(source, source_ptr - BASE)
        ref, = earlier["source_fields"]
        assert (source_field, source_ptr, original.hex()) == (ref["field"], ref["source_pointer"], ref["source_hex"])
        at = ptr - POOL
        encoded = cstring(payload, at)
        previous = encoded.decode("ascii").strip()
        assert previous == earlier["english"] and encoded == earlier["compiled"].encode("ascii")
        revised = index == 0
        english = "Source Item" if revised else previous
        compiled = compile_rows(english, 1, 16)[0].encode("ascii")
        assert compiled == encoded or revised
        records.append(dict(id=ident, file_path=ARM, speaker="Item interface",
            context="The main and compact item panels put the item category beside its role, effect and value.",
            clean_Japanese=original.decode("cp932"), source_meaning=meaning,
            english=english, previous_English=previous, localization_note=reason,
            decision="revision" if revised else "retention", source_reference=ref,
            current_reference=dict(table_entry=table + index * 4, runtime_pointer=ptr, ARM9_offset=storage + at),
            source_hex=original.hex(), current_hex=encoded.hex(), compiled_hex=compiled.hex(),
            review={gate: gate != "formatting" for gate in ("source", "context", "localization", "naturalness", "formatting")}))

    row = records[0]
    pointer = row["current_reference"]["runtime_pointer"]
    off = row["current_reference"]["ARM9_offset"]
    old = bytes.fromhex(row["current_hex"]) + b"\0"
    new = (bytes.fromhex(row["compiled_hex"]) + b"\0").ljust(len(old), b"\0")
    assert len(new) == len(old) and arm[off:off + len(old)] == old
    assert category["compiled_pointers"][1] == pointer + len(old)
    # Recognize both the start pointer and any preexisting interior owners.
    owners = [(i, at, value) for i, sec in enumerate(sections)
              for at, (value,) in enumerate(iter_unpack("<I", sec.data))
              if pointer <= value < pointer + len(old)]
    assert owners == [(3, (table - POOL) // 4, pointer)], owners
    target = arm[:off] + new + arm[off + len(old):]
    image.replace_file(ARM, target)
    output = bytes(image.rom.save())
    image.replace_file(ARM, arm)
    assert bytes(image.rom.save()) == parent.ROM.read_bytes()
    ROOT.mkdir(parents=True)
    ROM.write_bytes(output)
    base.save(PROOF, dict(candidate_sha256=base.digest(ROM), previous_sha256=release["candidate_sha256"],
        clean_input_sha256=release["clean_input_sha256"], registry_sha256=release["registry_sha256"],
        target_ARM9_sha256=native.digest(target), target_COMMON_sha256=release["target_COMMON_sha256"],
        source_proofs={str(p): base.digest(p) for p in (ITEM_PLAN, CONTEXT, EXCHANGE, Path(__file__))},
        translation_policy="natural-dialogue-v2", target_locale="en-US", encoder="dialogue-relocatable-v1",
        review_gates=list(row["review"]), records=records, entire_parent_inverse=True,
        slot=dict(offset=off, pointer=pointer, old_hex=old.hex(), new_hex=new.hex(),
                  consumers=list(TYPE_CALLS), wrapper=wrapper, getter=getter, table=table)))
    print("Reviewed 13 categories and staged Source Item in its original private allocation.")


if __name__ == "__main__":
    main()
