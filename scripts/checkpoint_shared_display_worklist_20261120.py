"""Bind the open shared text to the current release and preserve display coverage."""

from collections import Counter
from pathlib import Path
from struct import unpack_from

from dk4tool.patch.gallery_caption_bounds import validate as gallery_captions
from scripts import checkpoint_shared_display_owners_20261119 as previous
from scripts import register_market_bargaining_20261120 as current
from scripts.checkpoint_pending_shared_native_20261115 import exact_online_dependencies


base = current.base
BOOK = previous.BOOK
OUTPUT = BOOK / "shared_display_worklist_20261120_v1.json"
BASE = previous.BASE
CLEAN, ARM, COMMON = current.stage.CLEAN, current.stage.ARM, current.stage.COMMON
DEPENDENCIES = (
    (0x28B74, 0x28BAC), (0x29F94, 0x29FB8), (0x42C74, 0x42C94), (0x42E5C, 0x42ED4),
    (0x42F58, 0x42F70), (0x42FD0, 0x4300C), (0x432DC, 0x432FC), (0xCED28, 0xCED50),
)


def revalidate_displays(clean, active, previous_image, ledger):
    arm, earlier = (image.read_file(ARM) for image in (active, previous_image))
    for lo, hi in DEPENDENCIES:
        assert arm[lo:hi] == earlier[lo:hi]
    captions = gallery_captions(arm)
    assert captions == gallery_captions(earlier) and len(captions) == 164
    caption_rows = {(r["route"], r["position"]): r for r in captions}
    scene_rows = {r["message_ID"]: r for r in base.load(previous.SCENES)["records"]}
    art = {r["artwork"]["path"]: r["artwork"]["sha256"] for r in scene_rows.values() if r["artwork"]}
    assert len(art) == 168
    for path, digest in art.items():
        assert current.native.digest(clean.read_file(path)) == current.native.digest(active.read_file(path)) == digest
    opening = base.load(previous.OPENINGS)
    assert len(opening["records"]) == 37
    for path, digest in opening["original_visible_asset_sha256"].items():
        assert current.native.digest(active.read_file(path)) == digest

    independent_online = exact_online_dependencies(clean, active)
    assert independent_online == ledger["independent_Online_and_Extras"]
    chooser = {r["id"]: r for r in base.load(previous.CHOOSER)["records"]}
    assert len(chooser) == 4
    for row in chooser.values():
        ref = row["registered_reference"]
        field, size = ref["pointer_field"] - BASE, ref["byte_count"]
        assert all(row["review"].values())
        assert unpack_from("<I", arm, field)[0] == ref["runtime_address"]
        at = ref["ARM9_offset"]
        assert arm[at:at + size].hex() == ref["exact_hex"]
    return caption_rows


def bind_rows(ledger, prior, target, source, captions):
    reference = current.stage.workflow.reference
    shifts = ledger["physical_reference_index_updates"]
    rows = []
    count = Counter()
    for record in prior["records"]:
        n = record["message_ID"]
        installed = target[n]
        current_ref = reference(installed)
        before_ref = record["current_reference"]
        if str(n) in shifts:
            shifted = shifts[str(n)]
            assert before_ref == shifted["previous_reference"] and current_ref == shifted["current_reference"]
            assert shifted["exact_hex"] == record["current_hex"]
        else:
            assert before_ref == current_ref
        assert installed.text.hex() == record["current_hex"]
        assert reference(source[n]) == record["source_reference"] and source[n].text.hex() == record["source_hex"]
        gallery = record["independent_gallery_draw_sources"]
        for entry in gallery:
            before_caption, now = entry["clean"], entry["current"]
            assert before_caption["text_hex"] == record["source_hex"]
            caption = captions[now["route"], now["position"]]
            assert caption["pointer"] == now["pointer"] and caption["bounds"][0] == now["draw_x"]
            assert caption["English"].encode("ascii").hex() == now["text_hex"]
        if gallery:
            scope = "Independent Gallery captions"
        elif record.get("story_still_filename"):
            scope = "Original story artwork filename"
        elif record.get("observed_title_and_route_intros_use_separate_assets"):
            scope = "Independent title or opening assets"
        elif record.get("tested_Online_and_About_Extras_use_separate_ARM9_text"):
            scope = "Independent Online and About Extras pages"
        elif record.get("separate_chooser_biography_review"):
            scope = "Independent captain chooser biography"
        elif record["kind"] == "scene":
            scope = "Scene label without a specific display association"
        else:
            scope = "Legacy dialogue with remaining display questions"
        count[scope] += 1
        rows.append(record | dict(current_reference=current_ref, established_display_scope=scope))
    return rows, count


def main():
    assert not OUTPUT.exists()
    owners, release, review = map(base.load, (previous.OUTPUT, current.RELEASE, current.REVIEW))
    status = base.load(base.LEDGER)
    integrated = status["current_integrated_candidate"]
    assert base.digest(base.REGISTRY) == release["registry_sha256"]
    assert base.digest(CLEAN) == owners["clean_sha256"] == release["clean_input_sha256"]
    assert base.digest(current.ROM) == review["candidate_sha256"] == release["candidate_sha256"] == integrated["sha256"]
    earlier = base.load(previous.current.RELEASE)
    assert base.digest(earlier["candidate"]) == owners["candidate_sha256"] == earlier["candidate_sha256"]
    clean, active, previous_image = map(base.NdsImage.open, (CLEAN, current.ROM, earlier["candidate"]))
    allowed = revalidate_displays(clean, active, previous_image, owners)
    workflow = current.stage.workflow
    arm = active.read_file(ARM)
    archive = active.read_file(COMMON)
    assert workflow.digest(arm) == release["target_ARM9_sha256"]
    assert workflow.digest(archive) == release["target_COMMON_sha256"]
    directory = workflow.digest(arm[workflow.DIRECTORY_OFFSET:workflow.TABLE_OFFSET])
    source = workflow.common_message_entries(clean.read_file(COMMON), clean.read_file(ARM))
    current_entries = workflow.owned_entries(archive, arm, directory)
    records, counts = bind_rows(review, owners, current_entries, source, allowed)
    by_scope = {k: [r["message_ID"] for r in records if r["established_display_scope"] == k] for k in counts}
    assert len(source) == len(current_entries) == 3668
    assert len(records) == 276 == status["pending_shared_consumer_checkpoint_20261114"]["remaining_total"]
    assert status["records_editorially_completed"] == 27700 and not status["full_goal_complete"]
    focus = [n for k, keys in by_scope.items() if k.startswith(("Scene label without", "Legacy dialogue")) for n in keys]
    assert len(focus) == 35
    base.save(OUTPUT, dict(candidate_sha256=release["candidate_sha256"], clean_sha256=release["clean_input_sha256"],
        records=records, counts_by_established_scope=dict(counts), first_investigation_list=sorted(focus),
        remaining_stored_keys=len(records), prior_explicit_display_scope_keys=len(records) - len(focus),
        no_other_display_path_assumed_closed=True, offline_dependency_check=True, new_gameplay_runs=0,
        new_dialogue_credit=0, full_goal_complete=False, evidence={str(p): base.digest(p) for p in
            (previous.OUTPUT, previous.OPENINGS, previous.SCENES, previous.CHOOSER, current.RELEASE, current.REVIEW)}))
    print(f"Rebound {len(records)} shared keys. {len(records) - len(focus)} have specific display or artwork evidence and {len(focus)} are the first investigation list.")


if __name__ == "__main__":
    main()
