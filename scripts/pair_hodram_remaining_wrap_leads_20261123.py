"""Bind all remaining flagged Hodram exchanges and their later accepted versions."""

from inspect import getsource
from pathlib import Path

from scripts import pair_hodram_late_story_wraps_20261123 as prior
from scripts.source_locked_derivation_v5118 import checked_text


PARENT = Path("releases/all_routes_editorial_20261123_observed_wrap_followups_candidate/release_manifest.json")
QUEUE = Path("translations/editorial_checkpoints/observed_wrap_followups_20261123/current_wrap_queue.json")
OUTPUT = Path("translations/editorial_checkpoints/hodram_remaining_wrap_leads_20261123/paired_source.json")
INTERVALS = {
    "B221_B240": (221, 224, 225, 226, 227, 228, 229, 231, 232, 237, 238, 239, 240),
    "B241_B260": (242, 243, 246, 247, 251, 252, 254, 255, 258),
    "B261_B291": (266, 274, 279, 281, 282, 283, 286, 287, 291),
    "B292_B310": (294, 297, 298, 305, 309),
}
OVERLAYS = {
    238: "B241_B260",
    243: "B261_B291",
    283: "B292_B310",
    286: "B292_B310",
    294: "B311_B324",
    309: "B311_B324",
}


def overlay(block, records, live_hash, reviews):
    package = Path(f"releases/all_routes_editorial_20261122_hodram_{OVERLAYS[block]}_candidate")
    path = package / "verification/registered_review.json"
    base = prior.prior.base
    reviews[path.as_posix()] = base.digest(path)
    assert reviews[path.as_posix()] == base.load(package / "checksums.json")["verification/registered_review.json"]
    later = {row["id"]:row for row in base.load(path)["records"]
             if row["file_path"] == prior.prior.ARCHIVE and row["block"] == block}
    assert later.keys() == {row["id"] for row in records}, (block, path)
    for row in later.values():
        assert row["registered_reference"]["block_sha256"] == live_hash, (block, row["id"])
    return [later[row["id"]] for row in records], path


scope = prior.scope | globals()
source = checked_text(prior.source, {
    "len(groups) == 17 and wraps == 22": "len(groups) == 36 and wraps == 46",
    "    assert not OUTPUT.exists()": "    assert sum(counts.values()) == 663 and not OUTPUT.exists()",
})
exec(compile(source, __file__ + "::remaining-source-packet", "exec"), scope)


if __name__ == "__main__":
    scope["main"]()
