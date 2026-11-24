"""Tie all eight prepared story packets to the installed editorial decisions."""

from collections import Counter
from pathlib import Path

from dk4tool.formats.ilnk import IlnkContainer
from scripts import reconcile_deck_skill_acceptance_20261124 as current
from scripts.stage_cartridge_title_20261123 import CLEAN, GATES, NdsImage, REGISTRY, digest, read, reference, sha256, write

INTAKE = Path("translations/editorial_checkpoints/palace_and_london_20261122")
OUT = current.OUT.with_name("original_story_packets_current_20261124.json")
PACKETS = (
    ("rafael_north_sea_paired_source.json", 0, 49, 61, "north_sea_and_hodram_reconciliation"),
    ("rafael_B84_training_pairs.json", 0, 84, 131, "rafael_B84_training"),
    ("hodram_pirates_paired_source.json", 1, 17, 73, "hodram_and_lil_followups"),
    ("hodram_shared_celebration_paired_source.json", 1, 66, 13, "north_sea_and_hodram_reconciliation"),
    ("hodram_cristina_recruitment_paired_source.json", 1, 85, 56, "hodram_and_lil_followups"),
    ("lil_rumor_paired_source.json", 2, 26, 111, "hodram_and_lil_followups"),
    ("lil_rafael_introduction_paired_source.json", 2, 133, 50, "hodram_and_lil_followups"),
    ("maria_B116_paired_source.json", 3, 116, 26, "rafael_athens_and_maria_crew"),
)


def package(tag):
    root = Path("releases") / f"all_routes_editorial_20261122_{tag}_candidate"
    key = "verification/registered_review.json"
    path = root / key
    assert digest(path) == read(root / "checksums.json")[key]
    review = read(path)
    assert review["translation_policy"] == "natural-dialogue-v2"
    return path, review


def command(block, at, payload):
    body = bytes.fromhex(payload)
    assert block[at:at + len(body)] == body, at
    return body


def retained_pages(tag, review, block_number, block):
    if tag == "rafael_B84_training":
        records = review["unchanged_FE"]["records"]
        proof = None
        field = "owner"
    elif block_number == 116:
        receipt = review["retained_modal_pages"]
        path = Path(receipt["exact_panel_proof"])
        assert digest(path) == receipt["sha256"]
        records = [r for r in read(path)["records"] if r["block"] == block_number]
        proof = reference(path)
        field = "id"
    else:
        return None
    by_owner = {}
    for row in records:
        if row["second_page"]:
            group = [r for r in records if r[field] == row[field]]
            assert len(group) == 2 and sum(r["second_page"] for r in group) == 1
            result = []
            for page in group:
                at = page["stored_offset"]
                stored = command(block, at, page["exact_command_hex"])
                assert stored[5] == 0xFE and stored.endswith(b"\0")
                assert page["row_membership"]["complete_glyph_row_membership_exact"]
                result.append(dict(offset=at, exact_hex=stored.hex(), second_page=page["second_page"]))
            by_owner[row[field]] = result
    assert len(by_owner) == 2
    return dict(original_paired_pages_by_owner=by_owner, earlier_native_proof=proof)


