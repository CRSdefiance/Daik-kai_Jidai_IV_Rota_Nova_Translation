"""Align the title menu and empty notice with the original Historic Sites heading."""

from argparse import ArgumentParser
from dataclasses import replace
from pathlib import Path
from struct import pack_into, unpack_from
import sys

from dk4tool.dialogue.review import REQUIRED_REVIEW_GATES
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.main_pool_cache_visibility import POOL, STAGE
from dk4tool.patch.xdelta import apply_xdelta, make_xdelta
from ndspy.code import MainCodeFile
from scripts import headless_desmume_v193 as emulator
from scripts import observe_gallery_empty_common_20261114 as historical
from scripts import register_historic_sites_editorial_20261121 as parent
from scripts.reconcile_shared_display_20261121 import COMMON, workflow
from scripts.review_characters_gallery_20261121 import c_string


base, native = parent.base, parent.native
ARM, CLEAN = parent.stage.ARM, parent.stage.CLEAN
ROOT = Path("work/historic_sites_menu_20261121")
ROM, PROOF = ROOT / "Historic_Sites_Menu_STAGED.nds", ROOT / "staged.json"
LIVE = ROOT / "gallery_menu_verified.json"
NOTICE = Path("translations/editorial_checkpoints/SharedText_20261110_v1/gallery_empty_collections_reviewed_20261114_v1.json")
BASE, MENU, HEADING, MESSAGE = 0x02000000, 0x115718, 0x4423C, 99
ENGLISH = "Historic Sites"
EMPTY = "No historic sites discovered yet."
GATES = dict.fromkeys(REQUIRED_REVIEW_GATES, True) | {"formatting": False}


def transform(clean, old_arm, old_common):
    clean_arm = clean.read_file(ARM)
    heading_source = unpack_from("<I", clean_arm, HEADING)[0] - BASE
    menu_source = unpack_from("<I", clean_arm, MENU)[0] - BASE
    menu_before = unpack_from("<I", old_arm, MENU)[0] - BASE
    assert menu_before == menu_source == 0x13894C
    assert c_string(clean_arm, menu_source) == c_string(clean_arm, heading_source) == "史跡".encode("cp932") + b"\0"
    assert c_string(old_arm, menu_before) == b"Ruins\0"
    heading = unpack_from("<I", old_arm, HEADING)[0]
    pool, = (s.data for s in MainCodeFile(old_arm, BASE).sections if s.ramAddress == STAGE)
    assert heading == 0x02388741 and c_string(pool, heading - POOL) == ENGLISH.encode("ascii") + b"\0"
    new_arm = bytearray(old_arm)
    pack_into("<I", new_arm, MENU, heading)
    assert new_arm[:MENU] == old_arm[:MENU] and new_arm[MENU + 4:] == old_arm[MENU + 4:]

    directory = native.digest(old_arm[workflow.DIRECTORY_OFFSET:workflow.TABLE_OFFSET])
    old = workflow.owned_entries(old_common, old_arm, directory)
    source = workflow.common_message_entries(clean.read_file(COMMON), clean_arm)
    previous, = [r for r in base.load(NOTICE)["records"] if r["message_ID"] == MESSAGE]
    assert source[MESSAGE].text.hex() == previous["source_hex"] and old[MESSAGE].text.hex() == previous["current_hex"]
    assert old[MESSAGE].text[-1:] == b" "
    data = EMPTY.encode("ascii") + b" "
    assert len(data) == len(old[MESSAGE].text) and b"%" not in data
    entry = old[MESSAGE]
    blocks = list(IlnkContainer.parse(old_common).blocks)
    index, lo, hi = entry.block, entry.block_offset, entry.copy_end
    original = blocks[index]
    assert original[lo:hi] == entry.text
    blocks[index] = original[:lo] + data + original[hi:]
    common = IlnkContainer(blocks).to_bytes()
    installed = workflow.owned_entries(common, new_arm, directory)
    assert all(b == (replace(a, text=data) if a.message_id == MESSAGE else a)
               for a, b in zip(old, installed, strict=True))
    blocks[index] = blocks[index][:lo] + entry.text + blocks[index][hi:]
    assert IlnkContainer(blocks).to_bytes() == old_common
    allocations = dict(block=index, offset=lo, copy_end=hi, exact_span_bytes=hi - lo)
    records = [
        dict(id="GALLERY_RUINS_MENU", file_path=ARM, clean_Japanese="史跡", english=ENGLISH,
            previous_English="Ruins", speaker="Gallery interface", decision="revision",
            source_meaning="Historic sites in the Gallery collection.",
            context="The Gallery menu opens the Historic Sites screen with discoveries ranging from ruins to churches.",
            localization_note="Use the same established name as the screen heading. The Japanese uses the same term in both places.",
            source_reference=dict(pointer_field=MENU, offset=menu_source, exact_hex=c_string(clean_arm, menu_source).hex()),
            current_reference=dict(pointer_field=MENU, offset=menu_before, exact_hex=c_string(old_arm, menu_before).hex()),
            staged_reference=dict(pointer_field=MENU, address=heading, shared_heading_field=HEADING,
                                  exact_hex=(ENGLISH.encode("ascii") + b"\0").hex()), review=GATES.copy()),
        dict(id="COMMON_MESSAGE_99", message_ID=MESSAGE, file_path=COMMON, clean_Japanese=previous["source_Japanese"],
            english=EMPTY, previous_English=previous["english"], speaker="Gallery notice", decision="revision",
            source_meaning=previous["source_meaning"], context=previous["context"].replace("Ruins", ENGLISH),
            localization_note="Use historic sites for the same collection. The short notice clearly ties the absence to the current discoveries.",
            source_reference=workflow.reference(source[MESSAGE]), source_hex=source[MESSAGE].text.hex(),
            current_reference=workflow.reference(old[MESSAGE]), current_hex=old[MESSAGE].text.hex(),
            staged_reference=workflow.reference(installed[MESSAGE]) | {"exact_hex": data.hex()}, review=GATES.copy()),
    ]
    return bytes(new_arm), common, records, allocations


