"""Pair Rafael's Alexandria recruitment and ship lessons with the registered ROM."""

from collections import Counter
from pathlib import Path

from scripts import register_rafael_basra_and_map_keys_20261123 as release
from scripts.pair_rafael_midroute_exchanges_20261122 import ARCHIVE, bind_block


base, native = release.base, release.native
BLOCKS = (176, 177, 178, 179, 180)
EARLIER = tuple(Path(f"translations/rafael_{span}_final_review_v1.json")
                for span in ("B170_B176", "B177_B180"))
CHECKPOINTS = Path("translations/editorial_checkpoints")
QUEUE = CHECKPOINTS / "rafael_basra_and_map_keys_20261123/current_wrap_queue.json"
OUTPUT = CHECKPOINTS / "rafael_ship_lessons_20261123/paired_source.json"


def main():
    registered, queue = (base.load(path) for path in (release.RELEASE, QUEUE))
    candidate = base.digest(release.ROM)
    assert candidate == registered["candidate_sha256"] == queue["candidate_sha256"]
    assert base.digest(base.REGISTRY) == registered["registry_sha256"]
    assert base.digest(release.MANIFEST) == registered["manifest_sha256"]
    assert base.digest(native.CLEAN) == registered["clean_input_sha256"]
    images = [base.NdsImage.open(path) for path in (native.CLEAN, release.ROM)]
    arms = [image.read_file(native.ARM) for image in images]
    assert native.digest(arms[1]) == registered["target_ARM9_sha256"]
    archives = [image.read_file(ARCHIVE) for image in images]
    archive_hashes = [native.digest(data) for data in archives]
    assert archive_hashes[1] == registered["target_SC0_sha256"]
    banks = [native.IlnkContainer.parse(data).blocks for data in archives]
    inventory, _, _ = native.scoped_inventory()

    earlier = [row for path in EARLIER for row in base.load(path)["records"] if row["block"] in BLOCKS]
    groups = []
    for number in BLOCKS:
        records = [row for row in earlier if row["block"] == number]
        owners = {row["source_reference"]["offset"]: row for row in records}
        assert len(owners) == len(records)
        leads = {row["offset"]: row for row in queue["records"]
                 if row["file_path"] == ARCHIVE and row["block"] == number and "reviewed" not in row}
        group = bind_block(number, [bank[number] for bank in banks], arms, archive_hashes,
                           owners, leads, inventory)
        group["earlier_scene_context"] = records[0]["context"]
        groups.append(group)

    counts = Counter(row["native_command_word"] for group in groups for row in group["records"])
    wraps = sum(len(group["open_wrap_leads"]) for group in groups)
    assert counts == {0x4000: 209, 0x2100: 8} and wraps == 11, (counts, wraps)
    assert not OUTPUT.exists()
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    base.save(OUTPUT, dict(candidate_sha256=candidate, clean_sha256=registered["clean_input_sha256"],
        profile=registered["profile"], groups=groups, wrap_queue_sha256=base.digest(QUEUE),
        earlier_reviews={str(path): base.digest(path) for path in EARLIER},
        contextual_review_pending=True, new_review_credit=0))
    print(f"Paired {sum(counts.values())} texts and {wraps} wrap leads across five complete blocks.")


if __name__ == "__main__":
    main()
