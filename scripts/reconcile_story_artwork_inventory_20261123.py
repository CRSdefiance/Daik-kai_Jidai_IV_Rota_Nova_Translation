"""Rebind the original story still catalogue and the two remaining label scopes."""

from collections import defaultdict
from pathlib import Path
import re

from PIL import Image, ImageDraw

from dk4tool.graphics.pxl import PxlImage
from scripts import checkpoint_story_still_commands_20261120 as story
from scripts.reconcile_final_shared_artwork_leads_20261123 import (
    DRAFTS, OUT as PREVIOUS, base, current, native, visual_commands,
)


OUT = PREVIOUS.with_name("story_artwork_inventory_20261123.json")
SHEET = OUT.with_suffix(".png")
OLD_RELEASE = Path("releases/all_routes_editorial_20261120_tavern_help_candidate/verification/registered_release_verification.json")
CENSUS = current.REVIEW.with_name("current_route_coverage_20261123.json")
MARIA = Path("translations/maria_B37_B49_final_review_v1.json")
IMAGE_ID = re.compile(r"/evstill/evstill(\d{3})\.pxl")
DECODER_SPANS = ((0x293B8, 0x2A600), (0x28A28, 0x28A64), (0x28AA8, 0x28BAC))
PAIRS = {
    3401: ("/data/SC0.DK4", (0x4B, 0x08), {48: [], 145: [8, 9, 126, 126], 150: []}),
    3490: ("/data/SC3.DK4", (0x03, 0x1C), {30: [], 46: [241]}),
}


def old_commands(history):
    by_block = defaultdict(list)
    for art in history["assets"]:
        for item in art["commands"]:
            for version in ("source", "current"):
                row = item[version]
                by_block[version, row["path"], row["block"]].append(row)
    for rows in by_block.values():
        rows.sort(key=lambda row: row["byte_offset"])
    return by_block


def command_signature(rows):
    return [(r["opcode"], r["operand"], r["image_index"], len(r["ancestor_0100_offsets"])) for r in rows]


def refresh_commands(clean, old, active, history):
    paths = tuple(path for path in history["archive_results"]["installed"] if path.startswith("/data/"))
    by_block = old_commands(history)
    ja, before_arm, en = (image.read_file(current.ARM) for image in (clean, old, active))
    for start, end in DECODER_SPANS:
        assert ja[start:end] == before_arm[start:end] == en[start:end]
    walk = story.explicit_walk()
    archive_proof, active_refs = {}, {}
    for path in paths:
        source, prior, final = (image.read_file(path) for image in (clean, old, active))
        a, b, c = (native.IlnkContainer.parse(image).blocks for image in (source, prior, final))
        assert native.digest(source) == history["archive_results"]["clean"][path]["archive_sha256"]
        frozen = history["archive_results"]["installed"][path]
        assert native.digest(prior) == frozen["archive_sha256"] and not frozen["unresolved"]
        details = []
        for index, (jp, before, after) in enumerate(zip(a, b, c, strict=True)):
            original = by_block.get(("source", path, index), [])
            expected = by_block.get(("current", path, index), [])
            for block, rows in ((jp, original), (before, expected)):
                for row in rows:
                    pos, command = row["byte_offset"], bytes.fromhex(row["command_hex"])
                    assert block[pos:pos + len(command)] == command
            assert command_signature(original) == command_signature(expected)
            if before == after:
                active_refs[path, index] = expected
                continue
            _, found, unresolved = story.commands(walk, en, after)
            assert not unresolved, (path, index)
            actual = [found[n] for n in sorted(found)]
            assert command_signature(actual) == command_signature(original), (path, index)
            active_refs[path, index] = actual
            details.append(dict(block=index, prior_sha256=native.digest(before), current_sha256=native.digest(after),
                current_still_commands=actual))
        total = sum(len(active_refs[path, index]) for index in range(len(c)))
        assert total == frozen["counts"]["native_still_commands"]
        archive_proof[path] = dict(current_archive_sha256=native.digest(final), still_commands=total,
            rechecked_changed_blocks=details, exact_reused_blocks=len(c) - len(details))
        print(f"{path}: bound {total} still requests; checked {len(details)} changed blocks.", flush=True)
    for path, result in history["archive_results"]["installed"].items():
        if path.startswith("/testdata/"):
            assert old.read_file(path) == active.read_file(path)
            assert native.digest(active.read_file(path)) == result["archive_sha256"]
    return archive_proof, active_refs