def stage():
    assert not ROM.exists() and not PROOF.exists()
    release, ledger = map(base.load, (parent.RELEASE, base.LEDGER))
    assert base.digest(base.REGISTRY) == release["registry_sha256"]
    assert base.digest(parent.ROM) == release["candidate_sha256"] == ledger["current_integrated_candidate"]["sha256"]
    assert base.digest(CLEAN) == release["clean_input_sha256"]
    clean, image = map(base.NdsImage.open, (CLEAN, parent.ROM))
    arm, common = image.read_file(ARM), image.read_file(COMMON)
    new_arm, new_common, records, allocations = transform(clean, arm, common)
    image.replace_file(ARM, new_arm)
    image.replace_file(COMMON, new_common)
    target = bytes(image.rom.save())
    image.replace_file(ARM, arm)
    image.replace_file(COMMON, common)
    assert bytes(image.rom.save()) == parent.ROM.read_bytes()
    ROOT.mkdir(exist_ok=True)
    ROM.write_bytes(target)
    base.save(PROOF, dict(candidate_sha256=base.digest(ROM), parent_sha256=release["candidate_sha256"],
        clean_input_sha256=release["clean_input_sha256"], target_ARM9_sha256=native.digest(new_arm),
        target_COMMON_sha256=native.digest(new_common), records=records, allocation=allocations,
        translation_policy="natural-dialogue-v2", target_locale="en-US", encoder="dialogue-relocatable-v1",
        review_gates=sorted(REQUIRED_REVIEW_GATES), original_allocation_unchanged=True))
    patch, rebuilt = ROOT / "translation.xdelta", ROOT / "clean_rebuilt.nds"
    assert not patch.exists() and not rebuilt.exists()
    make_xdelta(CLEAN, ROM, patch)
    apply_xdelta(CLEAN, patch, rebuilt)
    assert rebuilt.read_bytes() == ROM.read_bytes()
    print("Staged the Historic Sites menu and notice with an exact clean-input patch.", flush=True)


def replay(case):
    before = case == "empty_before"
    rom = parent.ROM if before else ROM
    root = ROOT / case
    root.mkdir()
    fixture = []
    if case.startswith("empty"):
        schedule, frames, end, _, donor = historical.schedule("gallery_empty")
        inputs = root / "controls.json"
        base.save(inputs, schedule)
        donor = donor["source"]
    elif case == "full_popup":
        saved = Path("work/analysis/characters_gallery_v525")
        manifest = base.load(saved / "save_fixture_manifest.json")
        manifest.update(production_ROM=str(rom), production_ROM_sha256=base.digest(rom))
        manifest_path = root / "fixture.json"
        base.save(manifest_path, manifest)
        fixture = ["--allow-gallery-fixtures", "--gallery-save-fixture-manifest", str(manifest_path), "--touchscreen"]
        inputs, donor = saved / "inputs.json", manifest["fixture_save"]
        frames, end = [2400], 2400
    else:
        gallery = parent.stage
        manifest = base.load(gallery.GALLERY / "sites_fixture_manifest.json")
        manifest.update(production_ROM=str(rom), production_ROM_sha256=base.digest(rom))
        path = root / "fixture.json"
        base.save(path, manifest)
        fixture = ["--allow-gallery-fixtures", "--gallery-save-fixture-manifest", str(path), "--touchscreen"]
        inputs, donor = gallery.PLAN / "inputs.json", manifest["fixture_save"]
        frames, end = [2100, 2800, 3200, 7000, 7200, 7400], 7400
    sys.argv = [emulator.__file__, "--rom", str(rom), "--out", str(root / "capture"), "--frames", str(end),
        "--capture-every", "99999", "--capture-at", *map(str, frames),
        "--battery-save", donor, "--inputs-json", str(inputs), *fixture]
    emulator.main()


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("stage", "empty_before", "empty_after", "populated", "full_popup"))
    action = parser.parse_args().action
    stage() if action == "stage" else replay(action)
