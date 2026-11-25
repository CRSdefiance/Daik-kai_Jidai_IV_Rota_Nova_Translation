"""Separate historical lookup spellings from the current visible names."""

from inspect import getsource
import re
from pathlib import Path
from struct import pack, unpack_from

from unicorn.arm_const import UC_ARM_REG_LR, UC_ARM_REG_PC, UC_ARM_REG_R1, UC_ARM_REG_SP

from dk4tool.patch.confirmed_name_message_catalog import CALLS, MACRO
from dk4tool.patch.reviewed_name_catalog import ROUTE
from scripts import checkpoint_historical_name_spellings_20261115 as precedent
from scripts import register_tavern_nearby_town_wrap_20261123 as current
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.verify_ordinary_name_fidelity_research import initialized


base, native = current.base, current.native
OUT = current.audit.OUT.with_name("current_name_aliases_20261123.json")
MARIA = Path("translations/maria303_integrated_final_review_v1.json")
OLD = re.compile(rb"\b(?:Raphael|Kamil|Camil|Camile|Joachim|Christina|Hans Retzel|Janus Pasha)\b", re.IGNORECASE)


def janus_lookup(arm, rows, entry, installed_speech):
    cpu = initialized(arm)
    cases = [("current whole", installed_speech, 3, None), ("current body", installed_speech[1:], 3, None)]
    for old_row in rows:
        old = bytes.fromhex(old_row["key_hex"])
        label = old_row["requests"][0]["form"]
        cases.extend(((f"historical {label}", old, 3, old_row), (f"different route {label}", old, 0, None)))
    checks = []
    for name, data, route, selected in cases:
        for alignment in range(4):
            address = 0x02468020 + alignment
            raw = data + b"\0"
            protected = b"\xA5" * 16 + raw + b"\xA5" * 16
            cpu.mem_write(address - 16, protected)
            cpu.mem_write(ROUTE, pack("<I", route))
            cpu.reg_write(UC_ARM_REG_R1, address)
            cpu.reg_write(UC_ARM_REG_LR, precedent.BASE + CALLS[0] + 4)
            cpu.reg_write(UC_ARM_REG_SP, 0x027F0000)
            cpu.emu_start(entry, MACRO, count=1_000_000)
            assert cpu.reg_read(UC_ARM_REG_PC) == MACRO
            observed = cpu.reg_read(UC_ARM_REG_R1)
            assert observed == (selected["target_pointer"] if selected is not None else address)
            expected = bytes.fromhex(selected["target_hex"]) + b"\0" if selected is not None else raw
            assert bytes(cpu.mem_read(observed, len(expected))) == expected
            assert bytes(cpu.mem_read(address - 16, len(protected))) == protected
            assert b"Janus Pasha" not in expected or name.startswith("different route")
            checks.append(dict(case=name, route=route, alignment=alignment, selected_legacy_replacement=selected is not None,
                source_hex=data.hex(), selected_hex=expected[:-1].hex(), reached_original_expander_boundary=True))
    assert len(checks) == 24 and sum(row["selected_legacy_replacement"] for row in checks) == 8
    return checks


def janus_review(clean, current_image, arm, rows, entry):
    path, ident = "/data/SC3.DK4", "DK4_MES_B59_R0056"
    doc = base.load(MARIA)
    release_path = Path(doc["registered_release"])
    assert base.digest(release_path) == doc["registered_release_sha256"]
    review, = [row for row in doc["records"] if row["id"] == ident]
    left, right = (native.IlnkContainer.parse(image.read_file(path)).blocks[59] for image in (clean, current_image))
    sr, rr = review["source_reference"], review["planned_integrated_reference"]
    source = bytes.fromhex(review["source_hex"])
    installed = bytes.fromhex(rr["exact_stored_hex"])
    assert sr["block"] == rr["block"] == 59
    assert left[sr["offset"]:sr["offset"] + len(source)] == source
    assert right[rr["offset"]:rr["offset"] + len(installed)] == installed
    assert left[sr["command_offset"]:sr["offset"]] == right[rr["header_offset"]:rr["offset"]] == bytes.fromhex("0040ffff00")
    assert source[0] == installed[0] == 3 and installed[1:2] == b"I" and installed.isascii()
    assert installed.count(b"FI") == source.count(b"FI") == installed.count(b"FA") == source.count(b"FA") == 1
    assert "ジェナス・パサー" in review["source_Japanese"] and b"Janus Pasar" in installed
    assert all(review["review"].values()) and review["actual_utterance_observed_in_disclosed_fixture"]
    assert len(rows) == 2 and all(row["route_mask"] == 8 and row["requests"][0]["owner"] == [path, ident] for row in rows)
    return dict(id=ident, file_path=path, clean_reference=sr, clean_hex=source.hex(),
        clean_Japanese=review["source_Japanese"], installed_reference=rr | dict(active_block_sha256=native.digest(right)),
        native_name_controls=["FI", "FA"], english=review["editorial_logical_English"], review=review["review"],
        decision="retention", localization_note="The current introduction uses Janus Pasar and opens with a regular ASCII I.",
        prior_contextual_review=dict(path=str(MARIA), sha256=base.digest(MARIA), earlier_observed_fixture=True),
        prior_release=dict(path=str(release_path), sha256=base.digest(release_path)),
        isolated_catalogue_cases=janus_lookup(arm, rows, entry, installed))


