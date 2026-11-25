"""Stage three source-reviewed lines from Maria's confrontation at Nagasaki."""

from argparse import ArgumentParser
from pathlib import Path
from types import FunctionType

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.script.format_safety_relocated_v2 import bind_registered_story_percent_guard
from scripts import check_supply_ratio_release_inputs_20261123 as checks
from scripts import register_cartridge_title_20261123 as template
from scripts import register_nagasaki_dream_20261123 as parent
from scripts import stage_kurushima_surrender_20261122 as precedent
from scripts import verify_ezo_voyage_20261123 as observed
from scripts.stage_cartridge_title_20261123 import CLEAN, REGISTRY, NdsImage, digest, read, reference, sha256, write


ROOT = Path(".codex-release-work/kurushima_confrontation_wraps_20261123")
ROM, STORED = ROOT / "Kurushima_Confrontation_Wraps_STAGED.nds", ROOT / "stored_proof.json"
PATCH, REBUILT, PATCH_PROOF = (ROOT / name for name in ("translation.xdelta", "clean_rebuilt.nds", "clean_patch_proof.json"))
STARTUP_CAPTURE = ROOT / "startup/capture/capture_report.json"
ARM, COMMON, STORY, BLOCK = parent.ARM, parent.COMMON, observed.STORY, 3
native, renderer = precedent.native, precedent.renderer
PROPOSALS = {
    22: ("You raid the mainland coast and rob people who can't fight back. Is that the way of a proud samurai?",
         ("people who can't fight back.", "Is that the way of a proud samurai?"),
         "Yukihisa answers the insult by invoking a samurai's code of conduct. The whole question stays together after the two direct charges."),
    26: (None, ("So stiff and proper.", "Just the sort I can't stand."),
         "Keep the sneer, the mock appraisal and the personal dismissal. Each beat can sit on its own row without separating the last clause."),
    32: ("Heh heh, FI! Be mine, and you can surrender quietly. I'll spare you and no one else!",
         ("Be mine,", "you can surrender quietly.", "I'll spare you and no one else!"),
         "Kurushima makes his silence-and-surrender offer directly to Maria. She can surrender on his terms and he promises to spare her alone. Keep the given-name token."),
}


def stage():
    assert not ROOT.exists()
    release, gameplay, prior = map(read, (parent.RELEASE, observed.OUT, observed.earlier.REVIEW))
    assert digest(parent.ROM) == release["candidate_sha256"] == gameplay["candidate_sha256"]
    assert digest(REGISTRY) == release["registry_sha256"] and digest(CLEAN) == release["clean_input_sha256"]
    assert [r["id"] for r in gameplay["story"]] == [r["id"] for r in prior["records"]]
    original, image = map(NdsImage.open, (CLEAN, parent.ROM))
    clean, before = map(native.files, (original, image))
    arm = before[ARM]
    assert sha256(arm).hexdigest() == release["target_ARM9_sha256"]
    assert template.right_bound(arm, release["right_bound_configuration"])["matched_repair_spans"] == 8
    japanese, bank = (IlnkContainer.parse(files[STORY]) for files in (clean, before))
    records, changes = [], []
    for row, held in zip(prior["records"], gameplay["story"], strict=True):
        key = int(row["id"].rsplit("_R", 1)[1])
        source_ref, current_ref = row["source_reference"], row["registered_reference"]
        assert source_ref == held["source_reference"]
        assert current_ref["complete_command_hex"] == held["current_reference"]["complete_command_hex"]
        english, phrases, note = PROPOSALS.get(key, (None, (), row["localization_note"]))
        english = english or row["english"]
        changed = key in PROPOSALS
        if changed:
            changes.append(row["id"])
        records.append(row | dict(context=row["context"], english=english, previous_English=row["english"],
            current_reference=current_ref, current_hex=current_ref["exact_stored_hex"], protected_phrases=phrases,
            localization_note=note, decision="revision" if changed else "retention",
            change_class=("wording" if english != row["english"] else "wrap-only") if changed else "retention",
            review=row["review"] | ({"formatting": False} if changed else {}), previous_gameplay=held["captured"]))

    inventory, _, _ = native.scoped_inventory()
    old_block = bank.blocks[BLOCK]
    compiled, commands, plans = precedent.compiler.rebuild_function()(records, japanese.blocks[BLOCK], old_block,
        inventory, clean[ARM], arm, None)
    assert set(plans) == set(changes) and all(row["expected_native_pages"] == 1 for row in plans.values())
    assert [row["record_ids"][0] for row in commands if row["stored"] != row["current"] and row["record_ids"]] == changes
    bank.blocks[BLOCK] = compiled
    image.replace_file(STORY, bank.to_bytes())
    final = native.files(image)
    assert final.keys() == before.keys() and {path for path in final if final[path] != before[path]} == {STORY}
    before_blocks, after_blocks = (IlnkContainer.parse(data[STORY]).blocks for data in (before, final))
    assert [i for i, (a, b) in enumerate(zip(before_blocks, after_blocks, strict=True)) if a != b] == [BLOCK]
    guard = bind_registered_story_percent_guard(template.previous.guard_spec())(clean, final)
    assert guard["total_exact_source_bound_relocated_leading25_count"] == 7
    assert not any(guard["source_bound_new_command_counts"].values())
    binary = bytes(image.rom.save())
    image.replace_file(STORY, before[STORY])
    assert bytes(image.rom.save()) == parent.ROM.read_bytes()
    ROOT.mkdir()
    ROM.write_bytes(binary)
    assert native.files(NdsImage.open(ROM)) == final
    write(STORED, dict(candidate=reference(ROM), previous=reference(parent.ROM), clean=reference(CLEAN),
        source_review=reference(observed.OUT), changed_file=STORY, changed_block=BLOCK, changed_ids=changes,
        target_SC3_sha256=sha256(final[STORY]).hexdigest(), target_ARM9_sha256=release["target_ARM9_sha256"],
        target_COMMON_sha256=release["target_COMMON_sha256"], before_block_sha256=sha256(old_block).hexdigest(),
        target_block_sha256=sha256(compiled).hexdigest(), commands=commands, records=records, plans=plans,
        whole_parent_inverse=True, source25=guard))
    print(f"Staged two wording revisions and one wrap-only revision. {digest(ROM)}")


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
