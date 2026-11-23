"""Carry forward exact shared text and still-image evidence to the registered ROM."""

from collections import Counter
from hashlib import sha256

from dk4tool.formats.ilnk import IlnkContainer
from scripts import checkpoint_shared_display_worklist_20261120 as worklist
from scripts import checkpoint_story_still_commands_20261120 as still
from scripts import register_hangzhou_veracruz_trends_20261121 as current
from scripts import register_item_advice_phrase_wraps_20261121 as prior


base = current.base
PREVIOUS = worklist.BOOK / "shared_display_worklist_20261121_v2.json"
OUTPUT = worklist.BOOK / "shared_display_worklist_20261121_v3.json"
ARM, COMMON, CLEAN = worklist.ARM, worklist.COMMON, worklist.CLEAN
workflow = worklist.current.stage.workflow


def entries(image):
    arm = image.read_file(ARM)
    directory = sha256(arm[workflow.DIRECTORY_OFFSET:workflow.TABLE_OFFSET]).hexdigest()
    return workflow.owned_entries(image.read_file(COMMON), arm, directory)


def reconcile_stills(proof, clean, older, active):
    archive_rows, original_blocks, current_blocks = {}, {}, {}
    for path, known in proof["archive_results"]["installed"].items():
        source, before, after = (image.read_file(path) for image in (clean, older, active))
        assert sha256(source).hexdigest() == proof["archive_results"]["clean"][path]["archive_sha256"]
        assert sha256(before).hexdigest() == known["archive_sha256"]
        original_blocks[path], old, new = (IlnkContainer.parse(data).blocks for data in (source, before, after))
        current_blocks[path] = new
        updated = [i for i, (a, b) in enumerate(zip(old, new, strict=True)) if a != b]
        assert all(not still.POSSIBLE.search(blocks[i], 8) for i in updated for blocks in (old, new))
        archive_rows[path] = dict(sha256=sha256(after).hexdigest(), changed_blocks=updated)

    hits = Counter()
    for asset in proof["assets"]:
        path = asset["filename"]
        for version, image in (("clean", clean), ("installed", active)):
            assert sha256(image.read_file(path)).hexdigest() == asset["asset_hashes"][version]
        for pair in asset["commands"]:
            for version, blocks in (("source", original_blocks), ("current", current_blocks)):
                ref = pair[version]
                block = blocks[ref["path"]][ref["block"]]
                offset, command = ref["byte_offset"], bytes.fromhex(ref["command_hex"])
                assert sha256(block).hexdigest() == ref["block_sha256"]
                assert block[offset:offset + len(command)] == command
            path = pair["current"]["path"]
            hits["testdata" if path.startswith("/testdata/") else "data"] += 1
    assert hits == {"data": 781, "testdata": 781}
    # Earlier command extents remain in byte-identical blocks. Verify today's filename path.
    requests = still.image_requests(active.read_file(ARM), [row["image_index"] for row in proof["assets"]])
    assert requests == 432
    return dict(archives=archive_rows, command_hits=dict(hits), native_filename_requests=requests)


def main():
    assert not OUTPUT.exists()
    release, previous_release, previous, proof = map(base.load, (current.RELEASE, prior.RELEASE, PREVIOUS, still.OUTPUT))
    status = base.load(base.LEDGER)
    assert base.digest(base.REGISTRY) == release["registry_sha256"]
    assert base.digest(current.ROM) == release["candidate_sha256"] == status["current_integrated_candidate"]["sha256"]
    assert base.digest(prior.ROM) == previous_release["candidate_sha256"] == previous["candidate_sha256"]
    assert base.digest(still.registered.ROM) == proof["candidate_sha256"]
    assert base.digest(CLEAN) == release["clean_input_sha256"] == previous["clean_sha256"] == proof["clean_sha256"]
    clean, active, older, previous_image = map(base.NdsImage.open, (CLEAN, current.ROM, still.registered.ROM, prior.ROM))
    assert active.read_file(ARM) == previous_image.read_file(ARM)
    assert sha256(active.read_file(ARM)).hexdigest() == release["target_ARM9_sha256"]
    assert sha256(active.read_file(COMMON)).hexdigest() == release["target_COMMON_sha256"]
    origin = worklist.previous
    caption_candidate = base.load(origin.current.RELEASE)["candidate"]
    captions = worklist.revalidate_displays(clean, active, base.NdsImage.open(caption_candidate), base.load(origin.OUTPUT))
    scene = reconcile_stills(proof, clean, older, active)

    source = workflow.common_message_entries(clean.read_file(COMMON), clean.read_file(ARM))
    before, after = map(entries, (previous_image, active))
    labels = {row["message_ID"]: row for row in proof["labels"] if row["data_command_count"]}
    assert len(labels) == 163 and len(captions) == 164
    changed_refs, rows = {}, []
    for row in previous["records"]:
        key = row["message_ID"]
        assert source[key].text.hex() == row["source_hex"] and workflow.reference(source[key]) == row["source_reference"]
        assert before[key].text == after[key].text and after[key].text.hex() == row["current_hex"]
        assert workflow.reference(before[key]) == row["current_reference"]
        new_ref = workflow.reference(after[key])
        if new_ref != row["current_reference"]:
            changed_refs[key] = dict(previous=row["current_reference"], current=new_ref)
        updated = row | dict(current_reference=new_ref)
        if key in labels:
            label = labels[key]
            assert label["source_reference"] == row["source_reference"]
            updated["story_image_request"] = dict(
                image_index=label["image_index"], matching_data_commands=label["data_command_count"],
                matching_testdata_commands=label["testdata_command_count"],
                stored_text_display_gate="open",
            )
        rows.append(updated)
    assert len(rows) == 276 == status["pending_shared_consumer_checkpoint_20261114"]["remaining_total"]
    assert sum("story_image_request" in row for row in rows) == len(labels)
    evidence = {str(path): base.digest(path) for path in (PREVIOUS, still.OUTPUT, current.RELEASE, prior.RELEASE)}
    base.save(OUTPUT, previous | dict(
        candidate_sha256=release["candidate_sha256"], records=rows, preceding_rebind=str(PREVIOUS),
        current_reference_changes=changed_refs, registered_release=str(current.RELEASE),
        registered_review=str(current.REVIEW), independent_gallery_captions=len(captions),
        story_still_reconciliation=scene, newest_evidence=evidence,
    ))
    print(f"Checked {len(rows)} stored rows and verified {len(labels)} story artwork associations.")
    print(f"{len(changed_refs)} stored references moved. Verified {sum(scene['command_hits'].values())} still commands.")


if __name__ == "__main__":
    main()
