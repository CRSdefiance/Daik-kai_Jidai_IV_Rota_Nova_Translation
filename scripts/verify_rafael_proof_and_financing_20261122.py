"""Prove the retained gold notice and original tutorial choice at their native widths."""

from argparse import ArgumentParser
import sys
from types import FunctionType

from dk4tool.dialogue.reviewed_choice_object_v2 import labels
from scripts import check_rafael_two_choice_display_v2 as menu
from scripts import stage_rafael_proof_and_financing_20261122 as stage
from scripts import verify_all_routes_next_phrase_wraps_20261118 as display
from scripts import verify_palace_london_glyphs_20261122 as glyphs
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.stage_hamburg_ceramics_cross_route_20261120 import current_fe_painter


base, native = stage.base, stage.native
GLYPH_PROOF = stage.ROOT / "glyph_and_sheet_verification.json"
MENU_ROOT = stage.ROOT / "native_menu"
MENU_INPUT = stage.ROOT / "typed_choice_input.json"
MENU_PROOF = MENU_ROOT / "menu_provider_and_planes.json"
check_glyphs = FunctionType(glyphs.verify.__code__, vars(glyphs) | dict(stage=stage, OUTPUT=GLYPH_PROOF))


def stored_controls():
    proof, review = map(base.load, (stage.PROOF, stage.REVIEW))
    assert proof["candidate_sha256"] == base.digest(stage.ROM)
    assert proof["draft_sha256"] == base.digest(stage.REVIEW)
    assert proof["predecessor_sha256"] == base.digest(stage.parent.ROM)
    current = base.NdsImage.open(stage.ROM)
    block = native.IlnkContainer.parse(current.read_file(stage.paired.ARCHIVE)).blocks[44]
    group, = [g for g in proof["groups"] if g["block"] == 44]
    assert native.digest(block) == group["after"]
    menu, = (c for c in group["commands"] if c["word"] == 0x2100)
    modal, = (c for c in group["commands"] if "DK4_MES_B44_R0264" in c["record_ids"])
    for command in (menu, modal):
        at, data = command["stored_offset"], bytes.fromhex(command["stored"])
        assert command["current"] == command["stored"] and block[at:at+len(data)] == data
    return proof, review, modal, menu


def prepare():
    proof, review, modal, choice = stored_controls()
    release = base.load(stage.parent.RELEASE)
    active = native.RegisteredRuntime(stage.parent.RELEASE, release["own_registered_startup"], captain=3)
    target = base.NdsImage.open(stage.ROM)
    assert all(active.image.read_file(asset) == target.read_file(asset) for asset in display.ASSETS)
    data = bytes.fromhex(modal["stored"])
    assert data[:6] == bytes.fromhex("0040ffff00fe")
    text = data[6:data.index(0,6)]
    assert text.split() == [b"Received", b"30,000", b"gold!"]
    plane = current_fe_painter(active)(text)
    membership = stage.template.typed.forest.system.check_FE_rows(text, plane)
    assert plane["complete_consumed_bytes"] == len(text)
    physical = plane["physical"]
    assert all(not any(physical[y*228+216:(y+1)*228]) for y in range(64))
    cropped = b"".join(physical[y*228:y*228+216] for y in range(64))
    contact = display.display.inherited.early.contact_sheets
    path = stage.ROOT / "modal"
    path.mkdir()
    sheet, = FunctionType(contact.__code__, contact.__globals__ | dict(ROOT=path))([
        ("B44 original 30,000 gold notice", cropped)])
    screenshot = stage.Path(sheet["path"])
    renamed = screenshot.with_name("retained_gold_notice.png")
    screenshot.rename(renamed)
    sheet["path"] = str(renamed)
    assert base.digest(renamed) == sheet["sha256"]
    base.save(stage.FE_PROOF, dict(candidate_sha256=proof["candidate_sha256"], owner="DK4_MES_B44_R0264",
        stored_offset=modal["stored_offset"], exact_command_hex=modal["stored"], physical_plane_hex=physical.hex(),
        row_membership=membership, original_modal_consumer=True, sheets=[sheet]))
    prepared = []
    for row in review["retained_choice_labels"]:
        source, old = row["source_reference"], row["current_reference"]
        assert source["exact_command_hex"] == choice["source"] and old["exact_command_hex"] == choice["stored"]
        prepared.append(row | dict(kind="typed-choice-label", source_index=row["slot"],
            source_choice_object_hex=choice["source"], current_choice_object_hex=choice["current"],
            source_hex=source["exact_body_hex"], current_hex=old["exact_body_hex"]))
    base.save(MENU_INPUT, dict(current_ROM_sha256=proof["predecessor_sha256"], typed_choice_objects=2, records=prepared))
    check_glyphs()


def provider():
    release = base.load(stage.parent.RELEASE)
    sys.argv = [menu.__file__, "--manuscript", str(MENU_INPUT), "--release", str(stage.parent.RELEASE),
        "--startup", release["own_registered_startup"], "--out", str(MENU_ROOT)]
    source = checked_text(menu.source, {"captain=0": "captain=3"})
    scope = menu.main.__globals__ | dict(__name__="financing_native_choice_provider")
    exec(compile(source, __file__ + "::registered-native-provider", "exec"), scope)
    scope["main"]()
    proof, review, _, choice = stored_controls()
    shown = base.load(MENU_PROOF)
    raw = bytes.fromhex(choice["stored"])
    assert raw == (MENU_ROOT/"compiled_choice_object.bin").read_bytes()
    assert shown["native_choice_object_hex"] == raw.hex()
    assert shown["complete_caption_glyphs_centering_bounds_guards_andconsumption_pass"]
    assert shown["complete_English_caption_style_planes"] == 8 and len(shown["compiler_negatives_rejected"]) == 7
    assert [label.decode("ascii") for label in labels(raw)] == [r["english"] for r in review["retained_choice_labels"]]
    installed = [r | dict(registered_reference=r["current_reference"] | dict(
        command_offset=choice["stored_offset"], offset=choice["stored_offset"]+r["current_reference"]["offset"]-choice["current_offset"],
        candidate_sha256=proof["candidate_sha256"], archive_sha256=proof["archive_hashes"][stage.paired.ARCHIVE],
        block_sha256=next(g["after"] for g in proof["groups"] if g["block"] == 44)),
        review=r["review"] | {"formatting":True}) for r in review["retained_choice_labels"]]
    base.save(stage.CHOICE_PROOF, dict(candidate_sha256=proof["candidate_sha256"], captions=installed,
        exact_retained_object_hex=raw.hex(), stored_offset=choice["stored_offset"],
        native_provider_sha256=base.digest(MENU_PROOF), sheets=[shown["review_sheet"]]))


if __name__ == "__main__":
    cli = ArgumentParser(description=__doc__)
    cli.add_argument("action", choices=("prepare", "provider"))
    globals()[cli.parse_args().action]()
