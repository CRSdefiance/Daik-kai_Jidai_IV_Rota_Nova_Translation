"""Resolve stored scene labels whose verified story consumer loads artwork by filename."""

from collections import defaultdict
from pathlib import Path

from dk4tool.patch.duel_editorial import owned_entries
from dk4tool.script.common_message_table import DIRECTORY_OFFSET, TABLE_OFFSET, common_message_entries
from scripts import checkpoint_story_still_commands_20261120 as previous
from scripts import register_ending_credit_spacing_20261123 as current
from scripts.reconcile_chooser_and_online_dispositions_20261123 import OUT as EXTRAS
from scripts.reconcile_gallery_caption_dispositions_20261123 import WORKLIST
from scripts.seal_shared_text_source_v1 import reference


base, native = current.base, current.native
SCENE_DRAFTS = previous.owners.SCENES
OUT = EXTRAS.with_name("story_still_label_dispositions_20261123.json")


def verify_commands(catalogue, rom, arm, version):
    walk = previous.explicit_walk()
    planned = defaultdict(set)
    for index, refs in catalogue.items():
        for ref in refs:
            if ref["path"].startswith("/data/"):
                planned[ref["path"], ref["block"]].add(index)
    archives = {path: native.IlnkContainer.parse(rom.read_file(path)).blocks
                for path in {path for path, _ in planned}}
    hits = defaultdict(list)
    for (path, number), wanted in sorted(planned.items()):
        block = archives[path][number]
        _, checked, unresolved = previous.commands(walk, arm, block)
        assert not unresolved, (version, path, number)
        for index in sorted(wanted):
            rows = [row for row in checked.values() if row["image_index"] == index]
            assert rows, (version, path, number, index)
            for row in rows:
                assert row["native_scene_call"] == 0x02028AA8
                hits[index].append(row | dict(path=path, block=number, block_sha256=native.digest(block)))
    assert set(hits) == set(catalogue)
    return hits, len(planned)


def main():
    release, review, worklist, earlier, extras, manuscript = map(base.load,
        (current.RELEASE, current.REVIEW, WORKLIST, previous.OUTPUT, EXTRAS, SCENE_DRAFTS))
    candidate = release["candidate_sha256"]
    assert candidate == base.digest(current.ROM) == review["candidate_sha256"] == extras["candidate_sha256"]
    assert base.digest(base.REGISTRY) == release["registry_sha256"]
    assert base.digest(current.native.CLEAN) == release["clean_input_sha256"] == earlier["clean_sha256"] == worklist["clean_sha256"]
    clean, active = map(base.NdsImage.open, (current.native.CLEAN, current.ROM))
    clean_arm, arm = (image.read_file(current.ARM) for image in (clean, active))
    assert native.digest(arm) == release["target_ARM9_sha256"]
    original = common_message_entries(clean.read_file(current.COMMON), clean_arm)
    common = active.read_file(current.COMMON)
    assert native.digest(common) == release["target_COMMON_sha256"]
    installed = owned_entries(common, arm, native.digest(arm[DIRECTORY_OFFSET:TABLE_OFFSET]))
    bound = {row["message_ID"]: row for row in review["shared_consumer_binding"]["records"]}
    labels = {r["message_ID"]: r for r in earlier["labels"]}
    assets = {r["image_index"]: r for r in earlier["assets"]}
    drafts = {r["message_ID"]: r for r in manuscript["records"]}
    pending = set(extras["remaining_needing_distinct_disposition"])
    selected = [r for r in worklist["records"] if r["message_ID"] in pending and
                r["established_use"] == "Original story artwork filename" and r.get("story_image_request")]
    assert len(selected) == 45
    paths, source_commands, current_commands = {}, {}, {}
    for item in selected:
        key = item["message_ID"]
        index = item["story_image_request"]["image_index"]
        asset = assets[index]
        paths[index] = asset["filename"]
        assert item["story_still_filename"] == paths[index] and labels[key]["image_index"] == index
        before, after = (image.read_file(paths[index]) for image in (clean, active))
        assert before == after and native.digest(before) == asset["asset_hashes"]["clean"]
        source_commands[index] = [r["source"] for r in asset["commands"] if r["source"]["path"].startswith("/data/")]
        current_commands[index] = [r["current"] for r in asset["commands"] if r["current"]["path"].startswith("/data/")]
        assert len(source_commands[index]) == len(current_commands[index]) == item["story_image_request"]["matching_data_commands"]
    assert len(paths) == len(selected)
    clean_hits, source_block_count = verify_commands(source_commands, clean, clean_arm, "clean")
    active_hits, active_block_count = verify_commands(current_commands, active, arm, "installed")
    for index in paths:
        assert clean_hits[index] == source_commands[index]
        # Editorial relocation may shift an offset while retaining the command and its branch.
        assert [(r["path"], r["block"], r["command_hex"], len(r["ancestor_0100_offsets"])) for r in active_hits[index]] == [
            (r["path"], r["block"], r["command_hex"], len(r["ancestor_0100_offsets"])) for r in source_commands[index]]
    loaded = {name: previous.image_requests(data, sorted(paths)) for name, data in (("clean", clean_arm), ("installed", arm))}
    assert loaded == {"clean": 90, "installed": 90}

    rows = []
    for item in selected:
        key = item["message_ID"]
        index = item["story_image_request"]["image_index"]
        jp, en = original[key], installed[key]
        assert jp.text == en.text and jp.text.hex() == item["source_hex"] == item["installed_hex"]
        assert reference(jp) == item["source_reference"] and reference(en) == item["installed_reference"] == bound[key]["installed"]
        assert bound[key]["exact_body_retained"]
        draft = drafts[key]
        assert draft["source_hex"] == jp.text.hex() and draft["english"] == item["earlier_draft"]["english"]
        rows.append(dict(message_ID=key, file_path=current.COMMON, source_reference=reference(jp),
            installed_reference=reference(en), source_Japanese=jp.text.decode("cp932"), exact_COMMON_hex=jp.text.hex(),
            artwork=dict(image_index=index, filename=paths[index], sha256=assets[index]["asset_hashes"]["clean"]),
            contextual_draft=dict(english=draft["english"], localization_note=draft["localization_note"],
                source_meaning=draft["source_meaning"], review=draft["review"]),
            clean_story_commands=clean_hits[index], installed_story_commands=active_hits[index],
            checked_path_disposition="Original story command loads the associated image by filename.",
            direct_COMMON_display_outside_story_loader="Unverified. Retain the exact source and reopen for a distinct caller."))
        pending.remove(key)
    assert len(pending) == 100
    evidence = {str(p): base.digest(p) for p in
        (EXTRAS, current.RELEASE, current.REVIEW, WORKLIST, previous.OUTPUT, SCENE_DRAFTS, Path(previous.__file__), Path(__file__))}
    base.save(OUT, dict(candidate_sha256=candidate, clean_sha256=release["clean_input_sha256"],
        source_storage_inventory=len(bound), completed_prior_display_dispositions=131, story_label_dispositions=rows,
        remaining_needing_distinct_disposition=sorted(pending), verified_production_blocks={"clean": source_block_count,
            "installed": active_block_count}, original_filename_paths_checked=loaded, offline_native_verification=True,
        new_gameplay_runs=0, new_dialogue_credit=0, story_illustrations_edited=False, evidence=evidence))
    print(f"Verified {len(rows)} story image label dispositions and the complete remaining set of {len(pending)}.")


if __name__ == "__main__":
    main()
