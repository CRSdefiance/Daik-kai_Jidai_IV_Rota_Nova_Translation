"""Install only the revised Tavern Schemes text on the registered candidate."""

from types import FunctionType

from scripts import checkpoint_shared_display_owners_20261119 as scope
from scripts import prepare_tavern_strategist_followup_20261119 as review
from scripts.stage_shared_notices_storage_v1 import relocate

base, native, workflow = review.base, review.native, review.workflow
parent = review.parent
ARM, COMMON, CLEAN = native.ARM, review.shared.COMMON, native.CLEAN
ROOT = review.ROOT / "research_v3"
ROM, PROOF = ROOT / "Tavern_Strategist_RESEARCH_ONLY.nds", ROOT / "staged.json"
PENDING = scope.BINDINGS


def main():
    assert not ROOT.exists()
    draft, release = map(base.load, (review.OUTPUT, parent.RELEASE))
    assert draft["candidate_sha256"] == base.digest(parent.ROM) == release["candidate_sha256"]
    assert draft["registry_sha256"] == base.digest(base.REGISTRY) == release["registry_sha256"]
    image = base.NdsImage.open(parent.ROM)
    arm, common = image.read_file(ARM), image.read_file(COMMON)
    assert native.digest(arm) == release["target_ARM9_sha256"] and native.digest(common) == release["target_COMMON_sha256"]
    directory = native.digest(arm[workflow.DIRECTORY_OFFSET:workflow.TABLE_OFFSET])
    rows = {r["message_ID"]: r for r in draft["records"]}
    storage = {ident: bytes.fromhex(row["encoded_hex"]) for ident, row in rows.items() if row["decision"] == "revision"}
    assert storage.keys() == review.EDITS.keys()
    repack = FunctionType(relocate.__code__, relocate.__globals__ | {"DIRECTORY": directory})
    target_common, target_arm, entries, allocation = repack(common, arm, rows, storage)
    assert set(allocation["changed_visible_templates"]) == storage.keys()
    start, end = workflow.DIRECTORY_OFFSET, workflow.TABLE_OFFSET + len(entries) * 4
    assert target_arm[:start] == arm[:start] and target_arm[end:] == arm[end:]
    for item in base.load(PENDING)["records"]:
        row = entries[item["message_ID"]]
        assert workflow.reference(row) == item["current_reference"] and row.text.hex() == item["current_hex"]
    for ident, row in rows.items():
        reference = entries[ident]
        row.update(staged_reference=workflow.reference(reference), staged_hex=reference.text.hex())
        assert workflow.logical(reference.text) == row["english"]
    image.replace_file(COMMON, target_common)
    image.replace_file(ARM, target_arm)
    target = bytes(image.rom.save())
    image.replace_file(COMMON, common)
    image.replace_file(ARM, arm)
    assert bytes(image.rom.save()) == parent.ROM.read_bytes()
    ROOT.mkdir()
    ROM.write_bytes(target)
    base.save(PROOF, draft | dict(candidate_sha256=base.digest(ROM), previous_sha256=base.digest(parent.ROM),
        manuscript_sha256=base.digest(review.OUTPUT), clean_input_sha256=release["clean_input_sha256"],
        target_ARM9_sha256=native.digest(target_arm), target_COMMON_sha256=native.digest(target_common),
        entire_parent_inverse=True, allocation=allocation, records=list(rows.values()),
        pending_storage_dependency=dict(path=PENDING.as_posix(), sha256=base.digest(PENDING), exact_refs_and_payloads=True)))
    print("Staged 15 Tavern templates with exact parent inverse and all 276 pending entries preserved.")


if __name__ == "__main__":
    main()
