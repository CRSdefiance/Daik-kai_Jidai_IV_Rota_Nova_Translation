"""Bind the next 17 complete Hodram exchanges to the active registered build."""

from inspect import getsource
from pathlib import Path

from scripts import pair_hodram_late_midroute_wraps_20261123 as prior
from scripts.source_locked_derivation_v5118 import checked_text


PARENT = Path("releases/all_routes_editorial_20261123_hodram_late_midroute_wraps_candidate/release_manifest.json")
QUEUE = Path("translations/editorial_checkpoints/hodram_late_midroute_wraps_20261123/current_wrap_queue.json")
OUTPUT = Path("translations/editorial_checkpoints/hodram_late_story_wraps_20261123/paired_source.json")
INTERVALS = {
    "B181_B200": (181, 185, 186, 192, 197, 200),
    "B201_B220": (201, 204, 205, 207, 211, 212, 214, 215, 216, 217, 218),
}
OVERLAYS = {
    192: "all_routes_editorial_20261122_osaka_glass_candidate",
    218: "all_routes_editorial_20261122_hodram_B221_B240_candidate",
}


def overlay(block, records, live_hash, reviews):
    package = Path("releases") / OVERLAYS[block]
    path = package / "verification/registered_review.json"
    base = prior.base
    reviews[path.as_posix()] = base.digest(path)
    assert reviews[path.as_posix()] == base.load(package / "checksums.json")["verification/registered_review.json"]
    later = {row["id"]: row for row in base.load(path)["records"]
             if row["file_path"] == prior.ARCHIVE and row["block"] == block}
    assert later.keys() == {row["id"] for row in records}
    merged = []
    for original in records:
        row = later[original["id"]]
        ref = row["registered_reference"]
        if block == 192:
            assert row["native_command_word"] == original["native_command_word"] == 0x4000
            source = row["source_reference"]
            assert source["raw_hex"] == bytes([original["selector"]]).hex() + original["source_reference"]["exact_body_hex"]
            assert source["offset"] == original["source_reference"]["offset"]
            ref = ref | dict(block_sha256=live_hash, exact_command_hex=ref["complete_command_hex"])
            row = original | dict(registered_reference=ref, source_meaning=row["source_meaning"],
                                   localization_note=row["localization_note"], review=row["review"])
        assert ref["block_sha256"] == live_hash
        merged.append(row)
    return merged, path


native_binding = prior.prior.binding.copy()
bind_source = checked_text(prior.prior.bind_source, {
    'in (0x4000, 0x4100, 0x2100)': 'in (0x4000, 0x4100, 0x2100, 0x2200)',
})
exec(compile(bind_source, __file__ + "::complete-native-choice-binding", "exec"), native_binding)
scope = vars(prior) | globals()
source = checked_text(getsource(prior.main), {
    'prior.binding["bind_block"]': 'native_binding["bind_block"]',
    "            assert records and leads, block":
        "            owner = reference\n"
        "            if block in OVERLAYS:\n"
        "                records, owner = overlay(block, records, native.digest(banks[1][block]), reviews)\n"
        "            assert records and leads, block",
    "row.update(prior_registered_review=reference.as_posix()": "row.update(prior_registered_review=owner.as_posix()",
    "len(groups) == 15 and wraps == 20": "len(groups) == 17 and wraps == 22",
})
exec(compile(source, __file__ + "::clean-current-binding", "exec"), scope)


if __name__ == "__main__":
    scope["main"]()
