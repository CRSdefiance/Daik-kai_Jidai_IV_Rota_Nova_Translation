"""Carry the three unedited archives and their draft dialogue onto Rafael's registered successor."""

from pathlib import Path

from scripts import prepare_mosque_temple_shipyard_20261118 as original
from scripts import register_rafael_mosque_20261118 as latest
from scripts import review_london_guild_assignments_20261118 as history_index

base, native = latest.base, latest.native
SOURCE = original.ROOT / "paired_source.json"
SOURCE_SHA = "76dede3dafcc34f418b14147aa42ffa03c26bc81426924cf5635ef0473be2c3e"
OUT = original.ROOT / "remaining_three_routes_with_drafts_v1.json"
HODRAM_DRAFT = Path("docs/editorial_hodram_temple_wolf_draft_20261118.md")
LIL_MARIA_DRAFT = Path("docs/editorial_lil_maria_supply_shipyard_draft_20261118.md")
HISTORY = (
    Path("translations/hodram_B301_B310_integrated_final_review_v1.json"),
    Path("translations/lil278_B299_B311_integrated_final_review_v1.json"),
    Path("translations/maria359_B253_B274_integrated_final_review_v1.json"),
)


def proposals():
    result = {}
    for path in (HODRAM_DRAFT, LIL_MARIA_DRAFT):
        route = 1
        for line in path.read_text(encoding="utf-8").splitlines():
            if line == "## Proposed Lil variants":
                route = 2
            elif line == "## Proposed Maria variants":
                route = 3
            elif "|" in line:
                ordinal, english = line.split("|", 1)
                key = route, int(ordinal)
                assert key not in result and english.isascii() and english.strip() == english
                result[key] = english
    return result


def main():
    assert not OUT.exists() and base.digest(SOURCE) == SOURCE_SHA
    paired, release = map(base.load, (SOURCE, latest.RELEASE))
    assert paired["candidate_sha256"] == release["predecessor"]["candidate_sha256"]
    assert base.digest(base.REGISTRY) == release["registry_sha256"]
    assert base.digest(latest.ROM) == release["candidate_sha256"]
    assert release["changed_internal_files"] == ["/data/SC0.DK4"]
    images = [base.NdsImage.open(rom) for rom in (latest.parent.ROM, latest.ROM)]
    assert base.digest(latest.parent.ROM) == paired["candidate_sha256"]
    assert all(images[0].read_file(resource) == images[1].read_file(resource)
               for resource in (native.ARM, "/GRP/KANJI.FNT", "/COMMON/MESFILE.DK4"))
    archive_hashes = {}
    for route in (1, 2, 3):
        path = f"/data/SC{route}.DK4"
        old, new = [image.read_file(path) for image in images]
        assert new == old
        archive_hashes[path] = native.digest(new)
        assert archive_hashes[path] == release[f"target_SC{route}_sha256"]
    history_rows = [history_index.index_history(path) for path in HISTORY]
    suggested = proposals()
    ordinals, seen, groups = {}, set(), []
    for group in paired["groups"]:
        route, path, block = group["route"], group["file_path"], group["block"]
        rows = []
        for row in group["records"]:
            key = row["native_command_word"], row["Japanese"]
            if key not in ordinals:
                ordinals[key] = len(ordinals) + 1
            if route == 0:
                continue
            history = history_rows[route - 1][block, row["source_offset"]]
            selector = row["selector"]
            prefix = bytes([selector]).hex() if row["native_command_word"] == 0x4000 else ""
            assert history["source_hex"] == prefix + row["source_body_hex"]
            ordinal = ordinals[key]
            draft = suggested.get((route, ordinal))
            if draft:
                assert draft != " ".join(row["current_English"].split())
                seen.add((route, ordinal))
            rows.append(row | dict(packet_ordinal=ordinal, id=history["id"],
                speaker=history["speaker"], earlier_gloss=history["source_meaning"],
                earlier_exchange_context=history["context"], proposed_English=draft,
                review_pending=True))
        if rows:
            assert group["current_archive_sha256"] == archive_hashes[path]
            groups.append(group | {"records": rows})
    assert seen == suggested.keys() and len(seen) == 105
    assert len(groups) == 19 and sum(len(group["records"]) for group in groups) == 351
    base.save(OUT, paired | dict(groups=groups, profile=release["profile"],
        candidate_sha256=release["candidate_sha256"], verified_unchanged_archive_sha256=archive_hashes,
        previous_packet=dict(path=str(SOURCE), sha256=SOURCE_SHA),
        draft_sources={str(path): base.digest(path) for path in (HODRAM_DRAFT, LIL_MARIA_DRAFT)},
        editorial_review_pending=True, proposed_changes=len(seen), new_coverage_credit=0))
    print("Carried 351 exact records and 105 wording proposals forward on the registered candidate.")
    print(base.digest(OUT))


if __name__ == "__main__":
    main()
