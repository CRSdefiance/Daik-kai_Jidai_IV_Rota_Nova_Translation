"""Stage Gerhard's source-reviewed recruitment advice in its original text slot."""

from argparse import ArgumentParser
from pathlib import Path
from types import FunctionType, SimpleNamespace

from dk4tool.script.format_safety_relocated_v2 import bind_registered_story_percent_guard
from scripts import check_supply_ratio_release_inputs_20261123 as checks
from scripts import register_cartridge_title_20261123 as template
from scripts import stage_genoa_alternate_dialogue_20261123 as fixed
from scripts import verify_riga_auto_dock_20261124 as review
from scripts.stage_cartridge_title_20261123 import CLEAN, REGISTRY, NdsImage, digest, read, reference, sha256, write


ROOT = Path(".codex-release-work/stockholm_recruiting_20261124")
ROM, STORED = ROOT / "Stockholm_Recruiting_STAGED.nds", ROOT / "stored_proof.json"
PATCH, REBUILT, PATCH_PROOF = (ROOT / name for name in ("translation.xdelta", "clean_rebuilt.nds", "clean_patch_proof.json"))
STARTUP_CAPTURE = ROOT / "startup/capture/capture_report.json"
parent, panels = review.run.current, review.panels
ARM, COMMON, STORY, BLOCK = parent.ARM, parent.COMMON, panels.STORY, 134
native = fixed.previous.native


def stage():
    assert not ROOT.exists()
    release, packet = map(read, (parent.RELEASE, review.OUT))
    assert digest(parent.ROM) == release["candidate_sha256"] == packet["candidate_sha256"]
    assert digest(CLEAN) == release["clean_input_sha256"] and digest(REGISTRY) == release["registry_sha256"]
    assert digest(release["manifest"]) == release["manifest_sha256"] and packet["ordinary_existing_battery_save"]
    proposal = packet["open_revision"]
    assert reference(proposal["contact_sheet"]["path"]) == proposal["contact_sheet"]
    row, = [r for r in packet["recruiting"] if r["id"] == proposal["id"]]
    assert row["decision"] == "revision proposed" and all(row["review"].values())

    clean_rom, image = map(NdsImage.open, (CLEAN, parent.ROM))
    clean, before = map(native.files, (clean_rom, image))
    arm = before[ARM]
    assert sha256(arm).hexdigest() == release["target_ARM9_sha256"]
    assert sha256(before[COMMON]).hexdigest() == release["target_COMMON_sha256"]
    assert template.right_bound(arm, release["right_bound_configuration"])["matched_repair_spans"] == 8
    source, prior = (panels.IlnkContainer.parse(data[STORY]).blocks[BLOCK] for data in (clean, before))
    walk = fixed.explicit_walk()
    src = row["source_reference"]
    at = src["command_offset"]
    exact, = [r for r in walk(arm, source)["rows"] if r["offset"] == at]
    original = source[at:at + exact["native_extent"]]
    installed = panels.exact_command(prior, row["installed_reference"])
    source_body = bytes.fromhex(src["exact_body_hex"])
    assert panels.bytes_for(original) == source_body and original[:6] == installed[:6]
    encoded, plan = panels.layout.plan_progressive(proposal, installed[5], panels.bytes_for(installed), source_body)
    assert encoded.hex() == proposal["exact_fitted_body_hex"] and plan["lines"] == proposal["lines"]
    plane_sha = sha256(bytes.fromhex(proposal["native_preview"]["native_plane_hex"])).hexdigest()
    draft = row | dict(block=BLOCK, source_reference=src | {"exact_command_hex": original.hex()},
        proposed_English=proposal["english"], offline_preflight=dict(formatter_plan=plan,
            physical_source_and_installed_selectors=installed[5], native_plane_sha256=plane_sha))
    paint = panels.town.clipped_renderer(SimpleNamespace(image=image, arm=arm))
    kanji = image.read_file("/GRP/KANJI.FNT")
    result, (edit,), count = fixed.previous.apply_block(source, prior, arm, [draft], paint, kanji, walk)

    bank = panels.IlnkContainer.parse(before[STORY])
    bank.blocks[BLOCK] = result
    updated = bank.to_bytes()
    directory_end = 8 + (len(bank.blocks) + 1) * 4
    assert updated[:directory_end] == before[STORY][:directory_end]
    image.replace_file(STORY, updated)
    final = native.files(image)
    assert final.keys() == before.keys() and {k for k in final if final[k] != before[k]} == {STORY}
    guard = bind_registered_story_percent_guard(template.previous.guard_spec())(clean, final)
    assert guard["total_exact_source_bound_relocated_leading25_count"] == 7 and not any(guard["source_bound_new_command_counts"].values())
    binary = bytes(image.rom.save())
    image.replace_file(STORY, before[STORY])
    assert bytes(image.rom.save()) == parent.ROM.read_bytes()
    ROOT.mkdir()
    ROM.write_bytes(binary)
    assert native.files(NdsImage.open(ROM)) == final
    write(STORED, dict(candidate=reference(ROM), previous=reference(parent.ROM), clean=reference(CLEAN),
        source_review=reference(review.OUT), edit=edit, whole_parent_inverse=True, unchanged_archive_directory=True,
        visual=proposal["contact_sheet"], native_command_count=count, source25=guard,
        target_SC1_sha256=sha256(updated).hexdigest(), target_block_sha256=sha256(result).hexdigest()))
    print(f"Staged and verified Gerhard's recruiting advice. {digest(ROM)}", flush=True)


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
