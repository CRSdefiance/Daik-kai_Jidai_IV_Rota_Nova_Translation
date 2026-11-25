"""Stage the source-reviewed reply in its original Rafael B44 allocation."""

from argparse import ArgumentParser
from pathlib import Path
from types import FunctionType, SimpleNamespace

from PIL import Image
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.script.format_safety_relocated_v2 import bind_registered_story_percent_guard
from scripts import check_supply_ratio_release_inputs_20261123 as checks
from scripts import register_cartridge_title_20261123 as template
from scripts import register_kurushima_confrontation_wraps_20261123 as parent
from scripts import stage_genoa_alternate_dialogue_20261123 as fixed
from scripts import verify_rafael_prepare_alone_20261123 as review
from scripts.stage_cartridge_title_20261123 import CLEAN, REGISTRY, NdsImage, digest, read, reference, sha256, write
from scripts.verify_moonlit_violin_20261121 import bytes_for


ROOT = Path(".codex-release-work/rafael_prepare_alone_20261123")
ROM, STORED = ROOT / "Rafael_Prepare_Alone_STAGED.nds", ROOT / "stored_proof.json"
PATCH, REBUILT, PATCH_PROOF = (ROOT / name for name in ("translation.xdelta", "clean_rebuilt.nds", "clean_patch_proof.json"))
STARTUP_CAPTURE = ROOT / "startup/capture/capture_report.json"
NATIVE = ROOT / "rafael_prepare_alone_native_1_20261123.png"
ARM, COMMON, STORY, BLOCK = parent.ARM, parent.COMMON, review.STORY, review.BLOCK
native = fixed.previous.native
ENGLISH = "That's the spirit! Do your best!"
RATIONALE = "Julio is pleased that Rafael wants to manage on his own. His approval leads right into an encouraging send-off. Both beats fit on one native row."


def stage():
    assert not ROOT.exists()
    release, packet = map(read, (parent.RELEASE, review.OUT))
    assert digest(parent.ROM) == release["candidate_sha256"] == packet["candidate_sha256"]
    assert digest(CLEAN) == release["clean_input_sha256"] and digest(REGISTRY) == release["registry_sha256"]
    assert digest(release["manifest"]) == release["manifest_sha256"]
    assert packet["ordinary_new_game"] and packet["selection"]["selected_slot"] == 1
    row, = [record for record in packet["observations"] if record["id"] == review.RESPONSE]
    assert row["captured"]["frame"] == review.RESPONSE_FRAME
    original, image = map(NdsImage.open, (CLEAN, parent.ROM))
    clean, before = map(native.files, (original, image))
    arm = before[ARM]
    assert sha256(arm).hexdigest() == release["target_ARM9_sha256"]
    assert sha256(before[STORY]).hexdigest() == release["target_SC0_sha256"]
    assert template.right_bound(arm, release["right_bound_configuration"])["matched_repair_spans"] == 8
    source, bank = (IlnkContainer.parse(data[STORY]) for data in (clean, before))
    previous = bank.blocks[BLOCK]
    a = review.panels.exact_command(source.blocks[BLOCK], row["source_reference"])
    b = review.panels.exact_command(previous, row["current_reference"])
    kanji = image.read_file("/GRP/KANJI.FNT")
    context = SimpleNamespace(arm=arm, image=image)
    paint = review.panels.town.clipped_renderer(context)
    proposal = dict(id=review.RESPONSE, english=ENGLISH, protected_phrases=())
    encoded, plan = review.panels.layout.plan_progressive(proposal, b[5], bytes_for(b), bytes_for(a))
    assert plan["lines"] == [ENGLISH] and plan["expected_native_pages"] == 1 and len(encoded) <= len(bytes_for(b))
    display = paint(arm, kanji, encoded)
    page, = display["pages"]
    plane = bytes.fromhex(page["native_plane_hex"])
    assert page["native_independent_plane_equal"] and display["complete_consumed_bytes"] == len(encoded)
    draft = row | dict(installed_reference=row["current_reference"], proposed_English=ENGLISH,
        offline_preflight=dict(formatter_plan=plan, physical_source_and_installed_selectors=a[5],
            native_plane_sha256=sha256(plane).hexdigest()))
    result, (edit,), count = fixed.previous.apply_block(source.blocks[BLOCK], previous, arm, [draft], paint, kanji,
        fixed.explicit_walk())
    stored_command = bytes.fromhex(edit["after_hex"])
    assert display["pages"][0]["native_plane_hex"] == paint(arm, kanji, bytes_for(stored_command))["pages"][0]["native_plane_hex"]
    bank.blocks[BLOCK] = result
    updated = bank.to_bytes()
    directory_end = 8 + (len(bank.blocks) + 1) * 4
    assert updated[:directory_end] == before[STORY][:directory_end]
    image.replace_file(STORY, updated)
    final = native.files(image)
    assert final.keys() == before.keys() and {p for p in final if final[p] != before[p]} == {STORY}
    guard = bind_registered_story_percent_guard(template.previous.guard_spec())(clean, final)
    assert guard["total_exact_source_bound_relocated_leading25_count"] == 7
    assert not any(guard["source_bound_new_command_counts"].values())
    binary = bytes(image.rom.save())
    image.replace_file(STORY, before[STORY])
    assert bytes(image.rom.save()) == parent.ROM.read_bytes()
    ROOT.mkdir()
    ROM.write_bytes(binary)
    assert native.files(NdsImage.open(ROM)) == final
    preview = Image.new("RGB", (256, 384), (250, 245, 226))
    preview.paste(Image.frombytes("L", (216, 64), bytes(12 if pix else 245 for pix in plane)), (16, 296))
    sheets = FunctionType(review.panels.sheets_for.__code__, vars(review.panels) | {"OUT": STORED})
    visual, = sheets("rafael_prepare_alone_native", [(review.RESPONSE, preview)], (0, 288, 256, 366))
    assert visual == reference(NATIVE)
    write(STORED, dict(candidate=reference(ROM), previous=reference(parent.ROM), clean=reference(CLEAN),
        source_review=reference(review.OUT), edit=edit, whole_parent_inverse=True, unchanged_archive_directory=True,
        native_proof=display, visual=visual, native_command_count=count, source25=guard,
        target_SC0_sha256=sha256(updated).hexdigest(), target_block_sha256=sha256(result).hexdigest()))
    print(f"Staged and verified Julio's independent reply. {digest(ROM)}", flush=True)


def check(action):
    stored = read(STORED)
    proof = dict(candidate=str(ROM), candidate_sha256=stored["candidate"]["sha256"],
        predecessor_sha256=stored["previous"]["sha256"], clean_input_sha256=stored["clean"]["sha256"])
    scope = vars(checks) | dict(RELEASE=parent.RELEASE, PATCH=PATCH, REBUILT=REBUILT, STARTUP_CAPTURE=STARTUP_CAPTURE)
    FunctionType(getattr(checks, action).__code__, scope)(proof)
    if action == "patch":
        write(PATCH_PROOF, dict(clean_input_sha256=proof["clean_input_sha256"], candidate=reference(ROM),
            patch=reference(PATCH), rebuilt=reference(REBUILT), byte_exact=True))


if __name__ == "__main__":
    cli = ArgumentParser(description=__doc__)
    cli.add_argument("action", choices=("stage", "patch", "startup"))
    action = cli.parse_args().action
    stage() if action == "stage" else check(action)