def gallery_descriptions(arm, clean, image):
    old = base.load(precedent.OUTPUT)["native_gallery"]
    captions = precedent.validate(arm)
    assert len(captions) == old["active_caption_count"] == 164
    assert all(not OLD.search(row["English"].encode("ascii")) for row in captions)
    resident, = [raw for _, addr, raw in precedent.resident_components(image) if addr == precedent.STAGE]
    reviewed = old["descriptions"]
    for row in reviewed:
        offset = row["field"]
        source, = unpack_from("<I", clean, offset)
        installed, = unpack_from("<I", arm, offset)
        assert source == row["clean_pointer"] and installed == row["current_pointer"]
        assert clean[source - precedent.BASE:].split(b"\0", 1)[0].hex() == row["source_hex"]
        assert resident[installed - precedent.POOL:].split(b"\0", 1)[0].hex() == row["current_hex"]
    return dict(checked_active_captions=164, current_description_records=reviewed,
        earlier_description_bitmap_reference=dict(path=str(precedent.OUTPUT), sha256=base.digest(precedent.OUTPUT)))


def main():
    assert not OUT.exists()
    release = base.load(current.RELEASE)
    candidate = base.digest(current.ROM)
    assert release["candidate_sha256"] == candidate and release["registry_sha256"] == base.digest(base.REGISTRY)
    assert release["clean_input_sha256"] == base.digest(native.CLEAN)
    assert release["manifest_sha256"] == base.digest(current.MANIFEST)
    clean, image = map(base.NdsImage.open, (native.CLEAN, current.ROM))
    original, arm = (rom.read_file(current.ARM) for rom in (clean, image))
    assert native.digest(arm) == release["target_ARM9_sha256"]
    archives = list(current.routes.story_blocks(image).values())
    assert sum(map(len, archives)) == 1307
    assert all(not OLD.search(block) for blocks in archives for block in blocks)
    shared = current.stage.observed.prior.shared.paired.prior.entries(image)
    assert len(shared) == 3668 and all(not OLD.search(row.text) for row in shared)
    assert not OLD.search(image.read_file("/COMMON/HELP.DK4"))
    config = base.load(current.MANIFEST)["relocations"][current.ARM]["reviewed_name_integration"]["catalog"]
    validated = precedent.catalogue(arm, config, archives)
    old_keys = [row for row in config["records"] if OLD.search(bytes.fromhex(row["key_hex"]))]
    assert len(old_keys) == 197
    assert not any(OLD.search(bytes.fromhex(row["target_hex"])) for row in config["records"])
    stores = [b"\xFF".join(route) for route in archives]
    for row in old_keys:
        key = bytes.fromhex(row["key_hex"]) + b"\0"
        assert b"\xFF" not in key and not any(key in data for n, data in enumerate(stores) if row["route_mask"] & (1 << n))
    inherited = checked_text(getsource(precedent.legacy_hits), {"OLD.finditer": "ALIASES.finditer", "OLD.search": "ALIASES.search"})
    scope = vars(precedent) | dict(ALIASES=OLD)
    exec(compile(inherited, __file__ + "::retained-data", "exec"), scope)
    storage = scope["legacy_hits"](precedent.resident_components(image), config)
    selected = [row for row in old_keys if b"Janus Pasha" in bytes.fromhex(row["key_hex"])]
    janus = janus_review(clean, image, arm, selected, validated["entry"])
    earlier = base.load(current.audit.OUT)
    parent = base.load(current.parent.RELEASE)
    assert earlier["candidate_sha256"] == parent["candidate_sha256"]
    assert parent["target_ARM9_sha256"] == release["target_ARM9_sha256"]
    getters = earlier["default_actor_names"]
    assert getters["original_default_getter_cases"] == 414
    assert all(not OLD.search(row[field].encode("ascii")) for row in getters["outputs"] for field in ("progressive", "catalogue"))
    base.save(OUT, dict(candidate_sha256=candidate, clean_sha256=release["clean_input_sha256"],
        checked_production_story_blocks=1307, checked_COMMON_keys=3668, checked_Help_archive=True,
        catalogue=dict(entry=validated["entry"], table=validated["table"], helper_sha256=validated["helper_sha256"],
            total_rows=validated["total_rows"], historical_keys=len(old_keys), matching_installed_keys=0, retained_storage=storage),
        maria_introduction=janus, gallery=gallery_descriptions(arm, original, image),
        older_Hodram_save_middle_name=precedent.middle_cases(arm), earlier_414_name_getters_rebound=True,
        gameplay_scope="Uses the prior verified introduction. New native lookups stop before text display.", new_editorial_credit=0))
    print("Verified historical spellings in 197 lookup keys and rechecked the current Janus, Gallery and old-save name paths.")


if __name__ == "__main__":
    main()
