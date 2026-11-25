"""Bind B84's original dialogue, choice slots and two installed FE continuations."""

from pathlib import Path

from scripts import prepare_london_guild_assignments_20261118 as pairing
from scripts import register_rafael_east_asia_followup_20261121 as head


base, native = head.base, head.native
RELEASE_INPUT = Path("translations/rafael_B81_B84_editorial_release_v2.json")
ROOT = Path("work/analysis/rafael_tutorial_B84_followup_20261121")
OUTPUT = ROOT / "paired_source_with_pages.json"
ARCHIVE = "/data/SC0.DK4"


def main():
    assert not OUTPUT.exists()
    registered, config = map(base.load, (head.RELEASE, RELEASE_INPUT))
    sha = base.digest(head.ROM)
    assert sha == registered["candidate_sha256"] and base.digest(base.REGISTRY) == registered["registry_sha256"]
    assert base.digest(native.CLEAN) == registered["clean_input_sha256"]
    manuscript, previous = map(base.load, (config["manuscript"], config["reconstruction"]))
    historical, = [row for row in previous["groups"] if row["block"] == 84]
    first, extra = [historical[k] for k in ("first_page_reconstruction", "FE_pagination")]
    old = first["all_current_commands"]
    installed = extra["all_target_commands"]

    images = list(map(base.NdsImage.open, (native.CLEAN, head.ROM)))
    archives = [image.read_file(ARCHIVE) for image in images]
    blocks = [native.IlnkContainer.parse(data).blocks[84] for data in archives]
    assert native.digest(blocks[0]) == historical["clean_sha256"]
    inventory, _, _ = native.scoped_inventory()
    source, target = [inventory(image.read_file(native.ARM), raw)[0] for image, raw in zip(images, blocks, strict=True)]
    assert len(source) == len(old) == 217 and len(installed) == len(target) == 219
    mid, already = [{row["old_offset"]: row["new_offset"] for row in mapping}
                    for mapping in (first["command_map"], extra["original_command_map"])]
    moved = {before["offset"]: after["offset"] for before, after in zip(installed, target, strict=True)}
    current_offsets = {row["offset"]: row for row in target}
    compatible = {a["offset"]: moved[already[mid[b["offset"]]]] for a, b in zip(source, old, strict=True)}
    ends = [pairing.stage.logical_end(block) for block in blocks]
    compatible[ends[0]] = ends[1]
    moved[extra["new_logical_end"]] = ends[1]
    text = (pairing.stage.SPEECH, pairing.stage.STYLE, *pairing.stage.MENU)
    relative = pairing.stage.RELATIVE
    for originals, reference in ((source, compatible), (installed, moved)):
        for left in originals:
            old_at = left["offset"]
            right = current_offsets[reference[old_at]]
            assert left["word"] == right["word"]
            assert [reference[ancestor] for ancestor in left["ancestor_0100_offsets"]] == right["ancestor_0100_offsets"]
            before, after = [bytes.fromhex(item["whole_command_hex"]) for item in (left, right)]
            if left["word"] in relative:
                assert before[:2] == after[:2]
                assert reference[pairing.stage.jump(before, old_at)] == pairing.stage.jump(after, right["offset"])
            elif left["word"] not in text:
                assert before == after

    owners = {}
    for child in extra["continuations"]:
        first_at, second_at = [moved[child[key]] for key in ("first_command_offset", "new_command_offset")]
        a, b = current_offsets[first_at], current_offsets[second_at]
        codes = [bytes.fromhex(row["whole_command_hex"]) for row in (a, b)]
        assert all(code[:6].hex() == child["complete_source_preamble_hex"] for code in codes)
        assert a["ancestor_0100_offsets"] == b["ancestor_0100_offsets"]
        assert first_at + a["native_extent"] == second_at
        owners[first_at] = child["source_ID"], b
    assert set(current_offsets) - set(compatible.values()) == {child["offset"] for _, child in owners.values()}
    previous_rows = [r for r in manuscript["records"] if r["block"] == 84]
    speeches = {row["source_reference"]["offset"]: row for row in previous_rows if row["kind"] != "typed-choice-label"}
    captions = [row for row in previous_rows if row["kind"] == "typed-choice-label"]
    results = []
    for left in source:
        word, at = (left[k] for k in ("word", "offset"))
        if word not in text:
            continue
        right = current_offsets[compatible[at]]
        other = right["offset"]
        raw = [bytes.fromhex(row["whole_command_hex"]) for row in (left, right)]
        pairs = zip(*(pairing.text_records(item, word) for item in raw), strict=True)
        for (ja_rel, selector, ja, slots), (en_rel, en_sel, en, en_slots) in pairs:
            assert selector == en_sel and slots == en_slots
            if word in pairing.stage.MENU:
                previous_row, = [r for r in captions if r["source_command_offset"] == at
                                 and r["source_reference"]["offset"] == at + ja_rel]
            else:
                previous_row = speeches[at + ja_rel]
            ident = previous_row["id"]
            pages = [dict(command_offset=other, body_offset=other + en_rel, body_hex=en.hex(), text=en.decode("cp932"))]
            if other in owners:
                owner, page = owners[other]
                assert ident == owner and selector == 254
                _, _, body, _ = pairing.text_records(bytes.fromhex(page["whole_command_hex"]), word)[0]
                pages.append(dict(command_offset=page["offset"], body_offset=page["offset"] + 5,
                                  body_hex=body.hex(), text=body.decode("cp932")))
            results.append(dict(id=ident, native_command_word=word, source_selector=selector, source_slots=slots,
                                source_command_offset=at, source_offset=at + ja_rel, source_body_hex=ja.hex(),
                                Japanese=ja.decode("cp932"), installed_pages=pages))
    assert {row["id"] for row in results} == {row["id"] for row in previous_rows} and len(results) == 131
    assert len(captions) == 5 and sum(len(r["installed_pages"]) == 2 for r in results) == 2
    ROOT.mkdir(exist_ok=True)
    base.save(OUTPUT, dict(candidate_sha256=sha, profile=registered["profile"], file_path=ARCHIVE, block=84,
        clean_block_sha256=native.digest(blocks[0]), current_block_sha256=native.digest(blocks[1]),
        clean_archive_sha256=native.digest(archives[0]), current_archive_sha256=native.digest(archives[1]),
        historical_reconstruction=config["reconstruction"],
        historical_reconstruction_sha256=base.digest(config["reconstruction"]),
        exact_original_command_targets_and_branch_ancestors=True, original_commands=217, installed_commands=219,
        typed_choice_labels=5, source_review_pending=True, records=results))
    print("Paired 131 B84 records, including five choice labels and both two-page FE bodies.")


if __name__ == "__main__":
    main()
