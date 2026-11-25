"""Bind the remaining COMMON drafts and evidence to the registered review candidate."""

from collections import Counter
from hashlib import sha256
from pathlib import Path

from dk4tool.patch.duel_editorial import owned_entries
from dk4tool.script.common_message_table import DIRECTORY_OFFSET, TABLE_OFFSET, common_message_entries
from scripts import register_all_routes_final_flagged_wraps_20261118 as registered
from scripts.seal_shared_text_source_v1 import reference

base, native = registered.base, registered.native
COMMON = "/COMMON/MESFILE.DK4"
DRAFTS = Path("translations/editorial_checkpoints/SharedText_20261110_v1")
OUTPUT = registered.stage.ROOT / "shared_text_current_binding.json"
LEGACY = DRAFTS / "legacy_dialogue_review_20261115_v1.json"
STORED = DRAFTS / "pending_shared_native_scope_20261115_v1.json"
OPENING = DRAFTS / "opening_scene_labels_20261115_v1.json"
SCENES = Path("translations/common_scene_labels_manuscript_v2.json")
ONLINE = Path("translations/common_online_promotional_manuscript_v3.json")


def by_key(path):
    records = base.load(path)["records"]
    result = {row["message_ID"]: row for row in records}
    assert len(result) == len(records)
    return result


def main():
    release = base.load(registered.RELEASE)
    assert base.digest(base.REGISTRY) == release["registry_sha256"]
    assert base.digest(registered.ROM) == release["candidate_sha256"]
    assert base.digest(native.CLEAN) == release["clean_input_sha256"]
    pending = base.load(base.LEDGER)["pending_shared_consumer_checkpoint_20261114"]
    assert pending["candidate_sha256"] == release["candidate_sha256"]
    clean, image = map(base.NdsImage.open, (native.CLEAN, registered.ROM))
    arm, common = image.read_file(native.ARM), image.read_file(COMMON)
    assert native.digest(arm) == release["target_ARM9_sha256"]
    assert native.digest(common) == release["target_COMMON_sha256"]
    original = common_message_entries(clean.read_file(COMMON), clean.read_file(native.ARM))
    installed = owned_entries(common, arm, sha256(arm[DIRECTORY_OFFSET:TABLE_OFFSET]).hexdigest())

    legacy, stored, scene, online, opening = map(by_key, (LEGACY, STORED, SCENES, ONLINE, OPENING))
    assert set(legacy) == set(pending["remaining_legacy_keys"])
    assert set(stored) == set(scene) | set(online) and not (set(scene) & set(online))
    assert len(legacy) + len(stored) == pending["remaining_total"] == 276
    records = []
    for kind, ledger, drafts in (("legacy", LEGACY, legacy), ("online", ONLINE, online), ("scene", SCENES, scene)):
        ledger_sha256 = base.digest(ledger)
        for index, draft in drafts.items():
            source_row, current_row = original[index], installed[index]
            assert source_row.text.hex() == draft.get("source_hex", draft.get("clean_hex"))
            assert current_row.text.hex() == draft["current_hex"], (kind, index)
            source_ref, current_ref = reference(source_row), reference(current_row)
            assert source_ref == draft.get("source_reference", draft.get("clean_reference"))
            gates = draft["review"]
            assert len(gates) == 5 and not gates["formatting"]
            record = dict(message_ID=index, kind=kind, file_path=COMMON, source_reference=source_ref,
                current_reference=current_ref, source_hex=source_row.text.hex(), current_hex=current_row.text.hex(),
                current_allocation_bytes=current_row.copy_end - current_row.block_offset,
                draft=dict(path=str(ledger), sha256=ledger_sha256, english=draft["english"], review=gates))
            if index in stored:
                prior = stored[index]
                assert prior["stored_hex"] == current_row.text.hex()
                record["prior_display_evidence"] = dict(path=str(STORED), record=index,
                    classification_basis=prior["classification_basis"],
                    independent_display_evidence=prior["independent_display_evidence"],
                    legacy_display_owner=prior["legacy_display_owner"])
                record["artwork_associated"] = bool(prior["artwork_context"] or prior["opening_artwork_context"])
            if index in opening:
                assert opening[index]["current_hex"] == record["current_hex"]
                assert opening[index]["English_draft"] == draft["english"]
            records.append(record)
    counts = Counter(r["kind"] for r in records)
    assert counts == {"legacy": 31, "online": 31, "scene": 214}
    receipt = dict(candidate_sha256=release["candidate_sha256"], clean_sha256=release["clean_input_sha256"],
        arm9_sha256=release["target_ARM9_sha256"], common_sha256=release["target_COMMON_sha256"],
        evidence={str(p): base.digest(p) for p in (LEGACY, STORED, OPENING, SCENES, ONLINE)},
        counts=counts, records=records, caller_and_formatting_scope_open=True,
        new_gameplay_runs=0, new_editorial_credit=0, full_goal_complete=False)
    if OUTPUT.exists():
        assert base.load(OUTPUT) == receipt
    else:
        base.save(OUTPUT, receipt)
    print("Bound all 276 existing COMMON drafts to the registered candidate with exact source and installed bytes.")


if __name__ == "__main__":
    main()