def paired_speakers(active, coverage):
    result = defaultdict(dict)
    for path, reference in coverage["routes"].items():
        assert native.digest(active.read_file(path)) == reference["installed_archive_sha256"]
        source = reference["source_census"]
        assert base.digest(source["path"]) == source["sha256"]
        data = base.load(source["path"])
        assert not data["missing"] and len(data["records"]) == reference["exact_credited_clean_positions"]
        by_block = defaultdict(lambda: defaultdict(list))
        for item in data["records"]:
            if item["kind"] != "ordinary-speech" or not item["source_hex"]:
                continue
            actor = int(item["source_hex"][:2], 16)
            by_block[item["block"]][actor].append(item["id"])
        for key, (expected_route, actors, expected_blocks) in PAIRS.items():
            groups = {block: [speaker[i] for i in actors] for block, speaker in by_block.items()
                      if all(i in speaker for i in actors)}
            assert set(groups) == (expected_blocks.keys() if path == expected_route else set())
            if groups:
                result[key] = groups
    return result


def maria_entrance(clean, active, calls):
    path, n = PAIRS[3490][0], 46
    clean_block, installed_block = [native.IlnkContainer.parse(rom.read_file(path)).blocks[n] for rom in (clean, active)]
    walk = story.explicit_walk()
    source_calls, active_calls = [visual_commands(walk, rom.read_file(current.ARM), block)
                                  for rom, block in ((clean, clean_block), (active, installed_block))]
    prior_calls = calls[path, n]
    assert active_calls == [{k: r[k] for k in active_calls[0]} for r in prior_calls]
    assert command_signature(active_calls) == command_signature(source_calls)
    assert [r["image_index"] for r in active_calls] == [241]
    art = "/evstill/evstill241.pxl"
    assert clean.read_file(art) == active.read_file(art)
    indexes = ["DK4_MES_B46_R0004", "DK4_MES_B46_R0013", "DK4_MES_B46_R0017", "DK4_MES_B46_R0021"]
    reviewed = {r["id"]: r for r in base.load(MARIA)["records"] if r.get("block") == n}
    rows = []
    for key in indexes:
        row = reviewed[key]
        before, after = row["source_reference"], row["planned_integrated_reference"]
        a, b = bytes.fromhex(row["source_hex"]), bytes.fromhex(after["exact_stored_hex"])
        assert clean_block[before["offset"]:before["offset"] + len(a)] == a
        assert installed_block[after["offset"]:after["offset"] + len(b)] == b
        assert all(row["review"].values())
        rows.append({k: row[k] for k in ("id", "speaker", "source_Japanese", "english", "source_reference",
                                           "source_hex", "planned_integrated_reference", "review")})
    for refs, event in (("source_reference", source_calls[0]), ("planned_integrated_reference", active_calls[0])):
        voices = [row[refs]["offset"] for row in rows]
        assert voices[0] < event["byte_offset"] < voices[1] < voices[2] < voices[3]
    return dict(asset=art, asset_sha256=native.digest(active.read_file(art)), clean_call=source_calls[0],
        installed_call=active_calls[0], contextual_exchange=rows,
        verified_scope="Clifford's independent entrance artwork in his exchange with Maria.")


def draw_sheet(rom):
    examples = [(8, "Arcadius reveal, first still"), (9, "Arcadius reveal, second still"),
                (126, "Inn background"), (241, "Clifford's entrance in Maria B46")]
    panel = Image.new("RGB", (1024, 213), "#172630")
    draw = ImageDraw.Draw(panel)
    for i, (index, label) in enumerate(examples):
        x = i * 256
        art = PxlImage.from_bytes(rom.read_file(f"/evstill/evstill{index:03}.pxl")).render()
        draw.text((x + 5, 3), f"{index:03}  {label}", fill="white")
        panel.paste(art, (x, 19))
    panel.save(SHEET)