def audit_packet(packet, route, block_number, count, tag, clean, image, clean_sha):
    path = INTAKE / packet
    report = read(path)
    assert report["clean_sha256"] == clean_sha
    body = report["groups"][0] if "groups" in report else report
    asset = f"/data/SC{route}.DK4"
    assert (body["file_path"], body["block"]) == (asset, block_number)
    clean_archive, current_archive = (rom.read_file(asset) for rom in (clean, image))
    original, final = [IlnkContainer.parse(blob).blocks[block_number] for blob in (clean_archive, current_archive)]
    original_sha, final_sha = (sha256(content).hexdigest() for content in (original, final))
    assert sha256(clean_archive).hexdigest() == body["source_archive_sha256"]
    assert original_sha == body["source_block_sha256"]
    review_path, review = package(tag)
    rows = [r for r in review["records"] if (r["file_path"], r["block"]) == (asset, block_number)]
    if (route, block_number) == (2, 133):
        choice = review["retained_native_controls"]["original_choice"]
        assert choice["preserved_relative_branches"] and choice["both_branches_observed"]
        assert [row["slot"] for row in choice["captions"]] == [0, 1]
        rows += choice["captions"]
    decisions = {row["id"]: row for row in rows}
    assert len(body["records"]) == len(rows) == len(decisions) == count
    keys = []
    for pair in body["records"]:
        ident = pair.get("id")
        if ident is None:
            ident = f"DK4_MES_B{block_number}_R{pair['source_record_index']:04d}"
        review_row = decisions[ident]
        assert set(review_row["review"]) == set(GATES) and all(review_row["review"].values())
        assert review_row["localization_note"] and review_row["english"].strip()
        at = pair["source_command_offset"]
        if "source_command_hex" in pair:
            source_command = pair["source_command_hex"]
            assert review_row.get("source_command_hex", review_row.get("source_reference", {}).get("exact_command_hex")) == source_command
        else:
            registered_source = review_row["source_reference"]
            assert registered_source["command_offset"] == at and registered_source["offset"] == pair["source_offset"]
            assert registered_source["exact_body_hex"] == pair["source_body_hex"]
            source_command = registered_source["exact_command_hex"]
        command(original, at, source_command)
        installed = review_row["registered_reference"]
        assert installed["block_sha256"] == final_sha
        start = installed["command_offset"]
        stored = command(final, start, installed["exact_command_hex"])
        if "native_command_word" in pair:
            assert int.from_bytes(stored[:2], "little") == pair["native_command_word"]
        keys.append(dict(id=ident, decision=review_row["decision"], source_command_offset=at, installed_command_offset=start,
                         draft_packet_predecessor_offset=pair["current_command_offset"],
                         installed_sha256=sha256(stored).hexdigest()))
    assert len({r["id"] for r in keys}) == count
    return dict(packet=reference(path), editorial_review=reference(review_path), asset=asset, block=block_number,
        original_block_sha256=original_sha, installed_block_sha256=final_sha, prepared_texts=count,
        dispositions=Counter(row["decision"] for row in keys), exact_texts=keys,
        retained_tutorial_continuations=retained_pages(tag, review, block_number, final))


def main():
    release = read(current.current.RELEASE)
    acceptance = read(current.OUT)
    assert digest(REGISTRY) == release["registry_sha256"]
    assert digest(CLEAN) == release["clean_input_sha256"]
    assert digest(release["candidate"]) == release["candidate_sha256"] == acceptance["candidate_sha256"]
    clean, image = map(NdsImage.open, (CLEAN, release["candidate"]))
    results = [audit_packet(*row, clean, image, release["clean_input_sha256"]) for row in PACKETS]
    assert len(results) == 8 and sum(row["prepared_texts"] for row in results) == 521
    ledger = Path(acceptance["coverage"]["priority_story_decisions"]["ledger"]["path"])
    assert digest(ledger) == acceptance["coverage"]["priority_story_decisions"]["ledger"]["sha256"]
    priority = {(row["file_path"], row["block"], row["id"]) for row in read(ledger)["records"]}
    prepared = {(group["asset"], group["block"], row["id"]) for group in results for row in group["exact_texts"]}
    assert len(prepared) == 521 and len(priority) == 416 and len(priority & prepared) == 205
    write(OUT, dict(candidate_sha256=release["candidate_sha256"], current_acceptance=reference(current.OUT),
        prepared_story_texts=521, priority_story_decisions=416, overlap=len(priority & prepared),
        unique_priority_and_prepared_story_positions=len(priority | prepared),
        all_source_current_installed_and_review_gates_bound=True, packets=results,
        new_editorial_credit=0, ordinary_gameplay_added=False))
    print("All 521 prepared texts match their exact installed decisions, including two choice captions and four two-page tutorial notices.")


if __name__ == "__main__":
    main()