def main():
    release, previous, history, old_release, coverage = map(base.load,
        (current.RELEASE, PREVIOUS, story.OUTPUT, OLD_RELEASE, CENSUS))
    assert base.digest(current.ROM) == release["candidate_sha256"] == previous["candidate_sha256"]
    assert base.digest(base.REGISTRY) == release["registry_sha256"]
    assert base.digest(native.CLEAN) == release["clean_input_sha256"] == history["clean_sha256"]
    assert set(previous["remaining_without_scoped_disposition"]) == PAIRS.keys()
    old_path = Path(old_release["candidate"])
    assert base.digest(old_path) == old_release["candidate_sha256"] == history["candidate_sha256"]
    clean, old, active = map(base.NdsImage.open, (native.CLEAN, old_path, current.ROM))
    archives, requests = refresh_commands(clean, old, active, history)
    fired = sum(item["still_commands"] for item in archives.values())
    assert fired == 781
    paired = paired_speakers(active, coverage)
    for key, (path, _, expected) in PAIRS.items():
        for block in paired[key]:
            assert [r["image_index"] for r in requests[path, block]] == expected[block]
    labels = {row["message_ID"]: row for row in history["labels"]}
    adjacency = {key: [(n, labels[n]["image_index"]) for n in (key - 1, key, key + 1)] for key in PAIRS}
    assert adjacency == {3401: [(3400, 5), (3401, None), (3402, 6)], 3490: [(3489, 91), (3490, None), (3491, 92)]}
    maria = maria_entrance(clean, active, requests)
    indices = {0, 5, 6, 8, 9, 91, 92, 126, 241}
    for binary in (clean, active):
        assert story.image_requests(binary.read_file(current.ARM), sorted(indices)) == 2 * len(indices)
    stored_files = sorted(int(IMAGE_ID.fullmatch(p)[1]) for _, p, _ in active.iter_files() if IMAGE_ID.fullmatch(p))
    assert stored_files == list(range(243))
    known = {r["image_index"] for r in history["labels"] if r["image_index"] is not None} | {234, 238}
    unassigned = sorted(set(stored_files) - known)
    art_search = Path(".codex-release-work/shared_display_20261123/final_labels")
    atlases = sorted(art_search.glob("unpaired_stills_*.png"))
    assert len(unassigned) == 73 and len(atlases) == 4
    rows = []
    for row in previous["records"]:
        key = row["message_ID"]
        if key not in PAIRS:
            continue
        path, actors, expected = PAIRS[key]
        assert row["draft_english_retained"] == DRAFTS[key][0]
        info = dict(scoped_display=True, route=path, original_ordinary_actor_selectors=list(actors),
            verified_target_stills_by_paired_speech_block=expected, qualifying_source_speech_ids=paired[key],
            neighbouring_archived_labels=adjacency[key], exact_archived_image_assignment_unverified=True)
        if key == 3490:
            info.update(independent_entrance_image=maria)
        else:
            info.update(verified_scope="The three DS story blocks with both speakers use inline dialogue. The only still requests among them are the independently identified Arcadius reveal and inn images.")
        rows.append(row | info)
    assert len(rows) == 2
    draw_sheet(active)
    base.save(OUT, dict(candidate_sha256=release["candidate_sha256"], archived_story_labels=rows,
        still_file_count=len(stored_files), original_verified_production_still_requests=fired, production_archives=archives,
        remaining_without_scoped_disposition=[], exact_archived_artwork_identities_open=previous["exact_archived_artwork_identities_open"],
        still_review_additional_indices=unassigned, visual_sheets={str(p): base.digest(p) for p in atlases},
        independent_still_filename_requests_per_binary=2 * len(indices), actual_gameplay_runs=0, hardware=False, new_ROM=False,
        sheet=dict(path=str(SHEET), sha256=base.digest(SHEET)), evidence={str(p): base.digest(p) for p in (
            PREVIOUS, story.OUTPUT, OLD_RELEASE, CENSUS, MARIA, current.RELEASE, Path(__file__))}))
    print(f"Bound {fired} original still requests and documented the DS scope for both remaining labels.")


if __name__ == "__main__":
    main()
